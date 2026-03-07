import { useEffect, useRef, useState } from "react";

import { getWsBase } from "../api/client";
import { startTTSStream } from "../api/tts";

function b64ToBytes(payload: string) {
  const binary = atob(payload);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

export function useTTSStream() {
  const [connected, setConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [chunkCount, setChunkCount] = useState(0);
  const [finalUrl, setFinalUrl] = useState<string | null>(null);
  const [events, setEvents] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => () => void stop(), []);

  async function connect(model = "moss_realtime") {
    try {
      setError(null);
      setChunkCount(0);
      setFinalUrl(null);
      setEvents([]);
      const session = await startTTSStream({
        model,
        voice: "default",
        sample_rate: 24000,
        format: "wav",
        context_mode: "conversation",
        metadata: { source: "console" }
      });
      setSessionId(session.session_id);
      const socket = new WebSocket(`${getWsBase()}/tts/stream/${session.session_id}`);
      socketRef.current = socket;
      socket.onopen = () => setConnected(true);
      socket.onerror = () => setError("WebSocket stream failed");
      socket.onmessage = (message) => {
        const payload = JSON.parse(message.data) as { type: string; audio_b64?: string; metadata?: Record<string, string> };
        if (payload.type === "audio_chunk") {
          setChunkCount((value) => value + 1);
          setEvents((current) => [...current.slice(-5), `chunk ${chunkCount + 1}`]);
        }
        if (payload.type === "final_audio" && payload.audio_b64) {
          const bytes = b64ToBytes(payload.audio_b64);
          const url = URL.createObjectURL(new Blob([bytes], { type: "audio/wav" }));
          setFinalUrl(url);
          setEvents((current) => [...current.slice(-5), "final audio"]);
        }
      };
    } catch (err) {
      setError((err as Error).message);
    }
  }

  function send(text: string) {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      return;
    }
    socketRef.current.send(JSON.stringify({ type: "text_chunk", text }));
  }

  function stop() {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: "end_stream" }));
      socketRef.current.close();
    }
    setSessionId(null);
    setConnected(false);
  }

  return { connected, sessionId, chunkCount, finalUrl, events, error, connect, send, stop };
}
