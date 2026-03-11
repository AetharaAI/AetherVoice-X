import { useState } from "react";

const PARAMS = {
  prefillTextLen: {
    label: "Prefill text len",
    current: 6,
    recommended: 25,
    min: 0,
    max: 100,
    description: "Tokens sent silently before your real stream starts. This is your warm-up runway. The model needs ~20-30 tokens to stabilize its voice identity before the user hears anything.",
    impact: "CRITICAL",
    fix: "Increase to 25–40. Send a silent warm-up sentence like 'The system is ready.' — user never hears it, but the model locks onto the voice."
  },
  decodeChunkFrames: {
    label: "Decode chunk frames",
    current: 3,
    recommended: 5,
    min: 1,
    max: 20,
    description: "How many audio frames are decoded per chunk. Too low = choppy. Too high = latency.",
    impact: "MEDIUM",
    fix: "Increase to 5–8 for smoother playback. At 3, you're on the edge of audible seams."
  },
  decodeOverlapFrames: {
    label: "Decode overlap frames",
    current: 0,
    recommended: 2,
    min: 0,
    max: 10,
    description: "Frame overlap between chunks for crossfading. At 0, chunks are hard-cut — that's your 'bad phone signal' artifact.",
    impact: "HIGH",
    fix: "Set to 2–4. This crossfades the chunk boundaries and eliminates the choppy seam sound."
  },
  temperature: {
    label: "Temperature",
    current: 0.8,
    recommended: 0.65,
    min: 0,
    max: 1,
    step: 0.05,
    description: "Controls voice variation randomness. High temp = more expressive but less stable. For realtime, stability matters more.",
    impact: "MEDIUM",
    fix: "Drop to 0.6–0.7. Keeps the voice consistent across the stream without sounding robotic."
  },
  topP: {
    label: "Top p",
    current: 0.6,
    recommended: 0.75,
    min: 0,
    max: 1,
    step: 0.05,
    description: "Nucleus sampling. At 0.6 you're cutting off a lot of the probability mass — can cause sudden voice character shifts.",
    impact: "LOW",
    fix: "Raise to 0.75–0.85 for more natural voice flow."
  },
  topK: {
    label: "Top k",
    current: 30,
    recommended: 50,
    min: 1,
    max: 100,
    description: "Limits token candidates. At 30, the model is quite constrained. Works with temp.",
    impact: "LOW",
    fix: "Increase to 50 if voice sounds flat or clipped."
  },
  repetitionPenalty: {
    label: "Repetition penalty",
    current: 1.1,
    recommended: 1.1,
    min: 1.0,
    max: 2.0,
    step: 0.05,
    description: "Penalizes repeated audio patterns. Current value is good.",
    impact: "OK",
    fix: "Leave at 1.1. This is correctly set."
  },
  repetitionWindow: {
    label: "Repetition window",
    current: 50,
    recommended: 50,
    min: 10,
    max: 200,
    description: "Window size for repetition penalty. Current value is fine.",
    impact: "OK",
    fix: "Leave at 50."
  }
};

const WARMUP_TEMPLATE = `// Silent warm-up payload — send this BEFORE your real stream
// The user never hears this. It conditions the model voice.

const warmUpText = "The system is initialized and ready for your request.";

async function startConditionedStream(sessionId, realText) {
  const ws = new WebSocket(\`wss://your-host/api/v1/tts/stream/\${sessionId}\`);
  
  ws.onopen = () => {
    // Step 1: Send warm-up silently (prefill)
    ws.send(JSON.stringify({
      type: "prefill",
      text: warmUpText,
      suppress_output: true  // Don't send audio to client
    }));
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    
    if (msg.type === "prefill_complete") {
      // Step 2: NOW send real text — voice is warm
      ws.send(JSON.stringify({
        type: "stream",
        text: realText
      }));
    }
    
    if (msg.type === "audio_chunk") {
      // Route to your audio player
      playChunk(msg.data);
    }
  };
}`;

const IMPACT_COLORS = {
  CRITICAL: { bg: "bg-red-900/40", border: "border-red-500", text: "text-red-400", badge: "bg-red-500" },
  HIGH: { bg: "bg-orange-900/40", border: "border-orange-500", text: "text-orange-400", badge: "bg-orange-500" },
  MEDIUM: { bg: "bg-yellow-900/40", border: "border-yellow-600", text: "text-yellow-400", badge: "bg-yellow-600" },
  LOW: { bg: "bg-blue-900/40", border: "border-blue-500", text: "text-blue-400", badge: "bg-blue-500" },
  OK: { bg: "bg-green-900/30", border: "border-green-600", text: "text-green-400", badge: "bg-green-600" }
};

export default function MossRealtimeTuner() {
  const [activeTab, setActiveTab] = useState("params");
  const [values, setValues] = useState(
    Object.fromEntries(Object.entries(PARAMS).map(([k, v]) => [k, v.current]))
  );

  const applyRecommended = () => {
    setValues(Object.fromEntries(Object.entries(PARAMS).map(([k, v]) => [k, v.recommended])));
  };

  const resetCurrent = () => {
    setValues(Object.fromEntries(Object.entries(PARAMS).map(([k, v]) => [k, v.current])));
  };

  const diagnosisScore = () => {
    let issues = 0;
    if (values.prefillTextLen < 20) issues += 3;
    if (values.decodeOverlapFrames < 1) issues += 2;
    if (values.temperature > 0.75) issues += 1;
    if (values.decodeChunkFrames < 4) issues += 1;
    return issues;
  };

  const score = diagnosisScore();
  const health = score === 0 ? "Optimal" : score <= 2 ? "Good" : score <= 4 ? "Degraded" : "Poor";
  const healthColor = score === 0 ? "text-green-400" : score <= 2 ? "text-yellow-400" : score <= 4 ? "text-orange-400" : "text-red-400";

  return (
    <div style={{ fontFamily: "'JetBrains Mono', 'Fira Code', monospace", background: "#0a0d14", minHeight: "100vh", color: "#e2e8f0" }}>
      {/* Header */}
      <div style={{ borderBottom: "1px solid #1e2a3a", padding: "20px 32px", background: "#0d1117" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <div style={{ fontSize: "11px", letterSpacing: "3px", color: "#4a9eff", textTransform: "uppercase", marginBottom: "4px" }}>
              AETHERPRO VOICE — DIAGNOSTIC
            </div>
            <h1 style={{ fontSize: "22px", fontWeight: 700, color: "#fff", margin: 0 }}>
              MOSS Realtime Stream Tuner
            </h1>
            <div style={{ fontSize: "12px", color: "#64748b", marginTop: "4px" }}>
              moss_realtime · Voxtral ASR Live · Session Profile: Telephony
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>STREAM HEALTH</div>
            <div style={{ fontSize: "28px", fontWeight: 700 }} className={healthColor}>{health}</div>
            <div style={{ fontSize: "11px", color: "#64748b" }}>{score} issue{score !== 1 ? "s" : ""} detected</div>
          </div>
        </div>

        {/* Root cause banner */}
        {score > 0 && (
          <div style={{ marginTop: "16px", background: "#1a0a0a", border: "1px solid #7f1d1d", borderRadius: "8px", padding: "12px 16px" }}>
            <div style={{ fontSize: "11px", letterSpacing: "2px", color: "#ef4444", marginBottom: "6px" }}>ROOT CAUSE ANALYSIS</div>
            <div style={{ fontSize: "13px", color: "#fca5a5", lineHeight: 1.6 }}>
              {values.prefillTextLen < 20 && "① Prefill too short — model is cold-starting audibly. "}
              {values.decodeOverlapFrames < 1 && "② Zero overlap frames = hard chunk cuts = 'bad signal' artifact. "}
              {values.temperature > 0.75 && "③ High temp causing voice instability mid-stream. "}
              {values.decodeChunkFrames < 4 && "④ Chunk frames too low, increasing seam frequency. "}
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid #1e2a3a", background: "#0d1117" }}>
        {["params", "warmup", "architecture"].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: "12px 24px",
              fontSize: "12px",
              letterSpacing: "1px",
              textTransform: "uppercase",
              background: "none",
              border: "none",
              cursor: "pointer",
              color: activeTab === tab ? "#4a9eff" : "#64748b",
              borderBottom: activeTab === tab ? "2px solid #4a9eff" : "2px solid transparent",
              fontFamily: "inherit"
            }}
          >
            {tab === "params" ? "Parameter Tuning" : tab === "warmup" ? "Warm-Up Fix" : "Architecture"}
          </button>
        ))}
        <div style={{ marginLeft: "auto", display: "flex", gap: "8px", padding: "8px 24px" }}>
          <button onClick={applyRecommended} style={{ padding: "6px 16px", fontSize: "11px", background: "#4a9eff", color: "#fff", border: "none", borderRadius: "4px", cursor: "pointer", fontFamily: "inherit" }}>
            Apply Recommended
          </button>
          <button onClick={resetCurrent} style={{ padding: "6px 16px", fontSize: "11px", background: "#1e2a3a", color: "#94a3b8", border: "1px solid #2d3748", borderRadius: "4px", cursor: "pointer", fontFamily: "inherit" }}>
            Reset to Current
          </button>
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: "24px 32px" }}>
        {activeTab === "params" && (
          <div style={{ display: "grid", gap: "12px" }}>
            {Object.entries(PARAMS).map(([key, param]) => {
              const colors = IMPACT_COLORS[param.impact];
              const isChanged = values[key] !== param.current;
              const isRecommended = values[key] === param.recommended;
              return (
                <div key={key} style={{ background: "#0d1117", border: `1px solid ${param.impact === "CRITICAL" ? "#7f1d1d" : param.impact === "HIGH" ? "#7c2d12" : "#1e2a3a"}`, borderRadius: "8px", padding: "16px 20px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "10px" }}>
                    <span style={{ fontSize: "13px", fontWeight: 600, color: "#e2e8f0" }}>{param.label}</span>
                    <span style={{ fontSize: "10px", padding: "2px 8px", borderRadius: "3px", background: param.impact === "OK" ? "#14532d" : param.impact === "CRITICAL" ? "#7f1d1d" : "#1e2a3a", color: param.impact === "OK" ? "#4ade80" : param.impact === "CRITICAL" ? "#fca5a5" : param.impact === "HIGH" ? "#fb923c" : param.impact === "MEDIUM" ? "#fbbf24" : "#60a5fa" }}>
                      {param.impact}
                    </span>
                    {isChanged && <span style={{ fontSize: "10px", color: "#4a9eff" }}>● MODIFIED</span>}
                    {isRecommended && !isChanged && <span style={{ fontSize: "10px", color: "#4ade80" }}>✓ OPTIMAL</span>}
                  </div>

                  <div style={{ display: "flex", alignItems: "center", gap: "16px", marginBottom: "10px" }}>
                    <input
                      type="range"
                      min={param.min}
                      max={param.max}
                      step={param.step || 1}
                      value={values[key]}
                      onChange={e => setValues(v => ({ ...v, [key]: parseFloat(e.target.value) }))}
                      style={{ flex: 1, accentColor: "#4a9eff" }}
                    />
                    <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                      <span style={{ fontSize: "11px", color: "#64748b" }}>Current:</span>
                      <span style={{ fontSize: "14px", fontWeight: 700, color: "#e2e8f0", minWidth: "40px" }}>{values[key]}</span>
                      <span style={{ fontSize: "11px", color: "#64748b" }}>→ Rec:</span>
                      <span style={{ fontSize: "14px", fontWeight: 700, color: "#4ade80", minWidth: "40px" }}>{param.recommended}</span>
                    </div>
                  </div>

                  <div style={{ fontSize: "12px", color: "#64748b", lineHeight: 1.6, marginBottom: "8px" }}>{param.description}</div>
                  {param.impact !== "OK" && (
                    <div style={{ fontSize: "12px", color: "#93c5fd", background: "#0f172a", padding: "8px 12px", borderRadius: "4px", borderLeft: "3px solid #4a9eff" }}>
                      💡 {param.fix}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {activeTab === "warmup" && (
          <div>
            <div style={{ background: "#0d1117", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
              <div style={{ fontSize: "11px", letterSpacing: "2px", color: "#4a9eff", marginBottom: "8px" }}>THE CORE FIX — SILENT WARM-UP PREFILL</div>
              <p style={{ fontSize: "13px", color: "#94a3b8", lineHeight: 1.7, margin: "0 0 12px 0" }}>
                MOSS Realtime uses a neural codec that must "find" the target voice before it stabilizes. The first ~20-30 tokens are the model locking onto the conditioning asset (your .wav file). If those tokens play out loud, the user hears the unstable cold-start period. The fix: send a silent warm-up payload first, suppress its audio output, then begin your real stream once the model has its footing.
              </p>
              <div style={{ background: "#030712", border: "1px solid #1e2a3a", borderRadius: "6px", padding: "16px", overflowX: "auto" }}>
                <pre style={{ fontSize: "12px", color: "#a5f3fc", margin: 0, lineHeight: 1.7 }}>{WARMUP_TEMPLATE}</pre>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
              <div style={{ background: "#0d1117", border: "1px solid #14532d", borderRadius: "8px", padding: "16px" }}>
                <div style={{ fontSize: "11px", color: "#4ade80", marginBottom: "8px", letterSpacing: "1px" }}>✓ WHAT'S WORKING</div>
                <ul style={{ fontSize: "12px", color: "#86efac", lineHeight: 1.8, margin: 0, paddingLeft: "16px" }}>
                  <li>Final stream audio — perfect quality</li>
                  <li>Conditioning asset loading (Perfect-Technician-7s.wav)</li>
                  <li>WebSocket session management</li>
                  <li>Play button appearing on final stream</li>
                  <li>Voice preset resolving correctly</li>
                </ul>
              </div>
              <div style={{ background: "#0d1117", border: "1px solid #7f1d1d", borderRadius: "8px", padding: "16px" }}>
                <div style={{ fontSize: "11px", color: "#f87171", marginBottom: "8px", letterSpacing: "1px" }}>✗ WHAT'S BROKEN</div>
                <ul style={{ fontSize: "12px", color: "#fca5a5", lineHeight: 1.8, margin: 0, paddingLeft: "16px" }}>
                  <li>Cold-start voice instability (gender/pitch drift)</li>
                  <li>Chunk boundary artifacts (0 overlap)</li>
                  <li>No warm-up prefill before live stream</li>
                  <li>Prefill len too low to condition voice</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === "architecture" && (
          <div style={{ display: "grid", gap: "12px" }}>
            {[
              { step: "01", title: "Session Init", desc: "Create session with voice preset + conditioning .wav asset. This is already working correctly.", status: "ok" },
              { step: "02", title: "Silent Prefill", desc: "Send 25-40 token warm-up text with suppress_output: true. Model runs inference but audio is discarded. Voice locks onto conditioning.", status: "fix" },
              { step: "03", title: "Prefill Complete Event", desc: "Wait for prefill_complete message from backend before sending real content. This is your gate.", status: "fix" },
              { step: "04", title: "Real Stream Begins", desc: "Now send actual utterance text. Voice is warm, conditioned, stable. Chunks arrive with proper overlap.", status: "ok" },
              { step: "05", title: "Chunk Playback", desc: "Play chunks with crossfade (overlap frames = 2-4). Eliminates seam artifacts at boundaries.", status: "fix" },
              { step: "06", title: "Stream End", desc: "End stream, assemble final WAV, display play button. Already working.", status: "ok" }
            ].map(item => (
              <div key={item.step} style={{ display: "flex", gap: "16px", background: "#0d1117", border: `1px solid ${item.status === "ok" ? "#14532d" : "#7c2d12"}`, borderRadius: "8px", padding: "14px 18px" }}>
                <div style={{ fontSize: "20px", fontWeight: 800, color: item.status === "ok" ? "#4ade80" : "#f97316", minWidth: "32px" }}>{item.step}</div>
                <div>
                  <div style={{ display: "flex", gap: "10px", alignItems: "center", marginBottom: "4px" }}>
                    <span style={{ fontSize: "13px", fontWeight: 600, color: "#e2e8f0" }}>{item.title}</span>
                    <span style={{ fontSize: "10px", padding: "2px 8px", borderRadius: "3px", background: item.status === "ok" ? "#14532d" : "#7c2d12", color: item.status === "ok" ? "#4ade80" : "#fb923c" }}>
                      {item.status === "ok" ? "WORKING" : "NEEDS FIX"}
                    </span>
                  </div>
                  <div style={{ fontSize: "12px", color: "#64748b" }}>{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
