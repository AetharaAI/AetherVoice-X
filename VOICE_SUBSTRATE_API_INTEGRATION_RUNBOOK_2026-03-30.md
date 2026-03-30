# Voice Substrate API Integration Runbook

Date: 2026-03-30

## Purpose

Use this runbook to integrate external apps/harnesses with the current Aether Voice substrate using the stable gateway contract.

This pass captures the now-verified `voxtral_tts` provider lane (including preset voices and live stream flow in `TTS Live`) while preserving the frozen baseline (`voxtral_realtime` ASR + `kokoro_realtime` TTS).

## Canonical Endpoints

- HTTP base: `https://asr.aetherpro.us/api`
- WebSocket base: `wss://asr.aetherpro.us`

Use gateway endpoints for product integration. Do not couple external apps directly to internal containers unless explicitly running a debug harness.

## Primary Realtime Routes (Current)

- ASR realtime: `voxtral_realtime`
- TTS realtime baseline: `kokoro_realtime`
- TTS realtime/provider lane: `voxtral_tts`
- TTS experimental realtime clone lanes: `voxtream_realtime`, `voxtream2_realtime`

## Gateway Integration Contract

### 1) Start TTS stream

`POST /v1/tts/stream/start`

Example (`voxtral_tts`):

```json
{
  "model": "voxtral_tts",
  "voice": "voxtral_casual_female",
  "sample_rate": 24000,
  "format": "wav",
  "context_mode": "conversation",
  "metadata": {
    "source": "harness",
    "extra": {
      "lane": "tts_live",
      "realtime_profile": {
        "voice_preset_id": "voxtral_casual_female",
        "session_profile": "telephony",
        "tone": "warm",
        "cadence": "telephony",
        "speaking_style": "service",
        "latency_mode": "low_latency"
      }
    }
  }
}
```

Response includes:
- `session_id`
- `ws_url` (connect on `wss://asr.aetherpro.us`)
- `model_requested`
- `model_used`
- `runtime` (runtime truth block)

### 2) Stream websocket flow

Connect:
- `wss://asr.aetherpro.us/api/v1/tts/stream/{session_id}`

Send:

```json
{ "type": "text_chunk", "text": "A technician is being dispatched to your location now." }
```

```json
{ "type": "text_complete" }
```

```json
{ "type": "end_stream" }
```

Receive:
- `audio_chunk`
- `final_audio`
- runtime metadata in event `metadata.runtime`

### 3) Batch synth fallback/check

`POST /v1/tts/synthesize`

```json
{
  "model": "voxtral_tts",
  "voice": "casual_female",
  "text": "Voxtral TTS end-to-end test.",
  "format": "wav",
  "sample_rate": 24000,
  "stream": false
}
```

## Voice Selection Rule

Load voices from:
- `GET /v1/tts/studio/voices`

Then filter by `runtime_target`:
- `kokoro_realtime` -> Kokoro presets
- `voxtral_tts` -> Voxtral provider presets
- `voxtream2_realtime` -> imported reference-audio voices
- `qwen_customvoice*` -> Qwen presets

Do not hardcode provider `/v1/audio/voices` in product clients.

## Voxtral TTS Voice IDs

`voxtral_tts` now supports provider preset voices and model-aware voice resolution.

Accepted forms:
- Studio voice IDs (example: `voxtral_casual_female`)
- Raw provider voice name (example: `casual_female`)

## Warmup

For Voxtream routes:
- `POST /v1/tts/studio/routes/{route_name}/warmup`

For `voxtral_tts`, normal first request already exercises provider readiness; explicit warmup endpoint is not required for product integration.

## Harness Handoff Checklist

1. Use gateway base URLs only.
2. Start TTS with explicit `model` + `voice`.
3. Connect websocket from returned `ws_url`.
4. Send `text_chunk`, then `text_complete`, then `end_stream`.
5. Persist `session_id`, `request_id`, `runtime_path_used`, and `audio_url`.
6. Treat `runtime.model_used` as final route truth.

## Quick Smoke Commands

```bash
curl -sS -X POST "https://asr.aetherpro.us/api/v1/tts/synthesize" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -d '{
    "model":"voxtral_tts",
    "voice":"casual_female",
    "text":"Voxtral TTS smoke test",
    "format":"wav",
    "sample_rate":24000,
    "stream":false
  }' | jq
```

```bash
curl -sS "https://asr.aetherpro.us/api/v1/tts/studio/voices" \
  -H "X-Tenant-Id: default" | jq '.voices[] | select(.runtime_target=="voxtral_tts") | .voice_id'
```

## Notes

- `studio.aetherpro.us` remains the planned public-facing lane.
- `asr.aetherpro.us` remains the current internal speech infrastructure + integration surface.
- Promotion decisions remain runtime-proof based, not model-card based.
