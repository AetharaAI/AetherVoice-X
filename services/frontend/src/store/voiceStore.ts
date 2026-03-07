import { create } from "zustand";

import type { HealthResponse, ModelInfo, SessionSummary } from "../types/api";

interface VoiceState {
  health?: HealthResponse;
  models: ModelInfo[];
  sessions: SessionSummary[];
  setHealth: (health: HealthResponse) => void;
  setModels: (models: ModelInfo[]) => void;
  setSessions: (sessions: SessionSummary[]) => void;
}

export const useVoiceStore = create<VoiceState>((set) => ({
  models: [],
  sessions: [],
  setHealth: (health) => set({ health }),
  setModels: (models) => set({ models }),
  setSessions: (sessions) => set({ sessions })
}));
