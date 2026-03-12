# Aether Voice X Infrastructure And Capability Summary

Date: March 12, 2026

This document is a factual engineering summary of what exists in the Aether Voice X repository and what has been observed working in the current stack. It is written to support fast understanding by a technical reviewer or proposal writer. It avoids speculation and does not describe capabilities that are not present in code or verified in the current operator workflow.

## 1. What This System Does

Aether Voice X is a self-hosted voice infrastructure stack for speech input, speech output, session tracking, and operator control. In plain language, it provides:

- live microphone transcription
- file-based transcription
- batch text-to-speech generation
- realtime text-to-speech streaming
- reusable voice presets and voice asset management
- session logging and transcript persistence
- a browser-based operator console for testing and operating the voice system

The repository is organized as a monorepo and contains the API gateway, ASR service, TTS service, GPU model sidecars, frontend console, local storage and metadata services, and monitoring configuration. See [README.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/README.md#L1).

## 2. System Architecture

### Core application services

- `services/gateway/`
  - public API surface
  - exposes REST and WebSocket routes under `/v1/*`
  - handles auth context, quota checks, request/session recording, and proxying to ASR and TTS services
  - main ASR stream routes are implemented in [services/gateway/app/routers/asr.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/asr.py#L132)
  - turn-based ASR -> LLM -> TTS route is implemented in [services/gateway/app/routers/voice.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/voice.py#L24)

- `services/asr/`
  - batch and streaming speech recognition service
  - contains adapter logic for `faster_whisper` and `voxtral_realtime`
  - Voxtral realtime adapter is implemented in [services/asr/app/adapters/voxtral_realtime.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/asr/app/adapters/voxtral_realtime.py#L39)

- `services/tts/`
  - batch TTS, realtime TTS streaming, studio voice registry, and turn-based voice reply orchestration
  - turn-based reply orchestration is implemented in [services/tts/app/services/voice_turn_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/voice_turn_service.py#L13)
  - voice registry and route catalog are implemented in [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py#L74)

- `services/frontend/`
  - React and Vite operator console
  - includes pages for live ASR, file ASR, live TTS, file TTS, TTS Studio, sessions, metrics, and models
  - live microphone transcription client is implemented in [services/frontend/src/hooks/useASRStream.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/hooks/useASRStream.ts#L1)
  - live ASR operator page is implemented in [services/frontend/src/pages/ASRLive.tsx](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/pages/ASRLive.tsx#L1)

### Model-serving sidecars

The repository includes dedicated GPU model sidecars defined in [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L1):

- `voxtral`
  - vLLM-based realtime ASR sidecar using `Voxtral-Mini-4B-Realtime-2602`
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L62)

- `moss`
  - OpenMOSS realtime TTS sidecar
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L123)

- `moss-tts`
  - OpenMOSS batch TTS sidecar
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L173)

- `moss-ttsd`
  - OpenMOSS dialogue TTS sidecar
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L212)

- `moss-voice-generator`
  - OpenMOSS voice design / voice generation sidecar
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L253)

- `moss-soundeffect`
  - OpenMOSS sound effect sidecar
  - service definition begins at [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L292)

### Data and monitoring services

The same compose stack includes:

- `postgres`
  - persistent transactional metadata and session state
- `redis`
  - active session coordination and runtime state
- `minio`
  - S3-compatible artifact storage
- `prometheus`
  - metrics collection
- `grafana`
  - dashboarding

These are defined in [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml#L370).

## 3. How The Main Components Connect

### Live ASR path

The live ASR operator path works as follows:

1. The browser calls `POST /v1/asr/stream/start` on the gateway.
2. The gateway creates a live ASR session and chooses a model route.
3. The gateway returns a websocket path such as `/api/v1/asr/stream/{session_id}`.
4. The browser opens the gateway websocket and sends JSON `audio_frame` messages containing base64 PCM16 mono audio.
5. The gateway proxies that websocket to the internal ASR service.
6. The ASR service uses the `voxtral_realtime` adapter to connect upstream to the Voxtral `/v1/realtime` websocket.
7. Partial and final transcript events are returned through the gateway websocket to the browser.

This flow is implemented across:

- [services/frontend/src/hooks/useASRStream.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/hooks/useASRStream.ts#L1)
- [services/gateway/app/routers/asr.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/asr.py#L132)
- [services/asr/app/adapters/voxtral_realtime.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/asr/app/adapters/voxtral_realtime.py#L39)

### Batch ASR path

The batch ASR path accepts uploaded audio files at `POST /v1/asr/transcribe`, stores metadata, forwards the request to the ASR service, and returns transcript text plus timestamped segments. See [services/gateway/app/routers/asr.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/asr.py#L58).

### Turn-based voice path

The repository now contains a turn-based voice loop in which a finalized transcript is sent to an LLM route and then synthesized to audio through the TTS stack:

1. ASR final transcript is captured
2. `POST /v1/voice/turn` is called on the gateway
3. the TTS service loads the configured LLM routing settings from TTS Studio
4. the transcript is sent to a configured provider/model through an OpenAI-compatible chat completion call
5. the LLM reply is sent to TTS synthesis
6. audio output is persisted and returned for playback in the operator UI

This route is implemented in:

- [services/gateway/app/routers/voice.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/voice.py#L24)
- [services/tts/app/services/voice_turn_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/voice_turn_service.py#L13)

### TTS Studio path

The repository includes a new studio-oriented TTS surface that maintains:

- a voice registry
- route descriptors for available TTS backends
- model/provider routing settings for LLM-backed turn generation
- saved generated or imported voice assets

This logic is implemented in [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py#L74).

## 4. What Is Currently Deployed And Working

The following statements are grounded in repository code, current state docs, and runtime outputs captured in the present session.

### Verified in current code and docs

- Batch TTS works end-to-end through the unified gateway. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L15).
- Batch ASR works end-to-end through the unified gateway using `faster_whisper`. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L16).
- Sessions, metrics, and request tracing are working. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L17).
- Live ASR frontend, gateway, and internal websocket plumbing are working. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L19).
- Voxtral live lane is wired behind env-driven upstream configuration. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L20).
- OpenMOSS realtime TTS adapter path is implemented behind the `/v1/tts/stream/*` contract. See [README.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/README.md#L80) and [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L22).
- TTS Studio scaffolding, voice library, voice design preview, and route catalog are present. See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L24) and [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py#L74).
- The repo includes a working public API contract for ASR, TTS, sessions, and metrics. See [docs/api-contracts.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docs/api-contracts.md#L1).

### Verified in this session’s runtime outputs

Observed running services on the current VM during this session included:

- `aethervoice-x-frontend-1`
- `aethervoice-x-gateway-1`
- `aethervoice-x-tts-1`
- `aethervoice-x-moss-1`
- `aethervoice-x-moss-tts-1`
- `aethervoice-x-moss-voice-generator-1`
- `aethervoice-x-moss-soundeffect-1`
- `aethervoice-x-asr-1`
- `aethervoice-x-voxtral-1`
- `aethervoice-x-grafana-1`
- `aethervoice-x-prometheus-1`
- `aethervoice-x-postgres-1`
- `aethervoice-x-redis-1`
- `aethervoice-x-minio-1`

Also observed in this session:

- `aethervoice-x-moss-ttsd-1` was not running and had exited previously.
- Voxtral successfully loaded, published `/v1/realtime`, and exposed supported tasks `['generate', 'transcription', 'realtime']` in live logs.
- Gateway, ASR, TTS, and frontend all started cleanly and passed their internal health checks.
- The realtime ASR UI was restored and observed working again after rebuilding the stack.
- A turn-based `ASR -> LLM -> TTS` loop had already been exercised during this session before the grant-summary request, with transcript capture, LLM response generation, and audio playback through the operator UI.

## 5. What Is In Progress Or Partially Built

### Implemented but still experimental or not fully verified

- `voxtral_realtime`
  - implemented and running
  - current state docs describe it as materially working but still under output-shaping and normalization polish
  - see [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L91)

- `moss_realtime`
  - transport path is implemented and stable enough for continued use
  - current limitation is voice identity and conditioning strength, not basic transport
  - see [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L103)

- `moss_tts`
  - batch TTS route exists and is wired in the route catalog
  - batch reference-audio normalization was added in [services/moss/app/family.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/family.py#L139)
  - route/runtime verification and voice-quality validation remain active work items
  - current state docs still list `moss_tts` as needing production verification

- `moss_ttsd`
  - sidecar exists in compose and route catalog
  - not currently running in the observed VM state
  - current state docs explicitly say it still needs runtime verification before being treated as production-ready

- provider-backed LLM routing
  - `OpenAI`, `OpenRouter`, and `LiteLLM` provider shapes are present in TTS Studio
  - `Anthropic` is stubbed but not presented in current state docs as complete

### Scaffolds / not completed

Per the repository README adapter status:

- `qwen3_asr`: scaffold
- `sentinel`: rule-based scaffold for domain triage
- `phi_overlay`: scaffold

See [README.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/README.md#L78).

## 6. Architectural Decisions

### Self-hosted and locally controlled

The system is designed as a self-hosted stack with local infrastructure services and model-serving sidecars. It mounts model roots and Hugging Face cache paths directly into containers. The default compose profile publishes services to `127.0.0.1` rather than directly to the public internet. See [README.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/README.md#L43).

This is a local-first and operator-controlled architecture rather than a thin wrapper over third-party managed APIs.

### Stable public contracts with adapter-backed internals

The repository intentionally keeps the public browser and gateway contracts stable while allowing ASR and TTS backends to change behind adapters. This is stated directly in [README.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/README.md#L92) and is reflected in the gateway router layout and adapter design.

### Custom-built orchestration over open-source model servers

This system is not just a stock deployment of one model server. It combines:

- custom FastAPI gateway logic
- custom session and quota handling
- custom browser websocket flows
- custom OpenMOSS realtime wrapping
- custom turn-based ASR -> LLM -> TTS orchestration
- custom voice registry and route cataloging

It uses open-source components where appropriate, including:

- FastAPI
- React/Vite
- vLLM
- faster-whisper
- Redis
- PostgreSQL
- MinIO
- Prometheus
- Grafana

### GPU pinning by lane

The repo and state docs explicitly assign service lanes to specific GPUs:

- Voxtral realtime on host GPU `2`
- OpenMOSS realtime on host GPU `0`
- in-stack ASR lane on host GPU `1`
- `moss_tts` and `moss_ttsd` aligned to host GPU `0` unless re-planned
- `moss_voice_generator` treated as the shared studio/design lane on host GPU `3`

See [PROJECT_STATE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/PROJECT_STATE.md#L3).

### Sovereign / off-platform posture

Within the bounds of this repository, the stack is architected to run on owner-controlled infrastructure with self-hosted persistence and self-hosted model-serving lanes. It does contain external provider integration points for LLM routing, but the core voice infrastructure itself is implemented as local services and GPU sidecars. That is a material architectural choice for data control, deployment flexibility, and vendor independence.

## 7. Honest Gaps And Unfinished Areas

The following limitations are present in code, docs, or observed runtime state and should be described honestly.

- Realtime OpenMOSS voice identity is still the main blocker for production-quality realtime TTS voice selection.
- `moss_tts` and `moss_ttsd` are not yet fully verified as production-ready studio routes.
- `moss_ttsd` was not running in the observed VM runtime state during this session.
- Some model adapters are present only as scaffolds (`qwen3_asr`, `sentinel`, `phi_overlay`).
- The repo defaults to `AUTH_MODE=optional` for operator convenience; production-grade auth hardening is possible but is not the default local mode. See [services/worker-common/aether_common/settings.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/worker-common/aether_common/settings.py#L13).
- There is evidence of active runtime evolution and debugging in the voice stack, which means some UI truth surfaces and route-verification surfaces are still being tightened.
- The project state document explicitly describes several subsystems as stable enough to operate, but not yet final enough to freeze for full production deployment.

## 8. Concise Capability Summary

As it exists today, this repository contains a working self-hosted voice infrastructure platform with:

- browser-based live microphone transcription
- file-based transcription
- a gateway-mediated realtime ASR lane backed by Voxtral
- a gateway-mediated TTS system supporting both realtime and batch paths
- a turn-based ASR -> LLM -> TTS voice loop
- voice asset and preset management through TTS Studio
- persistent session tracking and transcript storage
- integrated monitoring and observability services

The strongest currently working areas are:

- realtime ASR
- batch ASR
- gateway/session infrastructure
- operator console workflows
- storage and observability plumbing

The most important unfinished area is:

- final voice quality and conditioning behavior for the OpenMOSS TTS family, especially realtime identity control and full runtime verification of all batch/dialogue routes

