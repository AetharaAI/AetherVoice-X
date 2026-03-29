from __future__ import annotations

import base64

import httpx

from .base import BaseTTSAdapter, BatchSynthesisResult
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


class VoxtralTTSAdapter(BaseTTSAdapter):
    name = "voxtral_tts"
    supports_streaming = False
    supports_batch = True

    def __init__(
        self,
        *,
        base_url: str | None,
        model_name: str,
        default_voice: str,
        timeout_seconds: float = 180.0,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.model_name = model_name
        self.default_voice = default_voice
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

    def _resolve_voice_name(self, request: TTSRequest) -> str:
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        resolved_voice = extra.get("resolved_voice")
        if isinstance(resolved_voice, dict):
            default_params = dict(resolved_voice.get("default_params") or {})
            voxtral_voice = str(default_params.get("voxtral_voice") or "").strip()
            if voxtral_voice:
                return voxtral_voice
        candidate = (request.voice or "").strip()
        if not candidate or candidate in {"default", "chatterbox_default"}:
            return self.default_voice
        return candidate

    async def synthesize(self, request: TTSRequest) -> BatchSynthesisResult:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtral TTS provider is not configured")
        voice_name = self._resolve_voice_name(request)
        response = await self.client.post(
            "/v1/audio/speech",
            json={
                "model": self.model_name,
                "input": request.text,
                "response_format": request.format,
                "voice": voice_name,
                "metadata": request.metadata,
            },
        )
        response.raise_for_status()

        audio_bytes: bytes
        output_format = request.format
        content_type = str(response.headers.get("content-type") or "").lower()
        if "application/json" in content_type:
            payload = response.json()
            audio_b64 = payload.get("audio_b64")
            if not isinstance(audio_b64, str) or not audio_b64:
                raise RuntimeError("Voxtral TTS provider returned no audio payload")
            audio_bytes = base64.b64decode(audio_b64)
            output_format = str(payload.get("format") or request.format)
        else:
            audio_bytes = response.content

        self.ready = True
        return BatchSynthesisResult(
            audio_bytes=audio_bytes,
            output_format=output_format,
            model_used=self.name,
            artifacts={
                "runtime_path_used": self.name,
                "voxtral_tts_voice": voice_name,
                "voxtral_tts_model": self.model_name,
            },
        )

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Voxtral TTS is integrated as a batch lane in this stack")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("Voxtral TTS is integrated as a batch lane in this stack")

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError("Voxtral TTS is integrated as a batch lane in this stack")

