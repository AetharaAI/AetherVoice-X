# API Contracts

Public routes are exposed by the gateway:

- `GET /v1/health`
- `GET /v1/models`
- `GET /v1/metrics`
- `POST /v1/asr/transcribe`
- `POST /v1/asr/stream/start`
- `WS /v1/asr/stream/{session_id}`
- `POST /v1/asr/triage`
- `POST /v1/asr/analyze`
- `POST /v1/tts/synthesize`
- `POST /v1/tts/stream/start`
- `WS /v1/tts/stream/{session_id}`
- `GET /v1/sessions`
- `GET /v1/sessions/{session_id}`
- `POST /v1/sessions/{session_id}/end`

The request and response shapes follow the spec prompt and are implemented as Pydantic models in gateway and worker services.
