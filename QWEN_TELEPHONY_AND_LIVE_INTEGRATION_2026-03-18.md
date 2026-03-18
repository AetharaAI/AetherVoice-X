# Qwen Telephony And Live Integration

## Current Truth

- `qwen_customvoice` is operational as a modular provider-backed batch lane.
- The provider runs outside `AetherVoice-X` in `qwen-experiments` and is reachable over the shared Docker network `aether-voice-mesh`.
- `ASR Live -> reply from final transcript` already works end to end against `qwen_customvoice`.
- `TTS Live` now exposes `qwen_customvoice` as a `batch-backed live` lane for voice and latency evaluation.
- This is not websocket chunk streaming yet. It is one-shot finalized audio per send.

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

Current provider truth:
- `/v1/audio/speech/stream` returns `501`
- `supports_streaming_contract` is currently `false`

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

`TTS Live` now has two honest modes:

- `kokoro_realtime`
  Native websocket streaming lane
- `qwen_customvoice`
  Batch-backed live lane for quality and latency evaluation

Batch-backed live means:
- click `Arm batch lane`
- click `Generate audio`
- one finalized WAV returns
- total latency is shown in the operator surface
- chunk count is not a true streaming metric

This is the correct surface for comparing:
- voice quality
- total synthesis latency
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

Bring up main stack with sidecar profiles:

```bash
COMPOSE_PROFILES=voxtral,kokoro docker compose up -d --build
```
