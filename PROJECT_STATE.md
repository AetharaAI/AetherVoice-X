# Project State

## Current status

- Batch TTS: working end-to-end through the unified gateway.
- Batch ASR: working end-to-end through the unified gateway on GPU with `faster_whisper`.
- Sessions, metrics, and request tracing: working.
- External model resource visibility: working on the Models page.
- Live ASR: frontend, gateway, and internal websocket plumbing are working.
- Voxtral live lane: first integration pass is now wired behind an env-driven upstream configuration.
- Live ASR observability: improved, and the browser stream is now reaching Voxtral with partials visible in the console and in the operator UI.
- Live TTS backend: OpenMOSS sidecar adapter path is now wired behind the existing `/v1/tts/stream/*` contract, with unit coverage for adapter-driven streaming and chatterbox fallback.
- Live TTS operator console: chunk playback, final WAV playback, explicit download controls, and stream-state feedback are now visible in the browser.
- TTS Live contract fix: operator-side structured controls no longer need to be prepended into spoken text, and the existing live playback contract remains intact.
- TTS Studio phase 1 scaffolding: additive studio backend and new top-level UI surface are now present without replacing the existing TTS Live lane.

## Stable lanes

- `faster_whisper`
  - batch ASR: working
  - live ASR fallback: working via micro-batch streaming
- `chatterbox`
  - batch TTS: working via HTTP passthrough
  - current fallback lane for batch generation inside the new studio shell: working

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
  - adapter-driven realtime path implemented
  - dedicated `moss` compose sidecar added behind `--profile moss`
  - TTS service now prefers true adapter lifecycle over fake chunked batch synth when the sidecar is available
  - fallback to chatterbox micro-batching remains in place when the sidecar is unavailable
  - sidecar build, boot, chunk streaming, and final WAV assembly are now working
  - first-turn latency remains poor enough to be a telephony concern, while second-turn latency is materially better
  - current quality blocker is prompt/alignment behavior rather than transport bring-up
  - current product blocker is voice catalog and conditioning readiness for a public-facing studio
- `tts_studio`
  - new additive nav item is wired directly under `TTS File`
  - backend voice registry now persists reusable preset, imported, generated, and cloned voice metadata
  - backend route catalog now advertises `moss_realtime`, `moss_tts`, `moss_ttsd`, `moss_voice_generator`, and `chatterbox`
  - provider-backed LLM routing config is now scaffolded for `OpenAI`, `OpenRouter`, `LiteLLM`, with `Anthropic` stubbed
  - provider model dropdowns are fetched live through backend `/models` calls with env-backed auth
  - current limitation: only `moss_realtime` and `chatterbox` are runtime-backed in the service layer today

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
- The TTS Live page now treats session profile, tone, cadence, style, and latency profile as console-side structured state rather than spoken markup.
- The new TTS Studio page now exposes:
  - Voice Library
  - Voice Clone
  - Voice Design
  - Batch Narration
  - Dialogue Studio
  - LLM Routing
  - Advanced
  - consistent bottom output panel with waveform, playback, download, route used, voice used, generation time, and duration

## Immediate next steps

1. Finish runtime adapters for `moss_tts`, `moss_ttsd`, and `moss_voice_generator` behind the new TTS Studio route catalog.
2. Add per-voice asset promotion flows so imported and generated voices can be bound cleanly into OpenMOSS runtime requests.
3. Rework `moss_realtime` turn construction so operator metadata remains structured state and does not leak into spoken output.
4. Validate provider-backed LLM model discovery against real `OpenAI`, `OpenRouter`, and internal `LiteLLM` endpoints.
5. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
6. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
7. Improve final transcript shaping for live ASR so the normalized transcript is operator-ready and final flush behavior is consistent.
8. Evaluate `MOSS-TTSD-v1.0` for studio dialogue generation and keep `moss_realtime` focused on low-latency agent turns only if warm-path latency stays acceptable.
9. If telephony latency remains too high after shaping fixes, switch the production realtime lane to a smaller model such as Kokoro and keep OpenMOSS in experimental status.
10. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Snapshot references

- Current OpenMOSS snapshot:
  [OpenMOSS-Realtime-State-Snapshot-2026-03-08.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/OpenMOSS-Realtime-State-Snapshot-2026-03-08.md)

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
