# Product Registry

## Purpose
Canonical list of all AetherPro products, sub-brands, platforms, and infrastructure surfaces.

| Product | Public Domain | Internal Surface(s) | Category | Purpose | Audience | Current State | Monetization Path | Dependencies | Notes |
|---|---|---|---|---|---|---|---|---|---|
| RedWatch | redwatch.us | internal security services | Security platform | Security readiness, assessments, runbooks, compliance-aligned ops | Teams, firms, regulated environments | planning | service-led -> platform | Perceptor, docs, infra | Standalone brand |
| Perceptor | perceptor.us | perception.aetherpro.us, audio.aetherpro.us | Perception platform | Sensor fusion, OCR, vision, audio, event interpretation | Internal + future enterprise | active development | platform / licensing / internal leverage | GPU nodes, models, event bus | Core capability layer |
| Aether Voice Platform | studio.aetherpro.us | asr.aetherpro.us, tts.aetherpro.us, voice.aetherpro.us | Voice platform | Unified ASR/TTS and telephony-capable voice agent surface | Developers, operators, product teams, trade businesses | active development | direct service revenue + voice agents | L4-360, gateway, ASR/TTS models, Twilio phone lane | Public surface should be studio only; phone lane is now funded and active for go-to-market |
| Passport Alliance | passportalliance.org | identity services | Identity platform | Human + agent identity / federation | Enterprise / protocol / infrastructure | active development | product / infrastructure layer | auth stack, control plane | Strategic moat |
| Aether Gateway | api.aetherpro.tech | internal model routing | Infra | Unified routing and model access | Internal / platform | operational internal | internal leverage | model nodes, router | Control-plane critical |
| Triad | triad.aetherpro.tech | internal DB surfaces | Data spine | Memory, state, vector search, coordination | Internal / all products | operational internal | internal leverage | Postgres, Redis, Mongo, Qdrant, Weaviate | Backbone |

## Product State Definitions
- planning
- active development
- operational internal
- production internal
- production external
- paused
- deprecated

## Rules
- Every new product gets an entry before major buildout.
- Every public domain must map to a product here.
- Every product must have:
  - one purpose sentence
  - one monetization path
  - one current state
  - one next milestone

## Current Notes

- The paid Twilio phone lane now belongs under Aether Voice Platform operations, not as an orphan integration.
- `voice.aetherpro.us` is the voice-agent telephony lane and should be treated as a revenue-path surface, even if the broader product packaging is still being refined.
