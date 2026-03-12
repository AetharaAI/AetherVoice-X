# AetherPro Operating Dossier

## 1. Executive Snapshot
- Company: AetherPro Technologies
- Current phase: Infrastructure consolidation / product hardening / revenue path execution
- Primary objective this quarter: convert infrastructure advantage into clean sellable product lanes
- Secondary objective: standardize documentation, operating records, and product packaging across repos
- Current top constraints: single-founder bandwidth, uneven packaging maturity, surface sprawl across domains/subdomains
- Current top risks: product clarity lagging infrastructure readiness, public/internal surface confusion, fragmented documentation truth
- Current top monetization priorities: Aether Voice Platform for trade businesses, RedWatch brand launch, identity/platform leverage through Passport

## 2. Active Product Portfolio
| Product | Domain | Category | Stage | Revenue Status | Priority | Owner | Notes |
|---|---|---:|---|---|---:|---|---|
| RedWatch | redwatch.us | Security | planning | Pre-revenue | High | CJ | Standalone security brand |
| Perceptor | perceptor.us / perception.aetherpro.us | Perception | active development | Internal platform | High | CJ | Multimodal sensor-fusion platform |
| Aether Voice Platform | studio.aetherpro.us / voice.aetherpro.us | Voice infra | active development | Near-term revenue | Critical | CJ | Unified ASR/TTS surface plus paid telephony lane |
| Passport Alliance | passportalliance.org | Identity | active development | Strategic | Medium | CJ | Federation / identity layer |
| Aether Agent Forge | aetheragentforge.org | Marketplace | operational internal | Monetized / strategic | Medium | CJ | Agent marketplace |
| Aether Gateway | api.aetherpro.tech | Infra | operational internal | Internal core | Critical | CJ | Model routing / gateway |
| Triad | triad.aetherpro.tech | Data spine | operational internal | Internal core | Critical | CJ | Memory / state / coordination |

## 3. Company Systems Overview
### Core domains
- Primary corporate: `aetherpro.us`
- Core product surfaces: `redwatch.us`, `perceptor.us`, `studio.aetherpro.us`, `passportalliance.org`
- Internal-only service surfaces: `api.aetherpro.tech`, `triad.aetherpro.tech`, internal service and model lanes
- Redirect / support / auxiliary domains: per-product support and internal service subdomains as needed

### Canonical infrastructure pattern
- Edge / public surfaces: branded domains and subdomains with clear public-purpose separation
- App / control-plane nodes: business logic, routing, orchestration, internal admin/control surfaces
- GPU nodes: dedicated by dominant purpose, not as a general dumping ground
- Data spine: central persistence, memory, vector, state, and coordination layers
- Developer / operator endpoints: internal-only control and operating surfaces

## 4. Standard System States
Use only one of:
- planning
- scaffolded
- active development
- operational internal
- production internal
- production external
- paused
- deprecated

## 5. Current Quarter Priorities
### P0
- [ ] Finalize voice-agent operating lane for trades-first sales motion.
- [ ] Launch RedWatch public brand surface and internal ops plan.
- [ ] Make dossier standard reproducible across all active repos.

### P1
- [ ] Complete Perceptor architecture and capability framing.
- [ ] Normalize model and node registry discipline.
- [ ] Standardize public/internal surface boundaries across products.

### P2
- [ ] Expand portfolio-wide decision log discipline.
- [ ] Add deeper integration registries where repos actually need them.
- [ ] Rationalize non-critical surfaces and backlog sprawl.

## 6. Revenue-Critical Tracks
| Track | Why it matters | Current blocker | Next action | ETA confidence |
|---|---|---|---|---|
| Voice platform | Immediate sellable capability and founder-led trade-market entry | live lane polish and production telephony packaging | stabilize live ASR/TTS and formalize Twilio-backed phone lane | High |
| RedWatch | Brand + security offer | Landing page not built | Build public-facing site | High |
| Passport | Identity leverage | Docs / GTM alignment | Standardize docs and product framing | Medium |

## 6.1 Current Revenue Note

- Twilio voice agent phone lane upgraded from trial to paid on 2026-03-08.
- Payment method: company Mercury business account debit card.
- Business meaning: the telephony lane is now an active paid operating dependency and should be treated as part of the Aether Voice Platform revenue path, not as a side experiment.

## 7. Infrastructure Standards
### Directory/layout standards
- Block storage root: standardized per node and documented per owning repo
- Model runner root: standardized by runtime owner, not ad hoc per experiment
- LiteLLM/control-plane root: documented in the owning infra/control repo
- Compose pattern: prefer one clear top-level compose entrypoint per serious runtime repo
- Env file conventions: `.env`, `.env.example`, and any scoped env variants with explicit naming
- Naming conventions: boring, exact, repeatable; avoid surface-name drift

### Documentation standards
Every serious repo should include:
- README.md
- PROJECT_STATE.md
- CHANGELOG.md
- ROADMAP.md
- ARCHITECTURE.md
- DEPLOYMENT.md
- BACKLOG.md
- DECISIONS.md

## 8. Decision Log Index
| Date | Decision | Why | Impacted systems |
|---|---|---|---|
| YYYY-MM-DD |  |  |  |

## 9. Risk Register
| Risk | Severity | Likelihood | Affected systems | Mitigation |
|---|---|---|---|---|
| Single-founder bandwidth | High | High | All | Standardize docs / templates / runbooks |
| GPU capacity fragmentation | High | Medium | Perceptor / Voice / model fleet | Formal model registry |
| Public/internal surface confusion | Medium | Medium | Voice / ASR / TTS | Clear surface separation |
| Revenue lane packaging lag | High | Medium | Voice / RedWatch | Treat GTM documentation as operating infrastructure |

## 10. Next 7 Days
- [ ] Finish canonical DOSSIER standard and normalize the highest-value repos to it.
- [ ] Document Twilio paid phone lane and voice-agent operating assumptions.
- [ ] Continue RedWatch public site plus internal ops build path.

## 11. Next 30 Days
- [ ] Push founder-led trade outreach using the voice-agent lane.
- [ ] Stabilize Aether Voice Platform packaging, lane definitions, and operating docs.
- [ ] Stand up the Aether Control Plane repo as the true master dossier source.
