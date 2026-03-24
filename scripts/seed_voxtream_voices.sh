#!/usr/bin/env bash
# seed_voxtream_voices.sh
# -----------------------
# Registers voxtream2 reference WAVs from audio-refs into the Studio voice registry.
# Run ONCE on the VM after git pull + docker compose build tts + docker compose up -d tts.
#
# Usage:
#   bash scripts/seed_voxtream_voices.sh
#
# Optional overrides (env vars):
#   GATEWAY_URL   - default: http://127.0.0.1:8010
#   TENANT_ID     - default: default  
#   AUDIO_REFS    - default: auto-detected sibling voxtream-experiments/audio-refs

set -euo pipefail

GATEWAY_URL="${GATEWAY_URL:-http://127.0.0.1:8010}"
TENANT_ID="${TENANT_ID:-default}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
AUDIO_REFS="${AUDIO_REFS:-$(dirname "$REPO_ROOT")/voxtream-experiments/audio-refs}"

IMPORT_URL="${GATEWAY_URL}/api/v1/tts/studio/voices/import"
VOICES_URL="${GATEWAY_URL}/api/v1/tts/studio/voices"

echo "[SEED] Gateway:   $GATEWAY_URL"
echo "[SEED] Tenant:    $TENANT_ID"
echo "[SEED] Audio-refs: $AUDIO_REFS"
echo ""

if [[ ! -d "$AUDIO_REFS" ]]; then
  echo "[ERROR] audio-refs directory not found: $AUDIO_REFS"
  exit 1
fi

# Check if a voice_id is already registered
is_registered() {
  local voice_id="$1"
  curl -sf \
    -H "X-Tenant-Id: $TENANT_ID" \
    -H "X-Request-Id: seed-check" \
    -H "X-Session-Id: seed" \
    "$VOICES_URL" 2>/dev/null \
  | grep -q "\"$voice_id\""
}

# Import one voice
import_voice() {
  local file="$1"
  local display_name="$2"
  local voice_id="$3"
  local tags="$4"
  local notes="$5"

  if [[ ! -f "$file" ]]; then
    echo "  [SKIP] $display_name — file not found: $file"
    return
  fi

  if is_registered "$voice_id"; then
    echo "  [SKIP] $display_name ($voice_id) — already registered"
    return
  fi

  echo "  [IMPORT] $display_name  ($voice_id)"
  local response
  response=$(curl -sf \
    -H "X-Tenant-Id: $TENANT_ID" \
    -H "X-Request-Id: seed-$voice_id" \
    -H "X-Session-Id: seed" \
    -F "file=@${file};type=audio/wav" \
    -F "display_name=$display_name" \
    -F "voice_id=$voice_id" \
    -F "source_model=imported" \
    -F "runtime_target=voxtream2_realtime" \
    -F "voice_type=imported" \
    -F "tags=$tags" \
    -F "notes=$notes" \
    "$IMPORT_URL" 2>&1) || {
      echo "    [FAIL] HTTP error — check gateway logs"
      return
    }

  if echo "$response" | grep -q "\"voice_id\""; then
    echo "    [OK] Registered"
  else
    echo "    [FAIL] Unexpected response: ${response:0:200}"
  fi
}

# ── Female voices ──────────────────────────────────────────────────────────────
import_voice \
  "$AUDIO_REFS/Calmer-upbeat-female-host.wav" \
  "Upbeat Host (Female)" \
  "vx2_upbeat_host_female" \
  "voxtream2,telephony,female,upbeat,host" \
  "Calmer upbeat female host cadence. Good for on-hold, IVR, and intake flows."

import_voice \
  "$AUDIO_REFS/Soothing-female-nice.wav" \
  "Soothing (Female)" \
  "vx2_soothing_female" \
  "voxtream2,telephony,female,soothing,warm" \
  "Warm and soothing female voice. Good for patient care or calming service flows."

import_voice \
  "$AUDIO_REFS/between-fast&slow-chill-female.wav" \
  "Chill Mid-Pace (Female)" \
  "vx2_chill_midpace_female" \
  "voxtream2,telephony,female,chill,natural" \
  "Mid-pace chill female. Natural cadence between fast and slow."

import_voice \
  "$AUDIO_REFS/calm-nuetral-slight-english-accent-female.wav" \
  "Calm Neutral Accent (Female)" \
  "vx2_calm_accent_female" \
  "voxtream2,telephony,female,calm,neutral,accent" \
  "Calm neutral female with a slight English accent. Professional and approachable."

import_voice \
  "$AUDIO_REFS/slower-chill-female-decent.wav" \
  "Slower Chill (Female)" \
  "vx2_slower_chill_female" \
  "voxtream2,telephony,female,slow,chill" \
  "Slower chill female cadence. Works well for deliberate, clear service delivery."

import_voice \
  "$AUDIO_REFS/bella_voice_ref.wav" \
  "Bella (Female)" \
  "vx2_bella_female" \
  "voxtream2,telephony,female,reference" \
  "Bella reference voice from initial voxtream2 curl tests."

# ── Male voices ────────────────────────────────────────────────────────────────
import_voice \
  "$AUDIO_REFS/CJ-02-26-2026-Test.wav" \
  "CJ (Clone - Male)" \
  "vx2_cj_clone_male" \
  "voxtream2,telephony,male,clone,owner" \
  "Deliberate even-paced clone voice recorded for zero-shot cloning tests."

import_voice \
  "$AUDIO_REFS/deep-gruff-male.wav" \
  "Deep Gruff (Male)" \
  "vx2_deep_gruff_male" \
  "voxtream2,telephony,male,deep,gruff,authoritative" \
  "Deep gruff male voice. Good for security, dispatch, and assertive service agents."

import_voice \
  "$AUDIO_REFS/Adam-voice-ref.wav" \
  "Adam (Male)" \
  "vx2_adam_male" \
  "voxtream2,telephony,male,reference" \
  "Adam reference voice from initial voxtream2 curl tests."

# Adam-voice-ref-wrong script.wav  ← excluded intentionally

echo ""
echo "[SEED] Done. Open TTS Live, select voxtream2_realtime, and check the voice dropdown."
