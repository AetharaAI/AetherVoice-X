import { useMemo, useState } from "react";

import { formatMs } from "../../lib/format";

type TranscriptSegment = { start_ms?: number; end_ms?: number; text?: string };

export function TranscriptPane({
  partialText,
  partialEventCount,
  finalText,
  finalSegments,
}: {
  partialText: string;
  partialEventCount: number;
  finalText: string;
  finalSegments: TranscriptSegment[];
}) {
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "error">("idle");
  const transcriptText = useMemo(() => finalText || partialText, [finalText, partialText]);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(transcriptText);
      setCopyStatus("copied");
      window.setTimeout(() => setCopyStatus("idle"), 1500);
    } catch {
      setCopyStatus("error");
      window.setTimeout(() => setCopyStatus("idle"), 1500);
    }
  }

  function handleDownload() {
    const lines = [
      "Aether Voice Realtime Transcript",
      "",
      finalText ? "Status: final" : "Status: partial",
      `Partial updates: ${partialEventCount}`,
      "",
      transcriptText || "No transcript captured.",
    ];
    if (finalSegments.length) {
      lines.push("", "Segments", "");
      finalSegments.forEach((segment) => {
        lines.push(`${formatMs(segment.start_ms ?? 0)} to ${formatMs(segment.end_ms ?? 0)}  ${segment.text ?? ""}`);
      });
    }
    const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `asr-live-${finalText ? "final" : "partial"}.txt`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="transcript-pane">
      <div className="detail-card">
        <div className="detail-card-header">
          <div>
            <span className="label">Realtime transcript</span>
            <p className="muted">{finalText ? "Final transcript captured." : "Live transcript updates in place as Voxtral refines the current utterance."}</p>
          </div>
          <div className="transcript-actions">
            <button type="button" className="secondary compact-button" onClick={handleCopy} disabled={!transcriptText}>
              {copyStatus === "copied" ? "Copied" : copyStatus === "error" ? "Copy failed" : "Quick copy"}
            </button>
            <button type="button" className="secondary compact-button" onClick={handleDownload} disabled={!transcriptText}>
              Download
            </button>
          </div>
        </div>
        <div className="transcript-document">
          {transcriptText ? (
            <p>{transcriptText}</p>
          ) : (
            <p className="muted">No partial transcript yet.</p>
          )}
        </div>
        <div className="transcript-footer">
          <span className="label">Partial updates</span>
          <strong>{partialEventCount}</strong>
          <span className="label">State</span>
          <strong>{finalText ? "final" : "live"}</strong>
        </div>
      </div>
      <div className="detail-card">
        <span className="label">Final segments</span>
        <p>{finalText ? "Timestamped final output from the realtime lane." : "Waiting for final transcript."}</p>
        {finalSegments.length ? (
          <div className="segment-list">
            {finalSegments.map((segment, index) => (
              <div className="segment-row" key={`${index}-${segment.start_ms ?? 0}-${segment.text ?? ""}`}>
                <span className="muted">{formatMs(segment.start_ms ?? 0)} to {formatMs(segment.end_ms ?? 0)}</span>
                <strong>{segment.text}</strong>
              </div>
            ))}
          </div>
        ) : <p className="muted">No final segments yet.</p>}
      </div>
    </div>
  );
}
