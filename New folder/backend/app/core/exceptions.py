"""Custom exception hierarchy and FastAPI exception handlers.

Every custom exception maps to a specific HTTP status code so the
``register_exception_handlers`` function can translate them automatically.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# ─── Base exception ──────────────────────────────────────────────────────────

class LedgerAIException(Exception):
    """Base exception for all application-level errors."""

    status_code: int = 500
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None, *, context: dict[str, Any] | None = None):
        self.detail = detail or self.__class__.detail
        self.context = context or {}
        super().__init__(self.detail)


# ─── Concrete exceptions ────────────────────────────────────────────────────

class NotFoundException(LedgerAIException):
    """Resource not found (404)."""
    status_code = 404
    detail = "The requested resource was not found."


class ForbiddenException(LedgerAIException):
    """Insufficient permissions (403)."""
    status_code = 403
    detail = "You do not have permission to perform this action."


class UnauthorizedException(LedgerAIException):
    """Authentication failure (401)."""
    status_code = 401
    detail = "Invalid or missing authentication credentials."


class ConflictException(LedgerAIException):
    """Duplicate / conflict (409)."""
    status_code = 409
    detail = "The resource already exists or conflicts with the current state."


class ValidationException(LedgerAIException):
    """Business-rule validation error (422)."""
    status_code = 422
    detail = "The provided data failed validation."


class RateLimitException(LedgerAIException):
    """Rate limit exceeded (429)."""
    status_code = 429
    detail = "Too many requests. Please try again later."


class BadRequestException(LedgerAIException):
    """Generic client error (400)."""
    status_code = 400
    detail = "The request is invalid."


class ServiceUnavailableException(LedgerAIException):
    """Downstream service not reachable (503)."""
    status_code = 503
    detail = "A required service is temporarily unavailable."


# ─── Exception handler registration ─────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Attach custom exception handlers to the FastAPI application."""

    @app.exception_handler(LedgerAIException)
    async def _ledgerai_handler(_request: Request, exc: LedgerAIException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": type(exc).__name__,
                "detail": exc.detail,
                "context": exc.context,
            },
        )

    @app.exception_handler(Exception)
    async def _unhandled_handler(_request: Request, exc: Exception) -> JSONResponse:
        # In production the traceback should go to a logger / Sentry, not the client.
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "detail": "An unexpected error occurred. Please try again later.",
            },
        )
