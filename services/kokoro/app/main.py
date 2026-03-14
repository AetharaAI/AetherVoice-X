from __future__ import annotations

import base64
import io
import logging
import os
import re
import time
import wave
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from kokoro import KModel, KPipeline


logger = logging.getLogger("kokoro_realtime")


class StreamStartRequest(BaseModel):
    session_id: str
    model: str
    voice: str = "af_sky"
    sample_rate: int = 24000
    format: str = "wav"
    context_mode: str = "conversation"
    metadata: dict[str, Any] = Field(default_factory=dict)


class TextChunkRequest(BaseModel):
    text: str


@dataclass
class SessionState:
    session_id: str
    voice: str
    sample_rate: int
    output_format: str
    context_mode: str
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: float = field(default_factory=time.perf_counter)
    first_chunk_at: float | None = None
    chunk_count: int = 0
    chunks: list[np.ndarray] = field(default_factory=list)


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value not in {None, ""} else default


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value not in {None, ""} else default


VOICE_CATALOG = [
    {"id": "af_sky", "name": "Sky", "gender": "female", "accent": "american"},
    {"id": "af_bella", "name": "Bella", "gender": "female", "accent": "american"},
    {"id": "af_heart", "name": "Heart", "gender": "female", "accent": "american"},
    {"id": "af_nicole", "name": "Nicole", "gender": "female", "accent": "american"},
    {"id": "af_sarah", "name": "Sarah", "gender": "female", "accent": "american"},
    {"id": "am_adam", "name": "Adam", "gender": "male", "accent": "american"},
    {"id": "am_michael", "name": "Michael", "gender": "male", "accent": "american"},
    {"id": "bf_emma", "name": "Emma", "gender": "female", "accent": "british"},
    {"id": "bf_isabella", "name": "Isabella", "gender": "female", "accent": "british"},
    {"id": "bm_george", "name": "George", "gender": "male", "accent": "british"},
    {"id": "bm_lewis", "name": "Lewis", "gender": "male", "accent": "british"},
]


class KokoroRuntime:
    def __init__(self) -> None:
        configured = os.getenv("KOKORO_DEVICE", "cuda:0")
        if configured.startswith("cuda") and not torch.cuda.is_available():
            self.device = torch.device("cpu")
        else:
            self.device = torch.device(configured)
        self.sample_rate = _env_int("KOKORO_SAMPLE_RATE", 24000)
        self.default_voice = os.getenv("KOKORO_DEFAULT_VOICE", "af_sky").strip() or "af_sky"
        self.model_id = os.getenv("KOKORO_MODEL_ID", "hexgrad/Kokoro-82M").strip() or "hexgrad/Kokoro-82M"
        self.model_path = os.getenv("KOKORO_MODEL_PATH", "/models/audio/kokoro").strip() or "/models/audio/kokoro"
        self.lang_code = os.getenv("KOKORO_LANG_CODE", "a").strip() or "a"
        self.voice_packs: dict[str, Any] = {}
        self.sessions: dict[str, SessionState] = {}
        self.metrics = {"requests": 0, "chunks": 0, "avg_ttfb_ms": 0.0}

        logger.info("kokoro_runtime_loading", extra={"device": str(self.device), "model_id": self.model_id})
        model_device = "cuda" if self.device.type == "cuda" else "cpu"
        self.model = KModel().to(model_device).eval()
        self.pipeline = KPipeline(lang_code=self.lang_code, model=False)
        logger.info("kokoro_runtime_loaded", extra={"device": model_device, "default_voice": self.default_voice})

    def _resolve_voice(self, voice: str | None) -> str:
        candidate = (voice or "").strip()
        if not candidate or candidate == "default":
            return self.default_voice
        valid = {entry["id"] for entry in VOICE_CATALOG}
        return candidate if candidate in valid else self.default_voice

    def _voice_pack(self, voice: str) -> Any:
        if voice not in self.voice_packs:
            self.voice_packs[voice] = self.pipeline.load_voice(voice)
        return self.voice_packs[voice]

    @staticmethod
    def _split_text(text: str) -> list[str]:
        normalized = re.sub(r"\s+", " ", text or "").strip()
        if not normalized:
            return []
        parts = re.split(r"([.!?]+\s+)", normalized)
        chunks: list[str] = []
        for index in range(0, len(parts) - 1, 2):
            chunk = (parts[index] + (parts[index + 1] if index + 1 < len(parts) else "")).strip()
            if chunk:
                chunks.append(chunk)
        if len(parts) % 2 == 1 and parts[-1].strip():
            chunks.append(parts[-1].strip())
        return chunks or [normalized]

    def _speed_from_metadata(self, metadata: dict[str, Any] | None) -> float:
        extra = metadata.get("extra") if isinstance(metadata, dict) else {}
        tuning = extra.get("realtime_tuning") if isinstance(extra, dict) else {}
        raw = tuning.get("speed") if isinstance(tuning, dict) else None
        try:
            speed = float(raw) if raw not in {None, ""} else _env_float("KOKORO_DEFAULT_SPEED", 1.0)
        except (TypeError, ValueError):
            speed = 1.0
        return min(max(speed, 0.5), 2.0)

    @staticmethod
    def _wav_bytes(audio: np.ndarray, sample_rate: int) -> bytes:
        clipped = np.clip(audio, -1.0, 1.0)
        audio_int16 = (clipped * 32767.0).astype(np.int16)
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
        return buffer.getvalue()

    def _synthesize_sentence(self, text: str, *, voice: str, speed: float) -> np.ndarray:
        pack = self._voice_pack(voice)
        outputs: list[np.ndarray] = []
        for _, phonemes, _ in self.pipeline(text, voice, speed):
            reference = pack[len(phonemes) - 1]
            with torch.inference_mode():
                audio = self.model(phonemes, reference, speed)
            if isinstance(audio, torch.Tensor):
                audio = audio.detach().cpu().numpy()
            outputs.append(np.asarray(audio, dtype=np.float32))
        if not outputs:
            duration_sec = max(len(text.split()) * 0.18 / max(speed, 1e-3), 0.1)
            return np.zeros(int(duration_sec * self.sample_rate), dtype=np.float32)
        return np.concatenate(outputs).astype(np.float32)

    def start_stream(self, request: StreamStartRequest) -> dict[str, Any]:
        voice = self._resolve_voice(request.voice)
        self.sessions[request.session_id] = SessionState(
            session_id=request.session_id,
            voice=voice,
            sample_rate=request.sample_rate or self.sample_rate,
            output_format=request.format or "wav",
            context_mode=request.context_mode or "conversation",
            metadata=dict(request.metadata or {}),
        )
        return {
            "session_id": request.session_id,
            "model": "kokoro_realtime",
            "expires_in_seconds": 3600,
            "voice": voice,
        }

    def push_text(self, session_id: str, text: str) -> list[dict[str, Any]]:
        state = self.sessions.get(session_id)
        if state is None:
            raise KeyError(session_id)
        speed = self._speed_from_metadata(state.metadata)
        events: list[dict[str, Any]] = []
        for sentence in self._split_text(text):
            started = time.perf_counter()
            audio = self._synthesize_sentence(sentence, voice=state.voice, speed=speed)
            inference_ms = int((time.perf_counter() - started) * 1000)
            state.chunks.append(audio)
            state.chunk_count += 1
            self.metrics["chunks"] += 1
            if state.first_chunk_at is None:
                state.first_chunk_at = time.perf_counter()
                ttfb_ms = int((state.first_chunk_at - state.started_at) * 1000)
                self.metrics["avg_ttfb_ms"] = (self.metrics["avg_ttfb_ms"] * 0.9) + (ttfb_ms * 0.1)
            wav_bytes = self._wav_bytes(audio, state.sample_rate)
            events.append(
                {
                    "type": "audio_chunk",
                    "session_id": session_id,
                    "sequence": state.chunk_count,
                    "audio_b64": base64.b64encode(wav_bytes).decode("ascii"),
                    "format": state.output_format,
                    "metadata": {
                        "provider": "kokoro_realtime",
                        "voice": state.voice,
                        "chunk_text": sentence,
                        "timings": {"inference_ms": inference_ms},
                    },
                }
            )
        self.metrics["requests"] += 1
        return events

    def end_stream(self, session_id: str) -> dict[str, Any]:
        state = self.sessions.pop(session_id, None)
        if state is None:
            raise KeyError(session_id)
        final_audio = np.concatenate(state.chunks).astype(np.float32) if state.chunks else np.zeros(int(0.1 * state.sample_rate), dtype=np.float32)
        wav_bytes = self._wav_bytes(final_audio, state.sample_rate)
        duration_ms = int((len(final_audio) / state.sample_rate) * 1000)
        total_ms = int((time.perf_counter() - state.started_at) * 1000)
        return {
            "audio_b64": base64.b64encode(wav_bytes).decode("ascii"),
            "format": state.output_format,
            "duration_ms": duration_ms,
            "timings": {
                "inference_ms": total_ms,
                "total_ms": total_ms,
            },
            "artifacts": {
                "runtime_path_used": "kokoro_realtime",
                "live_chunk_source_route": "kokoro_realtime.sentence_stream",
                "final_artifact_source_route": "kokoro_realtime.final_concat",
                "actual_runtime_conditioning_source": state.voice,
                "selected_voice_id": state.voice,
            },
        }


runtime = KokoroRuntime()
app = FastAPI(title="Aether Voice Kokoro", version="1.0.0")


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "kokoro",
        "default_voice": runtime.default_voice,
        "sample_rate": runtime.sample_rate,
        "model_id": runtime.model_id,
        "model_path": runtime.model_path,
        "voices": [voice["id"] for voice in VOICE_CATALOG],
    }


@app.get("/v1/voices")
async def list_voices() -> dict[str, Any]:
    return {"voices": VOICE_CATALOG}


@app.post("/v1/stream/start")
async def start_stream(payload: StreamStartRequest) -> dict[str, Any]:
    return runtime.start_stream(payload)


@app.post("/v1/stream/{session_id}/text")
async def push_text(session_id: str, payload: TextChunkRequest) -> dict[str, Any]:
    try:
        events = runtime.push_text(session_id, payload.text)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown Kokoro session.") from exc
    return {"events": events}


@app.post("/v1/stream/{session_id}/complete")
async def complete_text(session_id: str) -> dict[str, Any]:
    if session_id not in runtime.sessions:
        raise HTTPException(status_code=404, detail="Unknown Kokoro session.")
    return {"events": []}


@app.post("/v1/stream/{session_id}/end")
async def end_stream(session_id: str) -> dict[str, Any]:
    try:
        return runtime.end_stream(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown Kokoro session.") from exc
