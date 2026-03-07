from __future__ import annotations

import base64


def audio_to_b64(payload: bytes) -> str:
    return base64.b64encode(payload).decode("utf-8")
