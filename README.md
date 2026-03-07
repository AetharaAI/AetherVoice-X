# Aether Voice

Aether Voice is a self-hosted voice infrastructure monorepo with a FastAPI gateway, dedicated ASR and TTS services, a React operator console, and local infrastructure for Redis, Postgres, MinIO, Prometheus, and Grafana.

## What ships in this substrate

- Gateway with public `/v1/*` REST and WebSocket routes
- ASR service with working batch transcription via `faster-whisper` and fallback micro-batch streaming
- TTS service with Chatterbox HTTP passthrough plus streaming scaffolds
- React + Vite operator console for live and file workflows
- Redis-backed active session state
- Postgres-backed session, request, transcript, triage, and TTS metadata
- MinIO/S3-compatible artifact storage with local filesystem fallback
- Structured logging and Prometheus metrics hooks

## Repository layout

```text
docs/                Architecture, contracts, deployment, security
infra/               Nginx, Prometheus, Grafana, Postgres, Redis, MinIO config
services/gateway/    Public API and routing
services/asr/        Transcription and triage
services/tts/        Synthesis and streaming
services/worker-common/
services/frontend/   React operator console
tests/               Unit, contract, integration, and load scaffolds
scripts/             Local lifecycle, smoke, and benchmark helpers
```

## Prerequisites

- Docker and Docker Compose
- `ffmpeg` available in containers for normalization and encoding

Optional for fully working adapters:

- A reachable Chatterbox-compatible HTTP service for TTS
- GPU runtime if you want production-grade `faster-whisper` throughput

## Quick start

1. Copy `.env.example` to `.env`.
2. Verify the model and cache paths in `.env` point to your mounted storage:

```env
HOST_MODEL_ROOT=/mnt/aetherpro/models
HOST_HF_CACHE_ROOT=/mnt/aetherpro/hf-cache
FASTER_WHISPER_MODEL_PATH=/models/audio/Systran/faster-whisper-large-v3
VOXTRAL_MODEL_PATH=/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602
QWEN3_ASR_MODEL_PATH=/models/audio/Qwen/Qwen3-ASR-1.7B
MOSS_MODEL_PATH=/models/audio/OpenMOSS-Team/MOSS-TTS-Realtime
CHATTERBOX_BASE_URL=https://tts.aetherpro.us
CHATTERBOX_DEFAULT_VOICE=Emily.wav
```

3. Start the stack:

```bash
docker compose up --build
```

On nodes that already run host nginx, the unified gateway and frontend are intentionally published only on `127.0.0.1` by default:

```env
HOST_BIND_IP=127.0.0.1
GATEWAY_PORT=8010
FRONTEND_PORT=3010
```

That matches a common host-nginx upstream layout and keeps the containers off the public internet.

4. Open:

- Frontend: `http://localhost:3000`
- Gateway Swagger: `http://localhost:8080/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`
- MinIO console: `http://localhost:9001`

## Local verification

Run the service tests:

```bash
PYTHONPATH=services/worker-common:services/gateway:services/asr:services/tts pytest tests/unit
```

Run the smoke helper against a running stack:

```bash
./scripts/smoke_test.sh
```

## Auth model

The default local profile uses `AUTH_MODE=optional` so the operator console can function without bootstrapping JWTs or API keys first. Production deployments should switch to `AUTH_MODE=strict`, seed tenants and API keys, and place the gateway behind your preferred upstream identity layer.

## Adapter status

- `faster_whisper`: implemented for file transcription and used for streaming fallback
- `chatterbox`: implemented as an HTTP passthrough adapter
- `voxtral_realtime`: scaffold
- `qwen3_asr`: scaffold
- `moss_realtime`: scaffold
- `sentinel`: rule-based scaffold for domain triage
- `phi_overlay`: scaffold

## Development notes

- Advanced model integrations are intentionally marked as scaffolds instead of fake implementations.
- The public API surface stays stable while model backends evolve behind adapters and routing policy.
