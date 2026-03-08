import { formatMs } from "../../lib/format";

type TranscriptSegment = { start_ms?: number; end_ms?: number; text?: string };

export function TranscriptPane({
  partials,
  finalText,
  finalSegments,
}: {
  partials: string[];
  finalText: string;
  finalSegments: TranscriptSegment[];
}) {
  return (
    <div className="transcript-pane">
      <div>
        <span className="label">Partials</span>
        {partials.length ? partials.map((line, index) => <p key={`${index}-${line}`}>{line}</p>) : <p className="muted">No partial transcript yet.</p>}
      </div>
      <div>
        <span className="label">Final</span>
        <p>{finalText || "Waiting for final transcript."}</p>
        {finalSegments.length ? (
          <div className="segment-list">
            {finalSegments.map((segment, index) => (
              <p key={`${index}-${segment.start_ms ?? 0}-${segment.text ?? ""}`}>
                <span className="muted">{formatMs(segment.start_ms ?? 0)} to {formatMs(segment.end_ms ?? 0)}</span>
                {" "}
                {segment.text}
              </p>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  );
}
