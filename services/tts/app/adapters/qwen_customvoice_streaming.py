from __future__ import annotations

import base64

from .qwen_customvoice import QwenCustomVoiceAdapter
from ..schemas.requests import TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession, TimingBreakdown


class QwenCustomVoiceStreamingAdapter(QwenCustomVoiceAdapter):
    name = "qwen_customvoice_streaming"
    supports_streaming = True
    supports_batch = False

    async def synthesize(self, request):
        raise NotImplementedError("Qwen custom voice streaming lane is stream-oriented in this stack")

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen streaming provider is not configured")
        voice_name = self._resolve_voice_name(request)
        response = await self.client.post(
            "/v1/stream/start",
            json={
                "session_id": request.session_id,
                "model": self.model_name,
                "voice": voice_name,
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
            raise RuntimeError("Qwen streaming provider is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/text", json={"text": text})
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Qwen streaming provider returned an invalid event payload")
        return events

    async def complete_text(self, session_id: str) -> list[dict]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen streaming provider is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/complete")
        response.raise_for_status()
        payload = response.json()
        events = payload.get("events")
        if not isinstance(events, list):
            raise RuntimeError("Qwen streaming provider returned an invalid completion payload")
        return events

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen streaming provider is not configured")
        response = await self.client.post(f"/v1/stream/{session_id}/end")
        response.raise_for_status()
        payload = response.json()
        audio_b64 = payload.get("audio_b64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise RuntimeError("Qwen streaming provider did not return final audio")
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
