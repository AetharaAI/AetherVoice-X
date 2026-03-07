import { useEffect, useState } from "react";

import { endSession, fetchSessions } from "../api/sessions";
import { Panel } from "../components/common/Panel";
import { useSession } from "../hooks/useSession";
import type { SessionSummary } from "../types/api";

export function Sessions() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selected, setSelected] = useState<string | undefined>(undefined);
  const { detail, loading, error } = useSession(selected);

  useEffect(() => {
    fetchSessions().then(setSessions).catch(() => undefined);
  }, []);

  return (
    <div className="split-grid">
      <Panel title="Session list" eyebrow="Sessions">
        <div className="list-table">
          {sessions.map((session) => (
            <button key={session.id} className="list-row button-row" onClick={() => setSelected(session.id)}>
              <strong>{session.id}</strong>
              <span>{session.session_type}</span>
              <span>{session.status}</span>
            </button>
          ))}
        </div>
      </Panel>

      <Panel title="Session drill-down" eyebrow={selected ?? "Select a session"}>
        {loading ? <p className="muted">Loading session detail...</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
        {detail ? (
          <div className="stack">
            <button onClick={() => endSession(detail.session.id)} className="secondary">
              End session
            </button>
            <pre className="response-box">{JSON.stringify(detail, null, 2)}</pre>
          </div>
        ) : null}
      </Panel>
    </div>
  );
}
