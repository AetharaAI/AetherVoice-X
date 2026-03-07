# Architecture

Aether Voice uses a gateway pattern to keep the external contract stable while inference backends remain swappable. The gateway handles auth, request validation, session lifecycle, route selection, and service-to-service fan-out. ASR and TTS services own model adapters, audio/text normalization, streaming orchestration, and artifact generation.

## Control plane

- Gateway exposes `/v1/*` to the UI, SDKs, and automation clients.
- Redis stores hot session state for live streams.
- Postgres stores durable sessions, request timings, transcripts, triage results, and TTS outputs.
- MinIO stores raw audio, normalized audio, transcript JSON, and synthesized audio.

## Data plane

- File ASR flows: client -> gateway -> ASR service -> storage + metadata -> gateway response.
- File TTS flows: client -> gateway -> TTS service -> storage + metadata -> gateway response.
- Streaming flows use WebSocket proxying through the gateway so the public connection topology stays fixed.

## Routing

- `auto` model resolution happens inside the gateway policy engine.
- ASR uses batch-first `faster-whisper` and streaming fallback when realtime adapters are unavailable.
- TTS prefers `moss_realtime` for conversational streaming and `chatterbox` for batch synthesis.
