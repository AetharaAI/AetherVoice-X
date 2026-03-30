# Model Adapters

## Implemented

- `faster_whisper`: batch transcription and micro-batch streaming fallback
- `chatterbox`: HTTP passthrough TTS
- `voxtral_realtime`: upstream realtime ASR adapter
- `kokoro_realtime`: Kokoro sidecar-backed fast realtime TTS adapter
- `voxtream_realtime`: external provider realtime clone lane (reference-audio conditioned)
- `voxtream2_realtime`: external provider realtime clone lane with dynamic speaking-rate support
- `voxtral_tts`: external provider TTS lane (preset voices, batch + streaming)
- `qwen_customvoice`: external provider batch TTS lane
- `qwen_customvoice_streaming`: external provider incremental streaming lane
- `qwen_voice_design`: external provider prompt-driven voice-design lane
- `sentinel_scaffold`: rule-based triage classification

## Scaffolds

- `qwen3_asr`
- `phi_overlay`

Scaffolds deliberately return explicit "not implemented" style capabilities instead of pretending to run unavailable models.
