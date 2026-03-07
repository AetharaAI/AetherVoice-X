# Telemetry

Each service emits JSON logs with request and session identifiers when available. Prometheus metrics are exposed at `/metrics` internally and surfaced publicly as `/v1/metrics` from the gateway.

Key metrics:

- `voice_requests_total`
- `voice_request_errors_total`
- `voice_request_duration_ms`
- `voice_asr_stream_time_to_first_partial_ms`
- `voice_asr_stream_time_to_final_ms`
- `voice_tts_time_to_first_chunk_ms`
- `voice_active_sessions`
- `voice_model_fallback_total`
- `voice_queue_depth`
