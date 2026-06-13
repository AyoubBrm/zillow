"""Request-level middleware: logging, timing, and tenant context injection."""

from __future__ import annotations

import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("ledgerai")

# ─── Context vars (available to any async code in the same request) ──────────
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
tenant_id_ctx: ContextVar[str] = ContextVar("tenant_id", default="")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with a unique request ID and elapsed time."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        rid = str(uuid.uuid4())
        request_id_ctx.set(rid)

        # Extract tenant hint from header (set by the frontend / API gateway)
        tenant_header = request.headers.get("X-Tenant-ID", "")
        if tenant_header:
            tenant_id_ctx.set(tenant_header)

        start = time.perf_counter()
        logger.info(
            "→ %s %s  [request_id=%s tenant=%s]",
            request.method,
            request.url.path,
            rid,
            tenant_header or "-",
        )

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "← %s %s  status=%d  %.1fms  [request_id=%s]",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            rid,
        )
        response.headers["X-Request-ID"] = rid
        return response


def register_middleware(app: FastAPI) -> None:
    """Attach all custom middleware to the application."""
    app.add_middleware(RequestLoggingMiddleware)
