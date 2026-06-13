"""Billing Pydantic schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.billing import PlanTier, SubscriptionStatus


class PlanFeature(BaseModel):
    """A feature included in a plan."""

    name: str
    included: bool = True
    limit: int | str | None = None


class PlanResponse(BaseModel):
    """Billing plan description (static data for MVP)."""

    tier: PlanTier
    name: str
    price_monthly: float
    price_yearly: float
    max_transactions: int
    max_users: int
    max_organizations: int
    features: list[PlanFeature] = Field(default_factory=list)


class SubscriptionResponse(BaseModel):
    """Current subscription state for an organisation."""

    model_config = {"from_attributes": True}

    plan: PlanTier
    status: SubscriptionStatus
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    cancel_at_period_end: bool = False
    max_transactions_per_month: int
    max_users: int
