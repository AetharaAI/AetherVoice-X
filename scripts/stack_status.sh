#!/usr/bin/env bash
set -euo pipefail

# Show compose state plus a few direct health checks for the resident stack.
docker compose ps
echo
echo "---- gateway health ----"
curl -fsS http://127.0.0.1:8010/v1/health || true
echo
echo
echo "---- realtime moss health from tts ----"
docker compose exec tts curl -fsS http://moss:8021/health || true
echo
echo
echo "---- voice generator health from tts ----"
docker compose exec tts curl -fsS http://moss-voice-generator:8024/health || true
echo
echo
echo "---- voxtral-asr health from gateway ----"
docker compose exec gateway curl -fsS http://asr:8090/internal/health || true
echo
