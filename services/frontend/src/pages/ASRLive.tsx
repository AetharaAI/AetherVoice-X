import { useEffect, useRef, useState } from "react";

import { fetchStudioOverview } from "../api/studio";
import { generateVoiceTurn } from "../api/voice";
import { TranscriptPane } from "../components/asr/TranscriptPane";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { formatMs } from "../lib/format";
import { useASRStream } from "../hooks/useASRStream";
import type { StudioOverview, StudioRouteDescriptor, VoiceTurnResponse } from "../types/api";

function preferredTurnRoute(routes: StudioRouteDescriptor[]) {
  return (
    routes.find((route) => route.name === "moss_tts" && route.invokable)?.name ??
    routes.find((route) => route.name === "chatterbox" && route.invokable)?.name ??
    routes.find((route) => route.mode === "batch" && route.invokable)?.name ??
    routes.find((route) => route.name === "moss_tts")?.name ??
    routes.find((route) => route.name === "chatterbox")?.name ??
    "moss_tts"
  );
}

export function ASRLive() {
  const {
    connected,
    sessionId,
    modelUsed,
    fallbackUsed,
    partialText,
    partialEventCount,
    finalText,
    finalSegments,
    latencyLabel,
    firstPartialMs,
    finalMs,
    framesSent,
    error,
    start,
    stop,
  } = useASRStream();
  const [triageEnabled, setTriageEnabled] = useState(false);
  const [model, setModel] = useState("auto");
  const [studioOverview, setStudioOverview] = useState<StudioOverview | null>(null);
  const [turnAutoReply, setTurnAutoReply] = useState(false);
  const [turnVoiceId, setTurnVoiceId] = useState("moss_default");
  const [turnTtsModel, setTurnTtsModel] = useState<StudioRouteDescriptor["name"]>("moss_tts");
  const [turnBusy, setTurnBusy] = useState(false);
  const [turnError, setTurnError] = useState<string | null>(null);
  const [turnResult, setTurnResult] = useState<VoiceTurnResponse | null>(null);
  const lastAutoReplySessionRef = useRef<string | null>(null);
  const transcriptChars = (finalText || partialText).length;
  const turnRoutes = (studioOverview?.routes ?? []).filter((route) => route.mode === "batch" || route.name === "chatterbox");
  const turnVoices = studioOverview?.voices ?? [];
  const routing = studioOverview?.routing ?? null;

  useEffect(() => {
    void fetchStudioOverview()
      .then((overview) => {
        setStudioOverview(overview);
        setTurnVoiceId((current) => (
          overview.voices.some((voice) => voice.voice_id === current)
            ? current
            : (overview.voices[0]?.voice_id ?? "moss_default")
        ));
        setTurnTtsModel((current) => (
          overview.routes.some((route) => route.name === current)
            ? current
            : preferredTurnRoute(overview.routes)
        ));
      })
      .catch((err: Error) => setTurnError(err.message));
  }, []);

  async function runVoiceTurn(trigger: "manual" | "auto-final") {
    if (!finalText.trim()) {
      setTurnError("Wait for a final transcript before generating a voice reply.");
      return;
    }
    setTurnBusy(true);
    setTurnError(null);
    try {
      const payload = await generateVoiceTurn({
        transcript_text: finalText.trim(),
        voice: turnVoiceId,
        tts_model: turnTtsModel,
        format: "wav",
        sample_rate: 24000,
        style: { speed: 1.0, emotion: "neutral" },
        metadata: {
          source: "asr_live_turn_mode",
          extra: {
            trigger,
            asr_session_id: sessionId,
            asr_model_used: modelUsed,
            partial_event_count: partialEventCount
          }
        }
      });
      setTurnResult(payload);
      if (sessionId) {
        lastAutoReplySessionRef.current = sessionId;
      }
    } catch (err) {
      setTurnError((err as Error).message);
    } finally {
      setTurnBusy(false);
    }
  }

  useEffect(() => {
    if (!turnAutoReply || !sessionId || !finalText.trim()) {
      return;
    }
    if (lastAutoReplySessionRef.current === sessionId) {
      return;
    }
    void runVoiceTurn("auto-final");
  }, [finalText, sessionId, turnAutoReply]);

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
            <strong>{partialEventCount}</strong>
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
            <span className="label">Transcript chars</span>
            <strong>{transcriptChars}</strong>
          </div>
        </div>
        <TranscriptPane
          partialText={partialText}
          partialEventCount={partialEventCount}
          finalText={finalText}
          finalSegments={finalSegments}
        />
        <p className="muted">Model route: <strong>{model}</strong>. Auto will use the configured realtime lane when available and fall back if it is not ready.</p>
        <p className="muted">Disconnect finalizes the active stream and waits for the backend to flush the last transcript window before the session is closed.</p>
        {fallbackUsed ? <p className="muted">Fallback was used for this stream start. The selected realtime lane was not available.</p> : null}
        {triageEnabled ? <p className="muted">Triage flag is being sent with the stream start request. Persisted classification will appear on the Sessions page once the backend lane records it.</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>

      <Panel title="Turn-based voice reply" eyebrow="ASR -> LLM -> TTS">
        <div className="toolbar">
          <button onClick={() => void runVoiceTurn("manual")} disabled={!finalText.trim() || turnBusy}>
            {turnBusy ? "Generating reply..." : "Reply from final transcript"}
          </button>
          <label className="switch">
            <input type="checkbox" checked={turnAutoReply} onChange={(event) => setTurnAutoReply(event.target.checked)} />
            Auto reply on final transcript
          </label>
          <Badge value={routing?.enabled ? "routing-enabled" : "routing-disabled"} tone={routing?.enabled ? "good" : "warn"} />
        </div>
        <div className="meta-grid">
          <div className="meta-card">
            <span className="label">LLM provider</span>
            <strong>{routing?.provider ?? "unconfigured"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">LLM model</span>
            <strong>{routing?.model ?? "unconfigured"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">TTS route</span>
            <strong>{turnResult?.tts_model_used ?? turnTtsModel}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Voice</span>
            <strong>{turnVoices.find((voice) => voice.voice_id === turnVoiceId)?.display_name ?? turnVoiceId}</strong>
          </div>
          <div className="meta-card">
            <span className="label">LLM time</span>
            <strong>{formatMs(turnResult?.llm_timings?.total_ms ?? null)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Round trip</span>
            <strong>{formatMs(turnResult?.timings?.total_ms ?? null)}</strong>
          </div>
        </div>
        <div className="toolbar">
          <select value={turnVoiceId} onChange={(event) => setTurnVoiceId(event.target.value)}>
            {turnVoices.map((voice) => (
              <option key={voice.voice_id} value={voice.voice_id}>
                {voice.display_name}
              </option>
            ))}
          </select>
          <select value={turnTtsModel} onChange={(event) => setTurnTtsModel(event.target.value as StudioRouteDescriptor["name"])}>
            {turnRoutes.map((route) => (
              <option key={route.name} value={route.name}>
                {route.label} {route.invokable ? "" : `(${route.status})`}
              </option>
            ))}
          </select>
        </div>
        <div className="stack">
          <div>
            <p className="label">Transcript sent to LLM</p>
            <p>{finalText || "The final ASR transcript will land here once the live stream flushes."}</p>
          </div>
          <div>
            <p className="label">LLM response</p>
            <p>{turnResult?.response_text ?? "The generated response will appear here before playback."}</p>
          </div>
        </div>
        {turnResult ? (
          <div className="stack">
            <audio key={turnResult.request_id} controls autoPlay src={turnResult.audio_url} />
            <p className="muted">
              Reply session <strong>{turnResult.session_id}</strong> used <strong>{turnResult.llm_model_used}</strong> for generation and <strong>{turnResult.tts_model_used}</strong> for synthesis.
            </p>
          </div>
        ) : null}
        <p className="muted">This lane uses the saved provider/model from <code className="inline-code">TTS Studio -&gt; LLM Routing</code>, waits for a final Voxtral transcript, then synthesizes a full batch reply instead of hard realtime audio.</p>
        {turnError ? <p className="error-text">{turnError}</p> : null}
      </Panel>
    </div>
  );
}
