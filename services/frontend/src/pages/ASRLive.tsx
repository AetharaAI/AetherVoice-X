import { useState } from "react";

import { TranscriptPane } from "../components/asr/TranscriptPane";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { formatMs } from "../lib/format";
import { useASRStream } from "../hooks/useASRStream";

export function ASRLive() {
  const { connected, sessionId, modelUsed, fallbackUsed, partials, finalText, finalSegments, latencyLabel, firstPartialMs, finalMs, framesSent, error, start, stop } = useASRStream();
  const [triageEnabled, setTriageEnabled] = useState(false);
  const [model, setModel] = useState("auto");

  return (
    <div className="page-grid">
      <Panel title="Live microphone stream" eyebrow="ASR Live">
        <div className="toolbar">
          <select value={model} onChange={(event) => setModel(event.target.value)} disabled={connected}>
            <option value="auto">Auto route</option>
            <option value="voxtral_realtime">Voxtral realtime</option>
            <option value="faster_whisper">Faster Whisper fallback</option>
          </select>
          <button onClick={() => start(model, triageEnabled)} disabled={connected}>
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
            <strong>{latencyLabel}</strong>
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
            <span className="label">Frames sent</span>
            <strong>{framesSent}</strong>
          </div>
          <div className="meta-card">
            <span className="label">First partial</span>
            <strong>{formatMs(firstPartialMs)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Final latency</span>
            <strong>{formatMs(finalMs)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Route used</span>
            <strong>{modelUsed ?? "pending"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Final chars</span>
            <strong>{finalText.length}</strong>
          </div>
        </div>
        <TranscriptPane partials={partials} finalText={finalText} finalSegments={finalSegments} />
        <p className="muted">Model route: <strong>{model}</strong>. Auto will use the configured realtime lane when available and fall back if it is not ready.</p>
        {fallbackUsed ? <p className="muted">Fallback was used for this stream start. The selected realtime lane was not available.</p> : null}
        {triageEnabled ? <p className="muted">Triage flag is being sent with the stream start request. Persisted classification will appear on the Sessions page once the backend lane records it.</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
