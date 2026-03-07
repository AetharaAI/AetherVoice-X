from __future__ import annotations

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamSession, TTSResult


class MossRealtimeAdapter(BaseTTSAdapter):
    name = "moss_realtime"
    supports_streaming = True
    supports_batch = False

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        raise NotImplementedError("MOSS realtime is scaffolded but not integrated yet")

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("MOSS realtime is scaffolded but not integrated yet")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("MOSS realtime is scaffolded but not integrated yet")

    async def end_stream(self, session_id: str) -> TTSResult:
        raise NotImplementedError("MOSS realtime is scaffolded but not integrated yet")
