#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "Checking gateway health at ${BASE_URL}/v1/health"
curl -fsS "${BASE_URL}/v1/health"

echo
echo "Checking model catalog at ${BASE_URL}/v1/models"
curl -fsS "${BASE_URL}/v1/models"
