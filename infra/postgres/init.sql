CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS tenants (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS api_keys (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  key_hash TEXT NOT NULL,
  label TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_sessions (
  id TEXT PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  session_type TEXT NOT NULL,
  model_requested TEXT,
  model_used TEXT,
  status TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS voice_requests (
  id TEXT PRIMARY KEY,
  session_id TEXT REFERENCES voice_sessions(id),
  request_type TEXT NOT NULL,
  route TEXT NOT NULL,
  model_requested TEXT,
  model_used TEXT,
  status TEXT NOT NULL,
  audio_duration_ms INT,
  queue_ms INT,
  preprocess_ms INT,
  inference_ms INT,
  postprocess_ms INT,
  total_ms INT,
  fallback_used BOOLEAN NOT NULL DEFAULT FALSE,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transcripts (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES voice_sessions(id),
  language_detected TEXT,
  text TEXT NOT NULL,
  segments JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS triage_results (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES voice_sessions(id),
  domain TEXT NOT NULL,
  classification TEXT NOT NULL,
  priority NUMERIC(5,4),
  analysis TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  requires_human_review BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tts_outputs (
  id TEXT PRIMARY KEY,
  session_id TEXT REFERENCES voice_sessions(id),
  model_used TEXT NOT NULL,
  voice TEXT,
  text_input TEXT NOT NULL,
  output_uri TEXT,
  duration_ms INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO tenants (id, name)
VALUES ('00000000-0000-0000-0000-000000000001', 'Local Demo Tenant')
ON CONFLICT (id) DO NOTHING;
