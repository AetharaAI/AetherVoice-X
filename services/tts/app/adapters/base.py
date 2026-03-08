from __future__ import annotations

from abc import ABC, abstractmethod

from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


class BaseTTSAdapter(ABC):
    name: str
    supports_streaming: bool
    supports_batch: bool

    @abstractmethod
    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        raise NotImplementedError

    @abstractmethod
    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError

    @abstractmethod
    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError
