#!/usr/bin/env bash
set -Eeuo pipefail

echo "===== HOST ====="
hostname
echo

echo "===== TIME ====="
date
echo

echo "===== KERNEL / REBOOT STATUS ====="
uname -r
if [ -f /var/run/reboot-required ]; then
  echo "REBOOT REQUIRED: yes"
  cat /var/run/reboot-required || true
else
  echo "REBOOT REQUIRED: no marker file found"
fi
echo

echo "===== RUNNING CONTAINERS ====="
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
echo

echo "===== RESTART POLICIES (RUNNING CONTAINERS) ====="
RUNNING_CONTAINERS="$(docker ps -q || true)"
if [ -n "${RUNNING_CONTAINERS}" ]; then
  docker inspect ${RUNNING_CONTAINERS} \
    --format '{{.Name}} -> restart={{.HostConfig.RestartPolicy.Name}}'
else
  echo "No running containers."
fi
echo

echo "===== CONTAINERS THAT WILL NOT AUTO-RETURN ====="
if [ -n "${RUNNING_CONTAINERS}" ]; then
  docker inspect ${RUNNING_CONTAINERS} \
    --format '{{.Name}} -> restart={{.HostConfig.RestartPolicy.Name}}' \
    | grep 'restart=no' || true
else
  echo "No running containers."
fi
echo

echo "===== NVIDIA-SMI ====="
nvidia-smi || echo "nvidia-smi not available"
echo