from __future__ import annotations

import base64
from typing import Any

import httpx

from .base import BaseTTSAdapter, BatchSynthesisResult
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


class VoxtralTTSAdapter(BaseTTSAdapter):
    name = "voxtral_tts"
    supports_streaming = True
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
        self._stream_sessions: dict[str, dict[str, Any]] = {}

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
        return self._resolve_voice_name_from_extra(extra, fallback_voice=request.voice)

    def _resolve_voice_name_from_extra(self, extra: dict[str, Any], *, fallback_voice: str) -> str:
        resolved_voice = extra.get("resolved_voice")
        if isinstance(resolved_voice, dict):
            default_params = dict(resolved_voice.get("default_params") or {})
            voxtral_voice = str(default_params.get("voxtral_voice") or "").strip()
            if voxtral_voice:
                return voxtral_voice
        candidate = (fallback_voice or "").strip()
        if not candidate or candidate in {"default", "chatterbox_default"}:
            return self.default_voice
        return candidate

    async def _generate_audio(self, *, text: str, voice_name: str, output_format: str, metadata: dict[str, Any] | None = None) -> tuple[bytes, str]:
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtral TTS provider is not configured")
        response = await self.client.post(
            "/v1/audio/speech",
            json={
                "model": self.model_name,
                "input": text,
                "response_format": output_format,
                "voice": voice_name,
                "metadata": metadata or {},
            },
        )
        response.raise_for_status()

        content_type = str(response.headers.get("content-type") or "").lower()
        if "application/json" in content_type:
            payload = response.json()
            audio_b64 = payload.get("audio_b64")
            if not isinstance(audio_b64, str) or not audio_b64:
                raise RuntimeError("Voxtral TTS provider returned no audio payload")
            return base64.b64decode(audio_b64), str(payload.get("format") or output_format)

        return response.content, output_format

    async def synthesize(self, request: TTSRequest) -> BatchSynthesisResult:
        voice_name = self._resolve_voice_name(request)
        audio_bytes, output_format = await self._generate_audio(
            text=request.text,
            voice_name=voice_name,
            output_format=request.format,
            metadata=request.metadata,
        )

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
        if not self.base_url or self.client is None:
            raise RuntimeError("Voxtral TTS provider is not configured")
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        voice_name = self._resolve_voice_name_from_extra(extra, fallback_voice=request.voice)
        self._stream_sessions[request.session_id] = {
            "voice_name": voice_name,
            "format": request.format,
            "metadata": request.metadata,
            "sequence": 0,
            "text_fragments": [],
            "last_audio_bytes": b"",
            "last_output_format": request.format,
        }
        self.ready = True
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        state = self._stream_sessions.get(session_id)
        if state is None:
            raise RuntimeError(f"Unknown Voxtral stream session: {session_id}")
        state["sequence"] += 1
        state["text_fragments"].append(text)
        audio_bytes, output_format = await self._generate_audio(
            text=text,
            voice_name=str(state["voice_name"]),
            output_format=str(state["format"]),
            metadata=dict(state.get("metadata") or {}),
        )
        state["last_audio_bytes"] = audio_bytes
        state["last_output_format"] = output_format
        self.ready = True
        return [
            {
                "type": "audio_chunk",
                "session_id": session_id,
                "sequence": int(state["sequence"]),
                "audio_b64": base64.b64encode(audio_bytes).decode("ascii"),
                "format": output_format,
                "metadata": {
                    "runtime_path_used": self.name,
                    "voxtral_tts_voice": state["voice_name"],
                    "voxtral_tts_model": self.model_name,
                },
            }
        ]

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        state = self._stream_sessions.pop(session_id, None)
        if state is None:
            raise RuntimeError(f"Unknown Voxtral stream session: {session_id}")
        audio_bytes = bytes(state.get("last_audio_bytes") or b"")
        output_format = str(state.get("last_output_format") or "wav")
        if not audio_bytes:
            joined_text = " ".join(str(part) for part in state.get("text_fragments", []) if str(part).strip()).strip()
            if joined_text:
                audio_bytes, output_format = await self._generate_audio(
                    text=joined_text,
                    voice_name=str(state["voice_name"]),
                    output_format=str(state["format"]),
                    metadata=dict(state.get("metadata") or {}),
                )
            else:
                raise RuntimeError("Voxtral stream ended without any text to synthesize")
        self.ready = True
        return (
            StreamCompletion(
                model_used=self.name,
                format=output_format,
                duration_ms=0,
                artifacts={
                    "runtime_path_used": self.name,
                    "voxtral_tts_voice": state["voice_name"],
                    "voxtral_tts_model": self.model_name,
                },
            ),
            audio_bytes,
        )
