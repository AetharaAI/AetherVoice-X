import { useState } from "react";

import { TranscriptPane } from "../components/asr/TranscriptPane";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { useASRStream } from "../hooks/useASRStream";

export function ASRLive() {
  const { connected, sessionId, partials, finalText, latencyLabel, error, start, stop } = useASRStream();
  const [triageEnabled, setTriageEnabled] = useState(false);

  return (
    <div className="page-grid">
      <Panel title="Live microphone stream" eyebrow="ASR Live">
        <div className="toolbar">
          <button onClick={() => start("auto", triageEnabled)} disabled={connected}>
            Connect
          </button>
          <button onClick={stop} disabled={!connected} className="secondary">
            Disconnect
          </button>
          <label className="switch">
            <input type="checkbox" checked={triageEnabled} onChange={(event) => setTriageEnabled(event.target.checked)} />
            Triage enabled
          </label>
          <Badge value={latencyLabel} tone={latencyLabel === "final" ? "good" : "default"} />
        </div>
        <div className="meta-grid">
          <div className="meta-card">
            <span className="label">Connection</span>
            <strong>{connected ? "streaming" : "idle"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Session</span>
            <strong>{sessionId ?? "none"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Partial count</span>
            <strong>{partials.length}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Final chars</span>
            <strong>{finalText.length}</strong>
          </div>
        </div>
        <TranscriptPane partials={partials} finalText={finalText} />
        {triageEnabled ? <p className="muted">Triage flag is being sent with the stream start request. Persisted classification will appear on the Sessions page once the backend lane records it.</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
