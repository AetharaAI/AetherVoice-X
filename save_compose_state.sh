#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="${1:-$(pwd)}"
OUT_DIR="${2:-$HOME/state-snapshots}"

mkdir -p "$OUT_DIR"

TS="$(date +"%Y-%m-%d_%H-%M-%S")"
HOST="$(hostname)"
OUT_FILE="$OUT_DIR/compose-state_${HOST}_${TS}.log"

cd "$REPO_DIR"

{
  echo "===== HOST ====="
  hostname
  echo

  echo "===== TIME ====="
  date
  echo

  echo "===== REPO DIR ====="
  pwd
  echo

  echo "===== DOCKER COMPOSE PS ====="
  docker compose ps
  echo

  echo "===== DOCKER COMPOSE CONFIG SERVICES ====="
  docker compose config --services
  echo
} | tee "$OUT_FILE"

echo
echo "Saved compose state to: $OUT_FILE"