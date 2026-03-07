import { apiFetch } from "./client";
import type { StreamStartResponse, TTSResponse } from "../types/api";

export async function synthesizeText(payload: Record<string, unknown>): Promise<TTSResponse> {
  return apiFetch<TTSResponse>("/v1/tts/synthesize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function startTTSStream(payload: Record<string, unknown>): Promise<StreamStartResponse> {
  return apiFetch<StreamStartResponse>("/v1/tts/stream/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}
