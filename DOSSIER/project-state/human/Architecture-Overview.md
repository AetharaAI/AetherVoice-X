# Architecture Overview

## Current Project

This repository contains the internal AetherOps/PolyMorph harness and related infrastructure notes.

## Major Areas

- `mini-agent/`
  - active harness product/runtime
  - frontend, backend, providers, tools, evals, docs
- `L40S-90/`
  - LiteLLM and local inference node configuration
- `litellm-L40S-180/`
  - dual-GPU inference node configuration
- `model-test/`
  - harness and model benchmark prompts/results
- `model-cards/`
  - operational notes for local/self-hosted models
- `AETHERPRO_INFRA_TOPOLOGY.md`
  - cross-node infra map

## Responsibility Split

- Human docs in this package explain system shape and decisions.
- AI docs in this package encode current truth and contracts.
- Existing implementation docs under `mini-agent/docs/` remain source material for deeper detail.
