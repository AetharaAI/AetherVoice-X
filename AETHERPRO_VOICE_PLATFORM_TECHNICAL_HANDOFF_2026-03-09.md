# AetherPro Voice Platform Technical Handoff

Date: 2026-03-09

Scope: this document is a handoff-grade technical and architectural brief for the current Aether Voice Platform repo. It is intended to bring a fresh Codex pass up to speed quickly without forcing it to rediscover the platform shape, runtime truth, or current OpenMOSS direction.

Important truth boundary:
- This brief reflects the current local working tree, not just older committed markdown.
- Some older docs in this repo still describe an earlier state where only `moss_realtime` and `chatterbox` were runtime-backed.
- The codebase has moved beyond that in the current local state.

## 1. Executive summary

This repo is the unified voice infrastructure stack for AetherPro. It is not just a model playground. It is the integration surface for:
- unified ASR and TTS operator pages
- a future public `studio.aetherpro.us` Voice Studio
- backend route orchestration for speech models
- runtime truth, session tracking, metrics, artifacts, and playback
- eventual `ASR -> LLM -> TTS` voice-agent roundtrip flows

Current high-level reality:
- Batch ASR works.
- Live ASR works and is already operator-usable.
- Batch TTS works.
- OpenMOSS realtime TTS works end to end enough to start, stream, finalize, play, and download a correct final WAV.
- The main remaining OpenMOSS realtime problem is live chunk quality/behavior, not the final artifact path.
- An additive `TTS Studio` control plane now exists and is the correct home for broader OpenMOSS workflows.

## 2. Infrastructure and domain map

Canonical source: [AETHERPRO_INFRA_TOPOLOGY.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/AETHERPRO_INFRA_TOPOLOGY.md)

Primary domain surfaces:
- `asr.aetherpro.us`: ASR service and unified console entry
- `tts.aetherpro.us`: Chatterbox TTS service
- `operations.aetherpro.us`: AetherOps
- `api.aetherpro.tech`: multimodal inference gateway
- `triad.aetherpro.tech`: memory and database plane

Relevant node map:
- `L40S-180`: primary large-model inference node
- `L40S-90`: secondary multimodal/vision/agent-support inference node
- `L4-360`: speech/services node
  - GPU0: current OpenMOSS family work
  - GPU2: ASR lane
  - GPU3: Chatterbox lane
- `C3-32`: gateway/control-plane/VoiceOps/studio surface
- `R3-64`: data spine

Operational implication:
- This repo should be understood as the speech/voice substrate inside a wider AetherPro control plane, not as an isolated app.

## 3. Canonical model layout

Canonical OpenMOSS root:
- `/mnt/aetherpro/models/audio/OpenMOSS-Team`

Expected model folders:
- `MOSS-TTS-Realtime`
- `MOSS-TTS`
- `MOSS-TTSD-v1.0`
- `MOSS-VoiceGenerator`
- `MOSS-SoundEffect`
- `MOSS-Audio-Tokenizer`

Container mount convention:
- host root: `/mnt/aetherpro/models`
- container root: `/models`

The repo now explicitly treats `/mnt/aetherpro/models/audio/OpenMOSS-Team` as canonical truth and resolves container-visible equivalents for health/readiness checks.

## 4. Compose/runtime architecture

Canonical stack file: [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml)

Core services:
- `gateway`: public API layer and websocket routing
- `asr`: batch/live ASR service
- `tts`: TTS orchestration service
- `frontend`: operator console / studio UI
- `redis`, `postgres`, `minio`, `prometheus`, `grafana`

Model sidecars currently defined:
- `voxtral`
- `moss` for realtime OpenMOSS
- `moss-tts`
- `moss-ttsd`
- `moss-voice-generator`
- `moss-soundeffect`

Compose profile mapping:
- `voxtral`
- `moss`
- `moss-tts`
- `moss-ttsd`
- `moss-voicegen`
- `moss-sfx`

Meaning:
- The repo is no longer only a realtime MOSS pilot.
- The compose layer already has additive room for the wider OpenMOSS family.

## 5. Service responsibilities

### Gateway

Relevant files:
- [services/gateway/app/routers/tts.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/tts.py)
- [services/gateway/app/routers/studio.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/studio.py)

Responsibilities:
- public `/api/v1/*` contract
- TTS websocket contract
- studio backend proxying
- request routing to internal ASR/TTS services

### TTS service

Relevant files:
- [services/tts/app/main.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/main.py)
- [services/tts/app/services/model_registry.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/model_registry.py)
- [services/tts/app/services/synthesis_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/synthesis_service.py)
- [services/tts/app/services/streaming_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/streaming_service.py)
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)

Responsibilities:
- registry of available TTS adapters
- batch synthesis orchestration
- streaming TTS session lifecycle
- runtime truth reporting
- studio voice registry
- provider-backed LLM routing config storage and model discovery

### OpenMOSS realtime sidecar

Relevant file:
- [services/moss/app/main.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/main.py)

Responsibilities:
- load `MOSS-TTS-Realtime`
- start/push/complete/end stream lifecycle
- emit live audio chunk events
- finalize full WAV artifact on stream close

### OpenMOSS family sidecar

Relevant file:
- [services/moss/app/family.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/family.py)

Responsibilities:
- generic batch-mode HTTP runtime for:
  - `tts`
  - `ttsd`
  - `voice_generator`
  - `soundeffect`
- returns audio bytes and runtime artifacts through `/v1/synthesize`

## 6. Current runtime truth by model family

This section is the most important handoff correction because older markdown in the repo is stale.

### Actually runtime-backed in current local code

- `chatterbox`
- `moss_realtime`
- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

Clarification:
- These are runtime-backed in code and compose.
- Readiness in the UI still depends on live sidecar health and weights being present.
- A route can be wired in code but still not be healthy on a given VM if its sidecar is not started.

### Current adapter registry

Relevant file:
- [services/tts/app/services/model_registry.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/model_registry.py)

Registered adapters:
- `chatterbox`
- `moss_realtime`
- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

### Current alias normalization

Relevant file:
- [services/worker-common/aether_common/model_aliases.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/worker-common/aether_common/model_aliases.py)

The MOSS family names are normalized in current local code, not just `moss_realtime`.

### Truthful runtime categories

Stable enough:
- `faster_whisper`
- `chatterbox`
- live ASR lane with Voxtral upstream when configured

Working but still experimental:
- `moss_realtime`

Wired but still product-incomplete:
- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

Reason they are still product-incomplete:
- runtime wiring exists
- studio truth/readiness exists
- but broader UX, voice-conditioning semantics, and workflow hardening still need completion

## 7. TTS Live architecture

Relevant frontend:
- [services/frontend/src/pages/TTSLive.tsx](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/pages/TTSLive.tsx)
- [services/frontend/src/hooks/useTTSStream.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/hooks/useTTSStream.ts)

Relevant backend:
- [services/tts/app/services/streaming_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/streaming_service.py)
- [services/tts/app/adapters/moss_realtime.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/adapters/moss_realtime.py)
- [services/moss/app/main.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/main.py)

Contract summary:
1. Frontend starts stream via gateway.
2. Gateway -> TTS -> OpenMOSS realtime sidecar.
3. Browser opens returned websocket contract.
4. Frontend sends plain spoken text.
5. Structured controls stay in metadata, not spoken text.
6. Live chunk events can arrive during generation.
7. Final WAV is assembled at stream close.

Important product truth:
- Only the spoken body is sent as the utterance.
- Tone/cadence/style/session profile are console-side state.
- The UI now separates:
  - selected voice asset
  - requested preset
  - actual runtime conditioning source
  - fallback/default voice path

Known live-path issue:
- Final WAV can be clean and correct while live chunk playback still sounds wrong or unstable.
- That strongly suggests the remaining problem is in live chunk path framing/decoder behavior, not the final artifact path.

## 8. TTS Studio architecture

Relevant frontend:
- [services/frontend/src/pages/TTSStudio.tsx](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/pages/TTSStudio.tsx)

Relevant backend:
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)

Studio tabs:
- Voice Library
- Voice Clone
- Voice Design
- Batch Narration
- Dialogue Studio
- LLM Routing
- Advanced

Purpose:
- additive OpenMOSS control surface
- does not replace TTS Live
- holds reusable voice assets, route catalog, batch/dialogue workflows, and future LLM routing

Current route selection intent:
- Batch Narration should prefer `moss_tts` when healthy
- Dialogue Studio should prefer `moss_ttsd` when healthy
- Voice Design should prefer `moss_voice_generator`
- `chatterbox` remains safe fallback

## 9. Voice registry and seed library

Relevant backend:
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)

Seed payload:
- `voice-studio/23-seed-voices-shapes.json`

Registry characteristics:
- file-backed under local storage root
- supports preset/imported/generated/cloned/fallback voice records
- uploaded reference assets are reusable
- seed voices auto-load when the seed file exists

Important operator truth:
- Seed/example voices should appear automatically in the library.
- Users do not need to manually recreate them in the UI if the seed file is present.

Current limitation:
- Voice registry truth and realtime conditioning truth are not the same thing.
- A selected voice can exist as a registry asset without materially changing realtime inference yet.

## 10. OpenMOSS realtime conditioning truth

Relevant logic:
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)

Current truthful behavior:
- `moss_realtime` can preserve session truth for voice selection.
- It can log requested voice, selected asset, and current conditioning source.
- But realtime inference still tends to use the current default/global conditioning path unless per-session conditioning binding is active.

This is why the UI was changed to stop lying.

Do not assume:
- “selected voice in UI” means “realtime timbre materially changed”

Do assume:
- current UI now attempts to tell the truth about whether conditioning is active or registry-only

## 11. Provider-backed LLM routing

Relevant backend:
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)

Providers scaffolded now:
- `OpenAI`
- `OpenRouter`
- `LiteLLM`
- `Anthropic` stub

Important implementation details:
- model dropdowns are fetched live from provider `/models`
- auth stays backend-held via envs
- LiteLLM/internal endpoints can use internal base URLs and auth headers

This is groundwork for:
- `ASR -> LLM -> TTS` roundtrip voice agents
- selecting provider/model policy from the studio instead of hardcoding inference routes

## 12. Current OpenMOSS-specific findings

From verified repo behavior and notes:
- `moss_realtime` can produce correct final WAV output
- second turn is materially faster than cold first turn
- model appears to benefit from warm context / steady session reuse
- final artifact quality is currently better than live chunk playback quality
- earlier alignment failures were partly caused by prepending pseudo-tags into spoken text

Current best read:
- cold start and session warmup matter
- realtime chunk behavior still needs tuning against official OpenMOSS realtime expectations
- finalization path should remain untouched while live chunk path is being debugged

## 13. What is on disk vs what is actually connected

Connected in runtime code:
- Realtime
- TTS
- TTSD
- VoiceGenerator
- SoundEffect
- tokenizer

On disk and expected in canonical root:
- same as above

Still needs proof on a given VM:
- each sidecar is healthy
- each model route is actually invoked successfully from the studio
- VoiceGenerator-driven created assets flow cleanly into later batch/realtime use
- TTSD dialogue behavior is satisfactory

## 14. Current known gaps

1. Live chunk audio path for `moss_realtime` still needs deeper verification.
2. Realtime voice conditioning is not yet fully trustworthy as per-session voice control.
3. `moss_tts`, `moss_ttsd`, `moss_voice_generator`, and `moss_soundeffect` are wired, but product workflows still need full runtime validation on the target VM.
4. Older project markdown under-describes the current local code state.
5. The repo has local uncommitted work in the current working tree, so another Codex pass should not assume `main` fully matches this brief.

## 15. Recommended next-pass priorities

1. Keep the final WAV path for `moss_realtime` unchanged.
2. Verify OpenMOSS realtime live chunk handling against official serving expectations:
   - prompt audio / prompt_wav handling
   - streaming text delta flow
   - per-session context behavior
   - KV cache reuse
   - tokenizer/codec decode path
   - chunk framing, sample rate, PCM/container format, browser playback compatibility
3. Make per-session logs explicit for:
   - selected `voice_id`
   - requested preset
   - resolved conditioning asset
   - actual runtime conditioning source
   - live chunk source route
   - final artifact source route
   - fallback route if used
4. Validate each family sidecar from the studio UI once healthy:
   - `moss_tts`
   - `moss_ttsd`
   - `moss_voice_generator`
   - `moss_soundeffect`
5. Promote `moss_voice_generator` as the default safe path for voice-creation testing.
6. Treat `TTS Live` as the narrow realtime operator lane and keep broader voice workflows in `TTS Studio`.
7. Fold this repo’s truth into the operator/founder dossier repo as the canonical voice-platform subsystem brief.

## 16. Files a fresh Codex should read first

Highest-signal docs:
- [AETHERPRO_INFRA_TOPOLOGY.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/AETHERPRO_INFRA_TOPOLOGY.md)
- [AETHERPRO_VOICE_PLATFORM_TECHNICAL_HANDOFF_2026-03-09.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/AETHERPRO_VOICE_PLATFORM_TECHNICAL_HANDOFF_2026-03-09.md)
- [OpenMOSS-Realtime-State-Snapshot-2026-03-08.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/OpenMOSS-Realtime-State-Snapshot-2026-03-08.md)

Highest-signal code:
- [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml)
- [services/tts/app/services/model_registry.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/model_registry.py)
- [services/tts/app/services/studio_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/studio_service.py)
- [services/tts/app/services/streaming_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/streaming_service.py)
- [services/tts/app/services/synthesis_service.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/tts/app/services/synthesis_service.py)
- [services/moss/app/main.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/main.py)
- [services/moss/app/family.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/moss/app/family.py)
- [services/frontend/src/pages/TTSLive.tsx](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/pages/TTSLive.tsx)
- [services/frontend/src/pages/TTSStudio.tsx](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/pages/TTSStudio.tsx)

## 17. Bottom line

This repo has crossed from “single realtime pilot” into “real voice platform control surface,” but one part of the system still needs discipline:
- the final artifact path is stronger than the live path
- the voice registry is ahead of realtime conditioning
- the studio shell is ahead of full product hardening

That is not a failure. It just means the next pass should focus on truth, runtime validation, and OpenMOSS live-path correctness instead of inventing new surfaces.
