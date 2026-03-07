from __future__ import annotations

import base64
import io
import wave


def decode_payload_b64(payload_b64: str) -> bytes:
    return base64.b64decode(payload_b64.encode("utf-8"))


def pcm16_to_wav_bytes(frame_bytes: bytes, sample_rate: int = 16000, channels: int = 1) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frame_bytes)
    return buffer.getvalue()


def estimate_wav_duration_ms(payload: bytes) -> int:
    try:
        with wave.open(io.BytesIO(payload), "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            return int(frames / rate * 1000)
    except Exception:
        return 0
