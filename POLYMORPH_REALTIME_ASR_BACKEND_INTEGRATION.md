# PolyMorph Realtime ASR Backend Integration

This note tells Codex exactly how to call the Aether Voice realtime ASR backend so PolyMorph behaves like the working `ASR Live` tab.

## Non-negotiable Rule

Do not connect PolyMorph directly to the internal Voxtral container.

Use the gateway flow that `ASR Live` already uses:

1. `POST /v1/asr/stream/start`
2. open the returned websocket path at `/api/v1/asr/stream/{session_id}`
3. send `audio_frame` events
4. send `end_stream`
5. read `partial_transcript` and `final_transcript`

That is the known-good path.

## Working References

The exact working implementation lives here:

- [useASRStream.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/hooks/useASRStream.ts)
- [asr.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/api/asr.ts)
- [client.ts](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/frontend/src/api/client.ts)
- [asr.py](/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/gateway/app/routers/asr.py)

## Base URLs

For the deployed ASR Live surface, use:

- HTTP base: `https://asr.aetherpro.us/api`
- WebSocket base: `wss://asr.aetherpro.us`

If PolyMorph is behind the same reverse proxy and same origin, relative paths are fine:

- API base: `/api`
- WS base: same origin upgraded to `ws` or `wss`

If PolyMorph runs on another origin like `http://localhost:33333`, prefer explicit absolute URLs above unless you proxy the requests through the PolyMorph backend.

## Auth

Current voice stack config on this repo is:

- `AUTH_MODE=optional`
- gateway accepts either:
  - no auth at all in optional mode
  - `X-API-Key: <key>`
  - `Authorization: Bearer <valid JWT>`

Important:

- Do not send a fake or stale bearer token.
- A bad bearer token causes `401 Invalid bearer token` before the stream starts.
- For the current VM setup, if PolyMorph does not already have a valid JWT or API key, omit `Authorization` entirely.

This is the exact reason the earlier PolyMorph attempt failed.

## Step 1: Start The Stream

Send:

`POST https://asr.aetherpro.us/api/v1/asr/stream/start`

Headers:

- `Content-Type: application/json`
- optionally `X-API-Key: ...`
- do not send `Authorization` unless it is a valid JWT for this gateway

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
    "source": "polymorph_voice_mode",
    "extra": {
      "surface": "polymorph",
      "mode": "live_mic"
    }
  }
}
```

Notes:

- `model: "auto"` is the same default behavior as ASR Live.
- `model: "voxtral_realtime"` is also valid if PolyMorph wants to force Voxtral.
- Required audio contract is `16000 Hz`, `pcm_s16le`, `1 channel`.

Expected response:

```json
{
  "session_id": "sess_live_...",
  "ws_url": "/api/v1/asr/stream/sess_live_...",
  "expires_in_seconds": 3600,
  "model_requested": "auto",
  "model_used": "voxtral_realtime",
  "fallback_used": false
}
```

Important:

- `ws_url` is normally relative.
- PolyMorph must resolve it against the websocket base.
- For the deployed domain that becomes:
  - `wss://asr.aetherpro.us/api/v1/asr/stream/{session_id}`

## Step 2: Open The Gateway WebSocket

Open:

`wss://asr.aetherpro.us/api/v1/asr/stream/{session_id}`

Do not add custom query params unless the gateway is later updated to expect them.

This socket is the gateway proxy, not Voxtral directly.

## Step 3: Send Audio Frames

Send JSON messages of this shape:

```json
{
  "type": "audio_frame",
  "seq": 1,
  "timestamp_ms": 0,
  "sample_rate": 16000,
  "encoding": "pcm_s16le",
  "channels": 1,
  "payload_b64": "<base64 PCM16 little-endian bytes>"
}
```

Exact behavior used by ASR Live:

- browser mic audio is captured at `16000 Hz`
- mono channel only
- each chunk is converted from float samples to signed 16-bit PCM
- raw PCM bytes are base64 encoded into `payload_b64`

`payload_b64` is not WAV.
It is raw PCM16 little-endian audio bytes.

## Step 4: End The Stream

When the user stops talking or presses stop, send:

```json
{
  "type": "end_stream"
}
```

This is what causes the backend to flush the final Voxtral transcript.

Do not just close the socket immediately if you want the final transcript.

## Events PolyMorph Must Handle

### Partial transcript

```json
{
  "type": "partial_transcript",
  "session_id": "sess_live_...",
  "seq": 12,
  "stable": false,
  "text": "partial text here",
  "start_ms": 0,
  "end_ms": 1440
}
```

Behavior:

- update the live transcript view in place
- this is interim text

### Final transcript

```json
{
  "type": "final_transcript",
  "session_id": "sess_live_...",
  "text": "final normalized transcript here",
  "segments": [
    {
      "segment_id": "seg_1",
      "start_ms": 0,
      "end_ms": 3120,
      "text": "final normalized transcript here"
    }
  ]
}
```

Behavior:

- treat this as the finished transcript for the turn
- push this finalized text into the PolyMorph voice input pane
- stop mic capture and close the websocket on the client side after this lands

## Browser Implementation Notes

PolyMorph should match the ASR Live behavior:

1. call `navigator.mediaDevices.getUserMedia({ audio: true })`
2. create an `AudioContext({ sampleRate: 16000 })`
3. capture mono mic frames
4. convert float samples to PCM16
5. base64 encode the PCM bytes
6. send `audio_frame` JSON messages
7. on stop, send `end_stream`
8. wait for `final_transcript`

## Minimal TypeScript Skeleton

```ts
const API_BASE = "https://asr.aetherpro.us/api";
const WS_BASE = "wss://asr.aetherpro.us";

type StartResponse = {
  session_id: string;
  ws_url: string;
  model_used?: string;
  fallback_used?: boolean;
};

function encodePcm16(samples: Float32Array): string {
  const buffer = new ArrayBuffer(samples.length * 2);
  const view = new DataView(buffer);
  for (let i = 0; i < samples.length; i += 1) {
    const sample = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(i * 2, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
  }
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

function resolveWsUrl(path: string): string {
  if (/^wss?:\/\//.test(path)) return path;
  return `${WS_BASE}${path.startsWith("/") ? path : `/${path}`}`;
}

async function startRealtimeAsr(): Promise<StartResponse> {
  const response = await fetch(`${API_BASE}/v1/asr/stream/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "auto",
      language: "auto",
      sample_rate: 16000,
      encoding: "pcm_s16le",
      channels: 1,
      triage_enabled: false,
      metadata: {
        source: "polymorph_voice_mode",
        extra: {
          surface: "polymorph",
          mode: "live_mic"
        }
      }
    })
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return await response.json();
}

async function connectPolymorphAsr(onPartial: (text: string) => void, onFinal: (text: string) => void) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const start = await startRealtimeAsr();
  const socket = new WebSocket(resolveWsUrl(start.ws_url));
  const ctx = new AudioContext({ sampleRate: 16000 });
  const source = ctx.createMediaStreamSource(stream);
  const processor = ctx.createScriptProcessor(4096, 1, 1);
  let seq = 0;

  socket.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    if (payload.type === "partial_transcript" && payload.text) {
      onPartial(payload.text);
    }
    if (payload.type === "final_transcript" && payload.text) {
      onFinal(payload.text);
      stream.getTracks().forEach((track) => track.stop());
      processor.disconnect();
      source.disconnect();
      ctx.close();
      socket.close();
    }
  };

  socket.onopen = () => {
    processor.onaudioprocess = (evt) => {
      seq += 1;
      const input = evt.inputBuffer.getChannelData(0);
      socket.send(JSON.stringify({
        type: "audio_frame",
        seq,
        timestamp_ms: Math.round(ctx.currentTime * 1000),
        sample_rate: 16000,
        encoding: "pcm_s16le",
        channels: 1,
        payload_b64: encodePcm16(input)
      }));
    };

    source.connect(processor);
    processor.connect(ctx.destination);
  };

  return {
    stop: () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "end_stream" }));
      }
    }
  };
}
```

## Common Failure Modes

### `401 Invalid bearer token`

Cause:

- PolyMorph sent `Authorization: Bearer ...` with a token the gateway does not accept.

Fix:

- remove the `Authorization` header entirely for the current optional-auth VM
- or send a valid JWT
- or use `X-API-Key`

### Websocket connect failure

Cause:

- PolyMorph tried to connect directly to Voxtral
- or resolved the websocket path against the wrong base URL

Fix:

- call gateway start first
- use returned `ws_url`
- resolve it against `wss://asr.aetherpro.us`

### No final transcript

Cause:

- client closed the socket without sending `end_stream`

Fix:

- always send `{ "type": "end_stream" }`
- wait for `final_transcript`

### Wrong audio format

Cause:

- sending WAV blobs
- sending float arrays directly
- wrong sample rate
- stereo input not reduced to one channel

Fix:

- send raw PCM16 little-endian bytes in base64
- `16000 Hz`
- `channels: 1`

## Codex Instruction Block

Use this exact instruction in PolyMorph if needed:

```text
Integrate realtime ASR using the existing Aether Voice gateway contract, not direct Voxtral calls.

Use:
- POST https://asr.aetherpro.us/api/v1/asr/stream/start
- then connect to the returned websocket path on wss://asr.aetherpro.us

Start payload:
- model: "auto"
- language: "auto"
- sample_rate: 16000
- encoding: "pcm_s16le"
- channels: 1
- triage_enabled: false
- metadata.source: "polymorph_voice_mode"

Websocket send events:
- audio_frame with base64 raw PCM16 little-endian mono audio
- end_stream when stopping

Websocket receive events:
- partial_transcript
- final_transcript

Do not send Authorization unless it is a valid gateway JWT.
For the current VM, omit Authorization entirely unless an API key or valid JWT is explicitly wired.

Match the behavior in Aether Voice X:
- services/frontend/src/hooks/useASRStream.ts
- services/gateway/app/routers/asr.py
```

