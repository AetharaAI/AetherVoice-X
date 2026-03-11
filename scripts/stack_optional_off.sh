#!/usr/bin/env bash
set -euo pipefail

# Stop and remove the optional heavy OpenMOSS lanes so the resident stack keeps headroom.
docker compose stop moss-tts moss-ttsd moss-soundeffect || true
docker compose rm -sf moss-tts moss-ttsd moss-soundeffect || true
