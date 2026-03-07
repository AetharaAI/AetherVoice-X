from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest


voice_requests_total = Counter(
    "voice_requests_total",
    "Total voice requests",
    ["service", "route", "status"],
)
voice_request_errors_total = Counter(
    "voice_request_errors_total",
    "Total voice request errors",
    ["service", "route", "error_code"],
)
voice_request_duration_ms = Histogram(
    "voice_request_duration_ms",
    "Voice request duration in milliseconds",
    ["service", "route"],
    buckets=(10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, float("inf")),
)
voice_asr_stream_time_to_first_partial_ms = Histogram(
    "voice_asr_stream_time_to_first_partial_ms",
    "ASR time to first partial",
    ["service"],
)
voice_asr_stream_time_to_final_ms = Histogram(
    "voice_asr_stream_time_to_final_ms",
    "ASR time to final transcript",
    ["service"],
)
voice_tts_time_to_first_chunk_ms = Histogram(
    "voice_tts_time_to_first_chunk_ms",
    "TTS time to first chunk",
    ["service"],
)
voice_active_sessions = Gauge(
    "voice_active_sessions",
    "Active websocket sessions",
    ["service", "kind"],
)
voice_model_fallback_total = Counter(
    "voice_model_fallback_total",
    "Model fallback count",
    ["service", "requested", "used"],
)
voice_queue_depth = Gauge(
    "voice_queue_depth",
    "Approximate queue depth",
    ["service", "route"],
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service", "unknown"),
            "logger": record.name,
            "time": self.formatTime(record, self.datefmt),
        }
        for key in (
            "request_id",
            "session_id",
            "route",
            "tenant_id",
            "model_requested",
            "model_used",
            "audio_duration_ms",
            "queue_ms",
            "preprocess_ms",
            "inference_ms",
            "postprocess_ms",
            "total_ms",
            "status",
            "error_code",
            "fallback_used",
        ):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        return json.dumps(payload)


def configure_logging(service_name: str, level: str = "INFO") -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())
    root.addHandler(handler)
    logger = logging.getLogger(service_name)
    logger.setLevel(level.upper())
    return logging.LoggerAdapter(logger, {"service": service_name})  # type: ignore[return-value]


def record_request_metric(service: str, route: str, status: str, duration_ms: float) -> None:
    voice_requests_total.labels(service=service, route=route, status=status).inc()
    voice_request_duration_ms.labels(service=service, route=route).observe(duration_ms)


def record_error_metric(service: str, route: str, error_code: str) -> None:
    voice_request_errors_total.labels(service=service, route=route, error_code=error_code).inc()


def metrics_payload() -> bytes:
    return generate_latest()


def metrics_content_type() -> str:
    return CONTENT_TYPE_LATEST


def utc_timestamp_ms() -> int:
    return int(time.time() * 1000)
