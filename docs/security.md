# Security

The local stack defaults to optional auth for operator convenience. Production deployments should enable strict auth, seed real tenants and API keys, and scope access per route:

- `voice:asr`
- `voice:tts`
- `voice:sessions:read`
- `voice:metrics:read`
- `voice:triage`

Data controls available in the code:

- no-persist mode
- tenant-aware storage keys
- audit trail for triage outputs
- Redis hot state with explicit session end handling
