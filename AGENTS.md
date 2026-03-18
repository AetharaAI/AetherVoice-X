# AGENTS

## Repo Intent

`Aether-Voice-X` is the production voice platform repo.

It is not the place for speculative runner experiments.

Current platform truth:

- `Voxtral Realtime ASR` is the frozen realtime ASR baseline.
- `Kokoro Realtime TTS` is the frozen realtime TTS baseline.
- telephony stability takes priority over experimentation
- `studio.aetherpro.us` is the future public-facing product lane
- `asr.aetherpro.us` remains the internal speech infrastructure and test bed

## Working Rules

- protect the live `Voxtral + Kokoro` lane
- prefer additive changes over rewrites
- do not load idle model families onto GPU without a clear reason
- remove stale routes, stale docs, and stale UI truth when decommissioning a lane
- use runtime proof, not model-card claims, as the decision standard

## Qwen Rule

Qwen experiments should start outside this repo first.

The current external runner-validation repo is:

- `/home/cory/Aether-Voice-Platform/qwen-experiments`

Only integrate a Qwen runner here after:

1. the runner boots reliably
2. the runner logs clearly
3. the runner proves real value against the frozen baseline

## Documentation Rule

When branch truth changes:

- update project state
- update the active planning doc
- keep runtime truth auditable
