import { apiFetch, getApiBase } from "./client";
import type { HealthResponse, ModelInfo, SessionDetail, SessionSummary } from "../types/api";

export async function fetchHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/v1/health");
}

export async function fetchModels(): Promise<ModelInfo[]> {
  const payload = await apiFetch<{ models: ModelInfo[] }>("/v1/models");
  return payload.models;
}

export async function fetchSessions(): Promise<SessionSummary[]> {
  const payload = await apiFetch<{ sessions: SessionSummary[] }>("/v1/sessions");
  return payload.sessions;
}

export async function fetchSessionDetail(sessionId: string): Promise<SessionDetail> {
  return apiFetch<SessionDetail>(`/v1/sessions/${sessionId}`);
}

export async function endSession(sessionId: string) {
  return apiFetch(`/v1/sessions/${sessionId}/end`, { method: "POST" });
}

export async function fetchMetricsRaw(): Promise<string> {
  const response = await fetch(`${getApiBase()}/v1/metrics`);
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.text();
}
