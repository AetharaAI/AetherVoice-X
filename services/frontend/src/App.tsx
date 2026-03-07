import { Navigate, Route, Routes } from "react-router-dom";

import { ShellLayout } from "./components/layout/ShellLayout";
import { ASRFile } from "./pages/ASRFile";
import { ASRLive } from "./pages/ASRLive";
import { Dashboard } from "./pages/Dashboard";
import { Metrics } from "./pages/Metrics";
import { Models } from "./pages/Models";
import { Sessions } from "./pages/Sessions";
import { Triage } from "./pages/Triage";
import { TTSFile } from "./pages/TTSFile";
import { TTSLive } from "./pages/TTSLive";

export default function App() {
  return (
    <Routes>
      <Route element={<ShellLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/asr-live" element={<ASRLive />} />
        <Route path="/asr-file" element={<ASRFile />} />
        <Route path="/tts-live" element={<TTSLive />} />
        <Route path="/tts-file" element={<TTSFile />} />
        <Route path="/triage" element={<Triage />} />
        <Route path="/sessions" element={<Sessions />} />
        <Route path="/models" element={<Models />} />
        <Route path="/metrics" element={<Metrics />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
