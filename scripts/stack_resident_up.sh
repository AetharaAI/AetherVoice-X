#!/usr/bin/env bash
set -euo pipefail

# Bring up the always-on stack:
# frontend, gateway, tts, asr, redis, postgres, minio, prometheus, grafana,
# plus realtime model lanes: voxtral, moss realtime, and moss voice generator.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-voicegen \
  up -d --build
