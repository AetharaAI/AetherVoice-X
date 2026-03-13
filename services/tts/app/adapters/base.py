from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


@dataclass(slots=True)
class BatchSynthesisResult:
    audio_bytes: bytes
    output_format: str
    model_used: str | None = None
    timings: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)


class BaseTTSAdapter(ABC):
    name: str
    supports_streaming: bool
    supports_batch: bool

    @abstractmethod
    async def synthesize(self, request: TTSRequest) -> BatchSynthesisResult | tuple[bytes, str]:
        raise NotImplementedError

    @abstractmethod
    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError

    @abstractmethod
    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError

    async def complete_text(self, session_id: str) -> list[dict]:
        return []

    async def warmup(self, metadata: dict | None = None) -> dict:
        return {"status": "noop", "route": self.name, "metadata": metadata or {}}

    @abstractmethod
    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError
