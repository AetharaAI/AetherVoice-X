import { useState } from "react";

import { synthesizeText } from "../api/tts";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { canPlayAudio, formatMs } from "../lib/format";
import type { TTSResponse } from "../types/api";

export function TTSFile() {
  const [text, setText] = useState("A technician is being dispatched to your location now.");
  const [response, setResponse] = useState<TTSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    try {
      setError(null);
      setResponse(null);
      setResponse(
        await synthesizeText({
          model: "auto",
          voice: "Emily.wav",
          text,
          format: "wav",
          sample_rate: 24000,
          stream: false,
          style: { speed: 1, emotion: "calm", speaker_hint: "support_agent" },
          metadata: { source: "console" }
        })
      );
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="page-grid">
      <Panel title="Batch synthesis" eyebrow="TTS File">
        <div className="stack">
          <textarea value={text} onChange={(event) => setText(event.target.value)} rows={7} />
          <button onClick={onSubmit}>Synthesize</button>
          {response ? (
            <div className="stack">
              <div className="toolbar">
                <Badge value={response.model_used} tone="good" />
                <Badge value={formatMs(response.duration_ms)} />
                <Badge value={formatMs(response.timings.total_ms)} />
              </div>

              <div className="meta-grid">
                <div className="meta-card">
                  <span className="label">Request ID</span>
                  <strong>{response.request_id}</strong>
                </div>
                <div className="meta-card">
                  <span className="label">Session ID</span>
                  <strong>{response.session_id}</strong>
                </div>
                <div className="meta-card">
                  <span className="label">Artifact URI</span>
                  <strong>{response.audio_url}</strong>
                </div>
                <div className="meta-card">
                  <span className="label">Inference</span>
                  <strong>{formatMs(response.timings.inference_ms)}</strong>
                </div>
              </div>

              <div className="detail-section">
                <h3>Timing breakdown</h3>
                <div className="key-value-grid">
                  <div className="key-value-row"><span>Queue</span><strong>{formatMs(response.timings.queue_ms)}</strong></div>
                  <div className="key-value-row"><span>Inference</span><strong>{formatMs(response.timings.inference_ms)}</strong></div>
                  <div className="key-value-row"><span>Encode</span><strong>{formatMs(response.timings.encode_ms)}</strong></div>
                  <div className="key-value-row"><span>Total</span><strong>{formatMs(response.timings.total_ms)}</strong></div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Artifacts</h3>
                <div className="artifact-list">
                  <div className="artifact-row">
                    <span>audio</span>
                    <code className="inline-code">{response.audio_url}</code>
                  </div>
                  {Object.entries(response.artifacts ?? {}).map(([key, value]) => (
                    <div key={key} className="artifact-row">
                      <span>{key}</span>
                      <code className="inline-code">{value}</code>
                    </div>
                  ))}
                </div>
                {canPlayAudio(response.audio_url) ? <audio controls src={response.audio_url} /> : <p className="muted">Direct playback is only available when the artifact URI is browser-reachable. Current object storage URI is preserved for tracing.</p>}
              </div>
            </div>
          ) : null}
          {error ? <p className="error-text">{error}</p> : null}
        </div>
      </Panel>
    </div>
  );
}
