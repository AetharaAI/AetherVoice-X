from __future__ import annotations

import io

from pydub import AudioSegment


def normalize_audio(payload: bytes, *, format_hint: str | None = None, target_sample_rate: int = 16000) -> bytes:
    audio = AudioSegment.from_file(io.BytesIO(payload), format=format_hint)
    audio = audio.set_channels(1).set_frame_rate(target_sample_rate).set_sample_width(2)
    output = io.BytesIO()
    audio.export(output, format="wav")
    return output.getvalue()
