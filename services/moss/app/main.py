from __future__ import annotations

import asyncio
import base64
import importlib.util
import io
import logging
import os
import time
import wave
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch
import torchaudio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer

from mossttsrealtime.modeling_mossttsrealtime import MossTTSRealtime
from mossttsrealtime.processing_mossttsrealtime import MossTTSRealtimeProcessor
from mossttsrealtime.streaming_mossttsrealtime import (
    AudioStreamDecoder,
    MossTTSRealtimeInference,
    MossTTSRealtimeStreamingSession,
)


ASSISTANT_PREFIX = "<|im_end|>\n<|im_start|>assistant\n"
logger = logging.getLogger("moss_realtime")


class StreamStartRequest(BaseModel):
    session_id: str
    model: str
    voice: str = "default"
    sample_rate: int = 24000
    format: str = "wav"
    context_mode: str = "conversation"
    metadata: dict[str, Any] = Field(default_factory=dict)


class TextChunkRequest(BaseModel):
    text: str


@dataclass
class RuntimeAssets:
    device: torch.device
    dtype: torch.dtype
    model_source: str
    codec_source: str
    sample_rate: int
    max_length: int
    temperature: float
    top_p: float
    top_k: int
    repetition_penalty: float
    repetition_window: int
    prefill_text_len: int
    decode_chunk_frames: int
    decode_overlap_frames: int
    enable_compile: bool
    tokenizer: Any
    processor: Any
    model: Any
    codec: Any
    prompt_tokens: np.ndarray | None = None


@dataclass
class SessionState:
    session: Any
    decoder: AudioStreamDecoder
    sample_rate: int
    output_format: str
    requested_voice: str
    context_mode: str
    conditioning_source: str
    started_at: float = field(default_factory=time.perf_counter)
    first_chunk_at: float | None = None
    sequence: int = 0
    raw_audio_tokens: list[torch.Tensor] = field(default_factory=list)
    text_completed: bool = False


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value not in {None, ""} else default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value not in {None, ""} else default


def _resolve_device() -> torch.device:
    configured = os.getenv("MOSS_REALTIME_DEVICE", "cuda:0")
    if configured.startswith("cuda") and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(configured)


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value in {None, ""}:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_dtype(device: torch.device) -> torch.dtype:
    if device.type == "cuda":
        return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return torch.float32


def _resolve_attn_implementation(device: torch.device, dtype: torch.dtype) -> str:
    configured = (os.getenv("MOSS_REALTIME_ATTN_IMPLEMENTATION") or "").strip().lower()
    if configured and configured != "auto":
        return configured
    if (
        device.type == "cuda"
        and importlib.util.find_spec("flash_attn") is not None
        and dtype in {torch.float16, torch.bfloat16}
    ):
        major, _ = torch.cuda.get_device_capability()
        if major >= 8:
            return "flash_attention_2"
    if device.type == "cuda":
        return "sdpa"
    return "eager"


def _extract_codes(encode_result: Any) -> torch.Tensor:
    if isinstance(encode_result, dict):
        if "audio_codes" in encode_result:
            return encode_result["audio_codes"]
        if "codes_list" in encode_result:
            return encode_result["codes_list"][0]
    if hasattr(encode_result, "audio_codes"):
        return encode_result.audio_codes
    raise ValueError("Unsupported codec.encode output: expected audio codes.")


def _load_audio(path: str, target_sample_rate: int) -> torch.Tensor:
    wav, sr = torchaudio.load(path)
    if sr != target_sample_rate:
        wav = torchaudio.functional.resample(wav, sr, target_sample_rate)
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)
    return wav


def _sanitize_audio_tokens(tokens: torch.Tensor, *, codebook_size: int, audio_eos_token: int) -> torch.Tensor:
    if tokens.dim() == 3:
        tokens = tokens[0]
    if tokens.dim() == 1:
        tokens = tokens.unsqueeze(0)
    if tokens.numel() == 0:
        return tokens
    eos_rows = (tokens[:, 0] == audio_eos_token).nonzero(as_tuple=False)
    invalid_rows = ((tokens < 0) | (tokens >= codebook_size)).any(dim=1)
    stop_idx = None
    if eos_rows.numel() > 0:
        stop_idx = int(eos_rows[0].item())
    if invalid_rows.any():
        invalid_idx = int(invalid_rows.nonzero(as_tuple=False)[0].item())
        stop_idx = invalid_idx if stop_idx is None else min(stop_idx, invalid_idx)
    if stop_idx is not None:
        return tokens[:stop_idx]
    return tokens


def _wav_bytes_from_array(audio: np.ndarray, sample_rate: int) -> bytes:
    pcm = np.clip(audio.astype(np.float32), -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype(np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm16.tobytes())
    return buffer.getvalue()


def _chunk_event(runtime: RuntimeAssets, state: SessionState, session_id: str, wav: torch.Tensor) -> dict[str, Any] | None:
    if wav.numel() == 0:
        return None
    audio = wav.detach().cpu().numpy().reshape(-1)
    state.sequence += 1
    if state.first_chunk_at is None:
        state.first_chunk_at = time.perf_counter()
    return {
        "type": "audio_chunk",
        "session_id": session_id,
        "sequence": state.sequence,
        "audio_b64": base64.b64encode(_wav_bytes_from_array(audio, state.sample_rate)).decode("ascii"),
        "format": state.output_format,
        "metadata": {
            "sample_rate": state.sample_rate,
            "live_chunk_source_route": "moss_realtime.decoder_stream",
        },
    }


def _collect_live_events(
    runtime: RuntimeAssets,
    state: SessionState,
    session_id: str,
    audio_frames: list[torch.Tensor],
    *,
    codebook_size: int,
    audio_eos_token: int,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for frame in audio_frames:
        tokens = _sanitize_audio_tokens(frame.detach(), codebook_size=codebook_size, audio_eos_token=audio_eos_token)
        if tokens.numel() == 0:
            continue
        state.raw_audio_tokens.append(tokens.cpu())
        state.decoder.push_tokens(tokens)
        for wav in state.decoder.audio_chunks():
            event = _chunk_event(runtime, state, session_id, wav)
            if event is not None:
                events.append(event)
    return events


def _flush_decoder_events(runtime: RuntimeAssets, state: SessionState, session_id: str) -> list[dict[str, Any]]:
    flushed = state.decoder.flush()
    if flushed is None or flushed.numel() == 0:
        return []
    event = _chunk_event(runtime, state, session_id, flushed)
    return [event] if event is not None else []


def _drain_completed_text(
    runtime: RuntimeAssets,
    state: SessionState,
    session_id: str,
    *,
    codebook_size: int,
    audio_eos_token: int,
    flush_decoder: bool,
) -> list[dict[str, Any]]:
    events = _collect_live_events(
        runtime,
        state,
        session_id,
        list(state.session.end_text()),
        codebook_size=codebook_size,
        audio_eos_token=audio_eos_token,
    )
    while True:
        drained = list(state.session.drain(max_steps=1))
        if not drained:
            break
        events.extend(
            _collect_live_events(
                runtime,
                state,
                session_id,
                drained,
                codebook_size=codebook_size,
                audio_eos_token=audio_eos_token,
            )
        )
        if state.session.inferencer.is_finished:
            break
    if flush_decoder:
        events.extend(_flush_decoder_events(runtime, state, session_id))
    state.text_completed = True
    return events


def _decode_full_audio(runtime: RuntimeAssets, session_state: SessionState) -> tuple[bytes, int]:
    if not session_state.raw_audio_tokens:
        raise RuntimeError("No audio tokens produced for this session.")
    tokens = torch.cat(session_state.raw_audio_tokens, dim=0).to(runtime.device)
    decoded = runtime.codec.decode(tokens.permute(1, 0), chunk_duration=None)
    wav = decoded["audio"][0] if isinstance(decoded, dict) else decoded
    if isinstance(wav, np.ndarray):
        wav = torch.from_numpy(wav)
    if wav.dim() > 1:
        wav = wav.squeeze(0)
    audio = wav.detach().cpu().numpy().reshape(-1)
    duration_ms = int((audio.shape[0] / session_state.sample_rate) * 1000)
    return _wav_bytes_from_array(audio, session_state.sample_rate), duration_ms


def _assistant_only_input_ids(processor: MossTTSRealtimeProcessor, tokenizer, prompt_tokens: np.ndarray | None) -> np.ndarray:
    system_prompt = processor.make_ensemble(prompt_tokens)
    assistant_prefix_ids = tokenizer.encode(ASSISTANT_PREFIX)
    assistant_prefix = np.full(
        (len(assistant_prefix_ids), system_prompt.shape[1]),
        fill_value=processor.audio_channel_pad,
        dtype=np.int64,
    )
    assistant_prefix[:, 0] = assistant_prefix_ids
    return np.concatenate([system_prompt, assistant_prefix], axis=0)


def _build_runtime() -> RuntimeAssets:
    sample_rate = _env_int("MOSS_REALTIME_SAMPLE_RATE", 24000)
    device = _resolve_device()
    dtype = _resolve_dtype(device)
    if device.type == "cuda":
        torch.set_float32_matmul_precision("high")
    model_source = os.getenv("MOSS_MODEL_PATH") or os.getenv("MOSS_MODEL_ID") or "OpenMOSS-Team/MOSS-TTS-Realtime"
    codec_source = os.getenv("MOSS_CODEC_MODEL_PATH") or os.getenv("MOSS_CODEC_MODEL_ID") or "OpenMOSS-Team/MOSS-Audio-Tokenizer"
    attn_implementation = _resolve_attn_implementation(device, dtype)

    tokenizer = AutoTokenizer.from_pretrained(model_source)
    processor = MossTTSRealtimeProcessor(tokenizer)
    model = MossTTSRealtime.from_pretrained(
        model_source,
        attn_implementation=attn_implementation,
        torch_dtype=dtype,
    ).to(device)
    model.eval()

    codec = AutoModel.from_pretrained(codec_source, trust_remote_code=True).eval().to(device)

    prompt_tokens = None
    prompt_audio_path = os.getenv("MOSS_PROMPT_AUDIO_PATH")
    if prompt_audio_path:
        prompt_audio = _load_audio(prompt_audio_path, target_sample_rate=sample_rate)
        with torch.inference_mode():
            prompt_result = codec.encode(prompt_audio.unsqueeze(0).to(device))
        prompt_tokens = _extract_codes(prompt_result)
        if isinstance(prompt_tokens, torch.Tensor):
            prompt_tokens = prompt_tokens.squeeze(1).detach().cpu().numpy()

    return RuntimeAssets(
        device=device,
        dtype=dtype,
        model_source=model_source,
        codec_source=codec_source,
        sample_rate=sample_rate,
        max_length=_env_int("MOSS_REALTIME_MAX_LENGTH", 3000),
        temperature=_env_float("MOSS_REALTIME_TEMPERATURE", 0.8),
        top_p=_env_float("MOSS_REALTIME_TOP_P", 0.6),
        top_k=_env_int("MOSS_REALTIME_TOP_K", 30),
        repetition_penalty=_env_float("MOSS_REALTIME_REPETITION_PENALTY", 1.1),
        repetition_window=_env_int("MOSS_REALTIME_REPETITION_WINDOW", 50),
        prefill_text_len=_env_int("MOSS_REALTIME_PREFILL_TEXT_LEN", min(getattr(processor, "delay_tokens_len", 12), 6)),
        decode_chunk_frames=_env_int("MOSS_REALTIME_DECODE_CHUNK_FRAMES", 40),
        decode_overlap_frames=_env_int("MOSS_REALTIME_DECODE_OVERLAP_FRAMES", 4),
        enable_compile=_env_bool("MOSS_REALTIME_ENABLE_COMPILE", False),
        tokenizer=tokenizer,
        processor=processor,
        model=model,
        codec=codec,
        prompt_tokens=prompt_tokens,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime = _build_runtime()
    app.state.runtime = runtime
    app.state.sessions: dict[str, SessionState] = {}
    app.state.inference_lock = asyncio.Lock()
    yield
    app.state.sessions.clear()


app = FastAPI(title="Aether Voice OpenMOSS Runtime", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    return {
        "status": "ok",
        "model_source": runtime.model_source,
        "codec_source": runtime.codec_source,
        "device": str(runtime.device),
        "sample_rate": runtime.sample_rate,
    }


@app.post("/v1/stream/start")
async def start_stream(payload: StreamStartRequest) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    if payload.format != "wav":
        raise HTTPException(status_code=400, detail="Only wav output is currently supported for MOSS realtime.")
    if payload.sample_rate != runtime.sample_rate:
        raise HTTPException(
            status_code=400,
            detail=f"MOSS realtime sidecar is configured for {runtime.sample_rate} Hz audio.",
        )
    inferencer = MossTTSRealtimeInference(runtime.model, runtime.tokenizer, max_length=runtime.max_length)
    inferencer.reset_generation_state(keep_cache=False)
    if hasattr(inferencer, "_should_compile_local_transformer"):
        inferencer._should_compile_local_transformer = runtime.enable_compile
        if not runtime.enable_compile:
            inferencer._compiled_local_transformer = None
    session = MossTTSRealtimeStreamingSession(
        inferencer,
        runtime.processor,
        codec=runtime.codec,
        codec_sample_rate=runtime.sample_rate,
        codec_encode_kwargs={},
        prefill_text_len=runtime.prefill_text_len,
        temperature=runtime.temperature,
        top_p=runtime.top_p,
        top_k=runtime.top_k,
        do_sample=True,
        repetition_penalty=runtime.repetition_penalty,
        repetition_window=runtime.repetition_window,
    )
    if runtime.prompt_tokens is not None:
        session.set_voice_prompt_tokens(runtime.prompt_tokens)
    session.reset_turn(
        input_ids=_assistant_only_input_ids(runtime.processor, runtime.tokenizer, runtime.prompt_tokens),
        include_system_prompt=False,
        reset_cache=True,
    )
    decoder = AudioStreamDecoder(
        runtime.codec,
        chunk_frames=runtime.decode_chunk_frames,
        overlap_frames=runtime.decode_overlap_frames,
        decode_kwargs={"chunk_duration": -1},
        device=runtime.device,
    )
    app.state.sessions[payload.session_id] = SessionState(
        session=session,
        decoder=decoder,
        sample_rate=payload.sample_rate,
        output_format=payload.format,
        requested_voice=payload.voice,
        context_mode=payload.context_mode,
        conditioning_source=prompt_audio_path if (prompt_audio_path := os.getenv("MOSS_PROMPT_AUDIO_PATH")) else "moss_default_unconditioned",
    )
    logger.info(
        "moss_stream_started",
        extra={
            "session_id": payload.session_id,
            "requested_voice": payload.voice,
            "context_mode": payload.context_mode,
            "conditioning_source_used": app.state.sessions[payload.session_id].conditioning_source,
            "live_chunk_source_route": "moss_realtime.decoder_stream",
            "final_artifact_source_route": "moss_realtime.final_decode",
            "kv_cache_reuse": "session_local",
            "decode_chunk_frames": runtime.decode_chunk_frames,
            "decode_overlap_frames": runtime.decode_overlap_frames,
        },
    )
    return {"session_id": payload.session_id, "model": "moss_realtime", "expires_in_seconds": 3600}


@app.post("/v1/stream/{session_id}/text")
async def push_text(session_id: str, payload: TextChunkRequest) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    state: SessionState | None = app.state.sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Unknown MOSS stream session.")
    codebook_size = int(getattr(getattr(runtime.codec, "config", runtime.codec), "codebook_size", 1024))
    audio_eos_token = int(getattr(state.session.inferencer, "audio_eos_token", 1026))
    events: list[dict[str, Any]] = []
    async with app.state.inference_lock:
        if state.text_completed:
            raise HTTPException(status_code=409, detail="This MOSS stream turn is already completed. Start a new stream for another utterance.")
        audio_frames = list(state.session.push_text(payload.text))
        events = _collect_live_events(
            runtime,
            state,
            session_id,
            audio_frames,
            codebook_size=codebook_size,
            audio_eos_token=audio_eos_token,
        )
    logger.info(
        "moss_stream_text_push",
        extra={
            "session_id": session_id,
            "text_chars": len(payload.text),
            "requested_voice": state.requested_voice,
            "conditioning_source_used": state.conditioning_source,
            "chunk_events_emitted": len(events),
            "live_chunk_source_route": "moss_realtime.decoder_stream",
        },
    )
    return {"events": events}


@app.post("/v1/stream/{session_id}/complete")
async def complete_text(session_id: str) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    state: SessionState | None = app.state.sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Unknown MOSS stream session.")
    if state.text_completed:
        return {"events": []}
    codebook_size = int(getattr(getattr(runtime.codec, "config", runtime.codec), "codebook_size", 1024))
    audio_eos_token = int(getattr(state.session.inferencer, "audio_eos_token", 1026))
    async with app.state.inference_lock:
        events = _drain_completed_text(
            runtime,
            state,
            session_id,
            codebook_size=codebook_size,
            audio_eos_token=audio_eos_token,
            flush_decoder=True,
        )
    logger.info(
        "moss_stream_text_completed",
        extra={
            "session_id": session_id,
            "requested_voice": state.requested_voice,
            "conditioning_source_used": state.conditioning_source,
            "chunk_events_emitted": len(events),
            "live_chunk_source_route": "moss_realtime.decoder_stream",
            "kv_cache_reuse": "session_local",
        },
    )
    return {"events": events}


@app.post("/v1/stream/{session_id}/end")
async def end_stream(session_id: str) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    state: SessionState | None = app.state.sessions.pop(session_id, None)
    if state is None:
        raise HTTPException(status_code=404, detail="Unknown MOSS stream session.")
    codebook_size = int(getattr(getattr(runtime.codec, "config", runtime.codec), "codebook_size", 1024))
    audio_eos_token = int(getattr(state.session.inferencer, "audio_eos_token", 1026))
    async with app.state.inference_lock:
        if not state.text_completed:
            _drain_completed_text(
                runtime,
                state,
                session_id,
                codebook_size=codebook_size,
                audio_eos_token=audio_eos_token,
                flush_decoder=False,
            )
        audio_bytes, duration_ms = _decode_full_audio(runtime, state)

    total_ms = int((time.perf_counter() - state.started_at) * 1000)
    first_chunk_ms = 0
    if state.first_chunk_at is not None:
        first_chunk_ms = int((state.first_chunk_at - state.started_at) * 1000)
    logger.info(
        "moss_stream_finished",
        extra={
            "session_id": session_id,
            "requested_voice": state.requested_voice,
            "conditioning_source_used": state.conditioning_source,
            "chunk_count": state.sequence,
            "first_chunk_ms": first_chunk_ms,
            "duration_ms": duration_ms,
            "live_chunk_source_route": "moss_realtime.decoder_stream",
            "final_artifact_source_route": "moss_realtime.final_decode",
            "kv_cache_reuse": "session_local",
        },
    )
    return {
        "session_id": session_id,
        "audio_b64": base64.b64encode(audio_bytes).decode("ascii"),
        "format": state.output_format,
        "duration_ms": duration_ms,
        "timings": {
            "queue_ms": 0,
            "inference_ms": total_ms,
            "encode_ms": 0,
            "total_ms": total_ms,
        },
        "artifacts": {
            "format": state.output_format,
            "first_chunk_ms": first_chunk_ms,
            "chunk_count": state.sequence,
            "conditioning_source_used": state.conditioning_source,
            "live_chunk_source_route": "moss_realtime.decoder_stream",
            "final_artifact_source_route": "moss_realtime.final_decode",
        },
    }
