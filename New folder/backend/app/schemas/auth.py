"""Authentication Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Payload for POST /auth/register."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    org_name: str | None = Field(
        default=None,
        description="Optional organisation name to create on signup.",
    )


class LoginRequest(BaseModel):
    """Payload for POST /auth/login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token pair returned after login / register / refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token lifetime in seconds")


class RefreshRequest(BaseModel):
    """Payload for POST /auth/refresh."""

    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Payload for POST /auth/password-reset."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Payload for POST /auth/password-reset/confirm."""

    token: str
    new_password: str = Field(min_length=8, max_length=128)
