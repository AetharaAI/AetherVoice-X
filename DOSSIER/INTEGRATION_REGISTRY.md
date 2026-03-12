# Integration Registry

## Purpose

Canonical list of external and internal integrations that materially affect operations, revenue, delivery, or platform dependency.

Use this file only in repos where integrations are important enough to track as operating infrastructure.

| Integration | Category | Used By | Current State | Business Role | Owner | Dependency Criticality | Current Notes |
|---|---|---|---|---|---|---|---|
| Twilio | telephony | Aether Voice Platform | active paid | inbound/outbound voice agent phone lane | CJ | high | Upgraded from trial to paid on 2026-03-08 using Mercury business debit card; phone lane now treated as real operating dependency |

## Integration Rules

- Track only integrations that matter to operations, revenue, product delivery, or security.
- Do not add throwaway SDKs or casual services here.
- Every listed integration should have:
  - a business role
  - an owner
  - a current state
  - a criticality level
  - a short note on what changed

## Current Notes

- Twilio now belongs in operating documentation because the phone lane is part of the active voice-agent go-to-market path.
- The phone lane should be documented as a business system, not just a technical service.
- Do not place payment instrument details beyond what is operationally relevant. Business-funded and date-tracked is enough.
