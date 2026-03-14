# Realtime Stack Snapshot

Date: `2026-03-14`

This snapshot captures the first verified state where the current voice stack has both:

- stable realtime ASR through `voxtral_realtime`
- stable low-latency realtime TTS through `kokoro_realtime`

This is the first state that clearly feels like the intended operator product lane.

## Frozen Truth

- `voxtral_realtime` is the working realtime ASR lane and is actively used from the browser.
- `kokoro_realtime` is the working default realtime TTS lane.
- The public streaming contracts remain unchanged:
  - ASR: `POST /v1/asr/stream/start` + websocket stream
  - TTS: `POST /v1/tts/stream/start` + websocket stream
- `moss_realtime` remains present and functional, but it is no longer the default live reply lane.
- `moss_tts`, `moss_ttsd`, and `moss_voice_generator` remain part of the studio/family roadmap and were not torn apart to get this result.

## Verified On This Snapshot

Operator-provided UI and log captures show:

- the live TTS page running with:
  - `Realtime model = kokoro_realtime`
  - `Voice preset = Sky`
  - `Sample rate = 24000 Hz`
  - runtime path used = `kokoro_realtime`
- the live session returning chunked audio in the browser
- the gateway and TTS service forwarding the Kokoro stream lifecycle cleanly
- the Kokoro sidecar responding healthy on `http://kokoro:8026/health`

Observed log sequence in the provided captures:

- `POST /v1/stream/start` to Kokoro returned `200`
- `tts_stream_started`
- websocket accepted on `/api/v1/tts/stream/{session_id}`
- `tts_stream_text_push`
- `POST /v1/stream/{session_id}/text` to Kokoro returned `200`
- `tts_stream_first_chunk`
- `tts_stream_chunk_batch`
- `tts_stream_text_complete`
- `POST /v1/stream/{session_id}/complete` to Kokoro returned `200`

## Runtime Architecture At This Moment

### Realtime ASR

- Browser / operator UI
- Gateway websocket proxy
- ASR service adapter
- Voxtral upstream on the dedicated sidecar

### Realtime TTS

- Browser / operator UI
- Gateway websocket proxy
- TTS service streaming lifecycle
- `kokoro_realtime` adapter
- Kokoro sidecar

### Studio / Specialized TTS

- `moss_realtime`: experimental live lane, no longer the default
- `moss_tts`: batch narration path in progress
- `moss_ttsd`: dialogue path in progress
- `moss_voice_generator`: studio voice-design path available
- `chatterbox`: stable fallback and compatibility batch path

## GPU Layout In This Snapshot

- GPU `1`: in-stack ASR lane
- GPU `2`: Voxtral realtime ASR
- GPU `3`: Kokoro realtime TTS primary lane
- GPU `3`: also shared opportunistically by `moss_voice_generator` and external Chatterbox usage when needed
- GPU `0`: OpenMOSS family runtime lanes

## Product Meaning

This snapshot matters because the stack now has a credible realtime conversation substrate:

- speech in through Voxtral
- low-latency speech out through Kokoro
- stable gateway contracts in the middle

That is the first state where the separate VoiceOps / telephony client can be handed a clean API contract without pretending the TTS lane is still provisional.

## Immediate Follow-On Work

1. Freeze this transport/routing state.
2. Write the VoiceOps-facing API handoff against the existing public endpoints.
3. Build the first clean `ASR -> LLM -> TTS` conversational loop using this exact lane.
4. Keep MOSS isolated for studio, cloning, and deeper voice-quality experiments.
