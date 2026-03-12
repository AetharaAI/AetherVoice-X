# Runtime Contracts

## Provider Contract

Normalized provider interface:
- file: `mini-agent/backend/agent/providers/base.py`
- method: `generate(system, tools, messages, max_tokens, temperature, on_stream_event)`

Current provider implementations:
- `anthropic_provider.py`
- `openai_provider.py`
- `openai_compat_provider.py`
- `failover_provider.py`

Provider selection contract:
- `AGENT_PROVIDER=openai` means direct OpenAI adapter
- `AGENT_PROVIDER=openai_compat` means OpenAI-compatible router adapter
- `AGENT_PROVIDER=anthropic` means Anthropic adapter
- fallback order is:
  - explicit `AGENT_FALLBACK_*` target first, if configured
  - then discovered LiteLLM router aliases
- fallback is only used if the primary provider errors or returns an empty payload

Direct OpenAI contract notes:
- `gpt-5.x` requests must use `max_completion_tokens`
- compat-only `extra_body` fields must not be sent to `api.openai.com`
- tool calls remain OpenAI-style Chat Completions tool calls

Temporal context contract:
- every agent run prepends a structured temporal block into the effective system prompt
- the temporal block is authoritative for:
  - current UTC time
  - current local time
  - resolved timezone
  - unix timestamp
  - session creation time
  - elapsed time since prior user turn
  - elapsed time since prior agent run
- session state persists:
  - `last_user_message_at`
  - `last_agent_run_at`
- relative terms like `today`, `latest`, `now`, `yesterday`, and `tomorrow` should be reasoned from this block, not guessed by the model

## API Contract

Primary backend routes are served from the FastAPI backend in `mini-agent/backend/`.

Important routes:
- `POST /api/chat`
- `GET /api/health`
- `GET /api/health/diagnostics`
- `GET /api/connections`
- `POST /api/connections/test`
- `POST /api/connections/save`
- `POST /api/audio/transcribe`

Chat request multimodal extensions:
- `POST /api/chat` accepts optional:
  - `audio_input`
    - `{ data, format, filename?, mime_type?, duration_ms? }`
  - `audio_url`
    - `{ url, filename?, mime_type?, duration_ms? }`
- Direct audio chat path is intended for multimodal models and must not use ASR as an intermediate stage.
- Microphone-originated direct audio turns are routed to a dedicated multimodal provider/model when configured.

## Tool Contract

Tool registry:
- `mini-agent/backend/agent/tools/registry.py`

Dispatch model:
- tools are registered centrally
- execution is normalized through one dispatch layer
- long-running project work uses session workspaces under `workspaces/<session_id>/`

## Memory Contract

The harness is designed to use:
- Redis
- MongoDB
- Qdrant
- Postgres

MongoDB contract:
- DB name stays fixed at `aether_memory`
- namespace separation is document/key scoped, not database scoped
- bootstrap file: `mongo-mem/aether-init.js`
- `episodes` inserts must include at least:
  - `agent_id`
  - `session_id`
  - `summary`
  - `embedding`
  - `created_at`

Namespace behavior:
- Redis keys are namespaced
- Mongo documents include `namespace`
- Postgres may use schema-level separation
- Qdrant collection policy is independent of Mongo DB naming

## Direct Audio Routing Contract

Dedicated multimodal audio provider selection:
- `DIRECT_AUDIO_PROVIDER`
- `DIRECT_AUDIO_BASE_URL`
- `DIRECT_AUDIO_API_KEY`
- `DIRECT_AUDIO_MODEL`

Phi-4 convenience aliases:
- `PHI_4_INSTRUCT_MODEL_BASE_URL`
- `PHI_4_INSTRUCT_API_KEY`
- `PHI_4_INSTRUCT_MODEL_NAME`

Selection behavior:
- if a chat turn includes `audio_input` or `audio_url`, the runner prefers the dedicated multimodal audio provider
- if no dedicated multimodal provider is configured, the run fails fast with a clear configuration error
- text-only turns continue to use the normal provider/fallback chain

Persistence behavior:
- raw base64 audio and direct data URLs are not persisted into long-term memory
- only audio metadata placeholders are stored in session history and memory backends
