import { useEffect, useMemo, useState } from "react";

import { fetchModels } from "../api/sessions";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import type { ModelInfo } from "../types/api";

interface ExternalModelResource {
  name: string;
  full_name: string;
  base_url: string;
  status: string;
  provider: string;
  capabilities: string[];
}

function parseExternalModels(): { resources: ExternalModelResource[]; error: string | null } {
  const raw = import.meta.env.VITE_EXTERNAL_MODELS_JSON;
  if (!raw) {
    return { resources: [], error: null };
  }
  try {
    const parsed = JSON.parse(raw) as ExternalModelResource[];
    const resources = parsed.filter((resource) => (
      resource.name
      && resource.full_name
      && resource.base_url
      && resource.status
      && resource.provider
      && Array.isArray(resource.capabilities)
    ));
    return { resources, error: null };
  } catch (error) {
    return {
      resources: [],
      error: error instanceof Error ? error.message : "invalid external model configuration",
    };
  }
}

function statusTone(status: string): "default" | "good" | "warn" | "danger" {
  const normalized = status.toLowerCase();
  if (normalized === "live" || normalized === "active" || normalized === "connected") {
    return "good";
  }
  if (normalized === "degraded" || normalized === "pending") {
    return "warn";
  }
  if (normalized === "offline" || normalized === "error") {
    return "danger";
  }
  return "default";
}

export function Models() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const externalModels = useMemo(() => parseExternalModels(), []);

  useEffect(() => {
    fetchModels().then(setModels).catch(() => undefined);
  }, []);

  return (
    <div className="page-grid">
      <Panel title="Loaded and scaffolded adapters" eyebrow="Models">
        <div className="cards-grid">
          {models.map((model) => (
            <article key={model.name} className="model-card">
              <header>
                <h3>{model.name}</h3>
                <Badge value={model.status} tone={model.status === "ready" ? "good" : "warn"} />
              </header>
              <p>{model.kind.toUpperCase()}</p>
              <p>Route priority: {model.route_priority}</p>
              <p>Features: {model.features.join(", ") || "none"}</p>
              <p>Streaming: {String(model.supports_streaming)}</p>
              <p>Batch: {String(model.supports_batch)}</p>
            </article>
          ))}
        </div>
      </Panel>
      <Panel title="External model resources" eyebrow="Agent Models">
        {externalModels.error ? <p className="error-text">{externalModels.error}</p> : null}
        {externalModels.resources.length ? (
          <div className="cards-grid">
            {externalModels.resources.map((resource) => (
              <article key={resource.name} className="model-card">
                <header className="detail-card-header">
                  <div>
                    <h3>{resource.name}</h3>
                    <p className="muted">{resource.full_name}</p>
                  </div>
                  <Badge value={resource.status} tone={statusTone(resource.status)} />
                </header>
                <p>{resource.provider}</p>
                <div className="artifact-list">
                  <div className="artifact-row">
                    <span>Base API</span>
                    <code className="inline-code">{resource.base_url}</code>
                  </div>
                </div>
                <div className="toolbar">
                  {resource.capabilities.map((capability) => (
                    <Badge key={`${resource.name}-${capability}`} value={capability} />
                  ))}
                </div>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">No external model resources are configured in `VITE_EXTERNAL_MODELS_JSON`.</p>
        )}
      </Panel>
    </div>
  );
}
