# Product Manifest

## Name

Aether Voice X

## Product Thesis

Aether Voice X is a sovereign, self-hosted voice infrastructure stack for serious conversational systems.

The product exists to give operators full control over:

- ASR
- reasoning / LLM orchestration
- TTS
- routing
- deployment topology
- data residency
- performance envelopes
- fallback behavior

The product is intentionally designed to avoid hard dependency on third-party hosted voice APIs for the core experience.

## Why This Exists

Hosted API products can be useful, but they create structural risk:

- upstream model changes outside operator control
- pricing changes
- product deprecations
- service outages
- routing and latency uncertainty
- data handling constraints
- weak fit for private or air-gapped deployments

Aether Voice X exists to make the voice layer ownable.

## Core Promise

This stack should be able to run:

- on practical GPU hardware
- in private environments
- in controlled enterprise environments
- in air-gapped or restricted deployments
- as a modular system, not a monolith

## Product Lanes

### 1. Realtime Agent Mode

Pipeline:

`ASR -> LLM -> realtime TTS`

Purpose:

- telephony agents
- live customer intake
- low-latency operational voice systems
- interruption-capable turn taking

### 2. Turn-Based Voice Mode

Pipeline:

`ASR -> LLM -> batch / turn-based TTS`

Purpose:

- stronger voice fidelity
- easier debugging
- reliable conversational baseline
- operator-safe deployment path before hard realtime is fully tuned

### 3. Assisted / Staged Streaming Mode

Pipeline:

`ASR -> LLM -> staged/chunked playback`

Purpose:

- perceived realtime without strict realtime synthesis constraints
- useful for dispatch, intake, scheduling, support, and guided workflows

## Product Principles

- Own the infrastructure.
- Keep the stack modular.
- Treat every lane as a product surface with clear operational truth.
- Prefer deterministic operational controls over hidden magic.
- Separate “working” from “production-ready”.
- Build for deployment reality, not just benchmarks.

## Operator Reality

This repo is not just a codebase. It is part of a founder operations system:

- build notes
- infra truth
- deployment scripts
- runtime contracts
- troubleshooting knowledge
- handoff context

The product should remain understandable to an operator who actually has to run it.

## Near-Term Product Priority

1. Freeze Realtime Agent Mode at the current known-good baseline.
2. Build Turn-Based Voice Mode to completion.
3. Return to realtime identity and conditioning with stronger evidence and cleaner reference assets.
4. Add assisted / staged streaming once the two core lanes are stable.

## Long-Term Vision

The long-term goal is a deployable voice operating layer for private, high-control, high-trust conversational systems.

That includes:

- telephony agents
- service intake
- dispatch flows
- domain-specific assistants
- private research assistants
- secure and sovereign deployments
- future government and defense-adjacent operating environments
