# Context Handoff - March 11, 2026

## What This Repo Is

`Aether Voice X` is the user's sovereign voice stack. The product direction is explicit:

- self-hosted
- modular
- deployable on practical GPU hardware
- capable of private, air-gapped, and eventually government-facing deployments
- not dependent on third-party hosted voice APIs for the core product

The user is building toward a full conversational system, not isolated demos.

## Strategic Execution Lanes

### 1. Realtime Agent Mode

- Pipeline: `ASR -> LLM -> realtime TTS`
- Purpose: telephony, live interruption, low-latency agent turns
- Current status: partially working and good enough to freeze
- Main remaining blocker: realtime voice identity / conditioning strength

### 2. Turn-Based Voice Mode

- Pipeline: `ASR -> LLM -> batch / turn-based TTS`
- This is the next implementation target
- Purpose: get a known-good conversational baseline with stronger voice fidelity and easier debugging
- This lane should be completed before deeper realtime iteration resumes

### 3. Assisted / Staged Streaming Mode

- Pipeline: `ASR -> LLM -> staged/chunked playback`
- Future lane
- Purpose: perceived realtime without depending on strict realtime synthesis behavior

## Realtime Lane Freeze State

### What is working

- `moss_realtime` boots cleanly and serves on `:8021`
- `moss-voice-generator` boots cleanly and serves on `:8024`
- resident stack is stable enough for active testing
- selected voice registry assets now reach realtime conditioning
- longer prompt WAVs materially improve speaker identity versus very short clips
- current decode baseline is stable

### Known-good realtime defaults

- `prefill_text_len=24`
- `decode_chunk_frames=6`
- `decode_overlap_frames=0`
- `temperature=0.45`
- `top_p=0.65`
- `top_k=30`
- `repetition_penalty=1.1`
- `repetition_window=50`

### Important realtime truths

- preset switching plumbing is now working
- the UI now shows selected preset, selected voice asset, and realtime conditioning path truthfully
- selected voice assets can appear in `Runtime conditioning`
- however, `MOSS-TTS-Realtime` still does not strongly honor speaker identity across presets
- audible voice often collapses toward a house voice / model prior
- synthetic preview WAVs are weak conditioning sources compared with real human reference audio
- a clean real human reference WAV is the next decisive realtime identity test

### Lifecycle truth

- realtime stream is effectively one utterance per stream
- after `/complete`, another `/text` on the same stream returns `409 Conflict`
- this is expected with current backend behavior
- operator must start a new stream for another utterance

### Do not reopen

- nginx `/api/v1` routing was not the root issue
- preset selection wiring is no longer the main issue
- current realtime problem is not “UI cannot select the voice”
- current realtime problem is model behavior and conditioning strength

## Current GPU Contract

- GPU `0`: realtime `moss`
- GPU `1`: already partly occupied by non-stack embedding workloads
- GPU `2`: `voxtral`
- GPU `3`: `moss-voice-generator`

Do not assume all four GPUs are empty.

## Resident Stack

Keep these up for the main operator flow:

- `frontend`
- `gateway`
- `tts`
- `asr`
- `redis`
- `postgres`
- `minio`
- `prometheus`
- `grafana`
- `voxtral`
- `moss`
- `moss-voice-generator`

Keep these on-demand only:

- `moss-tts`
- `moss-ttsd`
- `moss-soundeffect`

## Operator Scripts Already Added

- `scripts/stack_resident_up.sh`
- `scripts/stack_resident_rebuild.sh`
- `scripts/stack_optional_off.sh`
- `scripts/stack_batch_tts_on.sh`
- `scripts/stack_dialogue_on.sh`
- `scripts/stack_sfx_on.sh`
- `scripts/stack_status.sh`
- `scripts/stack_logs_resident.sh`

`stack_status.sh` was fixed to use host-side health checks instead of `docker compose exec ... curl`.

## Code Changes Already Landed

1. Realtime tuning controls in `TTS Live` are wired to the MOSS sidecar.
2. Selected voice `reference_audio_path` overrides the global fallback prompt for realtime sessions.
3. Voice Design save path now preserves rendered preview WAVs as reusable conditioning assets.
4. Studio save/import path now preserves seed `voice_id` and upserts correctly.
5. Realtime default tuning values were updated in frontend, MOSS runtime defaults, and `.env.example`.
6. Resident stack scripts were added for deterministic startup and teardown.

## Most Relevant Files For Next Work

- `PROJECT_STATE.md`
- `.env.example`
- `services/frontend/src/pages/TTSLive.tsx`
- `services/frontend/src/pages/TTSStudio.tsx`
- `services/moss/app/main.py`
- `services/tts/app/services/streaming_service.py`
- `services/tts/app/services/studio_service.py`
- `services/tts/app/routers/studio.py`
- `services/tts/app/schemas/studio.py`

## Tests Already Passed

- `tests/unit/test_studio_service.py`
- `tests/unit/test_tts_streaming_service.py`
- frontend build passed
- Python compile checks passed

## The Next Task

Move to Turn-Based Voice Mode.

### Goal

- use realtime ASR as the input source
- send finalized utterance to the LLM
- generate a full response
- synthesize that response with non-realtime TTS
- return/play a clean spoken reply

### Why this is next

- it establishes a trustworthy baseline
- it avoids burning more time on the hardest part of the stack before the easier conversational loop is locked in
- it keeps realtime work preserved without pretending it is already final

## Read These First In The Next Session

1. `PROJECT_STATE.md`
2. `CONTEXT_HANDOFF-03-11-2026.md`
3. `project-state-note-03-11-2026.md`
4. `OpenMOSS-Realtime-State-Snapshot-2026-03-08.md`

## One-Line Instruction To The Next Codex

Do not reopen the old routing and transport rabbit holes; freeze realtime where it is and move directly to building Turn-Based Voice Mode.
