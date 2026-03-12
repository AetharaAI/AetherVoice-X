from __future__ import annotations

import json
import re
import time
from typing import Any, Callable

import httpx

from ..schemas.requests import TTSRequest
from ..schemas.responses import TimingBreakdown
from ..schemas.voice import VoiceTurnRequest, VoiceTurnResult, VoiceTurnTimings
from .studio_service import StudioService
from .synthesis_service import SynthesisService
from ..utils.text import normalize_text


class VoiceTurnService:
    _BLOCK_TAG_PATTERNS = (
        re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<tool_call>.*?</tool_call>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<tool_response>.*?</tool_response>", re.IGNORECASE | re.DOTALL),
    )
    _INLINE_TOKEN_PATTERNS = (
        re.compile(r"<\|reserved_\d+\|>", re.IGNORECASE),
        re.compile(r"<reserved_\d+>", re.IGNORECASE),
        re.compile(r"</?think>", re.IGNORECASE),
        re.compile(r"</?tool_call>", re.IGNORECASE),
        re.compile(r"</?tool_response>", re.IGNORECASE),
    )

    def __init__(
        self,
        settings,
        studio_service: StudioService,
        synthesis_service: SynthesisService,
        client_factory: Callable[..., httpx.AsyncClient] | None = None,
    ) -> None:
        self.settings = settings
        self.studio_service = studio_service
        self.synthesis_service = synthesis_service
        self.client_factory = client_factory or (lambda **kwargs: httpx.AsyncClient(timeout=45.0, **kwargs))

    @staticmethod
    def _content_text(content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str) and item.strip():
                    parts.append(item.strip())
                    continue
                if not isinstance(item, dict):
                    continue
                if isinstance(item.get("text"), str) and item["text"].strip():
                    parts.append(item["text"].strip())
                    continue
                if item.get("type") == "output_text" and isinstance(item.get("text"), str) and item["text"].strip():
                    parts.append(item["text"].strip())
            return "\n".join(parts).strip()
        return ""

    @classmethod
    def _extract_response_text(cls, payload: Any) -> str:
        if not isinstance(payload, dict):
            return ""
        choices = payload.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message") if isinstance(choices[0], dict) else None
            if isinstance(message, dict):
                text = cls._content_text(message.get("content"))
                if text:
                    return text
        output = payload.get("output")
        if isinstance(output, list):
            parts: list[str] = []
            for entry in output:
                if not isinstance(entry, dict):
                    continue
                text = cls._content_text(entry.get("content"))
                if text:
                    parts.append(text)
            if parts:
                return "\n".join(parts).strip()
        return cls._content_text(payload.get("content"))

    @classmethod
    def _sanitize_response_text(cls, text: str) -> str:
        cleaned = text or ""
        for pattern in cls._BLOCK_TAG_PATTERNS:
            cleaned = pattern.sub(" ", cleaned)
        for pattern in cls._INLINE_TOKEN_PATTERNS:
            cleaned = pattern.sub(" ", cleaned)
        cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
        cleaned = normalize_text(cleaned)
        return cleaned.strip()

    @staticmethod
    def _upstream_error_detail(response: httpx.Response) -> str:
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail") or payload.get("error") or payload.get("message")
                if isinstance(detail, dict):
                    return json.dumps(detail)
                if isinstance(detail, str) and detail.strip():
                    return detail.strip()
        except Exception:
            pass
        return response.text.strip() or response.reason_phrase or "LLM request failed"

    async def generate_turn(self, request: VoiceTurnRequest) -> VoiceTurnResult:
        transcript_text = request.transcript_text.strip()
        if not transcript_text:
            raise ValueError("A finalized transcript is required before generating a voice turn.")

        routing = self.studio_service.get_routing()
        if not routing.enabled:
            raise ValueError("Studio LLM routing is disabled. Save an enabled provider/model in TTS Studio first.")
        if not routing.model:
            raise ValueError("Studio LLM routing does not have a model selected yet.")

        base_url, headers = self.studio_service.resolve_provider_request_config(
            routing.provider,
            base_url_override=routing.base_url,
        )
        llm_started = time.perf_counter()
        llm_payload = {
            "model": routing.model,
            "messages": [
                {
                    "role": "system",
                    "content": routing.system_prompt or "Respond with short, spoken-ready voice agent replies.",
                },
                {"role": "user", "content": transcript_text},
            ],
            "stream": False,
            "temperature": 0.2,
        }

        async with self.client_factory(base_url=base_url) as client:
            response = await client.post("/chat/completions", headers=headers, json=llm_payload)
            if not response.is_success:
                raise RuntimeError(f"LLM generation failed: {self._upstream_error_detail(response)}")
            llm_response = response.json()

        response_text = self._sanitize_response_text(self._extract_response_text(llm_response))
        if not response_text:
            raise RuntimeError("LLM generation returned an empty reply.")

        llm_total_ms = int((time.perf_counter() - llm_started) * 1000)
        metadata = dict(request.metadata)
        extra = dict(metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        extra.update(
            {
                "source_transcript_text": transcript_text,
                "llm_provider": routing.provider,
                "llm_model_requested": routing.model,
                "llm_base_url": base_url,
                "llm_request_id": llm_response.get("id"),
            }
        )
        metadata["extra"] = extra

        tts_request = TTSRequest(
            request_id=request.request_id,
            session_id=request.session_id,
            tenant_id=request.tenant_id,
            model=request.tts_model,
            voice=request.voice,
            text=response_text,
            format=request.format,
            sample_rate=request.sample_rate,
            stream=False,
            style=request.style,
            metadata=metadata,
        )
        tts_result, _audio_bytes = await self.synthesis_service.synthesize(tts_request)
        tts_timings = tts_result.timings
        return VoiceTurnResult(
            request_id=request.request_id,
            transcript_text=transcript_text,
            response_text=response_text,
            llm_provider=routing.provider,
            llm_model_requested=routing.model,
            llm_model_used=str(llm_response.get("model") or routing.model),
            llm_base_url=base_url,
            llm_request_id=str(llm_response.get("id")) if llm_response.get("id") else None,
            llm_timings=TimingBreakdown(inference_ms=llm_total_ms, total_ms=llm_total_ms),
            tts_model_requested=request.tts_model,
            tts_model_used=tts_result.model_used,
            audio_url=tts_result.audio_url,
            duration_ms=tts_result.duration_ms,
            tts_timings=tts_timings,
            timings=VoiceTurnTimings(
                llm_ms=llm_total_ms,
                tts_ms=tts_timings.total_ms,
                total_ms=llm_total_ms + tts_timings.total_ms,
            ),
            artifacts={
                **dict(tts_result.artifacts),
                "llm_provider": routing.provider,
                "llm_model_requested": routing.model,
                "llm_model_used": str(llm_response.get("model") or routing.model),
            },
        )
