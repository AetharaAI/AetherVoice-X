from __future__ import annotations

from aether_common.telemetry import voice_active_sessions


class TelemetryService:
    def session_started(self) -> None:
        voice_active_sessions.labels(service="asr", kind="stream").inc()

    def session_ended(self) -> None:
        voice_active_sessions.labels(service="asr", kind="stream").dec()
