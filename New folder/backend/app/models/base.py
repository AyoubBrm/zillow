"""Base model mixin providing UUID primary key and timestamp columns.

Every ORM model inherits from ``TimestampMixin`` (or uses it as a mixin)
so that ``id``, ``created_at``, and ``updated_at`` are always present.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampMixin:
    """Mixin that adds UUID pk + audit timestamps to any model."""

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseModel(TimestampMixin, Base):
    """Abstract base model with UUID pk and timestamps.

    All application tables should subclass this instead of ``Base`` directly.
    """

    __abstract__ = True
