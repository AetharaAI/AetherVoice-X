# Model Adapters

## Implemented

- `faster_whisper`: batch transcription and micro-batch streaming fallback
- `chatterbox`: HTTP passthrough TTS
- `sentinel_scaffold`: rule-based triage classification

## Scaffolds

- `voxtral_realtime`
- `qwen3_asr`
- `moss_realtime`
- `phi_overlay`

Scaffolds deliberately return explicit "not implemented" style capabilities instead of pretending to run unavailable models.
