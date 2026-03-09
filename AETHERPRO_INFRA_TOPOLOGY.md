> Public-safe topology summary. Sanitized for collaboration, repo visibility, and external planning. No secrets, credentials, private IPs, or raw internal connection strings are included here.

# AetherPro Technologies Infrastructure Topology

## Domain footprint

### `aetherpro.us`
- Main corporate landing page
- `operations.aetherpro.us` - AetherOps
- `tts.aetherpro.us` - Chatterbox TTS service
- `embed.aetherpro.us` - embedding and reranker endpoints
- `asr.aetherpro.us` - Aether ASR service
- `perception.aetherpro.us` - perception and inference endpoints
- `audio.aetherpro.us` - acoustic perception engine

### `aetherpro.tech`
- `api.aetherpro.tech` - multimodal inference gateway
- `triad.aetherpro.tech` - Triad Intelligence memory and database plane

### Additional active domains
- `syndicateai.co` - agent and labor marketplace platform
- `redwatch.us` - autonomous security and compliance platform
- `blackboxaudio.tech` - audio inference and tooling platform
- `perceptor.us` - OCR and vision perception platform
- `passportalliance.org` - Passport Alliance federation and APIS identity work
- `passportalliance.us` - redirect domain
- `mcpfabric.space` - MCP tool server and A2A communication surface
- `aetheragentforge.org` - agent marketplace frontend

## Canonical node and workload map

### `L40S-180` - dual-GPU primary inference node
- Role: core large-model inference
- GPUs: `2x L40S`
- Primary workload: `Qwen3.5-122B-AWQ-4Bit`
- Additional resident or staged models include larger reasoning and coding lanes for future evaluation
- Operated behind an OpenAI-compatible inference gateway
- Treated as a high-value core intelligence node

### `L40S-90` - vision and multimodal node
- Role: multimodal and vision inference
- GPUs: `1x L40S`
- Hosts smaller multimodal, vision, and agent-support models
- Operated behind an OpenAI-compatible inference gateway
- Used as the secondary high-value intelligence node

### `L4-360` - multi-GPU services node
- Role: embeddings, TTS, ASR, and service-side experimentation
- GPUs: `4x NVIDIA L4`

#### GPU allocation
- `GPU0` - current OpenMOSS realtime pilot lane during Voice Studio integration work
- `GPU1` - security and experimental model lanes
- `GPU2` - ASR service lane and related speech models
- `GPU3` - Chatterbox TTS service lane

#### Service responsibilities
- Aether ASR server with standalone UI and API surface
- Chatterbox TTS server with standalone UI and API surface
- OpenMOSS realtime sidecar under active integration for the unified Voice Studio
- Unified Aether Voice Studio surface with additive `TTS Studio` control plane now scaffolded in the repo
- Audio infrastructure and routing experiments
- GPU-aware service multiplexing and deployment control

#### Current Voice Studio integration note
- As of March 8, 2026:
  - Voxtral realtime ASR is functioning in the unified console
  - OpenMOSS realtime TTS is emitting chunk audio and finalized WAV artifacts through the unified console
  - OpenMOSS realtime remains experimental due to prompt-shaping, voice-catalog, and latency-readiness concerns
  - a new additive `TTS Studio` surface is now wired for voice registry, clone/design workflows, and provider-backed LLM routing configuration

#### Canonical OpenMOSS model root
- Voice Studio work now treats `/mnt/aetherpro/models/audio/OpenMOSS-Team` as the canonical OpenMOSS model root
- Canonical subpaths expected by the current studio build include:
  - `MOSS-TTS-Realtime`
  - `MOSS-TTS`
  - `MOSS-TTSD-v1.0`
  - `MOSS-VoiceGenerator`
  - `MOSS-Audio-Tokenizer`

### `C3-32` - Aether gateway and platform node
- Role: gateway, control plane, VoiceOps, and voice agent product surfaces
- Hosts the primary platform and orchestration tier
- Intended to carry the unified `studio.aetherpro.us` experience

### `B3-16` - application backend node
- Role: SaaS backends and business APIs
- Hosts marketplace and operations backend workloads

### `B3-32 Flex` - identity and MCP node
- Role: identity, auth, protocol services
- Hosts Passport and MCP Fabric services

### `R3-64` - Triad node
- Role: data spine and intelligence backbone
- Datastores:
  - PostgreSQL clusters
  - Redis clusters
  - MongoDB clusters
  - Qdrant
  - Weaviate
- Purpose:
  - memory
  - state
  - vector search
  - coordination

### User devices
- Developer laptops act as the human control plane
- Used for orchestration, debugging, and manual intervention

## Shared service categories

### Vector and retrieval layer
- Qdrant for vector storage
- embedding endpoints for semantic search
- reranker endpoints for retrieval quality

### Persistence layer
- PostgreSQL for transactional state
- Redis for cache, queues, and session coordination
- MongoDB for memory and agent-oriented document storage

### Product surfaces
- Voice infrastructure and VoiceOps platform
- agent marketplace and labor marketplace work
- identity and agent passport services
- security and compliance systems
- multimodal perception and audio tooling

## Operational notes
- The public version intentionally omits:
  - API keys
  - passwords
  - database usernames
  - raw connection strings
  - private network addresses
  - code snippets with embedded credentials
- The internal working copy is [AETHERPRO_INFRA_TOPOLOGY_SENSITIVE.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/AETHERPRO_INFRA_TOPOLOGY_SENSITIVE.md)
