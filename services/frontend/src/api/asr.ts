import { apiFetch } from "./client";
import type { ASRResponse, StreamStartResponse } from "../types/api";

export async function transcribeFile(formData: FormData): Promise<ASRResponse> {
  return apiFetch<ASRResponse>("/v1/asr/transcribe", {
    method: "POST",
    body: formData
  });
}

export async function startASRStream(payload: Record<string, unknown>): Promise<StreamStartResponse> {
  return apiFetch<StreamStartResponse>("/v1/asr/stream/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function triageTranscript(payload: Record<string, unknown>) {
  return apiFetch<Record<string, unknown>>("/v1/asr/triage", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function analyzeTranscript(payload: Record<string, unknown>) {
  return apiFetch<Record<string, unknown>>("/v1/asr/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}
