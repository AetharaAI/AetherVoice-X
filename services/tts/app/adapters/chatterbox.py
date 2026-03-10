from __future__ import annotations

import httpx
from pathlib import Path
from urllib.parse import urljoin

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


class ChatterboxAdapter(BaseTTSAdapter):
    name = "chatterbox"
    supports_streaming = False
    supports_batch = True

    def __init__(self, base_url: str, *, default_voice: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.default_voice = default_voice
        self.client = httpx.AsyncClient(timeout=120.0)

    async def close(self) -> None:
        await self.client.aclose()

    def _resolve_voice_file(self, voice: str, *, extra: dict | None = None) -> str:
        resolved_voice = extra.get("resolved_voice") if isinstance(extra, dict) else None
        if isinstance(resolved_voice, dict):
            runtime_target = str(resolved_voice.get("runtime_target") or "").strip()
            source_model = str(resolved_voice.get("source_model") or "").strip()
            reference_audio_path = str(resolved_voice.get("reference_audio_path") or "").strip()
            if runtime_target == "chatterbox" or source_model == "chatterbox":
                if reference_audio_path:
                    reference_name = Path(reference_audio_path).name
                    if reference_name:
                        return reference_name
            elif runtime_target:
                return self.default_voice
        candidate = (voice or "").strip()
        if not candidate or candidate in {"default", "chatterbox_default"}:
            return self.default_voice
        if "." in candidate:
            return candidate
        return f"{candidate}.wav"

    def _resolve_voice_name(self, voice_file: str) -> str:
        return voice_file.rsplit(".", 1)[0]

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
        voice_file = self._resolve_voice_file(request.voice, extra=extra)
        voice_name = self._resolve_voice_name(voice_file)
        chunk_size = int(extra.get("chunk_size") or 120)
        split_text = bool(extra.get("split_text", True))
        language = str(extra.get("language") or "en")
        candidates = [
            (
                f"{self.base_url}/tts",
                {
                    "text": request.text,
                    "voice_mode": str(extra.get("voice_mode") or "predefined"),
                    "predefined_voice_id": voice_file,
                    "output_format": request.format,
                    "split_text": split_text,
                    "chunk_size": chunk_size,
                    "speed_factor": request.style.speed,
                    "language": language,
                    "temperature": extra.get("temperature"),
                    "exaggeration": extra.get("exaggeration"),
                    "cfg_weight": extra.get("cfg_weight"),
                    "seed": extra.get("seed"),
                },
            ),
            (
                f"{self.base_url}/v1/audio/speech",
                {
                    "model": self.name,
                    "input": request.text,
                    "voice": voice_name,
                    "response_format": request.format,
                    "speed": request.style.speed,
                },
            ),
        ]
        last_exc: Exception | None = None
        for url, payload in candidates:
            try:
                if url.endswith("/tts"):
                    payload = {key: value for key, value in payload.items() if value is not None}
                response = await self.client.post(url, json=payload, headers={"Accept": f"audio/{request.format}"})
                response.raise_for_status()
                if response.headers.get("content-type", "").startswith("audio/"):
                    return response.content, request.format
                body = response.json()
                if "audio_b64" in body:
                    import base64

                    return base64.b64decode(body["audio_b64"]), body.get("format", request.format)
                if "audio_url" in body:
                    follow_up = await self.client.get(urljoin(f"{self.base_url}/", body["audio_url"]))
                    follow_up.raise_for_status()
                    return follow_up.content, body.get("format", request.format)
            except Exception as exc:  # pragma: no cover - depends on external Chatterbox shape
                last_exc = exc
        raise RuntimeError(f"Unable to synthesize via Chatterbox passthrough: {last_exc}")

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")
