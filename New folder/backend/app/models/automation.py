"""AutomationRule ORM model for user-defined accounting rules."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class RuleTrigger(str, enum.Enum):
    """When the rule fires."""

    ON_TRANSACTION_CREATE = "on_transaction_create"
    ON_IMPORT = "on_import"
    SCHEDULED = "scheduled"


class AutomationRule(BaseModel):
    """User-defined automation rule for transaction processing.

    ``conditions`` is a JSON list of condition objects, e.g.::

        [{"field": "merchant_name", "op": "contains", "value": "starbucks"}]

    ``actions`` is a JSON list of action objects, e.g.::

        [{"action": "set_category", "value": "Meals & Entertainment"}]
    """

    __tablename__ = "automation_rules"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    trigger: Mapped[RuleTrigger] = mapped_column(
        Enum(RuleTrigger, name="rule_trigger"),
        default=RuleTrigger.ON_TRANSACTION_CREATE,
        nullable=False,
    )
    conditions: Mapped[dict] = mapped_column(JSONB, default=list, server_default="[]", nullable=False)
    actions: Mapped[dict] = mapped_column(JSONB, default=list, server_default="[]", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    times_triggered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    )

    def __repr__(self) -> str:
        return f"<AutomationRule id={self.id} name={self.name}>"
