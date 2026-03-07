
# Aether Voice Platform — Repo-Grade Engineering Spec

**Version:** v1
**Scope:** Self-hosted unified ASR + TTS platform with realtime + batch support, shared API gateway, shared UI, model adapters, session state, observability, and future multimodal overlays.

## 1. Product definition

Build a self-hosted platform with:

* **Aether Voice Gateway** — public API + auth + routing + session control
* **Aether ASR Service** — streaming and file transcription
* **Aether TTS Service** — streaming and file synthesis
* **Aether Voice Console** — frontend UI for live testing, uploads, sessions, and metrics
* **Shared infra** — Redis, Postgres, object storage, metrics, logs
* **Model adapters** — Voxtral Realtime, faster-whisper, Qwen3-ASR, Chatterbox, MOSS-TTS, optional Sentinel, optional Phi multimodal overlay

This is not “an app.” It is a **voice infrastructure substrate**.

---

# 2. Primary goals

## Functional goals

* Low-latency streaming ASR
* Batch/file ASR
* Low-latency streaming TTS
* Batch/file TTS
* Stable OpenAPI contract
* Operator UI
* Session memory and replay metadata
* Horizontal adapter model design

## Non-functional goals

* Self-hosted
* Docker-first
* Swappable model backends
* Clean telemetry
* Clear failure paths
* Stable public API regardless of model churn

---

# 3. High-level architecture

```text
clients
  ├── web ui
  ├── internal apps
  ├── sdk clients
  └── agents / tools
          |
          v
[aether-voice-gateway]
          |
   +------+------+
   |             |
   v             v
[aether-asr]  [aether-tts]
   |             |
   |             +--> chatterbox adapter
   |             +--> moss adapter
   |
   +--> voxtral adapter
   +--> faster-whisper adapter
   +--> qwen3-asr adapter
   +--> sentinel adapter (optional)
   +--> phi-mm overlay (optional)
          |
          v
   [redis] [postgres] [minio] [prometheus] [grafana]
```

---

# 4. Repository layout

```text
aether-voice/
├── README.md
├── LICENSE
├── .env.example
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
├── docs/
│   ├── architecture.md
│   ├── api-contracts.md
│   ├── deployment.md
│   ├── model-adapters.md
│   ├── telemetry.md
│   └── security.md
├── infra/
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── sites/
│   │       └── aether-voice.conf
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── provisioning/
│   ├── postgres/
│   │   └── init.sql
│   ├── redis/
│   │   └── redis.conf
│   └── minio/
│       └── policy.json
├── services/
│   ├── gateway/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── dependencies.py
│   │   │   ├── middleware/
│   │   │   │   ├── auth.py
│   │   │   │   ├── request_id.py
│   │   │   │   └── metrics.py
│   │   │   ├── routers/
│   │   │   │   ├── health.py
│   │   │   │   ├── models.py
│   │   │   │   ├── asr.py
│   │   │   │   ├── tts.py
│   │   │   │   ├── sessions.py
│   │   │   │   └── metrics.py
│   │   │   ├── schemas/
│   │   │   │   ├── common.py
│   │   │   │   ├── asr.py
│   │   │   │   ├── tts.py
│   │   │   │   └── sessions.py
│   │   │   ├── clients/
│   │   │   │   ├── asr_client.py
│   │   │   │   ├── tts_client.py
│   │   │   │   ├── redis_client.py
│   │   │   │   └── storage_client.py
│   │   │   ├── services/
│   │   │   │   ├── router_policy.py
│   │   │   │   ├── quota_service.py
│   │   │   │   └── session_service.py
│   │   │   └── utils/
│   │   │       ├── audio.py
│   │   │       └── ids.py
│   ├── asr/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── routers/
│   │   │   │   ├── health.py
│   │   │   │   ├── transcribe.py
│   │   │   │   ├── stream.py
│   │   │   │   ├── triage.py
│   │   │   │   └── analyze.py
│   │   │   ├── schemas/
│   │   │   │   ├── requests.py
│   │   │   │   ├── responses.py
│   │   │   │   └── stream_events.py
│   │   │   ├── adapters/
│   │   │   │   ├── base.py
│   │   │   │   ├── voxtral_realtime.py
│   │   │   │   ├── faster_whisper.py
│   │   │   │   ├── qwen3_asr.py
│   │   │   │   ├── sentinel.py
│   │   │   │   └── phi_overlay.py
│   │   │   ├── pipeline/
│   │   │   │   ├── audio_normalize.py
│   │   │   │   ├── chunker.py
│   │   │   │   ├── vad.py
│   │   │   │   ├── postprocess.py
│   │   │   │   └── orchestrator.py
│   │   │   ├── services/
│   │   │   │   ├── transcription_service.py
│   │   │   │   ├── streaming_service.py
│   │   │   │   ├── triage_service.py
│   │   │   │   ├── model_registry.py
│   │   │   │   └── telemetry_service.py
│   │   │   └── utils/
│   │   │       ├── audio_io.py
│   │   │       ├── time.py
│   │   │       └── lang.py
│   ├── tts/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── routers/
│   │   │   │   ├── health.py
│   │   │   │   ├── synthesize.py
│   │   │   │   └── stream.py
│   │   │   ├── schemas/
│   │   │   │   ├── requests.py
│   │   │   │   ├── responses.py
│   │   │   │   └── stream_events.py
│   │   │   ├── adapters/
│   │   │   │   ├── base.py
│   │   │   │   ├── chatterbox.py
│   │   │   │   └── moss_realtime.py
│   │   │   ├── pipeline/
│   │   │   │   ├── text_normalize.py
│   │   │   │   ├── voice_resolver.py
│   │   │   │   ├── audio_encode.py
│   │   │   │   └── orchestrator.py
│   │   │   ├── services/
│   │   │   │   ├── synthesis_service.py
│   │   │   │   ├── streaming_service.py
│   │   │   │   ├── model_registry.py
│   │   │   │   └── telemetry_service.py
│   │   │   └── utils/
│   │   │       └── text.py
│   ├── worker-common/
│   │   ├── aether_common/
│   │   │   ├── settings.py
│   │   │   ├── telemetry.py
│   │   │   ├── redis.py
│   │   │   ├── postgres.py
│   │   │   ├── storage.py
│   │   │   ├── auth.py
│   │   │   └── schemas.py
│   └── frontend/
│       ├── Dockerfile
│       ├── package.json
│       ├── vite.config.ts
│       ├── src/
│       │   ├── main.tsx
│       │   ├── App.tsx
│       │   ├── api/
│       │   │   ├── client.ts
│       │   │   ├── asr.ts
│       │   │   ├── tts.ts
│       │   │   └── sessions.ts
│       │   ├── components/
│       │   │   ├── layout/
│       │   │   ├── common/
│       │   │   ├── asr/
│       │   │   ├── tts/
│       │   │   ├── triage/
│       │   │   └── metrics/
│       │   ├── pages/
│       │   │   ├── Dashboard.tsx
│       │   │   ├── ASRLive.tsx
│       │   │   ├── ASRFile.tsx
│       │   │   ├── TTSLive.tsx
│       │   │   ├── TTSFile.tsx
│       │   │   ├── Triage.tsx
│       │   │   ├── Sessions.tsx
│       │   │   ├── Models.tsx
│       │   │   └── Metrics.tsx
│       │   ├── hooks/
│       │   │   ├── useASRStream.ts
│       │   │   ├── useTTSStream.ts
│       │   │   └── useSession.ts
│       │   ├── store/
│       │   │   └── voiceStore.ts
│       │   └── types/
│       │       └── api.ts
├── sdk/
│   ├── python/
│   └── typescript/
├── tests/
│   ├── integration/
│   ├── contract/
│   ├── load/
│   └── fixtures/
└── scripts/
    ├── dev_up.sh
    ├── dev_down.sh
    ├── seed_models.sh
    ├── smoke_test.sh
    └── benchmark_runner.py
```

---

# 5. Service responsibilities

## gateway

Public edge service.

Responsibilities:

* JWT/API-key auth
* request validation
* public REST + WebSocket endpoints
* model routing policy
* quota checks
* request ID generation
* session creation / teardown
* pass-through orchestration to ASR/TTS
* metrics emission

Does **not** load heavy models.

## asr

Dedicated inference/orchestration service for transcription.

Responsibilities:

* ingest file or audio frames
* normalize audio
* select adapter
* streaming partial transcripts
* final transcript generation
* optional triage phase
* optional multimodal overlay
* write transcripts/session artifacts

## tts

Dedicated inference/orchestration service for synthesis.

Responsibilities:

* input text normalization
* voice profile selection
* adapter invocation
* streaming or file response
* audio format normalization
* output storage

## frontend

Operator/developer console.

Responsibilities:

* live mic ASR testing
* file upload
* TTS testing
* triage pane
* session history
* metrics display
* model health/status display

---

# 6. Canonical API surface

## Health

```http
GET /v1/health
GET /v1/models
GET /v1/metrics
```

## ASR

```http
POST /v1/asr/transcribe
POST /v1/asr/stream/start
WS   /v1/asr/stream/{session_id}
POST /v1/asr/triage
POST /v1/asr/analyze
```

## TTS

```http
POST /v1/tts/synthesize
POST /v1/tts/stream/start
WS   /v1/tts/stream/{session_id}
```

## Sessions

```http
GET  /v1/sessions
GET  /v1/sessions/{session_id}
POST /v1/sessions/{session_id}/end
```

---

# 7. Request/response contracts

## POST /v1/asr/transcribe

### Request

```json
{
  "model": "auto",
  "task": "transcribe",
  "language": "auto",
  "timestamps": true,
  "diarization": false,
  "response_format": "json",
  "storage_mode": "persist",
  "metadata": {
    "source": "upload",
    "tenant_id": "tenant_123",
    "trace_id": "optional"
  }
}
```

### Response

```json
{
  "request_id": "req_123",
  "session_id": "sess_123",
  "task": "transcribe",
  "model_requested": "auto",
  "model_used": "faster_whisper",
  "language_detected": "en",
  "duration_ms": 18500,
  "text": "Hello, I need emergency service tonight.",
  "segments": [
    {
      "segment_id": "seg_1",
      "start_ms": 0,
      "end_ms": 1550,
      "text": "Hello, I need emergency service tonight.",
      "confidence": 0.93
    }
  ],
  "timings": {
    "queue_ms": 11,
    "preprocess_ms": 20,
    "inference_ms": 812,
    "postprocess_ms": 14,
    "total_ms": 857
  }
}
```

## POST /v1/asr/stream/start

### Request

```json
{
  "model": "auto",
  "language": "auto",
  "sample_rate": 16000,
  "encoding": "pcm_s16le",
  "channels": 1,
  "triage_enabled": false,
  "metadata": {
    "source": "mic",
    "tenant_id": "tenant_123"
  }
}
```

### Response

```json
{
  "session_id": "sess_live_123",
  "ws_url": "/v1/asr/stream/sess_live_123",
  "expires_in_seconds": 3600
}
```

## ASR WebSocket frame from client

```json
{
  "type": "audio_frame",
  "seq": 14,
  "timestamp_ms": 2810,
  "sample_rate": 16000,
  "encoding": "pcm_s16le",
  "channels": 1,
  "payload_b64": "..."
}
```

## ASR WebSocket partial event

```json
{
  "type": "partial_transcript",
  "session_id": "sess_live_123",
  "seq": 14,
  "stable": false,
  "text": "I need somebody",
  "start_ms": 2000,
  "end_ms": 2810
}
```

## ASR WebSocket final event

```json
{
  "type": "final_transcript",
  "session_id": "sess_live_123",
  "stable": true,
  "text": "I need somebody to come fix my breaker tonight.",
  "segments": [
    {
      "start_ms": 2000,
      "end_ms": 4380,
      "text": "I need somebody to come fix my breaker tonight."
    }
  ]
}
```

## POST /v1/asr/triage

### Request

```json
{
  "session_id": "sess_live_123",
  "input_mode": "transcript_plus_audio",
  "model": "sentinel",
  "domain": "electrical_emergency",
  "transcript": "My panel is sparking and the smell is getting worse.",
  "audio_ref": "optional://object/path.wav"
}
```

### Response

```json
{
  "request_id": "req_triage_123",
  "classification": "emergency",
  "priority": 0.98,
  "analysis": "Caller describes active electrical hazard with escalating signs of overheating.",
  "recommended_action": "Escalate to emergency after-hours dispatch immediately.",
  "requires_human_review": true
}
```

## POST /v1/tts/synthesize

### Request

```json
{
  "model": "auto",
  "voice": "default",
  "text": "A technician is being dispatched to your location now.",
  "format": "wav",
  "sample_rate": 24000,
  "stream": false,
  "style": {
    "speed": 1.0,
    "emotion": "calm",
    "speaker_hint": "support_agent"
  },
  "metadata": {
    "tenant_id": "tenant_123"
  }
}
```

### Response

```json
{
  "request_id": "req_tts_123",
  "model_used": "chatterbox",
  "audio_url": "s3://bucket/tts/req_tts_123.wav",
  "duration_ms": 2420,
  "timings": {
    "queue_ms": 4,
    "inference_ms": 291,
    "encode_ms": 19,
    "total_ms": 314
  }
}
```

## POST /v1/tts/stream/start

```json
{
  "model": "moss_realtime",
  "voice": "default",
  "sample_rate": 24000,
  "format": "pcm",
  "context_mode": "conversation"
}
```

### Response

```json
{
  "session_id": "sess_tts_123",
  "ws_url": "/v1/tts/stream/sess_tts_123"
}
```

---

# 8. Internal adapter contract

All adapters must implement the same interface.

## ASR adapter base

```python
class BaseASRAdapter(ABC):
    name: str
    supports_streaming: bool
    supports_batch: bool
    supports_timestamps: bool
    supports_language_detection: bool

    @abstractmethod
    async def transcribe_file(self, request: ASRFileRequest) -> ASRResult:
        ...

    @abstractmethod
    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        ...

    @abstractmethod
    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[ASREvent]:
        ...

    @abstractmethod
    async def end_stream(self, session_id: str) -> ASRResult:
        ...
```

## TTS adapter base

```python
class BaseTTSAdapter(ABC):
    name: str
    supports_streaming: bool
    supports_batch: bool

    @abstractmethod
    async def synthesize(self, request: TTSRequest) -> TTSResult:
        ...

    @abstractmethod
    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        ...

    @abstractmethod
    async def push_text(self, session_id: str, text: str) -> list[TTSEvent]:
        ...

    @abstractmethod
    async def end_stream(self, session_id: str) -> TTSResult:
        ...
```

---

# 9. Routing policy

## ASR route policy

```text
if task == "triage":
    base_asr = voxtral_realtime if streaming else faster_whisper
    stage2 = sentinel
elif mode == "streaming":
    prefer voxtral_realtime
    fallback qwen3_asr
elif mode == "batch":
    prefer faster_whisper
    fallback qwen3_asr
elif multilingual == true:
    prefer qwen3_asr
else:
    choose default tenant policy
```

## TTS route policy

```text
if stream == true and context_mode == "conversation":
    prefer moss_realtime
else:
    prefer chatterbox
```

## Overlay policy

```text
if multimodal_context == true:
    attach phi_overlay
```

Important: overlay models are **post-processors**, not the transcript engine.

---

# 10. Audio pipeline rules

## ASR normalization

* convert all uploaded audio to mono
* resample to 16 kHz unless adapter requires otherwise
* normalize PCM amplitude
* strip obvious container weirdness
* preserve original artifact if storage_mode = persist

## Streaming frame standard

* encoding: `pcm_s16le`
* sample rate: `16000`
* channels: `1`
* target frame size: `20ms` to `100ms`
* recommended default: `40ms`

## Batch uploads

Accepted:

* wav
* mp3
* m4a
* flac
* ogg
* webm audio

## TTS output standards

* wav for archive/download
* pcm chunks for websocket realtime
* mp3 optional for convenience download only

---

# 11. Session model

## Redis hot state

Use Redis for active stream/session state.

### Key layout

```text
voice:session:{session_id}:meta
voice:session:{session_id}:asr:partials
voice:session:{session_id}:asr:final
voice:session:{session_id}:tts:chunks
voice:session:{session_id}:events
voice:session:{session_id}:heartbeat
```

### Example meta object

```json
{
  "session_id": "sess_live_123",
  "tenant_id": "tenant_123",
  "type": "asr_stream",
  "model": "voxtral_realtime",
  "started_at": "2026-03-06T10:00:00Z",
  "status": "active",
  "triage_enabled": true
}
```

## Postgres durable schema

### tenants

```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### api_keys

```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  key_hash TEXT NOT NULL,
  label TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### voice_sessions

```sql
CREATE TABLE voice_sessions (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  session_type TEXT NOT NULL,
  model_requested TEXT,
  model_used TEXT,
  status TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
```

### voice_requests

```sql
CREATE TABLE voice_requests (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES voice_sessions(id),
  request_type TEXT NOT NULL,
  route TEXT NOT NULL,
  model_requested TEXT,
  model_used TEXT,
  status TEXT NOT NULL,
  audio_duration_ms INT,
  queue_ms INT,
  preprocess_ms INT,
  inference_ms INT,
  postprocess_ms INT,
  total_ms INT,
  fallback_used BOOLEAN NOT NULL DEFAULT FALSE,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### transcripts

```sql
CREATE TABLE transcripts (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES voice_sessions(id),
  language_detected TEXT,
  text TEXT NOT NULL,
  segments JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### triage_results

```sql
CREATE TABLE triage_results (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES voice_sessions(id),
  domain TEXT NOT NULL,
  classification TEXT NOT NULL,
  priority NUMERIC(5,4),
  analysis TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  requires_human_review BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### tts_outputs

```sql
CREATE TABLE tts_outputs (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES voice_sessions(id),
  model_used TEXT NOT NULL,
  voice TEXT,
  text_input TEXT NOT NULL,
  output_uri TEXT,
  duration_ms INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

# 12. Storage model

Use MinIO or S3-compatible object storage.

## Buckets

```text
voice-raw-audio
voice-normalized-audio
voice-transcripts
voice-tts-output
voice-debug-artifacts
```

## Object key conventions

```text
raw/{tenant_id}/{session_id}/{request_id}.wav
normalized/{tenant_id}/{session_id}/{request_id}.wav
transcripts/{tenant_id}/{session_id}/{request_id}.json
tts/{tenant_id}/{session_id}/{request_id}.wav
```

---

# 13. Frontend specification

## App sections

* Dashboard
* ASR Live
* ASR File
* TTS Live
* TTS File
* Triage
* Sessions
* Models
* Metrics

## Dashboard

* service health cards
* active sessions
* p95 latency
* failures last hour
* model availability

## ASR Live

* mic select
* connect/disconnect
* live transcript pane
* partial vs final transcript styling
* model selector
* triage toggle
* latency indicator
* copy/export transcript

## ASR File

* upload area
* timestamps toggle
* subtitle export
* model selector
* response inspector

## TTS Live

* model selector
* voice selector
* input prompt box
* stream button
* playback waveform
* chunk timing panel

## TTS File

* text area
* synthesis button
* downloadable output
* voice/style settings

## Triage

* live transcript
* urgency badge
* recommended action card
* operator note field
* escalation log

## Sessions

* list/filter/search
* session drill-down
* transcript view
* audio artifact links
* request timing breakdown

## Models

* loaded/unloaded
* health
* memory footprint
* supported features
* current route priority

## Metrics

* charts for p50/p95 latency
* error counts
* queue depth
* active websocket sessions
* fallback frequency

---

# 14. Config design

## Top-level env

```env
APP_ENV=development
LOG_LEVEL=INFO

JWT_SECRET=change_me
API_KEY_HEADER=X-API-Key

POSTGRES_URL=postgresql+psycopg://voice:voice@postgres:5432/aether_voice
REDIS_URL=redis://redis:6379/0
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=minio
S3_SECRET_KEY=miniosecret
S3_BUCKET_RAW=voice-raw-audio
S3_BUCKET_TTS=voice-tts-output

GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8080
ASR_HOST=0.0.0.0
ASR_PORT=8090
TTS_HOST=0.0.0.0
TTS_PORT=8091

DEFAULT_ASR_MODEL=voxtral_realtime
DEFAULT_BATCH_ASR_MODEL=faster_whisper
DEFAULT_TTS_MODEL=chatterbox
DEFAULT_STREAM_TTS_MODEL=moss_realtime

ENABLE_QWEN3_ASR=true
ENABLE_SENTINEL=true
ENABLE_PHI_OVERLAY=true
ENABLE_METRICS=true
ENABLE_SWAGGER=true
```

## Model-specific env

```env
VOXTRAL_MODEL_ID=mistralai/Voxtral-Mini-4B-Realtime-2602
FASTER_WHISPER_MODEL_SIZE=large-v3
QWEN3_ASR_MODEL_ID=Qwen/Qwen3-ASR-1.7B
SENTINEL_MODEL_ID=trishtan/voxtral-sentinel-4b
PHI_MM_MODEL_ID=microsoft/Phi-4-multimodal-instruct
CHATTERBOX_BASE_URL=http://chatterbox:8000
MOSS_MODEL_ID=OpenMOSS-Team/MOSS-TTS-Realtime
```

---

# 15. Docker Compose topology

## Core services

* gateway
* asr
* tts
* frontend
* redis
* postgres
* minio
* prometheus
* grafana
* nginx

## Optional external model containers

* chatterbox
* moss-worker
* qwen-worker
* sentinel-worker

## Example compose skeleton

```yaml
services:
  gateway:
    build: ./services/gateway
    env_file: .env
    ports:
      - "8080:8080"
    depends_on:
      - asr
      - tts
      - redis
      - postgres

  asr:
    build: ./services/asr
    env_file: .env
    ports:
      - "8090:8090"
    depends_on:
      - redis
      - postgres

  tts:
    build: ./services/tts
    env_file: .env
    ports:
      - "8091:8091"
    depends_on:
      - redis
      - postgres

  frontend:
    build: ./services/frontend
    env_file: .env
    ports:
      - "3000:3000"

  redis:
    image: redis:7

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: aether_voice
      POSTGRES_USER: voice
      POSTGRES_PASSWORD: voice

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"

  prometheus:
    image: prom/prometheus

  grafana:
    image: grafana/grafana
```

---

# 16. Observability spec

Every request emits:

* request_id
* session_id
* tenant_id
* route
* model_requested
* model_used
* audio_duration_ms
* queue_ms
* preprocess_ms
* inference_ms
* postprocess_ms
* total_ms
* fallback_used
* websocket_disconnect
* status
* error_code

## Structured log example

```json
{
  "request_id": "req_123",
  "session_id": "sess_123",
  "service": "asr",
  "route": "/internal/transcribe",
  "tenant_id": "tenant_123",
  "model_used": "voxtral_realtime",
  "audio_duration_ms": 8420,
  "queue_ms": 8,
  "preprocess_ms": 18,
  "inference_ms": 612,
  "postprocess_ms": 11,
  "total_ms": 649,
  "status": "ok"
}
```

## Prometheus metrics

* `voice_requests_total`
* `voice_request_errors_total`
* `voice_request_duration_ms`
* `voice_asr_stream_time_to_first_partial_ms`
* `voice_asr_stream_time_to_final_ms`
* `voice_tts_time_to_first_chunk_ms`
* `voice_active_sessions`
* `voice_model_fallback_total`
* `voice_queue_depth`

---

# 17. Security model

## Auth

* JWT bearer for users
* API keys for service-to-service or machine clients
* optional Passport IAM upstream later

## Authorization

* tenant isolation
* per-route scopes:

  * `voice:asr`
  * `voice:tts`
  * `voice:sessions:read`
  * `voice:metrics:read`
  * `voice:triage`

## Data controls

* optional no-persist mode
* configurable retention days
* delete raw audio after postprocessing if requested
* audit log for triage outputs

---

# 18. Test plan

## Unit tests

* adapter selection
* request validation
* audio normalization
* session state handling
* response schemas

## Contract tests

* OpenAPI responses
* websocket event sequence
* error response shape
* session lifecycle

## Integration tests

* upload -> transcript
* websocket live ASR
* TTS generation
* triage chain
* fallback path

## Load tests

* 50 concurrent file transcriptions
* 20 live websocket ASR sessions
* mixed ASR/TTS traffic
* memory pressure with fallback

## Smoke tests

* `/health`
* `/models`
* upload small WAV
* websocket partial transcript
* TTS sample playback URL

---

# 19. Milestone plan

## Milestone 1 — substrate

Ship:

* gateway
* asr file upload
* tts file synth
* frontend shell
* Redis/Postgres wiring
* Swagger
* faster-whisper + Chatterbox

## Milestone 2 — realtime

Ship:

* ASR websocket streaming
* Voxtral realtime adapter
* TTS websocket streaming
* session tracking
* metrics basics

## Milestone 3 — premium lanes

Ship:

* MOSS TTS adapter
* Qwen3-ASR adapter
* model routing policies
* richer frontend metrics

## Milestone 4 — moat

Ship:

* Sentinel triage
* domain triage templates
* emergency service workflows
* human review queue

## Milestone 5 — multimodal

Ship:

* Phi overlay
* audio + image workflows
* structured voice reports
* agent tool-calling support

---

# 20. Domain-specific triage templates

You were dead right about the service-business wedge.

Create domain profiles:

* `electrical_emergency`
* `hvac_after_hours`
* `plumbing_emergency`
* `locksmith_urgent`
* `restoration_dispatch`
* `security_alarm_intake`

## Example triage categories

* emergency
* urgent
* standard
* quote_request
* spam
* unclear

## Example electrical emergency triggers

* sparking
* burning smell
* panel hot
* breaker won’t reset
* partial outage with smoke
* buzzing meter base
* arcing sounds

This is where you stop being “another AI voice app” and become “after-hours revenue capture + risk triage for trades.” That prints better money.

---

# 21. What Manus and Codex should actually build first

Tell both systems:

## Round 1 deliverable

Build a working monorepo with:

* FastAPI gateway
* FastAPI ASR service
* FastAPI TTS service
* React frontend
* Redis + Postgres via Docker Compose
* OpenAPI docs
* health/models/session endpoints
* batch ASR using faster-whisper
* batch TTS using Chatterbox passthrough
* clean adapter interfaces

## Round 2 deliverable

Add:

* websocket streaming ASR
* Voxtral adapter scaffold
* websocket streaming TTS scaffold
* session persistence in Redis
* metrics endpoint
* frontend live panels

## Round 3 deliverable

Add:

* route policy engine
* MOSS adapter
* Qwen adapter
* Sentinel triage chain
* session drill-down UI

That sequencing matters. Otherwise they’ll build a shiny haunted house.

---

# 22. Copy-paste build instruction prompt for Manus/Codex

Use this as the handoff prompt:

```text
Build a production-style monorepo called `aether-voice` implementing the following architecture:

- FastAPI gateway service for public REST/WebSocket API
- FastAPI ASR service for transcription and streaming
- FastAPI TTS service for synthesis and streaming
- React + Vite frontend console
- Redis for active session state
- Postgres for durable session/request/transcript metadata
- MinIO/S3-compatible storage for audio and artifacts
- Prometheus metrics support
- Docker Compose local deployment

Requirements:
1. Use a clean adapter architecture so model backends are swappable.
2. Implement ASR adapters:
   - faster-whisper (working first)
   - voxtral realtime (scaffold if full model integration is difficult)
   - qwen3-asr (scaffold if full model integration is difficult)
   - sentinel triage as secondary stage
3. Implement TTS adapters:
   - chatterbox (working first as HTTP passthrough or direct adapter)
   - moss realtime (scaffold if full model integration is difficult)
4. Provide a stable OpenAPI contract with these routes:
   - GET /v1/health
   - GET /v1/models
   - POST /v1/asr/transcribe
   - POST /v1/asr/stream/start
   - WS /v1/asr/stream/{session_id}
   - POST /v1/asr/triage
   - POST /v1/tts/synthesize
   - POST /v1/tts/stream/start
   - WS /v1/tts/stream/{session_id}
   - GET /v1/sessions
   - GET /v1/sessions/{session_id}
   - POST /v1/sessions/{session_id}/end
5. Implement structured logging, request IDs, metrics hooks, and typed Pydantic schemas.
6. Frontend must include pages:
   - Dashboard
   - ASR Live
   - ASR File
   - TTS Live
   - TTS File
   - Triage
   - Sessions
   - Models
   - Metrics
7. Include a complete Docker Compose setup and `.env.example`.
8. Use the repo layout and data model from the provided engineering spec.
9. Prioritize working substrate over advanced polish.
10. Mark unimplemented model integrations clearly as scaffolds, not fake implementations.

Deliver:
- full file tree
- all core source files
- docker compose
- SQL init
- frontend pages
- README with startup instructions
- clear TODO markers for advanced adapters
```

