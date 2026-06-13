"""RBAC permission helpers.

Provides a ``require_role`` dependency factory that ensures the caller
has a sufficient role within the current organisation context.

Usage in a route::

    @router.post("/something")
    async def do_something(
        _: None = Depends(require_role(OrgRole.ADMIN)),
    ):
        ...
"""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.organization import OrganizationMember, OrgRole


class Permission(str, Enum):
    """Fine-grained permissions (optional future use)."""

    MANAGE_MEMBERS = "manage_members"
    MANAGE_BILLING = "manage_billing"
    MANAGE_TRANSACTIONS = "manage_transactions"
    VIEW_REPORTS = "view_reports"
    MANAGE_SETTINGS = "manage_settings"


# Role → permitted roles mapping (higher roles inherit lower)
_ROLE_HIERARCHY: dict[OrgRole, int] = {
    OrgRole.VIEWER: 0,
    OrgRole.MEMBER: 1,
    OrgRole.ACCOUNTANT: 2,
    OrgRole.ADMIN: 3,
    OrgRole.OWNER: 4,
}


def _role_sufficient(required: OrgRole, actual: OrgRole) -> bool:
    """Return True if *actual* is at least as powerful as *required*."""
    return _ROLE_HIERARCHY.get(actual, -1) >= _ROLE_HIERARCHY.get(required, 999)


async def get_member_role(
    user_id: UUID,
    org_id: UUID,
    session: AsyncSession,
) -> OrgRole:
    """Fetch the user's role within the organisation, or raise."""
    stmt = select(OrganizationMember).where(
        OrganizationMember.user_id == user_id,
        OrganizationMember.organization_id == org_id,
        OrganizationMember.is_active == True,  # noqa: E712
    )
    result = await session.execute(stmt)
    member = result.scalar_one_or_none()
    if member is None:
        raise NotFoundException("You are not a member of this organisation.")
    return member.role  # type: ignore[return-value]


def require_role(minimum_role: OrgRole) -> Any:
    """Return a FastAPI dependency that enforces a minimum org role.

    The dependency expects ``current_user`` and ``org_id`` to be present
    in the route signature via other dependencies.
    """

    async def _checker(
        current_user_id: UUID,
        org_id: UUID,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        actual_role = await get_member_role(current_user_id, org_id, session)
        if not _role_sufficient(minimum_role, actual_role):
            raise ForbiddenException(
                f"This action requires at least the '{minimum_role.value}' role."
            )

    return _checker
