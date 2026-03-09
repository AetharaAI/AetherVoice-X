# OpenMOSS Realtime State Snapshot

Date: March 8, 2026

## Confirmed working

- `moss` sidecar builds and boots on the L4 node with CUDA and Python 3.12.
- Gateway -> TTS -> OpenMOSS realtime websocket and HTTP contract is working end to end.
- TTS Live can:
  - start a stream
  - send plain spoken text over websocket while keeping operator controls structured on the console side
  - receive `audio_chunk` frames
  - play streamed chunk audio in the browser
  - finalize and return a downloadable WAV after `End stream`
- Final audio artifacts are being written and can be replayed or transcribed through ASR File.
- The repo now also contains additive TTS Studio scaffolding:
  - voice registry backend
  - studio route catalog
  - provider-backed LLM routing config
  - tabbed studio UI shell

## Confirmed issues

- Cold-start latency is poor on the first live turn.
  - Observed behavior: first request is slow enough to feel non-realtime.
  - Observed behavior: second request in the warmed container is much faster and subjectively near-instant.
- Semantic alignment is not production-ready.
  - ASR transcription of generated WAVs shows the spoken output does not reliably match the requested response.
  - The current tag block is being spoken as content instead of acting like a control schema.
  - Example observed ASR transcript included phrases such as `Agent Tong`, `Jingyu Warm Cadence`, and `Jingyu Telephony`, which indicates markup-like text is leaking into the synthesized speech.
- Voice control is not product-ready.
  - Current realtime lane is effectively single-voice unless a prompt audio path is injected.
  - A real voice registry is now scaffolded, but OpenMOSS runtime binding for cloned/generated voices is not fully wired yet.

## Technical findings

### 1. Runtime latency is not just a transport issue

- The sidecar now emits live chunks and the browser plays them immediately.
- The first-turn slowness is therefore not a websocket or gateway defect.
- A major portion of the cold-path overhead was runtime compilation and model warmup.
- The current sidecar now defaults toward lower-latency operation:
  - `MOSS_REALTIME_ENABLE_COMPILE=false`
  - `MOSS_REALTIME_PREFILL_TEXT_LEN=6`
  - CUDA matmul precision raised to `high`

Inference:
- The first-turn/warm-turn gap strongly suggests warmup and internal model/runtime setup costs are a meaningful part of the latency profile.
- If P95 latency remains poor after warmup, then the model behavior itself is not acceptable for the telephony lane.

### 2. The current text-shaping path is likely wrong for this operator workflow

Observed implementation:
- The current sidecar uses the upstream assistant-delta pattern:
  - system prompt via `processor.make_ensemble(prompt_tokens)`
  - assistant prefix only
  - streamed text fragments are pushed directly as assistant text deltas

Upstream evidence:
- `moss_tts_realtime/example_llm_stream_to_tts.py` uses assistant-only streaming for LLM deltas.
- `moss_tts_realtime/app.py` also includes a text-only turn builder with:
  - explicit `user` turn text
  - `assistant` generation boundary

Inference:
- Our current lane is correct only if the incoming text is already a clean assistant response delta stream.
- It is not a good match for raw operator-entered prompt tags plus spoken text in one buffer.
- The tag block should not be sent verbatim to the assistant stream if the model is expected to speak only the body text.

### 3. Voice conditioning is incomplete

Observed state:
- Realtime lane currently exposes `default` or custom string entry, but there is no actual voice catalog behind it.
- Upstream MOSS realtime supports prompt-audio timbre conditioning.
- Upstream family also includes:
  - `MOSS-VoiceGenerator`
  - `MOSS-TTSD-v1.0`

Repo/operator state during this session:
- `MOSS-VoiceGenerator` was downloaded to block storage.
- `MOSS-TTSD-v1.0` was being downloaded to block storage.

Inference:
- Public Voice Studio should not expose a fake voice selector for realtime.
- It needs one of:
  - prompt-audio backed voice presets
  - generated voice assets promoted into a real catalog
  - imported Chatterbox voice assets mapped into a shared voice registry

## Product recommendation

### Realtime telephony lane

- Keep OpenMOSS realtime in experimental status until two things are fixed:
  - prompt/chat shaping
  - sustained warm-path latency under telephony expectations
- If those do not converge quickly, move the production telephony lane to a faster model such as Kokoro and keep OpenMOSS for R&D.

### Batch and studio lane

- Keep Chatterbox as the current stable batch lane.
- Evaluate `MOSS-TTSD-v1.0` for:
  - multi-speaker dialogue generation
  - continuation workflows
  - prompt-audio plus prompt-text cloning workflows
- Evaluate `MOSS-VoiceGenerator` as a design layer that can feed a future voice catalog.

## Immediate next steps

1. Separate operator metadata from spoken text in TTS Live.
   - Do not stream the tag block verbatim into assistant speech.
   - Treat tags as console-side controls until a real schema is defined.
2. Add an alternate sidecar mode that builds a proper text-only turn input with explicit `user` and `assistant` boundaries.
3. Add first-turn and second-turn timing capture to the sidecar response metadata and to the TTS Live UI.
4. Design a shared voice registry.
   - source A: Chatterbox predefined voices
   - source B: uploaded/clone voices
   - source C: future MOSS-generated voices
5. Finish runtime adapters for `MOSS-TTS`, `MOSS-TTSD-v1.0`, and `MOSS-VoiceGenerator` so the new studio surface is backed by actual model routes.
6. Evaluate whether `MOSS-TTSD-v1.0` should own the rich studio dialogue lane while a smaller model owns the low-latency telephony lane.

## Decision status

- OpenMOSS realtime integration: technically functioning
- OpenMOSS realtime telephony readiness: not yet approved
- OpenMOSS realtime studio readiness: experimental
