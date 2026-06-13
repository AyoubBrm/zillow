"""AI-related Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CategorizationRequest(BaseModel):
    """Payload for AI categorization of a single transaction."""

    description: str
    merchant_name: str | None = None
    amount: float | None = None


class CategorizationResult(BaseModel):
    """Single categorization result."""

    category_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str | None = None


class CategorizationResponse(BaseModel):
    """AI categorization response (may include multiple suggestions)."""

    suggestions: list[CategorizationResult]
    source: str = Field(
        default="rule_based",
        description="Engine that produced the result: 'rule_based' or 'llm'",
    )


class BulkCategorizationRequest(BaseModel):
    """Categorize multiple transactions at once."""

    transaction_ids: list[UUID]


class BulkCategorizationResponse(BaseModel):
    """Results of bulk categorization."""

    results: dict[str, CategorizationResult] = Field(
        default_factory=dict,
        description="Mapping of transaction_id → result",
    )
    total: int
    categorized: int
    failed: int


class ChatRequest(BaseModel):
    """Payload for AI chat about financial data."""

    message: str = Field(min_length=1)
    context: dict | None = Field(
        default=None,
        description="Optional context such as date range, category filter, etc.",
    )


class ChatResponse(BaseModel):
    """AI chat response."""

    reply: str
    suggestions: list[str] = Field(default_factory=list)
    source: str = "rule_based"


class FeedbackRequest(BaseModel):
    """User feedback on an AI categorization."""

    transaction_id: UUID
    suggested_category: str
    correct_category: str
