"""Report Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ReportType(str, Enum):
    """Available report types."""

    PROFIT_AND_LOSS = "profit_and_loss"
    EXPENSE_REPORT = "expense_report"
    INCOME_REPORT = "income_report"
    TAX_SUMMARY = "tax_summary"
    CATEGORY_BREAKDOWN = "category_breakdown"


class ReportFormat(str, Enum):
    """Output format."""

    JSON = "json"
    CSV = "csv"
    PDF = "pdf"


class ReportRequest(BaseModel):
    """Payload for generating a report."""

    report_type: ReportType
    date_from: date
    date_to: date
    format: ReportFormat = ReportFormat.JSON
    category_ids: list[UUID] | None = None
    include_subcategories: bool = True


class ReportLineItem(BaseModel):
    """Single line in a report."""

    category: str
    amount: float
    percentage: float = 0.0
    transaction_count: int = 0


class ReportResponse(BaseModel):
    """Structured report output."""

    id: UUID | None = None
    report_type: ReportType
    title: str
    date_from: date
    date_to: date
    generated_at: datetime
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    line_items: list[ReportLineItem] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
