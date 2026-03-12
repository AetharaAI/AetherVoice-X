# Project State Package

This package separates human-readable documentation, machine-readable state, and bootstrap rule files.

## Purpose

The package exists to solve a repeatability problem:
- humans need explanation and context
- agents need stable current-state and contracts
- new projects need the same rule set every time

## Folder Layout

```text
project-state/
  human/
    Architecture-Overview.md
    Runtime-Contracts.md
    Changelog.md
  ai/
    manifest.yaml
    repo-map.yaml
    runtime-contracts.yaml
    current-state.yaml
  bootstrap/
    README.md
    AGENTS.md
    MEMORY.md
    CLAUDE.md
    GEMINI.md
```

## Canonical Rules

1. Human docs explain. AI docs declare.
2. AI docs must be YAML or JSON, not long prose.
3. AI docs contain current truth, not historical narrative.
4. Changelog remains the place for history and migration notes.
5. If runtime behavior changes, update both:
   - `human/Changelog.md`
   - `ai/current-state.yaml`
6. If interfaces change, update both:
   - `human/Runtime-Contracts.md`
   - `ai/runtime-contracts.yaml`
7. If repository structure changes materially, update:
   - `human/Architecture-Overview.md`
   - `ai/repo-map.yaml`
8. No secrets in this package.
9. The agent-facing entrypoint is `ai/manifest.yaml`.
10. Bootstrap files in `bootstrap/` are templates and policy shims for new projects.

## Read Order

For agents and IDE assistants:
1. `project-state/ai/manifest.yaml`
2. `project-state/ai/current-state.yaml`
3. `project-state/ai/runtime-contracts.yaml`
4. `project-state/ai/repo-map.yaml`
5. only then open human docs if more context is needed

## Intended Use

- Copy this package into new repos.
- Edit `ai/current-state.yaml` first.
- Update human docs as the system becomes more stable.
- Use `bootstrap/AGENTS.md` as the starting repo-level rules file.
