# OpenMOSS Family Wiring State - 2026-03-09

## Purpose

This snapshot records the actual repo state at the moment implementation was paused so the next pass can continue from verified context instead of stale assumptions.

## Current Repo Truth

### Runtime-backed today

- `moss_realtime`
- `chatterbox`

### Not yet runtime-backed today

- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

These are currently either visible in studio metadata or represented in the voice registry, but they are not connected to real batch/runtime adapters yet.

## What Was Verified

### TTS service registry

`services/tts/app/services/model_registry.py`

Only these adapters are actually registered:

- `ChatterboxAdapter`
- `MossRealtimeAdapter`

No adapters exist yet for:

- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

### Model alias normalization

`services/worker-common/aether_common/model_aliases.py`

TTS aliases currently normalize only:

- `chatterbox`
- `moss_realtime`

The remaining MOSS family names are not yet normalized.

### TTS batch path

`services/tts/app/services/synthesis_service.py`

Batch synthesis currently:

- uses the registered adapter directly
- falls back to `chatterbox` on non-chatterbox failure
- does not yet resolve a studio voice record into a real runtime conditioning asset before synthesis

### Current studio route catalog

`services/tts/app/services/studio_service.py`

Current route state in code:

- `moss_realtime`: runtime-wired and ready when endpoint/path exist
- `moss_tts`: force-disabled in code
- `moss_ttsd`: staged only
- `moss_voice_generator`: staged only
- `chatterbox`: ready

This is stale relative to the VM state, where the user reports the remaining MOSS family weights are now fully or nearly fully downloaded.

### Voice seed loading

`services/tts/app/services/studio_service.py`
`voice-studio/23-seed-voices-shapes.json`

Seed voices do auto-load into the studio registry.

The user does not need to recreate those seed records manually if the seed file is present.

### Studio UI truth

`services/frontend/src/pages/TTSStudio.tsx`

Current UI behavior:

- `Voice Library` shows seed and fallback voices
- `Voice Clone` imports reusable reference assets into the registry
- `Voice Design` currently saves a registry preset only
- `Batch Narration` only invokes currently invokable batch routes
- `Dialogue Studio` only invokes currently invokable dialogue routes
- output panel is shared and functional

Important limitation:

`Voice Design` does not yet call a real `moss_voice_generator` runtime.

### TTS Live truth

`services/frontend/src/pages/TTSLive.tsx`
`services/frontend/src/hooks/useTTSStream.ts`

Current live lane improvements already present:

- plain spoken body is sent, not prepended XML in the utterance
- runtime truth is surfaced
- selected voice asset, requested preset, runtime conditioning, fallback voice path, and runtime path used are all shown separately

Important limitation:

Realtime voice selection is still mostly registry truth, not guaranteed per-session conditioning truth. The sidecar still needs proper voice asset resolution and conditioning binding before the UI can claim realtime voice shaping is materially active.

## Current MOSS Sidecar Reality

### Existing sidecar

`services/moss/app/main.py`

This is still a dedicated realtime sidecar only.

It currently exposes:

- `GET /health`
- `POST /v1/stream/start`
- `POST /v1/stream/{session_id}/text`
- `POST /v1/stream/{session_id}/complete`
- `POST /v1/stream/{session_id}/end`

It logs runtime truth for:

- live chunk source route
- final artifact source route
- conditioning source used
- fallback route used

### Existing Docker image

`services/moss/Dockerfile`

This image is already a good reusable base for the wider MOSS family because it:

- installs CUDA runtime dependencies
- creates a venv
- installs the upstream `MOSS-TTS` repo with torch runtime

It is the right place to reuse for:

- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- possibly `moss_soundeffect`

## Compose Reality

`docker-compose.yml`

Current services:

- `moss` sidecar for realtime
- no sidecars yet for batch/dialogue/voice-generator/soundeffect

This means the studio cannot truthfully invoke the full MOSS family yet even if the model folders exist on disk.

## Settings Reality

`services/worker-common/aether_common/settings.py`
`.env.example`

Current env/settings already include some model identifiers:

- `MOSS_MODEL_ID`
- `MOSS_TTS_MODEL_ID`
- `MOSS_TTSD_MODEL_ID`
- `MOSS_VOICE_GENERATOR_MODEL_ID`

Missing today:

- dedicated base URLs for family sidecars
- dedicated timeouts
- dedicated model paths
- any sound effect model envs

## Upstream OpenMOSS Usage Pattern Verified

Reference repo inspected locally:

- `/tmp/MOSS-TTS-ref-2`

### Confirmed patterns

- `MOSS-TTS` uses `AutoProcessor` + `AutoModel` + `processor.build_user_message(...)`
- `MOSS-TTS` supports direct text generation and reference-audio-assisted generation
- `MOSS-TTSD` expects dialogue text and supports continuation / reference audio patterns
- `MOSS-VoiceGenerator` produces audio from a text description + instruction
- `MOSS-SoundEffect` is a separate text-to-sound path and should not be silently mixed into narration/dialogue

This means the repo should not fake these modes behind a single adapter. They need real sidecars or a real runtime switch.

## Recommended Next Implementation Path

### 1. Add real MOSS family sidecars

Preferred additive shape:

- reuse `services/moss/Dockerfile`
- add a generic batch family app under `services/moss/app/`
- run separate compose services for:
  - `moss_tts`
  - `moss_ttsd`
  - `moss_voice_generator`
  - optionally `moss_soundeffect`

### 2. Add real TTS adapters

Add adapters under `services/tts/app/adapters/`:

- `moss_tts.py`
- `moss_ttsd.py`
- `moss_voice_generator.py`
- optionally `moss_soundeffect.py`

### 3. Expand settings/envs

Add explicit settings for:

- base URLs
- model IDs
- model paths
- timeouts
- GPU routing / ports if needed

### 4. Update alias normalization

Expand `TTS_MODEL_ALIASES` to include:

- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`

### 5. Make studio voice records materially affect runtime

Current missing step:

- resolve `voice_id` into real conditioning/reference assets before runtime invocation

Needed for:

- truthful studio narration
- truthful dialogue preview
- truthful realtime conditioning claims

### 6. Keep realtime final artifact path untouched

The working final WAV path for `moss_realtime` should not be changed while wiring the wider MOSS family.

## Important User-Reported Runtime Context

The user reported:

- all MOSS family models are now downloaded or completing
- `voice-studio/` contains seed voice design material
- realtime still has conditioning/path truth concerns
- final WAV path is more important to preserve than experimental live-chunk tweaks

That means the next pass should prioritize:

1. additive batch/dialogue/voice-generator runtime wiring
2. truthful UI/readiness
3. no regression to the existing working final realtime artifact path

## Current Working Tree State

At the time of this snapshot:

- no runtime code changes were applied in this pass
- one unrelated untracked file was visible:
  - `audio-tts/Me-Sells-Script-0.1-weak-testing realtime.wav`

## Bottom Line

The repo already has a good studio shell, a good registry shell, and a working realtime sidecar.

What it does not yet have is the actual runtime wiring for the rest of the MOSS family.

The next pass should be implementation, not more UI theater:

- real sidecars
- real adapters
- real readiness
- real voice resolution
- no breaking changes to the working live/final realtime path
