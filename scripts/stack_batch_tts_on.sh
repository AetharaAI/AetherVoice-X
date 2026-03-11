#!/usr/bin/env bash
set -euo pipefail

# Start the large single-speaker batch TTS lane on demand.
docker compose --profile moss-tts up -d --build moss-tts
