"""Transaction ORM model and TransactionCategory junction table."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    Float,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class TransactionType(str, enum.Enum):
    """Whether money comes in or goes out."""

    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionSource(str, enum.Enum):
    """How the transaction was created."""

    MANUAL = "manual"
    CSV_IMPORT = "csv_import"
    BANK_SYNC = "bank_sync"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    API = "api"


class TransactionStatus(str, enum.Enum):
    """Workflow status."""

    PENDING = "pending"
    CATEGORIZED = "categorized"
    REVIEWED = "reviewed"
    RECONCILED = "reconciled"


class TransactionCategory(BaseModel):
    """Junction table linking transactions to one or more categories."""

    __tablename__ = "transaction_categories"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relationships ────────────────────────────────────────────────
    transaction: Mapped["Transaction"] = relationship(
        back_populates="category_links",
    )
    category: Mapped["Category"] = relationship(lazy="selectin")  # noqa: F821


class Transaction(BaseModel):
    """Financial transaction belonging to an organisation."""

    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_org_date", "organization_id", "date"),
        Index("ix_transactions_hash", "hash_fingerprint"),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped["__import__('datetime').date"] = mapped_column(Date, nullable=False, index=True)  # type: ignore[name-defined]
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    merchant_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type"), nullable=False
    )
    source: Mapped[TransactionSource] = mapped_column(
        Enum(TransactionSource, name="transaction_source"), default=TransactionSource.MANUAL, nullable=False
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, name="transaction_status"), default=TransactionStatus.PENDING, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[dict] = mapped_column(JSONB, default=list, server_default="[]", nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, server_default="{}", nullable=False)

    # AI categorization
    ai_category_suggestion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ai_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Duplicate detection
    hash_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Optional links
    invoice_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True
    )
    receipt_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("receipts.id", ondelete="SET NULL"), nullable=True
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # ── Relationships ────────────────────────────────────────────────
    category_links: Mapped[list[TransactionCategory]] = relationship(
        back_populates="transaction",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} amount={self.amount} type={self.type}>"
