"""User Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    """Public user representation."""

    model_config = {"from_attributes": True}

    id: UUID
    email: EmailStr
    full_name: str
    phone: str | None = None
    is_active: bool
    email_verified: bool
    avatar_url: str | None = None
    preferences: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    """Fields the user can update on their own profile."""

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = None
    avatar_url: str | None = None
    preferences: dict | None = None
