import { useState } from "react";

import { transcribeFile } from "../api/asr";
import { Panel } from "../components/common/Panel";
import type { ASRResponse } from "../types/api";

export function ASRFile() {
  const [file, setFile] = useState<File | null>(null);
  const [response, setResponse] = useState<ASRResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    if (!file) {
      return;
    }
    const formData = new FormData();
    formData.set("file", file);
    formData.set("model", "auto");
    formData.set("task", "transcribe");
    formData.set("language", "auto");
    formData.set("timestamps", "true");
    formData.set("storage_mode", "persist");
    formData.set("metadata", JSON.stringify({ source: "upload" }));
    try {
      setError(null);
      setResponse(await transcribeFile(formData));
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="page-grid">
      <Panel title="Batch transcription" eyebrow="ASR File">
        <div className="stack">
          <input type="file" accept="audio/*" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
          <button onClick={onSubmit}>Transcribe</button>
          {error ? <p className="error-text">{error}</p> : null}
          {response ? <pre className="response-box">{JSON.stringify(response, null, 2)}</pre> : null}
        </div>
      </Panel>
    </div>
  );
}
