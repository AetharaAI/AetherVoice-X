#!/usr/bin/env bash
set -euo pipefail

# Rebuild only the services that change most often during live ASR/TTS work.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-voicegen \
  up -d --build frontend gateway tts asr voxtral moss moss-voice-generator
