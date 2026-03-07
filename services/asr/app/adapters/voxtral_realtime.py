from __future__ import annotations

from .base import BaseASRAdapter
from ..schemas.requests import ASRFileRequest, ASRStreamStartRequest, AudioFrame
from ..schemas.responses import ASRResult, StreamSession


class VoxtralRealtimeAdapter(BaseASRAdapter):
    name = "voxtral_realtime"
    supports_streaming = True
    supports_batch = False
    supports_timestamps = True
    supports_language_detection = True

    async def transcribe_file(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        raise NotImplementedError("Voxtral realtime is scaffolded but not integrated yet")

    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Voxtral realtime is scaffolded but not integrated yet")

    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[dict]:
        raise NotImplementedError("Voxtral realtime is scaffolded but not integrated yet")

    async def end_stream(self, session_id: str) -> ASRResult:
        raise NotImplementedError("Voxtral realtime is scaffolded but not integrated yet")
