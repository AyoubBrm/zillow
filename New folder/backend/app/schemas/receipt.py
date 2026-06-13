"""Receipt Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.receipt import ReceiptStatus


class ReceiptResponse(BaseModel):
    """Receipt detail response."""

    model_config = {"from_attributes": True}

    id: UUID
    organization_id: UUID
    file_name: str
    file_size: int | None = None
    mime_type: str | None = None
    status: ReceiptStatus
    extracted_merchant: str | None = None
    extracted_amount: float | None = None
    extracted_date: str | None = None
    extracted_data: dict
    created_at: datetime
    updated_at: datetime


class ReceiptMatchRequest(BaseModel):
    """Payload for manually matching a receipt to a transaction."""

    receipt_id: UUID
    transaction_id: UUID
    is_confirmed: bool = True
