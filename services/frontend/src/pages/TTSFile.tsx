import { useEffect, useMemo, useState } from "react";

import { fetchModels } from "../api/sessions";
import { synthesizeText } from "../api/tts";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { canPlayAudio, formatMs } from "../lib/format";
import type { ModelInfo, TTSResponse } from "../types/api";

function composeStructuredText(tags: string, body: string) {
  return [tags.trim(), body.trim()].filter(Boolean).join("\n");
}

export function TTSFile() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState("chatterbox");
  const [voiceMode, setVoiceMode] = useState("default");
  const [customVoice, setCustomVoice] = useState("");
  const [tagBlock, setTagBlock] = useState("<narration mode=\"support\" />");
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [speed, setSpeed] = useState(1);
  const [emotion, setEmotion] = useState("calm");
  const [speakerHint, setSpeakerHint] = useState("support_agent");
  const [format, setFormat] = useState("wav");
  const [response, setResponse] = useState<TTSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const batchModels = models.filter((entry) => entry.kind === "tts" && entry.supports_batch);
  const resolvedVoice = voiceMode === "custom" ? customVoice.trim() || "default" : "default";
  const structuredText = useMemo(() => composeStructuredText(tagBlock, bodyText), [tagBlock, bodyText]);

  useEffect(() => {
    fetchModels()
      .then((payload) => setModels(payload))
      .catch(() => setModels([]));
  }, []);

  useEffect(() => {
    if (batchModels.length > 0 && !batchModels.some((entry) => entry.name === model)) {
      setModel(batchModels[0].name);
    }
  }, [batchModels, model]);

  async function onSubmit() {
    try {
      setError(null);
      setResponse(null);
      setResponse(
        await synthesizeText({
          model,
          voice: resolvedVoice,
          text: structuredText,
          format,
          sample_rate: 24000,
          stream: false,
          style: { speed, emotion, speaker_hint: speakerHint || undefined },
          metadata: { source: "console", lane: "tts_file" }
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
          <div className="control-grid">
            <div className="field-group">
              <label htmlFor="tts-file-model">Batch model</label>
              <select id="tts-file-model" value={model} onChange={(event) => setModel(event.target.value)}>
                {batchModels.length ? (
                  batchModels.map((entry) => (
                    <option key={entry.name} value={entry.name}>
                      {entry.name}
                    </option>
                  ))
                ) : (
                  <option value="chatterbox">chatterbox</option>
                )}
              </select>
              <p className="field-hint">This lane should target Chatterbox for long-form or batch synthesis.</p>
            </div>
            <div className="field-group">
              <label htmlFor="tts-file-voice-mode">Voice</label>
              <select id="tts-file-voice-mode" value={voiceMode} onChange={(event) => setVoiceMode(event.target.value)}>
                <option value="default">Default voice</option>
                <option value="custom">Custom voice id / file</option>
              </select>
              {voiceMode === "custom" ? (
                <input
                  value={customVoice}
                  onChange={(event) => setCustomVoice(event.target.value)}
                  placeholder="example: Emily.wav"
                />
              ) : null}
            </div>
            <div className="field-group">
              <label htmlFor="tts-file-format">Output format</label>
              <select id="tts-file-format" value={format} onChange={(event) => setFormat(event.target.value)}>
                <option value="wav">wav</option>
                <option value="mp3">mp3</option>
              </select>
            </div>
          </div>
          <div className="control-grid">
            <div className="field-group">
              <label htmlFor="tts-file-tags">Control tags / directives</label>
              <textarea
                id="tts-file-tags"
                className="textarea-mono"
                value={tagBlock}
                onChange={(event) => setTagBlock(event.target.value)}
                rows={4}
                placeholder="<prosody rate=&quot;medium&quot; />"
              />
            </div>
            <div className="field-group">
              <label htmlFor="tts-file-body">Narration body</label>
              <textarea
                id="tts-file-body"
                value={bodyText}
                onChange={(event) => setBodyText(event.target.value)}
                rows={6}
                placeholder="Paste the long-form or structured text you want Chatterbox to synthesize."
              />
            </div>
          </div>
          <div className="control-grid">
            <div className="field-group">
              <label htmlFor="tts-file-speed">Speed</label>
              <div className="range-row">
                <input
                  id="tts-file-speed"
                  type="range"
                  min="0.7"
                  max="1.3"
                  step="0.05"
                  value={speed}
                  onChange={(event) => setSpeed(Number(event.target.value))}
                />
                <output>{speed.toFixed(2)}x</output>
              </div>
            </div>
            <div className="field-group">
              <label htmlFor="tts-file-emotion">Emotion hint</label>
              <select id="tts-file-emotion" value={emotion} onChange={(event) => setEmotion(event.target.value)}>
                <option value="calm">calm</option>
                <option value="neutral">neutral</option>
                <option value="confident">confident</option>
                <option value="urgent">urgent</option>
              </select>
            </div>
            <div className="field-group">
              <label htmlFor="tts-file-speaker-hint">Speaker hint</label>
              <input
                id="tts-file-speaker-hint"
                value={speakerHint}
                onChange={(event) => setSpeakerHint(event.target.value)}
                placeholder="support_agent"
              />
            </div>
          </div>
          <button onClick={onSubmit}>Synthesize</button>
          <p className="muted">Tags are inserted verbatim before the body so you can test your Chatterbox text controls without changing the API contract.</p>
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
