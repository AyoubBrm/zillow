"""Category repository with tree queries."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category, CategoryType
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entities with hierarchy support."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Category, session)

    async def get_for_org(
        self, org_id: UUID, *, include_system: bool = True
    ) -> Sequence[Category]:
        """Fetch all categories visible to an organisation.

        Returns both organisation-specific and system-wide categories.
        """
        conditions = [Category.organization_id == org_id]
        if include_system:
            conditions = [
                or_(
                    Category.organization_id == org_id,
                    Category.is_system == True,  # noqa: E712
                )
            ]
        stmt = (
            select(Category)
            .where(*conditions, Category.is_active == True)  # noqa: E712
            .order_by(Category.sort_order, Category.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_roots(
        self, org_id: UUID, *, include_system: bool = True
    ) -> Sequence[Category]:
        """Fetch only top-level (root) categories."""
        conditions = [Category.parent_id == None]  # noqa: E711
        if include_system:
            conditions.append(
                or_(
                    Category.organization_id == org_id,
                    Category.is_system == True,  # noqa: E712
                )
            )
        else:
            conditions.append(Category.organization_id == org_id)
        stmt = (
            select(Category)
            .where(*conditions, Category.is_active == True)  # noqa: E712
            .order_by(Category.sort_order, Category.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_name(
        self, name: str, org_id: UUID | None = None
    ) -> Category | None:
        """Find a category by name (case-insensitive)."""
        stmt = select(Category).where(Category.name.ilike(name))
        if org_id is not None:
            stmt = stmt.where(
                or_(
                    Category.organization_id == org_id,
                    Category.is_system == True,  # noqa: E712
                )
            )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_type(
        self, cat_type: CategoryType, org_id: UUID | None = None
    ) -> Sequence[Category]:
        """Return all categories of a given type."""
        stmt = select(Category).where(
            Category.type == cat_type,
            Category.is_active == True,  # noqa: E712
        )
        if org_id is not None:
            stmt = stmt.where(
                or_(
                    Category.organization_id == org_id,
                    Category.is_system == True,  # noqa: E712
                )
            )
        stmt = stmt.order_by(Category.sort_order, Category.name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_children(self, parent_id: UUID) -> Sequence[Category]:
        """Return direct children of a category."""
        stmt = (
            select(Category)
            .where(Category.parent_id == parent_id, Category.is_active == True)  # noqa: E712
            .order_by(Category.sort_order, Category.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def system_categories_exist(self) -> bool:
        """Check if system categories have been seeded."""
        stmt = select(func.count(Category.id)).where(Category.is_system == True)  # noqa: E712
        from sqlalchemy import func

        stmt = select(func.count(Category.id)).where(Category.is_system == True)  # noqa: E712
        result = await self.session.execute(stmt)
        return (result.scalar_one() or 0) > 0
