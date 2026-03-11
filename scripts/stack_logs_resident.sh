#!/usr/bin/env bash
set -euo pipefail

# Follow the logs for the always-on operator stack.
docker compose logs -f frontend gateway tts asr voxtral moss moss-voice-generator
