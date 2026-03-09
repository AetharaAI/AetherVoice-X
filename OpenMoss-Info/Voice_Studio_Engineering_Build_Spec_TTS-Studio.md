
**No breaking changes.**
This is an additive build. Existing working flows stay intact except for the one targeted fix on `TTS Live`: remove the bogus structured-tag injection path and replace it with the controls the realtime lane actually expects. The broader product split, voice registry, and LLM routing belong in a new `TTS Studio` section, not jammed into the current live page. That aligns with the notes you saved. 

---

# Aether Voice Studio — Engineering Spec v1

## 1) Objective

Build **Aether Voice Studio** as the unified voice control plane for:

* ASR Live
* ASR File
* TTS Live
* TTS File
* Voice cloning
* Voice design / character voice creation
* Batch narration
* Multi-speaker dialogue generation
* Future sound effects
* Future end-to-end voice loop: `ASR -> LLM -> TTS`

This is an **add-on architecture**, not a rewrite.

## 2) Hard constraints

### 2.1 No breaking changes

Do not break:

* current nav
* current ASR pages
* current TTS Live start/send/end contract shape unless absolutely necessary
* current streaming/playback path
* current output artifact handling
* Chatterbox fallback behavior

### 2.2 One surgical fix on `TTS Live`

The current raw structured-tag textarea is wrong for OpenMOSS realtime and should no longer be treated as the primary control surface. Replace that behavior with proper structured server-side fields. This is the only intended behavioral change on the current live lane. 

### 2.3 New capability goes into new surface

All new full-stack MOSS functionality belongs in a new top-level page:

* `TTS Studio`

Not in `TTS Live`.

---

# 3) Navigation / IA

## 3.1 Preserve existing nav

Keep existing items:

* Dashboard
* ASR Live
* ASR File
* TTS Live
* TTS File
* Triage
* Sessions
* Models
* Metrics

## 3.2 Add one new nav item

Insert:

* **TTS Studio**

Placement:

* directly under `TTS File`

Reason:

* keeps operations pages intact
* separates live ops from studio workflows
* avoids turning `TTS Live` into a landfill of unrelated controls

This matches the saved notes. 

---

# 4) Page responsibilities

## 4.1 TTS Live

Purpose:

* realtime operational lane only
* low-latency turn-taking
* session-bound voice playback
* websocket chunk streaming
* final WAV artifact on stream end

### Keep

* Start stream
* Send text
* End stream
* realtime model selector
* connection/session/chunks/final-audio status
* spoken body
* output surface

### Remove / replace

Remove the current primary use of:

* `Structured tags / directives` textarea as injected spoken content

Replace with:

* `Voice Preset`
* `Session Profile`
* `Style Controls` (collapsed)

  * tone
  * cadence
  * speaking style
  * latency/quality mode

These controls must be sent as structured fields to backend logic, **not prepended into the text body**.

### Optional compatibility bridge

Keep the old directives textarea only behind an:

* `Experimental Raw Directives` accordion

Default collapsed, hidden from normal use, clearly marked unsupported for OpenMOSS realtime.

## 4.2 TTS File

Purpose:

* simple batch single-speaker generation
* quick export lane
* route selection for batch TTS

Minimal additions allowed:

* `Route Target` dropdown

  * `moss_tts`
  * `chatterbox`
* output format
* chunking

## 4.3 TTS Studio

Purpose:

* full MOSS-family capability surface
* reusable voice asset management
* future LLM roundtrip orchestration control

Studio sub-tabs:

1. Voice Library
2. Voice Clone
3. Voice Design
4. Batch Narration
5. Dialogue Studio
6. LLM Routing
7. Advanced

---

# 5) TTS Studio page layout

## 5.1 Overall layout

Top header band:

* Page title: `TTS Studio`
* Active route target
* Selected voice
* Output target
* Save-to-library toggle

Below header:

* horizontal tabs or segmented tabs for studio modes

Bottom region:

* persistent output panel

  * waveform
  * playback
  * download
  * generation metadata
  * route used
  * voice used
  * duration
  * generation time

Borrow the **usability pattern** from Chatterbox:

* clean input area
* import reference workflow
* collapsible advanced controls
* output panel at bottom
  but do **not** copy Chatterbox backend assumptions. 

---

# 6) TTS Studio tabs

## 6.1 Voice Library

Purpose:

* browse, preview, tag, and reuse all voice assets

### UI

Filters:

* All
* Preset
* Cloned
* Generated
* Imported
* Fallback/Chatterbox

Fields per voice card:

* display name
* type
* source model
* runtime target
* tags
* preview button
* edit metadata
* duplicate
* archive

### Actions

* set default voice by route
* assign to realtime
* assign to narration
* assign to dialogue speaker slot

---

## 6.2 Voice Clone

Purpose:

* upload reference audio and generate reusable cloned voices

### UI

Fields:

* Voice name
* Tags
* Upload `.wav`
* Optional reference transcript
* Sample text input
* Target route default: `moss_tts`
* Generate preview
* Save to library

### Behavior

Imported clone references become reusable entries in Voice Library.
User should not need to re-upload the same reference every time.

---

## 6.3 Voice Design

Purpose:

* use `moss_voice_generator` to create voices from free-form description

### UI

Fields:

* Voice description prompt
* Optional tags:

  * gender
  * style
  * mood
  * use-case
* Sample text
* Optional decoding controls
* Generate preview
* Save to library

### Examples

* warm female dispatcher
* calm documentary narrator
* gritty field technician
* dramatic noir detective

---

## 6.4 Batch Narration

Purpose:

* high-quality single-speaker production via `moss_tts`

### UI

Fields:

* Source text / longform textarea
* Voice select
* Chunking toggle
* Chunk size
* Output format
* Quality profile
* Preview segment
* Generate full audio

### Output

* waveform
* download
* per-chunk metadata if chunking enabled

---

## 6.5 Dialogue Studio

Purpose:

* multi-speaker composition via `moss_ttsd`

### UI

Fields:

* Script editor
* speaker slots (`Speaker A`, `Speaker B`, etc.)
* voice assignment per speaker
* scene preview
* export final dialogue

### Future-friendly

Should support podcast, roleplay, dubbed scene, dramatic script.

---

## 6.6 LLM Routing

Purpose:

* configure the model that sits between ASR and TTS for full end-to-end roundtrip

This is where your `ASR -> LLM -> TTS` control surface lives.

### UI

Fields:

* Provider dropdown
* Base URL dropdown/input
* Model dropdown
* System prompt / response style
* Enable roundtrip toggle
* Response post-processing rules
* Prompt template for voice reply
* Test endpoint button

### Providers

Implement now:

* `OpenAI`
* `OpenRouter`
* `LiteLLM`

Stub:

* `Anthropic`

### Behavior by provider

#### OpenAI

* auto-fill official base URL
* fetch available models dynamically
* model dropdown populated from provider models endpoint

#### OpenRouter

* auto-fill OpenRouter base URL
* fetch available models dynamically

#### LiteLLM

* allow selection from known internal base URLs
* fetch available models from `/v1/models`
* must send authorization header
* populate dropdown from live endpoint, not hardcoded list

### Internal base URLs

Support two selectable internal endpoints:

* `api.aetherpro.tech/v1`
* `api.blackboxaudio.tech/v1`

The backend must map base URL -> correct auth token from env/secrets.

### Important rule

No secrets typed into frontend for current internal use.

For current internal build:

* provider keys/base URLs live in `.env`
* UI selects provider/base/model only

For future public production:

* replace with secrets vault / per-user credential store

---

## 6.7 Advanced

Purpose:

* power-user and operator-only controls

Collapsed by default.

Fields:

* runtime model paths
* cache paths
* output directories
* sample rate
* decode defaults
* model health
* loaded model state
* route target diagnostics

---

# 7) Backend architecture

## 7.1 Route separation

Do not hide distinct engines behind one vague endpoint.

Required route targets:

* `moss_realtime`
* `moss_tts`
* `moss_ttsd`
* `moss_voice_generator`
* `chatterbox` fallback

## 7.2 Realtime endpoints

Preserve existing live flow shape where possible.

### `POST /tts/realtime/start`

Request:

```json
{
  "session_id": "uuid-or-client-id",
  "voice_id": "voice_dispatcher_warm_01",
  "route_target": "moss_realtime",
  "sample_rate": 24000,
  "profile_id": "telephony_warm_v1",
  "style": {
    "tone": "warm",
    "cadence": "telephony",
    "latency_mode": "fast"
  },
  "reference_audio_id": null
}
```

### `POST /tts/realtime/send`

```json
{
  "session_id": "same-session-id",
  "text": "A technician is being dispatched to your location now.",
  "metadata": {
    "source": "ui"
  }
}
```

### `POST /tts/realtime/end`

```json
{
  "session_id": "same-session-id"
}
```

### Server rule

Do not prepend XML tags into spoken text.

The server should map voice/profile/style -> runtime conditioning logic.

---

## 7.3 Batch generation endpoint

### `POST /tts/generate`

```json
{
  "route_target": "moss_tts",
  "voice_id": "voice_doc_narrator_01",
  "text": "Long-form narration text goes here.",
  "chunking": {
    "enabled": true,
    "chunk_size": 350
  },
  "output_format": "wav",
  "params": {
    "quality_profile": "studio"
  }
}
```

Support route targets:

* `moss_tts`
* `moss_ttsd`
* `chatterbox`

---

## 7.4 Voice endpoints

### `POST /voices/import-reference`

Upload reference audio + metadata

### `POST /voices/create-from-description`

Generate voice using `moss_voice_generator`

### `POST /voices/preview`

Generate preview audio without saving

### `POST /voices/save`

Persist voice asset into registry

### `GET /voices`

List/filter voice library

### `GET /voices/{voice_id}`

Load single voice asset

### `PATCH /voices/{voice_id}`

Update metadata/default params/tags

### `POST /voices/{voice_id}/archive`

Archive voice without hard delete

---

## 7.5 LLM routing endpoints

### `GET /llm/providers`

Return supported providers

### `GET /llm/providers/{provider}/models`

Return live model list for provider/base URL

### `POST /llm/roundtrip/test`

Test the selected provider/model/base URL/auth path

### `POST /llm/roundtrip/respond`

Optional orchestration endpoint for:

* input transcript
* provider
* model
* voice target
* output TTS response

---

# 8) Voice registry schema

Use real persistence, not UI state.

## 8.1 Voice record

```json
{
  "voice_id": "voice_dispatcher_warm_01",
  "display_name": "Dispatcher Warm",
  "type": "generated",
  "source_model": "moss_voice_generator",
  "runtime_target": "moss_realtime",
  "reference_audio_path": null,
  "reference_text": null,
  "generation_prompt": "Warm, calm American female dispatcher voice with telephony-friendly cadence.",
  "default_params": {
    "sample_rate": 24000,
    "style": {
      "tone": "warm",
      "cadence": "telephony"
    }
  },
  "tags": ["warm", "dispatcher", "telephony"],
  "is_archived": false,
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

## 8.2 Cloned voice example

```json
{
  "voice_id": "voice_cj_clone_01",
  "display_name": "CJ Clone",
  "type": "cloned",
  "source_model": "moss_tts",
  "runtime_target": "moss_tts",
  "reference_audio_path": "/mnt/aetherpro/voices/references/cj_01.wav",
  "reference_text": "reference transcript here",
  "generation_prompt": null,
  "default_params": {
    "sample_rate": 24000
  },
  "tags": ["clone", "founder", "english"],
  "is_archived": false
}
```

## 8.3 Fallback voice example

```json
{
  "voice_id": "voice_chatterbox_emily",
  "display_name": "Emily",
  "type": "preset",
  "source_model": "chatterbox",
  "runtime_target": "chatterbox",
  "reference_audio_path": null,
  "reference_text": null,
  "generation_prompt": null,
  "default_params": {},
  "tags": ["fallback", "preset"]
}
```

---

# 9) LLM provider config schema

## 9.1 Provider config

```json
{
  "provider_id": "litellm_internal_primary",
  "provider_type": "litellm",
  "display_name": "AetherPro Internal Models",
  "base_url": "https://api.aetherpro.tech/v1",
  "models_endpoint": "/models",
  "auth_strategy": "env_token",
  "env_key_name": "AETHERPRO_API_KEY",
  "is_enabled": true
}
```

## 9.2 UI behavior

* user selects provider
* UI populates allowed base URL(s)
* backend calls provider’s live models endpoint
* backend injects auth header using mapped secret
* model dropdown is populated dynamically

---

# 10) End-to-end roundtrip mode

## 10.1 Goal

Enable:

1. user speaks
2. ASR realtime transcribes
3. selected LLM generates response text
4. selected TTS route voices response
5. audio streams back

## 10.2 Placement

This belongs under:

* `TTS Studio > LLM Routing`
  and later optionally surfaced as a toggle on `TTS Live`

## 10.3 Initial scope

Do not fully wire agent orchestration on this pass.

Wire the config surface and backend route contracts first.

---

# 11) Data + secrets rules

## 11.1 Current internal build

Allowed:

* provider secrets in `.env`
* internal base URLs in config
* UI chooses provider/base/model
* backend maps to correct token

## 11.2 Future public build

Required later:

* secrets vault / per-user provider credentials
* encrypted storage
* no raw secret passing to browser runtime

---

# 12) Styling / layout direction

## 12.1 TTS Live

Do not redesign from scratch.
Only:

* remove broken structured-tag workflow
* add proper collapsed style controls
* improve spacing
* preserve working layout

## 12.2 TTS Studio

This is the big polish surface.
Direction:

* feels like a real studio
* larger cards
* more breathing room
* bottom output panel
* collapsible advanced sections
* clean voice import workflow
* clear route separation

Use the Chatterbox UX pattern as inspiration for:

* imports
* parameter accordions
* generated audio display
* general ease of use

Do **not** mirror Chatterbox backend semantics.

---

# 13) Implementation phases

## Phase 1 — Safe fixes

* finish `MOSS-TTS` download
* normalize ownership on `MOSS-TTS`
* remove structured-tag injection from live path
* add server-side voice/style fields for realtime contract

## Phase 2 — Registry

* implement voice registry backend
* wire reusable voices
* support import + save + preview

## Phase 3 — Studio shell

* add `TTS Studio` nav page
* add tabs and base layout
* wire Voice Library, Voice Clone, Voice Design

## Phase 4 — Batch lanes

* Batch Narration via `moss_tts`
* Dialogue Studio via `moss_ttsd`

## Phase 5 — LLM routing

* provider dropdown
* base URL/model fetch
* auth-aware backend proxy
* roundtrip config panel

## Phase 6 — Later

* SoundEffect
* secrets vault
* public multi-tenant credential handling

---

# 14) Explicit non-goals for this pass

* no breaking rewrite of ASR pages
* no breaking rewrite of VoiceOps telephony app
* no replacement of Chatterbox right now
* no secrets-vault implementation yet
* no hard dependency on Anthropic support
* no giant redesign of current operational pages

---


# Appendix A — UX behavior, helpers, examples, and non-breaking constraints

## A1. Non-breaking UI rule

This implementation is additive. Existing working pages and contracts must remain intact except for the one targeted fix on `TTS Live`:

* remove the current structured-tag / XML directive injection behavior from the live lane
* replace it with structured realtime controls that map to backend state instead of being prepended into spoken text

No other breaking changes to `TTS Live`, ASR pages, or current streaming behavior are allowed.

## A2. Collapsible UX pattern

`TTS Studio` should use collapsible sections throughout, similar to the Chatterbox interaction pattern.

Use collapsible sections for:

* Generation Parameters
* Voice Import / Reference Details
* Server / Runtime Configuration
* Tips & Examples
* Advanced / Diagnostics

Default behavior:

* simple controls visible by default
* advanced/operator controls collapsed by default
* bottom output panel always visible after generation

## A3. Examples everywhere

Every major input surface should include:

* placeholder example text
* inline helper text
* tooltip/help icon
* at least 3 to 6 concrete examples

Users should never have to guess what a field means.

### Required example coverage

Examples must be shown for:

* voice description prompts
* clone reference quality guidance
* narration text input
* dialogue script input
* LLM routing provider/base/model usage
* style/tone selectors
* sample voice presets

## A4. Voice Design example presets

Preload example prompts for `Voice Design` so users can instantly test the system.

Include at least these examples:

* Warm female dispatcher
* Calm documentary narrator
* Gritty field technician
* Noir detective monologue
* Stoic motivational narrator
* Overworked parent bedtime storyteller
* Scientific abstract reader
* Conspiracy podcast host
* Children’s story narrator
* Fairy tale villain monologue

Each example should:

* populate the prompt field
* populate suggested tags
* optionally set recommended defaults for route/preview

## A5. Voice asset samples

The Studio should support seeded demo/sample assets so the page is not empty on first load.

Seed examples for:

* generated voices
* cloned reference voices
* narration presets
* dialogue voices

These should live as demo records in the voice registry, clearly marked as sample/demo.

## A6. Tips & Tricks section

Add a collapsible `Tips & Tricks` section near the output panel or bottom of each relevant Studio tab.

Examples of content:

* Best reference audio practices
* Recommended chunk sizes for long-form narration
* When to use Realtime vs TTS vs TTSD
* How to write good voice design prompts
* Why cloned voices need clean input audio
* Recommended output formats by use case

This section should be content-driven and easy to update without code surgery.

## A7. Output panel behavior

Every generation tab should render output in a consistent bottom panel with:

* waveform preview
* play button
* download button
* route used
* voice used
* generation time
* output duration
* metadata summary

## A8. Helper text direction

Use plain-English helper copy, not research-paper nonsense.
The UI should feel like a pro studio, not a graduate seminar.

---

## Add this mini appendix too

# Appendix B — Voice Design preset examples

## Example preset: Warm female dispatcher

Prompt:
“Warm, calm American female dispatcher voice with clear enunciation, telephony-friendly pacing, and reassuring authority.”

Tags:

* warm
* dispatcher
* telephony
* support

## Example preset: Calm documentary narrator

Prompt:
“Calm, steady mid-range narrator voice with documentary pacing, clean diction, and a polished professional tone.”

Tags:

* narrator
* documentary
* calm
* polished

## Example preset: Gritty field technician

Prompt:
“Grounded working-class male voice with slight rasp, practical delivery, calm confidence, and no theatrical exaggeration.”

Tags:

* technician
* gritty
* practical
* field-service

## Example preset: Noir detective

Prompt:
“Low, dramatic noir detective voice with controlled grit, deliberate pacing, and late-night monologue energy.”

Tags:

* noir
* detective
* dramatic
* monologue

## Example preset: Stoic motivational narrator

Prompt:
“Deep, steady, emotionally controlled motivational narrator voice with stoic restraint, clarity, and calm authority.”

Tags:

* stoic
* motivational
* disciplined
* narrator

## Example preset: Scientific abstract reader

Prompt:
“Neutral, precise, articulate voice for reading scientific or technical content with minimal drama and high clarity.”

Tags:

* technical
* scientific
* neutral
* precise

## Example preset: Children’s story narrator

Prompt:
“Gentle, expressive storyteller voice with warmth, clarity, and playful but controlled energy suitable for children’s stories.”

Tags:

* children
* storyteller
* warm
* expressive

## Example preset: Fairy tale villain monologue

Prompt:
“Elegant theatrical villain voice with controlled menace, articulate diction, and dramatic storytelling presence.”

Tags:

* villain
* theatrical
* fantasy
* dramatic

---

