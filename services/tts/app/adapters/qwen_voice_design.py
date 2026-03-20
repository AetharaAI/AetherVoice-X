from __future__ import annotations

import base64

from .qwen_customvoice import LANGUAGE_MAP, QwenCustomVoiceAdapter
from .base import BatchSynthesisResult
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession


class QwenVoiceDesignAdapter(QwenCustomVoiceAdapter):
    name = "qwen_voice_design"
    supports_streaming = False
    supports_batch = True

    def _resolve_voice_name(self, request: TTSRequest) -> str:
        return "prompt_driven"

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
        explicit_instruction = str(extra.get("qwen_instructions") or "").strip()
        if explicit_instruction:
            return explicit_instruction
        generation_prompt = str(extra.get("generation_prompt") or "").strip()
        if generation_prompt:
            return generation_prompt
        resolved_voice = extra.get("resolved_voice")
        if isinstance(resolved_voice, dict):
            nested_prompt = str(resolved_voice.get("generation_prompt") or "").strip()
            if nested_prompt:
                return nested_prompt
        return None

    async def synthesize(self, request: TTSRequest) -> BatchSynthesisResult:
        if not self.base_url or self.client is None:
            raise RuntimeError("Qwen provider is not configured")
        language = self._resolve_language(request)
        instruction = self._resolve_instruction(request)
        if not instruction:
            raise RuntimeError("Qwen VoiceDesign requires a non-empty generation prompt.")
        response = await self.client.post(
            "/v1/audio/speech",
            json={
                "model": self.model_name,
                "input": request.text,
                "voice": self._resolve_voice_name(request),
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
                "qwen_language": language,
                "qwen_instructions": instruction,
                "qwen_voice": "prompt_driven",
                **dict(payload.get("artifacts") or {}),
            },
        )

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Qwen VoiceDesign is a batch-only lane in this stack")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("Qwen VoiceDesign is a batch-only lane in this stack")

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError("Qwen VoiceDesign is a batch-only lane in this stack")
