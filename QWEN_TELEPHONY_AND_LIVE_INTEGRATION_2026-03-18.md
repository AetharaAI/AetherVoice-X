# Qwen Telephony And Live Integration

## Current Truth

- `qwen_customvoice` is operational as a modular provider-backed batch lane.
- `qwen_customvoice_streaming` is the dedicated sibling lane for incremental live testing. It should be exposed beside the batch lane, not replace it.
- The provider runs outside `AetherVoice-X` in `qwen-experiments` and is reachable over the shared Docker network `aether-voice-mesh`.
- `ASR Live -> reply from final transcript` already works end to end against `qwen_customvoice`.
- `TTS Live` now exposes `qwen_customvoice` as a `batch-backed live` lane for voice and latency evaluation.
- The streaming lane should use the same operator page and the same seeded Qwen voices so batch vs live can be compared without relearning the tool.

## Provider Runtime

Provider repo:
- `/home/cory/Aether-Voice-Platform/qwen-experiments`

Provider container:
- `qwen-provider`

Provider endpoints:
- `GET /health`
- `GET /v1/models`
- `GET /v1/voices`
- `POST /v1/warmup`
- `POST /v1/audio/speech`
- `POST /v1/audio/speech/stream`
- `POST /v1/stream/start`
- `POST /v1/stream/{session_id}/text`
- `POST /v1/stream/{session_id}/complete`
- `POST /v1/stream/{session_id}/end`

Current provider truth:
- `qwen_customvoice` remains the stable batch contract
- `qwen_customvoice_streaming` owns incremental chunk delivery for live testing
- `AetherVoice-X` should treat these as two separate lanes on the same page

## Direct Provider Request

Use this if `Polymorph` or telephony wants to hit the provider directly instead of going through the main gateway.

Example:

```json
{
  "model": "qwen_customvoice",
  "input": "Thanks for calling Aether. How can I help you today?",
  "voice": "Serena",
  "response_format": "wav",
  "language": "English",
  "instructions": "Speak in a calm, telephony-friendly style.",
  "metadata": {
    "source": "polymorph",
    "lane": "telephony_probe"
  }
}
```

Response shape:

```json
{
  "model": "qwen_customvoice",
  "format": "wav",
  "sample_rate": 24000,
  "audio_b64": "...",
  "timings": {
    "inference_ms": 1234,
    "total_ms": 1456
  },
  "artifacts": {
    "runtime_path_used": "qwen_customvoice",
    "qwen_model_id": "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "qwen_voice": "Serena",
    "qwen_language": "English",
    "provider_public_base_url": "...",
    "supports_streaming_contract": false
  }
}
```

## Gateway Request

Use this if telephony wants the same path the app already uses.

Gateway endpoint:
- `POST /v1/tts/synthesize`

Example:

```json
{
  "model": "qwen_customvoice",
  "voice": "qwen_serena",
  "text": "Thanks for calling Aether. How can I help you today?",
  "format": "wav",
  "sample_rate": 24000,
  "stream": false,
  "style": {
    "speed": 1.0,
    "emotion": "calm",
    "speaker_hint": "Serena"
  },
  "metadata": {
    "source": "polymorph",
    "lane": "telephony_probe",
    "extra": {
      "qwen_instructions": "Speak in a calm, telephony-friendly style."
    }
  }
}
```

Why use the gateway path:
- same auth and quota surface as the rest of the platform
- same storage/artifact behavior
- same model alias normalization
- same studio voice-resolution behavior

## Live Testing In AetherVoice-X

`TTS Live` should now have two honest Qwen modes plus the existing Kokoro lane:

- `kokoro_realtime`
  Native websocket streaming lane
- `qwen_customvoice`
  Batch-backed live lane for quality and latency evaluation
- `qwen_customvoice_streaming`
  Incremental provider-driven live lane for first-chunk and chunk-cadence testing

Batch-backed live means:
- click `Arm batch lane`
- click `Generate audio`
- one finalized WAV returns
- total latency is shown in the operator surface
- chunk count is not a true streaming metric

This is the correct surface for comparing:
- voice quality
- total synthesis latency
- first-audio latency
- chunk cadence
- preset voice usefulness
- operator workflow

It is not yet the final proof for:
- websocket chunk cadence
- telephony-grade streaming interruption behavior
- first-audio chunk latency parity with Kokoro

## Telephony Recommendation

Use Qwen in telephony only in this order:

1. Direct harness probe through `Polymorph`
2. Measure:
   - request start
   - first audio available
   - total synthesis complete
   - audio duration
   - turn latency
3. Compare against `kokoro_realtime`
4. Promote only if Qwen wins enough quality to justify the latency tradeoff

## Repo Ownership

`qwen-experiments` owns:
- provider runtime behavior
- provider HTTP contract
- model loading, warmup, and chunking strategy
- direct runner experiments

`AetherVoice-X` owns:
- adapters and model aliasing
- gateway and studio contracts
- operator pages like `TTS Live`
- routing truth, voice registry, and product-facing UX

Rule:
- if the change is about how Qwen loads, chunks, streams, or exposes provider endpoints, change `qwen-experiments`
- if the change is about how the platform routes, displays, stores, or compares Qwen, change `AetherVoice-X`

## Known Limitations

- Qwen provider is currently batch only
- `flash_attn` is not installed in the provider container, so it falls back to `sdpa`
- warmup is recommended before serious latency testing
- `TTS Live` Qwen lane is for honest evaluation, not a claim of realtime websocket streaming

## Operator Commands

Watch provider only:

```bash
cd ~/aetherpro/voice-x/experiments/qwen-experiments
docker compose logs -f qwen-provider
```

Warm the provider:

```bash
curl -X POST http://127.0.0.1:8072/v1/warmup
```

Bring up only the provider:

```bash
cd ~/aetherpro/voice-x/experiments/qwen-experiments
docker compose up -d --build qwen-provider
```

Rebuild only TTS after backend adapter changes:

```bash
cd ~/aetherpro/voice-x/AetherVoice-X
docker compose up -d --build --no-deps tts
```

Rebuild only frontend after `TTS Live` changes:

```bash
cd ~/aetherpro/voice-x/AetherVoice-X
docker compose up -d --build --no-deps frontend
```

Bring up main stack with sidecar profiles when a wider pass is actually needed:

```bash
COMPOSE_PROFILES=voxtral,kokoro docker compose up -d --build
```
