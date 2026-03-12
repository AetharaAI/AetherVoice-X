# GPU Node Registry

## Purpose
Canonical map of compute nodes, workloads, and intended use.

| Node | GPU(s) | Role | Current workloads | Intended workloads | Public surfaces | Internal surfaces | Storage pattern | Notes |
|---|---|---|---|---|---|---|---|---|
| L40S-180 | 2x L40S | Core large-model inference | Qwen3.5-122B-AWQ-4Bit | Primary reasoning / coding / future premium lanes | via gateway only | model runners | standardized block storage | High-value core node |
| L40S-90 | 1x L40S | Vision / multimodal | Phi-4 / smaller multimodal candidates | Perceptor, multimodal, support lanes | via gateway/internal API | model runners | standardized block storage | Avoid model hoarding |
| L4-360 | 4x L4 | Service node | ASR, TTS, embeddings, reranker | voice platform / service multiplexing | studio only | asr, tts, embed | standardized block storage | Multi-lane infra node |

## Per-node checklist
For each node record:
- hostname:
- provider:
- attached block storage:
- mounted paths:
- active Docker services:
- active ports:
- reverse proxy mapping:
- auth strategy:
- monitoring:
- backup / recovery notes:

## Node role rule
Each node should have a dominant purpose:
- core inference
- multimodal inference
- service multiplexing
- data spine
- control plane

Do not blur roles unless there is a clear business reason.