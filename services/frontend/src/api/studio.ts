import { apiFetch } from "./client";
import type { LLMProviderModel, LLMProviderSummary, LLMRoutingConfig, StudioOverview, StudioVoice } from "../types/api";

export async function fetchStudioOverview(): Promise<StudioOverview> {
  return apiFetch<StudioOverview>("/v1/tts/studio/overview");
}

export async function fetchStudioVoices(): Promise<StudioVoice[]> {
  const payload = await apiFetch<{ voices: StudioVoice[] }>("/v1/tts/studio/voices");
  return payload.voices;
}

export async function createStudioVoice(payload: Record<string, unknown>): Promise<StudioVoice> {
  return apiFetch<StudioVoice>("/v1/tts/studio/voices", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function importStudioVoice(payload: FormData): Promise<StudioVoice> {
  return apiFetch<StudioVoice>("/v1/tts/studio/voices/import", {
    method: "POST",
    body: payload
  });
}

export async function fetchStudioProviders(): Promise<LLMProviderSummary[]> {
  const payload = await apiFetch<{ providers: LLMProviderSummary[] }>("/v1/tts/studio/providers");
  return payload.providers;
}

export async function fetchProviderModels(provider: string): Promise<LLMProviderModel[]> {
  const payload = await apiFetch<{ models: LLMProviderModel[] }>(`/v1/tts/studio/providers/${provider}/models`);
  return payload.models;
}

export async function fetchStudioRouting(): Promise<LLMRoutingConfig> {
  return apiFetch<LLMRoutingConfig>("/v1/tts/studio/routing");
}

export async function saveStudioRouting(payload: Record<string, unknown>): Promise<LLMRoutingConfig> {
  return apiFetch<LLMRoutingConfig>("/v1/tts/studio/routing", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}
