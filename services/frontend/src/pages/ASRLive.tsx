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
        <p className="muted">Session: {sessionId ?? "none"}</p>
        <TranscriptPane partials={partials} finalText={finalText} />
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
