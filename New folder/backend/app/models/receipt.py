"""Receipt and ReceiptMatch ORM models."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ReceiptStatus(str, enum.Enum):
    """Processing status of an uploaded receipt."""

    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    MATCHED = "matched"
    FAILED = "failed"


class Receipt(BaseModel):
    """An uploaded receipt image / PDF."""

    __tablename__ = "receipts"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int | None] = mapped_column(nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[ReceiptStatus] = mapped_column(
        Enum(ReceiptStatus, name="receipt_status"), default=ReceiptStatus.UPLOADED, nullable=False,
    )

    # OCR / extracted data
    extracted_merchant: Mapped[str | None] = mapped_column(String(255), nullable=True)
    extracted_amount: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    extracted_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    extracted_data: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}", nullable=False)

    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    )

    # ── Relationships ────────────────────────────────────────────────
    matches: Mapped[list["ReceiptMatch"]] = relationship(
        back_populates="receipt", lazy="selectin", cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Receipt id={self.id} file={self.file_name}>"


class ReceiptMatch(BaseModel):
    """A suggested or confirmed match between a receipt and a transaction."""

    __tablename__ = "receipt_matches"

    receipt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)

    # ── Relationships ────────────────────────────────────────────────
    receipt: Mapped["Receipt"] = relationship(back_populates="matches")

    def __repr__(self) -> str:
        return f"<ReceiptMatch receipt={self.receipt_id} txn={self.transaction_id}>"
