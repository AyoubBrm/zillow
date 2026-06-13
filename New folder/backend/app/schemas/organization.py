"""Organisation Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.organization import OrgRole


class OrgCreate(BaseModel):
    """Payload for creating an organisation."""

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255, pattern=r"^[a-z0-9\-]+$")
    industry: str | None = None
    tax_id: str | None = None
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    default_currency: str = "USD"
    fiscal_year_start_month: int = Field(default=1, ge=1, le=12)


class OrgUpdate(BaseModel):
    """Partial update payload for an organisation."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    industry: str | None = None
    tax_id: str | None = None
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    logo_url: str | None = None
    default_currency: str | None = None
    fiscal_year_start_month: int | None = Field(default=None, ge=1, le=12)
    settings: dict | None = None


class OrgResponse(BaseModel):
    """Organisation detail response."""

    model_config = {"from_attributes": True}

    id: UUID
    name: str
    slug: str
    industry: str | None = None
    tax_id: str | None = None
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    logo_url: str | None = None
    default_currency: str
    fiscal_year_start_month: int
    is_active: bool
    settings: dict
    created_at: datetime
    updated_at: datetime


class MemberCreate(BaseModel):
    """Payload for inviting a user to an organisation."""

    user_id: UUID | None = None
    email: str | None = None
    role: OrgRole = OrgRole.MEMBER


class MemberResponse(BaseModel):
    """Organisation member detail."""

    model_config = {"from_attributes": True}

    id: UUID
    user_id: UUID
    organization_id: UUID
    role: OrgRole
    is_active: bool
    created_at: datetime
    # Denormalised for convenience
    user_email: str | None = None
    user_full_name: str | None = None
