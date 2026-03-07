#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"
TTS_TEXT="${TTS_TEXT:-Aether Voice platform smoke test. This is a synthesis check.}"
TTS_VOICE="${TTS_VOICE:-Emily.wav}"
ASR_FILE="${ASR_FILE:-}"
pretty_print() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

echo "Checking gateway health at ${BASE_URL}/v1/health"
curl -fsS "${BASE_URL}/v1/health"

echo
echo "Checking model catalog at ${BASE_URL}/v1/models"
curl -fsS "${BASE_URL}/v1/models" | pretty_print

echo
echo "Checking batch TTS at ${BASE_URL}/v1/tts/synthesize"
curl -fsS \
  -X POST \
  -H "Content-Type: application/json" \
  -d "$(printf '{"model":"auto","voice":"%s","text":"%s","format":"wav","sample_rate":24000,"stream":false}' "${TTS_VOICE}" "${TTS_TEXT}")" \
  "${BASE_URL}/v1/tts/synthesize" | pretty_print

if [[ -n "${ASR_FILE}" ]]; then
  echo
  echo "Checking batch ASR at ${BASE_URL}/v1/asr/transcribe using ${ASR_FILE}"
  curl -fsS \
    -X POST \
    -F "file=@${ASR_FILE}" \
    -F "model=auto" \
    -F "task=transcribe" \
    -F "language=auto" \
    -F "timestamps=true" \
    -F "storage_mode=persist" \
    -F 'metadata={"source":"smoke_test"}' \
    "${BASE_URL}/v1/asr/transcribe" | pretty_print
fi
