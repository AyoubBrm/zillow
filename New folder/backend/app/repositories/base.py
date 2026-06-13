"""Generic async CRUD repository with tenant filtering.

All entity-specific repositories extend ``BaseRepository`` and inherit
``get``, ``get_multi``, ``create``, ``update``, ``delete`` out of the box.
"""

from __future__ import annotations

from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic async repository providing standard CRUD operations.

    Parameters
    ----------
    model:
        The SQLAlchemy ORM model class this repository manages.
    """

    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    # ── Helpers ──────────────────────────────────────────────────────

    def _tenant_filter(self, stmt: Select, org_id: UUID | None) -> Select:
        """Apply organisation_id filter if the model has one."""
        if org_id is not None and hasattr(self.model, "organization_id"):
            stmt = stmt.where(self.model.organization_id == org_id)  # type: ignore[attr-defined]
        return stmt

    # ── Read ─────────────────────────────────────────────────────────

    async def get(self, entity_id: UUID, *, org_id: UUID | None = None) -> ModelT | None:
        """Fetch a single entity by primary key, optionally scoped to a tenant."""
        stmt = select(self.model).where(self.model.id == entity_id)  # type: ignore[attr-defined]
        stmt = self._tenant_filter(stmt, org_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        org_id: UUID | None = None,
        offset: int = 0,
        limit: int = 25,
        order_by: Any | None = None,
        filters: list[Any] | None = None,
    ) -> tuple[Sequence[ModelT], int]:
        """Return a paginated list and the total count.

        Parameters
        ----------
        org_id:
            Tenant scope (applied when the model has ``organization_id``).
        offset / limit:
            Pagination.
        order_by:
            SQLAlchemy order clause.  Defaults to ``created_at DESC``.
        filters:
            Extra SQLAlchemy ``where`` clauses.

        Returns
        -------
        (items, total)
        """
        base = select(self.model)
        base = self._tenant_filter(base, org_id)
        if filters:
            for f in filters:
                base = base.where(f)

        # Count
        count_stmt = select(func.count()).select_from(base.subquery())
        total = (await self.session.execute(count_stmt)).scalar_one()

        # Items
        if order_by is not None:
            base = base.order_by(order_by)
        elif hasattr(self.model, "created_at"):
            base = base.order_by(self.model.created_at.desc())  # type: ignore[attr-defined]
        base = base.offset(offset).limit(limit)
        result = await self.session.execute(base)
        items = result.scalars().all()

        return items, total

    # ── Create ───────────────────────────────────────────────────────

    async def create(self, data: dict[str, Any]) -> ModelT:
        """Insert a new row and return the ORM instance."""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    # ── Update ───────────────────────────────────────────────────────

    async def update(
        self,
        entity_id: UUID,
        data: dict[str, Any],
        *,
        org_id: UUID | None = None,
    ) -> ModelT | None:
        """Update a row by PK and return the refreshed instance."""
        instance = await self.get(entity_id, org_id=org_id)
        if instance is None:
            return None
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    # ── Delete ───────────────────────────────────────────────────────

    async def delete(self, entity_id: UUID, *, org_id: UUID | None = None) -> bool:
        """Delete by PK.  Returns ``True`` if the row existed."""
        stmt = delete(self.model).where(self.model.id == entity_id)  # type: ignore[attr-defined]
        if org_id is not None and hasattr(self.model, "organization_id"):
            stmt = stmt.where(self.model.organization_id == org_id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return (result.rowcount or 0) > 0
