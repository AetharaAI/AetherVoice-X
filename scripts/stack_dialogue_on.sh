#!/usr/bin/env bash
set -euo pipefail

# Start the dialogue / long-form TTSD lane on demand.
docker compose --profile moss-ttsd up -d --build moss-ttsd
