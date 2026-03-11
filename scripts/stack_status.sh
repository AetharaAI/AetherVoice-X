#!/usr/bin/env bash
set -euo pipefail

# Show compose state plus a few direct health checks for the resident stack.
docker compose ps
echo
echo "---- gateway health ----"
curl -fsS http://127.0.0.1:8010/v1/health || true
echo
echo
echo "---- realtime moss health ----"
curl -fsS http://127.0.0.1:8013/health || true
echo
echo
echo "---- voice generator health ----"
curl -fsS http://127.0.0.1:8016/health || true
echo
echo
echo "---- asr health ----"
curl -fsS http://127.0.0.1:8090/internal/health || true
echo
