# Deployment

## Local

1. Copy `.env.example` to `.env`.
2. Start `docker compose up --build`.
3. Verify `GET /v1/health` from the gateway.

## Production notes

- Replace `AUTH_MODE=optional` with `AUTH_MODE=strict`.
- Rotate JWT secrets and API keys.
- Put the gateway behind TLS and your upstream identity provider.
- Run ASR and TTS workers on nodes with the right CPU/GPU profile for the selected models.
- Move MinIO, Postgres, and Redis to managed or clustered deployments if you need HA.
