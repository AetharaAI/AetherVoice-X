from __future__ import annotations

import asyncio
import base64
import importlib.util
import io
import logging
import os
import subprocess
import tempfile
import time
import wave
from copy import deepcopy
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import torch
import torchaudio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoProcessor


torch.backends.cuda.enable_cudnn_sdp(False)
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_math_sdp(True)

logger = logging.getLogger("moss_family")

FamilyKind = Literal["tts", "ttsd", "voice_generator", "soundeffect"]


class SynthesizeRequest(BaseModel):
    text: str
    format: str = "wav"
    sample_rate: int = 24000
    voice: str = "default"
    style: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WarmupRequest(BaseModel):
    metadata: dict[str, Any] = Field(default_factory=dict)


@dataclass
class RuntimeAssets:
    kind: FamilyKind
    device: torch.device
    dtype: torch.dtype
    model_source: str
    codec_source: str | None
    sample_rate: int
    max_new_tokens: int
    temperature: float
    top_p: float
    top_k: int
    repetition_penalty: float
    processor: Any
    model: Any


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value not in {None, ""} else default


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value not in {None, ""} else default


def _resolve_kind() -> FamilyKind:
    raw = (os.getenv("MOSS_FAMILY_KIND") or "tts").strip().lower()
    if raw not in {"tts", "ttsd", "voice_generator", "soundeffect"}:
        raise RuntimeError(f"Unsupported MOSS_FAMILY_KIND={raw}")
    return raw  # type: ignore[return-value]


def _resolve_device() -> torch.device:
    configured = os.getenv("MOSS_FAMILY_DEVICE", "cuda:0")
    if configured.startswith("cuda") and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(configured)


def _resolve_dtype(device: torch.device) -> torch.dtype:
    if device.type == "cuda":
        return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return torch.float32


def _resolve_attn_implementation(device: torch.device, dtype: torch.dtype) -> str | None:
    configured = (os.getenv("MOSS_FAMILY_ATTN_IMPLEMENTATION") or "auto").strip().lower()
    if configured == "none":
        return None
    if configured not in {"", "auto"}:
        return configured
    if (
        device.type == "cuda"
        and importlib.util.find_spec("flash_attn") is not None
        and dtype in {torch.float16, torch.bfloat16}
    ):
        major, _minor = torch.cuda.get_device_capability(device)
        if major >= 8:
            return "flash_attention_2"
    if device.type == "cuda":
        return "sdpa"
    return "eager"


def _kind_defaults(kind: FamilyKind) -> tuple[int, float, float, int, float]:
    if kind == "ttsd":
        return 2000, 1.2, 0.6, 50, 1.2
    if kind == "voice_generator":
        return 4096, 1.5, 0.6, 50, 1.2
    if kind == "soundeffect":
        return 4096, 1.5, 0.6, 50, 1.2
    return 4096, 0.8, 0.6, 50, 1.2


def _normalized_dialogue_text(text: str) -> str:
    cleaned = (text or "").replace("\n", " ").strip()
    cleaned = cleaned.replace("[1]", "[S1]").replace("[2]", "[S2]").replace("[3]", "[S3]").replace("[4]", "[S4]").replace("[5]", "[S5]")
    return cleaned


def _load_audio(path: str) -> tuple[torch.Tensor, int]:
    wav, sample_rate = torchaudio.load(Path(path).expanduser().as_posix())
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)
    return wav, int(sample_rate)


def _normalize_reference_audio(
    path: str,
    *,
    target_sample_rate: int,
    temp_dir: Path,
    prefix: str,
) -> tuple[str, dict[str, Any]]:
    source_path = Path(path).expanduser()
    if not source_path.exists():
        raise ValueError(f"Reference audio path does not exist: {source_path}")

    wav, sample_rate = torchaudio.load(source_path.as_posix())
    source_channels = int(wav.shape[0]) if wav.ndim > 1 else 1
    mono_mixed = False
    resampled = False

    if source_channels > 1:
        wav = wav.mean(dim=0, keepdim=True)
        mono_mixed = True

    if int(sample_rate) != int(target_sample_rate):
        wav = torchaudio.functional.resample(wav, int(sample_rate), int(target_sample_rate))
        resampled = True

    temp_dir.mkdir(parents=True, exist_ok=True)
    normalized_path = temp_dir / f"{prefix}_{source_path.stem}_{target_sample_rate}.wav"
    torchaudio.save(normalized_path.as_posix(), wav.cpu(), int(target_sample_rate))

    artifacts = {
        "original_reference_audio_path": source_path.as_posix(),
        "normalized_reference_audio_path": normalized_path.as_posix(),
        "reference_audio_source_sample_rate": int(sample_rate),
        "reference_audio_target_sample_rate": int(target_sample_rate),
        "reference_audio_source_channels": source_channels,
        "reference_audio_resampled": resampled,
        "reference_audio_mono_mixed": mono_mixed,
    }
    logger.info("moss_family_reference_audio_normalized", extra=artifacts)
    return normalized_path.as_posix(), artifacts


def _to_pcm_wav(audio_np: np.ndarray, sample_rate: int) -> bytes:
    pcm = np.clip(audio_np.astype(np.float32), -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype(np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm16.tobytes())
    return buffer.getvalue()


def _transcode_bytes(audio_bytes: bytes, output_format: str) -> bytes:
    if output_format == "wav":
        return audio_bytes
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "audio.wav"
        dst = Path(tmpdir) / f"audio.{output_format}"
        src.write_bytes(audio_bytes)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                src.as_posix(),
                dst.as_posix(),
            ],
            check=True,
            capture_output=True,
        )
        return dst.read_bytes()


def _extract_audio_np(messages: Any) -> np.ndarray:
    if not messages or messages[0] is None:
        raise RuntimeError("OpenMOSS did not return a decodable audio result.")
    audio = messages[0].audio_codes_list[0]
    if isinstance(audio, torch.Tensor):
        audio_np = audio.detach().float().cpu().numpy()
    else:
        audio_np = np.asarray(audio, dtype=np.float32)
    if audio_np.ndim > 1:
        audio_np = audio_np.reshape(-1)
    return audio_np.astype(np.float32, copy=False)


def _build_conversations(
    runtime: RuntimeAssets,
    request: SynthesizeRequest,
    *,
    temp_dir: Path | None = None,
) -> tuple[list[list[Any]], str, dict[str, Any]]:
    extra = dict(request.metadata.get("extra") or {}) if isinstance(request.metadata, dict) else {}
    resolved_voice = dict(extra.get("resolved_voice") or {})
    generation_prompt = (
        extra.get("generation_prompt")
        or request.metadata.get("generation_prompt")
        or resolved_voice.get("generation_prompt")
        or ""
    )
    reference_audio_path = extra.get("reference_audio_path") or resolved_voice.get("reference_audio_path")
    reference_text = extra.get("reference_text") or resolved_voice.get("reference_text")
    speaker_references = extra.get("speaker_references") or []
    artifacts: dict[str, Any] = {
        "requested_voice_id": resolved_voice.get("voice_id") or request.voice,
        "resolved_conditioning_asset": reference_audio_path or generation_prompt or None,
        "fallback_route_used": None,
    }
    processor = runtime.processor
    normalized_dir = temp_dir or Path(tempfile.mkdtemp(prefix="moss-family-ref-"))

    if runtime.kind == "voice_generator":
        instruction = str(generation_prompt or "").strip()
        if not instruction:
            raise ValueError("OpenMOSS Voice Generator requires a generation prompt.")
        conversations = [[processor.build_user_message(text=request.text.strip(), instruction=instruction)]]
        artifacts["actual_runtime_conditioning_source"] = f"instruction:{instruction[:120]}"
        artifacts["voice_generation_prompt"] = instruction
        return conversations, "generation", artifacts

    if runtime.kind == "soundeffect":
        duration_seconds = float(extra.get("duration_seconds") or 10)
        expected_tokens = max(1, int(duration_seconds * 12.5))
        conversations = [[processor.build_user_message(ambient_sound=request.text.strip(), tokens=expected_tokens)]]
        artifacts["actual_runtime_conditioning_source"] = "ambient_prompt"
        artifacts["requested_duration_seconds"] = duration_seconds
        return conversations, "generation", artifacts

    if runtime.kind == "ttsd":
        dialogue_text = _normalized_dialogue_text(request.text)
        conversations = [[processor.build_user_message(text=dialogue_text)]]
        if speaker_references:
            normalized_speakers: list[dict[str, Any]] = []
            original_speaker_paths: list[str] = []
            normalized_speaker_paths: list[str] = []
            speaker_normalization: list[dict[str, Any]] = []
            for index, speaker in enumerate(speaker_references):
                if not isinstance(speaker, dict):
                    normalized_speakers.append(speaker)
                    continue
                speaker_copy = deepcopy(speaker)
                audio_path = str(speaker_copy.get("audio_path") or "").strip()
                if audio_path:
                    normalized_path, normalization_artifacts = _normalize_reference_audio(
                        audio_path,
                        target_sample_rate=runtime.sample_rate,
                        temp_dir=normalized_dir,
                        prefix=f"speaker_{index}",
                    )
                    speaker_copy["audio_path"] = normalized_path
                    original_speaker_paths.append(audio_path)
                    normalized_speaker_paths.append(normalized_path)
                    speaker_normalization.append(
                        {
                            "speaker_index": index,
                            **normalization_artifacts,
                        }
                    )
                normalized_speakers.append(speaker_copy)
            artifacts["speaker_references"] = normalized_speakers
            if original_speaker_paths:
                artifacts["original_speaker_reference_paths"] = original_speaker_paths
                artifacts["normalized_speaker_reference_paths"] = normalized_speaker_paths
                artifacts["speaker_reference_normalization"] = speaker_normalization
        artifacts["actual_runtime_conditioning_source"] = (
            artifacts.get("normalized_speaker_reference_paths", [])[0]
            if artifacts.get("normalized_speaker_reference_paths")
            else (
                speaker_references[0].get("audio_path")
                if isinstance(speaker_references, list) and speaker_references and isinstance(speaker_references[0], dict)
                else "unconditioned_dialogue"
            )
        )
        return conversations, "generation", artifacts

    user_kwargs: dict[str, Any] = {"text": request.text.strip()}
    if reference_audio_path:
        normalized_path, normalization_artifacts = _normalize_reference_audio(
            str(reference_audio_path),
            target_sample_rate=runtime.sample_rate,
            temp_dir=normalized_dir,
            prefix="tts_reference",
        )
        user_kwargs["reference"] = [normalized_path]
        artifacts["actual_runtime_conditioning_source"] = normalized_path
        artifacts.update(normalization_artifacts)
    else:
        artifacts["actual_runtime_conditioning_source"] = "unconditioned_tts"
    if reference_text:
        artifacts["reference_text"] = reference_text
    conversations = [[processor.build_user_message(**user_kwargs)]]
    return conversations, "generation", artifacts


def _build_warmup_request(runtime: RuntimeAssets, metadata: dict[str, Any] | None = None) -> SynthesizeRequest:
    metadata = dict(metadata or {})
    if runtime.kind == "voice_generator":
        return SynthesizeRequest(
            text="AetherPro confirms the voice design warmup path is online.",
            metadata={
                **metadata,
                "extra": {
                    "generation_prompt": "Clear, modern, lightly motivational voice with practical focus, minimal fluff, and strong instructional cadence."
                },
            },
        )
    if runtime.kind == "ttsd":
        return SynthesizeRequest(
            text="[S1] The control room is online. [S2] Dialogue synthesis warmup complete.",
            metadata=metadata,
        )
    if runtime.kind == "soundeffect":
        return SynthesizeRequest(
            text="subtle synth confirmation tone with clean futuristic ambience",
            metadata={"extra": {"duration_seconds": 2}, **metadata},
        )
    return SynthesizeRequest(
        text="AetherPro confirms OpenMOSS batch synthesis is online.",
        metadata=metadata,
    )


def _run_generation(runtime: RuntimeAssets, request: SynthesizeRequest) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="moss-family-ref-") as temp_dir:
        conversations, mode, artifacts = _build_conversations(runtime, request, temp_dir=Path(temp_dir))
        batch = runtime.processor(conversations, mode=mode)
        input_ids = batch["input_ids"].to(runtime.device)
        attention_mask = batch["attention_mask"].to(runtime.device)

        with torch.no_grad():
            outputs = runtime.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=runtime.max_new_tokens,
                audio_temperature=runtime.temperature,
                audio_top_p=runtime.top_p,
                audio_top_k=runtime.top_k,
                audio_repetition_penalty=runtime.repetition_penalty,
            )

        messages = runtime.processor.decode(outputs)
        audio_np = _extract_audio_np(messages)
        wav_bytes = _to_pcm_wav(audio_np, runtime.sample_rate)
        final_bytes = _transcode_bytes(wav_bytes, request.format)
        duration_ms = int((len(audio_np) / float(runtime.sample_rate)) * 1000)
        return {
            "audio_bytes": final_bytes,
            "duration_ms": duration_ms,
            "artifacts": artifacts,
        }


def load_runtime() -> RuntimeAssets:
    kind = _resolve_kind()
    device = _resolve_device()
    dtype = _resolve_dtype(device)
    attn_implementation = _resolve_attn_implementation(device, dtype)
    default_tokens, default_temp, default_top_p, default_top_k, default_penalty = _kind_defaults(kind)
    model_source = os.getenv("MOSS_FAMILY_MODEL_PATH") or os.getenv("MOSS_FAMILY_MODEL_ID") or ""
    codec_source = os.getenv("MOSS_FAMILY_CODEC_MODEL_PATH") or os.getenv("MOSS_FAMILY_CODEC_MODEL_ID")
    if not model_source:
        raise RuntimeError("MOSS family sidecar requires MOSS_FAMILY_MODEL_PATH or MOSS_FAMILY_MODEL_ID.")

    model_kwargs: dict[str, Any] = {
        "trust_remote_code": True,
        "torch_dtype": dtype,
    }
    if attn_implementation:
        model_kwargs["attn_implementation"] = attn_implementation

    processor_kwargs: dict[str, Any] = {"trust_remote_code": True}
    if kind == "ttsd":
        if not codec_source:
            raise RuntimeError("TTSD requires MOSS_FAMILY_CODEC_MODEL_PATH or MOSS_FAMILY_CODEC_MODEL_ID.")
        processor_kwargs["codec_path"] = codec_source
    if kind == "voice_generator":
        processor_kwargs["normalize_inputs"] = True

    processor = AutoProcessor.from_pretrained(model_source, **processor_kwargs)
    if hasattr(processor, "audio_tokenizer"):
        processor.audio_tokenizer = processor.audio_tokenizer.to(device)
        if hasattr(processor.audio_tokenizer, "eval"):
            processor.audio_tokenizer.eval()

    model = AutoModel.from_pretrained(model_source, **model_kwargs).to(device)
    model.eval()
    if device.type == "cuda":
        torch.set_float32_matmul_precision("high")

    return RuntimeAssets(
        kind=kind,
        device=device,
        dtype=dtype,
        model_source=model_source,
        codec_source=codec_source,
        sample_rate=int(getattr(processor.model_config, "sampling_rate", _env_int("MOSS_FAMILY_SAMPLE_RATE", 24000))),
        max_new_tokens=_env_int("MOSS_FAMILY_MAX_NEW_TOKENS", default_tokens),
        temperature=_env_float("MOSS_FAMILY_TEMPERATURE", default_temp),
        top_p=_env_float("MOSS_FAMILY_TOP_P", default_top_p),
        top_k=_env_int("MOSS_FAMILY_TOP_K", default_top_k),
        repetition_penalty=_env_float("MOSS_FAMILY_REPETITION_PENALTY", default_penalty),
        processor=processor,
        model=model,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime = await asyncio.to_thread(load_runtime)
    app.state.runtime = runtime
    logger.info(
        "moss_family_ready",
        extra={
            "kind": runtime.kind,
            "model_source": runtime.model_source,
            "codec_source": runtime.codec_source,
            "device": str(runtime.device),
            "sample_rate": runtime.sample_rate,
        },
    )
    try:
        yield
    finally:
        runtime = app.state.runtime
        del runtime


app = FastAPI(title="OpenMOSS Family Sidecar", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    return {
        "status": "ok",
        "kind": runtime.kind,
        "model_source": runtime.model_source,
        "codec_source": runtime.codec_source,
        "device": str(runtime.device),
        "sample_rate": runtime.sample_rate,
    }


@app.post("/v1/synthesize")
async def synthesize(payload: SynthesizeRequest) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    started_at = time.perf_counter()
    try:
        result = await asyncio.to_thread(_run_generation, runtime, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - runtime depends on upstream model behavior
        logger.exception("moss_family_synthesis_failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    return {
        "model": f"moss_{runtime.kind}",
        "kind": runtime.kind,
        "format": payload.format,
        "sample_rate": runtime.sample_rate,
        "duration_ms": result["duration_ms"],
        "audio_b64": base64.b64encode(result["audio_bytes"]).decode("ascii"),
        "timings": {
            "inference_ms": elapsed_ms,
            "total_ms": elapsed_ms,
        },
        "artifacts": {
            **result["artifacts"],
            "runtime_path_used": f"moss_{runtime.kind}",
        },
    }


@app.post("/v1/warmup")
async def warmup(payload: WarmupRequest) -> dict[str, Any]:
    runtime: RuntimeAssets = app.state.runtime
    started_at = time.perf_counter()
    request = _build_warmup_request(runtime, payload.metadata)
    logger.info(
        "moss_family_warmup_started",
        extra={
            "kind": runtime.kind,
            "model_source": runtime.model_source,
            "device": str(runtime.device),
        },
    )
    try:
        result = await asyncio.to_thread(_run_generation, runtime, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - runtime depends on upstream model behavior
        logger.exception("moss_family_warmup_failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    logger.info(
        "moss_family_warmup_complete",
        extra={
            "kind": runtime.kind,
            "model_source": runtime.model_source,
            "device": str(runtime.device),
            "elapsed_ms": elapsed_ms,
            "duration_ms": result["duration_ms"],
        },
    )
    return {
        "status": "ok",
        "route": f"moss_{runtime.kind}",
        "elapsed_ms": elapsed_ms,
        "duration_ms": result["duration_ms"],
        "artifacts": {
            **result["artifacts"],
            "runtime_path_used": f"moss_{runtime.kind}",
        },
    }
