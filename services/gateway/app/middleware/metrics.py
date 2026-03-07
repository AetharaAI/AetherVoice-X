from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from aether_common.telemetry import record_error_metric, record_request_metric


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, service_name: str) -> None:
        super().__init__(app)
        self.service_name = service_name

    async def dispatch(self, request: Request, call_next):
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - started) * 1000
            record_error_metric(self.service_name, request.url.path, "internal_error")
            record_request_metric(self.service_name, request.url.path, "error", duration_ms)
            raise
        duration_ms = (time.perf_counter() - started) * 1000
        record_request_metric(self.service_name, request.url.path, str(response.status_code), duration_ms)
        return response
