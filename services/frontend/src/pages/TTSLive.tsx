import { useState } from "react";

import { Panel } from "../components/common/Panel";
import { WaveformPlaceholder } from "../components/tts/WaveformPlaceholder";
import { useTTSStream } from "../hooks/useTTSStream";

export function TTSLive() {
  const { connected, chunkCount, finalUrl, events, error, connect, send, stop } = useTTSStream();
  const [text, setText] = useState("A technician is being dispatched to your location now.");

  return (
    <div className="page-grid">
      <Panel title="Realtime synthesis lane" eyebrow="TTS Live">
        <div className="toolbar">
          <button onClick={() => connect()} disabled={connected}>
            Start stream
          </button>
          <button onClick={() => send(text)} disabled={!connected}>
            Send text
          </button>
          <button onClick={stop} disabled={!connected} className="secondary">
            End stream
          </button>
        </div>
        <textarea value={text} onChange={(event) => setText(event.target.value)} rows={5} />
        <WaveformPlaceholder chunks={chunkCount} />
        <div className="list-table">
          {events.map((event) => (
            <div key={event} className="list-row">
              <span>{event}</span>
            </div>
          ))}
        </div>
        {finalUrl ? <audio controls src={finalUrl} /> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
