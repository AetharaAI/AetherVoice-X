export function MetricBars({ values }: { values: Array<{ label: string; value: number }> }) {
  return (
    <div className="metric-bars">
      {values.map((item) => (
        <div key={item.label}>
          <span>{item.label}</span>
          <div className="metric-track">
            <div className="metric-fill" style={{ width: `${Math.min(item.value, 100)}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}
