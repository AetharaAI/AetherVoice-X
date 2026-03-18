# MOSS Decommission Plan - Qwen Test Branch - 2026-03-18

## Summary

This document marks the start of the `qwentest` branch.

The purpose of this branch is to:

- cleanly decommission the `OpenMOSS` family from the active Aether Voice stack
- preserve the current production-safe realtime path
- remove unnecessary GPU residency and cost from idle MOSS services
- establish a clean pre-Qwen checkpoint
- move into first-pass `Qwen-TTS` family testing the same work day

This is not a broad rewrite of the live speech platform.

This branch exists to make one thing true first:

`docker compose down && docker compose up` should restore a clean stack that powers only the known-good realtime voice substrate, without loading any MOSS models onto GPU.

After that checkpoint is verified, Qwen integration can begin from a clean and truthful baseline.

## Branch Intent

Current branch:

- `qwentest`

Branch mission:

- remove MOSS thoroughly
- keep `Voxtral Realtime ASR` untouched
- keep `Kokoro Realtime TTS` untouched
- keep current telephony behavior untouched
- keep `asr.aetherpro.us` usable as the internal speech infrastructure and testing surface
- prepare the repo and runtime for the next backend family: `Qwen-TTS`

## Current State Before Decommission

As of `2026-03-18`, the current operational truth is:

- `Voxtral Realtime ASR` is the production-promising realtime ASR lane and is actively used
- `Kokoro Realtime TTS` is the current known-good low-latency live reply lane
- telephony depends on the current realtime path and must not be destabilized
- `asr.aetherpro.us` functions as the internal test bed and speech infrastructure surface
- `OpenMOSS` remains wired into the repo, runtime catalog, docs, and UI even though it is no longer the preferred live lane
- MOSS sidecars and related config still represent unnecessary GPU load, runtime clutter, and product ambiguity

The present problem is not that the stack lacks a working realtime lane.

The problem is that MOSS is still attached to the system even though:

- it is not the frozen production baseline
- it is consuming planning and operational space
- it creates stale routes, stale docs, and stale UI assumptions
- it risks confusion during the transition to Qwen

## Non-Negotiable Constraints

- Do not break `Voxtral Realtime ASR`.
- Do not break `Kokoro Realtime TTS`.
- Do not break active telephony workflows.
- Do not remove the ability to use the internal app for ASR and TTS testing.
- Do not leave behind fake or stale MOSS choices in runtime config, route catalogs, or UI copy.
- Do not start Qwen integration on top of a half-removed MOSS surface.

## Immediate Objective

The immediate objective for this work block is:

1. decommission MOSS cleanly
2. verify a clean pre-Qwen compose boot with only the intended live stack
3. begin first Qwen model testing from that clean checkpoint

## Definition of Done

MOSS decommission is considered done only when all of the following are true:

1. `docker compose down && docker compose up` no longer boots any MOSS service in the normal stack path.
2. No MOSS model is intentionally loaded onto GPU during the standard stack bring-up.
3. `Voxtral` and `Kokoro` still come back cleanly and remain usable after the decommission boot.
4. Internal ASR usage on `asr.aetherpro.us` still works the same way it worked before the decommission.
5. Telephony-facing realtime behavior remains unchanged.
6. Backend config no longer defaults to MOSS for any active route.
7. Studio/backend route catalogs no longer advertise MOSS routes as active capabilities.
8. Voice registry seeds and defaults no longer depend on MOSS-specific records for normal operation.
9. Frontend studio copy, labels, and route selectors no longer present MOSS as a live family.
10. Documentation reflects the new truth: the system is running the frozen `Voxtral + Kokoro` live baseline while Qwen integration is the next planned family buildout.

## Pre-Qwen Checkpoint

Before any Qwen runtime work begins, this checkpoint must be true:

- compose boot is clean
- GPU load is limited to the intended live stack
- no MOSS routes are masquerading as available product surface
- the internal app remains usable for realtime ASR and Kokoro testing
- the repo state and docs match runtime truth

This checkpoint is the control run.

If anything fails after Qwen work begins, the team must be able to say with confidence that the failure was introduced by Qwen integration rather than by leftover MOSS state.

## Work Sequence

The decommission should proceed in this order:

1. runtime and compose
2. env and settings defaults
3. backend adapters, aliases, schemas, and route catalog
4. voice registry seeds and studio defaults
5. frontend studio language and route selectors
6. docs and project-state notes
7. VM bring-down / bring-up verification
8. first Qwen model test

## Verification Pass

After the MOSS removal changes are applied, verification should include:

- full stack shutdown
- full stack startup
- confirm only intended services are back
- confirm no MOSS model is occupying GPU
- confirm realtime ASR still works
- confirm realtime Kokoro TTS still works
- confirm telephony-safe baseline behavior is unchanged

## End-of-Day Target

The target for this work day is not just "MOSS removed in code."

The target is:

- MOSS decommissioned cleanly
- stack re-booted cleanly
- baseline verified
- first `Qwen-TTS` family model test started

## Working Note

This document is the planning anchor for the `qwentest` branch.

If runtime truth changes during this branch, update this document so the branch history stays understandable and the transition from `OpenMOSS` to `Qwen-TTS` remains explicit and auditable.
