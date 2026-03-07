import { useEffect, useRef, useState } from "react";

import { startASRStream } from "../api/asr";

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
  const [partials, setPartials] = useState<string[]>([]);
  const [finalText, setFinalText] = useState("");
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

  useEffect(() => () => void stop(), []);

  async function start(model = "auto", triageEnabled = false) {
    try {
      setError(null);
      setSessionId(null);
      setModelUsed(null);
      setFallbackUsed(false);
      setPartials([]);
      setFinalText("");
      setFirstPartialMs(null);
      setFinalMs(null);
      setFramesSent(0);
      setLatencyLabel("requesting-mic");
      sequenceRef.current = 0;
      startedAtRef.current = Date.now();
      firstPartialRecordedRef.current = false;
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
        const payload = JSON.parse(event.data) as { type: string; text?: string };
        if (payload.type === "partial_transcript" && payload.text) {
          setPartials((current) => [...current.slice(-4), payload.text as string]);
          setLatencyLabel("partial");
          if (startedAtRef.current && !firstPartialRecordedRef.current) {
            firstPartialRecordedRef.current = true;
            setFirstPartialMs(Date.now() - startedAtRef.current);
          }
        }
        if (payload.type === "final_transcript" && payload.text) {
          setFinalText(payload.text);
          setLatencyLabel("final");
          if (startedAtRef.current) {
            setFinalMs(Date.now() - startedAtRef.current);
          }
        }
      };
      socket.onerror = () => {
        setError("WebSocket stream failed.");
        setLatencyLabel("socket-error");
        setConnected(false);
      };
      socket.onclose = () => {
        setConnected(false);
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
      mediaRef.current?.getTracks().forEach((track) => track.stop());
      mediaRef.current = null;
      setConnected(false);
    }
  }

  function stop() {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: "end_stream" }));
      socketRef.current.close();
    }
    processorRef.current?.disconnect();
    contextRef.current?.close();
    mediaRef.current?.getTracks().forEach((track) => track.stop());
    processorRef.current = null;
    contextRef.current = null;
    mediaRef.current = null;
    socketRef.current = null;
    setConnected(false);
    setLatencyLabel("idle");
  }

  return { connected, sessionId, modelUsed, fallbackUsed, partials, finalText, latencyLabel, firstPartialMs, finalMs, framesSent, error, start, stop };
}
