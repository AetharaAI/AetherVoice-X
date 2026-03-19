

# Show which compose services are actually up.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  --profile moss-sfx \
  ps

# Scan recent logs for successful model boot vs OOM.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  --profile moss-sfx \
  logs --since=15m \
  | rg "Application startup complete|Uvicorn running|EngineCore|OutOfMemory|CUDA out of memory|exited with code"

# Snapshot GPU allocations in plain text.
nvidia-smi




# Stop everything in this compose project.
docker compose down

# Bring up the exact stack for:
# frontend + gateway + tts + asr + realtime moss + voice design + voxtral live ASR
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-voicegen \
  up -d --build
# Stage the actual code, env template, and operator scripts.
git add .env.example services/frontend/src/pages/TTSLive.tsx services/moss/app/main.py scripts/stack_*.sh

# Commit the known-good realtime defaults and resident-stack scripts.
git commit -m "set moss realtime defaults and add resident stack scripts"

# Push your branch/main.
git push origin main

# Get the latest pushed code.
git pull --rebase origin main

# Rebuild only the resident live stack:
# frontend, gateway, tts, asr, voxtral, moss, voice generator
./scripts/stack_resident_rebuild.sh

# Verify the resident stack is actually healthy.
./scripts/stack_status.sh

# If you want to watch the important logs.
./scripts/stack_logs_resident.sh

