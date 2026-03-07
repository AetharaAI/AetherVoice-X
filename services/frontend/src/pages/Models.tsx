import { useEffect, useState } from "react";

import { fetchModels } from "../api/sessions";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import type { ModelInfo } from "../types/api";

export function Models() {
  const [models, setModels] = useState<ModelInfo[]>([]);

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
    </div>
  );
}
