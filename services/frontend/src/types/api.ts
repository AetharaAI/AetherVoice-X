export interface TimingBreakdown {
  queue_ms?: number;
  preprocess_ms?: number;
  inference_ms?: number;
  postprocess_ms?: number;
  total_ms?: number;
  encode_ms?: number;
}

export interface ASRSegment {
  segment_id?: string;
  start_ms: number;
  end_ms: number;
  text: string;
  confidence?: number;
}

export interface ASRResponse {
  request_id: string;
  session_id: string;
  task: string;
  model_requested: string;
  model_used: string;
  language_detected?: string;
  duration_ms: number;
  text: string;
  segments: ASRSegment[];
  timings: TimingBreakdown;
  artifacts: Record<string, string>;
}

export interface TTSResponse {
  request_id: string;
  session_id: string;
  model_used: string;
  audio_url: string;
  duration_ms: number;
  timings: TimingBreakdown;
  artifacts: Record<string, string>;
}

export interface HealthResponse {
  status: string;
  service: string;
  dependencies: Record<string, string>;
}

export interface ModelInfo {
  name: string;
  kind: string;
  supports_streaming: boolean;
  supports_batch: boolean;
  status: string;
  features: string[];
  route_priority: number;
  memory_footprint?: string;
}

export interface SessionSummary {
  id: string;
  tenant_id: string;
  session_type: string;
  model_requested?: string;
  model_used?: string;
  status: string;
  started_at: string;
  ended_at?: string | null;
  metadata: Record<string, unknown>;
}

export interface RequestRecord {
  id: string;
  session_id?: string | null;
  request_type: string;
  route: string;
  model_requested?: string | null;
  model_used?: string | null;
  status: string;
  audio_duration_ms?: number | null;
  queue_ms?: number | null;
  preprocess_ms?: number | null;
  inference_ms?: number | null;
  postprocess_ms?: number | null;
  total_ms?: number | null;
  fallback_used?: boolean | null;
  error_message?: string | null;
  created_at?: string;
}

export interface TranscriptRecord {
  id: string;
  session_id: string;
  language_detected?: string | null;
  text: string;
  segments: ASRSegment[];
  created_at?: string;
}

export interface TriageRecord {
  id: string;
  session_id: string;
  domain: string;
  classification: string;
  priority?: number | null;
  analysis: string;
  recommended_action: string;
  requires_human_review: boolean;
  created_at?: string;
}

export interface TTSOutputRecord {
  id: string;
  session_id?: string | null;
  model_used: string;
  voice?: string | null;
  text_input: string;
  output_uri?: string | null;
  duration_ms?: number | null;
  created_at?: string;
}

export interface SessionDetail {
  session: SessionSummary;
  requests: RequestRecord[];
  transcripts: TranscriptRecord[];
  triage_results: TriageRecord[];
  tts_outputs: TTSOutputRecord[];
}

export interface StreamStartResponse {
  session_id: string;
  ws_url: string;
  expires_in_seconds?: number;
  model_requested?: string | null;
  model_used?: string | null;
  fallback_used?: boolean;
}

export interface StudioVoice {
  voice_id: string;
  display_name: string;
  tenant_id?: string | null;
  type: "preset" | "cloned" | "generated" | "imported" | "fallback";
  source_model: string;
  runtime_target: "moss_realtime" | "moss_tts" | "moss_ttsd" | "moss_voice_generator" | "chatterbox";
  reference_audio_path?: string | null;
  reference_text?: string | null;
  generation_prompt?: string | null;
  sample_rate: number;
  language: string;
  tags: string[];
  default_params: Record<string, unknown>;
  notes?: string | null;
}

export interface StudioRouteDescriptor {
  name: "moss_realtime" | "moss_tts" | "moss_ttsd" | "moss_voice_generator" | "chatterbox";
  label: string;
  mode: "stream" | "batch" | "dialogue" | "voice-design";
  status: "ready" | "configured" | "staged" | "missing";
  model_path?: string | null;
  notes?: string | null;
  fallback_target?: string | null;
}

export interface LLMProviderSummary {
  provider: "openai" | "openrouter" | "litellm" | "anthropic";
  label: string;
  enabled: boolean;
  base_url?: string | null;
  auth_configured: boolean;
  notes?: string | null;
}

export interface LLMProviderModel {
  id: string;
  label: string;
  provider: "openai" | "openrouter" | "litellm" | "anthropic";
}

export interface LLMRoutingConfig {
  provider: "openai" | "openrouter" | "litellm" | "anthropic";
  model?: string | null;
  base_url?: string | null;
  enabled: boolean;
  mode: "manual" | "asr_llm_tts" | "shadow";
  system_prompt?: string | null;
  metadata: Record<string, unknown>;
}

export interface ExamplePreset {
  title: string;
  description: string;
  tags: string[];
  generation_prompt: string;
}

export interface StudioOverview {
  routes: StudioRouteDescriptor[];
  voices: StudioVoice[];
  providers: LLMProviderSummary[];
  routing: LLMRoutingConfig;
  example_presets: ExamplePreset[];
  canonical_model_root: string;
}
