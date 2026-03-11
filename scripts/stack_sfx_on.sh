#!/usr/bin/env bash
set -euo pipefail

# Start the sound-effect lane on demand.
docker compose --profile moss-sfx up -d --build moss-soundeffect
