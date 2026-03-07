import { useEffect, useState } from "react";

import { fetchHealth, fetchModels, fetchSessions } from "../api/sessions";
import { Panel } from "../components/common/Panel";
import { StatCard } from "../components/common/StatCard";
import { useVoiceStore } from "../store/voiceStore";

export function Dashboard() {
  const { health, models, sessions, setHealth, setModels, setSessions } = useVoiceStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([fetchHealth(), fetchModels(), fetchSessions()])
      .then(([healthPayload, modelPayload, sessionPayload]) => {
        setHealth(healthPayload);
        setModels(modelPayload);
        setSessions(sessionPayload);
      })
      .catch((err: Error) => setError(err.message));
  }, [setHealth, setModels, setSessions]);

  const degradedDeps = Object.values(health?.dependencies ?? {}).filter((value) => value !== "ok").length;
  const streamingModels = models.filter((model) => model.supports_streaming).length;

  return (
    <div className="page-grid">
      <Panel title="Platform snapshot" eyebrow="Dashboard">
        <div className="stat-grid">
          <StatCard label="Gateway health" value={health?.status ?? "loading"} tone={health?.status === "ok" ? "good" : "danger"} />
          <StatCard label="Active sessions" value={String(sessions.filter((session) => session.status === "active").length)} />
          <StatCard label="Model lanes" value={String(models.length)} />
          <StatCard label="Degraded deps" value={String(degradedDeps)} tone={degradedDeps ? "danger" : "good"} />
          <StatCard label="Realtime-ready" value={String(streamingModels)} />
          <StatCard label="Failures last hour" value="Use metrics page" />
        </div>
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>

      <Panel title="Recent sessions" eyebrow="Session memory">
        <div className="list-table">
          {sessions.slice(0, 6).map((session) => (
            <div key={session.id} className="list-row">
              <strong>{session.id}</strong>
              <span>{session.session_type}</span>
              <span>{session.model_used ?? session.model_requested}</span>
              <span>{session.status}</span>
            </div>
          ))}
        </div>
      </Panel>

      <Panel title="Model availability" eyebrow="Route inventory">
        <div className="cards-grid">
          {models.map((model) => (
            <article key={model.name} className="mini-card">
              <h3>{model.name}</h3>
              <p>{model.kind.toUpperCase()}</p>
              <p>{model.features.join(", ")}</p>
            </article>
          ))}
        </div>
      </Panel>
    </div>
  );
}
