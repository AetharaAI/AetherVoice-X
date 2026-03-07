import { useEffect, useState } from "react";

import { fetchMetricsRaw } from "../api/sessions";
import { Panel } from "../components/common/Panel";
import { MetricBars } from "../components/metrics/MetricBars";

function parseMetrics(metricsRaw: string) {
  const lines = metricsRaw.split("\n");
  const requestCount = Number(lines.find((line) => line.startsWith("voice_requests_total"))?.split(" ").at(-1) ?? 0);
  const errorCount = Number(lines.find((line) => line.startsWith("voice_request_errors_total"))?.split(" ").at(-1) ?? 0);
  const activeSessions = Number(lines.find((line) => line.startsWith("voice_active_sessions"))?.split(" ").at(-1) ?? 0);
  return { requestCount, errorCount, activeSessions };
}

export function Metrics() {
  const [raw, setRaw] = useState("");

  useEffect(() => {
    fetchMetricsRaw().then(setRaw).catch(() => undefined);
  }, []);

  const parsed = parseMetrics(raw);

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
        <pre className="response-box">{raw || "Metrics will appear once the services have handled traffic."}</pre>
      </Panel>
    </div>
  );
}
