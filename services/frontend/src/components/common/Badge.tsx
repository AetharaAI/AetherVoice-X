export function Badge({ value, tone = "default" }: { value: string; tone?: "default" | "good" | "warn" | "danger" }) {
  return <span className={`badge ${tone}`}>{value}</span>;
}
