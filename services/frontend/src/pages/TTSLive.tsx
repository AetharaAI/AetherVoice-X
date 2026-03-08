import { useEffect, useMemo, useState } from "react";

import { fetchModels } from "../api/sessions";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { WaveformPlaceholder } from "../components/tts/WaveformPlaceholder";
import { useTTSStream } from "../hooks/useTTSStream";
import type { ModelInfo } from "../types/api";

function composeStructuredText(tags: string, body: string) {
  return [tags.trim(), body.trim()].filter(Boolean).join("\n");
}

export function TTSLive() {
  const { connected, connectionLabel, sessionId, wsUrl, modelUsed, chunkCount, finalUrl, events, error, connect, send, stop } = useTTSStream();
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState("moss_realtime");
  const [voiceMode, setVoiceMode] = useState("default");
  const [customVoice, setCustomVoice] = useState("");
  const [tagBlock, setTagBlock] = useState("<agent tone=\"warm\" cadence=\"telephony\" />");
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [sampleRate, setSampleRate] = useState(24000);
  const structuredText = useMemo(() => composeStructuredText(tagBlock, bodyText), [tagBlock, bodyText]);
  const resolvedVoice = voiceMode === "custom" ? customVoice.trim() || "default" : "default";
  const liveModels = models.filter((entry) => entry.kind === "tts" && entry.supports_streaming);

  useEffect(() => {
    fetchModels()
      .then((payload) => setModels(payload))
      .catch(() => setModels([]));
  }, []);

  useEffect(() => {
    if (liveModels.length > 0 && !liveModels.some((entry) => entry.name === model)) {
      setModel(liveModels[0].name);
    }
  }, [liveModels, model]);

  return (
    <div className="page-grid">
      <Panel title="Realtime synthesis lane" eyebrow="TTS Live">
        <div className="toolbar">
          <button
            onClick={() =>
              connect({
                model,
                voice: resolvedVoice,
                sampleRate,
                format: "wav",
                contextMode: "conversation",
                metadata: { source: "console", lane: "tts_live" },
              })
            }
            disabled={connected}
          >
            Start stream
          </button>
          <button onClick={() => send(structuredText)} disabled={!connected || !structuredText.trim()}>
            Send structured text
          </button>
          <button onClick={stop} disabled={!connected} className="secondary">
            End stream
          </button>
          <Badge value={connectionLabel} tone={connectionLabel === "final" ? "good" : connectionLabel.includes("error") ? "danger" : "default"} />
        </div>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-model">Realtime model</label>
            <select id="tts-live-model" value={model} onChange={(event) => setModel(event.target.value)} disabled={connected}>
              {liveModels.length ? (
                liveModels.map((entry) => (
                  <option key={entry.name} value={entry.name}>
                    {entry.name}
                  </option>
                ))
              ) : (
                <option value="moss_realtime">moss_realtime</option>
              )}
            </select>
            <p className="field-hint">This lane should stay pointed at the realtime model for live agent turn-taking.</p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-voice-mode">Voice</label>
            <select id="tts-live-voice-mode" value={voiceMode} onChange={(event) => setVoiceMode(event.target.value)} disabled={connected}>
              <option value="default">Default voice</option>
              <option value="custom">Custom voice id</option>
            </select>
            {voiceMode === "custom" ? (
              <input
                value={customVoice}
                onChange={(event) => setCustomVoice(event.target.value)}
                placeholder="voice id or prompt-conditioned alias"
                disabled={connected}
              />
            ) : null}
            <p className="field-hint">OpenMOSS realtime is effectively single-voice today unless you add custom conditioning on the server side.</p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-sample-rate">Sample rate</label>
            <select id="tts-live-sample-rate" value={sampleRate} onChange={(event) => setSampleRate(Number(event.target.value))} disabled={connected}>
              <option value={24000}>24000 Hz</option>
            </select>
            <p className="field-hint">Realtime lane is pinned to the model-native sample rate right now.</p>
          </div>
        </div>
        <div className="meta-grid">
          <div className="meta-card">
            <span className="label">Connection</span>
            <strong>{connectionLabel}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Session</span>
            <strong>{sessionId ?? "none"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Route target</span>
            <strong>{modelUsed ?? model}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Chunks</span>
            <strong>{chunkCount}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Final audio</span>
            <strong>{finalUrl ? "ready" : "pending"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">WebSocket contract</span>
            <strong>{wsUrl ?? "pending"}</strong>
          </div>
        </div>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-tags">Structured tags / directives</label>
            <textarea
              id="tts-live-tags"
              className="textarea-mono"
              value={tagBlock}
              onChange={(event) => setTagBlock(event.target.value)}
              rows={4}
              placeholder="<agent tone=&quot;warm&quot; />"
            />
            <p className="field-hint">These lines are inserted verbatim ahead of the spoken body so you can test telephony-style prompt tags.</p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-body">Spoken body</label>
            <textarea
              id="tts-live-body"
              value={bodyText}
              onChange={(event) => setBodyText(event.target.value)}
              rows={4}
              placeholder="Write the response your agent should say."
            />
            <p className="field-hint">Send text keeps the stream open. End stream asks the backend for final audio and waits for the last response frame.</p>
          </div>
        </div>
        <WaveformPlaceholder chunks={chunkCount} />
        <div className="artifact-list">
          {events.map((event) => (
            <div key={event} className="artifact-row">
              <span>{event}</span>
            </div>
          ))}
        </div>
        {finalUrl ? <audio controls src={finalUrl} /> : null}
        <p className="muted">Primary use case: push structured response text from your reasoning layer into this open stream and let the telephony agent speak it back with minimal ceremony.</p>
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
