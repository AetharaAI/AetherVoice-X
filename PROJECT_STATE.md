# Project State

## GPU contract

- Chatterbox TTS is external to this stack and uses host GPU `3` opportunistically during generation.
- Host GPU `3` is currently treated as the shared studio/design lane for `moss_voice_generator` until Chatterbox is retired.
- Operational rule for now: do not rely on Chatterbox and `moss_voice_generator` concurrently.
- Voxtral Realtime is pinned to host GPU `2`.
- OpenMOSS realtime is pinned to host GPU `0`.
- `moss_tts` and `moss_ttsd` remain aligned to host GPU `0` unless explicitly re-planned.
- ASR stays off host GPU `3`; current pinned expectation is host GPU `1` for the in-stack ASR lane.
- Inside a container, `cuda:0` is still correct when only one host GPU is exposed through `NVIDIA_VISIBLE_DEVICES`.
- Current working studio exception: `moss_voice_generator` is stable on host GPU `3` and now boots, warms, and renders successfully through the UI.
- Long-term target: once OpenMOSS fully replaces Chatterbox, this app owns the full L40S-360 envelope and GPU `3` becomes a first-class unified stack lane.

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
- TTS Live conditioning contract: selected voice reference audio is now forwarded into `moss_realtime` at stream start, with `MOSS_PROMPT_AUDIO_PATH` kept only as the fallback prompt path.
- TTS Studio phase 1 scaffolding: additive studio backend and new top-level UI surface are now present without replacing the existing TTS Live lane.
- TTS Studio voice design preview: `moss_voice_generator` is now runtime-backed, warms successfully, and renders end-to-end through the browser.
- TTS Studio voice save path: when a Voice Design preview has been rendered, saving the design now persists the preview WAV into the registry record so `TTS Live` can switch realtime conditioning by preset instead of always falling back to the global prompt file.

## Platform execution lanes

### Lane 1: Realtime Agent Mode

- Pipeline: `ASR -> LLM -> realtime TTS`
- Primary product lane for telephony and live agent work.
- Current state: materially improved and stable enough to freeze.
- Realtime ASR is strong and should be treated as production-promising infrastructure.
- Realtime MOSS TTS is now transport-stable and tunable, but speaker identity is still the main blocker.

### Lane 2: Turn-Based Voice Mode

- Pipeline: `ASR -> LLM -> batch / turn-based TTS`
- This is the next implementation target.
- Goal: establish a known-good end-to-end conversational baseline with stronger voice fidelity, easier debugging, and cleaner operator truth.
- This lane should be completed before deeper realtime experimentation resumes.

### Lane 3: Assisted / Staged Streaming Mode

- Pipeline: `ASR -> LLM -> staged / chunked TTS playback`
- Future enhancement lane.
- Goal: create a perceived-realtime conversational experience without depending on strict realtime synthesis behavior.
- Useful for dispatch, intake, scheduling, and service workflows where slight latency is acceptable.

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
  - per-session reference audio now overrides the global prompt WAV when the selected voice has a usable registry asset
  - selected voice registry assets now reach realtime and show up in `Runtime conditioning`
  - longer prompt WAVs materially improve identity compared with very short references
  - current stable decode baseline is:
    - `prefill_text_len=24`
    - `decode_chunk_frames=6`
    - `decode_overlap_frames=0`
  - current stable prosody baseline is:
    - `temperature=0.45`
    - `top_p=0.65`
    - `top_k=30`
    - `repetition_penalty=1.1`
    - `repetition_window=50`
  - current limitation: `MOSS-TTS-Realtime` still tends to collapse toward a house voice / model prior instead of strongly locking speaker identity across presets
  - current limitation: synthetic preview WAVs are weaker conditioning sources than clean real human reference audio
  - current lifecycle truth: one utterance per stream; after `/complete`, another `/text` on the same stream returns `409 Conflict`
  - first-turn latency remains poor enough to be a telephony concern, while second-turn latency is materially better
  - current quality blocker is voice identity / conditioning strength rather than transport bring-up
  - current product blocker is not routing; it is whether realtime conditioning can become strong enough for production voice selection
- `tts_studio`
  - new additive nav item is wired directly under `TTS File`
  - backend voice registry now persists reusable preset, imported, generated, and cloned voice metadata
  - backend route catalog now advertises `moss_realtime`, `moss_tts`, `moss_ttsd`, `moss_voice_generator`, and `chatterbox`
  - provider-backed LLM routing config is now scaffolded for `OpenAI`, `OpenRouter`, `LiteLLM`, with `Anthropic` stubbed
  - provider model dropdowns are fetched live through backend `/models` calls with env-backed auth
  - `moss_voice_generator` is now runtime-backed and verified through curl plus the browser UI
  - current limitation: `moss_tts` and `moss_ttsd` still need the same runtime verification pass before they can be treated as production-ready studio routes

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
- The TTS Live page now exposes stream-start tuning knobs for immediate realtime quality tests without changing env defaults.
- Realtime voice truth has changed: selected voice reference audio should now materially override the global fallback prompt on stream start when that asset exists and can be serialized from the voice registry.
- Voice Design truth has changed: text-only generated presets are still metadata-only, but a rendered preview saved into the library now becomes a real reusable reference asset for later realtime conditioning.
- Realtime lane should currently be operated as:
  - start a stream
  - send one utterance
  - wait for completion
  - start a fresh stream for the next utterance
- Current default fallback prompt voice is controlled by `MOSS_PROMPT_AUDIO_PATH` in the active `.env`, not by UI metadata.
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

1. Freeze Realtime Agent Mode as a known-good-but-not-final lane and stop reopening solved routing / transport issues.
2. Move immediately to Turn-Based Voice Mode using realtime ASR as the input source and non-realtime TTS as the output lane.
3. Finish runtime adapters and production verification for `moss_tts` and `moss_ttsd` behind the TTS Studio route catalog.
4. Build the first clean `ASR -> LLM -> turn-based TTS` conversational loop before revisiting deeper realtime changes.
5. Validate provider-backed LLM model discovery against real `OpenAI`, `OpenRouter`, and internal `LiteLLM` endpoints.
6. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
7. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
8. Improve final transcript shaping for live ASR so the normalized transcript is operator-ready and final flush behavior is consistent.
9. Evaluate `MOSS-TTSD-v1.0` for studio dialogue generation and keep `moss_realtime` focused on low-latency agent turns only if warm-path latency stays acceptable.
10. If telephony latency remains too high after shaping fixes, switch the production realtime lane to a smaller model such as Kokoro and keep OpenMOSS in experimental status.
11. After Turn-Based Voice Mode is solid, revisit realtime identity using clean human reference WAVs rather than synthetic preview assets as the decisive test.
12. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Snapshot references

- Current OpenMOSS snapshot:
  [OpenMOSS-Realtime-State-Snapshot-2026-03-08.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/OpenMOSS-Realtime-State-Snapshot-2026-03-08.md)

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
