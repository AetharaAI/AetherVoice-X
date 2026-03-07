# Changelog

## 2026-03-07

- Stabilized the GPU batch ASR lane:
  - fixed gateway multipart forwarding to the ASR worker
  - fixed missing ASR runtime dependencies for `faster-whisper`
  - fixed NVIDIA/CUDA device exposure so `ctranslate2` can see the assigned GPU
- Verified end-to-end batch TTS through the unified gateway and Chatterbox upstream.
- Verified end-to-end batch ASR through the unified gateway and `faster_whisper` on GPU.
- Added external model resource cards to the Models page using `VITE_EXTERNAL_MODELS_JSON`.
- Split infrastructure topology docs into:
  - `AETHERPRO_INFRA_TOPOLOGY.md` (public-safe)
  - `AETHERPRO_INFRA_TOPOLOGY_SENSITIVE.md` (internal-only)
- Added the first Voxtral live ASR integration pass:
  - env-driven upstream adapter via OpenAI-compatible `/v1/audio/transcriptions`
  - micro-batch live partial generation over the existing websocket contract
  - live ASR model selector and browser-side timing visibility
  - benchmark helper script for live ASR websocket timing

