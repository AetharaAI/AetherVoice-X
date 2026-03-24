#!/usr/bin/env python3
"""
seed_voxtream_voices.py
-----------------------
Registers pre-built reference WAVs from the voxtream-experiments/audio-refs
directory into the Aether TTS Studio voice registry so they appear in the
TTS Live reference-voice dropdown immediately after the TTS container restarts.

Run this ONCE on the VM after 'docker compose up -d tts':

    python3 scripts/seed_voxtream_voices.py

It hits the gateway's /api/v1/tts/studio/voices/import endpoint for each WAV.
Voices that are already registered (same voice_id) are skipped.

The script reads WAVs from the path set by VOXTREAM_AUDIO_REFS_DIR
(defaults to the sibling voxtream-experiments/audio-refs directory).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Config — override via env vars
# ---------------------------------------------------------------------------

GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://127.0.0.1:8010")
TENANT_ID = os.getenv("SEED_TENANT_ID", "default")

# Absolute path to the voxtream-experiments audio-refs dir
_THIS_DIR = Path(__file__).resolve().parent
_DEFAULT_REFS = _THIS_DIR.parent.parent / "voxtream-experiments" / "audio-refs"
AUDIO_REFS_DIR = Path(os.getenv("VOXTREAM_AUDIO_REFS_DIR", str(_DEFAULT_REFS)))

# ---------------------------------------------------------------------------
# Voice definitions — keyed by stem so they survive filename changes
# ---------------------------------------------------------------------------
# fmt: off
VOICE_MAP: dict[str, dict] = {
    # --- Female voices ---
    "Calmer-upbeat-female-host": {
        "display_name": "Upbeat Host (Female)",
        "voice_id":     "vx2_upbeat_host_female",
        "tags":         "voxtream2, telephony, female, upbeat, host",
        "notes":        "Calmer upbeat female host cadence. Good for on-hold, IVR, and intake flows.",
    },
    "Soothing-female-nice": {
        "display_name": "Soothing (Female)",
        "voice_id":     "vx2_soothing_female",
        "tags":         "voxtream2, telephony, female, soothing, warm",
        "notes":        "Warm and soothing female voice. Good for patient care or calming service flows.",
    },
    "between-fast&slow-chill-female": {
        "display_name": "Chill Mid-Pace (Female)",
        "voice_id":     "vx2_chill_midpace_female",
        "tags":         "voxtream2, telephony, female, chill, natural",
        "notes":        "Mid-pace chill female. Natural cadence between fast and slow; good for conversational agents.",
    },
    "calm-nuetral-slight-english-accent-female": {
        "display_name": "Calm Neutral Accent (Female)",
        "voice_id":     "vx2_calm_accent_female",
        "tags":         "voxtream2, telephony, female, calm, neutral, accent",
        "notes":        "Calm neutral female with a slight English accent. Professional and approachable.",
    },
    "slower-chill-female-decent": {
        "display_name": "Slower Chill (Female)",
        "voice_id":     "vx2_slower_chill_female",
        "tags":         "voxtream2, telephony, female, slow, chill",
        "notes":        "Slower chill female cadence. Works well for deliberate, clear service delivery.",
    },
    "bella_voice_ref": {
        "display_name": "Bella (Female)",
        "voice_id":     "vx2_bella_female",
        "tags":         "voxtream2, telephony, female, reference",
        "notes":        "Bella reference voice from initial voxtream2 curl tests.",
    },
    # --- Male voices ---
    "CJ-02-26-2026-Test": {
        "display_name": "CJ (Clone — Male)",
        "voice_id":     "vx2_cj_clone_male",
        "tags":         "voxtream2, telephony, male, clone, owner",
        "notes":        "Deliberate even-paced clone voice recorded for zero-shot cloning tests. "
                        "Careful pacing and enunciation optimized for voxtream2 identity locking.",
    },
    "deep-gruff-male": {
        "display_name": "Deep Gruff (Male)",
        "voice_id":     "vx2_deep_gruff_male",
        "tags":         "voxtream2, telephony, male, deep, gruff, authoritative",
        "notes":        "Deep gruff male voice. Good for security, dispatch, and assertive service agents.",
    },
    "Adam-voice-ref": {
        "display_name": "Adam (Male)",
        "voice_id":     "vx2_adam_male",
        "tags":         "voxtream2, telephony, male, reference",
        "notes":        "Adam reference voice from initial voxtream2 curl tests.",
    },
    # Adam-voice-ref-wrong script.wav  ← deliberately excluded
}
# fmt: on

COMMON = {
    "source_model": "imported",
    "runtime_target": "voxtream2_realtime",
    "voice_type": "imported",
}


def _already_registered(client: httpx.Client, voice_id: str) -> bool:
    resp = client.get(
        "/api/v1/tts/studio/voices",
        headers={"X-Tenant-Id": TENANT_ID, "X-Request-Id": "seed-check", "X-Session-Id": "seed"},
    )
    if not resp.is_success:
        return False
    voices = resp.json().get("voices", [])
    return any(v.get("voice_id") == voice_id for v in voices)


def main() -> None:
    if not AUDIO_REFS_DIR.exists():
        print(f"[SEED] ERROR: audio-refs dir not found: {AUDIO_REFS_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"[SEED] Gateway: {GATEWAY_BASE_URL}")
    print(f"[SEED] Tenant:  {TENANT_ID}")
    print(f"[SEED] WAV dir: {AUDIO_REFS_DIR}")
    print()

    skipped = 0
    imported = 0
    failed = 0

    with httpx.Client(base_url=GATEWAY_BASE_URL, timeout=30) as client:
        for stem, meta in VOICE_MAP.items():
            wav_path = AUDIO_REFS_DIR / f"{stem}.wav"
            if not wav_path.exists():
                print(f"  [SKIP] {stem}.wav — file not found, skipping")
                skipped += 1
                continue

            voice_id = meta["voice_id"]
            if _already_registered(client, voice_id):
                print(f"  [SKIP] {meta['display_name']} ({voice_id}) — already in registry")
                skipped += 1
                continue

            print(f"  [IMPORT] {meta['display_name']}  ({voice_id})  ← {wav_path.name}")
            with wav_path.open("rb") as fh:
                resp = client.post(
                    "/api/v1/tts/studio/voices/import",
                    headers={
                        "X-Tenant-Id": TENANT_ID,
                        "X-Request-Id": f"seed-{voice_id}",
                        "X-Session-Id": "seed",
                    },
                    data={
                        "display_name":   meta["display_name"],
                        "voice_id":       voice_id,
                        "source_model":   COMMON["source_model"],
                        "runtime_target": COMMON["runtime_target"],
                        "voice_type":     COMMON["voice_type"],
                        "tags":           meta["tags"],
                        "notes":          meta["notes"],
                    },
                    files={"file": (wav_path.name, fh, "audio/wav")},
                )
            if resp.is_success:
                result = resp.json()
                print(f"         ✓ registered as {result.get('voice_id')} — {result.get('display_name')}")
                imported += 1
            else:
                print(f"         ✗ FAILED {resp.status_code}: {resp.text[:200]}")
                failed += 1

    print()
    print(f"[SEED] Done — {imported} imported, {skipped} skipped, {failed} failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
