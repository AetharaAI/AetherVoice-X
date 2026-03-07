import { useEffect, useState } from "react";

import { fetchHealth, fetchMetricsRaw } from "../api/sessions";
import { Panel } from "../components/common/Panel";
import { MetricBars } from "../components/metrics/MetricBars";
import { formatCount, formatMs } from "../lib/format";
import { parsePrometheusMetrics } from "../lib/metrics";
import type { HealthResponse } from "../types/api";

export function Metrics() {
  const [raw, setRaw] = useState("");
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    fetchMetricsRaw().then(setRaw).catch(() => undefined);
    fetchHealth().then(setHealth).catch(() => undefined);
  }, []);

  const parsed = parsePrometheusMetrics(raw);

  return (
    <div className="page-grid">
      <Panel title="Prometheus edge view" eyebrow="Metrics">
        <MetricBars
          values={[
            { label: "requests", value: parsed.requestCount },
            { label: "errors", value: parsed.errorCount },
            { label: "active sessions", value: parsed.activeSessions }
          ]}
        />
        <div className="cards-grid">
          <article className="mini-card">
            <h3>Totals</h3>
            <p>Requests: {formatCount(parsed.requestCount)}</p>
            <p>Errors: {formatCount(parsed.errorCount)}</p>
            <p>Average latency: {parsed.avgLatencyMs ? formatMs(Math.round(parsed.avgLatencyMs)) : "n/a"}</p>
          </article>
          <article className="mini-card">
            <h3>Dependency health</h3>
            <p>Gateway: {health?.status ?? "unknown"}</p>
            <p>ASR: {health?.dependencies.asr ?? "unknown"}</p>
            <p>TTS: {health?.dependencies.tts ?? "unknown"}</p>
          </article>
          <article className="mini-card">
            <h3>Top routes</h3>
            {parsed.routeCounts.slice(0, 5).map((route) => <p key={route.route}>{route.route}: {formatCount(route.value)}</p>)}
            {!parsed.routeCounts.length ? <p>No route traffic yet.</p> : null}
          </article>
          <article className="mini-card">
            <h3>Error codes</h3>
            {parsed.errorCounts.length ? parsed.errorCounts.slice(0, 5).map((item) => <p key={item.code}>{item.code}: {formatCount(item.value)}</p>) : <p>No request errors recorded.</p>}
          </article>
        </div>
        <details className="raw-metrics">
          <summary>Raw metrics</summary>
          <pre className="response-box">{raw || "Metrics will appear once the services have handled traffic."}</pre>
        </details>
      </Panel>
    </div>
  );
}
