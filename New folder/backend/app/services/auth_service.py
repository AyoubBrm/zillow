"""Authentication service — register, login, refresh, password reset."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.organization import OrgRole
from app.repositories.organization_repo import OrganizationRepository
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

settings = get_settings()


class AuthService:
    """Handles registration, login, token refresh, and password reset."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.org_repo = OrganizationRepository(session)

    # ── Register ─────────────────────────────────────────────────────

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        """Create a new user account and optionally an organisation.

        Returns a token pair so the user is immediately logged in.

        Raises
        ------
        ConflictException
            If the email is already registered.
        """
        email = payload.email.lower()
        if await self.user_repo.email_exists(email):
            raise ConflictException("An account with this email already exists.")

        user = await self.user_repo.create({
            "email": email,
            "password_hash": hash_password(payload.password),
            "full_name": payload.full_name,
            "phone": payload.phone,
        })

        # If an org name was provided, create the org and make the user the owner
        if payload.org_name:
            slug = payload.org_name.lower().replace(" ", "-")
            # Ensure slug uniqueness by appending user id fragment
            if await self.org_repo.slug_exists(slug):
                slug = f"{slug}-{str(user.id)[:8]}"
            org = await self.org_repo.create({
                "name": payload.org_name,
                "slug": slug,
            })
            await self.org_repo.add_member(org.id, user.id, role=OrgRole.OWNER)

        return self._build_tokens(user.id)

    # ── Login ────────────────────────────────────────────────────────

    async def login(self, payload: LoginRequest) -> TokenResponse:
        """Authenticate with email + password.

        Raises
        ------
        UnauthorizedException
            If credentials are invalid.
        """
        user = await self.user_repo.get_by_email(payload.email.lower())
        if user is None or not verify_password(payload.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedException("This account has been deactivated.")
        return self._build_tokens(user.id)

    # ── Refresh ──────────────────────────────────────────────────────

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Issue new tokens from a valid refresh token.

        Raises
        ------
        UnauthorizedException
            If the refresh token is invalid / expired.
        """
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException("The provided token is not a refresh token.")
        user_id = UUID(payload["sub"])
        user = await self.user_repo.get(user_id)
        if user is None or not user.is_active:
            raise UnauthorizedException("User not found or inactive.")
        return self._build_tokens(user_id)

    # ── Password reset (placeholder — needs email service) ───────────

    async def request_password_reset(self, email: str) -> None:
        """Initiate a password reset flow.

        In a production system this would send an email with a one-time
        link / token.  For the MVP we just verify the user exists.
        """
        user = await self.user_repo.get_by_email(email.lower())
        if user is None:
            # Return silently to prevent email enumeration
            return
        # TODO: integrate email service to send reset link
        # For now, we log that a reset was requested
        return

    # ── Helpers ──────────────────────────────────────────────────────

    def _build_tokens(self, user_id: UUID) -> TokenResponse:
        """Create an access + refresh token pair."""
        access = create_access_token({"sub": str(user_id)})
        refresh = create_refresh_token({"sub": str(user_id)})
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
