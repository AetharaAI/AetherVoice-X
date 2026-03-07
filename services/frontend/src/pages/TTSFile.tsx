import { useState } from "react";

import { synthesizeText } from "../api/tts";
import { Panel } from "../components/common/Panel";
import type { TTSResponse } from "../types/api";

export function TTSFile() {
  const [text, setText] = useState("A technician is being dispatched to your location now.");
  const [response, setResponse] = useState<TTSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    try {
      setError(null);
      setResponse(
        await synthesizeText({
          model: "auto",
          voice: "default",
          text,
          format: "wav",
          sample_rate: 24000,
          stream: false,
          style: { speed: 1, emotion: "calm", speaker_hint: "support_agent" },
          metadata: { source: "console" }
        })
      );
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="page-grid">
      <Panel title="Batch synthesis" eyebrow="TTS File">
        <div className="stack">
          <textarea value={text} onChange={(event) => setText(event.target.value)} rows={7} />
          <button onClick={onSubmit}>Synthesize</button>
          {response ? (
            <div className="stack">
              <p className="muted">Output: {response.audio_url}</p>
              <pre className="response-box">{JSON.stringify(response, null, 2)}</pre>
            </div>
          ) : null}
          {error ? <p className="error-text">{error}</p> : null}
        </div>
      </Panel>
    </div>
  );
}
