"""Organisation repository with member management."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.organization import Organization, OrganizationMember, OrgRole
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """Repository for Organisation entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Organization, session)

    async def get_by_slug(self, slug: str) -> Organization | None:
        """Find an organisation by its URL slug."""
        stmt = select(Organization).where(Organization.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str) -> bool:
        """Return True if the slug is taken."""
        return (await self.get_by_slug(slug)) is not None

    async def get_user_organizations(self, user_id: UUID) -> list[Organization]:
        """Return all organisations the user is an active member of."""
        stmt = (
            select(Organization)
            .join(OrganizationMember)
            .where(
                OrganizationMember.user_id == user_id,
                OrganizationMember.is_active == True,  # noqa: E712
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── Member management ────────────────────────────────────────────

    async def add_member(
        self,
        org_id: UUID,
        user_id: UUID,
        role: OrgRole = OrgRole.MEMBER,
    ) -> OrganizationMember:
        """Add a user as a member of the organisation."""
        member = OrganizationMember(
            organization_id=org_id,
            user_id=user_id,
            role=role,
        )
        self.session.add(member)
        await self.session.flush()
        await self.session.refresh(member)
        return member

    async def get_member(
        self, org_id: UUID, user_id: UUID
    ) -> OrganizationMember | None:
        """Fetch a specific membership record."""
        stmt = select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_members(self, org_id: UUID) -> list[OrganizationMember]:
        """List all active members of an organisation."""
        stmt = (
            select(OrganizationMember)
            .options(selectinload(OrganizationMember.user))
            .where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.is_active == True,  # noqa: E712
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_member_role(
        self, org_id: UUID, user_id: UUID, role: OrgRole
    ) -> OrganizationMember | None:
        """Change a member's role."""
        member = await self.get_member(org_id, user_id)
        if member is None:
            return None
        member.role = role
        await self.session.flush()
        await self.session.refresh(member)
        return member

    async def remove_member(self, org_id: UUID, user_id: UUID) -> bool:
        """Soft-delete: deactivate a member."""
        member = await self.get_member(org_id, user_id)
        if member is None:
            return False
        member.is_active = False
        await self.session.flush()
        return True
