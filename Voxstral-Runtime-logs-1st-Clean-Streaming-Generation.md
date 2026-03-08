ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ git pull
docker compose --profile voxtral up -d --build asr frontend
remote: Enumerating objects: 35, done.
remote: Counting objects: 100% (35/35), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 18 (delta 12), reused 18 (delta 12), pack-reused 0 (from 0)
Unpacking objects: 100% (18/18), 3.14 KiB | 1.05 MiB/s, done.
From https://github.com/AetharaAI/AetherVoice-X
   a3b10f6..072ef71  main       -> origin/main
Updating a3b10f6..072ef71
Fast-forward
 CHANGELOG.md                                            |  5 +++++
 PROJECT_STATE.md                                        | 32 ++++++++++++--------------------
 services/asr/app/adapters/voxtral_realtime.py           | 13 +++++++++++--
 services/frontend/src/components/asr/TranscriptPane.tsx | 25 ++++++++++++++++++++++++-
 services/frontend/src/hooks/useASRStream.ts             | 51 +++++++++++++++++++++++++++++++++++++++------------
 services/frontend/src/pages/ASRLive.tsx                 |  4 ++--
 6 files changed, 93 insertions(+), 37 deletions(-)
[+] Building 1.5s (37/37) FINISHED                                                                                                                                                      
 => [internal] load local bake definitions                                                                                                                                         0.0s
 => => reading from stdin 2.00kB                                                                                                                                                   0.0s
 => [gateway internal] load build definition from Dockerfile                                                                                                                       0.0s
 => => transferring dockerfile: 480B                                                                                                                                               0.0s
 => [frontend internal] load build definition from Dockerfile                                                                                                                      0.0s
 => => transferring dockerfile: 410B                                                                                                                                               0.0s
 => [asr internal] load build definition from Dockerfile                                                                                                                           0.0s
 => => transferring dockerfile: 618B                                                                                                                                               0.0s
 => [tts internal] load build definition from Dockerfile                                                                                                                           0.0s
 => => transferring dockerfile: 464B                                                                                                                                               0.0s
 => [tts internal] load metadata for docker.io/library/python:3.12-slim                                                                                                            0.6s
 => [frontend internal] load metadata for docker.io/library/node:22-alpine                                                                                                         0.7s
 => [frontend internal] load .dockerignore                                                                                                                                         0.0s
 => => transferring context: 2B                                                                                                                                                    0.0s
 => [asr 1/6] FROM docker.io/library/python:3.12-slim@sha256:ccc7089399c8bb65dd1fb3ed6d55efa538a3f5e7fca3f5988ac3b5b87e593bf0                                                      0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:ccc7089399c8bb65dd1fb3ed6d55efa538a3f5e7fca3f5988ac3b5b87e593bf0                                                          0.0s
 => [asr internal] load build context                                                                                                                                              0.1s
 => => transferring context: 3.72MB                                                                                                                                                0.1s
 => [frontend 1/7] FROM docker.io/library/node:22-alpine@sha256:8094c002d08262dba12645a3b4a15cd6cd627d30bc782f53229a2ec13ee22a00                                                   0.0s
 => => resolve docker.io/library/node:22-alpine@sha256:8094c002d08262dba12645a3b4a15cd6cd627d30bc782f53229a2ec13ee22a00                                                            0.0s
 => [frontend internal] load build context                                                                                                                                         0.0s
 => => transferring context: 15.13kB                                                                                                                                               0.0s
 => CACHED [frontend 2/7] WORKDIR /app/services/frontend                                                                                                                           0.0s
 => CACHED [frontend 3/7] COPY services/frontend/package.json ./package.json                                                                                                       0.0s
 => CACHED [frontend 4/7] COPY services/frontend/tsconfig.json ./tsconfig.json                                                                                                     0.0s
 => CACHED [frontend 5/7] COPY services/frontend/vite.config.ts ./vite.config.ts                                                                                                   0.0s
 => CACHED [frontend 6/7] RUN npm install                                                                                                                                          0.0s
 => [frontend 7/7] COPY services/frontend /app/services/frontend                                                                                                                   0.0s
 => CACHED [asr 2/6] WORKDIR /app                                                                                                                                                  0.0s
 => CACHED [asr 3/6] RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*                                                        0.0s
 => CACHED [tts 4/6] COPY services/tts/requirements.txt /tmp/requirements.txt                                                                                                      0.0s
 => CACHED [tts 5/6] RUN pip install --no-cache-dir -r /tmp/requirements.txt                                                                                                       0.0s
 => CACHED [gateway 4/6] COPY services/gateway/requirements.txt /tmp/requirements.txt                                                                                              0.0s
 => CACHED [gateway 5/6] RUN pip install --no-cache-dir -r /tmp/requirements.txt                                                                                                   0.0s
 => CACHED [asr 4/6] COPY services/asr/requirements.txt /tmp/requirements.txt                                                                                                      0.0s
 => CACHED [asr 5/6] RUN pip install --no-cache-dir -r /tmp/requirements.txt                                                                                                       0.0s
 => [asr 6/6] COPY . /app                                                                                                                                                          0.1s
 => [frontend] exporting to image                                                                                                                                                  0.1s
 => => exporting layers                                                                                                                                                            0.0s
 => => exporting manifest sha256:c198140c2ec0038a6b161cf754ddf4e11c00f91eb8931ae221392712947e572d                                                                                  0.0s
 => => exporting config sha256:115c85e2858de3b047a08acef85124c97fa5833ffa9ca608587e43234eab0ea6                                                                                    0.0s
 => => exporting attestation manifest sha256:c8c6c6c2dce19f6547426688cf56afef2c6e4173e634e7e8da84715c9b164153                                                                      0.0s
 => => exporting manifest list sha256:309329f0382a65dc33a509970c67432127ef70c9bb06986a1ee656796a1f7169                                                                             0.0s
 => => naming to docker.io/library/aethervoice-x-frontend:latest                                                                                                                   0.0s
 => => unpacking to docker.io/library/aethervoice-x-frontend:latest                                                                                                                0.0s
 => [gateway 6/6] COPY . /app                                                                                                                                                      0.1s
 => [tts 6/6] COPY . /app                                                                                                                                                          0.1s
 => [asr] exporting to image                                                                                                                                                       0.4s
 => => exporting layers                                                                                                                                                            0.2s
 => => exporting manifest sha256:9611d8a8c55abde3eaa9d5691666dd26da1353d54f0fb821ca6bd155fda4ebbf                                                                                  0.0s
 => => exporting config sha256:7424aef15656216262cab972ab7b3b0b4919796aca1ab3204a8a590bd48826e0                                                                                    0.0s
 => => exporting attestation manifest sha256:eccc8341470c785dbcc9ae8c77f2c23bc11b3d9aa845363f2aa878b872cfe7ca                                                                      0.0s
 => => exporting manifest list sha256:5cb34fee94f9cfd9672fa8e876f66939c0e1295b98a4ab649716b6ca040fb69e                                                                             0.0s
 => => naming to docker.io/library/aethervoice-x-asr:latest                                                                                                                        0.0s
 => => unpacking to docker.io/library/aethervoice-x-asr:latest                                                                                                                     0.1s
 => [tts] exporting to image                                                                                                                                                       0.4s
 => => exporting layers                                                                                                                                                            0.2s
 => => exporting manifest sha256:9605a4cd096a132f6bcbdf0e085f7ac858969136879f95897cfd835bbe7eda4a                                                                                  0.0s
 => => exporting config sha256:7e99a360bcaf9656bb2b12f9341fe1ce44802ceff4afe36dd08962ee7018c753                                                                                    0.0s
 => => exporting attestation manifest sha256:ab8df7b04c5e0acd783933edb1cfd100e3cf0039410b764485143f66237d1df5                                                                      0.0s
 => => exporting manifest list sha256:f60f77120ab42b85f54da1805bdac1db6f17cf9fcb9fb888b03d8a988cb560f8                                                                             0.0s
 => => naming to docker.io/library/aethervoice-x-tts:latest                                                                                                                        0.0s
 => => unpacking to docker.io/library/aethervoice-x-tts:latest                                                                                                                     0.1s
 => [gateway] exporting to image                                                                                                                                                   0.4s
 => => exporting layers                                                                                                                                                            0.2s
 => => exporting manifest sha256:26e92d2fdf2f796d6b28a405aa16cb8a473906d58a8c17fe73fd12d3a31d6880                                                                                  0.0s
 => => exporting config sha256:fc8ae2048022ea76f90a920936640a179d265ebfbb1342da56ddcb28f14a7052                                                                                    0.0s
 => => exporting attestation manifest sha256:7f7625e72d5d6a5481d7e778be3e93510101a249e14a98ae5f2587b10920eb6b                                                                      0.0s
 => => exporting manifest list sha256:b1f42aa1791febe19dbc5ec24a25d2107121a2c0ba32dfbeb3225ab94e0c087e                                                                             0.0s
 => => naming to docker.io/library/aethervoice-x-gateway:latest                                                                                                                    0.0s
 => => unpacking to docker.io/library/aethervoice-x-gateway:latest                                                                                                                 0.1s
 => [frontend] resolving provenance for metadata file                                                                                                                              0.0s
 => [tts] resolving provenance for metadata file                                                                                                                                   0.0s
 => [gateway] resolving provenance for metadata file                                                                                                                               0.0s
 => [asr] resolving provenance for metadata file                                                                                                                                   0.0s
[+] up 11/11
 ✔ Image aethervoice-x-gateway        Built                                                                                                                                        1.6ss
 ✔ Image aethervoice-x-tts            Built                                                                                                                                        1.6ss
 ✔ Image aethervoice-x-frontend       Built                                                                                                                                        1.6ss
 ✔ Image aethervoice-x-asr            Built                                                                                                                                        1.6ss
 ✔ Container aethervoice-x-minio-1    Running                                                                                                                                      0.0ss
 ✔ Container aethervoice-x-redis-1    Running                                                                                                                                      0.0ss
 ✔ Container aethervoice-x-postgres-1 Running                                                                                                                                      0.0ss
 ✔ Container aethervoice-x-tts-1      Recreated                                                                                                                                    10.4s
 ✔ Container aethervoice-x-asr-1      Recreated                                                                                                                                    10.4s
 ✔ Container aethervoice-x-gateway-1  Recreated                                                                                                                                    10.3s
 ✔ Container aethervoice-x-frontend-1 Recreated                                                                                                                                    0.2s
ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/AetherVoice-X$ docker compose --profile voxtral logs -f gateway asr voxtral
asr-1  | INFO:     Started server process [54]
asr-1  | INFO:     Waiting for application startup.
asr-1  | {"level": "INFO", "message": "voxtral_adapter_initialized", "service": "asr", "logger": "asr", "time": "2026-03-08 04:49:49,037", "taskName": "Task-2"}
asr-1  | {"level": "INFO", "message": "asr_started", "service": "asr", "logger": "asr", "time": "2026-03-08 04:49:49,037", "taskName": "Task-2"}
asr-1  | INFO:     Application startup complete.
asr-1  | INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
asr-1  | INFO:     172.18.0.8:37578 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | INFO:     Started server process [10]
gateway-1  | INFO:     Waiting for application startup.
gateway-1  | {"level": "INFO", "message": "gateway_started", "service": "gateway", "logger": "gateway", "time": "2026-03-08 04:49:49,031", "taskName": "Task-2"}
gateway-1  | INFO:     Application startup complete.
gateway-1  | INFO:     Uvicorn running on http://0.0.0.0:8010 (Press CTRL+C to quit)
voxtral-1  | /usr/local/lib/python3.12/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
voxtral-1  |   warnings.warn(
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302] 
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302]        █     █     █▄   ▄█
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.17.0
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302]   █▄█▀ █     █     █     █  model   /models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:302] 
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:19 [utils.py:238] non-default args: {'model_tag': '/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602', 'tokenizer_mode': 'mistral', 'trust_remote_code': True, 'max_model_len': 8192, 'enforce_eager': True, 'served_model_name': ['mistralai/Voxtral-Mini-4B-Realtime-2602'], 'config_format': 'mistral', 'generation_config': 'vllm', 'load_format': 'mistral', 'gpu_memory_utilization': 0.85, 'compilation_config': {'level': None, 'mode': None, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': [], 'splitting_ops': None, 'compile_mm_encoder': False, 'compile_sizes': None, 'compile_ranges_split_points': None, 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.PIECEWISE: 1>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': None, 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': None, 'pass_config': {}, 'max_cudagraph_capture_size': None, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': None, 'static_all_moe_layers': []}}
voxtral-1  | (APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] The params.json file is missing 'max_position_embeddings' and could not get a value from the HF config. Defaulting to 128000
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] Traceback (most recent call last):
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:49:50,085", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:49:50,088", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:60518 - "GET /api/health HTTP/1.1" 200 OK
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/transformers/models/auto/configuration_auto.py", line 1360, in from_pretrained
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     config_class = CONFIG_MAPPING[config_dict["model_type"]]
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]                    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/transformers/models/auto/configuration_auto.py", line 1048, in __getitem__
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     raise KeyError(key)
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] KeyError: 'voxtral_realtime'
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] 
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] During handling of the above exception, another exception occurred:
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] 
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] Traceback (most recent call last):
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/config.py", line 1145, in _maybe_retrieve_max_pos_from_hf
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     hf_config = get_config(
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]                 ^^^^^^^^^^^
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/config.py", line 628, in get_config
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     config_dict, config = config_parser.parse(
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]                           ^^^^^^^^^^^^^^^^^^^^
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/config.py", line 194, in parse
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     raise e
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/config.py", line 173, in parse
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     config = AutoConfig.from_pretrained(
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]   File "/usr/local/lib/python3.12/dist-packages/transformers/models/auto/configuration_auto.py", line 1362, in from_pretrained
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154]     raise ValueError(
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] ValueError: The checkpoint you are trying to load has model type `voxtral_realtime` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] 
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:19 [config.py:1154] You can update Transformers with the command `pip install --upgrade transformers`. If this does not work, and the checkpoint is very new, then there may not be a release version that supports this model yet. In this case, you can get the most up-to-date code by installing Transformers from source with the command `pip install git+https://github.com/huggingface/transformers.git`
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:26 [model.py:531] Resolved architecture: VoxtralRealtimeGeneration
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:26 [model.py:1554] Using max model len 8192
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:26 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=2048.
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:26 [vllm.py:747] Asynchronous scheduling is enabled.
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:26 [vllm.py:781] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:06:26 [vllm.py:792] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:26 [vllm.py:957] Cudagraph is disabled under eager mode
voxtral-1  | (APIServer pid=1) [2026-03-08 03:06:26] INFO tekken.py:195: Non special vocabulary size is 130072 with 1000 special tokens.
voxtral-1  | (APIServer pid=1) [2026-03-08 03:06:26] INFO tekken.py:572: Cutting non special vocabulary to first 130072 tokens.
voxtral-1  | (APIServer pid=1) [2026-03-08 03:06:27] INFO tekken.py:195: Non special vocabulary size is 130072 with 1000 special tokens.
voxtral-1  | (APIServer pid=1) [2026-03-08 03:06:27] INFO tekken.py:572: Cutting non special vocabulary to first 130072 tokens.
voxtral-1  | /usr/local/lib/python3.12/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
voxtral-1  |   warnings.warn(
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:33 [core.py:101] Initializing a V1 LLM engine (v0.17.0) with config: model='/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602', speculative_config=None, tokenizer='/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602', skip_tokenizer_init=False, tokenizer_mode=mistral, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=8192, download_dir=None, load_format=mistral, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=False, quantization=None, enforce_eager=True, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=mistralai/Voxtral-Mini-4B-Realtime-2602, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['all'], 'splitting_ops': [], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [2048], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 0, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
voxtral-1  | (EngineCore_DP0 pid=499) [2026-03-08 03:06:33] INFO tekken.py:195: Non special vocabulary size is 130072 with 1000 special tokens.
voxtral-1  | (EngineCore_DP0 pid=499) [2026-03-08 03:06:33] INFO tekken.py:572: Cutting non special vocabulary to first 130072 tokens.
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:34 [parallel_state.py:1393] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.7:58187 backend=nccl
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:34 [parallel_state.py:1715] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:34 [base.py:106] Offloader set to NoopOffloader
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:34 [gpu_model_runner.py:4255] Starting to load model /models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602...
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:35 [vllm.py:747] Asynchronous scheduling is enabled.
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:35 [vllm.py:781] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:35 [vllm.py:792] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:35 [vllm.py:957] Cudagraph is disabled under eager mode
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:35 [cuda.py:405] Using FLASH_ATTN attention backend out of potential backends: ['FLASH_ATTN', 'FLASHINFER', 'TRITON_ATTN', 'FLEX_ATTENTION'].
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:35 [flash_attn.py:587] Using FlashAttention version 2
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:35 [vllm.py:781] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:35 [vllm.py:792] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:35 [vllm.py:957] Cudagraph is disabled under eager mode
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:01<00:00,  1.40s/it]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:01<00:00,  1.40s/it]
voxtral-1  | (EngineCore_DP0 pid=499) 
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:37 [default_loader.py:293] Loading weights took 1.66 seconds
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:37 [gpu_model_runner.py:4338] Model loading took 8.38 GiB memory and 2.248291 seconds
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:38 [gpu_model_runner.py:5254] Encoder cache will be initialized with a budget of 8192 tokens, and profiled with 1 audio items of the maximum feature size.
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:45 [gpu_worker.py:424] Available KV cache memory: 9.58 GiB
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:45 [kv_cache_utils.py:1054] Add 6 padding layers, may waste at most 23.08% KV cache memory
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:45 [kv_cache_utils.py:1314] GPU KV cache size: 4,896 tokens
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:45 [kv_cache_utils.py:1319] Maximum concurrency for 8,192 tokens per request: 2.54x
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:45 [core.py:282] init engine (profile, create kv cache, warmup model) took 7.34 seconds
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:45 [vllm.py:781] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-1  | (EngineCore_DP0 pid=499) WARNING 03-08 03:06:45 [vllm.py:792] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-1  | (EngineCore_DP0 pid=499) INFO 03-08 03:06:45 [vllm.py:957] Cudagraph is disabled under eager mode
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [api_server.py:495] Supported tasks: ['generate', 'transcription', 'realtime']
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - decorators.py:76: [PING] Framework handler registered: ping
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - base_factory.py:88: [INJECT_ADAPTER_ID] Transform decorator applied to: invocations
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - base_factory.py:113: [INJECT_ADAPTER_ID] Registered transform handler for invocations
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - base_factory.py:88: [STATEFUL_SESSION_MANAGER] Transform decorator applied to: decorated_func
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - base_factory.py:113: [STATEFUL_SESSION_MANAGER] Registered transform handler for decorated_func
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - decorators.py:76: [INVOKE] Framework handler registered: decorated_func
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [api_router.py:56] Realtime API router attached
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - __init__.py:156: Starting SageMaker bootstrap process
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - registry.py:109: [REGISTRY] Middleware resolution and registration complete
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - core.py:100: [MIDDLEWARE_LOADER] Middleware stack rebuilt successfully
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - core.py:102: [MIDDLEWARE_LOADER] Processed 4 middlewares
voxtral-1  | (APIServer pid=1) [WARNING] model_hosting_container_standards - function_loader.py:71: Failed to load function from spec 'model:custom_sagemaker_invocation_handler': HandlerFileNotFoundError: File '/opt/ml/model/model.py' not found in search paths: ['/opt/ml/model/']
voxtral-1  | (APIServer pid=1) [WARNING] model_hosting_container_standards - function_loader.py:71: Failed to load function from spec 'model:custom_sagemaker_ping_handler': HandlerFileNotFoundError: File '/opt/ml/model/model.py' not found in search paths: ['/opt/ml/model/']
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - sagemaker_router.py:91: Creating SageMaker router with unified route resolver
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - routing.py:170: Creating router with prefix='', tags=['sagemaker']
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - routing.py:108: Mounting 2 handlers to router
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - routing.py:182: Router created with 0 routes
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - sagemaker_router.py:99: SageMaker router created successfully with 0 routes
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - routing.py:285: Including router with conflict detection
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - routing.py:303: Successfully included router with 0 routes
voxtral-1  | (APIServer pid=1) [INFO] model_hosting_container_standards - __init__.py:168: SageMaker bootstrap completed successfully
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [serving.py:185] Warming up chat template processing...
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [serving.py:210] Chat template warmup completed in 1.6ms
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [speech_to_text.py:220] Warming up multimodal input processor...
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [speech_to_text.py:243] Input processor warmup completed in 0.01s
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [speech_to_text.py:220] Warming up multimodal input processor...
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [speech_to_text.py:243] Input processor warmup completed in 0.00s
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [serving.py:47] OpenAIServingRealtime initialized for task: realtime
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [api_server.py:500] Starting vLLM API server 0 on http://0.0.0.0:8000
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:38] Available routes are:
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /openapi.json, Methods: GET, HEAD
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /docs, Methods: GET, HEAD
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /docs/oauth2-redirect, Methods: GET, HEAD
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /redoc, Methods: GET, HEAD
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /tokenize, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /detokenize, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /load, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /version, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /health, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /metrics, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/models, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /ping, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /ping, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /invocations, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/chat/completions, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/chat/completions/render, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/responses, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/responses/{response_id}, Methods: GET
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/responses/{response_id}/cancel, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/completions, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/completions/render, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/messages, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/messages/count_tokens, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /inference/v1/generate, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /scale_elastic_ep, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /is_scaling_elastic_ep, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/audio/transcriptions, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:47] Route: /v1/audio/translations, Methods: POST
voxtral-1  | (APIServer pid=1) INFO 03-08 03:06:45 [launcher.py:58] Route: /v1/realtime, Endpoint: realtime_endpoint
voxtral-1  | (APIServer pid=1) INFO:     Started server process [1]
voxtral-1  | (APIServer pid=1) INFO:     Waiting for application startup.
voxtral-1  | (APIServer pid=1) INFO:     Application startup complete.
voxtral-1  | (APIServer pid=1) INFO:     172.18.0.6:58636 - "WebSocket /v1/realtime" [accepted]
voxtral-1  | (APIServer pid=1) INFO:     connection open
voxtral-1  | (APIServer pid=1) INFO:     connection closed
voxtral-1  | (APIServer pid=1) INFO:     172.18.0.6:34976 - "WebSocket /v1/realtime" [accepted]
voxtral-1  | (APIServer pid=1) INFO:     connection open
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:01 [input_processor.py:254] Passing raw prompts to InputProcessor is deprecated and will be removed in v0.18. You should instead pass the outputs of Renderer.render_cmpl() or Renderer.render_chat().
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:02 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:02 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:03 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:03 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:04 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:04 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:05 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:05 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 03:19:05 [loggers.py:259] Engine 000: Avg prompt throughput: 344.4 tokens/s, Avg generation throughput: 5.3 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 1.1%, Prefix cache hit rate: 0.0%
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:06 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:06 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:07 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:07 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:08 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:08 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:09 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:09 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:10 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:10 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:11 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:11 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:12 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:12 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:13 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:13 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:14 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:14 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:15 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:15 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 03:19:15 [loggers.py:259] Engine 000: Avg prompt throughput: 1925.0 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 2.6%, Prefix cache hit rate: 0.0%
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:16 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:16 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:17 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:17 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:18 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:18 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:19 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) WARNING 03-08 03:19:19 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO:     connection closed
voxtral-1  | (APIServer pid=1) INFO 03-08 03:19:25 [loggers.py:259] Engine 000: Avg prompt throughput: 1731.8 tokens/s, Avg generation throughput: 6.9 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
voxtral-1  | (APIServer pid=1) INFO 03-08 03:19:35 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
asr-1      | INFO:     172.18.0.8:58818 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:22,422", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:22,425", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:36962 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "stream_adapter_selected", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,074", "taskName": "Task-9"}
asr-1      | {"level": "INFO", "message": "voxtral_ws_connecting", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,074", "taskName": "Task-9"}
voxtral-1  | (APIServer pid=1) INFO:     172.18.0.6:52962 - "WebSocket /v1/realtime" [accepted]
voxtral-1  | (APIServer pid=1) INFO:     connection open
asr-1      | {"level": "INFO", "message": "voxtral_stream_started", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,079", "taskName": "Task-9"}
asr-1      | INFO:     172.18.0.8:40874 - "GET /internal/health HTTP/1.1" 200 OK
asr-1      | INFO:     172.18.0.8:40862 - "POST /internal/stream/start HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:38,081", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: POST http://asr:8090/internal/stream/start \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:38,081", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:35324 - "POST /api/v1/asr/stream/start HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:38,084", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:35336 - "GET /api/health HTTP/1.1" 200 OK
gateway-1  | INFO:     172.18.0.1:35352 - "WebSocket /api/v1/asr/stream/sess_live_8df0ece0d3f741c0af57a831" [accepted]
gateway-1  | {"level": "INFO", "message": "gateway_stream_proxy_connecting", "service": "gateway", "logger": "gateway", "time": "2026-03-08 04:50:38,307", "taskName": "Task-31"}
gateway-1  | INFO:     connection open
asr-1      | INFO:     172.18.0.8:40878 - "WebSocket /internal/stream/sess_live_8df0ece0d3f741c0af57a831" [accepted]
asr-1      | {"level": "INFO", "message": "stream_websocket_accepted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,311", "taskName": "Task-14"}
asr-1      | INFO:     connection open
gateway-1  | {"level": "INFO", "message": "gateway_stream_proxy_connected", "service": "gateway", "logger": "gateway", "time": "2026-03-08 04:50:38,312", "taskName": "Task-31"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,621", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:38,878", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:39,134", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:39,390", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:39 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:39,646", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:39,891", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:39 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,158", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,158", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,404", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:40 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,660", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,660", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,926", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:40,926", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:40 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,172", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,172", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,438", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,438", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:41 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,694", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,694", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,939", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:41,939", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:41 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,207", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,207", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,451", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,451", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:42 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,791", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:42,792", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,048", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,048", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:43 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,220", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,220", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,487", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:43 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,743", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:43,999", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:43 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:44,255", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:44,511", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:44 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:44,767", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,023", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:45 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,279", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,279", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,524", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,524", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:45 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,780", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:45,780", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,046", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,047", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:46 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:50:46 [loggers.py:259] Engine 000: Avg prompt throughput: 713.3 tokens/s, Avg generation throughput: 8.7 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 1.5%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,291", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,291", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,558", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:46 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,804", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:46,804", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,060", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,060", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:47 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,326", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,326", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,572", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:47 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,838", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:47,838", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,094", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:48 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,340", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,340", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,606", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:48 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,862", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:48,862", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,118", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:49 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,375", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,375", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,631", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,631", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:49 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,887", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:49,887", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,143", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,143", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:50 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,398", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,398", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,655", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,655", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:50 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,900", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:50,900", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,156", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,156", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:51 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,412", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,412", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,679", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,679", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:51 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:51,924", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:52,179", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:52 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:52,446", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:52,691", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:52 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:52,958", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:52,958", "taskName": "Task-14"}
asr-1      | INFO:     172.18.0.8:55262 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:53,077", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:50:53,079", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:36680 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,214", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:53 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,459", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,726", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,727", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:53 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,982", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:53,983", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,239", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,239", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:54 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,495", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,495", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,751", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:54,751", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:54 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,007", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,007", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,263", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:55 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,518", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,519", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:55,774", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:55 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,031", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,031", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:50:56 [loggers.py:259] Engine 000: Avg prompt throughput: 2349.9 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 2.9%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,276", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,276", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:56 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,531", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:56,798", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:56 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,055", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,310", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,311", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:57 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,577", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,577", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,822", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:57,822", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:57 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:58,078", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:58,345", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:58 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:58,590", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:58,590", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:58,857", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:58 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,113", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,113", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,358", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,358", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:59 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,625", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,625", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,881", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:50:59,881", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:50:59 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,137", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,137", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,383", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,383", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:00 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,639", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,639", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,895", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:00,895", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:00 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,151", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,406", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:01 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,735", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,735", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,918", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:01,919", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:01 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,175", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,175", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,431", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,431", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:02 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,697", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,698", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:02,943", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:02 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,198", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,198", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,465", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,465", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:03 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,710", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,711", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:03,977", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:03 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,233", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,234", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,478", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,478", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:04 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,745", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,745", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:04,991", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:04 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:05,257", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:05,513", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:05,513", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:05 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:05,758", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:05,758", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,087", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:06 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:06 [loggers.py:259] Engine 000: Avg prompt throughput: 3875.0 tokens/s, Avg generation throughput: 12.4 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 4.4%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,271", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,271", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,527", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,527", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:06 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,783", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:06,783", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,039", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,039", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:07 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,295", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,295", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,551", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,551", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:07 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,818", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:07,818", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,063", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:08 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | INFO:     172.18.0.8:60342 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:08,076", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:08,079", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:56202 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,318", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,318", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,564", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,564", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:08 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,821", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:08,821", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,078", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:09 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,334", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,334", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,590", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,590", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:09 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,847", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:09,847", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,105", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,105", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:10 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,360", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,360", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,617", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,617", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:10 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,873", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:10,873", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,130", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,130", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:11 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,376", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,376", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,632", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:11 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:11,889", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,145", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,145", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:12 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,401", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,401", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,658", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,658", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:12 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:12,915", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,172", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,172", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:13 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,428", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,684", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,684", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:13 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,940", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:13,940", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,197", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,197", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:14 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,453", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,710", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,710", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:14 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:14,967", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,224", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,224", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:15 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,479", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,480", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,808", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,809", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:15 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,993", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:15,993", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:16 [loggers.py:259] Engine 000: Avg prompt throughput: 5562.2 tokens/s, Avg generation throughput: 12.7 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 5.9%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:16,249", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:16 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:16,506", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:16,506", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:16,751", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:16,751", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:16 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,008", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,008", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,265", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,265", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:17 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,521", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,521", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:17,777", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:17 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,034", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,290", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,290", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:18 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,547", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,547", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,804", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:18,804", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:18 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,060", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,060", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,316", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:19 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,573", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,573", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:19,829", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:19 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,085", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,342", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,342", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:20 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,600", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,600", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,855", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:20,855", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:20 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,112", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,113", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,368", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,368", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:21 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,625", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:21,882", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:21 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,138", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,138", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,384", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,384", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:22 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,640", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,640", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,897", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:22,897", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:22 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | INFO:     172.18.0.8:55456 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:23,072", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:23,074", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:49664 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,153", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,410", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,410", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:23 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,666", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,666", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,923", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:23,923", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:23 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:24,179", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:24,436", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:24 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:24,692", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:24,948", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:24 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,205", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,462", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:25 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,717", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,717", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,975", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:25,975", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:25 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:26 [loggers.py:259] Engine 000: Avg prompt throughput: 6986.7 tokens/s, Avg generation throughput: 12.4 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 7.4%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,231", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,231", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,488", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,488", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:26 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,744", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:26,744", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,074", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,074", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:27 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,257", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,257", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,513", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:27 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:27,760", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,016", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,017", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:28 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,273", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,529", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,529", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:28 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,786", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:28,786", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,043", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,043", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:29 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,299", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,555", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,555", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:29 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,812", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:29,812", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,068", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,068", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:30 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,325", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,325", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,581", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,581", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:30 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:30,837", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,094", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,094", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:31 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,350", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,607", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,607", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:31 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,864", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:31,864", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:32,120", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:32 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:32,377", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:32,377", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:32,633", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:32 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:32,890", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,135", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,136", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:33 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,391", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,391", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,648", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:33 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,905", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:33,905", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,161", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:34 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,418", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,418", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,675", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:34 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,930", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:34,931", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,188", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,188", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:35 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,444", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,700", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:35 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,956", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:35,957", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:36 [loggers.py:259] Engine 000: Avg prompt throughput: 8674.2 tokens/s, Avg generation throughput: 12.6 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 8.7%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:36,213", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:36,213", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:36 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:36,469", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:36,726", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:36 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:36,983", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,239", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,239", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:37 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,495", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,495", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,752", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:37,752", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:37 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,009", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,009", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,266", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,266", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:38 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,522", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,522", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,768", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:38,768", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:38 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,024", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,024", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,280", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,280", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:39 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,537", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,538", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,794", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:39,794", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:39 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,050", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,050", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,307", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,307", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:40 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,564", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,564", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,820", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:40,820", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:40 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,077", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,077", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,332", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,332", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:41 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,589", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,589", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,845", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:41,845", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:41 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,103", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,358", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:42 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,615", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,615", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,872", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:42,872", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:42 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,128", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,129", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,385", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,385", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:43 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,641", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,897", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:43,897", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:43 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,144", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,144", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,400", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,400", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:44 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,656", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,656", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,913", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:44,913", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:44 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,170", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,426", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,426", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:45 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,683", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,683", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:45,939", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:45 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:46 [loggers.py:259] Engine 000: Avg prompt throughput: 10173.8 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.0%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,195", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,453", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,453", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:46 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,709", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,709", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,964", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:46,964", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:46 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:47,221", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:47,221", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:47,477", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:47 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:47,734", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:47,991", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:47 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,247", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,247", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,504", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,504", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:48 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,761", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:48,761", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,017", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,018", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:49 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,273", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,273", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,519", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,520", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:49 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,776", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:49,776", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,032", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,032", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:50 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | INFO:     172.18.0.8:54908 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:50,096", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:51:50,099", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:34184 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,289", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,545", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,545", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:50 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,802", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:50,802", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:51,059", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:51 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:51,315", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:51,572", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:51,572", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:51 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:51,829", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,085", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,085", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:52 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,341", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,341", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,597", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:52 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:52,853", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,110", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:53 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,366", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,366", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,623", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,623", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:53 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,879", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:53,879", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,136", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,136", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:54 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,392", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,392", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,650", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,650", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:54 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:54,906", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,152", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,152", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:55 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,408", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,664", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,664", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:55 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:55,921", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:51:56 [loggers.py:259] Engine 000: Avg prompt throughput: 11737.0 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.2%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:56,177", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:56 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:56,435", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:56,763", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:56 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:56,948", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:57,204", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:57 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:57,461", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:57,717", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:57 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:57,972", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:58,229", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:58 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:58,486", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:58,743", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:58 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:58,998", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:58,999", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:59,255", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:59 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:59,512", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:51:59,770", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:51:59 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:00,025", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:00,282", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:00 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:00,527", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:00,783", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:00 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,041", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,041", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,297", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,297", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:01 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,554", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,810", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:01,810", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:01 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,066", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,323", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,323", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:02 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,579", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,579", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:02,836", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:02 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,092", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,092", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,348", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,348", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:03 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,605", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,861", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:03,861", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:03 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,118", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,118", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,375", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,375", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:04 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,632", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,632", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,888", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:04,888", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:04 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:05,144", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:05,401", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:05 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:05,657", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:05,914", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:05,914", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:05 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:06 [loggers.py:259] Engine 000: Avg prompt throughput: 13298.2 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.3%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,159", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,160", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,417", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:06 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,673", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,673", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,929", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:06,929", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:06 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,185", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,185", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,442", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,442", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:07 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,753", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,955", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:07,955", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:07 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,212", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,212", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,468", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,468", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:08 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,725", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:08,981", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:08 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:09,237", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:09,237", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:09,494", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:09,495", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:09 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:09,750", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,007", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,008", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:10 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,264", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,264", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,525", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:10 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,777", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:10,777", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,034", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,034", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:11 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,290", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,290", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,535", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,535", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:11 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,792", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:11,792", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,049", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:12 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,305", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,305", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,562", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,562", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:12 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,819", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:12,819", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,075", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:13 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,332", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,332", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,589", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,589", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:13 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:13,940", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:14,624", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:14,624", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:14 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:16 [loggers.py:259] Engine 000: Avg prompt throughput: 12009.9 tokens/s, Avg generation throughput: 10.2 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.5%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:17,375", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:17,375", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:17,637", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:17,637", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:17 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:19,380", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:19,380", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,094", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,094", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:20 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,241", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,241", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,537", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:20,537", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:20 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:21,541", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:21,542", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:26 [loggers.py:259] Engine 000: Avg prompt throughput: 2851.9 tokens/s, Avg generation throughput: 2.3 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.5%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:27,022", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:27,022", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:27 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:27,357", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:28,577", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:28,577", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:28 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:28,960", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:29,826", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:29,826", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:29 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:30,309", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:30,309", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:30,531", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:30 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:32,397", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:32,901", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:32 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:36 [loggers.py:259] Engine 000: Avg prompt throughput: 3543.4 tokens/s, Avg generation throughput: 2.8 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.3%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:37,901", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:38,520", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:38,520", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:38 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:40,149", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:40,149", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:42,798", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:42,798", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:42 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:44,558", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:44,558", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:45,782", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:45,782", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:45 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:46 [loggers.py:259] Engine 000: Avg prompt throughput: 2578.8 tokens/s, Avg generation throughput: 2.0 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:48,097", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:48,097", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:48,949", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:48,949", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:48 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:49,283", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:49,283", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:49,692", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:49 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | INFO:     172.18.0.8:46216 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:52:50,182", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:52:50,184", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:42740 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:51,269", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:51,269", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:51,416", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:51,416", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:51 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:52,062", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:52,356", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:52,356", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:52 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:52,914", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:52:52,915", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:52:52 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:52:56 [loggers.py:259] Engine 000: Avg prompt throughput: 4209.5 tokens/s, Avg generation throughput: 3.2 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
voxtral-1  | (APIServer pid=1) INFO 03-08 04:53:06 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:13,855", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:13,856", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:53:13 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,171", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,172", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,174", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:53:14 [connection.py:164] Generation already in progress, ignoring commit
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,874", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,874", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:14,875", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:53:14 [connection.py:164] Generation already in progress, ignoring commit
voxtral-1  | (APIServer pid=1) INFO 03-08 04:53:16 [loggers.py:259] Engine 000: Avg prompt throughput: 2547.7 tokens/s, Avg generation throughput: 1.9 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:16,891", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "stream_events_emitted", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:16,891", "taskName": "Task-14"}
asr-1      | {"level": "INFO", "message": "voxtral_stream_partial_window_ready", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:16,893", "taskName": "Task-14"}
voxtral-1  | (APIServer pid=1) WARNING 03-08 04:53:16 [connection.py:164] Generation already in progress, ignoring commit
gateway-1  | INFO:     connection closed
asr-1      | {"level": "INFO", "message": "stream_websocket_disconnected", "service": "asr", "logger": "asr", "time": "2026-03-08 04:53:17,902", "taskName": "Task-14"}
asr-1      | INFO:     connection closed
gateway-1  | {"level": "INFO", "message": "gateway_stream_proxy_disconnected", "service": "gateway", "logger": "gateway", "time": "2026-03-08 04:53:17,901", "taskName": "Task-31"}
voxtral-1  | (APIServer pid=1) INFO 03-08 04:53:26 [loggers.py:259] Engine 000: Avg prompt throughput: 812.1 tokens/s, Avg generation throughput: 0.6 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
voxtral-1  | (APIServer pid=1) INFO 03-08 04:53:36 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 9.6%, Prefix cache hit rate: 0.0%
asr-1      | INFO:     172.18.0.8:49642 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:53:50,077", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:53:50,079", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:54544 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | INFO:     172.18.0.8:59924 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:54:50,077", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:54:50,080", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:52304 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | INFO:     172.18.0.8:57136 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:55:50,083", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:55:50,085", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:58300 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | INFO:     172.18.0.8:58168 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:56:50,100", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:56:50,103", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:53554 - "GET /api/health HTTP/1.1" 200 OK
asr-1      | INFO:     172.18.0.8:60052 - "GET /internal/health HTTP/1.1" 200 OK
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://asr:8090/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:57:50,077", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | {"level": "INFO", "message": "HTTP Request: GET http://tts:8091/internal/health \"HTTP/1.1 200 OK\"", "service": "unknown", "logger": "httpx", "time": "2026-03-08 04:57:50,079", "taskName": "starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"}
gateway-1  | INFO:     172.18.0.1:43070 - "GET /api/health HTTP/1.1" 200 OK
^C

