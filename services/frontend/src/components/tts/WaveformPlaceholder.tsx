export function WaveformPlaceholder({ chunks }: { chunks: number }) {
  return (
    <div className="waveform">
      {Array.from({ length: 20 }).map((_, index) => (
        <span key={index} style={{ height: `${20 + ((index + chunks) % 7) * 12}px` }} />
      ))}
    </div>
  );
}
