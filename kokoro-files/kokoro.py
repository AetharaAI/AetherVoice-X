"""
Kokoro TTS Module - hexgrad/Kokoro-82M
Fast, streaming text-to-speech synthesis
"""
import asyncio
import logging
import time
import io
import wave
from pathlib import Path
from typing import Dict, AsyncGenerator, Optional

import torch
import numpy as np
import soundfile as sf  # keep around if you want to dump to disk later

from kokoro import KModel, KPipeline  # <- real Kokoro API
from config import settings

logger = logging.getLogger(__name__)


class KokoroTTS:
    """
    Kokoro-82M TTS for streaming speech synthesis

    Model: hexgrad/Kokoro-82M (Apache-2.0)
    Features:
    - High-quality, small model (82M)
    - Multiple voices (af_sky, af_heart, etc.)
    - Streaming-style generation (chunked text)
    """

    def __init__(self, model_path: Path, device_id: str):
        # We keep model_path for future local overrides,
        # but Kokoro itself manages weights via HF cache.
        self.model_path = model_path

        # Device string: "cuda" or "cpu"
        if device_id and torch.cuda.is_available():
            self.device = f"cuda:{device_id}"
        else:
            self.device = "cpu"

        # Kokoro pieces
        self.kmodel: Optional[KModel] = None   # actual neural TTS model
        self.pipeline: Optional[KPipeline] = None  # text/phoneme pipeline

        self.sample_rate = settings.tts_sample_rate  # 24000 Hz

        self.metrics = {
            "total_requests": 0,
            "total_chars_synthesized": 0,
            "avg_ttfb_ms": 0.0,
            "avg_rtf": 0.0,
        }

        self._load_model()

    def _load_model(self):
        """Load Kokoro-82M model + pipeline via official API."""
        logger.info(f"Loading Kokoro-82M from HF cache (device={self.device})")

        try:
            use_gpu = self.device.startswith("cuda") and torch.cuda.is_available()
            model_device = "cuda" if use_gpu else "cpu"

            # This will download weights once into HF cache (which you
            # already pointed at /mnt/aetherpro/hf), then reuse them.
            self.kmodel = KModel().to(model_device).eval()

            # 'a' = American English (see Kokoro docs for others)
            self.pipeline = KPipeline(lang_code="a", model=False)

            logger.info(f"✅ Kokoro-82M loaded (model on {model_device})")

        except Exception as e:
            logger.error(f"Failed to load Kokoro-82M: {e}")
            logger.warning("Using silent audio placeholder for TTS")
            self.kmodel = None
            self.pipeline = None

    async def synthesize_stream(
        self,
        text: str,
        voice: str = "af_sky",  # Default Kokoro voice
        speed: float = 1.0,
    ) -> AsyncGenerator[bytes, None]:
        """
        Synthesize speech with streaming output.

        Args:
            text: Text to synthesize
            voice: Voice ID (af_sky, af_bella, am_adam, etc.)
            speed: Speech rate multiplier

        Yields:
            WAV audio chunks (16-bit PCM)
        """
        start_time = time.time()
        self.metrics["total_requests"] += 1
        self.metrics["total_chars_synthesized"] += len(text)

        sentences = self._split_sentences(text)
        first_chunk = True

        for sentence in sentences:
            if not sentence.strip():
                continue

            audio_chunk = await self._synthesize_sentence(sentence, voice, speed)

            if first_chunk:
                ttfb_ms = (time.time() - start_time) * 1000
                self.metrics["avg_ttfb_ms"] = (
                    self.metrics["avg_ttfb_ms"] * 0.9 + ttfb_ms * 0.1
                )
                logger.debug(f"TTS TTFB: {ttfb_ms:.1f}ms")
                first_chunk = False

            yield self._create_wav_chunk(audio_chunk)

        total_time = time.time() - start_time
        audio_duration = self._estimate_duration(text, speed)
        rtf = total_time / audio_duration if audio_duration > 0 else 0.0

        self.metrics["avg_rtf"] = self.metrics["avg_rtf"] * 0.9 + rtf * 0.1

    async def _synthesize_sentence(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> np.ndarray:
        """Synthesize a single sentence (async wrapper)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._synthesize_sync, text, voice, speed
        )

    def _synthesize_sync(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> np.ndarray:
        """Synchronous synthesis using Kokoro pipeline + model."""

        # If Kokoro isn't loaded, fall back to silence so the pipeline
        # still works while you debug.
        if self.kmodel is None or self.pipeline is None:
            duration_sec = len(text) * 0.08 / max(speed, 1e-3)
            num_samples = int(duration_sec * self.sample_rate)
            logger.warning(f"[Kokoro] Using silent placeholder for: {text[:80]!r}")
            return np.zeros(num_samples, dtype=np.float32)

        try:
            pipeline = self.pipeline
            model = self.kmodel

            # Preload the voice pack once for this call
            pack = pipeline.load_voice(voice)

            audio_chunks = []

            # This mirrors hexgrad's official HF Space logic: pipeline
            # yields (gs, ps, audio_placeholder). We ignore the placeholder
            # audio and call KModel ourselves.
            for _, ps, _ in pipeline(text, voice, speed):
                ref_s = pack[len(ps) - 1]
                with torch.no_grad():
                    audio = model(ps, ref_s, speed)

                if isinstance(audio, torch.Tensor):
                    audio = audio.cpu().numpy()

                audio_chunks.append(audio)

            if not audio_chunks:
                duration_sec = len(text) * 0.08 / max(speed, 1e-3)
                num_samples = int(duration_sec * self.sample_rate)
                return np.zeros(num_samples, dtype=np.float32)

            audio = np.concatenate(audio_chunks).astype(np.float32)
            return audio

        except Exception as e:
            logger.error(f"Synthesis error in Kokoro: {e}")
            duration_sec = len(text) * 0.08 / max(speed, 1e-3)
            num_samples = int(duration_sec * self.sample_rate)
            return np.zeros(num_samples, dtype=np.float32)

    def _split_sentences(self, text: str) -> list:
        """Split text into sentences for progressive synthesis."""
        import re

        parts = re.split(r"([.!?]+\s+)", text)
        result = []

        for i in range(0, len(parts) - 1, 2):
            sentence = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
            result.append(sentence)

        if len(parts) % 2 == 1:
            result.append(parts[-1])

        return [s for s in result if s.strip()]

    def _create_wav_chunk(self, audio: np.ndarray) -> bytes:
        """Convert numpy audio to WAV bytes."""
        audio_int16 = (audio * 32767.0).clip(-32768, 32767).astype(np.int16)

        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        return wav_buffer.getvalue()

    def _estimate_duration(self, text: str, speed: float) -> float:
        """Rough duration estimate for metrics."""
        words = len(text.split())
        duration_sec = (words / 150.0) * 60.0 / max(speed, 1e-3)
        return max(duration_sec, 0.1)

    def get_metrics(self) -> Dict:
        """Return metrics."""
        return {f"tts_{k}": v for k, v in self.metrics.items()}

    def get_voices(self) -> list:
        """Return available Kokoro voices."""
        return [
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

    def is_loaded(self) -> bool:
        """Check if model is ready."""
        return self.kmodel is not None and self.pipeline is not None

    def get_info(self) -> Dict:
        """Return model info for API."""
        return {
            "name": "kokoro",
            "description": "Fast TTS (82M params) - ideal for realtime/streaming",
            "sample_rate": self.sample_rate,
            "supports_cloning": False,
            "supports_streaming": True,
            "latency": "low (~100-300ms TTFB)",
            "voices": self.get_voices(),
            "loaded": self.is_loaded(),
        }

    def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up Kokoro TTS")
        self.kmodel = None
        self.pipeline = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
