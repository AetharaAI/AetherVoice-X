# Project State

## Current status

- Batch TTS: working end-to-end through the unified gateway.
- Batch ASR: working end-to-end through the unified gateway on GPU with `faster_whisper`.
- Sessions, metrics, and request tracing: working.
- External model resource visibility: working on the Models page.
- Live ASR: frontend, gateway, and internal websocket plumbing are working.
- Voxtral live lane: first integration pass is now wired behind an env-driven upstream configuration.

## Stable lanes

- `faster_whisper`
  - batch ASR: working
  - live ASR fallback: working via micro-batch streaming
- `chatterbox`
  - batch TTS: working via HTTP passthrough

## In-progress lanes

- `voxtral_realtime`
  - implemented as an upstream-backed adapter
  - uses OpenAI-compatible audio transcription requests for low-latency partial refreshes
  - not marked ready until `VOXTRAL_REALTIME_BASE_URL` is configured
- `moss_realtime`
  - still scaffolded

## Operator notes

- The current live ASR page now exposes:
  - selected realtime model
  - session ID
  - partial count
  - frames sent
  - browser-measured time to first partial
  - browser-measured time to final transcript
- The file ASR page now supports explicit model selection for comparison runs.

## Immediate next steps

1. Stand up or point to a Voxtral upstream and set:
   - `VOXTRAL_REALTIME_BASE_URL`
   - `VOXTRAL_REALTIME_MODEL_NAME`
   - `VOXTRAL_REALTIME_API_KEY` if required
2. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
3. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
4. After Voxtral timings are stable, wire `moss_realtime` for live TTS.
5. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
