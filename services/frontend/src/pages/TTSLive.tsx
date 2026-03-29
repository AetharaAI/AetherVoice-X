import { useEffect, useMemo, useState } from "react";

import { fetchStudioVoices, importStudioVoice, warmStudioRouteDetailed } from "../api/studio";
import { fetchModels } from "../api/sessions";
import { synthesizeText } from "../api/tts";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { WaveformPlaceholder } from "../components/tts/WaveformPlaceholder";
import { useTTSStream } from "../hooks/useTTSStream";
import { formatMs } from "../lib/format";
import type { ModelInfo, StudioVoice, TTSResponse } from "../types/api";

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
  if (value === "generating" || value === "streaming-audio" || value === "finalizing" || value === "batch-generating") {
    return "warn" as const;
  }
  return "default" as const;
}

function statusHeadline(value: string, hasFinalAudio: boolean) {
  if (hasFinalAudio) {
    return value.startsWith("batch") ? "Batch-backed audio ready for review" : "Audio ready for review";
  }
  if (value === "generation-error") {
    return "Generation failed before audio returned";
  }
  if (value === "batch-generating") {
    return "Batch-backed live synthesis is generating";
  }
  if (value === "batch-ready") {
    return "Batch-backed live lane armed";
  }
  if (value === "generating") {
    return "Realtime TTS is generating";
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
    return value.startsWith("batch")
      ? "Batch-backed live synthesis finished. Final audio is ready for playback or download."
      : "Realtime TTS active. Final audio has landed and is ready for playback or download.";
  }
  if (value === "generation-error") {
    return "The realtime TTS lane accepted the stream, then the backend generation path failed before a final waveform came back.";
  }
  if (value === "batch-generating") {
    return `Batch-backed live synthesis is generating from the latest ${lastSentChars || 0}-character payload.`;
  }
  if (value === "batch-ready") {
    return `Batch-backed live lane armed for ${sessionId ?? "pending session"}. Each send returns a single finalized waveform so you can compare Qwen voice quality and total latency.`;
  }
  if (value === "generating") {
    return `Realtime TTS is generating from the latest ${lastSentChars || 0}-character payload.`;
  }
  if (value === "streaming-audio") {
    return "Realtime TTS is emitting audio chunks. Stay on the lane until the final frame arrives.";
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

function isBatchBackedLiveModel(entry: ModelInfo) {
  return entry.kind === "tts" && (entry.supports_streaming || entry.name === "qwen_customvoice");
}

function sortVoices(left: StudioVoice, right: StudioVoice) {
  const rank = (voice: StudioVoice) => {
    if (voice.runtime_target === "kokoro_realtime") {
      return 0;
    }
    if (voice.runtime_target === "voxtral_tts") {
      return 1;
    }
    if (voice.runtime_target === "voxtream_realtime") {
      return 2;
    }
    if (voice.runtime_target === "voxtream2_realtime") {
      return 3;
    }
    if (voice.runtime_target === "qwen_customvoice" || voice.runtime_target === "qwen_customvoice_streaming") {
      return 4;
    }
    if (voice.runtime_target === "chatterbox") {
      return 5;
    }
    return 6;
  };
  return rank(left) - rank(right) || left.display_name.localeCompare(right.display_name);
}

function usesReferenceVoiceAssets(model: string) {
  return model === "voxtream_realtime" || model === "voxtream2_realtime" || model === "chatterbox";
}

function supportsDynamicSpeakingRate(model: string) {
  return model === "voxtream2_realtime" || model === "voxtream_realtime";
}

function supportsManualWarmup(model: string) {
  return model === "voxtream2_realtime" || model === "voxtream_realtime";
}

function voiceSelectorLabel(model: string) {
  return usesReferenceVoiceAssets(model) ? "Reference voice asset" : "Voice preset";
}

function voiceImportDefaultName(model: string) {
  if (model === "voxtream2_realtime") {
    return "Voxtream2 Reference";
  }
  if (model === "voxtream_realtime") {
    return "Voxtream Reference";
  }
  if (model === "chatterbox") {
    return "Chatterbox Reference";
  }
  return "Reference Voice";
}

export function TTSLive() {
  const stream = useTTSStream();
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [voices, setVoices] = useState<StudioVoice[]>([]);
  const [model, setModel] = useState("kokoro_realtime");
  const [voiceId, setVoiceId] = useState("af_sky");
  const [sessionProfile, setSessionProfile] = useState("telephony");
  const [tone, setTone] = useState("warm");
  const [cadence, setCadence] = useState("telephony");
  const [speakingStyle, setSpeakingStyle] = useState("service");
  const [latencyMode, setLatencyMode] = useState("low_latency");
  const [sampleRate, setSampleRate] = useState(24000);
  const [prefillTextLen, setPrefillTextLen] = useState(24);
  const [decodeChunkFrames, setDecodeChunkFrames] = useState(6);
  const [decodeOverlapFrames, setDecodeOverlapFrames] = useState(0);
  const [temperature, setTemperature] = useState(0.45);
  const [topP, setTopP] = useState(0.65);
  const [topK, setTopK] = useState(30);
  const [repetitionPenalty, setRepetitionPenalty] = useState(1.1);
  const [repetitionWindow, setRepetitionWindow] = useState(50);
  const [speakingRate, setSpeakingRate] = useState(2.0);
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [rawDirectives, setRawDirectives] = useState("<agent tone=\"warm\" cadence=\"telephony\" />");
  const [batchSessionArmed, setBatchSessionArmed] = useState(false);
  const [batchConnectionLabel, setBatchConnectionLabel] = useState("idle");
  const [batchSessionId, setBatchSessionId] = useState<string | null>(null);
  const [batchResponse, setBatchResponse] = useState<TTSResponse | null>(null);
  const [batchEvents, setBatchEvents] = useState<string[]>([]);
  const [batchError, setBatchError] = useState<string | null>(null);
  const [batchObservedTotalMs, setBatchObservedTotalMs] = useState<number | null>(null);
  const [referenceImportName, setReferenceImportName] = useState("Voxtream2 Reference");
  const [referenceImportFile, setReferenceImportFile] = useState<File | null>(null);
  const [referenceImportTags, setReferenceImportTags] = useState("telephony, reference");
  const [referenceImportNotes, setReferenceImportNotes] = useState("Imported from TTS Live for fast realtime reference-voice evaluation.");
  const [referenceImportText, setReferenceImportText] = useState("");
  const [referenceImportBusy, setReferenceImportBusy] = useState(false);
  const [referenceImportMessage, setReferenceImportMessage] = useState<string | null>(null);
  const [referenceImportError, setReferenceImportError] = useState<string | null>(null);
  const [warmupBusy, setWarmupBusy] = useState(false);
  const [warmupMessage, setWarmupMessage] = useState<string | null>(null);
  const [warmupError, setWarmupError] = useState<string | null>(null);

  const liveModels = useMemo(() => models.filter(isBatchBackedLiveModel), [models]);
  const selectedModel = useMemo(() => liveModels.find((entry) => entry.name === model) ?? null, [liveModels, model]);
  const isBatchBackedLive = Boolean(selectedModel && !selectedModel.supports_streaming);
  const referenceVoiceModel = usesReferenceVoiceAssets(model);
  const warmupEnabled = supportsManualWarmup(model);
  const sortedVoices = useMemo(() => [...voices].sort(sortVoices), [voices]);
  const modelVoices = useMemo(() => {
    if (model.startsWith("qwen_customvoice")) {
      return sortedVoices.filter(
        (voice) => voice.runtime_target === "qwen_customvoice" || voice.runtime_target === "qwen_customvoice_streaming"
      );
    }
    if (model === "kokoro_realtime") {
      return sortedVoices.filter((voice) => voice.runtime_target === "kokoro_realtime");
    }
    if (model === "voxtral_tts") {
      return sortedVoices.filter((voice) => voice.runtime_target === "voxtral_tts");
    }
    if (model === "voxtream_realtime") {
      return sortedVoices.filter((voice) => voice.runtime_target === "voxtream_realtime" && Boolean(voice.reference_audio_path));
    }
    if (model === "voxtream2_realtime") {
      return sortedVoices.filter((voice) => voice.runtime_target === "voxtream2_realtime" && Boolean(voice.reference_audio_path));
    }
    if (model === "chatterbox") {
      return sortedVoices.filter((voice) => voice.runtime_target === "chatterbox" || Boolean(voice.reference_audio_path));
    }
    return sortedVoices;
  }, [model, sortedVoices]);
  const selectedVoice = modelVoices.find((voice) => voice.voice_id === voiceId) ?? modelVoices[0] ?? null;
  const selectedVoiceAsset = selectedVoice?.display_name ?? "Kokoro Default Voice";
  const requestedPreset = selectedVoice?.voice_id ?? "af_sky";

  const realtimeProfile = useMemo(
    () => ({
      voice_preset_id: selectedVoice?.voice_id ?? "af_sky",
      session_profile: sessionProfile,
      tone,
      cadence,
      speaking_style: speakingStyle,
      latency_mode: latencyMode,
      ...(supportsDynamicSpeakingRate(model) ? { speaking_rate: speakingRate } : {}),
      raw_directives: rawDirectives,
    }),
    [cadence, latencyMode, model, rawDirectives, selectedVoice?.voice_id, sessionProfile, speakingRate, speakingStyle, tone]
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
      repetition_window: repetitionWindow,
      ...(supportsDynamicSpeakingRate(model) ? { speaking_rate: speakingRate } : {}),
    }),
    [decodeChunkFrames, decodeOverlapFrames, model, prefillTextLen, repetitionPenalty, repetitionWindow, speakingRate, temperature, topK, topP]
  );

  async function refreshVoices() {
    const payload = await fetchStudioVoices();
    setVoices(payload);
    return payload;
  }

  useEffect(() => {
    fetchModels()
      .then((payload) => setModels(payload))
      .catch(() => setModels([]));
    refreshVoices()
      .then(() => undefined)
      .catch(() => setVoices([]));
  }, []);

  useEffect(() => {
    if (!referenceVoiceModel) {
      return;
    }
    setReferenceImportName((current) => (current.trim() ? current : voiceImportDefaultName(model)));
    setReferenceImportMessage(null);
    setReferenceImportError(null);
  }, [model, referenceVoiceModel]);

  useEffect(() => {
    if (liveModels.length > 0 && !liveModels.some((entry) => entry.name === model)) {
      setModel(liveModels[0].name);
    }
  }, [liveModels, model]);

  useEffect(() => {
    if (modelVoices.length > 0 && !modelVoices.some((voice) => voice.voice_id === voiceId)) {
      setVoiceId(modelVoices[0].voice_id);
    }
  }, [modelVoices, voiceId]);

  function appendBatchEvent(message: string) {
    setBatchEvents((current) => [...current.slice(-11), message]);
  }

  function resetBatchState() {
    setBatchSessionArmed(false);
    setBatchConnectionLabel("idle");
    setBatchSessionId(null);
    setBatchResponse(null);
    setBatchObservedTotalMs(null);
    setBatchEvents([]);
    setBatchError(null);
  }

  async function handleReferenceImport() {
    if (!referenceImportFile) {
      setReferenceImportError("Choose a reference WAV before importing.");
      return;
    }
    setReferenceImportBusy(true);
    setReferenceImportError(null);
    setReferenceImportMessage(null);
    try {
      const form = new FormData();
      form.set("file", referenceImportFile);
      form.set("display_name", referenceImportName.trim() || voiceImportDefaultName(model));
      form.set("source_model", "imported");
      form.set("runtime_target", model);
      form.set("voice_type", "imported");
      form.set("notes", referenceImportNotes.trim());
      form.set("tags", referenceImportTags.trim());
      if (referenceImportText.trim()) {
        form.set("reference_text", referenceImportText.trim());
      }
      const voice = await importStudioVoice(form);
      const nextVoices = await refreshVoices();
      setReferenceImportMessage(`Imported ${voice.display_name} into the shared voice library.`);
      setReferenceImportFile(null);
      setVoiceId(voice.voice_id);
      if (!nextVoices.some((entry) => entry.voice_id === voice.voice_id)) {
        setReferenceImportError(`Imported ${voice.display_name}, but the live voice list did not refresh yet.`);
      }
    } catch (err) {
      setReferenceImportError((err as Error).message);
    } finally {
      setReferenceImportBusy(false);
    }
  }

  async function handleStart() {
    if (!isBatchBackedLive) {
      await stream.connect({
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
            realtime_tuning: realtimeTuning,
          },
        },
      });
      return;
    }
    const session = `sess_tts_live_batch_${Date.now().toString(36)}`;
    setBatchSessionArmed(true);
    setBatchConnectionLabel("batch-ready");
    setBatchSessionId(session);
    setBatchResponse(null);
    setBatchEvents([`batch lane armed · ${session}`, `route selected · ${model}`, `voice selected · ${selectedVoice?.display_name ?? voiceId}`]);
    setBatchError(null);
  }

  async function handleWarmup() {
    if (!warmupEnabled || sessionOpen) {
      return;
    }
    setWarmupBusy(true);
    setWarmupError(null);
    setWarmupMessage(null);
    try {
      const payload = await warmStudioRouteDetailed(model);
      const status = String(payload.warmup.status ?? "ready");
      const elapsedMs = payload.warmup.elapsed_ms;
      const elapsedLabel = typeof elapsedMs === "number" ? `${Math.round(elapsedMs)} ms` : null;
      const routeLabel = String(payload.warmup.route ?? payload.route ?? model);
      setWarmupMessage(`Warmup ${status} on ${routeLabel}${elapsedLabel ? ` in ${elapsedLabel}` : ""}.`);
    } catch (err) {
      setWarmupError((err as Error).message);
    } finally {
      setWarmupBusy(false);
    }
  }

  async function handleSend() {
    if (!isBatchBackedLive) {
      await stream.send(bodyText.trim());
      return;
    }
    if (!batchSessionArmed) {
      setBatchError("Batch-backed live lane is not armed.");
      return;
    }
    if (!bodyText.trim()) {
      setBatchError("Nothing to send.");
      return;
    }
    try {
      setBatchError(null);
      setBatchResponse(null);
      setBatchObservedTotalMs(null);
      setBatchConnectionLabel("batch-generating");
      appendBatchEvent(`batch request started · ${bodyText.trim().length} chars`);
      const startedAt = performance.now();
      const response = await synthesizeText({
        model,
        voice: selectedVoice?.voice_id ?? voiceId,
        text: bodyText.trim(),
        format: "wav",
        sample_rate: sampleRate,
        stream: false,
        style: {
          emotion: tone === "neutral" ? "neutral" : tone,
          speed: 1,
          speaker_hint: selectedVoice?.display_name ?? undefined,
        },
        metadata: {
          source: "console",
          lane: "tts_live_batch_probe",
          extra: {
            realtime_profile: realtimeProfile,
            realtime_tuning: realtimeTuning,
            live_mode: "batch_backed",
            qwen_instructions: rawDirectives.trim() || undefined,
          },
        },
      });
      setBatchObservedTotalMs(Math.round(performance.now() - startedAt));
      setBatchResponse(response);
      setBatchSessionId(response.session_id);
      setBatchConnectionLabel("batch-ready");
      appendBatchEvent(`batch audio ready · ${response.audio_url}`);
      appendBatchEvent(`total latency · ${formatMs(response.timings.total_ms)}`);
      appendBatchEvent(`inference latency · ${formatMs(response.timings.inference_ms)}`);
    } catch (err) {
      setBatchError((err as Error).message);
      setBatchConnectionLabel("generation-error");
      appendBatchEvent(`batch generation failed · ${(err as Error).message}`);
    }
  }

  function handleStop() {
    if (!isBatchBackedLive) {
      stream.stop();
      return;
    }
    resetBatchState();
  }

  const sessionOpen = isBatchBackedLive ? batchSessionArmed : stream.connected;
  const connectionLabel = isBatchBackedLive ? batchConnectionLabel : stream.connectionLabel;
  const sessionId = isBatchBackedLive ? batchSessionId : stream.sessionId;
  const modelUsed = isBatchBackedLive ? batchResponse?.model_used ?? selectedModel?.name ?? model : stream.modelUsed;
  const runtimeTruth = isBatchBackedLive ? null : stream.runtimeTruth;
  const chunkCount = isBatchBackedLive ? 0 : stream.chunkCount;
  const lastSentChars = isBatchBackedLive ? bodyText.trim().length : stream.lastSentChars;
  const finalUrl = isBatchBackedLive ? batchResponse?.audio_url ?? null : stream.finalUrl;
  const events = isBatchBackedLive ? batchEvents : stream.events;
  const error = isBatchBackedLive ? batchError : stream.error;
  const wsUrl = isBatchBackedLive ? null : stream.wsUrl;
  const hasFinalAudio = Boolean(finalUrl);
  const liveTone = connectionTone(connectionLabel, hasFinalAudio);
  const busy = ["starting", "opening-socket", "generating", "streaming-audio", "finalizing", "batch-generating"].includes(connectionLabel);
  const runtimeConditioning = isBatchBackedLive
    ? "provider_batch_live_probe"
    : runtimeTruth?.actual_runtime_conditioning_source ?? "pending";
  const fallbackVoicePath = isBatchBackedLive ? "none" : runtimeTruth?.fallback_voice_path ?? "none";
  const runtimePathUsed = isBatchBackedLive ? modelUsed ?? model : runtimeTruth?.runtime_path_used ?? modelUsed ?? model;
  const observedFirstChunkMs = isBatchBackedLive ? null : stream.latencies.observedFirstChunkMs;
  const observedFinalAudioMs = isBatchBackedLive ? batchObservedTotalMs : stream.latencies.observedFinalAudioMs;
  const backendFirstChunkMs = isBatchBackedLive ? null : stream.latencies.backendFirstChunkMs;
  const backendInferenceMs = isBatchBackedLive ? batchResponse?.timings?.inference_ms ?? null : stream.latencies.backendInferenceMs;
  const backendTotalMs = isBatchBackedLive ? batchResponse?.timings?.total_ms ?? null : stream.latencies.backendTotalMs;
  const outputHint = isBatchBackedLive
    ? "This lane is batch-backed for Qwen evaluation. Each send returns one finalized WAV so you can judge voice quality and total latency without claiming realtime chunks."
    : "The finalized WAV appears here after you click End stream. Live audio chunks can still play before that, but the downloadable file is assembled at stream close.";

  return (
    <div className="page-grid">
      <Panel title="Realtime synthesis lane" eyebrow="TTS Live">
        <div className="toolbar">
          <button onClick={handleStart} disabled={sessionOpen}>
            {isBatchBackedLive ? (batchSessionArmed ? "Batch lane armed" : "Arm batch lane") : "Start stream"}
          </button>
          {warmupEnabled ? (
            <button onClick={() => void handleWarmup()} disabled={sessionOpen || warmupBusy} className="secondary">
              {warmupBusy ? "Warming..." : "Warm up"}
            </button>
          ) : null}
          <button onClick={handleSend} disabled={!sessionOpen || !bodyText.trim()}>
            {isBatchBackedLive ? "Generate audio" : "Send text"}
          </button>
          <button onClick={handleStop} disabled={!sessionOpen} className="secondary">
            {isBatchBackedLive ? "Reset lane" : "End stream"}
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
              <strong>{chunkCount || (isBatchBackedLive && hasFinalAudio ? 1 : 0)}</strong>
            </div>
            <div className="status-chip">
              <span className="label">Audio</span>
              <strong>{hasFinalAudio ? "ready" : "pending"}</strong>
            </div>
            <div className="status-chip">
              <span className="label">First chunk</span>
              <strong>{formatMs(observedFirstChunkMs)}</strong>
            </div>
            <div className="status-chip">
              <span className="label">Final audio</span>
              <strong>{formatMs(observedFinalAudioMs)}</strong>
            </div>
          </div>
        </section>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-model">Synthesis model</label>
            <select id="tts-live-model" value={model} onChange={(event) => setModel(event.target.value)} disabled={sessionOpen}>
              {liveModels.length ? (
                liveModels.map((entry) => (
                  <option key={entry.name} value={entry.name}>
                    {entry.name} {entry.supports_streaming ? "(streaming)" : "(batch-backed live)"}
                  </option>
                ))
              ) : (
                <option value="kokoro_realtime">kokoro_realtime</option>
              )}
            </select>
            <p className="field-hint">
              {isBatchBackedLive
                ? "Qwen is exposed here as a batch-backed live probe so you can judge voices and total latency on the operator lane without pretending it is websocket-streaming."
                : "Keep this lane on the realtime route for live agent turn-taking. Wider studio workflows belong in TTS Studio."}
            </p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-voice">{voiceSelectorLabel(model)}</label>
            <select id="tts-live-voice" value={selectedVoice?.voice_id ?? voiceId} onChange={(event) => setVoiceId(event.target.value)} disabled={sessionOpen}>
              {modelVoices.length ? (
                modelVoices.map((voice) => (
                  <option key={voice.voice_id} value={voice.voice_id}>
                    {voice.display_name} {voice.runtime_target !== model ? `(${voice.runtime_target})` : ""}
                  </option>
                ))
              ) : (
                <option value="af_sky">Sky</option>
              )}
            </select>
            <p className="field-hint">
              {isBatchBackedLive
                ? "Qwen voices here are the seeded built-in CustomVoice presets. Use this lane to compare voice quality and total generation time before moving into telephony harness tests."
                : model.startsWith("qwen_customvoice")
                  ? "Qwen streaming uses the same seeded CustomVoice preset list. This lane is for first-audio and chunk-latency judgment against the batch-backed Qwen probe."
                : runtimePathUsed === "voxtream_realtime"
                  ? "Original Voxtream expects a bound reference-audio asset and benefits from reference text. Pick an imported or generated voice with a real WAV asset before judging telephony realism."
                : runtimePathUsed === "voxtream2_realtime"
                  ? "Voxtream2 expects a bound reference-audio asset for zero-shot prompting and adds dynamic speaking-rate control. Pick an imported or generated voice with a real WAV asset before judging telephony realism."
                : runtimePathUsed === "kokoro_realtime"
                  ? "Kokoro uses built-in preset voices for the live lane, so no reference-audio conditioning is required."
                  : runtimePathUsed === "voxtral_tts"
                    ? "Voxtral TTS uses built-in preset voices from the provider lane and supports both low-latency streaming and batch synthesis."
                  : runtimeTruth?.conditioning_active
                    ? "This session resolved to a real conditioning asset. Realtime inference is materially using the bound conditioning source."
                  : "This session is falling back to the default global prompt path because the selected voice does not have a usable reference asset."}
            </p>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-sample-rate">Sample rate</label>
            <select id="tts-live-sample-rate" value={sampleRate} onChange={(event) => setSampleRate(Number(event.target.value))} disabled={sessionOpen}>
              <option value={24000}>24000 Hz</option>
            </select>
            <p className="field-hint">Live testing stays pinned to the model-native sample rate for now.</p>
          </div>
        </div>
        {referenceVoiceModel ? (
          <details className="accordion" open>
            <summary>Reference voice library</summary>
            <div className="accordion-body">
              <div className="control-grid">
                <div className="field-group">
                  <label htmlFor="tts-live-reference-file">Reference WAV</label>
                  <input
                    id="tts-live-reference-file"
                    type="file"
                    accept="audio/wav,audio/*"
                    onChange={(event) => setReferenceImportFile(event.target.files?.[0] ?? null)}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                  <p className="field-hint">Imports a reusable voice asset into the Studio registry so Voxtream can clone from a dropdown instead of a raw VM path.</p>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-name">Asset name</label>
                  <input
                    id="tts-live-reference-name"
                    value={referenceImportName}
                    onChange={(event) => setReferenceImportName(event.target.value)}
                    placeholder={voiceImportDefaultName(model)}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-tags">Tags</label>
                  <input
                    id="tts-live-reference-tags"
                    value={referenceImportTags}
                    onChange={(event) => setReferenceImportTags(event.target.value)}
                    placeholder="telephony, dispatch, male"
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
              </div>
              <div className="control-grid">
                <div className="field-group">
                  <label htmlFor="tts-live-reference-text">Reference transcript</label>
                  <textarea
                    id="tts-live-reference-text"
                    value={referenceImportText}
                    onChange={(event) => setReferenceImportText(event.target.value)}
                    rows={3}
                    placeholder={model === "voxtream_realtime" ? "Optional but recommended for original Voxtream." : "Optional. Voxtream2 can run without it, but save it when you have it."}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-notes">Operator notes</label>
                  <textarea
                    id="tts-live-reference-notes"
                    value={referenceImportNotes}
                    onChange={(event) => setReferenceImportNotes(event.target.value)}
                    rows={3}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
              </div>
              <div className="toolbar">
                <button onClick={() => void handleReferenceImport()} disabled={sessionOpen || referenceImportBusy}>
                  {referenceImportBusy ? "Importing reference..." : "Import reference into library"}
                </button>
                <Badge value={`${modelVoices.length} assets`} tone={modelVoices.length ? "good" : "warn"} />
              </div>
              {selectedVoice?.reference_audio_path ? (
                <p className="field-hint">
                  Active reference asset: <code className="inline-code">{selectedVoice.reference_audio_path}</code>
                </p>
              ) : null}
              {referenceImportMessage ? <p className="muted">{referenceImportMessage}</p> : null}
              {referenceImportError ? <p className="error-text">{referenceImportError}</p> : null}
            </div>
          </details>
        ) : null}
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-profile">Session profile</label>
            <select id="tts-live-profile" value={sessionProfile} onChange={(event) => setSessionProfile(event.target.value)} disabled={sessionOpen}>
              <option value="telephony">Telephony</option>
              <option value="assistant">Assistant</option>
              <option value="narration">Narration</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-tone">Tone</label>
            <select id="tts-live-tone" value={tone} onChange={(event) => setTone(event.target.value)} disabled={sessionOpen}>
              <option value="warm">warm</option>
              <option value="calm">calm</option>
              <option value="neutral">neutral</option>
              <option value="confident">confident</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-cadence">Cadence</label>
            <select id="tts-live-cadence" value={cadence} onChange={(event) => setCadence(event.target.value)} disabled={sessionOpen}>
              <option value="telephony">telephony</option>
              <option value="conversational">conversational</option>
              <option value="measured">measured</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-style">Speaking style</label>
            <select id="tts-live-style" value={speakingStyle} onChange={(event) => setSpeakingStyle(event.target.value)} disabled={sessionOpen}>
              <option value="service">service</option>
              <option value="dispatcher">dispatcher</option>
              <option value="support">support</option>
              <option value="narrator">narrator</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="tts-live-latency">Latency profile</label>
            <select id="tts-live-latency" value={latencyMode} onChange={(event) => setLatencyMode(event.target.value)} disabled={sessionOpen}>
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
                <input id="tts-live-prefill" type="number" min={1} max={64} value={prefillTextLen} onChange={(event) => setPrefillTextLen(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-chunk-frames">Decode chunk frames</label>
                <input id="tts-live-chunk-frames" type="number" min={1} max={64} value={decodeChunkFrames} onChange={(event) => setDecodeChunkFrames(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-overlap-frames">Decode overlap frames</label>
                <input id="tts-live-overlap-frames" type="number" min={0} max={16} value={decodeOverlapFrames} onChange={(event) => setDecodeOverlapFrames(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-temperature">Temperature</label>
                <input id="tts-live-temperature" type="number" min={0.1} max={2} step={0.05} value={temperature} onChange={(event) => setTemperature(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-top-p">Top p</label>
                <input id="tts-live-top-p" type="number" min={0.05} max={1} step={0.05} value={topP} onChange={(event) => setTopP(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-top-k">Top k</label>
                <input id="tts-live-top-k" type="number" min={1} max={200} step={1} value={topK} onChange={(event) => setTopK(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-repetition-penalty">Repetition penalty</label>
                <input id="tts-live-repetition-penalty" type="number" min={0.8} max={2} step={0.05} value={repetitionPenalty} onChange={(event) => setRepetitionPenalty(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              <div className="field-group">
                <label htmlFor="tts-live-repetition-window">Repetition window</label>
                <input id="tts-live-repetition-window" type="number" min={1} max={512} step={1} value={repetitionWindow} onChange={(event) => setRepetitionWindow(Number(event.target.value))} disabled={sessionOpen} />
              </div>
              {supportsDynamicSpeakingRate(model) ? (
                <div className="field-group">
                  <label htmlFor="tts-live-speaking-rate">Speaking rate</label>
                  <input
                    id="tts-live-speaking-rate"
                    type="number"
                    min={0.5}
                    max={5}
                    step={0.1}
                    value={speakingRate}
                    onChange={(event) => setSpeakingRate(Number(event.target.value))}
                    disabled={sessionOpen}
                  />
                </div>
              ) : null}
            </div>
            <p className="field-hint">
              {isBatchBackedLive
                ? "These controls are preserved in metadata for the Qwen provider. This lane is for latency and voice evaluation, not true chunked streaming yet."
                : supportsDynamicSpeakingRate(model)
                  ? "These controls apply at stream start for the current session only. Voxtream routes also read the speaking-rate knob here, so you can judge cadence and latency without changing provider env defaults."
                  : "These controls apply at stream start for the current session only. Use them for immediate live quality tests without changing backend env defaults."}
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
            <span className="label">Reference path</span>
            <strong className="meta-value-wrap">{selectedVoice?.reference_audio_path ?? "none"}</strong>
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
            <span className="label">Provider first chunk</span>
            <strong>{formatMs(backendFirstChunkMs)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Provider inference</span>
            <strong>{formatMs(backendInferenceMs)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Provider total</span>
            <strong>{formatMs(backendTotalMs)}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Delivery contract</span>
            <strong className="meta-value-wrap">{isBatchBackedLive ? `batch-backed via /v1/tts/synthesize · ${formatMs(batchResponse?.timings?.total_ms)}` : wsUrl ?? "pending"}</strong>
          </div>
        </div>
        <div className="control-grid">
          <div className="field-group">
            <label htmlFor="tts-live-body">Spoken body</label>
            <textarea id="tts-live-body" value={bodyText} onChange={(event) => setBodyText(event.target.value)} rows={5} placeholder="Write the response your agent should say." />
            <p className="field-hint">Only the spoken body is sent into the live utterance. Session profile and style controls ride in backend state.</p>
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
              <p className="field-hint">{outputHint}</p>
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
        <p className="muted">
          {isBatchBackedLive
            ? "Primary use case: compare Qwen voices, artifacts, and total latency on the operator surface before deciding whether the model is good enough to promote into a deeper telephony harness."
            : "Primary use case: keep the stream open, bind a voice preset to the session, and push plain assistant text from your reasoning layer with minimal operator ceremony."}
        </p>
        {warmupMessage ? <p className="muted">{warmupMessage}</p> : null}
        {warmupError ? <p className="error-text">{warmupError}</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
