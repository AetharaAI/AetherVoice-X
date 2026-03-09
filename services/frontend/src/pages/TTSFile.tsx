import { useEffect, useMemo, useState } from "react";

import { fetchModels } from "../api/sessions";
import { synthesizeText } from "../api/tts";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { canPlayAudio, formatMs } from "../lib/format";
import type { ModelInfo, TTSResponse } from "../types/api";

export function TTSFile() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState("chatterbox");
  const [voiceMode, setVoiceMode] = useState("default");
  const [customVoice, setCustomVoice] = useState("");
  const [operatorNotes, setOperatorNotes] = useState("Support dispatch narration with clear sentence boundaries.");
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [speed, setSpeed] = useState(1);
  const [emotion, setEmotion] = useState("calm");
  const [speakerHint, setSpeakerHint] = useState("support_agent");
  const [splitText, setSplitText] = useState(true);
  const [chunkSize, setChunkSize] = useState(180);
  const [temperature, setTemperature] = useState(0.8);
  const [exaggeration, setExaggeration] = useState(1.15);
  const [cfgWeight, setCfgWeight] = useState(0.5);
  const [seed, setSeed] = useState("2025");
  const [format, setFormat] = useState("wav");
  const [response, setResponse] = useState<TTSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const batchModels = models.filter((entry) => entry.kind === "tts" && entry.supports_batch);
  const resolvedVoice = voiceMode === "custom" ? customVoice.trim() || "default" : "default";
  const selectedModel = useMemo(() => batchModels.find((entry) => entry.name === model) ?? null, [batchModels, model]);
  const isChatterbox = model === "chatterbox";
  const modelHelperText = isChatterbox
    ? "Chatterbox batch mode supports richer shaping controls. These knobs ride in request metadata instead of being prepended into spoken text."
    : "OpenMOSS batch routes preserve operator notes in metadata. Only the narration body is spoken.";

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
          text: bodyText.trim(),
          format,
          sample_rate: 24000,
          stream: false,
          style: { speed, emotion, speaker_hint: speakerHint || undefined },
          metadata: {
            source: "console",
            lane: "tts_file",
            extra: {
              operator_notes: operatorNotes.trim() || undefined,
              voice_mode: voiceMode,
              split_text: splitText,
              chunk_size: chunkSize,
              temperature,
              exaggeration,
              cfg_weight: cfgWeight,
              seed: seed.trim() ? Number(seed) : undefined,
            }
          }
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
              <label htmlFor="tts-file-notes">Operator notes</label>
              <textarea
                id="tts-file-notes"
                className="textarea-mono"
                value={operatorNotes}
                onChange={(event) => setOperatorNotes(event.target.value)}
                rows={4}
                placeholder="Document the intended delivery, use-case, or model-specific shaping notes."
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
          <div className="detail-section">
            <h3>{selectedModel?.name ?? model} controls</h3>
            <p className="muted">{modelHelperText}</p>
            {isChatterbox ? (
              <div className="control-grid">
                <div className="field-group">
                  <label htmlFor="tts-file-split">Split long text</label>
                  <label className="switch">
                    <input id="tts-file-split" type="checkbox" checked={splitText} onChange={(event) => setSplitText(event.target.checked)} />
                    Split long passages before synthesis
                  </label>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-file-chunk-size">Chunk size</label>
                  <div className="range-row">
                    <input id="tts-file-chunk-size" type="range" min="120" max="500" step="10" value={chunkSize} onChange={(event) => setChunkSize(Number(event.target.value))} />
                    <output>{chunkSize}</output>
                  </div>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-file-temperature">Temperature</label>
                  <div className="range-row">
                    <input id="tts-file-temperature" type="range" min="0.2" max="1.4" step="0.05" value={temperature} onChange={(event) => setTemperature(Number(event.target.value))} />
                    <output>{temperature.toFixed(2)}</output>
                  </div>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-file-exaggeration">Exaggeration</label>
                  <div className="range-row">
                    <input id="tts-file-exaggeration" type="range" min="0.8" max="1.8" step="0.05" value={exaggeration} onChange={(event) => setExaggeration(Number(event.target.value))} />
                    <output>{exaggeration.toFixed(2)}</output>
                  </div>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-file-cfg">CFG weight</label>
                  <div className="range-row">
                    <input id="tts-file-cfg" type="range" min="0.2" max="1.2" step="0.05" value={cfgWeight} onChange={(event) => setCfgWeight(Number(event.target.value))} />
                    <output>{cfgWeight.toFixed(2)}</output>
                  </div>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-file-seed">Generation seed</label>
                  <input id="tts-file-seed" value={seed} onChange={(event) => setSeed(event.target.value)} placeholder="2025" />
                </div>
              </div>
            ) : (
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
            )}
          </div>
          <button onClick={onSubmit}>Synthesize</button>
          <p className="muted">Only the narration body is spoken. Operator notes and model-specific shaping controls stay in metadata so batch synthesis is easier to reason about.</p>
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
                  <span className="label">Playback URL</span>
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
                <h3>Playback and artifacts</h3>
                <div className="stream-output-actions">
                  {canPlayAudio(response.audio_url) ? <audio controls src={response.audio_url} /> : <div className="playback-placeholder"><span className="label">Playback deck</span><strong>Waiting for browser-reachable audio</strong></div>}
                  <a className="button-link" href={response.audio_url} download={`${response.session_id}.${format}`}>Download</a>
                </div>
                <div className="artifact-list">
                  <div className="artifact-row">
                    <span>playback</span>
                    <code className="inline-code">{response.audio_url}</code>
                  </div>
                  {Object.entries(response.artifacts ?? {}).map(([key, value]) => (
                    <div key={key} className="artifact-row">
                      <span>{key}</span>
                      <code className="inline-code">{value}</code>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : null}
          {error ? <p className="error-text">{error}</p> : null}
        </div>
      </Panel>
    </div>
  );
}
