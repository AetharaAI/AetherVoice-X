from __future__ import annotations

from abc import ABC, abstractmethod

from ..schemas.requests import ASRFileRequest, ASRStreamStartRequest, AudioFrame
from ..schemas.responses import ASRResult, StreamSession


class BaseASRAdapter(ABC):
    name: str
    supports_streaming: bool
    supports_batch: bool
    supports_timestamps: bool
    supports_language_detection: bool
    ready: bool = True

    @abstractmethod
    async def transcribe_file(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        raise NotImplementedError

    @abstractmethod
    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        raise NotImplementedError

    @abstractmethod
    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def end_stream(self, session_id: str) -> ASRResult:
        raise NotImplementedError

    async def abort_stream(self, session_id: str) -> None:
        """Best-effort teardown of an in-flight stream without waiting for a clean
        final (used when the client disconnects or the socket errors). Must be
        idempotent and safe to call when no such session exists. The default
        drops any per-session state held in a ``_sessions`` dict; adapters with
        external resources (e.g. an upstream websocket) should override and also
        release those."""
        sessions = getattr(self, "_sessions", None)
        if isinstance(sessions, dict):
            sessions.pop(session_id, None)
