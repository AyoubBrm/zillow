"""User service — profile management."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    """Business logic for user profile operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session)

    async def get_user(self, user_id: UUID) -> User:
        """Fetch a user by ID.

        Raises
        ------
        NotFoundException
            If the user does not exist.
        """
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFoundException("User not found.")
        return user

    async def update_profile(self, user_id: UUID, payload: UserUpdate) -> User:
        """Update the current user's profile fields.

        Only non-None fields in the payload are applied.

        Raises
        ------
        NotFoundException
            If the user does not exist.
        """
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_user(user_id)
        user = await self.repo.update(user_id, update_data)
        if user is None:
            raise NotFoundException("User not found.")
        return user

    async def deactivate_user(self, user_id: UUID) -> User:
        """Soft-delete a user account."""
        user = await self.repo.update(user_id, {"is_active": False})
        if user is None:
            raise NotFoundException("User not found.")
        return user
