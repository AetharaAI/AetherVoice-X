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

function formatConnectionLabel(value: string) {
  return value.replace(/-/g, " ");
}

function connectionTone(value: string, hasFinalAudio: boolean) {
  if (value.includes("error")) {
    return "danger" as const;
  }
  if (hasFinalAudio || value === "final") {
    return "good" as const;
  }
  if (value === "generating" || value === "streaming-audio" || value === "finalizing") {
    return "warn" as const;
  }
  return "default" as const;
}

function statusHeadline(value: string, hasFinalAudio: boolean) {
  if (hasFinalAudio) {
    return "Audio ready for review";
  }
  if (value === "generation-error") {
    return "Generation failed before audio returned";
  }
  if (value === "generating") {
    return "MOSS Realtime is generating";
  }
  if (value === "streaming-audio") {
    return "Audio frames are returning";
  }
  if (value === "finalizing") {
    return "Closing the stream and assembling final audio";
  }
  if (value === "open") {
    return "Stream is armed and ready for text";
  }
  if (value === "starting" || value === "opening-socket") {
    return "Negotiating the live session";
  }
  return "Realtime synthesis lane idle";
}

function statusMessage(value: string, hasFinalAudio: boolean, sessionId: string | null, lastSentChars: number) {
  if (hasFinalAudio) {
    return "MOSS Realtime active. Final audio has landed and is ready for playback or download.";
  }
  if (value === "generation-error") {
    return "MOSS Realtime accepted the stream, then the backend generation path failed before a final waveform came back.";
  }
  if (value === "generating") {
    return `MOSS Realtime active and generating from the latest ${lastSentChars || 0}-character payload.`;
  }
  if (value === "streaming-audio") {
    return "MOSS Realtime is emitting audio chunks. Stay on the lane until the final frame arrives.";
  }
  if (value === "finalizing") {
    return "Finalizing the session and waiting for the completed audio asset.";
  }
  if (value === "open") {
    return `WebSocket open for ${sessionId ?? "pending session"}. Send structured text to trigger synthesis.`;
  }
  if (value === "starting" || value === "opening-socket") {
    return "Bringing the gateway, TTS service, and realtime sidecar into the same session contract.";
  }
  return "Start a stream, send structured text, and keep the lane open long enough to receive the final audio response.";
}

function TypewriterStatus({ text, active }: { text: string; active: boolean }) {
  const [visibleChars, setVisibleChars] = useState(active ? 0 : text.length);

  useEffect(() => {
    if (!active) {
      setVisibleChars(text.length);
      return;
    }
    setVisibleChars(0);
    const timer = window.setInterval(() => {
      setVisibleChars((current) => {
        if (current >= text.length) {
          window.clearInterval(timer);
          return text.length;
        }
        return current + 1;
      });
    }, 18);
    return () => window.clearInterval(timer);
  }, [active, text]);

  return (
    <p className="stream-typewriter">
      {text.slice(0, visibleChars)}
      <span className={`stream-caret ${active ? "active" : ""}`} aria-hidden="true" />
    </p>
  );
}

export function TTSLive() {
  const { connected, connectionLabel, sessionId, wsUrl, modelUsed, chunkCount, lastSentChars, finalUrl, events, error, connect, send, stop } = useTTSStream();
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
  const hasFinalAudio = Boolean(finalUrl);
  const liveTone = connectionTone(connectionLabel, hasFinalAudio);
  const busy = connected || connectionLabel === "starting" || connectionLabel === "opening-socket" || connectionLabel === "generating" || connectionLabel === "streaming-audio" || connectionLabel === "finalizing";

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
          <Badge value={formatConnectionLabel(connectionLabel)} tone={liveTone} />
        </div>
        <section className={`stream-hero ${liveTone}`}>
          <div className="stream-hero-copy">
            <p className="eyebrow">Live generation status</p>
            <h3>{statusHeadline(connectionLabel, hasFinalAudio)}</h3>
            <TypewriterStatus text={statusMessage(connectionLabel, hasFinalAudio, sessionId, lastSentChars)} active={busy && !hasFinalAudio && !error} />
          </div>
          <div className="stream-hero-metrics">
            <div className="status-chip">
              <span className="label">Payload</span>
              <strong>{lastSentChars || structuredText.trim().length} chars</strong>
            </div>
            <div className="status-chip">
              <span className="label">Chunks</span>
              <strong>{chunkCount}</strong>
            </div>
            <div className="status-chip">
              <span className="label">Audio</span>
              <strong>{hasFinalAudio ? "ready" : "pending"}</strong>
            </div>
          </div>
        </section>
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
            <strong className="meta-value-wrap">{wsUrl ?? "pending"}</strong>
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
        <section className="stream-output-shell">
          <div className="stream-output-header">
            <div>
              <p className="eyebrow">Output surface</p>
              <h3>Operator playback and transport artifacts</h3>
              <p className="field-hint">
                The finalized WAV appears here after you click <strong>End stream</strong>. Live audio chunks can still play before that, but the
                downloadable file is assembled at stream close.
              </p>
            </div>
            <div className="stream-output-actions">
              {finalUrl ? (
                <audio controls src={finalUrl} />
              ) : (
                <div className="playback-placeholder">
                  <span className="label">Playback deck</span>
                  <strong>Waiting for final audio</strong>
                </div>
              )}
              <a
                className={`button-link ${finalUrl ? "" : "disabled"}`}
                href={finalUrl ?? "#"}
                download={`${sessionId ?? "tts-live"}.wav`}
                aria-disabled={!finalUrl}
                onClick={(event) => {
                  if (!finalUrl) {
                    event.preventDefault();
                  }
                }}
              >
                Download WAV
              </a>
            </div>
          </div>
          <WaveformPlaceholder
            chunks={Math.max(chunkCount, lastSentChars > 0 ? 1 : 0)}
            active={busy && !hasFinalAudio}
            tone={error ? "danger" : hasFinalAudio ? "good" : "default"}
          />
          <div className="artifact-list">
            {events.map((event) => (
              <div key={event} className="artifact-row">
                <span>{event}</span>
              </div>
            ))}
          </div>
        </section>
        <p className="muted">Primary use case: push structured response text from your reasoning layer into this open stream and let the telephony agent speak it back with minimal ceremony.</p>
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
