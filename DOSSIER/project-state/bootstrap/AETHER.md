# Repo Operating Rules

## Canonical Project State
The canonical machine-readable project state lives in:
- `project-state/ai/manifest.yaml`
- `project-state/ai/current-state.yaml`
- `project-state/ai/runtime-contracts.yaml`
- `project-state/ai/repo-map.yaml`

Read those before making structural changes.

## Update Rules
- If architecture changes, update `project-state/human/Architecture-Overview.md` and `project-state/ai/repo-map.yaml`.
- If runtime behavior or interfaces change, update `project-state/human/Runtime-Contracts.md` and `project-state/ai/runtime-contracts.yaml`.
- If operational truth changes, update `project-state/ai/current-state.yaml`.
- If behavior changes over time, add a note to `project-state/human/Changelog.md`.

## Safety Rules
- Do not store secrets in project-state files.
- Prefer explicit contracts over narrative when writing AI-facing state.
- Do not silently change provider behavior without recording it in runtime contracts.
