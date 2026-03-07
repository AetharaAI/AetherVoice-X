import { useState } from "react";

import { transcribeFile } from "../api/asr";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { formatMs } from "../lib/format";
import type { ASRResponse } from "../types/api";

export function ASRFile() {
  const [file, setFile] = useState<File | null>(null);
  const [response, setResponse] = useState<ASRResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    if (!file) {
      return;
    }
    const formData = new FormData();
    formData.set("file", file);
    formData.set("model", "auto");
    formData.set("task", "transcribe");
    formData.set("language", "auto");
    formData.set("timestamps", "true");
    formData.set("storage_mode", "persist");
    formData.set("metadata", JSON.stringify({ source: "upload" }));
    try {
      setError(null);
      setResponse(null);
      setResponse(await transcribeFile(formData));
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="page-grid">
      <Panel title="Batch transcription" eyebrow="ASR File">
        <div className="stack">
          <input type="file" accept="audio/*" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
          <button onClick={onSubmit}>Transcribe</button>
          {error ? <p className="error-text">{error}</p> : null}
          {response ? (
            <div className="stack">
              <div className="toolbar">
                <Badge value={response.model_used} tone="good" />
                <Badge value={response.language_detected ?? "auto"} />
                <Badge value={formatMs(response.duration_ms)} />
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
                  <span className="label">Task</span>
                  <strong>{response.task}</strong>
                </div>
                <div className="meta-card">
                  <span className="label">Total latency</span>
                  <strong>{formatMs(response.timings.total_ms)}</strong>
                </div>
              </div>

              <div className="detail-section">
                <h3>Transcript</h3>
                <p>{response.text}</p>
              </div>

              <div className="detail-section">
                <h3>Timing breakdown</h3>
                <div className="key-value-grid">
                  <div className="key-value-row"><span>Queue</span><strong>{formatMs(response.timings.queue_ms)}</strong></div>
                  <div className="key-value-row"><span>Preprocess</span><strong>{formatMs(response.timings.preprocess_ms)}</strong></div>
                  <div className="key-value-row"><span>Inference</span><strong>{formatMs(response.timings.inference_ms)}</strong></div>
                  <div className="key-value-row"><span>Postprocess</span><strong>{formatMs(response.timings.postprocess_ms)}</strong></div>
                  <div className="key-value-row"><span>Total</span><strong>{formatMs(response.timings.total_ms)}</strong></div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Artifacts</h3>
                <div className="artifact-list">
                  {Object.entries(response.artifacts ?? {}).map(([key, value]) => (
                    <div key={key} className="artifact-row">
                      <span>{key}</span>
                      <code className="inline-code">{value}</code>
                    </div>
                  ))}
                </div>
              </div>

              <div className="detail-section">
                <h3>Segments</h3>
                <div className="segment-list">
                  {response.segments.map((segment, index) => (
                    <div key={`${segment.segment_id ?? index}`} className="segment-row">
                      <span>{formatMs(segment.start_ms)} - {formatMs(segment.end_ms)}</span>
                      <strong>{segment.text}</strong>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </Panel>
    </div>
  );
}
