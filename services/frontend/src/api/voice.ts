import { apiFetch } from "./client";
import type { VoiceTurnResponse } from "../types/api";

export async function generateVoiceTurn(payload: Record<string, unknown>): Promise<VoiceTurnResponse> {
  return apiFetch<VoiceTurnResponse>("/v1/voice/turn", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}
