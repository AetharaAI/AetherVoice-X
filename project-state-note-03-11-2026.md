
## Realtime MOSS Status - March 11, 2026

What is working:
- `moss_realtime` now boots cleanly and serves on `:8021`
- `moss-voice-generator` boots cleanly and serves on `:8024`
- resident stack layout is stable enough for testing:
  - GPU 0: `moss_realtime`
  - GPU 2: `voxtral`
  - GPU 3: `moss-voice-generator`
- realtime decode baseline is stable:
  - `prefill_text_len=24`
  - `decode_chunk_frames=6`
  - `decode_overlap_frames=0`
- good live prosody baseline:
  - `temperature=0.45`
  - `top_p=0.65`
  - `top_k=30`
  - `repetition_penalty=1.1`
  - `repetition_window=50`
- default fallback prompt path can be changed through `MOSS_PROMPT_AUDIO_PATH`
- longer conditioning clips materially improve speaker identity versus very short clips
- selected preset assets now reach realtime and appear in `Runtime conditioning`

What is partially working:
- realtime voice identity is better than before, but still not reliably locked
- a longer male conditioning clip got much closer to the intended voice
- prosody is far more stable than before, but still model-dependent

What is not solved:
- preset switching does not yet guarantee a materially different audible identity every time
- `moss_realtime` still tends to collapse toward a house voice / speaker prior
- synthetic preview WAVs are weaker conditioning sources than real human reference audio
- stream lifecycle is one-turn-per-stream right now
  - after `/complete`, another `/text` on the same stream returns `409 Conflict`

Operational truth:
- current realtime lane should be treated as:
  - one stream
  - one utterance
  - then start a new stream
- do not judge speaker identity from very short or synthetic references alone
- next decisive test should use a clean real human reference WAV
