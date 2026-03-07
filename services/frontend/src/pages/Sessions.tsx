import { useEffect, useState } from "react";

import { endSession, fetchSessions } from "../api/sessions";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { useSession } from "../hooks/useSession";
import { formatDateTime, formatMs, formatValue } from "../lib/format";
import type { SessionSummary } from "../types/api";

export function Sessions() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selected, setSelected] = useState<string | undefined>(undefined);
  const [ending, setEnding] = useState(false);
  const { detail, loading, error } = useSession(selected);

  useEffect(() => {
    fetchSessions().then(setSessions).catch(() => undefined);
  }, []);

  async function onEndSession() {
    if (!detail) {
      return;
    }
    setEnding(true);
    try {
      await endSession(detail.session.id);
      setSessions(await fetchSessions());
    } finally {
      setEnding(false);
    }
  }

  return (
    <div className="split-grid">
      <Panel title="Session list" eyebrow="Sessions">
        <div className="list-table">
          {sessions.map((session) => (
            <button key={session.id} className="list-row button-row" onClick={() => setSelected(session.id)}>
              <strong>{session.id}</strong>
              <span>{session.session_type}</span>
              <span>{session.model_used ?? session.model_requested ?? "auto"}</span>
              <span>{session.status} · {formatDateTime(session.started_at)}</span>
            </button>
          ))}
        </div>
      </Panel>

      <Panel title="Session drill-down" eyebrow={selected ?? "Select a session"}>
        {loading ? <p className="muted">Loading session detail...</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
        {detail ? (
          <div className="stack">
            <div className="toolbar">
              <button onClick={onEndSession} className="secondary" disabled={ending || detail.session.status === "ended"}>
                {detail.session.status === "ended" ? "Session ended" : ending ? "Ending..." : "End session"}
              </button>
              <Badge value={detail.session.status} tone={detail.session.status === "active" ? "good" : "default"} />
            </div>

            <div className="meta-grid">
              <div className="meta-card">
                <span className="label">Session ID</span>
                <strong>{detail.session.id}</strong>
              </div>
              <div className="meta-card">
                <span className="label">Lane</span>
                <strong>{detail.session.session_type}</strong>
              </div>
              <div className="meta-card">
                <span className="label">Model</span>
                <strong>{detail.session.model_used ?? detail.session.model_requested ?? "auto"}</strong>
              </div>
              <div className="meta-card">
                <span className="label">Started</span>
                <strong>{formatDateTime(detail.session.started_at)}</strong>
              </div>
            </div>

            <div className="detail-section">
              <h3>Session metadata</h3>
              <div className="key-value-grid">
                {Object.entries(detail.session.metadata ?? {}).map(([key, value]) => (
                  <div key={key} className="key-value-row">
                    <span>{key}</span>
                    <strong>{formatValue(value)}</strong>
                  </div>
                ))}
              </div>
            </div>

            <div className="detail-section">
              <h3>Requests</h3>
              <div className="stack">
                {detail.requests.length ? detail.requests.map((request) => (
                  <article key={request.id} className="detail-card">
                    <div className="detail-card-header">
                      <strong>{request.id}</strong>
                      <Badge value={request.status} tone={request.status === "ok" ? "good" : "danger"} />
                    </div>
                    <div className="key-value-grid">
                      <div className="key-value-row"><span>Type</span><strong>{request.request_type}</strong></div>
                      <div className="key-value-row"><span>Route</span><strong>{request.route}</strong></div>
                      <div className="key-value-row"><span>Model</span><strong>{request.model_used ?? request.model_requested ?? "auto"}</strong></div>
                      <div className="key-value-row"><span>Total</span><strong>{formatMs(request.total_ms)}</strong></div>
                      <div className="key-value-row"><span>Inference</span><strong>{formatMs(request.inference_ms)}</strong></div>
                      <div className="key-value-row"><span>Created</span><strong>{formatDateTime(request.created_at)}</strong></div>
                    </div>
                    {request.error_message ? <p className="error-text">{request.error_message}</p> : null}
                  </article>
                )) : <p className="muted">No request records stored for this session.</p>}
              </div>
            </div>

            <div className="detail-section">
              <h3>Transcript outputs</h3>
              <div className="stack">
                {detail.transcripts.length ? detail.transcripts.map((transcript) => (
                  <article key={transcript.id} className="detail-card">
                    <div className="detail-card-header">
                      <strong>{transcript.id}</strong>
                      <span className="muted">{transcript.language_detected ?? "language auto"}</span>
                    </div>
                    <p>{transcript.text}</p>
                    <div className="segment-list">
                      {transcript.segments.map((segment, index) => (
                        <div key={`${transcript.id}-${segment.segment_id ?? index}`} className="segment-row">
                          <span>{formatMs(segment.start_ms)} - {formatMs(segment.end_ms)}</span>
                          <strong>{segment.text}</strong>
                        </div>
                      ))}
                    </div>
                  </article>
                )) : <p className="muted">No transcript payloads stored for this session.</p>}
              </div>
            </div>

            <div className="detail-section">
              <h3>TTS outputs</h3>
              <div className="stack">
                {detail.tts_outputs.length ? detail.tts_outputs.map((output) => (
                  <article key={output.id} className="detail-card">
                    <div className="detail-card-header">
                      <strong>{output.model_used}</strong>
                      <span className="muted">{formatMs(output.duration_ms)}</span>
                    </div>
                    <p>{output.text_input}</p>
                    <p className="muted">Voice: {output.voice ?? "default"}</p>
                    <code className="inline-code">{output.output_uri ?? "n/a"}</code>
                  </article>
                )) : <p className="muted">No TTS outputs stored for this session.</p>}
              </div>
            </div>

            <div className="detail-section">
              <h3>Triage results</h3>
              <div className="stack">
                {detail.triage_results.length ? detail.triage_results.map((triage) => (
                  <article key={triage.id} className="detail-card">
                    <div className="detail-card-header">
                      <strong>{triage.domain}</strong>
                      <Badge value={triage.classification} tone={triage.classification === "emergency" ? "danger" : triage.classification === "urgent" ? "warn" : "good"} />
                    </div>
                    <p>{triage.analysis}</p>
                    <p className="muted">{triage.recommended_action}</p>
                  </article>
                )) : <p className="muted">No triage decisions stored for this session.</p>}
              </div>
            </div>
          </div>
        ) : null}
      </Panel>
    </div>
  );
}
