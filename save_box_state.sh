#!/usr/bin/env bash
set -Eeuo pipefail

OUT_DIR="${1:-$HOME/state-snapshots}"
mkdir -p "$OUT_DIR"

TS="$(date +"%Y-%m-%d_%H-%M-%S")"
HOST="$(hostname)"
OUT_FILE="$OUT_DIR/box-state_${HOST}_${TS}.log"

{
  echo "===== HOST ====="
  hostname
  echo

  echo "===== TIME ====="
  date
  echo

  echo "===== PWD ====="
  pwd
  echo

  echo "===== DOCKER PS -A ====="
  docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
  echo

  echo "===== DOCKER RESTART POLICIES (RUNNING CONTAINERS) ====="
  RUNNING_CONTAINERS="$(docker ps -q || true)"
  if [ -n "${RUNNING_CONTAINERS}" ]; then
    docker inspect ${RUNNING_CONTAINERS} \
      --format '{{.Name}} -> restart={{.HostConfig.RestartPolicy.Name}}'
  else
    echo "No running containers."
  fi
  echo

  echo "===== NVIDIA-SMI ====="
  nvidia-smi || echo "nvidia-smi not available"
  echo

  echo "===== GPU PROCESS QUERY ====="
  nvidia-smi --query-compute-apps=pid,gpu_uuid,used_memory,process_name --format=csv \
    || echo "GPU process query unavailable"
  echo
} | tee "$OUT_FILE"

echo
echo "Saved box state to: $OUT_FILE"