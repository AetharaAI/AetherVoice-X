import { useEffect, useMemo, useState } from "react";

import { fetchStudioVoices } from "../api/studio";
import { fetchModels } from "../api/sessions";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { WaveformPlaceholder } from "../components/tts/WaveformPlaceholder";
import { useTTSStream } from "../hooks/useTTSStream";
import type { ModelInfo, StudioVoice } from "../types/api";

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
    return `WebSocket open for ${sessionId ?? "pending session"}. Send plain spoken text to trigger synthesis.`;
  }
  if (value === "starting" || value === "opening-socket") {
    return "Bringing the gateway, TTS service, and realtime sidecar into the same session contract.";
  }
  return "Start a stream, choose a voice preset, and send plain spoken text into the live lane.";
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
  const { connected, connectionLabel, sessionId, wsUrl, modelUsed, runtimeTruth, chunkCount, lastSentChars, finalUrl, events, error, connect, send, stop } = useTTSStream();
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [voices, setVoices] = useState<StudioVoice[]>([]);
  const [model, setModel] = useState("moss_realtime");
  const [voiceId, setVoiceId] = useState("moss_default");
  const [sessionProfile, setSessionProfile] = useState("telephony");
  const [tone, setTone] = useState("warm");
  const [cadence, setCadence] = useState("telephony");
  const [speakingStyle, setSpeakingStyle] = useState("service");
  const [latencyMode, setLatencyMode] = useState("low_latency");
  const [sampleRate, setSampleRate] = useState(24000);
  const [prefillTextLen, setPrefillTextLen] = useState(6);
  const [decodeChunkFrames, setDecodeChunkFrames] = useState(3);
  const [decodeOverlapFrames, setDecodeOverlapFrames] = useState(0);
  const [temperature, setTemperature] = useState(0.8);
  const [topP, setTopP] = useState(0.6);
  const [topK, setTopK] = useState(30);
  const [repetitionPenalty, setRepetitionPenalty] = useState(1.1);
  const [repetitionWindow, setRepetitionWindow] = useState(50);
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [rawDirectives, setRawDirectives] = useState("<agent tone=\"warm\" cadence=\"telephony\" />");
  const liveModels = models.filter((entry) => entry.kind === "tts" && entry.supports_streaming);
  const liveVoices = useMemo(
    () =>
      [...voices].sort((left, right) => {
        const rank = (voice: StudioVoice) => {
          if (voice.runtime_target === "moss_realtime") {
            return 0;
          }
          if (voice.source_model === "moss_voice_generator") {
            return 1;
          }
          if (voice.runtime_target === "moss_tts" || voice.runtime_target === "moss_ttsd") {
            return 2;
          }
          if (voice.runtime_target === "chatterbox") {
            return 3;
          }
          return 4;
        };
        return rank(left) - rank(right) || left.display_name.localeCompare(right.display_name);
      }),
    [voices]
  );
  const selectedVoice = liveVoices.find((voice) => voice.voice_id === voiceId) ?? liveVoices[0] ?? null;
  const selectedVoiceAsset = runtimeTruth?.selected_voice_asset ?? selectedVoice?.display_name ?? "MOSS Default Voice";
  const requestedPreset = runtimeTruth?.requested_preset ?? selectedVoice?.voice_id ?? "moss_default";
  const runtimeConditioning = runtimeTruth?.actual_runtime_conditioning_source ?? "pending";
  const fallbackVoicePath = runtimeTruth?.fallback_voice_path ?? "none";
  const runtimePathUsed = runtimeTruth?.runtime_path_used ?? modelUsed ?? model;
  const hasFinalAudio = Boolean(finalUrl);
  const liveTone = connectionTone(connectionLabel, hasFinalAudio);
  const busy =
    connected ||
    connectionLabel === "starting" ||
    connectionLabel === "opening-socket" ||
    connectionLabel === "generating" ||
    connectionLabel === "streaming-audio" ||
    connectionLabel === "finalizing";
  const realtimeProfile = useMemo(
    () => ({
      voice_preset_id: selectedVoice?.voice_id ?? "moss_default",
      session_profile: sessionProfile,
      tone,
      cadence,
      speaking_style: speakingStyle,
      latency_mode: latencyMode,
      raw_directives: rawDirectives
    }),
    [cadence, latencyMode, rawDirectives, selectedVoice?.voice_id, sessionProfile, speakingStyle, tone]
  );
  const realtimeTuning = useMemo(
    () => ({
      prefill_text_len: prefillTextLen,
      decode_chunk_frames: decodeChunkFrames,
      decode_overlap_frames: decodeOverlapFrames,
      temperature,
      top_p: topP,
      top_k: topK,
      repetition_penalty: repetitionPenalty,
      repetition_window: repetitionWindow
    }),
    [decodeChunkFrames, decodeOverlapFrames, prefillTextLen, repetitionPenalty, repetitionWindow, temperature, topK, topP]
  );

  useEffect(() => {
    fetchModels()
      .then((payload) => setModels(payload))
      .catch(() => setModels([]));
    fetchStudioVoices()
      .then((payload) => setVoices(payload))
      .catch(() => setVoices([]));
  }, []);

  useEffect(() => {
    if (liveModels.length > 0 && !liveModels.some((entry) => entry.name === model)) {
      setModel(liveModels[0].name);
    }
  }, [liveModels, model]);

  useEffect(() => {
    if (liveVoices.length > 0 && !liveVoices.some((voice) => voice.voice_id === voiceId)) {
      setVoiceId(liveVoices[0].voice_id);
    }
  }, [liveVoices, voiceId]);

  return (
    <div className="page-grid">
      <Panel title="Realtime synthesis lane" eyebrow="TTS Live">
        <div className="toolbar">
          <button
            onClick={() =>
              connect({
                model,
                voice: selectedVoice?.voice_id ?? "default",
                sampleRate,
                format: "wav",
                contextMode: "conversation",
                metadata: {
                  source: "console",
                  extra: {
                    lane: "tts_live",
                    realtime_profile: realtimeProfile,
                    realtime_tuning: realtimeTuning
                  }
                }
              })
            }
            disabled={connected}
          >
            Start stream
          </button>
          <button onClick={() => send(bodyText.trim())} disabled={!connected || !bodyText.trim()}>
            Send text
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
              <strong>{lastSentChars || bodyText.trim().length} chars</strong>
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
            <p className="field-hint">Keep this lane on the realtime route for live agent turn-taking. Wider studio workflows belong in TTS Studio.</p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-voice">Voice preset</label>
            <select id="tts-live-voice" value={selectedVoice?.voice_id ?? voiceId} onChange={(event) => setVoiceId(event.target.value)} disabled={connected}>
              {liveVoices.length ? (
                liveVoices.map((voice) => (
                  <option key={voice.voice_id} value={voice.voice_id}>
                    {voice.display_name} {voice.runtime_target !== "moss_realtime" ? `(${voice.runtime_target})` : ""}
                  </option>
                ))
              ) : (
                <option value="moss_default">MOSS Default Voice</option>
              )}
            </select>
            <p className="field-hint">
              {runtimeTruth?.conditioning_active
                ? "This session resolved to a real conditioning asset. Realtime inference is materially using the bound conditioning source."
                : "This binds a registry voice record to the session, but realtime inference is still using the current default conditioning path until per-session conditioning lands."}
            </p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-sample-rate">Sample rate</label>
            <select id="tts-live-sample-rate" value={sampleRate} onChange={(event) => setSampleRate(Number(event.target.value))} disabled={connected}>
              <option value={24000}>24000 Hz</option>
            </select>
            <p className="field-hint">Realtime stays pinned to the model-native sample rate for now.</p>
          </div>
        </div>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-profile">Session profile</label>
            <select id="tts-live-profile" value={sessionProfile} onChange={(event) => setSessionProfile(event.target.value)} disabled={connected}>
              <option value="telephony">Telephony</option>
              <option value="assistant">Assistant</option>
              <option value="narration">Narration</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-tone">Tone</label>
            <select id="tts-live-tone" value={tone} onChange={(event) => setTone(event.target.value)} disabled={connected}>
              <option value="warm">warm</option>
              <option value="calm">calm</option>
              <option value="neutral">neutral</option>
              <option value="confident">confident</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-cadence">Cadence</label>
            <select id="tts-live-cadence" value={cadence} onChange={(event) => setCadence(event.target.value)} disabled={connected}>
              <option value="telephony">telephony</option>
              <option value="conversational">conversational</option>
              <option value="measured">measured</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-style">Speaking style</label>
            <select id="tts-live-style" value={speakingStyle} onChange={(event) => setSpeakingStyle(event.target.value)} disabled={connected}>
              <option value="service">service</option>
              <option value="dispatcher">dispatcher</option>
              <option value="support">support</option>
              <option value="narrator">narrator</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-latency">Latency profile</label>
            <select id="tts-live-latency" value={latencyMode} onChange={(event) => setLatencyMode(event.target.value)} disabled={connected}>
              <option value="low_latency">low latency</option>
              <option value="balanced">balanced</option>
              <option value="quality">quality</option>
            </select>
          </div>
        </div>
        <details className="accordion">
          <summary>Realtime tuning</summary>
          <div className="accordion-body">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="tts-live-prefill">Prefill text len</label>
                <input
                  id="tts-live-prefill"
                  type="number"
                  min={1}
                  max={64}
                  value={prefillTextLen}
                  onChange={(event) => setPrefillTextLen(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-chunk-frames">Decode chunk frames</label>
                <input
                  id="tts-live-chunk-frames"
                  type="number"
                  min={1}
                  max={64}
                  value={decodeChunkFrames}
                  onChange={(event) => setDecodeChunkFrames(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-overlap-frames">Decode overlap frames</label>
                <input
                  id="tts-live-overlap-frames"
                  type="number"
                  min={0}
                  max={16}
                  value={decodeOverlapFrames}
                  onChange={(event) => setDecodeOverlapFrames(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-temperature">Temperature</label>
                <input
                  id="tts-live-temperature"
                  type="number"
                  min={0.1}
                  max={2}
                  step={0.05}
                  value={temperature}
                  onChange={(event) => setTemperature(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-top-p">Top p</label>
                <input
                  id="tts-live-top-p"
                  type="number"
                  min={0.05}
                  max={1}
                  step={0.05}
                  value={topP}
                  onChange={(event) => setTopP(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-top-k">Top k</label>
                <input
                  id="tts-live-top-k"
                  type="number"
                  min={1}
                  max={200}
                  step={1}
                  value={topK}
                  onChange={(event) => setTopK(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-repetition-penalty">Repetition penalty</label>
                <input
                  id="tts-live-repetition-penalty"
                  type="number"
                  min={0.8}
                  max={2}
                  step={0.05}
                  value={repetitionPenalty}
                  onChange={(event) => setRepetitionPenalty(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-repetition-window">Repetition window</label>
                <input
                  id="tts-live-repetition-window"
                  type="number"
                  min={1}
                  max={512}
                  step={1}
                  value={repetitionWindow}
                  onChange={(event) => setRepetitionWindow(Number(event.target.value))}
                  disabled={connected}
                />
              </div>
            </div>
            <p className="field-hint">
              These controls apply at stream start for the current session only. Use them for immediate live quality tests without changing backend env defaults.
            </p>
          </div>
        </details>
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
            <span className="label">Selected voice asset</span>
            <strong>{selectedVoiceAsset}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Requested preset</span>
            <strong>{requestedPreset}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Runtime conditioning</span>
            <strong className="meta-value-wrap">{runtimeConditioning}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Fallback voice path</span>
            <strong className="meta-value-wrap">{fallbackVoicePath}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Runtime path used</span>
            <strong>{runtimePathUsed}</strong>
          </div>
          <div className="meta-card">
            <span className="label">WebSocket contract</span>
            <strong className="meta-value-wrap">{wsUrl ?? "pending"}</strong>
          </div>
        </div>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-body">Spoken body</label>
            <textarea
              id="tts-live-body"
              value={bodyText}
              onChange={(event) => setBodyText(event.target.value)}
              rows={5}
              placeholder="Write the response your agent should say."
            />
            <p className="field-hint">Only the spoken body is sent into the realtime utterance. Session profile and style controls ride in backend state.</p>
          </div>
          <details className="accordion">
            <summary>Experimental raw directives</summary>
            <div className="accordion-body">
              <label htmlFor="tts-live-raw-directives">Unsupported passthrough notes</label>
              <textarea
                id="tts-live-raw-directives"
                className="textarea-mono"
                value={rawDirectives}
                onChange={(event) => setRawDirectives(event.target.value)}
                rows={4}
                placeholder="<agent tone=&quot;warm&quot; cadence=&quot;telephony&quot; />"
              />
              <p className="field-hint">These directives are preserved in metadata for operator debugging only. They are no longer prepended into spoken text.</p>
            </div>
          </details>
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
            {events.map((event, index) => (
              <div key={`${index}-${event}`} className="artifact-row">
                <span>{event}</span>
              </div>
            ))}
          </div>
        </section>
        <p className="muted">Primary use case: keep the stream open, bind a voice preset to the session, and push plain assistant text from your reasoning layer with minimal operator ceremony.</p>
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
