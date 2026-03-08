# Aether Voice

Aether Voice is a self-hosted voice infrastructure monorepo with a FastAPI gateway, dedicated ASR and TTS services, a React operator console, and local infrastructure for Redis, Postgres, MinIO, Prometheus, and Grafana.

## What ships in this substrate

- Gateway with public `/v1/*` REST and WebSocket routes
- ASR service with working batch transcription via `faster-whisper` and fallback micro-batch streaming
- TTS service with Chatterbox batch passthrough and OpenMOSS realtime streaming
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
- An OpenAI-compatible Voxtral upstream if you want the dedicated live ASR lane
- GPU runtime if you want the local OpenMOSS realtime TTS sidecar

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
MOSS_CODEC_MODEL_ID=OpenMOSS-Team/MOSS-Audio-Tokenizer
MOSS_REALTIME_BASE_URL=http://moss:8021
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
- `voxtral_realtime`: implemented against vLLM's `/v1/realtime` websocket when `VOXTRAL_REALTIME_BASE_URL` or `VOXTRAL_REALTIME_WS_URL` is configured
- `qwen3_asr`: scaffold
- `moss_realtime`: implemented against the local OpenMOSS sidecar when `MOSS_REALTIME_BASE_URL` is configured
- `sentinel`: rule-based scaffold for domain triage
- `phi_overlay`: scaffold

## Development notes

- Voxtral Realtime is documented by Mistral and vLLM to run through vLLM's realtime websocket API on `/v1/realtime`. This repo keeps the existing browser and gateway contracts stable and translates them inside the ASR service.
- You can launch a local Voxtral sidecar with `docker compose --profile voxtral up -d --build voxtral` and then set:
  - `VOXTRAL_REALTIME_BASE_URL=http://voxtral:8000`
  - `VOXTRAL_REALTIME_WS_URL=ws://voxtral:8000`
- The local Voxtral sidecar uses a dedicated Dockerfile that upgrades to the nightly audio-capable vLLM build, matching the current official guidance for Voxtral Realtime.
- OpenMOSS Realtime is not an OpenAI/vLLM realtime websocket. The local `moss` sidecar wraps the official OpenMOSS incremental `push_text -> end_text -> drain` session model and keeps the browser-facing `/v1/tts/stream/*` contract stable.
- You can launch the local OpenMOSS sidecar with `docker compose --profile moss up -d --build moss`. The TTS service will use `moss_realtime` automatically when `MOSS_REALTIME_BASE_URL` points at that sidecar and fall back to Chatterbox micro-batching when it does not.
- The public API surface stays stable while model backends evolve behind adapters and routing policy.
