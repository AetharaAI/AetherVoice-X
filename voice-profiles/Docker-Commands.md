No, you do not need to rebuild the whole thing for the latest code pass.

The latest functional changes were in:
- `frontend`
- `tts`
- `moss`

So the minimum rebuild is:

```bash
# Rebuild and restart only the services changed by the latest realtime-conditioning work.
docker compose --profile moss up -d --build frontend tts moss
```

If you also changed `.env` values that affect other services, recreate those too. If you want the safer “don’t make me think” version, include `gateway`:

```bash
# Same as above, but also recreates gateway so the API edge is definitely aligned.
docker compose --profile moss up -d --build frontend gateway tts moss
```

The compose layout is defined in [docker-compose.yml](/home/cory/Aether-Voice-Platform/Aether-Voice-X/docker-compose.yml). The optional profile services are:
- `voxtral`
- `moss`
- `moss-tts`
- `moss-ttsd`
- `moss-voicegen`
- `moss-sfx`
- `local-edge`

The always-on base services are:
- `frontend`
- `gateway`
- `asr`
- `tts`
- `redis`
- `postgres`
- `minio`
- `prometheus`
- `grafana`

**Operator Cheat Sheet**

```bash
# Show what is running right now.
docker compose ps

# Show full container list, including profile-backed services that may be up.
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# Follow logs for the main app edge.
docker compose logs -f frontend gateway tts asr

# Follow logs for realtime MOSS only.
docker compose --profile moss logs -f moss

# Follow logs for Voice Generator only.
docker compose --profile moss-voicegen logs -f moss-voice-generator
```

**Start Base Stack**

```bash
# Start the core app stack without optional model sidecars.
docker compose up -d --build

# Start the core stack without rebuilding images.
docker compose up -d
```

**Start Common Working Layouts**

```bash
# Base stack + realtime MOSS.
docker compose --profile moss up -d --build

# Base stack + realtime MOSS + Voice Generator.
docker compose --profile moss --profile moss-voicegen up -d --build

# Base stack + realtime MOSS + Voice Generator + TTSD + base TTS.
docker compose \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  up -d --build

# Base stack + Voxtral ASR sidecar.
docker compose --profile voxtral up -d --build

# Full in-repo optional model surface.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  --profile moss-sfx \
  up -d --build

# Base stack + local nginx edge inside compose.
docker compose --profile local-edge up -d --build
```

**Start Specific Pieces Only**

```bash
# Start only realtime MOSS sidecar.
docker compose --profile moss up -d --build moss

# Start only Voice Generator sidecar.
docker compose --profile moss-voicegen up -d --build moss-voice-generator

# Start only MOSS base TTS sidecar.
docker compose --profile moss-tts up -d --build moss-tts

# Start only MOSS TTSD sidecar.
docker compose --profile moss-ttsd up -d --build moss-ttsd

# Start only Voxtral sidecar.
docker compose --profile voxtral up -d --build voxtral

# Start only frontend.
docker compose up -d --build frontend

# Start only gateway.
docker compose up -d --build gateway

# Start only TTS service.
docker compose up -d --build tts

# Start only ASR service.
docker compose up -d --build asr
```

**Rebuild Only What Changed**

```bash
# Latest realtime-conditioning code path.
docker compose --profile moss up -d --build frontend tts moss

# If you are testing studio voice design too.
docker compose --profile moss --profile moss-voicegen up -d --build frontend tts moss moss-voice-generator

# If you changed env only and want clean container recreation without image rebuild.
docker compose --profile moss up -d --force-recreate frontend tts moss
```

**Stop Parts Of The Stack**

```bash
# Stop one service without removing it.
docker compose stop frontend

# Stop realtime MOSS only.
docker compose stop moss

# Stop Voice Generator only.
docker compose stop moss-voice-generator

# Stop frontend, gateway, and tts together.
docker compose stop frontend gateway tts

# Stop everything managed by this compose project.
docker compose stop
```

**Remove / Tear Down**

```bash
# Remove only one service container.
docker compose rm -sf frontend

# Remove one sidecar container so the next up is a clean recreate.
docker compose rm -sf moss

# Tear down the whole compose project but keep named volumes.
docker compose down

# Tear down everything and remove orphan containers too.
docker compose down --remove-orphans

# Tear down everything and also delete Postgres/MinIO data volumes.
# Do not run this unless you intentionally want to wipe local state.
docker compose down -v
```

**Restart / Bounce**

```bash
# Restart one service in place.
docker compose restart tts

# Restart frontend, gateway, and tts together.
docker compose restart frontend gateway tts

# Bounce realtime MOSS after env changes.
docker compose restart moss
```

**Good Current Layout For You**

For your current VM workflow, these are the three most useful commands:

```bash
# 1. Bring up the normal app stack plus realtime MOSS.
docker compose --profile moss up -d --build frontend gateway tts asr moss

# 2. Add Voice Generator when you want studio voice design.
docker compose --profile moss-voicegen up -d --build moss-voice-generator

# 3. Rebuild only the latest changed services after a pull.
docker compose --profile moss up -d --build frontend tts moss
```

**Mental Model**

- `docker compose up -d --build` starts base services and rebuilds images as needed.
- `--profile X` only adds services tagged with that profile.
- If you do not name services at the end, Compose starts everything in the selected base/profile set.
- If you do name services, Compose only starts those named services, plus needed dependencies.

If you want, I can turn this into a checked-in `docs/docker-operations.md` or a `scripts/stack-cheatsheet.sh` next so you have it in-repo.
