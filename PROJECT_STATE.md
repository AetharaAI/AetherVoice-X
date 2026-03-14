# Project State

## GPU contract

- Kokoro realtime TTS is pinned to host GPU `3`.
- Host GPU `3` is now the fast live-agent reply lane for `kokoro`.
- `moss_voice_generator` still shares host GPU `3` opportunistically for studio/design work.
- Chatterbox TTS is external to this stack and may also consume host GPU `3` opportunistically during generation.
- Operational rule for now: do not rely on `kokoro`, `moss_voice_generator`, and Chatterbox concurrently under tight latency or memory expectations.
- Voxtral Realtime is pinned to host GPU `2`.
- OpenMOSS realtime is pinned to host GPU `0`.
- `moss_tts` and `moss_ttsd` remain aligned to host GPU `0` unless explicitly re-planned.
- ASR stays off host GPU `3`; current pinned expectation is host GPU `1` for the in-stack ASR lane.
- Inside a container, `cuda:0` is still correct when only one host GPU is exposed through `NVIDIA_VISIBLE_DEVICES`.
- Current working studio exception: `moss_voice_generator` is stable on host GPU `3` and now boots, warms, and renders successfully through the UI when the live Kokoro lane is not being stressed.
- Long-term target: keep GPU `3` as the first-class low-latency TTS lane while the rest of the voice stack settles around it.

## Current status

- Batch TTS: working end-to-end through the unified gateway.
- Batch ASR: working end-to-end through the unified gateway on GPU with `faster_whisper`.
- Sessions, metrics, and request tracing: working.
- External model resource visibility: working on the Models page.
- Live ASR: frontend, gateway, and internal websocket plumbing are working.
- Voxtral live lane: stable, operator-verified, and actively used from the browser as the default realtime ASR surface.
- Live ASR observability: improved, and the browser stream is reaching Voxtral with partials and finals visible in both the console and the operator UI.
- Live TTS backend: sidecar-backed streaming TTS is wired behind the existing `/v1/tts/stream/*` contract. Kokoro is now the preferred fast/default live lane, with OpenMOSS retained for specialized R&D and studio follow-up.
- Live TTS operator verification: Kokoro succeeded on the first operator run with the `Sky` preset, produced smooth low-latency audio, and completed the full `start -> text -> complete -> final audio` path through the current UI and gateway contract on `2026-03-14`.
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
- Current state: materially improved and stable enough to freeze at the transport/routing layer.
- Realtime ASR is strong and should be treated as production-promising infrastructure.
- Realtime Kokoro TTS is now the default voice-response lane and has been operator-verified as the first real low-latency voice that feels deployment-worthy.
- Realtime MOSS TTS remains transport-stable and useful for experimentation, but is no longer the default live reply lane.

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
- `voxtral_realtime`
  - upstream-backed realtime ASR lane is stable enough to freeze
  - browser, gateway, and upstream websocket contract are all working
  - operator is actively using this lane for day-to-day speech input
- `kokoro_realtime`
  - adapter-driven realtime TTS lane is now the default live reply path
  - dedicated `kokoro` sidecar is healthy and integrated behind the existing `/v1/tts/stream/*` contract
  - preset-voice route has been verified in the UI with clean runtime truth and low-latency chunk return
- `chatterbox`
  - batch TTS: working via HTTP passthrough
  - current fallback lane for batch generation inside the new studio shell: working

## In-progress lanes

- `moss_realtime`
  - adapter-driven realtime path implemented
  - dedicated `moss` compose sidecar added behind `--profile moss`
  - TTS service preserves true adapter lifecycle when this sidecar is selected
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
  - backend route catalog now advertises `kokoro_realtime`, `moss_realtime`, `moss_tts`, `moss_ttsd`, `moss_voice_generator`, and `chatterbox`
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
- The TTS Live page now defaults to `kokoro_realtime` and exposes preset Kokoro voices directly through the shared voice registry.
- Realtime voice truth has changed: selected voice reference audio should now materially override the global fallback prompt on stream start when that asset exists and can be serialized from the voice registry.
- Realtime voice truth also now has a second branch: when `runtime_path_used=kokoro_realtime`, preset voice identity is the runtime truth and no reference-audio conditioning is required.
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

1. Freeze the current `Voxtral ASR + Kokoro TTS` realtime lane as the new known-good operator baseline.
2. Write the clean API handoff for external VoiceOps / telephony clients against the existing ASR and TTS public contracts.
3. Build the first clean `ASR -> LLM -> turn-based TTS` conversational loop before reopening deeper TTS experimentation.
4. Finish runtime adapters and production verification for `moss_tts` and `moss_ttsd` behind the TTS Studio route catalog.
5. Validate provider-backed LLM model discovery against real `OpenAI`, `OpenRouter`, and internal `LiteLLM` endpoints.
6. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
7. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
8. Improve final transcript shaping for live ASR so the normalized transcript is operator-ready and final flush behavior is consistent.
9. Keep `moss_realtime` in experimental status while evaluating whether it belongs in dialogue/studio workflows instead of the default telephony lane.
10. After Turn-Based Voice Mode is solid, revisit realtime identity using clean human reference WAVs rather than synthetic preview assets as the decisive test for MOSS-family conditioning.
11. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Snapshot references

- Current stable realtime snapshot:
  [REALTIME_STACK_SNAPSHOT_2026-03-14.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/REALTIME_STACK_SNAPSHOT_2026-03-14.md)
- Current OpenMOSS snapshot:
  [OpenMOSS-Realtime-State-Snapshot-2026-03-08.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/OpenMOSS-Realtime-State-Snapshot-2026-03-08.md)

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
