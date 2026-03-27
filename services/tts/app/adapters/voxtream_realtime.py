from __future__ import annotations

import base64
from typing import Any

import httpx

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession, TimingBreakdown


class VoxtreamRealtimeAdapter(BaseTTSAdapter):
    supports_streaming = True
    supports_batch = False

    def __init__(self, *, name: str, base_url: str | None, model_name: str, timeout_seconds: float = 120.0) -> None:
        self.name = name
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
        raise NotImplementedError("Voxtream realtime is stream-oriented in this stack")

    @staticmethod
    def _start_payload(request: TTSStreamStartRequest, *, model_name: str) -> dict[str, Any]:
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        resolved_voice = dict(extra.get("resolved_voice") or {}) if isinstance(extra.get("resolved_voice"), dict) else {}
        realtime_profile = dict(extra.get("realtime_profile") or {}) if isinstance(extra.get("realtime_profile"), dict) else {}
        realtime_tuning = dict(extra.get("realtime_tuning") or {}) if isinstance(extra.get("realtime_tuning"), dict) else {}

        payload: dict[str, Any] = {
            "session_id": request.session_id,
            "model": model_name,
            "voice": request.voice,
            "sample_rate": request.sample_rate,
            "format": request.format,
            "context_mode": request.context_mode,
            "metadata": request.metadata,
        }

        reference_audio_path = str(extra.get("reference_audio_path") or "").strip()
        if reference_audio_path:
            payload["prompt_audio_path"] = reference_audio_path

        reference_audio_b64 = str(extra.get("reference_audio_b64") or "").strip()
        if reference_audio_b64:
            payload["prompt_audio_b64"] = reference_audio_b64

        reference_text = str(extra.get("reference_text") or "").strip()
        if reference_text:
            payload["prompt_text"] = reference_text

        generation_prompt = str(extra.get("generation_prompt") or "").strip()
        if generation_prompt:
            payload["instructions"] = generation_prompt

        speaking_rate = realtime_tuning.get("speaking_rate")
        if speaking_rate is None:
            speaking_rate = realtime_profile.get("speaking_rate")
        if speaking_rate is not None:
            payload["speaking_rate"] = speaking_rate

        selected_voice_asset = str(extra.get("selected_voice_asset") or resolved_voice.get("display_name") or "").strip()
        if selected_voice_asset:
            payload["voice"] = selected_voice_asset

        return payload

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtream realtime upstream is not configured")
        response = await self.client.post(
            "/v1/stream/start",
            json=self._start_payload(request, model_name=self.name),
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
            raise RuntimeError("Voxtream realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/text", json={"text": text})
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Voxtream realtime upstream returned an invalid event payload")
        return events

    async def complete_text(self, session_id: str) -> list[dict]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtream realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/complete")
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Voxtream realtime upstream returned an invalid completion payload")
        return events

    async def warmup(self, metadata: dict | None = None) -> dict:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtream realtime upstream is not configured")
        payload = dict(metadata or {})
        payload.setdefault("model", self.name)
        response = await self.client.post("/v1/warmup", json=payload)
        response.raise_for_status()
        self.ready = True
        result = dict(response.json())
        result.setdefault("route", self.name)
        return result

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtream realtime upstream is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/end")
        response.raise_for_status()
        payload = response.json()
        audio_b64 = payload.get("audio_b64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise RuntimeError("Voxtream realtime upstream did not return final audio")
        audio_bytes = base64.b64decode(audio_b64)
        completion = StreamCompletion(
            model_used=str(payload.get("model", self.name)),
            format=str(payload.get("format", "wav")),
            duration_ms=int(payload.get("duration_ms", 0)),
            timings=TimingBreakdown.model_validate(payload.get("timings") or {}),
            artifacts=dict(payload.get("artifacts") or {}),
        )
        self.ready = True
        return completion, audio_bytes
