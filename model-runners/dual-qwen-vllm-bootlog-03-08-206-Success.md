ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/dual-qwen$ docker compose logs -f
qwen3.5-4b  | /usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/chat_completion/protocol.py:346: SyntaxWarning: invalid escape sequence '\e'
qwen3.5-4b  |   "(e.g. 'abcdabcdabcd...' or '\emoji \emoji \emoji ...'). This feature "
qwen3.5-9b  | /usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/chat_completion/protocol.py:346: SyntaxWarning: invalid escape sequence '\e'
qwen3.5-9b  |   "(e.g. 'abcdabcdabcd...' or '\emoji \emoji \emoji ...'). This feature "
qwen3.5-4b  | /usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/completion/protocol.py:176: SyntaxWarning: invalid escape sequence '\e'
qwen3.5-4b  |   "(e.g. 'abcdabcdabcd...' or '\emoji \emoji \emoji ...'). This feature "
qwen3.5-9b  | /usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/completion/protocol.py:176: SyntaxWarning: invalid escape sequence '\e'
qwen3.5-9b  |   "(e.g. 'abcdabcdabcd...' or '\emoji \emoji \emoji ...'). This feature "
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302] 
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]        █     █     █▄   ▄█
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.16.1rc1.dev265+gd106bf39f
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]   █▄█▀ █     █     █     █  model   /models/cyankiwi/Qwen3.5-4B-AWQ-4bit
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302] 
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:238] non-default args: {'model_tag': '/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', 'max_model_len': 16384, 'served_model_name': ['qwen3.5-4b'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'gpu_memory_utilization': 0.3, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 4096, 'max_num_seqs': 8, 'enable_chunked_prefill': True}
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302] 
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]        █     █     █▄   ▄█
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.16.1rc1.dev265+gd106bf39f
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]   █▄█▀ █     █     █     █  model   /models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:302] 
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:16 [utils.py:238] non-default args: {'model_tag': '/models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8', 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8', 'max_model_len': 16384, 'served_model_name': ['qwen3.5-9b'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'gpu_memory_utilization': 0.48, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 4096, 'max_num_seqs': 8, 'enable_chunked_prefill': True}
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:22 [model.py:530] Resolved architecture: Qwen3_5ForConditionalGeneration
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:22 [model.py:1553] Using max model len 16384
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:22 [model.py:530] Resolved architecture: Qwen3_5ForConditionalGeneration
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:22 [model.py:1553] Using max model len 16384
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:22 [cache.py:223] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [cache.py:223] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:23 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=4096.
qwen3.5-4b  | (APIServer pid=1) WARNING 03-09 12:54:23 [config.py:392] Mamba cache mode is set to 'align' for Qwen3_5ForConditionalGeneration by default when prefix caching is enabled
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:412] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=4096.
qwen3.5-9b  | (APIServer pid=1) WARNING 03-09 12:54:23 [config.py:392] Mamba cache mode is set to 'align' for Qwen3_5ForConditionalGeneration by default when prefix caching is enabled
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:412] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:232] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:263] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:54:23 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:232] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [config.py:263] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:54:23 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:34 [core.py:101] Initializing a V1 LLM engine (v0.16.1rc1.dev265+gd106bf39f) with config: model='/models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8', speculative_config=None, tokenizer='/models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=qwen3.5-9b, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [4096], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 16, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:34 [core.py:101] Initializing a V1 LLM engine (v0.16.1rc1.dev265+gd106bf39f) with config: model='/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', speculative_config=None, tokenizer='/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=qwen3.5-4b, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [4096], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 16, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:35 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.2:47131 backend=nccl
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:35 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:35 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.5:60373 backend=nccl
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:35 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [gpu_model_runner.py:4261] Starting to load model /models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8...
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [gpu_model_runner.py:4261] Starting to load model /models/cyankiwi/Qwen3.5-4B-AWQ-4bit...
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [cuda.py:453] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [mm_encoder_attention.py:215] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [cuda.py:453] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [mm_encoder_attention.py:215] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:40 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:41 [cuda.py:405] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:41 [cuda.py:405] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
qwen3.5-9b  | (EngineCore_DP0 pid=132) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
qwen3.5-9b  | (EngineCore_DP0 pid=132) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
qwen3.5-4b  | (EngineCore_DP0 pid=132) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
qwen3.5-4b  | (EngineCore_DP0 pid=132) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
Loading safetensors checkpoint shards:   0% Completed | 0/3 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  33% Completed | 1/3 [00:01<00:03,  1.89s/it]
Loading safetensors checkpoint shards:  67% Completed | 2/3 [00:03<00:01,  1.92s/it]
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:04<00:00,  1.39s/it]
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:04<00:00,  1.53s/it]
qwen3.5-9b  | (EngineCore_DP0 pid=132) 
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:46 [default_loader.py:293] Loading weights took 4.71 seconds
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:47 [gpu_model_runner.py:4344] Model loading took 13.04 GiB memory and 5.444196 seconds
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:47 [gpu_model_runner.py:5260] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:57 [backends.py:913] Using cache directory: /root/.cache/vllm/torch_compile_cache/f2458f04dc/rank_0_0/backbone for vLLM's torch.compile
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:54:57 [backends.py:973] Dynamo bytecode transform time: 5.72 s
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:00 [backends.py:370] Cache the graph of compile range (1, 4096) for later use
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:17 [backends.py:386] Compiling a graph for compile range (1, 4096) takes 20.06 s
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:19 [decorators.py:592] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/e7e5c7d53bf47372b98c17a52c2df46e1ae1a0c753e840fbdc46141c07b5ae4b/rank_0_0/model
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:21 [monitor.py:35] torch.compile and initial profiling run took 29.93 s in total
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:28 [gpu_worker.py:424] Available KV cache memory: 2.43 GiB
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:28 [kv_cache_utils.py:1314] GPU KV cache size: 39,072 tokens
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:28 [kv_cache_utils.py:1319] Maximum concurrency for 16,384 tokens per request: 6.82x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 5/5 [00:00<00:00, 27.72it/s]
Capturing CUDA graphs (decode, FULL): 100%|██████████| 4/4 [00:01<00:00,  2.01it/s]
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:31 [gpu_model_runner.py:5366] Graph capturing finished in 3 secs, took 0.51 GiB
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:31 [core.py:282] init engine (profile, create kv cache, warmup model) took 44.67 seconds
qwen3.5-9b  | (EngineCore_DP0 pid=132) INFO 03-09 12:55:32 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:32 [api_server.py:491] Supported tasks: ['generate']
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:32 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:32 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:32 [serving.py:185] Warming up chat template processing...
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [hf.py:318] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [serving.py:210] Chat template warmup completed in 1120.4ms
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [api_server.py:496] Starting vLLM server on http://0.0.0.0:8000
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:38] Available routes are:
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /openapi.json, Methods: HEAD, GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /docs, Methods: HEAD, GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /docs/oauth2-redirect, Methods: HEAD, GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /redoc, Methods: HEAD, GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /tokenize, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /detokenize, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /load, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /version, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /health, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /metrics, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/models, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /ping, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /ping, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /invocations, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/chat/completions, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/chat/completions/render, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/responses, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/responses/{response_id}, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/responses/{response_id}/cancel, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/completions, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/completions/render, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/messages, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /v1/messages/count_tokens, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /inference/v1/generate, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /scale_elastic_ep, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-09 12:55:33 [launcher.py:47] Route: /is_scaling_elastic_ep, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO:     Started server process [1]
qwen3.5-9b  | (APIServer pid=1) INFO:     Waiting for application startup.
qwen3.5-9b  | (APIServer pid=1) INFO:     Application startup complete.
Loading safetensors checkpoint shards: 100% Completed | 1/1 [01:19<00:00, 79.24s/it]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [01:19<00:00, 79.24s/it]
qwen3.5-4b  | (EngineCore_DP0 pid=132) 
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:00 [default_loader.py:293] Loading weights took 79.39 seconds
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:01 [gpu_model_runner.py:4344] Model loading took 3.85 GiB memory and 80.081264 seconds
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:01 [gpu_model_runner.py:5260] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:11 [backends.py:913] Using cache directory: /root/.cache/vllm/torch_compile_cache/3a332b42ba/rank_0_0/backbone for vLLM's torch.compile
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:11 [backends.py:973] Dynamo bytecode transform time: 6.29 s
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:15 [backends.py:370] Cache the graph of compile range (1, 4096) for later use
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:33 [backends.py:386] Compiling a graph for compile range (1, 4096) takes 21.81 s
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:35 [decorators.py:592] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/8eb57c07a0cb28e25c05fe4f6a26f79c17d1dbab45c8135a7f283823486c9a3d/rank_0_0/model
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:37 [monitor.py:35] torch.compile and initial profiling run took 32.00 s in total
qwen3.5-4b  | (EngineCore_DP0 pid=132) INFO 03-09 12:56:44 [gpu_worker.py:424] Available KV cache memory: -8.59 GiB
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100] EngineCore failed to start.
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100] Traceback (most recent call last):
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1090, in run_engine_core
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     return func(*args, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 834, in __init__
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     super().__init__(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 120, in __init__
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     num_gpu_blocks, num_cpu_blocks, kv_cache_config = self._initialize_kv_caches(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     return func(*args, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 263, in _initialize_kv_caches
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     kv_cache_configs = get_kv_cache_configs(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]                        ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/core/kv_cache_utils.py", line 1572, in get_kv_cache_configs
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     _check_enough_kv_cache_memory(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/core/kv_cache_utils.py", line 623, in _check_enough_kv_cache_memory
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100]     raise ValueError(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ERROR 03-09 12:56:44 [core.py:1100] ValueError: No available memory for the cache blocks. Try increasing `gpu_memory_utilization` when initializing the engine. See https://docs.vllm.ai/en/latest/configuration/conserving_memory/ for more details.
qwen3.5-4b  | (EngineCore_DP0 pid=132) Process EngineCore_DP0:
qwen3.5-4b  | (EngineCore_DP0 pid=132) Traceback (most recent call last):
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
qwen3.5-4b  | (EngineCore_DP0 pid=132)     self.run()
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
qwen3.5-4b  | (EngineCore_DP0 pid=132)     self._target(*self._args, **self._kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1104, in run_engine_core
qwen3.5-4b  | (EngineCore_DP0 pid=132)     raise e
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1090, in run_engine_core
qwen3.5-4b  | (EngineCore_DP0 pid=132)     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132)                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (EngineCore_DP0 pid=132)     return func(*args, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 834, in __init__
qwen3.5-4b  | (EngineCore_DP0 pid=132)     super().__init__(
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 120, in __init__
qwen3.5-4b  | (EngineCore_DP0 pid=132)     num_gpu_blocks, num_cpu_blocks, kv_cache_config = self._initialize_kv_caches(
qwen3.5-4b  | (EngineCore_DP0 pid=132)                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (EngineCore_DP0 pid=132)     return func(*args, **kwargs)
qwen3.5-4b  | (EngineCore_DP0 pid=132)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 263, in _initialize_kv_caches
qwen3.5-4b  | (EngineCore_DP0 pid=132)     kv_cache_configs = get_kv_cache_configs(
qwen3.5-4b  | (EngineCore_DP0 pid=132)                        ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/core/kv_cache_utils.py", line 1572, in get_kv_cache_configs
qwen3.5-4b  | (EngineCore_DP0 pid=132)     _check_enough_kv_cache_memory(
qwen3.5-4b  | (EngineCore_DP0 pid=132)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/core/kv_cache_utils.py", line 623, in _check_enough_kv_cache_memory
qwen3.5-4b  | (EngineCore_DP0 pid=132)     raise ValueError(
qwen3.5-4b  | (EngineCore_DP0 pid=132) ValueError: No available memory for the cache blocks. Try increasing `gpu_memory_utilization` when initializing the engine. See https://docs.vllm.ai/en/latest/configuration/conserving_memory/ for more details.
qwen3.5-4b  | [rank0]:[W309 12:56:45.480623726 ProcessGroupNCCL.cpp:1553] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
qwen3.5-4b  | (APIServer pid=1) Traceback (most recent call last):
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/bin/vllm", line 10, in <module>
qwen3.5-4b  | (APIServer pid=1)     sys.exit(main())
qwen3.5-4b  | (APIServer pid=1)              ^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/cli/main.py", line 75, in main
qwen3.5-4b  | (APIServer pid=1)     args.dispatch_function(args)
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/cli/serve.py", line 112, in cmd
qwen3.5-4b  | (APIServer pid=1)     uvloop.run(run_server(args))
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 96, in run
qwen3.5-4b  | (APIServer pid=1)     return __asyncio.run(
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 195, in run
qwen3.5-4b  | (APIServer pid=1)     return runner.run(main)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
qwen3.5-4b  | (APIServer pid=1)     return self._loop.run_until_complete(task)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 48, in wrapper
qwen3.5-4b  | (APIServer pid=1)     return await main
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 527, in run_server
qwen3.5-4b  | (APIServer pid=1)     await run_server_worker(listen_address, sock, args, **uvicorn_kwargs)
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 541, in run_server_worker
qwen3.5-4b  | (APIServer pid=1)     async with build_async_engine_client(
qwen3.5-4b  | (APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
qwen3.5-4b  | (APIServer pid=1)     return await anext(self.gen)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 97, in build_async_engine_client
qwen3.5-4b  | (APIServer pid=1)     async with build_async_engine_client_from_engine_args(
qwen3.5-4b  | (APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
qwen3.5-4b  | (APIServer pid=1)     return await anext(self.gen)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 138, in build_async_engine_client_from_engine_args
qwen3.5-4b  | (APIServer pid=1)     async_llm = AsyncLLM.from_vllm_config(
qwen3.5-4b  | (APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 225, in from_vllm_config
qwen3.5-4b  | (APIServer pid=1)     return cls(
qwen3.5-4b  | (APIServer pid=1)            ^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 154, in __init__
qwen3.5-4b  | (APIServer pid=1)     self.engine_core = EngineCoreClient.make_async_mp_client(
qwen3.5-4b  | (APIServer pid=1)                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (APIServer pid=1)     return func(*args, **kwargs)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 127, in make_async_mp_client
qwen3.5-4b  | (APIServer pid=1)     return AsyncMPClient(*client_args)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
qwen3.5-4b  | (APIServer pid=1)     return func(*args, **kwargs)
qwen3.5-4b  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 911, in __init__
qwen3.5-4b  | (APIServer pid=1)     super().__init__(
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 569, in __init__
qwen3.5-4b  | (APIServer pid=1)     with launch_core_engines(
qwen3.5-4b  | (APIServer pid=1)          ^^^^^^^^^^^^^^^^^^^^
qwen3.5-4b  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
qwen3.5-4b  | (APIServer pid=1)     next(self.gen)
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 951, in launch_core_engines
qwen3.5-4b  | (APIServer pid=1)     wait_for_engine_startup(
qwen3.5-4b  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1010, in wait_for_engine_startup
qwen3.5-4b  | (APIServer pid=1)     raise RuntimeError(
qwen3.5-4b  | (APIServer pid=1) RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
qwen3.5-4b exited with code 1 (restarting)
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302] 
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302]        █     █     █▄   ▄█
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.16.1rc1.dev265+gd106bf39f
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302]   █▄█▀ █     █     █     █  model   /models/cyankiwi/Qwen3.5-4B-AWQ-4bit
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:302] 
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [utils.py:238] non-default args: {'model_tag': '/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', 'max_model_len': 16384, 'served_model_name': ['qwen3.5-4b'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'gpu_memory_utilization': 0.3, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 4096, 'max_num_seqs': 8, 'enable_chunked_prefill': True}
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [model.py:530] Resolved architecture: Qwen3_5ForConditionalGeneration
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [model.py:1553] Using max model len 16384
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [cache.py:223] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=4096.
qwen3.5-4b  | (APIServer pid=1) WARNING 03-09 12:56:57 [config.py:392] Mamba cache mode is set to 'align' for Qwen3_5ForConditionalGeneration by default when prefix caching is enabled
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [config.py:412] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [config.py:232] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [config.py:263] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:56:57 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:11 [core.py:101] Initializing a V1 LLM engine (v0.16.1rc1.dev265+gd106bf39f) with config: model='/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', speculative_config=None, tokenizer='/models/cyankiwi/Qwen3.5-4B-AWQ-4bit', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=qwen3.5-4b, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [4096], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 16, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:12 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.5:54795 backend=nccl
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:12 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:17 [gpu_model_runner.py:4261] Starting to load model /models/cyankiwi/Qwen3.5-4B-AWQ-4bit...
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:17 [cuda.py:453] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:17 [mm_encoder_attention.py:215] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:17 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:17 [cuda.py:405] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
qwen3.5-4b  | (EngineCore_DP0 pid=94) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
qwen3.5-4b  | (EngineCore_DP0 pid=94) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:05<00:00,  5.26s/it]
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:05<00:00,  5.26s/it]
qwen3.5-4b  | (EngineCore_DP0 pid=94) 
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:23 [default_loader.py:293] Loading weights took 5.59 seconds
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:24 [gpu_model_runner.py:4344] Model loading took 3.85 GiB memory and 6.201251 seconds
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:24 [gpu_model_runner.py:5260] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:29 [decorators.py:465] Directly load AOT compilation from path /root/.cache/vllm/torch_compile_cache/torch_aot_compile/8eb57c07a0cb28e25c05fe4f6a26f79c17d1dbab45c8135a7f283823486c9a3d/rank_0_0/model
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:29 [backends.py:913] Using cache directory: /root/.cache/vllm/torch_compile_cache/3a332b42ba/rank_0_0/backbone for vLLM's torch.compile
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:29 [backends.py:973] Dynamo bytecode transform time: 2.08 s
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:31 [backends.py:283] Directly load the compiled graph(s) for compile range (1, 4096) from the cache, took 0.961 s
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:31 [monitor.py:35] torch.compile and initial profiling run took 3.37 s in total
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:38 [gpu_worker.py:424] Available KV cache memory: 7.73 GiB
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:38 [kv_cache_utils.py:1314] GPU KV cache size: 125,664 tokens
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:38 [kv_cache_utils.py:1319] Maximum concurrency for 16,384 tokens per request: 21.77x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 5/5 [00:00<00:00, 34.03it/s]
Capturing CUDA graphs (decode, FULL): 100%|██████████| 4/4 [00:01<00:00,  2.09it/s]
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:41 [gpu_model_runner.py:5366] Graph capturing finished in 3 secs, took 0.51 GiB
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:41 [core.py:282] init engine (profile, create kv cache, warmup model) took 16.99 seconds
qwen3.5-4b  | (EngineCore_DP0 pid=94) INFO 03-09 12:57:41 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:42 [api_server.py:491] Supported tasks: ['generate']
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:42 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:42 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:42 [serving.py:185] Warming up chat template processing...
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [hf.py:318] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [serving.py:210] Chat template warmup completed in 1124.9ms
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [api_server.py:496] Starting vLLM server on http://0.0.0.0:8000
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:38] Available routes are:
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /openapi.json, Methods: GET, HEAD
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /docs, Methods: GET, HEAD
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /docs/oauth2-redirect, Methods: GET, HEAD
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /redoc, Methods: GET, HEAD
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /tokenize, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /detokenize, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /load, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /version, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /health, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /metrics, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/models, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /ping, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /ping, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /invocations, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/chat/completions, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/chat/completions/render, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/responses, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/responses/{response_id}, Methods: GET
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/responses/{response_id}/cancel, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/completions, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/completions/render, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/messages, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /v1/messages/count_tokens, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /inference/v1/generate, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /scale_elastic_ep, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO 03-09 12:57:43 [launcher.py:47] Route: /is_scaling_elastic_ep, Methods: POST
qwen3.5-4b  | (APIServer pid=1) INFO:     Started server process [1]
qwen3.5-4b  | (APIServer pid=1) INFO:     Waiting for application startup.
qwen3.5-4b  | (APIServer pid=1) INFO:     Application startup complete.


