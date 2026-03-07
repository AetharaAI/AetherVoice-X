def speech_detected(payload: bytes) -> bool:
    return any(byte != 0 for byte in payload[:256])
