# Memory Rules

## Purpose
This file defines how project memory should be treated.

## Rules
- Distinguish current operational truth from historical narrative.
- Keep current truth in `project-state/ai/current-state.yaml`.
- Keep migration history in `project-state/human/Changelog.md`.
- If memory backends require bootstrap, record that in both human runtime docs and AI current state.
- Memory failures should degrade gracefully when possible and should not silently corrupt state.
