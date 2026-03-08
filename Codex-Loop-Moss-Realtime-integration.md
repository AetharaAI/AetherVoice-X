
I’ve confirmed there’s already a moss_realtime scaffold in the TTS service and a thin TTS Live frontend. I’m reading that path now so I can turn it into a real upstream lane instead of bolting on a new parallel implementation.

Explored 4 files
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
Read TTSLive.tsx
The current TTS Live path is still a stub: it micro-batches text into the existing synthesis service and immediately closes the socket on stop. I’m reading the settings/model registry and your local model-card/runtime docs next so I can replace that with a real MOSS upstream lane.

Explored 2 files, 2 searches, 1 list
Read settings.py
Read model_registry.py
Searched for model*card* in .
Listed files in .
Searched for phi4|qwen3\.5|moss|openmoss|voxtral|runner|run-model|docker-compose
Context automatically compacted
I’m reviewing the current TTS Live path, the local modelcards docs, and your runner templates first so I can wire OpenMOSS without touching the ASR path that’s already working.

Explored 1 search, 1 list
Background terminal finished with git status --short


I’ve confirmed the current TTS live path is still mostly scaffold code. I’m pulling the local OpenMOSS docs and any runner examples next so I can wire the sidecar/runtime the same way Voxtral was wired.

Explored 4 files, 2 lists
The ASR live path is in the right place now. I’m switching to OpenMOSS by reading the local model card and the current upstream docs/endpoints first, then I’ll patch the live TTS lane without disturbing the working ASR flow.

Explored 5 files, 1 list
Searched web for OpenMOSS Team MOSS-TTS-Realtime documentation websocket realtime endpoint site:github.com OpenMOSS-Team MOSS-TTS-Realtime
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for site:github.com/OpenMOSS/MOSS-TTS moss_tts_realtime_model_card.md realtime websocket
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
I’ve confirmed two things from the upstream docs: OpenMOSS realtime is a true incremental push_text / end_text / drain flow, and it doesn’t look like the right first move is another vLLM websocket proxy. I’m inspecting the current TTS plumbing now so I can add a dedicated MOSS runtime sidecar and keep the existing live UI contract stable.

Explored 4 files, 2 searches, 2 lists
Read base.py
Read model_registry.py
Read synthesis_service.py
Read settings.py
Listed files in model-runners
Searched for moss|openmoss|tts
Listed files in modelcards
Searched for moss|openmoss|tts|audio
Context automatically compacted
I’m moving from the working ASR live path into the TTS live lane now. I’m confirming the current OpenMOSS runtime contract against the upstream docs and then I’ll patch the existing TTS stream service/adapters in the smallest way that preserves the working UI flow.

Searched web for OpenMOSS-Team MOSS-TTS-Realtime GitHub realtime push_text end_text drain documentation
ASR live is in the right place now. I’m patching the TTS live lane against the current OpenMOSS runtime contract and keeping the existing frontend flow stable so we don’t disturb what’s already working.

Explored 4 files
Read moss_realtime.py
Read streaming_service.py
Read stream.py
Read useTTSStream.ts
Searched web for OpenMOSS-Team MOSS-TTS-Realtime GitHub realtime push_text end_text docs
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
I’m into the TTS side now. The ASR live lane is stable enough, so I’m wiring OpenMOSS as a real internal runtime instead of trying to fake streaming through the existing batch synth path.

Explored 4 files, 1 search
Searched for tts/stream|startTTSStream|moss_realtime|stream/start|websocket in gateway
Read tts.py
Read tts_client.py
Read model_registry.py
Read settings.py
Context automatically compacted
ASR live is where it needs to be. I’m checking the local model card/docs you just added and the current OpenMOSS upstream contract, then I’ll wire the TTS live lane without disturbing the working ASR path.

Explored 2 searches, 2 lists
Listed files in .
Searched for model cards|model_cards|MOSS|OpenMOSS|moss
Listed files
Searched for moss_realtime|TTS Live|useTTSStream|stream/start|final_audio|text_chunk|end_stream|chatterbox in tts
I’m using the current working ASR live flow as the pattern and treating the TTS live work as an isolated lane. I’m reading your new runtime/UI notes plus the current TTS stream implementation so I can replace the scaffold without touching the ASR path.

Explored 10 files
Read Enhancement-List-GPT-5.4-After-1st-asr-success.md
Read ASR-Realtime-1st-UI-Clean-Response-03-07-2026.md
Read Voxstral-Runtime-logs-1st-Clean-Streaming-Generation.md
Read moss_realtime.py
Read streaming_service.py
Read stream.py
Read useTTSStream.ts
Read TTSLive.tsx
Read tts.py
Read settings.py
Context automatically compacted
I’m treating the working ASR live lane as locked and isolating TTS live behind the existing websocket contract. I’m reading the current TTS adapter, stream service, and the local model-card/runtime notes so I can replace the moss_realtime scaffold without perturbing ASR.

Explored 4 files, 1 search
Searched for moss|TTSLive|useTTSStream|stream/start|internal/stream|moss_realtime in services
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
Read TTSLive.tsx
Context automatically compacted
I’m treating the working ASR live lane as locked and isolating TTS live behind the existing websocket contract. I’m reading the current TTS adapter, stream service, and the local model-card/runtime notes so I can replace the moss_realtime scaffold without perturbing ASR.

Explored 4 files, 2 searches, 1 list
Searched for moss|OpenMOSS|MOSS|tts/stream|TTSLive|useTTSStream|streaming_service in .
Listed files in .
Searched for Enhancements-List-GPT5\.4|Enhancement|model card|model-cards|MOSS|OpenMOSS|moss
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
Read TTSLive.tsx
ASR live is locked in. I’m switching to MOSS now, and I’m checking the current OpenMOSS/vLLM integration surface first so I don’t wire this against stale API assumptions.

Searched web for OpenMOSS-Team MOSS-TTS-Realtime Hugging Face realtime API model card
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for OpenMOSS MOSS-TTS-Realtime websocket realtime API docs github
I have enough to start wiring it. I’m reading the local enhancement note and the current TTS gateway/router/schemas now so I can keep the existing public contract and swap the backend from fake chunked synthesis to real adapter-driven streaming.

Explored 8 files
Read Enhancement-List-GPT-5.4-After-1st-asr-success.md
Read stream.py
Read requests.py
Read responses.py
Read tts_client.py
Read settings.py
Read tts.py
Read docker-compose.yml
Context automatically compacted
I’m keeping ASR live untouched and mapping the current TTS path before I wire MOSS into it. First step is reading the existing TTS adapter, streaming service, and any local MOSS runner/model-card material so I can replace the fake chunk synthesis path without breaking the public contract.

Explored 3 files, 1 search
Searched for moss|OpenMOSS|MOSS in .
Read moss_realtime.py
Read streaming_service.py
Read settings.py
ASR live is in the polishing phase now, so I’m moving to the TTS live lane without touching that contract. I’m checking whether you already dropped local MOSS runner/model-card material into the repo, and if not I’ll confirm the current OpenMOSS/vLLM runtime shape from primary sources before I wire the adapter.

Explored 3 files, 2 searches, 1 list
Listed files
Searched for (^|/)(model-cards|model_cards|model-runners|model_runners|MOSS|moss)
Searched for *moss* in .
Read stream.py
Read useTTSStream.ts
Read TTSLive.tsx
I’ve confirmed the current TTS live path is still the old fake chunk synthesizer, so MOSS needs both a real adapter and a small streaming-service refactor. Next I’m checking your working runner templates plus the current OpenMOSS/vLLM docs so I can wire the sidecar with the right command shape and keep the existing /v1/tts/stream/* contract intact.

Explored 6 files
Read docker-compose.yml
Read docker-compose.yml
Read Dockerfile.phi4
Read Dockerfile.qwen35
Read synthesis_service.py
Read model_registry.py
Searched web for OpenMOSS Team MOSS-TTS-Realtime Hugging Face websocket realtime docs vllm March 2026
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
I’ve got the shape now: MOSS isn’t just a missing adapter, the current live TTS service still does per-chunk batch synth under the hood. I’m reading the TTS schemas/base classes and then I’m going to patch in a real MOSS sidecar + adapter lifecycle while leaving the gateway/websocket surface the same, so TTS Live becomes the TTS analog of what we just got working for ASR Live.

Explored 9 files
Read base.py
Read requests.py
Read responses.py
Read tts_client.py
Read tts.py
Read tts.ts
Read client.ts
Read docker-compose.yml
Read .env.example
Context automatically compacted
ASR live is in a good state, so I’m keeping that contract intact and wiring a real MOSS live lane underneath the existing TTS stream surface. First I’m checking the current TTS streaming path and the runtime shape for OpenMOSS so I can patch the backend without regressing the working ASR flow.

Explored 4 files
Searched web for OpenMOSS MOSS-TTS-Realtime Hugging Face realtime API websocket official
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime/blob/main/streaming_mossttsrealtime.py
ASR live is where it needs to be, so I’m leaving that surface alone and replacing the fake TTS stream backend with a real MOSS session lifecycle. I’m reading the current TTS hook/router/schema path and the OpenMOSS runtime entry points so I can wire the sidecar without breaking the working gateway/websocket contract.

Explored 6 files
Read useTTSStream.ts
Read TTSLive.tsx
Read tts.ts
Read requests.py
Read base.py
Read responses.py
Context automatically compacted
I’m preserving the working ASR live path and focusing only on the TTS live lane now. First I’m checking the current OpenMOSS runtime/API shape and comparing it to the existing TTS streaming service so I can wire it in without breaking the gateway/frontend contract.

Searched web for OpenMOSS Team MOSS-TTS-Realtime Hugging Face realtime api websocket docs
Searched web for OpenMOSS MOSS-TTS GitHub realtime README
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
I’m treating ASR live as stable now and leaving that path alone. Next I’m wiring the real OpenMOSS TTS live lane against the existing gateway/frontend contract, using your working runner templates as the reference for the runtime shape.

Explored 2 files, 2 searches, 1 list
Listed files in model-runners
Searched for docker-compose|Dockerfile|README|run-model
Searched for moss|MOSS|tts live|stream/start|MossRealtime|moss_realtime in services
Read moss_realtime.py
Read streaming_service.py
Context automatically compacted
You want the next move to be OpenMOSS realtime TTS without destabilizing the live ASR lane, so I’m checking the current TTS scaffolding and your model-runner templates first to match the runtime shape you already use.

Explored 4 files, 1 search
Read docker-compose.yml
Searched for moss|MOSS|stream in tts
Read docker-compose.yml
Read moss_realtime.py
Read streaming_service.py
ASR live is in the right place now. I’m going to wire the TTS live lane the same way: check your local runner/docs first, then verify the current OpenMOSS runtime/API against official sources before patching the scaffold.

Explored 5 files, 1 search, 1 list
Searched web for OpenMOSS-Team MOSS-TTS-Realtime Hugging Face realtime websocket API docs
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
The next patch is going to stay narrow: keep the current /v1/tts/stream/* contract and swap the fake chunked path behind it for a real MOSS sidecar/client path. I’m checking the shared settings and the current TTS gateway contract now so I can wire it without blowing up the UI we already have.

Explored 6 files
Read settings.py
Read config.py
Read tts.py
Read tts_client.py
Read base.py
Read stream.py
Context automatically compacted
I’m reading the current TTS live path and the local runner templates first, then I’m going to wire OpenMOSS in behind the existing contract instead of redesigning the whole stack.

Explored 3 files, 1 search, 1 list
Listed files
Searched for Enhancements-List-GPT5\.4|OpenMOSS|MOSS|moss|model-runners|run-model|model cards|MODEL_CARDS|model_cards
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
I’ve confirmed the current TTS live path is still the old micro-batch loop, so the next step is wiring OpenMOSS behind that existing contract instead of replacing the UI. I’m pulling the current OpenMOSS docs and checking the repo’s TTS settings/model registry now.

Searched web for OpenMOSS MOSS TTS Realtime Hugging Face docs websocket API March 2026
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
I’ve got enough context now: the cleanest path is a dedicated OpenMOSS sidecar plus a real streaming adapter in the existing TTS service, keeping the current gateway/frontend contract stable. I’m patching the model/env plumbing first, then I’ll switch the live TTS service from fake micro-batch to true adapter-driven streaming without touching the working ASR path.

Explored 8 files
Read model_registry.py
Read settings.py
Read stream.py
Read tts.py
Read TTSLive.tsx
Read tts_client.py
Read responses.py
Read requests.py
Context automatically compacted
ASR live is in the right place now. I’m reading the current TTS live path, your new root docs/files, and the OpenMOSS integration surface so I can wire the real realtime lane without disturbing the working ASR contract.

Explored 4 files, 1 search, 1 list
Searched web for OpenMOSS Team MOSS-TTS-Realtime vllm realtime API docs Hugging Face March 2026
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
I’ve confirmed the current TTS live lane is still fake micro-batching, while OpenMOSS is a real streaming target. I’m reading the OpenMOSS surface and the current TTS service contract now so I can swap in adapter-driven live streaming without breaking Chatterbox or the existing gateway/frontend routes.

Explored 7 files
Read settings.py
Read model_registry.py
Read stream.py
Read tts.py
Read tts_client.py
Read requests.py
Read responses.py
Context automatically compacted
I’m reading the current TTS live path and the OpenMOSS/model-runner material first so I can wire the realtime lane without destabilizing the working ASR flow.

Explored 3 files, 1 search, 1 list
Listed files
Searched for model-runners|model cards|model_cards|OpenMOSS|MOSS|moss|TTSLive|useTTSStream|services/tts|docker-compose.yml|README.md|CHANGELOG.md|PROJECT_STATE.md
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
I’ve confirmed the current TTS live lane is still doing fake per-chunk synths. I’m pulling the OpenMOSS runtime shape from the model/docs and your runner templates now so I can wire a real adapter instead of guessing.

Searched web for site:huggingface.co OpenMOSS-Team MOSS-TTS-Realtime Hugging Face
Searched web for https://docs.vllm.ai/en/latest/api/vllm/entrypoints/openai/realtime/api_router/
Searched web for site:github.com/OpenMOSS/MOSS-TTS moss_tts_realtime_model_card.md
I’ve confirmed the ASR live lane is stable enough to leave alone. The next step is using the OpenMOSS runtime shape directly, not forcing it through the current fake chunked TTS path.

Explored 5 files, 1 search
Searched for *moss* in .
Read TTSLive.tsx
Read model_registry.py
Read docker-compose.yml
Read settings.py
Read docker-compose.yml
Context automatically compacted
I’m reading the current TTS runtime and the OpenMOSS integration points first, then I’ll patch the live lane without disturbing the working ASR path.

Searched web for OpenMOSS-Team MOSS-TTS-Realtime vllm realtime docs official
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
I’ve confirmed the current state: ASR live is good, and the next task is replacing the fake TTS live path with a real OpenMOSS lane while keeping the existing chatterbox batch path intact. I’m reading the current TTS adapter/service/frontend flow and the official OpenMOSS model card so I can patch the smallest real runtime path instead of guessing.

Explored 5 files, 1 search
Searched for class MossRealtimeAdapter|start_stream\(|push_text\(|end_stream\(|synthesize\( in app
Read moss_realtime.py
Read streaming_service.py
Read useTTSStream.ts
Read TTSLive.tsx
Read settings.py
Context automatically compacted
You’ve got ASR live where it needs to be. I’m going to inspect the current TTS live path and verify the current OpenMOSS runtime/API shape from primary sources before I patch anything, so we don’t break the working substrate.

Searched web for OpenMOSS MOSS-TTS-Realtime official docs realtime api websocket huggingface
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
The ASR live lane is in the right place now. I’m inspecting the existing TTS stream service and the official MOSS-TTS-Realtime usage path so I can wire it in as a real lane without disturbing the working ASR behavior.

Explored 6 files
Read streaming_service.py
Read moss_realtime.py
Read model_registry.py
Read settings.py
Read TTSLive.tsx
Read useTTSStream.ts
Context automatically compacted
I’ve verified the current TTS live path is still the old fake chunked-batch flow. Next I’m checking the current OpenMOSS runtime/API contract so I can wire the real lane without breaking the working ASR stack.

Searched web for OpenMOSS-Team MOSS-TTS-Realtime Hugging Face realtime API websocket docs
ASR live is in the right place now. I’m moving to the TTS side by tracing the current live TTS gateway/backend path and matching it to the current OpenMOSS runtime contract before I patch anything.

Explored 5 files
Read stream.py
Read tts.py
Read tts_client.py
Read schemas.py
Read base.py
I’ve confirmed the current TTS live path still proxies a websocket, but the backend service itself is faking streaming by batch-synthesizing chunks. I’m opening the TTS request/response models and the existing Chatterbox adapter next so I can add OpenMOSS without disturbing the batch path.

Explored 5 files
Read responses.py
Read requests.py
Read chatterbox.py
Read TTSFile.tsx
Read tts.ts
Searched web for OpenMOSS-Team MOSS-TTS-Realtime Hugging Face realtime websocket api
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
I’ve got the current OpenMOSS contract now. It isn’t an OpenAI realtime websocket service like Voxtral; the official usage is a local streaming inferencer that accepts incremental text deltas and yields audio frames. I’m checking your local runner templates and model docs next so I can wire the right backend shape instead of forcing the wrong protocol onto it.

Explored 2 searches, 2 lists
Listed files in model-runners
Listed files in model.cards
Searched for MOSS-TTS|moss_tts_realtime|MOSS-TTS-Realtime|OpenMOSS in .
Searched for docker-compose* in model-runners
Context automatically compacted
I’m tracing the current TTS live path and the exact OpenMOSS runtime contract before I patch anything. The goal is to swap the fake chunked-batch lane for a real MOSS-backed streaming adapter without disturbing the ASR flow that’s now working.

Searched web for OpenMOSS MOSS-TTS-Realtime vLLM realtime API docs Hugging Face
I’ve confirmed Voxtral live is healthy and the duplicate-paragraph issue was UI-side accumulation, not multiple GPU runs. I’m moving to the TTS live lane now, starting with the MOSS model card/runtime contract and the current studio TTS stream path so I can replace the fake chunked-batch path without touching the working ASR flow.

Explored 3 files, 1 search, 1 list
Listed files in .
Searched for (^|/)(MOSS|moss|model_cards|Model Cards|Voxtel|Voxtral|Enhancements-List-GPT5\.4|PROJECT_STATE|CHANGELOG)
Read streaming_service.py
Read moss_realtime.py
Read TTSLive.tsx
I’ve confirmed the current TTS Live tab is still using a fake stream path: it chunks text, batch-synthesizes each chunk, and only produces a final blob at the end. I’m reading the hook, adapter interface, and TTS schemas now so I can replace that with a real MOSS-backed streaming adapter while keeping Chatterbox batch untouched.

Explored 6 files
Read useTTSStream.ts
Read model_registry.py
Read base.py
Read settings.py
Read requests.py
Read responses.py
Searched web for OpenMOSS-Team MOSS-TTS-Realtime GitHub docs realtime websocket API
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
Searched web for https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md
I have the key OpenMOSS runtime shape now: it isn’t an OpenAI realtime websocket service like Voxtral. The model card’s primary streaming contract is incremental push_text() / end_text() against a local inferencer, so I’m checking the repo docs you dropped in-root and the current TTS Live UI before I patch the backend path.

Explored 2 files, 2 searches, 1 list
Listed files in .
Searched for Voxtel runtime logs first clean streaming generation|ASR real-time first UI clean response|Enhancements-List-GPT5\.4|model cards|model_cards
Read CHANGELOG.md
Read PROJECT_STATE.md
Searched for stream|moss|tts live|audio_chunk|final_audio|quick copy|Download in frontend
Context automatically compacted
I’m moving to the TTS live lane now. First step is to inspect the current MOSS/streaming path in the repo and the upstream OpenMOSS docs so I can replace the fake chunked path without disturbing the working ASR flow.

Explored 2 searches, 1 list
Searched for moss|OpenMOSS|TTSStream|streaming_service|tts/stream|audio_chunk|final_audio|moss_realtime in services
Listed files in .
Searched for (model_cards|Model Cards|openmoss|moss|MOSS|Enhancements-List-GPT5\.4|AGENTS\.md)$
I’m treating ASR live as stable and moving the next implementation to the MOSS realtime TTS lane. I’m checking the current OpenMOSS runtime contract and the repo’s TTS stream path now so I can replace the fake chunked synth flow without breaking the working batch TTS or ASR live path.

Searched web for OpenMOSS-Team MOSS-TTS-Realtime realtime API docs official GitHub Hugging Face
Searched web for https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime
I’ve confirmed the current TTS live path is still a fake micro-batch loop and OpenMOSS wants a real incremental streaming path. I’m reading the exact TTS stream code and the upstream model card now so I can swap the backend contract first, then tighten the UI around the real stream states.

Explored 4 files
Read streaming_service.py
Read moss_realtime.py
Read useTTSStream.ts
Read TTSLive.tsx
Context automatically compacted
I’m moving to the TTS live lane now. I’ve confirmed the current implementation is still a fake chunked wrapper over batch synth, so I’m wiring a real env-backed OpenMOSS adapter path without touching the now-working Voxtral ASR flow.
