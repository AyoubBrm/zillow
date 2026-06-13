"""Transaction service — CRUD, CSV/Excel import, duplicate detection."""

from __future__ import annotations

import hashlib
import io
from datetime import date
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ValidationException
from app.models.transaction import Transaction, TransactionSource, TransactionStatus, TransactionType
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionFilter,
    TransactionImportResponse,
    TransactionUpdate,
)


class TransactionService:
    """Business logic for financial transactions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TransactionRepository(session)

    # ── CRUD ─────────────────────────────────────────────────────────

    async def create_transaction(
        self, org_id: UUID, payload: TransactionCreate, *, user_id: UUID | None = None
    ) -> Transaction:
        """Create a single transaction with duplicate checking."""
        fingerprint = TransactionRepository.compute_hash(
            payload.date, payload.amount, payload.description, payload.merchant_name
        )
        is_dup = (await self.repo.find_by_hash(org_id, fingerprint)) is not None

        data: dict[str, Any] = {
            "organization_id": org_id,
            "date": payload.date,
            "amount": payload.amount,
            "currency": payload.currency,
            "description": payload.description,
            "merchant_name": payload.merchant_name,
            "reference": payload.reference,
            "type": payload.type,
            "source": payload.source,
            "notes": payload.notes,
            "tags": payload.tags,
            "hash_fingerprint": fingerprint,
            "is_duplicate": is_dup,
            "created_by": user_id,
        }
        txn = await self.repo.create(data)

        if payload.category_ids:
            await self.repo.set_categories(txn.id, payload.category_ids)

        return txn

    async def get_transaction(self, org_id: UUID, txn_id: UUID) -> Transaction:
        """Fetch a single transaction.

        Raises
        ------
        NotFoundException
            If the transaction does not exist in this org.
        """
        txn = await self.repo.get(txn_id, org_id=org_id)
        if txn is None:
            raise NotFoundException("Transaction not found.")
        return txn

    async def list_transactions(
        self,
        org_id: UUID,
        *,
        filters: TransactionFilter | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> tuple[Sequence[Transaction], int]:
        """Return a filtered, paginated list of transactions."""
        return await self.repo.get_filtered(
            org_id, filters=filters, offset=offset, limit=limit
        )

    async def update_transaction(
        self, org_id: UUID, txn_id: UUID, payload: TransactionUpdate
    ) -> Transaction:
        """Update a transaction's fields.

        Raises
        ------
        NotFoundException
            If the transaction does not exist.
        """
        update_data = payload.model_dump(exclude_unset=True)
        category_ids = update_data.pop("category_ids", None)

        txn = await self.repo.update(txn_id, update_data, org_id=org_id)
        if txn is None:
            raise NotFoundException("Transaction not found.")

        if category_ids is not None:
            await self.repo.set_categories(txn_id, category_ids)

        return txn

    async def delete_transaction(self, org_id: UUID, txn_id: UUID) -> bool:
        """Delete a transaction.

        Raises
        ------
        NotFoundException
            If the transaction does not exist.
        """
        deleted = await self.repo.delete(txn_id, org_id=org_id)
        if not deleted:
            raise NotFoundException("Transaction not found.")
        return True

    # ── CSV / Excel import ───────────────────────────────────────────

    async def import_transactions(
        self,
        org_id: UUID,
        rows: list[dict[str, Any]],
        *,
        user_id: UUID | None = None,
    ) -> TransactionImportResponse:
        """Import parsed transaction rows (from CSV/Excel).

        Each row dict must have at least: date, amount, description.
        Optional: merchant_name, type, reference, currency.

        Returns a summary of the import results.
        """
        imported = 0
        duplicates = 0
        errors = 0
        error_details: list[str] = []

        for idx, row in enumerate(rows, start=1):
            try:
                txn_date = self._parse_date(row.get("date"))
                amount = float(row.get("amount", 0))
                description = str(row.get("description", "")).strip()

                if not description:
                    error_details.append(f"Row {idx}: missing description")
                    errors += 1
                    continue

                merchant = row.get("merchant_name") or row.get("merchant") or None
                if merchant:
                    merchant = str(merchant).strip()

                txn_type_str = str(row.get("type", "expense")).lower().strip()
                if txn_type_str in ("income", "revenue", "credit"):
                    txn_type = TransactionType.INCOME
                elif txn_type_str in ("transfer",):
                    txn_type = TransactionType.TRANSFER
                else:
                    txn_type = TransactionType.EXPENSE

                currency = str(row.get("currency", "USD")).upper().strip()[:3]
                reference = row.get("reference")
                if reference:
                    reference = str(reference).strip()

                fingerprint = TransactionRepository.compute_hash(
                    txn_date, amount, description, merchant
                )

                existing = await self.repo.find_by_hash(org_id, fingerprint)
                if existing is not None:
                    duplicates += 1
                    continue

                await self.repo.create({
                    "organization_id": org_id,
                    "date": txn_date,
                    "amount": abs(amount),
                    "currency": currency,
                    "description": description,
                    "merchant_name": merchant,
                    "reference": reference,
                    "type": txn_type,
                    "source": TransactionSource.CSV_IMPORT,
                    "status": TransactionStatus.PENDING,
                    "hash_fingerprint": fingerprint,
                    "is_duplicate": False,
                    "created_by": user_id,
                })
                imported += 1

            except Exception as exc:
                error_details.append(f"Row {idx}: {str(exc)}")
                errors += 1

        return TransactionImportResponse(
            total_rows=len(rows),
            imported=imported,
            duplicates_skipped=duplicates,
            errors=errors,
            error_details=error_details[:50],  # Cap error messages
        )

    # ── Duplicates ───────────────────────────────────────────────────

    async def get_duplicates(self, org_id: UUID) -> Sequence[Transaction]:
        """Return all transactions flagged as potential duplicates."""
        return await self.repo.get_duplicates(org_id)

    # ── Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_date(value: Any) -> date:
        """Parse a date from various input formats."""
        if value is None:
            raise ValidationException("Date is required.")
        if isinstance(value, date):
            return value
        from dateutil import parser as dateutil_parser
        try:
            return dateutil_parser.parse(str(value)).date()
        except (ValueError, TypeError) as exc:
            raise ValidationException(f"Invalid date format: {value}") from exc
