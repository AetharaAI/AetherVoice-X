import { useState } from "react";

import { triageTranscript } from "../api/asr";
import { Panel } from "../components/common/Panel";
import { UrgencyBadge } from "../components/triage/UrgencyBadge";

export function Triage() {
  const [sessionId, setSessionId] = useState("sess_live_demo");
  const [domain, setDomain] = useState("electrical_emergency");
  const [transcript, setTranscript] = useState("My panel is sparking and the smell is getting worse.");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    try {
      setError(null);
      setResult(
        await triageTranscript({
          session_id: sessionId,
          input_mode: "transcript_plus_audio",
          model: "sentinel",
          domain,
          transcript
        })
      );
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="page-grid">
      <Panel title="Domain urgency classifier" eyebrow="Triage">
        <div className="stack">
          <input value={sessionId} onChange={(event) => setSessionId(event.target.value)} placeholder="Session ID" />
          <select value={domain} onChange={(event) => setDomain(event.target.value)}>
            <option value="electrical_emergency">Electrical emergency</option>
            <option value="hvac_after_hours">HVAC after hours</option>
            <option value="plumbing_emergency">Plumbing emergency</option>
            <option value="locksmith_urgent">Locksmith urgent</option>
            <option value="restoration_dispatch">Restoration dispatch</option>
            <option value="security_alarm_intake">Security alarm intake</option>
          </select>
          <textarea value={transcript} onChange={(event) => setTranscript(event.target.value)} rows={6} />
          <button onClick={onSubmit}>Classify</button>
          {result ? (
            <div className="triage-card">
              <UrgencyBadge classification={String(result.classification ?? "unknown")} />
              <p>{String(result.analysis ?? "")}</p>
              <p>{String(result.recommended_action ?? "")}</p>
            </div>
          ) : null}
          {error ? <p className="error-text">{error}</p> : null}
        </div>
      </Panel>
    </div>
  );
}
