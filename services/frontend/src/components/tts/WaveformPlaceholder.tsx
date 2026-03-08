type WaveformPlaceholderProps = {
  chunks: number;
  active?: boolean;
  tone?: "default" | "good" | "danger";
};

export function WaveformPlaceholder({ chunks, active = false, tone = "default" }: WaveformPlaceholderProps) {
  return (
    <div className={`waveform ${active ? "active" : ""} ${tone}`}>
      {Array.from({ length: 20 }).map((_, index) => (
        <span
          key={index}
          style={{
            height: `${20 + ((index + chunks) % 7) * 12}px`,
            ["--bar-index" as string]: index,
          }}
        />
      ))}
    </div>
  );
}
