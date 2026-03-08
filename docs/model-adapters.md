# Model Adapters

## Implemented

- `faster_whisper`: batch transcription and micro-batch streaming fallback
- `chatterbox`: HTTP passthrough TTS
- `voxtral_realtime`: upstream realtime ASR adapter
- `moss_realtime`: OpenMOSS sidecar-backed realtime TTS adapter
- `sentinel_scaffold`: rule-based triage classification

## Scaffolds

- `qwen3_asr`
- `phi_overlay`

Scaffolds deliberately return explicit "not implemented" style capabilities instead of pretending to run unavailable models.
