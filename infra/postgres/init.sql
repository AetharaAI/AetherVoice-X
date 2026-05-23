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

CREATE TABLE IF NOT EXISTS scriber_installs (
  install_id TEXT PRIMARY KEY,
  first_seen_app_version TEXT,
  last_seen_app_version TEXT,
  platform TEXT NOT NULL DEFAULT 'linux',
  email TEXT,
  stripe_customer_id TEXT,
  last_checkout_session_id TEXT,
  free_seconds_granted INT NOT NULL DEFAULT 1800,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scriber_entitlements (
  install_id TEXT PRIMARY KEY REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
  plan_slug TEXT NOT NULL,
  status TEXT NOT NULL,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  stripe_checkout_session_id TEXT,
  cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scriber_checkout_sessions (
  checkout_session_id TEXT PRIMARY KEY,
  install_id TEXT NOT NULL REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
  plan_slug TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  checkout_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS scriber_usage_ledger (
  ledger_id TEXT PRIMARY KEY,
  install_id TEXT NOT NULL REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
  session_id TEXT,
  metric TEXT NOT NULL,
  quantity_seconds INT NOT NULL,
  source TEXT NOT NULL DEFAULT 'gateway',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO tenants (id, name)
VALUES ('00000000-0000-0000-0000-000000000001', 'Local Demo Tenant')
ON CONFLICT (id) DO NOTHING;
