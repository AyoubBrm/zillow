"""Organisation service — CRUD + member management."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.models.organization import Organization, OrganizationMember, OrgRole
from app.repositories.organization_repo import OrganizationRepository
from app.repositories.user_repo import UserRepository
from app.schemas.organization import MemberCreate, OrgCreate, OrgUpdate


class OrganizationService:
    """Business logic for organisations and their members."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.org_repo = OrganizationRepository(session)
        self.user_repo = UserRepository(session)

    # ── Org CRUD ─────────────────────────────────────────────────────

    async def create_org(self, payload: OrgCreate, owner_id: UUID) -> Organization:
        """Create a new organisation and assign the creator as owner.

        Raises
        ------
        ConflictException
            If the slug is already in use.
        """
        if await self.org_repo.slug_exists(payload.slug):
            raise ConflictException(f"Slug '{payload.slug}' is already taken.")

        org = await self.org_repo.create(payload.model_dump())
        await self.org_repo.add_member(org.id, owner_id, role=OrgRole.OWNER)
        return org

    async def get_org(self, org_id: UUID) -> Organization:
        """Fetch an organisation by ID.

        Raises
        ------
        NotFoundException
            If the organisation does not exist.
        """
        org = await self.org_repo.get(org_id)
        if org is None:
            raise NotFoundException("Organisation not found.")
        return org

    async def update_org(self, org_id: UUID, payload: OrgUpdate) -> Organization:
        """Update organisation details.

        Raises
        ------
        NotFoundException
            If the organisation does not exist.
        """
        update_data = payload.model_dump(exclude_unset=True)
        org = await self.org_repo.update(org_id, update_data)
        if org is None:
            raise NotFoundException("Organisation not found.")
        return org

    async def delete_org(self, org_id: UUID) -> bool:
        """Soft-delete an organisation."""
        org = await self.org_repo.update(org_id, {"is_active": False})
        return org is not None

    async def list_user_orgs(self, user_id: UUID) -> list[Organization]:
        """List all orgs a user belongs to."""
        return await self.org_repo.get_user_organizations(user_id)

    # ── Member management ────────────────────────────────────────────

    async def add_member(
        self, org_id: UUID, payload: MemberCreate
    ) -> OrganizationMember:
        """Add a member to the organisation by user_id or email.

        Raises
        ------
        NotFoundException
            If the user is not found.
        ConflictException
            If the user is already a member.
        """
        user_id = payload.user_id
        if user_id is None and payload.email:
            user = await self.user_repo.get_by_email(payload.email)
            if user is None:
                raise NotFoundException(f"No user found with email '{payload.email}'.")
            user_id = user.id
        if user_id is None:
            raise NotFoundException("Either user_id or email must be provided.")

        existing = await self.org_repo.get_member(org_id, user_id)
        if existing is not None and existing.is_active:
            raise ConflictException("User is already a member of this organisation.")
        # Re-activate if previously removed
        if existing is not None and not existing.is_active:
            existing.is_active = True
            existing.role = payload.role
            await self.session.flush()
            await self.session.refresh(existing)
            return existing

        return await self.org_repo.add_member(org_id, user_id, role=payload.role)

    async def list_members(self, org_id: UUID) -> list[OrganizationMember]:
        """List active members of an organisation."""
        return await self.org_repo.get_members(org_id)

    async def update_member_role(
        self, org_id: UUID, target_user_id: UUID, new_role: OrgRole
    ) -> OrganizationMember:
        """Change a member's role.

        Raises
        ------
        NotFoundException
            If the member is not found.
        ForbiddenException
            If trying to change the owner's role.
        """
        member = await self.org_repo.get_member(org_id, target_user_id)
        if member is None:
            raise NotFoundException("Member not found.")
        if member.role == OrgRole.OWNER and new_role != OrgRole.OWNER:
            raise ForbiddenException("Cannot change the owner's role directly.")
        updated = await self.org_repo.update_member_role(org_id, target_user_id, new_role)
        if updated is None:
            raise NotFoundException("Member not found.")
        return updated

    async def remove_member(self, org_id: UUID, target_user_id: UUID) -> bool:
        """Remove (deactivate) a member from the organisation.

        Raises
        ------
        ForbiddenException
            If trying to remove the owner.
        """
        member = await self.org_repo.get_member(org_id, target_user_id)
        if member is None:
            raise NotFoundException("Member not found.")
        if member.role == OrgRole.OWNER:
            raise ForbiddenException("Cannot remove the organisation owner.")
        return await self.org_repo.remove_member(org_id, target_user_id)
