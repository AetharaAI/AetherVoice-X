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
}

export interface TTSResponse {
  request_id: string;
  model_used: string;
  audio_url: string;
  duration_ms: number;
  timings: TimingBreakdown;
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

export interface SessionDetail {
  session: SessionSummary;
  requests: Record<string, unknown>[];
  transcripts: Record<string, unknown>[];
  triage_results: Record<string, unknown>[];
  tts_outputs: Record<string, unknown>[];
}

export interface StreamStartResponse {
  session_id: string;
  ws_url: string;
  expires_in_seconds?: number;
}
