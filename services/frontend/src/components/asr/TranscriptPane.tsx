export function TranscriptPane({ partials, finalText }: { partials: string[]; finalText: string }) {
  return (
    <div className="transcript-pane">
      <div>
        <span className="label">Partials</span>
        {partials.length ? partials.map((line, index) => <p key={`${index}-${line}`}>{line}</p>) : <p className="muted">No partial transcript yet.</p>}
      </div>
      <div>
        <span className="label">Final</span>
        <p>{finalText || "Waiting for final transcript."}</p>
      </div>
    </div>
  );
}
