"""Category Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.category import CategoryType


class CategoryCreate(BaseModel):
    """Payload for creating a category."""

    name: str = Field(min_length=1, max_length=255)
    code: str | None = None
    description: str | None = None
    type: CategoryType
    parent_id: UUID | None = None
    color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon: str | None = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    """Partial update payload for a category."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = None
    description: str | None = None
    type: CategoryType | None = None
    parent_id: UUID | None = None
    color: str | None = None
    icon: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    """Category detail response."""

    model_config = {"from_attributes": True}

    id: UUID
    organization_id: UUID | None = None
    parent_id: UUID | None = None
    name: str
    code: str | None = None
    description: str | None = None
    type: CategoryType
    color: str | None = None
    icon: str | None = None
    is_system: bool
    is_active: bool
    sort_order: int
    children: list["CategoryResponse"] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


# Allow forward-reference resolution
CategoryResponse.model_rebuild()
