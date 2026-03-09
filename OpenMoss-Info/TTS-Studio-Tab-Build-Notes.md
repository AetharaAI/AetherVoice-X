
## Product split

Keep the current nav for operations:

* Dashboard
* ASR Live
* ASR File
* TTS Live
* TTS File
* Triage
* Sessions
* Models
* Metrics

Then add a **new first-class section**:

* **TTS Studio**

That is where the full MOSS family lives.

This avoids blowing up your current flow, and it avoids turning `TTS Live` into a junk drawer full of controls that belong to completely different generation modes.

## What each page should be for

### TTS Live

This stays narrow and operational:

* Real-time lane only
* Start stream / stop stream
* session id
* voice preset picker
* spoken text
* maybe advanced realtime options in a collapsed section
* playback / chunks / final audio

No cloning workflow here. No voice creation workflow here. No batch dialogue workflow here. This page is for **live turn-taking**.

### TTS File

This becomes batch generation:

* single-speaker batch TTS
* long text
* output format
* maybe chunking
* maybe route selector for `moss_tts` vs `chatterbox`

### TTS Studio

This becomes the capability surface for the MOSS family:

* **Voice Library**
* **Voice Clone**
* **Voice Design**
* **Batch Narration**
* **Dialogue Studio**
* later **Sound Effects**

That is the page that should feel like your Chatterbox screen, but done properly and mapped to the real models.

## The architecture you want Codex to implement

This is the clean split.

### 1. Voice registry

You need a real server-side voice registry, not “dropdown values hardcoded in UI.”

Each voice record should store:

* `voice_id`
* `display_name`
* `type`: `preset | cloned | generated`
* `source_model`: `moss_voice_generator | moss_tts | chatterbox | imported`
* `reference_audio_path` optional
* `reference_text` optional
* `generation_prompt` optional
* `default_params` object
* `runtime_target`: `moss_realtime | moss_tts | moss_ttsd | chatterbox`
* tags like `warm`, `telephony`, `support`, `narration`

That gives you the behavior you described:

* import a `.wav`
* it becomes part of the library
* later it appears in dropdowns
* you do not re-upload it every time like a caveman

### 2. Route-specific MOSS execution

Right now the app needs explicit model lanes, because these are not all the same thing.

#### `moss_realtime`

Use for:

* live agent turns
* per-session history
* low-latency streaming
* persistent voice binding per session

Do **not** prepend XML-ish tags into the spoken body. The MOSS family describes Realtime as a context-aware multi-turn streaming model for voice agents, conditioned on dialogue history; VoiceGenerator is the part explicitly aimed at creating custom timbres from free-form text descriptions. ([Hugging Face][2])

So for Realtime, the UI controls should map to server-side state, not get injected as literal prompt junk.

#### `moss_tts`

Use for:

* premium single-speaker batch generation
* narration
* long-form clean output
* voice cloning
* controllable production output

OpenMOSS positions MOSS-TTS as the flagship production-ready backbone, and even calls out the 8B “Delay” model as the production priority. ([Hugging Face][1])

#### `moss_ttsd`

Use for:

* scripted dialogue
* multi-speaker scenes
* podcast/drama style generation
* role-play, dubbing, conversational long-form output

That is exactly what the family says TTSD is for. ([Hugging Face][3])

#### `moss_voice_generator`

Use for:

* create a new voice from text description
* “warm female dispatcher”
* “calm documentary male narrator”
* “gritty field technician with slight rasp”
* save result into voice registry

That is the correct model for text-described voice creation. ([Hugging Face][2])

## UI structure for TTS Studio

This is what I’d tell Codex to build.

### Section header

Top band:

* active route selector
* selected voice
* output target
* save to library toggle

Then tabs inside TTS Studio:

### Tab 1: Voice Library

Purpose: browse and manage all available voices.

Show:

* search
* filters: preset / cloned / generated / imported
* cards or rows with:

  * name
  * type
  * runtime target
  * tags
  * preview button
  * edit metadata
  * duplicate
  * archive

This should also be the place to choose “default voice” per route.

### Tab 2: Voice Clone

Purpose: upload a reference and generate reusable cloned voices.

Controls:

* upload `.wav`
* optional transcript/reference text
* target route: `moss_tts` default
* voice display name
* tags
* generate sample text box
* output preview
* save to library

This is your Chatterbox-style import flow, but now it becomes a real asset pipeline.

### Tab 3: Voice Design

Purpose: use MOSS-VoiceGenerator.

Controls:

* text description prompt
* gender/style/emotion tags if useful
* sample text
* optional decoding params
* generate preview
* save to voice library

This is where the “character voice” workflow lives.

### Tab 4: Batch Narration

Purpose: long-form single-speaker TTS.

Controls:

* source text
* selected voice
* route defaults to `moss_tts`
* chunking
* output format
* quality/latency profile
* preview segment
* full export

This is basically your “file TTS but production-grade.”

### Tab 5: Dialogue Studio

Purpose: multi-speaker composition via TTSD.

Controls:

* script editor
* speaker assignments
* select voices for each speaker
* scene preview
* export full dialogue audio

This page is where your future podcast/drama/use-case money lives.

### Tab 6: Advanced

Collapsed by default. Hidden from casual users.

Contains:

* runtime model path
* server route target
* cache path
* sample rate
* decode config defaults
* maybe model health / loaded model info

This gives you the “server configuration” concept you liked from Chatterbox, without vomiting it across the main UI.

## What should change on the current TTS Live page

Minimal breaking change version:

Remove or de-emphasize:

* raw “structured tags / directives” textarea as a first-class control

Replace it with:

* **Voice Preset**
* **Session Profile**
* optional **Style Controls** section

  * tone
  * cadence
  * speaking style
  * latency/quality mode

Those values go to the backend as structured fields, and the backend decides how to translate them into:

* voice binding
* prompt state
* reference audio
* runtime parameters

The current tags field can remain temporarily under an “experimental / raw directives” accordion if you want to preserve branch continuity, but it should stop being the main UX. Because right now it encourages the exact wrong abstraction.

## The backend contract Codex should implement

Not code here, just the shape.

### Realtime request

`POST /tts/realtime/start`

* `session_id`
* `voice_id`
* `route_target = moss_realtime`
* `sample_rate`
* `profile_id`
* optional `reference_audio_id`
* optional style object

`POST /tts/realtime/send`

* `session_id`
* `text`
* optional `metadata`

`POST /tts/realtime/end`

* `session_id`

That is the contract. Not “jam tags and body together and pray.”

### Voice creation endpoints

`POST /voices/import-reference`
`POST /voices/create-from-description`
`POST /voices/preview`
`POST /voices/save`

### Batch generation

`POST /tts/generate`
with explicit route:

* `moss_tts`
* `moss_ttsd`
* `chatterbox`

That route select matters. No more hiding fundamentally different backends behind one muddy button.

## What to tell Codex, plainly

Here’s the job:

**Do not patch the current TTS Live page into a universal studio.**
Create a new `TTS Studio` section and wire the MOSS family the way the family is actually divided.

Implementation order by ROI:

1. **Finish MOSS-TTS base model download and normalize ownership** - (CJ is doing this)
2. **Refactor Realtime contract**

   * stop prepending raw tags into spoken text
   * make session voice binding real
3. **Add voice registry**

   * cloned / generated / preset voices become reusable assets
4. **Add TTS Studio page**

   * Voice Library
   * Voice Clone
   * Voice Design
   * Batch Narration
   * Dialogue Studio
5. **Keep Chatterbox as fallback only**
6. **Add SoundEffect later**, not now

That sequence is the least breaking and highest leverage.

## Your Chatterbox screenshots matter for one reason

Not because Chatterbox is the architecture to copy.

Because it proves the UX pattern users expect:

* text input
* voice mode
* reference upload
* saved references
* advanced parameters in collapsible sections
* generated output panel at bottom
* sane layout with breathing room

That is the part worth borrowing.

So yes:

* mirror the usability pattern
* do **not** mirror the backend assumptions

## Final verdict

You’re right to stop treating this like a toy.

The right product shape is:

* **TTS Live** for real-time ops
* **TTS File** for simple batch jobs
* **TTS Studio** for the full MOSS family and reusable voice assets

And the core technical fix is:

* **stop treating MOSS Realtime like Chatterbox with different branding**
* **start treating the MOSS family as separate but coordinated engines**, because that is exactly how OpenMOSS presents the family. ([Hugging Face][3])

