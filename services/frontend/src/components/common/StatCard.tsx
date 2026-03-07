export function StatCard({ label, value, tone = "default" }: { label: string; value: string; tone?: "default" | "danger" | "good" }) {
  return (
    <div className={`stat-card ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
