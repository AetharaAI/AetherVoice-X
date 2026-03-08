import { useEffect, useRef, useState } from "react";

import { startASRStream } from "../api/asr";

const STORAGE_KEY = "aether.asr.live.v1";

type TranscriptSegment = { start_ms?: number; end_ms?: number; text?: string };
type PersistedStreamState = {
  sessionId: string | null;
  modelUsed: string | null;
  fallbackUsed: boolean;
  partialText: string;
  partialEventCount: number;
  finalText: string;
  finalSegments: TranscriptSegment[];
  latencyLabel: string;
  firstPartialMs: number | null;
  finalMs: number | null;
  framesSent: number;
  error: string | null;
};

function encodePcm16(samples: Float32Array) {
  const buffer = new ArrayBuffer(samples.length * 2);
  const view = new DataView(buffer);
  for (let index = 0; index < samples.length; index += 1) {
    const sample = Math.max(-1, Math.min(1, samples[index]));
    view.setInt16(index * 2, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
  }
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

function resolveWsUrl(path: string): string {
  if (/^wss?:\/\//.test(path)) {
    return path;
  }
  const url = new URL(window.location.origin);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = path.startsWith("/") ? path : `/${path}`;
  url.search = "";
  url.hash = "";
  return url.toString();
}

export function useASRStream() {
  const [connected, setConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [modelUsed, setModelUsed] = useState<string | null>(null);
  const [fallbackUsed, setFallbackUsed] = useState(false);
  const [partialText, setPartialText] = useState("");
  const [partialEventCount, setPartialEventCount] = useState(0);
  const [finalText, setFinalText] = useState("");
  const [finalSegments, setFinalSegments] = useState<TranscriptSegment[]>([]);
  const [latencyLabel, setLatencyLabel] = useState("idle");
  const [firstPartialMs, setFirstPartialMs] = useState<number | null>(null);
  const [finalMs, setFinalMs] = useState<number | null>(null);
  const [framesSent, setFramesSent] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const mediaRef = useRef<MediaStream | null>(null);
  const contextRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const sequenceRef = useRef(0);
  const startedAtRef = useRef<number | null>(null);
  const firstPartialRecordedRef = useRef(false);
  const endingRef = useRef(false);
  const finalReceivedRef = useRef(false);

  function cleanupMedia() {
    processorRef.current?.disconnect();
    contextRef.current?.close();
    mediaRef.current?.getTracks().forEach((track) => track.stop());
    processorRef.current = null;
    contextRef.current = null;
    mediaRef.current = null;
  }

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const raw = window.sessionStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return;
    }
    try {
      const persisted = JSON.parse(raw) as PersistedStreamState;
      setSessionId(persisted.sessionId);
      setModelUsed(persisted.modelUsed);
      setFallbackUsed(persisted.fallbackUsed);
      setPartialText(persisted.partialText);
      setPartialEventCount(persisted.partialEventCount);
      setFinalText(persisted.finalText);
      setFinalSegments(persisted.finalSegments);
      setLatencyLabel(persisted.latencyLabel);
      setFirstPartialMs(persisted.firstPartialMs);
      setFinalMs(persisted.finalMs);
      setFramesSent(persisted.framesSent);
      setError(persisted.error);
    } catch {
      window.sessionStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const snapshot: PersistedStreamState = {
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
    };
    window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
  }, [error, fallbackUsed, finalMs, finalSegments, finalText, firstPartialMs, framesSent, latencyLabel, modelUsed, partialEventCount, partialText, sessionId]);

  useEffect(() => () => void stop(), []);

  async function start(model = "auto", triageEnabled = false) {
    try {
      setError(null);
      setSessionId(null);
      setModelUsed(null);
      setFallbackUsed(false);
      setPartialText("");
      setPartialEventCount(0);
      setFinalText("");
      setFinalSegments([]);
      setFirstPartialMs(null);
      setFinalMs(null);
      setFramesSent(0);
      setLatencyLabel("requesting-mic");
      sequenceRef.current = 0;
      startedAtRef.current = Date.now();
      firstPartialRecordedRef.current = false;
      endingRef.current = false;
      finalReceivedRef.current = false;
      const userMedia = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRef.current = userMedia;
      setLatencyLabel("starting-session");
      const streamSession = await startASRStream({
        model,
        language: "auto",
        sample_rate: 16000,
        encoding: "pcm_s16le",
        channels: 1,
        triage_enabled: triageEnabled,
        metadata: { source: "mic" }
      });
      setSessionId(streamSession.session_id);
      setModelUsed(streamSession.model_used ?? model);
      setFallbackUsed(Boolean(streamSession.fallback_used));
      setLatencyLabel("opening-socket");
      const socket = new WebSocket(resolveWsUrl(streamSession.ws_url));
      socketRef.current = socket;
      socket.onmessage = (event) => {
        const payload = JSON.parse(event.data) as { type: string; text?: string; segments?: Array<{ start_ms?: number; end_ms?: number; text?: string }> };
        if (payload.type === "partial_transcript" && payload.text) {
          setPartialText(payload.text.trim());
          setPartialEventCount((current) => current + 1);
          setLatencyLabel("partial");
          if (startedAtRef.current && !firstPartialRecordedRef.current) {
            firstPartialRecordedRef.current = true;
            setFirstPartialMs(Date.now() - startedAtRef.current);
          }
        }
        if (payload.type === "final_transcript" && payload.text) {
          finalReceivedRef.current = true;
          const normalized = payload.text.trim();
          setFinalText(normalized);
          setPartialText(normalized);
          setFinalSegments(payload.segments ?? []);
          setLatencyLabel("final");
          if (startedAtRef.current) {
            setFinalMs(Date.now() - startedAtRef.current);
          }
          cleanupMedia();
          socket.close();
        }
      };
      socket.onerror = () => {
        setError("WebSocket stream failed.");
        setLatencyLabel(endingRef.current ? "finalizing" : "socket-error");
        setConnected(false);
      };
      socket.onclose = () => {
        setConnected(false);
        cleanupMedia();
        socketRef.current = null;
        if (endingRef.current && finalReceivedRef.current) {
          setLatencyLabel("final");
          endingRef.current = false;
          return;
        }
        if (endingRef.current) {
          setLatencyLabel("closed");
          endingRef.current = false;
          return;
        }
        if (latencyLabel !== "final") {
          setLatencyLabel("closed");
        }
      };
      socket.onopen = async () => {
        const context = new AudioContext({ sampleRate: 16000 });
        contextRef.current = context;
        const source = context.createMediaStreamSource(userMedia);
        const processor = context.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;
        processor.onaudioprocess = (evt) => {
          sequenceRef.current += 1;
          setFramesSent(sequenceRef.current);
          const input = evt.inputBuffer.getChannelData(0);
          socket.send(
            JSON.stringify({
              type: "audio_frame",
              seq: sequenceRef.current,
              timestamp_ms: Math.round(context.currentTime * 1000),
              sample_rate: 16000,
              encoding: "pcm_s16le",
              channels: 1,
              payload_b64: encodePcm16(input)
            })
          );
        };
        source.connect(processor);
        processor.connect(context.destination);
        setConnected(true);
        setLatencyLabel("streaming");
      };
    } catch (err) {
      setError((err as Error).message);
      setLatencyLabel("error");
      cleanupMedia();
      setConnected(false);
    }
  }

  function stop() {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      endingRef.current = true;
      setLatencyLabel("finalizing");
      socketRef.current.send(JSON.stringify({ type: "end_stream" }));
      return;
    }
    cleanupMedia();
    socketRef.current = null;
    setConnected(false);
    setLatencyLabel("idle");
  }

  return {
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
    stop
  };
}
