# Model Registry

## Purpose
Track every model that exists, where it runs, why it exists, and whether it deserves to keep burning compute.

| Model | Modality | Size / Quant | Node | Runtime | Primary Role | Secondary Role | Status | Revenue Relevance | Keep / Pause / Remove | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-AWQ-4Bit | multimodal / reasoning | 122B AWQ 4-bit | L40S-180 | OpenAI-compatible gateway | primary intelligence lane | advanced reasoning | production core | high | keep | Core large-model node |
| Phi-4 Multimodal Instruct | multimodal | TBD | L40S-90 | model runner | voice / audio / image experimentation | operator assistant | active experiment | medium-high | evaluate | Must justify GPU occupancy |
| Qwen3.5-9B-AWQ | multimodal / utility | 9B AWQ | L40S-90 or staged | model runner | sub-agent / utility lane | fallback vision | bench candidate | medium | evaluate | Potential sidecar candidate |
| Qwen3.5-4B-AWQ | multimodal / utility | 4B AWQ | staged | model runner | lightweight sub-agent | mobile / edge experiments | bench candidate | low-medium | evaluate | Good for small workers |
| Jan Code 4B AWQ | code | 4B AWQ | staged | model runner | coding sub-agent | infra utility | future fleet | medium | keep staged | Sub-agent lane |

## Status values
- production core
- active experiment
- bench candidate
- future fleet
- deprecated
- removed

## Hard rules
- No model stays deployed without a job.
- No model gets GPU residency without:
  - a primary role
  - a measured benefit
  - a defined owner
- Every production model must have:
  - endpoint
  - runtime owner
  - node assignment
  - rollback path