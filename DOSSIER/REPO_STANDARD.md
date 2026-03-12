# AetherPro Repo Standard

## Purpose

This document defines the canonical documentation and directory standard that should be reused across AetherPro repositories.

The goal is not maximum paperwork. The goal is a boringly accurate, repeatable operating spine so every serious repo can answer the same questions:

- What is this repo?
- What product or system does it support?
- What is its current state?
- What is running?
- What depends on it?
- What is blocked?
- What is next?

## Canonical Spelling and Naming

Use these names exactly:

- `DOSSIER/` is the canonical folder name.
- `registry` is the canonical term, not `registery`.
- `project state` is the canonical term for current-state docs.
- `operating dossier` is the canonical term for the higher-level operating summary.

Do not vary between `dossier`, `DOSSIER`, `docsier`, or ad hoc folder names across repos. The directory should be `DOSSIER/` everywhere.

## Governing Rules

1. Every serious repo gets the same core document spine.
2. Scope changes by repo, but the file names stay stable.
3. If a section does not apply, mark it `not applicable` rather than deleting the section.
4. Do not scaffold telemetry, GPU, model, or security directories unless the repo actually owns those concerns.
5. The standard should reflect reality, not aspiration.
6. Public product language and internal operating truth must remain clearly separated.

## Master Dossier Rule

There should only be one true master operating dossier system across the business.

That master belongs in the Aether Control Plane repo.

All other repos should follow the same standard, but they should contain only:

- the local product or platform slice
- the local dependencies that materially matter
- the local operating truth for that repo

They are not supposed to become competing company-wide sources of truth.

Use this rule:

- Aether Control Plane repo = master company-wide dossier
- every other repo = local dossier slice following the same standard

This keeps structure repeatable without creating conflicting portfolio records across repos.

## Repo Classes

### 1. Product or App Repo

Use this for a single product, app, API, UI, or service surface.

Examples:

- RedWatch
- Perceptor
- Aether Voice Platform

In these repos, the dossier should describe the local product plus the immediate dependencies around it.

### 2. Platform or Infra Repo

Use this for shared infrastructure, routing, identity, orchestration, gateways, data spines, or runtime systems.

Examples:

- model gateway
- identity platform
- shared event bus
- data/control plane

In these repos, the dossier should describe the platform service and the systems it supports.

### 3. Aether Control Plane Repo

This is the company-wide master operating repo.

It uses the same structure as every other repo, but it is expected to be the fullest version. It should contain the complete company and platform-wide registries, not just the local slice.

That means:

- all products
- all projects
- all major infrastructure surfaces
- all major node and model registries
- company-level operating priorities
- company-level risks and decisions

## Mandatory Root Docs

Every serious repo should include these root-level files:

- `README.md`
- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`
- `DEPLOYMENT.md`
- `BACKLOG.md`
- `DECISIONS.md`

Use these consistently:

- `README.md` = what it is and how to use it
- `PROJECT_STATE.md` = current reality, current blockers, next actions
- `CHANGELOG.md` = chronological changes
- `ROADMAP.md` = forward plan
- `ARCHITECTURE.md` = system design and boundaries
- `DEPLOYMENT.md` = runtime/deploy/release instructions
- `BACKLOG.md` = queued work
- `DECISIONS.md` = architectural and operational decisions

## Mandatory DOSSIER Docs

Every serious repo should include these files inside `DOSSIER/`:

- `REPO_STANDARD.md`
- `OPERATING_DOSSIER.md`
- `PROJECT_PORTFOLIO.md`
- `PRODUCT_REGISTRY.md`

### Required meanings

- `REPO_STANDARD.md`
  - the canonical standard this repo claims to follow
  - local deviations can be noted here

- `OPERATING_DOSSIER.md`
  - executive snapshot
  - current priorities
  - portfolio context
  - risks
  - next 7/30 days

- `PROJECT_PORTFOLIO.md`
  - active project list
  - priority
  - blocker
  - next action
  - owner

- `PRODUCT_REGISTRY.md`
  - all products or surfaces relevant to this repo
  - public domains
  - internal surfaces
  - current state
  - monetization or strategic role

## Conditional DOSSIER Docs

Only add these when the repo actually owns the concern.

- `GPU_NODE_REGISTRY.md`
  - required if the repo owns or directly manages GPU nodes

- `MODEL_REGISTRY.md`
  - required if the repo deploys, routes, benchmarks, or governs models

- `<PRODUCT>_PROJECT_STATE.md`
  - use when the repo needs a deep-dive current-state doc for the primary product or a major subsystem
  - example: `PERCEPTOR_PROJECT_STATE.md`

- `SERVICE_REGISTRY.md`
  - use when the repo owns multiple internal or public services

- `INTEGRATION_REGISTRY.md`
  - use when the repo depends on many external or internal integrations

- `SECURITY_REGISTRY.md`
  - use when the repo owns security posture, test surfaces, controls, or formal security workflows

- `COMPLIANCE_REGISTRY.md`
  - use when the repo owns compliance mappings, controls, or evidence workflows

- `IDENTITY_REGISTRY.md`
  - use when the repo owns auth, SSO, federation, or identity surfaces

- `ENVIRONMENT_REGISTRY.md`
  - use when the repo spans multiple important environments with distinct runtime rules

## Canonical Directory Layout

The exact source-code directories can vary by language and stack. A Python repo, Next.js repo, and desktop repo do not need identical code layout.

What should be standardized is the operating/documentation spine and the meaning of the major support directories.

Use this as the baseline:

```text
repo-root/
  README.md
  PROJECT_STATE.md
  CHANGELOG.md
  ROADMAP.md
  ARCHITECTURE.md
  DEPLOYMENT.md
  BACKLOG.md
  DECISIONS.md

  DOSSIER/
    REPO_STANDARD.md
    OPERATING_DOSSIER.md
    PROJECT_PORTFOLIO.md
    PRODUCT_REGISTRY.md
    <PRODUCT>_PROJECT_STATE.md         # when needed
    GPU_NODE_REGISTRY.md               # when repo owns GPU nodes
    MODEL_REGISTRY.md                  # when repo owns models
    SERVICE_REGISTRY.md                # when needed
    INTEGRATION_REGISTRY.md            # when needed
    SECURITY_REGISTRY.md               # when needed
    IDENTITY_REGISTRY.md               # when needed
    COMPLIANCE_REGISTRY.md             # when needed
    ENVIRONMENT_REGISTRY.md            # when needed

  SPECS/
    original_build_spec.md
    current_build_spec.md

  docs/
    architecture/
    api-contracts/
    deployment/
    security/
    telemetry/
    product/

  scripts/
  tests/
  telemetry/                          # only if this repo owns telemetry assets
  infrastructure/                     # only if this repo owns infra code/assets
  models/                             # only if this repo owns model artifacts/config
```

## Telemetry and Monitoring Rules

Do not blindly scaffold `prometheus/`, `grafana/`, `loki/`, or `tempo/` into every repo.

Use telemetry directories only when the repo owns observability configuration, dashboards, rules, or alerting assets.

Current practical example:

- Aether Voice X / the full ASR-TTS voice pipeline is the repo most likely to legitimately own a fuller Prometheus/Grafana footprint right now.

For ordinary product repos:

- include telemetry docs only if the repo owns monitoring assets
- otherwise document monitoring dependencies in `DEPLOYMENT.md` or `OPERATING_DOSSIER.md`

If a repo does own telemetry assets, use this layout:

```text
telemetry/
  prometheus/
    config/
    rules/
    alerts/
  grafana/
    dashboards/
    screenshots/
  loki/
    config/
    rules/
  tempo/
    config/
```

## Documentation Standards

Every core dossier file should be concise, current, and decision-useful.

Minimum standards:

- Start with a clear title.
- State purpose near the top.
- Use fixed tables where possible.
- Use consistent state vocabulary.
- Every tracked item should have an owner.
- Every tracked item should have a next action.
- Every important list should distinguish active from future work.

Preferred fields in tables:

- `Current State`
- `Priority`
- `Revenue Impact` or `Strategic Importance`
- `Blockers`
- `Next Step`
- `Owner`

## Standard State Vocabulary

Use one controlled vocabulary across repos whenever possible.

Recommended system states:

- `planning`
- `scaffolded`
- `active development`
- `operational internal`
- `production internal`
- `production external`
- `paused`
- `deprecated`

Recommended priority vocabulary:

- `P0`
- `P1`
- `P2`
- `P3`

Recommended revenue/importance vocabulary:

- `critical`
- `high`
- `medium`
- `low`
- `strategic`

## Registry Rules

### Product Registry

Every listed product should have:

- public domain
- internal surface(s)
- purpose
- audience
- current state
- monetization path or strategic role
- dependencies

### Project Portfolio

Every listed project should have:

- objective
- current state
- priority
- blocker
- next step
- owner

No project should remain active without a defined next step.

### GPU Node Registry

Every listed node should have:

- node identity
- role
- current workloads
- intended workloads
- public/internal exposure pattern
- storage pattern
- notes on boundaries or risk

### Model Registry

Every listed model should have:

- modality
- size/quant
- node
- runtime
- primary role
- status
- business relevance
- keep/evaluate/remove decision

No model should retain residency without a purpose.

## Freshness Rules

This standard fails if the docs rot.

Minimum hygiene:

- `PROJECT_STATE.md` should change when reality changes materially.
- `OPERATING_DOSSIER.md` should be reviewed weekly.
- `PROJECT_PORTFOLIO.md` should be reviewed weekly.
- `PRODUCT_REGISTRY.md` should be updated whenever a new public or internal surface is created.
- `GPU_NODE_REGISTRY.md` and `MODEL_REGISTRY.md` should be updated whenever placement changes.
- `DECISIONS.md` should capture non-trivial architecture or operating decisions.

## What Not To Do

- Do not create giant empty directory trees just because a template said so.
- Do not include Grafana or Prometheus folders in repos that do not own them.
- Do not use different file names for the same concept across repos.
- Do not mix public marketing language into internal operating records.
- Do not leave project entries without blockers or next actions.
- Do not keep stale models or infrastructure notes in registries after reality changes.

## Application to This Repo

This repo already has a good starting `DOSSIER/` package:

- `OPERATING_DOSSIER.md`
- `PROJECT_PORTFOLIO.md`
- `PRODUCT_REGISTRY.md`
- `PERCEPTOR_PROJECT_STATE.md`
- `GPU_NODE_REGISTRY.md`
- `MODEL_REGISTRY.md`

That is a valid pattern for a repo with:

- product context
- infrastructure dependence
- GPU/model relevance

What matters now is keeping the naming stable and the content accurate, then reproducing this spine cleanly across the rest of the business.
