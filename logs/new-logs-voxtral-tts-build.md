(.venv-voxtral) ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/providers/voxtral-tts/voxtral-tts$ docker compose down voxtral-tts-provider
[+] down 1/1
 ✔ Container voxtral-tts-provider Removed                                                                                                                               2.5s
(.venv-voxtral) ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/providers/voxtral-tts/voxtral-tts$ git pull
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 4 (delta 3), reused 4 (delta 3), pack-reused 0 (from 0)
Unpacking objects: 100% (4/4), 451 bytes | 451.00 KiB/s, done.
From https://github.com/AetharaAI/voxtral-tts
   81e1596..9b12118  main       -> origin/main
Updating 81e1596..9b12118
Fast-forward
 README.md          | 1 +
 docker-compose.yml | 1 +
 2 files changed, 2 insertions(+)
(.venv-voxtral) ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/providers/voxtral-tts/voxtral-tts$ docker compose up -d --build
[+] Building 0.9s (9/9) FINISHED                                                                                                                                            
 => [internal] load local bake definitions                                                                                                                             0.0s
 => => reading from stdin 644B                                                                                                                                         0.0s
 => [internal] load build definition from Dockerfile                                                                                                                   0.0s
 => => transferring dockerfile: 589B                                                                                                                                   0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04                                                                                0.7s
 => [internal] load .dockerignore                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                        0.0s
 => [1/3] FROM docker.io/nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04@sha256:ac55d124da4882b497f732d8dfd9a702d5447a5f29d08d56da6f64f0a1eb34bc                          0.0s
 => => resolve docker.io/nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04@sha256:ac55d124da4882b497f732d8dfd9a702d5447a5f29d08d56da6f64f0a1eb34bc                          0.0s
 => CACHED [2/3] RUN apt-get update     && apt-get install -y --no-install-recommends         python3         python3-pip         ffmpeg         git     && rm -rf /v  0.0s
 => CACHED [3/3] RUN python3 -m pip install --break-system-packages -U vllm     && python3 -m pip install --break-system-packages "git+https://github.com/vllm-projec  0.0s
 => exporting to image                                                                                                                                                 0.1s
 => => exporting layers                                                                                                                                                0.0s
 => => exporting manifest sha256:dee8257fc99bac6af3aba1e0a1e8010c341c630c95880ea2a54b8adadb0eaa49                                                                      0.0s
 => => exporting config sha256:b28e94a97bbbbc86e455742f0dc48e6bbcc169e2a7782f1e9fbc2b2e507ff1f2                                                                        0.0s
 => => exporting attestation manifest sha256:c891b3288691c72000a56c816940ffc05bdeb49c6ab443ef14f0412098428138                                                          0.0s
 => => exporting manifest list sha256:a0ecb26bef23ec0784088049687d8f4826ebbe2f5c53a0feebd4dc2db821e4a0                                                                 0.0s
 => => naming to docker.io/library/voxtral-tts-voxtral-tts-provider:latest                                                                                             0.0s
 => => unpacking to docker.io/library/voxtral-tts-voxtral-tts-provider:latest                                                                                          0.0s
 => resolving provenance for metadata file                                                                                                                             0.0s
[+] up 2/2
 ✔ Image voxtral-tts-voxtral-tts-provider Built                                                                                                                         1.0s
 ✔ Container voxtral-tts-provider         Created                                                                                                                       0.0s
(.venv-voxtral) ubuntu@l4-360-us-west-or-1:~/aetherpro/voice-x/providers/voxtral-tts/voxtral-tts$ docker compose logs -f voxtral-tts-provider
voxtral-tts-provider  | 
voxtral-tts-provider  | ==========
voxtral-tts-provider  | == CUDA ==
voxtral-tts-provider  | ==========
voxtral-tts-provider  | 
voxtral-tts-provider  | CUDA Version 12.8.1
voxtral-tts-provider  | 
voxtral-tts-provider  | Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
voxtral-tts-provider  | 
voxtral-tts-provider  | This container image and its contents are governed by the NVIDIA Deep Learning Container License.
voxtral-tts-provider  | By pulling and using the container, you accept the terms and conditions of this license:
voxtral-tts-provider  | https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
voxtral-tts-provider  | 
voxtral-tts-provider  | A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
voxtral-tts-provider  | 
voxtral-tts-provider  | /usr/local/lib/python3.12/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
voxtral-tts-provider  |   warnings.warn(
voxtral-tts-provider  | WARNING 03-29 18:56:11 [utils.py:140] To make v1/embeddings API fast, please install orjson by `pip install orjson`
voxtral-tts-provider  | INFO 03-29 18:56:11 [logo.py:45]        █     █     █▄   ▄█       ▄▀▀▀▀▄ █▄   ▄█ █▄    █ ▀█▀ 
voxtral-tts-provider  | INFO 03-29 18:56:11 [logo.py:45]  ▄▄ ▄█ █     █     █ ▀▄▀ █  ▄▄▄  █    █ █ ▀▄▀ █ █ ▀▄  █  █  
voxtral-tts-provider  | INFO 03-29 18:56:11 [logo.py:45]   █▄█▀ █     █     █     █       █    █ █     █ █   ▀▄█  █  
voxtral-tts-provider  | INFO 03-29 18:56:11 [logo.py:45]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀        ▀▀▀▀  ▀     ▀ ▀     ▀ ▀▀▀ 
voxtral-tts-provider  | INFO 03-29 18:56:11 [logo.py:45] 
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [utils.py:297] vLLM server version 0.18.0, serving model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [utils.py:233] non-default args: {'model_tag': '/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', 'host': '0.0.0.0', 'model': '/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', 'enforce_eager': True}
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [omni_base.py:93] [AsyncOmni] Initializing with model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [async_omni_engine.py:216] [AsyncOmniEngine] Initializing with model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [config.py:279] Inferred from consolidated*.safetensors files torch.bfloat16 dtype.
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:11 [utils.py:115] Filtered out 1 callable object(s) from base_engine_args that are not compatible with OmegaConf: ['dispatch_function']. 
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:11 [async_omni_engine.py:248] [AsyncOmniEngine] Launching Orchestrator thread with 2 stages
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:12 [initialization.py:270] Loaded OmniTransferConfig with 1 connector configurations
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:12 [async_omni_engine.py:466] [AsyncOmniEngine] Initializing stage 0
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:12 [stage_init_utils.py:222] [stage_init] Stage-0 set runtime devices: 0
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:12 [async_omni_engine.py:466] [AsyncOmniEngine] Initializing stage 1
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:12 [config.py:338] Config format `mistral` is already registered, and will be overwritten by the new parser class `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>`.
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:12 [config.py:349] Registered config parser `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>` with config format `mistral`
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [model.py:533] Resolved architecture: VoxtralTTSForConditionalGeneration
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [model.py:1582] Using max model len 4096
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:19 [arg_utils.py:2080] This model does not officially support disabling chunked prefill. Disabling this manually may cause the engine to crash or produce incorrect outputs.
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [vllm.py:754] Asynchronous scheduling is enabled.
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [async_omni_engine.py:360] [AsyncOmniEngine] Stage 0 engine launch started
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [stage_init_utils.py:222] [stage_init] Stage-1 set runtime devices: 0
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [model.py:533] Resolved architecture: VoxtralTTSForConditionalGeneration
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [model.py:1582] Using max model len 65536
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=65536.
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [vllm.py:754] Asynchronous scheduling is disabled.
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:19 [vllm.py:788] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:19 [vllm.py:799] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [vllm.py:964] Cudagraph is disabled under eager mode
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:19 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
voxtral-tts-provider  | /usr/local/lib/python3.12/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
voxtral-tts-provider  |   warnings.warn(
voxtral-tts-provider  | WARNING 03-29 18:56:25 [utils.py:140] To make v1/embeddings API fast, please install orjson by `pip install orjson`
voxtral-tts-provider  | WARNING 03-29 18:56:25 [config.py:338] Config format `mistral` is already registered, and will be overwritten by the new parser class `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>`.
voxtral-tts-provider  | INFO 03-29 18:56:25 [config.py:349] Registered config parser `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>` with config format `mistral`
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:25 [core.py:103] Initializing a V1 LLM engine (v0.18.0) with config: model='/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', speculative_config=None, tokenizer='/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', skip_tokenizer_init=False, tokenizer_mode=mistral, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=4096, download_dir=None, load_format=mistral, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603, enable_prefix_caching=False, enable_chunked_prefill=False, pooler_config=None, compilation_config={'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::olmo_hybrid_gdn_full_forward', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 64, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:26 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.22.0.3:57671 backend=nccl
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:26 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:26 [gpu_model_runner.py:4481] Starting to load model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603...
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:27 [vllm.py:754] Asynchronous scheduling is enabled.
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:27 [cuda.py:317] Using FLASH_ATTN attention backend out of potential backends: ['FLASH_ATTN', 'FLASHINFER', 'TRITON_ATTN', 'FLEX_ATTENTION'].
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:27 [flash_attn.py:598] Using FlashAttention version 2
voxtral-tts-provider  | (EngineCore pid=514) <frozen importlib._bootstrap_external>:1297: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
voxtral-tts-provider  | (EngineCore pid=514) <frozen importlib._bootstrap_external>:1297: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
voxtral-tts-provider  | (EngineCore pid=514) WARNING 03-29 18:56:27 [voxtral_tts_audio_tokenizer.py:44] flash_attn is not installed. Falling back to PyTorch SDPA for audio tokenizer attention. Install flash-attn for better performance.
voxtral-tts-provider  | (EngineCore pid=514) WARNING 03-29 18:56:27 [vllm.py:1739] `torch.compile` is turned on, but the model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603 does not support it. Please open an issue on GitHub if you want it to be supported.
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:27 [voxtral_tts.py:140] Available voice embeddings: ['casual_female', 'casual_male', 'cheerful_female', 'neutral_female', 'neutral_male', 'pt_male', 'pt_female', 'nl_male', 'nl_female', 'it_male', 'it_female', 'fr_male', 'fr_female', 'es_male', 'es_female', 'de_male', 'de_female', 'ar_male', 'hi_male', 'hi_female']
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:00<00:00, 153.83it/s]
voxtral-tts-provider  | (EngineCore pid=514) 
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:28 [cuda_graph_acoustic_transformer_wrapper.py:69] CUDAGraphAcousticTransformerWrapper: starting warmup and capture for sizes [1, 2, 4, 8, 16, 32]
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=1
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=2
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=4
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=8
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=16
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:91]   Captured CUDA Graph for batch_size=32
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [cuda_graph_acoustic_transformer_wrapper.py:101] CUDAGraphAcousticTransformerWrapper warmup complete. Captured 6/6 graphs.
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [voxtral_tts.py:177] CUDA Graph for acoustic transformer enabled
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:29 [default_loader.py:384] Loading weights took 1.79 seconds
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:30 [gpu_model_runner.py:4566] Model loading took 7.78 GiB memory and 2.354923 seconds
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:30 [gpu_model_runner.py:5461] Skipping memory profiling for multimodal encoder and encoder cache.
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:33 [backends.py:988] Using cache directory: /root/.cache/vllm/torch_compile_cache/65dc423a29/rank_0_0/backbone for vLLM's torch.compile
voxtral-tts-provider  | (EngineCore pid=514) INFO 03-29 18:56:33 [backends.py:1048] Dynamo bytecode transform time: 3.28 s
voxtral-tts-provider  | (EngineCore pid=514) [rank0]:W0329 18:56:34.715000 514 torch/_inductor/utils.py:1679] Not enough SMs to use max_autotune_gemm mode
voxtral-tts-provider  | (EngineCore pid=514) Process EngineCore:
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099] EngineCore failed to start.
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099] Traceback (most recent call last):
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1073, in run_engine_core
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 839, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     super().__init__(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 122, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     kv_cache_config = self._initialize_kv_caches(vllm_config)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 245, in _initialize_kv_caches
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     available_gpu_memory = self.model_executor.determine_available_memory()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/abstract.py", line 136, in determine_available_memory
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self.collective_rpc("determine_available_memory")
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/uniproc_executor.py", line 78, in collective_rpc
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     result = run_method(self.driver_worker, method, args, kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/serial_utils.py", line 459, in run_method
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_contextlib.py", line 124, in decorate_context
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/worker/base.py", line 107, in determine_available_memory
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.model_runner.profile_run()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/worker/gpu_model_runner.py", line 5516, in profile_run
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     hidden_states, last_hidden_states = self._dummy_run(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                                         ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_contextlib.py", line 124, in decorate_context
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/worker/gpu_model_runner.py", line 808, in _dummy_run
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     outputs = self.model(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]               ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/cuda_graph.py", line 251, in __call__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self.runnable(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self._call_impl(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1787, in _call_impl
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return forward_call(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/model_executor/models/voxtral_tts/voxtral_tts.py", line 250, in forward
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     hidden_states = self.model(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                     ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self._call_impl(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1787, in _call_impl
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return forward_call(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/model_executor/models/voxtral_tts/voxtral_tts_audio_generation.py", line 926, in forward
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     hidden_states = self.language_model.model(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 583, in __call__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.aot_compiled_fn = self.aot_compile(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/wrapper.py", line 168, in aot_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self._compiled_callable.aot_compile((args, kwargs))
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_dynamo/eval_frame.py", line 832, in aot_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return aot_compile_fullgraph(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_dynamo/aot_compile.py", line 239, in aot_compile_fullgraph
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     compiled_fn = backend(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                   ^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/__init__.py", line 2514, in __call__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self.compiler_fn(model_, inputs_, **self.kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/lib/python3.12/contextlib.py", line 81, in inner
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwds)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 1114, in __call__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     PiecewiseCompileInterpreter(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 640, in run
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return super().run(*args)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/fx/interpreter.py", line 200, in run
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.env[node] = self.run_node(node)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                      ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/fx/interpreter.py", line 295, in run_node
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return getattr(self, n.op)(n.target, args, kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 667, in call_module
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     piecewise_backend = PiecewiseBackend(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                         ^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/piecewise_backend.py", line 189, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.compile_all_ranges()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/piecewise_backend.py", line 265, in compile_all_ranges
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     range_entry.runnable = self.vllm_backend.compiler_manager.compile(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 346, in compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     compiled_graph, handle = self.compiler.compile(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                              ^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/compiler_interface.py", line 384, in compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     compiled_graph = standalone_compile(graph, example_inputs, **compile_kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/__init__.py", line 445, in standalone_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return standalone_compile(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/standalone_compile.py", line 423, in standalone_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     compiled_fn = compile_fx(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                   ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2486, in compile_fx
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return compile_fx(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2537, in compile_fx
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return _maybe_wrap_and_compile_fx_main(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2614, in _maybe_wrap_and_compile_fx_main
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return _compile_fx_main(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2823, in _compile_fx_main
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     raise e.remove_dynamo_frames() from None  # see TORCHDYNAMO_VERBOSE=1
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1019, in _compile_fx_inner
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     raise InductorError(e, currentframe()).with_traceback(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1003, in _compile_fx_inner
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     mb_compiled_graph = fx_codegen_and_compile(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                         ^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1766, in fx_codegen_and_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return scheme.codegen_and_compile(gm, example_inputs, inputs_to_check, graph_kwargs)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1537, in codegen_and_compile
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     compiled_module = graph.compile_to_module()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                       ^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2416, in compile_to_module
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self._compile_to_module()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2422, in _compile_to_module
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.codegen_with_cpp_wrapper() if self.cpp_wrapper else self.codegen()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                                                              ^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2354, in codegen
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self._update_scheduler()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2348, in _update_scheduler
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.scheduler = Scheduler(self.operations)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 2765, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self._init(nodes)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 2865, in _init
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.create_combo_kernel_nodes(num_ck_nodes=None)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 4209, in create_combo_kernel_nodes
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     if not self.speedup_by_combo_kernel(node_list):
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 6343, in speedup_by_combo_kernel
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     ms, path = self.benchmark_fused_nodes(node_list)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 3614, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return backend.benchmark_fused_nodes(nodes)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/cuda_combined_scheduling.py", line 144, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return self._triton_scheduling.benchmark_fused_nodes(nodes)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5953, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     src_code = self.generate_kernel_code_from_nodes(nodes, benchmark_kernel=True)
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/simd.py", line 3091, in generate_kernel_code_from_nodes
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     src_code = kernel.codegen_kernel()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                ^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5295, in codegen_kernel
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     **self.inductor_meta_common(),
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5097, in inductor_meta_common
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     "backend_hash": torch.utils._triton.triton_hash_with_backend(),
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_triton.py", line 200, in triton_hash_with_backend
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     backend = triton_backend()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]               ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_triton.py", line 192, in triton_backend
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     target = driver.active.get_current_target()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]              ^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 28, in active
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self._active = self.default
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                    ^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 22, in default
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self._default = _create_driver()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                     ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 10, in _create_driver
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     return active_drivers[0]()
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/driver.py", line 720, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     self.utils = CudaUtils()  # TODO: make static
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]                  ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/driver.py", line 62, in __init__
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     mod = compile_module_from_src(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]           ^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/build.py", line 93, in compile_module_from_src
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     so = _build(name, src_path, tmpdir, library_dirs or [], include_dirs or [], libraries or [], ccflags or [])
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/build.py", line 32, in _build
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099]     raise RuntimeError(
voxtral-tts-provider  | (EngineCore pid=514) ERROR 03-29 18:56:34 [core.py:1099] torch._inductor.exc.InductorError: RuntimeError: Failed to find C compiler. Please specify via CC environment variable or set triton.knobs.build.impl.
voxtral-tts-provider  | (EngineCore pid=514) Traceback (most recent call last):
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
voxtral-tts-provider  | (EngineCore pid=514)     self.run()
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
voxtral-tts-provider  | (EngineCore pid=514)     self._target(*self._args, **self._kwargs)
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1103, in run_engine_core
voxtral-tts-provider  | (EngineCore pid=514)     raise e
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1073, in run_engine_core
voxtral-tts-provider  | (EngineCore pid=514)     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 839, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     super().__init__(
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 122, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     kv_cache_config = self._initialize_kv_caches(vllm_config)
voxtral-tts-provider  | (EngineCore pid=514)                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 245, in _initialize_kv_caches
voxtral-tts-provider  | (EngineCore pid=514)     available_gpu_memory = self.model_executor.determine_available_memory()
voxtral-tts-provider  | (EngineCore pid=514)                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/abstract.py", line 136, in determine_available_memory
voxtral-tts-provider  | (EngineCore pid=514)     return self.collective_rpc("determine_available_memory")
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/uniproc_executor.py", line 78, in collective_rpc
voxtral-tts-provider  | (EngineCore pid=514)     result = run_method(self.driver_worker, method, args, kwargs)
voxtral-tts-provider  | (EngineCore pid=514)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/serial_utils.py", line 459, in run_method
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_contextlib.py", line 124, in decorate_context
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/worker/base.py", line 107, in determine_available_memory
voxtral-tts-provider  | (EngineCore pid=514)     self.model_runner.profile_run()
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/worker/gpu_model_runner.py", line 5516, in profile_run
voxtral-tts-provider  | (EngineCore pid=514)     hidden_states, last_hidden_states = self._dummy_run(
voxtral-tts-provider  | (EngineCore pid=514)                                         ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_contextlib.py", line 124, in decorate_context
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/worker/gpu_model_runner.py", line 808, in _dummy_run
voxtral-tts-provider  | (EngineCore pid=514)     outputs = self.model(
voxtral-tts-provider  | (EngineCore pid=514)               ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/cuda_graph.py", line 251, in __call__
voxtral-tts-provider  | (EngineCore pid=514)     return self.runnable(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
voxtral-tts-provider  | (EngineCore pid=514)     return self._call_impl(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1787, in _call_impl
voxtral-tts-provider  | (EngineCore pid=514)     return forward_call(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/model_executor/models/voxtral_tts/voxtral_tts.py", line 250, in forward
voxtral-tts-provider  | (EngineCore pid=514)     hidden_states = self.model(
voxtral-tts-provider  | (EngineCore pid=514)                     ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
voxtral-tts-provider  | (EngineCore pid=514)     return self._call_impl(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/nn/modules/module.py", line 1787, in _call_impl
voxtral-tts-provider  | (EngineCore pid=514)     return forward_call(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/model_executor/models/voxtral_tts/voxtral_tts_audio_generation.py", line 926, in forward
voxtral-tts-provider  | (EngineCore pid=514)     hidden_states = self.language_model.model(
voxtral-tts-provider  | (EngineCore pid=514)                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 583, in __call__
voxtral-tts-provider  | (EngineCore pid=514)     self.aot_compiled_fn = self.aot_compile(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/wrapper.py", line 168, in aot_compile
voxtral-tts-provider  | (EngineCore pid=514)     return self._compiled_callable.aot_compile((args, kwargs))
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_dynamo/eval_frame.py", line 832, in aot_compile
voxtral-tts-provider  | (EngineCore pid=514)     return aot_compile_fullgraph(
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_dynamo/aot_compile.py", line 239, in aot_compile_fullgraph
voxtral-tts-provider  | (EngineCore pid=514)     compiled_fn = backend(
voxtral-tts-provider  | (EngineCore pid=514)                   ^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/__init__.py", line 2514, in __call__
voxtral-tts-provider  | (EngineCore pid=514)     return self.compiler_fn(model_, inputs_, **self.kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/lib/python3.12/contextlib.py", line 81, in inner
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwds)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 1114, in __call__
voxtral-tts-provider  | (EngineCore pid=514)     PiecewiseCompileInterpreter(
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 640, in run
voxtral-tts-provider  | (EngineCore pid=514)     return super().run(*args)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/fx/interpreter.py", line 200, in run
voxtral-tts-provider  | (EngineCore pid=514)     self.env[node] = self.run_node(node)
voxtral-tts-provider  | (EngineCore pid=514)                      ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/fx/interpreter.py", line 295, in run_node
voxtral-tts-provider  | (EngineCore pid=514)     return getattr(self, n.op)(n.target, args, kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 667, in call_module
voxtral-tts-provider  | (EngineCore pid=514)     piecewise_backend = PiecewiseBackend(
voxtral-tts-provider  | (EngineCore pid=514)                         ^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/piecewise_backend.py", line 189, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     self.compile_all_ranges()
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/piecewise_backend.py", line 265, in compile_all_ranges
voxtral-tts-provider  | (EngineCore pid=514)     range_entry.runnable = self.vllm_backend.compiler_manager.compile(
voxtral-tts-provider  | (EngineCore pid=514)                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
voxtral-tts-provider  | (EngineCore pid=514)     return func(*args, **kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/backends.py", line 346, in compile
voxtral-tts-provider  | (EngineCore pid=514)     compiled_graph, handle = self.compiler.compile(
voxtral-tts-provider  | (EngineCore pid=514)                              ^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/compiler_interface.py", line 384, in compile
voxtral-tts-provider  | (EngineCore pid=514)     compiled_graph = standalone_compile(graph, example_inputs, **compile_kwargs)
voxtral-tts-provider  | (EngineCore pid=514)                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/__init__.py", line 445, in standalone_compile
voxtral-tts-provider  | (EngineCore pid=514)     return standalone_compile(
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/standalone_compile.py", line 423, in standalone_compile
voxtral-tts-provider  | (EngineCore pid=514)     compiled_fn = compile_fx(
voxtral-tts-provider  | (EngineCore pid=514)                   ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2486, in compile_fx
voxtral-tts-provider  | (EngineCore pid=514)     return compile_fx(
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2537, in compile_fx
voxtral-tts-provider  | (EngineCore pid=514)     return _maybe_wrap_and_compile_fx_main(
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2614, in _maybe_wrap_and_compile_fx_main
voxtral-tts-provider  | (EngineCore pid=514)     return _compile_fx_main(
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 2823, in _compile_fx_main
voxtral-tts-provider  | (EngineCore pid=514)     raise e.remove_dynamo_frames() from None  # see TORCHDYNAMO_VERBOSE=1
voxtral-tts-provider  | (EngineCore pid=514)     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1019, in _compile_fx_inner
voxtral-tts-provider  | (EngineCore pid=514)     raise InductorError(e, currentframe()).with_traceback(
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1003, in _compile_fx_inner
voxtral-tts-provider  | (EngineCore pid=514)     mb_compiled_graph = fx_codegen_and_compile(
voxtral-tts-provider  | (EngineCore pid=514)                         ^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1766, in fx_codegen_and_compile
voxtral-tts-provider  | (EngineCore pid=514)     return scheme.codegen_and_compile(gm, example_inputs, inputs_to_check, graph_kwargs)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/compile_fx.py", line 1537, in codegen_and_compile
voxtral-tts-provider  | (EngineCore pid=514)     compiled_module = graph.compile_to_module()
voxtral-tts-provider  | (EngineCore pid=514)                       ^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2416, in compile_to_module
voxtral-tts-provider  | (EngineCore pid=514)     return self._compile_to_module()
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2422, in _compile_to_module
voxtral-tts-provider  | (EngineCore pid=514)     self.codegen_with_cpp_wrapper() if self.cpp_wrapper else self.codegen()
voxtral-tts-provider  | (EngineCore pid=514)                                                              ^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2354, in codegen
voxtral-tts-provider  | (EngineCore pid=514)     self._update_scheduler()
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/graph.py", line 2348, in _update_scheduler
voxtral-tts-provider  | (EngineCore pid=514)     self.scheduler = Scheduler(self.operations)
voxtral-tts-provider  | (EngineCore pid=514)                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 2765, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     self._init(nodes)
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 2865, in _init
voxtral-tts-provider  | (EngineCore pid=514)     self.create_combo_kernel_nodes(num_ck_nodes=None)
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 4209, in create_combo_kernel_nodes
voxtral-tts-provider  | (EngineCore pid=514)     if not self.speedup_by_combo_kernel(node_list):
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 6343, in speedup_by_combo_kernel
voxtral-tts-provider  | (EngineCore pid=514)     ms, path = self.benchmark_fused_nodes(node_list)
voxtral-tts-provider  | (EngineCore pid=514)                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/scheduler.py", line 3614, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514)     return backend.benchmark_fused_nodes(nodes)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/cuda_combined_scheduling.py", line 144, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514)     return self._triton_scheduling.benchmark_fused_nodes(nodes)
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5953, in benchmark_fused_nodes
voxtral-tts-provider  | (EngineCore pid=514)     src_code = self.generate_kernel_code_from_nodes(nodes, benchmark_kernel=True)
voxtral-tts-provider  | (EngineCore pid=514)                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/simd.py", line 3091, in generate_kernel_code_from_nodes
voxtral-tts-provider  | (EngineCore pid=514)     src_code = kernel.codegen_kernel()
voxtral-tts-provider  | (EngineCore pid=514)                ^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5295, in codegen_kernel
voxtral-tts-provider  | (EngineCore pid=514)     **self.inductor_meta_common(),
voxtral-tts-provider  | (EngineCore pid=514)       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/_inductor/codegen/triton.py", line 5097, in inductor_meta_common
voxtral-tts-provider  | (EngineCore pid=514)     "backend_hash": torch.utils._triton.triton_hash_with_backend(),
voxtral-tts-provider  | (EngineCore pid=514)                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_triton.py", line 200, in triton_hash_with_backend
voxtral-tts-provider  | (EngineCore pid=514)     backend = triton_backend()
voxtral-tts-provider  | (EngineCore pid=514)               ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_triton.py", line 192, in triton_backend
voxtral-tts-provider  | (EngineCore pid=514)     target = driver.active.get_current_target()
voxtral-tts-provider  | (EngineCore pid=514)              ^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 28, in active
voxtral-tts-provider  | (EngineCore pid=514)     self._active = self.default
voxtral-tts-provider  | (EngineCore pid=514)                    ^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 22, in default
voxtral-tts-provider  | (EngineCore pid=514)     self._default = _create_driver()
voxtral-tts-provider  | (EngineCore pid=514)                     ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 10, in _create_driver
voxtral-tts-provider  | (EngineCore pid=514)     return active_drivers[0]()
voxtral-tts-provider  | (EngineCore pid=514)            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/driver.py", line 720, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     self.utils = CudaUtils()  # TODO: make static
voxtral-tts-provider  | (EngineCore pid=514)                  ^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/driver.py", line 62, in __init__
voxtral-tts-provider  | (EngineCore pid=514)     mod = compile_module_from_src(
voxtral-tts-provider  | (EngineCore pid=514)           ^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/build.py", line 93, in compile_module_from_src
voxtral-tts-provider  | (EngineCore pid=514)     so = _build(name, src_path, tmpdir, library_dirs or [], include_dirs or [], libraries or [], ccflags or [])
voxtral-tts-provider  | (EngineCore pid=514)          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (EngineCore pid=514)   File "/usr/local/lib/python3.12/dist-packages/triton/runtime/build.py", line 32, in _build
voxtral-tts-provider  | (EngineCore pid=514)     raise RuntimeError(
voxtral-tts-provider  | (EngineCore pid=514) torch._inductor.exc.InductorError: RuntimeError: Failed to find C compiler. Please specify via CC environment variable or set triton.knobs.build.impl.
voxtral-tts-provider  | [rank0]:[W329 18:56:35.322655508 ProcessGroupNCCL.cpp:1553] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:36 [stage_init_utils.py:475] [stage_init] Failed to close launched engine manager for stage 0: 'CoreEngineProcManager' object has no attribute 'close'
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:36 [async_omni_engine.py:360] [AsyncOmniEngine] Stage 1 engine launch started
voxtral-tts-provider  | /usr/local/lib/python3.12/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
voxtral-tts-provider  |   warnings.warn(
voxtral-tts-provider  | WARNING 03-29 18:56:43 [utils.py:140] To make v1/embeddings API fast, please install orjson by `pip install orjson`
voxtral-tts-provider  | WARNING 03-29 18:56:43 [config.py:338] Config format `mistral` is already registered, and will be overwritten by the new parser class `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>`.
voxtral-tts-provider  | INFO 03-29 18:56:43 [config.py:349] Registered config parser `<class 'vllm_omni.model_executor.models.voxtral_tts.configuration_voxtral_tts.VoxtralTTSConfigParser'>` with config format `mistral`
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:43 [core.py:103] Initializing a V1 LLM engine (v0.18.0) with config: model='/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', speculative_config=None, tokenizer='/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603', skip_tokenizer_init=False, tokenizer_mode=mistral, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=65536, download_dir=None, load_format=mistral, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=None, enforce_eager=True, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603, enable_prefix_caching=False, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['all'], 'splitting_ops': [], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [65536], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 0, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:44 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.22.0.3:40201 backend=nccl
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:44 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [gpu_model_runner.py:4481] Starting to load model /mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603...
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [vllm.py:754] Asynchronous scheduling is disabled.
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:45 [vllm.py:788] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:45 [vllm.py:799] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [vllm.py:964] Cudagraph is disabled under eager mode
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:45 [voxtral_tts_audio_tokenizer.py:44] flash_attn is not installed. Falling back to PyTorch SDPA for audio tokenizer attention. Install flash-attn for better performance.
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:00<00:00,  9.96it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:00<00:00,  9.94it/s]
voxtral-tts-provider  | (EngineCore pid=884) 
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [default_loader.py:384] Loading weights took 0.10 seconds
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:45 [gpu_model_runner.py:4566] Model loading took 0.61 GiB memory and 0.156058 seconds
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [voxtral_tts.py:260] audio_tokenizer: sample run with dummy input
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [voxtral_tts_audio_tokenizer.py:1102] Min value of decoded waveform signal is tensor(-3.5625)
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [voxtral_tts_audio_tokenizer.py:1104] Max value of decoded waveform signal is tensor(3.4844)
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [gpu_generation_model_runner.py:464] Dummy sampler run is not implemented for generation model
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [core.py:281] init engine (profile, create kv cache, warmup model) took 0.42 seconds
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [scheduler.py:173] Using custom scheduler class vllm_omni.core.sched.omni_generation_scheduler.OmniGenerationScheduler. This scheduler interface is not public and compatibility may not be maintained.
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [core.py:132] Disabling chunked prefill for model without KVCache
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [factory.py:46] Created connector: SharedMemoryConnector
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [vllm.py:788] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
voxtral-tts-provider  | (EngineCore pid=884) WARNING 03-29 18:56:46 [vllm.py:799] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [vllm.py:964] Cudagraph is disabled under eager mode
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:46 [async_omni_engine.py:362] [AsyncOmniEngine] Stage 1 engine startup completed
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542] [AsyncOmniEngine] Stage initialization failed; shutting down 0 initialized stage(s)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542] Traceback (most recent call last):
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 522, in _initialize_stages
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     started_llm_stages[stage_id] = llm_launch_futures[stage_id].result()
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 449, in result
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     return self.__get_result()
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     raise self._exception
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     result = self.fn(*self.args, **self.kwargs)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 361, in _launch_llm_stage
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     launch_cm.__exit__(None, None, None)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     next(self.gen)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 972, in launch_core_engines
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     wait_for_engine_startup(
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1031, in wait_for_engine_startup
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542]     raise RuntimeError(
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:542] RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
voxtral-tts-provider  | (APIServer pid=1) WARNING 03-29 18:56:46 [stage_init_utils.py:475] [stage_init] Failed to close launched engine manager for stage 1: 'CoreEngineProcManager' object has no attribute 'close'
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607] [AsyncOmniEngine] Orchestrator thread crashed
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607] Traceback (most recent call last):
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 603, in _bootstrap_orchestrator
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     loop.run_until_complete(_run_orchestrator())
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/lib/python3.12/asyncio/base_events.py", line 687, in run_until_complete
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     return future.result()
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]            ^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 588, in _run_orchestrator
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     self._initialize_stages(stage_init_timeout)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 522, in _initialize_stages
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     started_llm_stages[stage_id] = llm_launch_futures[stage_id].result()
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 449, in result
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     return self.__get_result()
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     raise self._exception
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     result = self.fn(*self.args, **self.kwargs)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 361, in _launch_llm_stage
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     launch_cm.__exit__(None, None, None)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     next(self.gen)
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 972, in launch_core_engines
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     wait_for_engine_startup(
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1031, in wait_for_engine_startup
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607]     raise RuntimeError(
voxtral-tts-provider  | (APIServer pid=1) ERROR 03-29 18:56:46 [async_omni_engine.py:607] RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
voxtral-tts-provider  | (APIServer pid=1) INFO 03-29 18:56:46 [async_omni_engine.py:1133] [AsyncOmniEngine] Shutting down Orchestrator
voxtral-tts-provider  | (APIServer pid=1) Exception in thread orchestrator:
voxtral-tts-provider  | (APIServer pid=1) Traceback (most recent call last):
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/threading.py", line 1073, in _bootstrap_inner
voxtral-tts-provider  | (APIServer pid=1)     self.run()
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/threading.py", line 1010, in run
voxtral-tts-provider  | (APIServer pid=1)     self._target(*self._args, **self._kwargs)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 603, in _bootstrap_orchestrator
voxtral-tts-provider  | (APIServer pid=1)     loop.run_until_complete(_run_orchestrator())
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/base_events.py", line 687, in run_until_complete
voxtral-tts-provider  | (APIServer pid=1)     return future.result()
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 588, in _run_orchestrator
voxtral-tts-provider  | (APIServer pid=1)     self._initialize_stages(stage_init_timeout)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 522, in _initialize_stages
voxtral-tts-provider  | (APIServer pid=1)     started_llm_stages[stage_id] = llm_launch_futures[stage_id].result()
voxtral-tts-provider  | (APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 449, in result
voxtral-tts-provider  | (APIServer pid=1)     return self.__get_result()
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
voxtral-tts-provider  | (APIServer pid=1)     raise self._exception
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
voxtral-tts-provider  | (APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
voxtral-tts-provider  | (APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 361, in _launch_llm_stage
voxtral-tts-provider  | (APIServer pid=1)     launch_cm.__exit__(None, None, None)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
voxtral-tts-provider  | (APIServer pid=1)     next(self.gen)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 972, in launch_core_engines
voxtral-tts-provider  | (APIServer pid=1)     wait_for_engine_startup(
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1031, in wait_for_engine_startup
voxtral-tts-provider  | (APIServer pid=1)     raise RuntimeError(
voxtral-tts-provider  | (APIServer pid=1) RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
voxtral-tts-provider  | (APIServer pid=1) Traceback (most recent call last):
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/bin/vllm", line 8, in <module>
voxtral-tts-provider  | (APIServer pid=1)     sys.exit(main())
voxtral-tts-provider  | (APIServer pid=1)              ^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/cli/main.py", line 53, in main
voxtral-tts-provider  | (APIServer pid=1)     args.dispatch_function(args)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/cli/serve.py", line 63, in cmd
voxtral-tts-provider  | (APIServer pid=1)     uvloop.run(omni_run_server(args))
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 96, in run
voxtral-tts-provider  | (APIServer pid=1)     return __asyncio.run(
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
voxtral-tts-provider  | (APIServer pid=1)     return runner.run(main)
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
voxtral-tts-provider  | (APIServer pid=1)     return self._loop.run_until_complete(task)
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 48, in wrapper
voxtral-tts-provider  | (APIServer pid=1)     return await main
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/openai/api_server.py", line 266, in omni_run_server
voxtral-tts-provider  | (APIServer pid=1)     await omni_run_server_worker(listen_address, sock, args, **uvicorn_kwargs)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/openai/api_server.py", line 284, in omni_run_server_worker
voxtral-tts-provider  | (APIServer pid=1)     async with build_async_omni(
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
voxtral-tts-provider  | (APIServer pid=1)     return await anext(self.gen)
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/openai/api_server.py", line 390, in build_async_omni
voxtral-tts-provider  | (APIServer pid=1)     async with build_async_omni_from_stage_config(
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
voxtral-tts-provider  | (APIServer pid=1)     return await anext(self.gen)
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/openai/api_server.py", line 430, in build_async_omni_from_stage_config
voxtral-tts-provider  | (APIServer pid=1)     async_omni = AsyncOmni(model=args.model, **kwargs)
voxtral-tts-provider  | (APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/async_omni.py", line 71, in __init__
voxtral-tts-provider  | (APIServer pid=1)     OmniBase.__init__(self, model=model, **kwargs)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/entrypoints/omni_base.py", line 95, in __init__
voxtral-tts-provider  | (APIServer pid=1)     self.engine = AsyncOmniEngine(
voxtral-tts-provider  | (APIServer pid=1)                   ^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm_omni/engine/async_omni_engine.py", line 266, in __init__
voxtral-tts-provider  | (APIServer pid=1)     startup_future.result(timeout=startup_timeout)
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 456, in result
voxtral-tts-provider  | (APIServer pid=1)     return self.__get_result()
voxtral-tts-provider  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^
voxtral-tts-provider  | (APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
voxtral-tts-provider  | (APIServer pid=1)     raise self._exception
voxtral-tts-provider  | (APIServer pid=1) RuntimeError: Orchestrator initialization failed: Engine core initialization failed. See root cause above. Failed core proc(s): {}
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [core.py:1201] Shutdown initiated (timeout=0)
voxtral-tts-provider  | (EngineCore pid=884) INFO 03-29 18:56:46 [core.py:1224] Shutdown complete
voxtral-tts-provider  | [rank0]:[W329 18:56:46.341869905 ProcessGroupNCCL.cpp:1553] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
^C

