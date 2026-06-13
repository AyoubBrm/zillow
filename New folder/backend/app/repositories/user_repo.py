"""User repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by email address (case-insensitive)."""
        stmt = select(User).where(User.email == email.lower())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Return True if the email is already registered."""
        return (await self.get_by_email(email)) is not None

    async def set_email_verified(self, user: User) -> User:
        """Mark a user's email as verified."""
        user.email_verified = True
        await self.session.flush()
        await self.session.refresh(user)
        return user
