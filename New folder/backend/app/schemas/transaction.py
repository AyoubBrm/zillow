"""Transaction Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.transaction import TransactionSource, TransactionStatus, TransactionType


class TransactionCreate(BaseModel):
    """Payload for creating a transaction."""

    date: date
    amount: float
    currency: str = "USD"
    description: str = Field(min_length=1)
    merchant_name: str | None = None
    reference: str | None = None
    type: TransactionType
    source: TransactionSource = TransactionSource.MANUAL
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)
    category_ids: list[UUID] = Field(default_factory=list)


class TransactionUpdate(BaseModel):
    """Partial update payload for a transaction."""

    date: date | None = None
    amount: float | None = None
    currency: str | None = None
    description: str | None = None
    merchant_name: str | None = None
    reference: str | None = None
    type: TransactionType | None = None
    status: TransactionStatus | None = None
    notes: str | None = None
    tags: list[str] | None = None
    category_ids: list[UUID] | None = None


class CategoryLink(BaseModel):
    """Nested category reference in a transaction response."""

    model_config = {"from_attributes": True}

    category_id: UUID
    category_name: str | None = None
    confidence: float | None = None
    is_primary: bool = True


class TransactionResponse(BaseModel):
    """Transaction detail response."""

    model_config = {"from_attributes": True}

    id: UUID
    organization_id: UUID
    date: date
    amount: float
    currency: str
    description: str
    merchant_name: str | None = None
    reference: str | None = None
    type: TransactionType
    source: TransactionSource
    status: TransactionStatus
    notes: str | None = None
    tags: list[str]
    ai_category_suggestion: str | None = None
    ai_confidence: float | None = None
    is_duplicate: bool
    categories: list[CategoryLink] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class TransactionFilter(BaseModel):
    """Filter/search parameters for listing transactions."""

    search: str | None = None
    type: TransactionType | None = None
    status: TransactionStatus | None = None
    source: TransactionSource | None = None
    category_id: UUID | None = None
    date_from: date | None = None
    date_to: date | None = None
    amount_min: float | None = None
    amount_max: float | None = None
    merchant_name: str | None = None
    is_duplicate: bool | None = None


class TransactionImportResponse(BaseModel):
    """Result summary after CSV / Excel import."""

    total_rows: int
    imported: int
    duplicates_skipped: int
    errors: int
    error_details: list[str] = Field(default_factory=list)
