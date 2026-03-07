import { useEffect, useState } from "react";

import { fetchHealth, fetchMetricsRaw, fetchModels, fetchSessions } from "../api/sessions";
import { Panel } from "../components/common/Panel";
import { StatCard } from "../components/common/StatCard";
import { formatDateTime, formatMs } from "../lib/format";
import { parsePrometheusMetrics } from "../lib/metrics";
import { useVoiceStore } from "../store/voiceStore";

export function Dashboard() {
  const { health, models, sessions, setHealth, setModels, setSessions } = useVoiceStore();
  const [error, setError] = useState<string | null>(null);
  const [metricsRaw, setMetricsRaw] = useState("");

  useEffect(() => {
    Promise.allSettled([fetchHealth(), fetchModels(), fetchSessions(), fetchMetricsRaw()]).then(([healthResult, modelsResult, sessionsResult, metricsResult]) => {
      const errors: string[] = [];

      if (healthResult.status === "fulfilled") {
        setHealth(healthResult.value);
      } else {
        errors.push(`health: ${healthResult.reason instanceof Error ? healthResult.reason.message : String(healthResult.reason)}`);
      }

      if (modelsResult.status === "fulfilled") {
        setModels(modelsResult.value);
      } else {
        errors.push(`models: ${modelsResult.reason instanceof Error ? modelsResult.reason.message : String(modelsResult.reason)}`);
      }

      if (sessionsResult.status === "fulfilled") {
        setSessions(sessionsResult.value);
      } else {
        errors.push(`sessions: ${sessionsResult.reason instanceof Error ? sessionsResult.reason.message : String(sessionsResult.reason)}`);
      }

      if (metricsResult.status === "fulfilled") {
        setMetricsRaw(metricsResult.value);
      } else {
        errors.push(`metrics: ${metricsResult.reason instanceof Error ? metricsResult.reason.message : String(metricsResult.reason)}`);
      }

      setError(errors.length ? errors.join(" | ") : null);
    });
  }, [setHealth, setModels, setSessions]);

  const degradedDeps = Object.values(health?.dependencies ?? {}).filter((value) => value !== "ok").length;
  const streamingModels = models.filter((model) => model.supports_streaming).length;
  const readyModels = models.filter((model) => model.status === "ready").length;
  const metrics = parsePrometheusMetrics(metricsRaw);
  const recentSessions = sessions.slice(0, 5);
  const topRoutes = metrics.routeCounts.slice(0, 4);

  return (
    <div className="page-grid">
      <Panel title="Platform snapshot" eyebrow="Dashboard">
        <div className="stat-grid">
          <StatCard label="Gateway health" value={health?.status ?? "loading"} tone={health?.status === "ok" ? "good" : "danger"} />
          <StatCard label="Active sessions" value={String(sessions.filter((session) => session.status === "active").length || metrics.activeSessions)} />
          <StatCard label="Request volume" value={String(metrics.requestCount)} />
          <StatCard label="Request errors" value={String(metrics.errorCount)} tone={metrics.errorCount ? "danger" : "good"} />
          <StatCard label="Degraded deps" value={String(degradedDeps)} tone={degradedDeps ? "danger" : "good"} />
          <StatCard label="Realtime-ready" value={String(streamingModels)} />
          <StatCard label="Avg latency" value={metrics.avgLatencyMs ? formatMs(Math.round(metrics.avgLatencyMs)) : "n/a"} />
        </div>
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>

      <Panel title="Recent sessions" eyebrow="Session memory">
        <div className="list-table">
          {recentSessions.length ? recentSessions.map((session) => (
            <div key={session.id} className="list-row">
              <strong>{session.id}</strong>
              <span>{session.session_type}</span>
              <span>{session.model_used ?? session.model_requested}</span>
              <span>{session.status} · {formatDateTime(session.started_at)}</span>
            </div>
          )) : <p className="muted">No persisted sessions yet. Run ASR or TTS to populate this lane.</p>}
        </div>
      </Panel>

      <Panel title="Operator summary" eyebrow="Route inventory">
        <div className="cards-grid">
          <article className="mini-card">
            <h3>Lane readiness</h3>
            <p>{readyModels} ready / {models.length} registered</p>
            <p>{streamingModels} streaming-capable lanes</p>
          </article>
          <article className="mini-card">
            <h3>Dependency state</h3>
            <p>ASR: {health?.dependencies.asr ?? "unknown"}</p>
            <p>TTS: {health?.dependencies.tts ?? "unknown"}</p>
          </article>
          <article className="mini-card">
            <h3>Top routes</h3>
            {topRoutes.length ? topRoutes.map((route) => <p key={route.route}>{route.route}: {route.value}</p>) : <p>No route traffic yet.</p>}
          </article>
        </div>
      </Panel>
    </div>
  );
}
