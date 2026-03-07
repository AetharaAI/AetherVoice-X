from __future__ import annotations

import tempfile
from pathlib import Path

from .base import BaseASRAdapter
from ..logging import logger
from ..schemas.requests import ASRFileRequest, ASRStreamStartRequest, AudioFrame
from ..schemas.responses import ASRResult, ASRSegment, StreamSession, TimingBreakdown
from ..utils.audio_io import decode_payload_b64, pcm16_to_wav_bytes
from ..utils.time import elapsed_ms

try:
    from faster_whisper import WhisperModel
except Exception:  # pragma: no cover - optional import at runtime
    WhisperModel = None


class FasterWhisperAdapter(BaseASRAdapter):
    name = "faster_whisper"
    supports_streaming = True
    supports_batch = True
    supports_timestamps = True
    supports_language_detection = True

    def __init__(self, model_source: str, device: str, compute_type: str) -> None:
        self.model_source = model_source
        self.device = device
        self.compute_type = compute_type
        self._model = None
        self._sessions: dict[str, dict] = {}

    def _get_model(self):
        if WhisperModel is None:
            raise RuntimeError("faster-whisper is not installed in this environment")
        if self._model is None:
            logger.info("loading_faster_whisper_model", extra={"model_used": self.model_source})
            self._model = WhisperModel(self.model_source, device=self.device, compute_type=self.compute_type)
        return self._model

    async def transcribe_file(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        started = __import__("time").perf_counter()
        timings = TimingBreakdown(queue_ms=0, preprocess_ms=0, inference_ms=0, postprocess_ms=0, total_ms=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
            handle.write(audio_bytes)
            tmp_path = Path(handle.name)
        try:
            model = self._get_model()
            inference_started = __import__("time").perf_counter()
            segments_iter, info = model.transcribe(
                str(tmp_path),
                language=None if request.language == "auto" else request.language,
                task=request.task,
                vad_filter=True,
            )
            timings.inference_ms = elapsed_ms(inference_started)
            segments = [
                ASRSegment(
                    segment_id=f"seg_{index}",
                    start_ms=int(segment.start * 1000),
                    end_ms=int(segment.end * 1000),
                    text=segment.text.strip(),
                    confidence=getattr(segment, "avg_logprob", None),
                )
                for index, segment in enumerate(segments_iter, start=1)
            ]
            text = " ".join(segment.text for segment in segments).strip()
            timings.total_ms = elapsed_ms(started)
            return ASRResult(
                request_id=request.request_id,
                session_id=request.session_id,
                task=request.task,
                model_requested=request.model,
                model_used=self.name,
                language_detected=getattr(info, "language", request.language if request.language != "auto" else None),
                duration_ms=segments[-1].end_ms if segments else 0,
                text=text,
                segments=segments,
                timings=timings,
            )
        finally:
            tmp_path.unlink(missing_ok=True)

    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        self._sessions[request.session_id] = {
            "request": request,
            "buffer": bytearray(),
            "seq": 0,
            "last_partial": "",
        }
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)

    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[dict]:
        state = self._sessions[session_id]
        state["buffer"].extend(decode_payload_b64(frame.payload_b64))
        state["seq"] = frame.seq
        if frame.seq % 5 != 0:
            return []
        wav_bytes = pcm16_to_wav_bytes(bytes(state["buffer"]), sample_rate=frame.sample_rate, channels=frame.channels)
        request = ASRFileRequest(
            request_id=f"{session_id}_partial_{frame.seq}",
            session_id=session_id,
            tenant_id=state["request"].tenant_id,
            model=self.name,
            task="transcribe",
            language=state["request"].language,
            timestamps=True,
            metadata=state["request"].metadata,
        )
        result = await self.transcribe_file(request, wav_bytes)
        if not result.text or result.text == state["last_partial"]:
            return []
        state["last_partial"] = result.text
        return [
            {
                "type": "partial_transcript",
                "session_id": session_id,
                "seq": frame.seq,
                "stable": False,
                "text": result.text,
                "start_ms": result.segments[0].start_ms if result.segments else 0,
                "end_ms": result.segments[-1].end_ms if result.segments else frame.timestamp_ms,
            }
        ]

    async def end_stream(self, session_id: str) -> ASRResult:
        state = self._sessions.pop(session_id)
        wav_bytes = pcm16_to_wav_bytes(
            bytes(state["buffer"]),
            sample_rate=state["request"].sample_rate,
            channels=state["request"].channels,
        )
        request = ASRFileRequest(
            request_id=f"{session_id}_final",
            session_id=session_id,
            tenant_id=state["request"].tenant_id,
            model=self.name,
            task="transcribe",
            language=state["request"].language,
            timestamps=True,
            metadata=state["request"].metadata,
        )
        return await self.transcribe_file(request, wav_bytes)
