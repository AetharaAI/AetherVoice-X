# Project State

## Current status

- Batch TTS: working end-to-end through the unified gateway.
- Batch ASR: working end-to-end through the unified gateway on GPU with `faster_whisper`.
- Sessions, metrics, and request tracing: working.
- External model resource visibility: working on the Models page.
- Live ASR: frontend, gateway, and internal websocket plumbing are working.
- Voxtral live lane: first integration pass is now wired behind an env-driven upstream configuration.
- Live ASR observability: improved, and the browser stream is now reaching Voxtral with partials visible in the console and in the operator UI.

## Stable lanes

- `faster_whisper`
  - batch ASR: working
  - live ASR fallback: working via micro-batch streaming
- `chatterbox`
  - batch TTS: working via HTTP passthrough

## In-progress lanes

- `voxtral_realtime`
  - implemented as an upstream-backed adapter
  - now targets a vLLM realtime websocket upstream when configured
  - sidecar model load on GPU is verified
  - realtime websocket handshake is working through the gateway
  - partial transcripts are visible in the browser
  - disconnect now finalizes the stream instead of immediately tearing down the browser socket
  - duplicate cumulative partial rendering has been removed at the UI layer in favor of one evolving transcript card
  - the last live transcript snapshot now persists across page navigation in the browser session
  - current polishing target is structured final transcript quality and realtime output normalization
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
  - final segment rendering when the stream flushes a final result
  - quick-copy and transcript download actions
- The file ASR page now supports explicit model selection for comparison runs.

## Immediate next steps

1. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
2. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
3. Improve final transcript shaping for live ASR so the normalized transcript is operator-ready and final flush behavior is consistent.
4. Add the same copy/download affordances to other text and audio result panes across the console.
5. After Voxtral timings are stable, wire `moss_realtime` for live TTS.
6. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
