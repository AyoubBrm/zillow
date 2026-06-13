"""Invoice Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.invoice import InvoiceStatus


class InvoiceItemCreate(BaseModel):
    """Single line item for invoice creation."""

    description: str = Field(min_length=1)
    quantity: float = Field(default=1, gt=0)
    unit_price: float = Field(gt=0)


class InvoiceCreate(BaseModel):
    """Payload for creating an invoice."""

    client_name: str = Field(min_length=1, max_length=255)
    client_email: EmailStr | None = None
    client_address: str | None = None
    issue_date: date
    due_date: date
    currency: str = "USD"
    tax_rate: float = Field(default=0, ge=0, le=100)
    notes: str | None = None
    terms: str | None = None
    items: list[InvoiceItemCreate] = Field(min_length=1)


class InvoiceUpdate(BaseModel):
    """Partial update payload for an invoice."""

    client_name: str | None = None
    client_email: EmailStr | None = None
    client_address: str | None = None
    issue_date: date | None = None
    due_date: date | None = None
    status: InvoiceStatus | None = None
    tax_rate: float | None = None
    notes: str | None = None
    terms: str | None = None


class InvoiceItemResponse(BaseModel):
    """Invoice line item response."""

    model_config = {"from_attributes": True}

    id: UUID
    description: str
    quantity: float
    unit_price: float
    amount: float
    sort_order: int


class PaymentCreate(BaseModel):
    """Payload for recording a payment against an invoice."""

    amount: float = Field(gt=0)
    payment_date: date
    payment_method: str | None = None
    reference: str | None = None
    notes: str | None = None


class PaymentResponse(BaseModel):
    """Invoice payment response."""

    model_config = {"from_attributes": True}

    id: UUID
    amount: float
    payment_date: date
    payment_method: str | None = None
    reference: str | None = None
    notes: str | None = None
    created_at: datetime


class InvoiceResponse(BaseModel):
    """Full invoice response."""

    model_config = {"from_attributes": True}

    id: UUID
    organization_id: UUID
    invoice_number: str
    client_name: str
    client_email: str | None = None
    client_address: str | None = None
    issue_date: date
    due_date: date
    status: InvoiceStatus
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    amount_paid: float
    currency: str
    notes: str | None = None
    terms: str | None = None
    items: list[InvoiceItemResponse] = Field(default_factory=list)
    payments: list[PaymentResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
