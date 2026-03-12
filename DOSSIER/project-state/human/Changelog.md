# Changelog

## 2026-03-09
- Replaced the failed direct Phi-4 voice path with a split PolyMorph voice lane.
- Added a dedicated frontend `PolyMorph Voice Mode` pane backed by `qwen3.5-4b`.
- Kept the mic button on batch WAV ASR transcription into the main composer.
- Added backend voice routes for qwen4b text responses and TTS audio file playback.
- Updated ASR health/transcription probing to prefer the current `/v1/asr/*` gateway contract.

## 2026-03-06
- Added Project State package for explicit human-readable and machine-readable repo state.
- Added reusable bootstrap rule templates for AGENTS/Memory/provider-specific assistant docs.
- Documented current direct OpenAI GPT-5 compatibility constraints.

## 2026-03-05
- Hardened direct OpenAI GPT-5 request compatibility in the harness provider layer.
- Added recent search/profit/campaign tooling and documentation updates.
