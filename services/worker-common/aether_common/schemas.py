from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RequestMetadata(BaseModel):
    source: str | None = None
    tenant_id: str | None = None
    trace_id: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class TimingBreakdown(BaseModel):
    queue_ms: int = 0
    preprocess_ms: int = 0
    inference_ms: int = 0
    postprocess_ms: int = 0
    total_ms: int = 0
    encode_ms: int = 0


class ModelInfo(BaseModel):
    name: str
    kind: str
    supports_streaming: bool
    supports_batch: bool
    status: str
    features: list[str] = Field(default_factory=list)
    route_priority: int = 100
    memory_footprint: str | None = None


class SessionSummary(BaseModel):
    id: str
    tenant_id: str
    session_type: str
    model_requested: str | None = None
    model_used: str | None = None
    status: str
    started_at: datetime
    ended_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    detail: str
