# Polymorph Voice Integration Note

This note is for wiring `Polymorph` into `Aether Voice X` without rediscovering the contract.

## Goal

Expose two voice buttons inside Polymorph:

1. `Transcribe`
   - live mic capture
   - realtime ASR only
   - final transcript lands in the text box

2. `Voice`
   - full spoken interaction loop
   - first target should be turn-based voice mode, not hard realtime

## Base URLs

Assume the public edge is the gateway served at:

- `https://asr.aetherpro.us`

The gateway exposes both REST and websocket routes.

## Button 1: Transcribe

### Start the stream

POST:

- `/api/v1/asr/stream/start`

Body:

```json
{
  "model": "auto",
  "language": "auto",
  "sample_rate": 16000,
  "encoding": "pcm_s16le",
  "channels": 1,
  "triage_enabled": false,
  "metadata": {
    "source": "polymorph-mic"
  }
}
```

Expected response:

```json
{
  "session_id": "sess_live_...",
  "ws_url": "/api/v1/asr/stream/{session_id}",
  "model_requested": "auto",
  "model_used": "...",
  "fallback_used": false
}
```

### Open websocket

Connect to:

- `/api/v1/asr/stream/{session_id}`

### Send audio frames

Send JSON messages shaped like:

```json
{
  "type": "audio_frame",
  "seq": 1,
  "timestamp_ms": 1234,
  "sample_rate": 16000,
  "encoding": "pcm_s16le",
  "channels": 1,
  "payload_b64": "..."
}
```

Notes:

- audio must be mono
- PCM 16-bit little-endian
- 16 kHz
- the existing browser implementation base64-encodes raw PCM16 frames

### Receive transcript events

The websocket emits:

- `partial_transcript`
- `final_transcript`

Typical payloads:

```json
{
  "type": "partial_transcript",
  "text": "partial text"
}
```

```json
{
  "type": "final_transcript",
  "text": "final cleaned text",
  "segments": [
    {
      "start_ms": 0,
      "end_ms": 1000,
      "text": "final cleaned text"
    }
  ]
}
```

### End the stream

Send:

```json
{
  "type": "end_stream"
}
```

### What Polymorph should do

- while the mic is open, update live transcript UI from `partial_transcript`
- when `final_transcript` arrives, write the final text into the main input box
- treat final transcript as the source of truth, not partial text

## Button 2: Voice

Do not start with hard realtime.

First implement:

- `ASR -> LLM -> turn-based TTS`

That means:

1. Use the `Transcribe` button flow above to capture speech.
2. Wait for the final ASR transcript.
3. Send the final text to Polymorph's LLM layer.
4. Take the full LLM response.
5. Send that full response to the batch TTS route.
6. Play the returned audio.

## Turn-Based TTS Route

POST:

- `/api/v1/tts/synthesize`

Body:

```json
{
  "model": "moss_tts",
  "voice": "your_voice_id_or_default",
  "text": "Full LLM response text",
  "stream": false,
  "sample_rate": 24000,
  "format": "wav",
  "metadata": {
    "source": "polymorph-turn-based"
  }
}
```

Expected result includes:

- `audio_url`
- `model_used`
- `duration_ms`
- `artifacts`

Polymorph should fetch/play the returned `audio_url`.

## Realtime TTS Route

This exists, but should not be Polymorph's first integration target.

Start stream:

- `POST /api/v1/tts/stream/start`

Websocket:

- `/api/v1/tts/stream/{session_id}`

Client text messages:

```json
{
  "type": "text_chunk",
  "text": "some text"
}
```

To finalize:

```json
{
  "type": "complete"
}
```

Important current truth:

- current `moss_realtime` lane is effectively one utterance per stream
- after completion, sending another text chunk on the same stream returns `409 Conflict`
- do not model this as an unlimited open conversation socket yet

## Recommended Polymorph Rollout Order

### Phase 1

- add `Transcribe` button
- live ASR fills the text box
- no TTS involved

### Phase 2

- add `Voice` button
- use finalized ASR transcript
- call Polymorph LLM
- synthesize full reply with turn-based TTS
- play final audio

### Phase 3

- add realtime voice mode only after turn-based mode is stable

## Why This Order

- realtime ASR is already strong
- turn-based voice is easier to make trustworthy
- current realtime TTS still has speaker-identity limitations
- this gets a working personal talking agent faster

## Repo Files That Define The Current Contract

- `services/frontend/src/hooks/useASRStream.ts`
- `services/frontend/src/hooks/useTTSStream.ts`
- `services/gateway/app/routers/asr.py`
- `services/gateway/app/routers/tts.py`

## One-Line Implementation Instruction

For Polymorph, wire the mic button to the live ASR websocket contract first, then wire the voice button to `ASR final transcript -> LLM -> /api/v1/tts/synthesize` before attempting hard realtime speech output.
