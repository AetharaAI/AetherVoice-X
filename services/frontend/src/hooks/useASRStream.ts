import { useEffect, useRef, useState } from "react";

import { startASRStream } from "../api/asr";
import { getWsBase } from "../api/client";

function encodePcm16(samples: Float32Array) {
  const buffer = new ArrayBuffer(samples.length * 2);
  const view = new DataView(buffer);
  for (let index = 0; index < samples.length; index += 1) {
    const sample = Math.max(-1, Math.min(1, samples[index]));
    view.setInt16(index * 2, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
  }
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

export function useASRStream() {
  const [connected, setConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [partials, setPartials] = useState<string[]>([]);
  const [finalText, setFinalText] = useState("");
  const [latencyLabel, setLatencyLabel] = useState("idle");
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const mediaRef = useRef<MediaStream | null>(null);
  const contextRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const sequenceRef = useRef(0);

  useEffect(() => () => void stop(), []);

  async function start(model = "auto", triageEnabled = false) {
    try {
      setError(null);
      setPartials([]);
      setFinalText("");
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
      const socket = new WebSocket(`${getWsBase()}/asr/stream/${streamSession.session_id}`);
      socketRef.current = socket;
      socket.onmessage = (event) => {
        const payload = JSON.parse(event.data) as { type: string; text?: string };
        if (payload.type === "partial_transcript" && payload.text) {
          setPartials((current) => [...current.slice(-4), payload.text as string]);
          setLatencyLabel("partial");
        }
        if (payload.type === "final_transcript" && payload.text) {
          setFinalText(payload.text);
          setLatencyLabel("final");
        }
      };
      socket.onerror = () => setError("WebSocket stream failed");
      socket.onopen = async () => {
        const userMedia = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRef.current = userMedia;
        const context = new AudioContext({ sampleRate: 16000 });
        contextRef.current = context;
        const source = context.createMediaStreamSource(userMedia);
        const processor = context.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;
        processor.onaudioprocess = (evt) => {
          sequenceRef.current += 1;
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
      };
    } catch (err) {
      setError((err as Error).message);
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
  }

  return { connected, sessionId, partials, finalText, latencyLabel, error, start, stop };
}
