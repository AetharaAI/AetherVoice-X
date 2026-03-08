# Project State

## Current status

- Batch TTS: working end-to-end through the unified gateway.
- Batch ASR: working end-to-end through the unified gateway on GPU with `faster_whisper`.
- Sessions, metrics, and request tracing: working.
- External model resource visibility: working on the Models page.
- Live ASR: frontend, gateway, and internal websocket plumbing are working.
- Voxtral live lane: first integration pass is now wired behind an env-driven upstream configuration.
- Live ASR observability: improved, but the next verification point is explicit Voxtral sidecar bring-up plus confirmed websocket traffic and microphone capture in the browser.

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
  - not marked ready until `VOXTRAL_HTTP_BASE_URL` or `VOXTRAL_WS_BASE_URL` are configured
  - explicit selection should now fail loudly instead of silently falling back
  - compose/runtime was updated to the current vLLM container entrypoint pattern where the command begins with the model path instead of wrapping `vllm serve`
  - current blocker moved from model loading to the vLLM realtime websocket path; the image now includes a hotfix for the `scope["method"]` websocket crash seen on `vllm 0.17.0`
  - realtime auth is now explicitly wired for internal Docker traffic via `VOXTRAL_HTTP_BASE_URL`, `VOXTRAL_WS_BASE_URL`, and `VOXTRAL_API_KEY`
  - temporary local fallback sends `Authorization: Bearer EMPTY` when no explicit key is configured and the sidecar still expects auth
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
   - `VOXTRAL_HTTP_BASE_URL`
   - `VOXTRAL_WS_BASE_URL`
   - `VOXTRAL_REALTIME_MODEL_NAME`
   - `VOXTRAL_API_KEY` if required
   - `VOXTRAL_VLLM_WORKER_MULTIPROC_METHOD`
   - `VOXTRAL_VLLM_LOGGING_LEVEL`
   - `VOXTRAL_UVICORN_LOG_LEVEL`
2. Run live ASR timing checks from the UI and from `scripts/benchmark_live_asr.py`.
3. Record timing notes for:
   - first partial latency
   - final latency
   - partial event cadence
   - transcript stability under real speech
4. Verify the Voxtral websocket hotfix by confirming the sidecar no longer throws `KeyError: 'method'` during `/v1/realtime` handshake.
5. After Voxtral timings are stable, wire `moss_realtime` for live TTS.
6. When the unified stack is production-solid, flip the repo private before public cutover to `studio.aetherpro.us`.

## Suggested benchmark command

```bash
python3 scripts/benchmark_live_asr.py --file /path/to/test-16k-mono.wav --model voxtral_realtime --realtime
```

If `websockets` is not installed on the host, run it from an environment that has the script dependencies available.
