"""Invoice, InvoiceItem, and InvoicePayment ORM models."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class InvoiceStatus(str, enum.Enum):
    """Invoice lifecycle status."""

    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(BaseModel):
    """An invoice issued by the organisation to a client."""

    __tablename__ = "invoices"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    client_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    issue_date: Mapped["__import__('datetime').date"] = mapped_column(Date, nullable=False)  # type: ignore[name-defined]
    due_date: Mapped["__import__('datetime').date"] = mapped_column(Date, nullable=False)  # type: ignore[name-defined]
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus, name="invoice_status"), default=InvoiceStatus.DRAFT, nullable=False,
    )
    subtotal: Mapped[float] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    total: Mapped[float] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(15, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    terms: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, server_default="{}", nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    )

    # ── Relationships ────────────────────────────────────────────────
    items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="invoice", lazy="selectin", cascade="all, delete-orphan",
    )
    payments: Mapped[list["InvoicePayment"]] = relationship(
        back_populates="invoice", lazy="selectin", cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Invoice id={self.id} number={self.invoice_number}>"


class InvoiceItem(BaseModel):
    """A single line item on an invoice."""

    __tablename__ = "invoice_items"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(10, 2), default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────────────
    invoice: Mapped["Invoice"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<InvoiceItem id={self.id} amount={self.amount}>"


class InvoicePayment(BaseModel):
    """A payment recorded against an invoice."""

    __tablename__ = "invoice_payments"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    payment_date: Mapped["__import__('datetime').date"] = mapped_column(Date, nullable=False)  # type: ignore[name-defined]
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ────────────────────────────────────────────────
    invoice: Mapped["Invoice"] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return f"<InvoicePayment id={self.id} amount={self.amount}>"
