export interface MetricsSummary {
  requestCount: number;
  errorCount: number;
  activeSessions: number;
  avgLatencyMs: number;
  routeCounts: Array<{ route: string; value: number }>;
  errorCounts: Array<{ code: string; value: number }>;
}

function parseLabels(labelChunk: string): Record<string, string> {
  const labels: Record<string, string> = {};
  for (const part of labelChunk.split(",")) {
    const [key, rawValue] = part.split("=");
    if (!key || !rawValue) {
      continue;
    }
    labels[key] = rawValue.replace(/^"/, "").replace(/"$/, "");
  }
  return labels;
}

function parseMetricLine(line: string): { name: string; labels: Record<string, string>; value: number } | null {
  if (!line || line.startsWith("#")) {
    return null;
  }
  const match = line.match(/^([a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{([^}]*)\})?\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)$/);
  if (!match) {
    return null;
  }
  return {
    name: match[1],
    labels: match[2] ? parseLabels(match[2]) : {},
    value: Number(match[3])
  };
}

export function parsePrometheusMetrics(raw: string): MetricsSummary {
  const routeTotals = new Map<string, number>();
  const errorTotals = new Map<string, number>();
  let requestCount = 0;
  let errorCount = 0;
  let activeSessions = 0;
  let durationSum = 0;
  let durationCount = 0;

  for (const line of raw.split("\n")) {
    const parsed = parseMetricLine(line.trim());
    if (!parsed) {
      continue;
    }
    if (parsed.name === "voice_requests_total") {
      requestCount += parsed.value;
      const route = parsed.labels.route ?? "unknown";
      routeTotals.set(route, (routeTotals.get(route) ?? 0) + parsed.value);
      continue;
    }
    if (parsed.name === "voice_request_errors_total") {
      errorCount += parsed.value;
      const code = parsed.labels.error_code ?? "unknown";
      errorTotals.set(code, (errorTotals.get(code) ?? 0) + parsed.value);
      continue;
    }
    if (parsed.name === "voice_active_sessions") {
      activeSessions += parsed.value;
      continue;
    }
    if (parsed.name === "voice_request_duration_ms_sum") {
      durationSum += parsed.value;
      continue;
    }
    if (parsed.name === "voice_request_duration_ms_count") {
      durationCount += parsed.value;
    }
  }

  return {
    requestCount,
    errorCount,
    activeSessions,
    avgLatencyMs: durationCount ? durationSum / durationCount : 0,
    routeCounts: [...routeTotals.entries()]
      .map(([route, value]) => ({ route, value }))
      .sort((left, right) => right.value - left.value),
    errorCounts: [...errorTotals.entries()]
      .map(([code, value]) => ({ code, value }))
      .sort((left, right) => right.value - left.value)
  };
}
