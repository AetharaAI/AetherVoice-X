from __future__ import annotations

import base64

import httpx

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession, TimingBreakdown


class KokoroRealtimeAdapter(BaseTTSAdapter):
    name = "kokoro_realtime"
    supports_streaming = True
    supports_batch = False

    def __init__(self, *, base_url: str | None, model_name: str, timeout_seconds: float = 120.0) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout_seconds) if self.base_url else None
        self.configured = bool(self.base_url)
        self.ready = self.refresh_health()

    def refresh_health(self) -> bool:
        if not self.base_url:
            self.ready = False
            return self.ready
        try:
            response = httpx.get(f"{self.base_url}/health", timeout=min(self.timeout_seconds, 3.0))
            self.ready = response.is_success
        except Exception:
            self.ready = False
        return self.ready

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        raise NotImplementedError("Kokoro realtime is stream-oriented in this stack")

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        if not self.base_url or self.client is None:
            raise RuntimeError("Kokoro realtime upstream is not configured")
        response = await self.client.post(
            "/v1/stream/start",
            json={
                "session_id": request.session_id,
                "model": self.model_name,
                "voice": request.voice,
                "sample_rate": request.sample_rate,
                "format": request.format,
                "context_mode": request.context_mode,
                "metadata": request.metadata,
            },
        )
        response.raise_for_status()
        payload = response.json()
        self.ready = True
        return StreamSession(
            session_id=str(payload["session_id"]),
            model=str(payload.get("model", self.name)),
            expires_in_seconds=int(payload.get("expires_in_seconds", 3600)),
        )

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Kokoro realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/text", json={"text": text})
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Kokoro realtime upstream returned an invalid event payload")
        return events

    async def complete_text(self, session_id: str) -> list[dict]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Kokoro realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/complete")
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Kokoro realtime upstream returned an invalid completion event payload")
        return events

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Kokoro realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/end")
        response.raise_for_status()
        payload = response.json()
        audio_b64 = payload.get("audio_b64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise RuntimeError("Kokoro realtime upstream did not return final audio")
        audio_bytes = base64.b64decode(audio_b64)
        completion = StreamCompletion(
            model_used=self.name,
            format=str(payload.get("format", "wav")),
            duration_ms=int(payload.get("duration_ms", 0)),
            timings=TimingBreakdown.model_validate(payload.get("timings") or {}),
            artifacts=dict(payload.get("artifacts") or {}),
        )
        return completion, audio_bytes
