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
