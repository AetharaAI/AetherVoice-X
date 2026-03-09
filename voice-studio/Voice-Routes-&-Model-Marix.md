# Aether Voice Studio — Voice Routes and Model Matrix

## Purpose

This document defines the canonical routing model for Aether Voice Studio.

It answers:
- which route should be used for which task
- which model family powers that route
- what the input/output expectations are
- what UI surface should expose that capability
- which fallback paths are allowed

This file is intended for:
- humans reading system behavior
- agents selecting the correct route automatically
- backend routing logic
- docs generation
- test planning

---

## Canonical Route Targets

### `moss_realtime`
Primary use:
- low-latency live TTS
- session-based turn-taking
- voice agent reply playback
- telephony / live assistant response lane

Best for:
- TTS Live
- future full roundtrip `ASR -> LLM -> TTS`
- low-latency browser playback
- session-bound voice behavior

Input shape:
- `session_id`
- `voice_id`
- `text`
- optional structured style/profile metadata

Output shape:
- streamed audio chunks
- finalized audio artifact after end/flush

Notes:
- do not prepend XML/structured tags into spoken text
- voice/style controls must be translated server-side
- keep this route narrow and operational

UI surfaces:
- `TTS Live`
- later `Studio > LLM Routing` integration

Fallback:
- none preferred for live lane
- Chatterbox may be used only as explicit fallback mode, not hidden substitution

---

### `moss_tts`
Primary use:
- premium single-speaker batch TTS
- narration
- cloned voice generation
- high-quality export workflows

Best for:
- Batch Narration
- Voice Clone output generation
- content creator exports
- polished long-form spoken content

Input shape:
- `voice_id`
- `text`
- optional chunking options
- output format
- optional generation params

Output shape:
- single file or chunked file outputs
- preview audio
- metadata summary

Notes:
- this is the flagship production lane for batch TTS
- use for quality-first generation, not low-latency live turn-taking

UI surfaces:
- `TTS File`
- `TTS Studio > Batch Narration`
- `TTS Studio > Voice Clone`

Fallback:
- `chatterbox` allowed only when explicitly selected or when MOSS route unavailable

---

### `moss_ttsd`
Primary use:
- multi-speaker dialogue generation
- scripted conversations
- podcast / drama / roleplay
- dialogue scene rendering

Best for:
- Dialogue Studio
- cinematic scenes
- multi-character voice exports
- long-form scripted conversation

Input shape:
- speaker map
- script or structured dialogue turns
- assigned voice IDs
- optional scene params

Output shape:
- full dialogue audio
- optional per-speaker / per-scene exports

Notes:
- this is not a live lane
- do not overload `TTS Live` with TTSD controls

UI surfaces:
- `TTS Studio > Dialogue Studio`

Fallback:
- none preferred
- if unavailable, UI should disable route rather than silently downgrade

---

### `moss_voice_generator`
Primary use:
- create new voice assets from textual descriptions
- character voice ideation
- style-safe custom voice creation

Best for:
- Voice Design
- internal preset creation
- creator-facing style exploration

Input shape:
- free-form voice prompt
- optional tags
- sample text
- optional advanced params

Output shape:
- preview audio
- saved voice asset metadata
- reusable voice registry entry

Notes:
- output should be persistable into the voice registry
- generated voices become selectable in later routes

UI surfaces:
- `TTS Studio > Voice Design`

Fallback:
- none needed
- if unavailable, Voice Design tab should show degraded state / disabled generation

---

### `moss_soundeffect`
Primary use:
- text-to-audio non-speech generation
- ambience
- stingers
- scene texture
- effects for creators and product polish

Best for:
- future Sound Design tab
- creator workflows
- transition sounds
- background beds
- agent/product earcons later

Input shape:
- sound prompt
- optional duration/style controls
- optional category tags

Output shape:
- generated non-speech audio
- downloadable audio asset
- reusable sound asset later

Notes:
- not part of current implementation pass
- should be planned as a future Studio tab

UI surfaces:
- future `TTS Studio > Sound Design`

Fallback:
- none

---

### `chatterbox`
Primary use:
- fallback batch TTS
- current reference UX
- stable production fallback while MOSS studio matures

Best for:
- explicit user-selected fallback
- known-good generation route
- continuity while Studio is being built out

Input shape:
- text
- voice selection or reference audio
- route-specific params

Output shape:
- generated audio file
- preview/playback
- downloadable asset

Notes:
- keep as fallback only
- do not let Chatterbox semantics leak into MOSS route assumptions

UI surfaces:
- current TTS pages where fallback is supported
- future Voice Library entries may reference fallback voices

Fallback:
- n/a

---

## Route Selection Matrix

| Use Case | Preferred Route | Fallback | UI Surface |
|---|---|---|---|
| Live agent reply | `moss_realtime` | optional explicit `chatterbox` fallback only | `TTS Live` |
| Telephony response lane | `moss_realtime` | optional explicit fallback | `TTS Live` / VoiceOps integration |
| Single-speaker narration | `moss_tts` | `chatterbox` | `TTS File`, `Studio > Batch Narration` |
| Voice cloning output | `moss_tts` | `chatterbox` | `Studio > Voice Clone` |
| New voice creation from text | `moss_voice_generator` | none | `Studio > Voice Design` |
| Multi-speaker dialogue | `moss_ttsd` | none | `Studio > Dialogue Studio` |
| Creator ambience/effects | `moss_soundeffect` | none | future `Studio > Sound Design` |
| Internal trusted fallback batch voice | `chatterbox` | none | current fallback paths |

---

## Canonical UI-to-Route Mapping

### `TTS Live`
Allowed routes:
- `moss_realtime`
- optional explicit `chatterbox` fallback

### `TTS File`
Allowed routes:
- `moss_tts`
- `chatterbox`

### `TTS Studio > Voice Library`
No generation route directly required
- registry surface only
- may preview through associated runtime target

### `TTS Studio > Voice Clone`
Primary:
- `moss_tts`

### `TTS Studio > Voice Design`
Primary:
- `moss_voice_generator`

### `TTS Studio > Batch Narration`
Primary:
- `moss_tts`
Fallback:
- `chatterbox`

### `TTS Studio > Dialogue Studio`
Primary:
- `moss_ttsd`

### `TTS Studio > LLM Routing`
This is orchestration config, not itself a generation engine.
Expected downstream routes:
- `moss_realtime`
- `moss_tts`
- later route-aware selection

---

## Canonical Model Root

OpenMOSS canonical model root:
`/mnt/aetherpro/models/audio/OpenMOSS-Team`

Expected children:
- `MOSS-Audio-Tokenizer`
- `MOSS-TTS`
- `MOSS-TTS-Realtime`
- `MOSS-TTSD-v1.0`
- `MOSS-VoiceGenerator`
- later `MOSS-SoundEffect`

Do not use stray cache/snapshot paths as runtime source of truth.

---

## Canonical Cache Root

Canonical HF cache root:
`/mnt/aetherpro/cache/hf`

Do not rely on:
- `~/.cache/huggingface`
for OpenMOSS production routes.

---

## Routing Rules

1. Route choice must be explicit.
2. No silent cross-route substitution except explicit fallback behavior.
3. `TTS Live` must not behave like `Voice Design`.
4. `Voice Design` outputs should be saveable as reusable voice registry entries.
5. `Voice Clone` should create reusable assets, not one-off throwaway uploads.
6. `LLM Routing` must remain provider-aware and route-aware.
7. Chatterbox remains a fallback/reference system, not the hidden backend for MOSS pages.

---

## Future Expansion

Planned later:
- `Sound Design` tab for `moss_soundeffect`
- asset layering (voice + ambience + transitions)
- creator export bundles
- full roundtrip `ASR -> LLM -> TTS`
- public secrets vault / credential isolation
