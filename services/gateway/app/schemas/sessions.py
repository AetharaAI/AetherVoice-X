from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from aether_common.schemas import SessionSummary


class SessionListResponse(BaseModel):
    sessions: list[SessionSummary]


class SessionDetailResponse(BaseModel):
    session: SessionSummary
    requests: list[dict[str, Any]] = Field(default_factory=list)
    transcripts: list[dict[str, Any]] = Field(default_factory=list)
    triage_results: list[dict[str, Any]] = Field(default_factory=list)
    tts_outputs: list[dict[str, Any]] = Field(default_factory=list)


class SessionEndResponse(BaseModel):
    session_id: str
    status: str
