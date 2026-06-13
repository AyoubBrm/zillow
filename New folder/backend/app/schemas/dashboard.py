"""Dashboard Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChartDataPoint(BaseModel):
    """Single data point for charts."""

    label: str
    value: float
    color: str | None = None
    percentage: float | None = None


class MonthlyTrend(BaseModel):
    """Monthly income / expense / profit data."""

    month: str = Field(description="YYYY-MM format")
    income: float = 0.0
    expenses: float = 0.0
    profit: float = 0.0


class DashboardSummary(BaseModel):
    """Aggregated dashboard metrics."""

    total_income: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    transaction_count: int = 0
    pending_categorization: int = 0
    overdue_invoices: int = 0
    monthly_trends: list[MonthlyTrend] = Field(default_factory=list)
    expense_by_category: list[ChartDataPoint] = Field(default_factory=list)
    income_by_category: list[ChartDataPoint] = Field(default_factory=list)
    recent_transactions_count: int = 0
