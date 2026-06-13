"""Transaction repository with filtering, search, and statistics."""

from __future__ import annotations

import hashlib
from datetime import date
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import String, and_, cast, extract, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.transaction import (
    Transaction,
    TransactionCategory,
    TransactionSource,
    TransactionStatus,
    TransactionType,
)
from app.repositories.base import BaseRepository
from app.schemas.transaction import TransactionFilter


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction entities with advanced querying."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Transaction, session)

    # ── Filtered listing ─────────────────────────────────────────────

    async def get_filtered(
        self,
        org_id: UUID,
        *,
        filters: TransactionFilter | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> tuple[Sequence[Transaction], int]:
        """Return transactions matching the provided filter criteria."""
        where_clauses: list[Any] = [Transaction.organization_id == org_id]

        if filters:
            if filters.search:
                pattern = f"%{filters.search}%"
                where_clauses.append(
                    or_(
                        Transaction.description.ilike(pattern),
                        Transaction.merchant_name.ilike(pattern),
                        Transaction.reference.ilike(pattern),
                    )
                )
            if filters.type is not None:
                where_clauses.append(Transaction.type == filters.type)
            if filters.status is not None:
                where_clauses.append(Transaction.status == filters.status)
            if filters.source is not None:
                where_clauses.append(Transaction.source == filters.source)
            if filters.date_from is not None:
                where_clauses.append(Transaction.date >= filters.date_from)
            if filters.date_to is not None:
                where_clauses.append(Transaction.date <= filters.date_to)
            if filters.amount_min is not None:
                where_clauses.append(Transaction.amount >= filters.amount_min)
            if filters.amount_max is not None:
                where_clauses.append(Transaction.amount <= filters.amount_max)
            if filters.merchant_name is not None:
                where_clauses.append(
                    Transaction.merchant_name.ilike(f"%{filters.merchant_name}%")
                )
            if filters.is_duplicate is not None:
                where_clauses.append(Transaction.is_duplicate == filters.is_duplicate)
            if filters.category_id is not None:
                where_clauses.append(
                    Transaction.id.in_(
                        select(TransactionCategory.transaction_id).where(
                            TransactionCategory.category_id == filters.category_id
                        )
                    )
                )

        return await self.get_multi(
            org_id=None,  # already in where_clauses
            offset=offset,
            limit=limit,
            order_by=Transaction.date.desc(),
            filters=where_clauses,
        )

    # ── Duplicate detection ──────────────────────────────────────────

    @staticmethod
    def compute_hash(
        txn_date: date,
        amount: float,
        description: str,
        merchant_name: str | None = None,
    ) -> str:
        """Deterministic fingerprint for duplicate detection."""
        raw = f"{txn_date.isoformat()}|{amount:.2f}|{description.strip().lower()}"
        if merchant_name:
            raw += f"|{merchant_name.strip().lower()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    async def find_by_hash(self, org_id: UUID, fingerprint: str) -> Transaction | None:
        """Find an existing transaction with the same fingerprint."""
        stmt = select(Transaction).where(
            Transaction.organization_id == org_id,
            Transaction.hash_fingerprint == fingerprint,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_duplicates(self, org_id: UUID) -> Sequence[Transaction]:
        """Return all transactions flagged as duplicates."""
        stmt = (
            select(Transaction)
            .where(
                Transaction.organization_id == org_id,
                Transaction.is_duplicate == True,  # noqa: E712
            )
            .order_by(Transaction.date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # ── Statistics / aggregation ─────────────────────────────────────

    async def get_total_by_type(
        self,
        org_id: UUID,
        txn_type: TransactionType,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> float:
        """Sum transaction amounts for a given type within an optional date range."""
        stmt = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.organization_id == org_id,
            Transaction.type == txn_type,
        )
        if date_from:
            stmt = stmt.where(Transaction.date >= date_from)
        if date_to:
            stmt = stmt.where(Transaction.date <= date_to)
        result = await self.session.execute(stmt)
        return float(result.scalar_one())

    async def get_monthly_totals(
        self,
        org_id: UUID,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[dict[str, Any]]:
        """Return monthly income/expense totals.

        Returns a list of dicts: ``{"month": "2025-01", "type": "income", "total": 1234.56}``
        """
        month_expr = func.to_char(Transaction.date, "YYYY-MM")
        stmt = (
            select(
                month_expr.label("month"),
                Transaction.type,
                func.sum(Transaction.amount).label("total"),
            )
            .where(Transaction.organization_id == org_id)
            .group_by(month_expr, Transaction.type)
            .order_by(month_expr)
        )
        if date_from:
            stmt = stmt.where(Transaction.date >= date_from)
        if date_to:
            stmt = stmt.where(Transaction.date <= date_to)
        result = await self.session.execute(stmt)
        return [
            {"month": row.month, "type": row.type.value, "total": float(row.total)}
            for row in result.all()
        ]

    async def get_category_breakdown(
        self,
        org_id: UUID,
        txn_type: TransactionType,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[dict[str, Any]]:
        """Return spending or income totals grouped by category."""
        stmt = (
            select(
                Category.name.label("category"),
                func.sum(Transaction.amount).label("total"),
                func.count(Transaction.id).label("count"),
            )
            .join(TransactionCategory, TransactionCategory.transaction_id == Transaction.id)
            .join(Category, Category.id == TransactionCategory.category_id)
            .where(
                Transaction.organization_id == org_id,
                Transaction.type == txn_type,
                TransactionCategory.is_primary == True,  # noqa: E712
            )
            .group_by(Category.name)
            .order_by(func.sum(Transaction.amount).desc())
        )
        if date_from:
            stmt = stmt.where(Transaction.date >= date_from)
        if date_to:
            stmt = stmt.where(Transaction.date <= date_to)
        result = await self.session.execute(stmt)
        return [
            {"category": row.category, "total": float(row.total), "count": row.count}
            for row in result.all()
        ]

    async def count_pending(self, org_id: UUID) -> int:
        """Count transactions awaiting categorization."""
        stmt = select(func.count(Transaction.id)).where(
            Transaction.organization_id == org_id,
            Transaction.status == TransactionStatus.PENDING,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_by_date_range(
        self, org_id: UUID, date_from: date, date_to: date
    ) -> int:
        """Count transactions in a date range."""
        stmt = select(func.count(Transaction.id)).where(
            Transaction.organization_id == org_id,
            Transaction.date >= date_from,
            Transaction.date <= date_to,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    # ── Category linking ─────────────────────────────────────────────

    async def set_categories(
        self,
        transaction_id: UUID,
        category_ids: list[UUID],
        *,
        confidence: float | None = None,
    ) -> None:
        """Replace all category links for a transaction."""
        # Delete existing links
        from sqlalchemy import delete as sa_delete

        await self.session.execute(
            sa_delete(TransactionCategory).where(
                TransactionCategory.transaction_id == transaction_id
            )
        )
        # Create new links
        for idx, cat_id in enumerate(category_ids):
            link = TransactionCategory(
                transaction_id=transaction_id,
                category_id=cat_id,
                confidence=confidence,
                is_primary=(idx == 0),
            )
            self.session.add(link)
        await self.session.flush()
