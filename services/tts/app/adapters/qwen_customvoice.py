from __future__ import annotations

import base64

import httpx

from .base import BaseTTSAdapter, BatchSynthesisResult
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


LANGUAGE_MAP = {
    "en": "English",
    "english": "English",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}


class QwenCustomVoiceAdapter(BaseTTSAdapter):
    name = "qwen_customvoice"
    supports_streaming = False
    supports_batch = True

    def __init__(
        self,
        *,
        base_url: str | None,
        model_name: str,
        default_voice: str,
        default_language: str,
        timeout_seconds: float = 180.0,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.model_name = model_name
        self.default_voice = default_voice
        self.default_language = default_language
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
            runtime_target = str(resolved_voice.get("runtime_target") or "").strip()
            default_params = dict(resolved_voice.get("default_params") or {})
            qwen_speaker = str(default_params.get("qwen_speaker") or "").strip()
            if qwen_speaker:
                return qwen_speaker
            display_name = str(resolved_voice.get("display_name") or "").strip()
            if display_name and runtime_target in {"qwen_customvoice", "qwen_customvoice_streaming"}:
                return display_name
            return self.default_voice
        candidate = (request.voice or "").strip()
        if not candidate or candidate in {"default", "chatterbox_default"}:
            return self.default_voice
        return candidate

    def _resolve_language(self, request: TTSRequest) -> str:
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        resolved_voice = extra.get("resolved_voice")
        if isinstance(resolved_voice, dict):
            language = str(resolved_voice.get("language") or "").strip().lower()
            if language:
                return LANGUAGE_MAP.get(language, language.title())
        return LANGUAGE_MAP.get(self.default_language.lower(), self.default_language)

    def _resolve_instruction(self, request: TTSRequest) -> str | None:
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        if isinstance(extra.get("qwen_instructions"), str) and str(extra["qwen_instructions"]).strip():
            return str(extra["qwen_instructions"]).strip()
        resolved_voice = extra.get("resolved_voice")
        if isinstance(resolved_voice, dict):
            generation_prompt = str(resolved_voice.get("generation_prompt") or "").strip()
            if generation_prompt:
                return generation_prompt
        emotion = str(getattr(request.style, "emotion", "") or "").strip()
        if emotion and emotion != "neutral":
            return f"Speak in a {emotion} but telephony-friendly style."
        return None

    async def synthesize(self, request: TTSRequest) -> BatchSynthesisResult:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen provider is not configured")
        voice_name = self._resolve_voice_name(request)
        language = self._resolve_language(request)
        instruction = self._resolve_instruction(request)
        response = await self.client.post(
            "/v1/audio/speech",
            json={
                "model": self.model_name,
                "input": request.text,
                "voice": voice_name,
                "response_format": request.format,
                "language": language,
                "instructions": instruction,
                "metadata": request.metadata,
            },
        )
        response.raise_for_status()
        payload = response.json()
        audio_b64 = payload.get("audio_b64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise RuntimeError("Qwen provider returned no audio payload")
        self.ready = True
        return BatchSynthesisResult(
            audio_bytes=base64.b64decode(audio_b64),
            output_format=str(payload.get("format", request.format)),
            model_used=str(payload.get("model") or self.name),
            timings=dict(payload.get("timings") or {}),
            artifacts={
                "runtime_path_used": self.name,
                "qwen_voice": voice_name,
                "qwen_language": language,
                "qwen_instructions": instruction or "",
                **dict(payload.get("artifacts") or {}),
            },
        )

    async def warmup(self, metadata: dict | None = None) -> dict:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen provider is not configured")
        payload = dict(metadata or {})
        payload.setdefault("model", self.model_name)
        response = await self.client.post("/v1/warmup", json=payload)
        response.raise_for_status()
        self.ready = True
        payload = dict(response.json())
        payload.setdefault("route", self.name)
        return payload

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Qwen custom voice streaming is not integrated yet")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("Qwen custom voice streaming is not integrated yet")

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError("Qwen custom voice streaming is not integrated yet")
