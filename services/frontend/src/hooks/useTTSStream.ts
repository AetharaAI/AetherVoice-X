import { useEffect, useRef, useState } from "react";

import { resolveWsUrl } from "../api/client";
import { startTTSStream } from "../api/tts";

function b64ToBytes(payload: string) {
  const binary = atob(payload);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

type ConnectOptions = {
  model: string;
  voice: string;
  sampleRate: number;
  format: string;
  contextMode: string;
  metadata?: Record<string, unknown>;
};

export function useTTSStream() {
  const [connected, setConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [chunkCount, setChunkCount] = useState(0);
  const [lastSentChars, setLastSentChars] = useState(0);
  const [finalUrl, setFinalUrl] = useState<string | null>(null);
  const [events, setEvents] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [connectionLabel, setConnectionLabel] = useState("idle");
  const [wsUrl, setWsUrl] = useState<string | null>(null);
  const [modelUsed, setModelUsed] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const nextPlaybackTimeRef = useRef(0);
  const chunkCountRef = useRef(0);
  const finalUrlRef = useRef<string | null>(null);
  const phaseRef = useRef("idle");

  function appendEvent(message: string) {
    setEvents((current) => [...current.slice(-7), message]);
  }

  function setPhase(phase: string) {
    phaseRef.current = phase;
    setConnectionLabel(phase);
  }

  function revokeFinalUrl() {
    if (finalUrlRef.current) {
      URL.revokeObjectURL(finalUrlRef.current);
      finalUrlRef.current = null;
    }
  }

  async function ensureAudioContext(): Promise<AudioContext | null> {
    if (typeof window === "undefined") {
      return null;
    }
    const Context = window.AudioContext || (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Context) {
      return null;
    }
    if (!audioContextRef.current) {
      audioContextRef.current = new Context();
    }
    if (audioContextRef.current.state === "suspended") {
      await audioContextRef.current.resume();
    }
    return audioContextRef.current;
  }

  async function playChunkAudio(payload: string) {
    const context = await ensureAudioContext();
    if (!context) {
      return;
    }
    const bytes = b64ToBytes(payload);
    const chunkBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const decoded = await context.decodeAudioData(chunkBuffer.slice(0));
    const source = context.createBufferSource();
    source.buffer = decoded;
    source.connect(context.destination);
    const now = context.currentTime + 0.03;
    const startAt = Math.max(now, nextPlaybackTimeRef.current);
    source.start(startAt);
    nextPlaybackTimeRef.current = startAt + decoded.duration;
  }

  function resetForNewSession() {
    revokeFinalUrl();
    chunkCountRef.current = 0;
    nextPlaybackTimeRef.current = 0;
    setConnected(false);
    setSessionId(null);
    setChunkCount(0);
    setLastSentChars(0);
    setFinalUrl(null);
    setEvents([]);
    setWsUrl(null);
    setModelUsed(null);
    setPhase("idle");
  }

  function closeSocket(force = false) {
    if (!socketRef.current) {
      return;
    }
    const socket = socketRef.current;
    socketRef.current = null;
    socket.onopen = null;
    socket.onmessage = null;
    socket.onerror = null;
    socket.onclose = null;
    if (force && socket.readyState < WebSocket.CLOSING) {
      socket.close();
    }
  }

  useEffect(
    () => () => {
      closeSocket(true);
      revokeFinalUrl();
      if (audioContextRef.current) {
        void audioContextRef.current.close();
        audioContextRef.current = null;
      }
    },
    []
  );

  async function connect(options: ConnectOptions) {
    try {
      closeSocket(true);
      setError(null);
      resetForNewSession();
      setPhase("starting");
      await ensureAudioContext();
      const session = await startTTSStream({
        model: options.model,
        voice: options.voice,
        sample_rate: options.sampleRate,
        format: options.format,
        context_mode: options.contextMode,
        metadata: options.metadata ?? { source: "console" }
      });
      setSessionId(session.session_id);
      setModelUsed(options.model);
      setWsUrl(session.ws_url);
      appendEvent(`stream started · ${session.session_id}`);
      setPhase("opening-socket");
      const socket = new WebSocket(resolveWsUrl(session.ws_url));
      socketRef.current = socket;
      socket.onopen = () => {
        setConnected(true);
        setPhase("open");
        appendEvent("websocket open");
      };
      socket.onerror = () => {
        setError("WebSocket stream failed.");
        setConnected(false);
        setPhase("socket-error");
        appendEvent("websocket error");
      };
      socket.onmessage = (message) => {
        const payload = JSON.parse(message.data) as {
          type: string;
          audio_b64?: string;
          metadata?: Record<string, string>;
          format?: string;
          message?: string;
        };
        if (payload.type === "error") {
          const detail = payload.message || "TTS stream failed during generation.";
          setError(detail);
          setConnected(false);
          setPhase("generation-error");
          appendEvent(`generation failed · ${detail}`);
          socket.close();
          return;
        }
        if (payload.type === "audio_chunk") {
          chunkCountRef.current += 1;
          setChunkCount(chunkCountRef.current);
          setPhase("streaming-audio");
          appendEvent(`audio chunk ${chunkCountRef.current}`);
          if (payload.audio_b64) {
            void playChunkAudio(payload.audio_b64);
          }
        }
        if (payload.type === "final_audio" && payload.audio_b64) {
          const bytes = b64ToBytes(payload.audio_b64);
          revokeFinalUrl();
          const mimeType = payload.format ? `audio/${payload.format}` : "audio/wav";
          const url = URL.createObjectURL(new Blob([bytes], { type: mimeType }));
          finalUrlRef.current = url;
          setFinalUrl(url);
          setConnected(false);
          setPhase("final");
          appendEvent(payload.metadata?.audio_url ? `final audio ready · ${payload.metadata.audio_url}` : "final audio ready");
          socket.close();
        }
      };
      socket.onclose = () => {
        socketRef.current = null;
        setConnected(false);
        if (phaseRef.current !== "final" && phaseRef.current !== "socket-error") {
          setPhase("closed");
          appendEvent("websocket closed");
        }
      };
    } catch (err) {
      setError((err as Error).message);
      setPhase("error");
    }
  }

  function send(text: string) {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      setError("Stream is not open.");
      return;
    }
    setError(null);
    setLastSentChars(text.length);
    setPhase("generating");
    void ensureAudioContext();
    socketRef.current.send(JSON.stringify({ type: "text_chunk", text }));
    appendEvent(`text chunk sent · ${text.length} chars`);
  }

  function stop() {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: "end_stream" }));
      setPhase("finalizing");
      appendEvent("end requested");
      return;
    }
    closeSocket(true);
    setConnected(false);
    setPhase("idle");
  }

  return { connected, connectionLabel, sessionId, wsUrl, modelUsed, chunkCount, lastSentChars, finalUrl, events, error, connect, send, stop };
}
