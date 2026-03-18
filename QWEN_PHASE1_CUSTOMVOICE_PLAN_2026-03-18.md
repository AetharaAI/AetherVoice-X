# Qwen Phase 1 Plan - CustomVoice First - 2026-03-18

## Summary

Phase 1 of the `qwentest` branch will start with:

- `Qwen3-TTS-12Hz-1.7B-CustomVoice`

This is the first Qwen model to integrate because it has the highest near-term product value and the lowest integration risk relative to the rest of the released Qwen TTS family.

The goal is not to replace the frozen realtime lane on day one.

The goal is to add a stronger sellable voice inventory lane while preserving the current:

- `Voxtral Realtime ASR`
- `Kokoro Realtime TTS`
- telephony-safe runtime contract

## Why This Model First

Based on the local Qwen model card in [modelcards/Qwen-TTS-Modelcard.md](/home/cory/Aether-Voice-Platform/Aether-Voice-X/modelcards/Qwen-TTS-Modelcard.md), the `1.7B-CustomVoice` model is the best first fit because it provides:

- instruction-controlled generation
- streaming support
- 9 premium timbres
- broad language support
- lower operational complexity than clone-first workflows

This aligns with the immediate business need:

- improve available voice quality and variety for telephony and demos
- avoid another large speculative integration before proving runtime truth
- ship a monetizable voice layer before expanding into design and clone workflows

## Phase 1 Scope

Phase 1 is limited to one backend family member:

- `qwen_customvoice`

Phase 1 does not include:

- `qwen_voicedesign`
- `qwen_baseclone`
- replacing `kokoro_realtime` in the live telephony lane
- loading the full Qwen family onto GPU by default

## Runtime Positioning

The Qwen Phase 1 lane should be treated as:

- a premium studio and telephony-voice selection lane
- suitable for batch and staged generation first
- a proving ground for future promotion into lower-latency lanes

It should not be treated as the live telephony reply engine until it wins on measured runtime truth.

## GPU Policy

Current host GPU truth after MOSS decommission:

- GPU `2`: `Voxtral Realtime`
- GPU `3`: `Kokoro Realtime`
- GPU `1`: internal ASR fallback and embeddings/reranker workloads
- GPU `0`: free for the first Qwen runner

Phase 1 recommendation:

- pin `Qwen3-TTS-12Hz-1.7B-CustomVoice` to host GPU `0`

This preserves the current production-safe lane and isolates Qwen bring-up from the frozen realtime path.

## Product Positioning

The first user-facing value of Qwen should be:

1. a better voice catalog for telephony builds
2. stronger premium voice demos
3. better voice selection for future public studio users

The first user-facing value of Qwen should not be:

1. open-ended voice design as the first surface
2. cloning as the first operational promise
3. replacing the current realtime reply engine before benchmarks exist

## Integration Order

The next implementation sequence should be:

1. add the `qwen_customvoice` backend runner and adapter surface
2. verify direct generation on GPU `0`
3. expose it inside the internal app as a controlled test lane
4. benchmark output quality, repeatability, and first-audio latency
5. use those learnings to design the public `studio.aetherpro.us` experience

## Definition Of Done

Phase 1 is considered successful only when all of the following are true:

1. `Qwen3-TTS-12Hz-1.7B-CustomVoice` boots cleanly on GPU `0`.
2. The system can synthesize repeatable audio through a stable internal backend path.
3. The new Qwen lane does not disrupt `Voxtral` or `Kokoro`.
4. The internal app can exercise the Qwen lane without pretending it is already the telephony default.
5. The team can evaluate real voice quality and runtime behavior from a known-good baseline.

## Follow-On Phases

If Phase 1 succeeds, the next order should be:

1. `Qwen3-TTS-12Hz-1.7B-VoiceDesign`
2. `Qwen3-TTS-12Hz-1.7B-Base`

`VoiceDesign` belongs next because it is a studio product multiplier.

`Base` belongs after that because it unlocks higher-touch enterprise cloning workflows and should likely be treated as an on-demand lane rather than a permanently resident one.
