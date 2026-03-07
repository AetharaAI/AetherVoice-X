import { Badge } from "../common/Badge";

export function UrgencyBadge({ classification }: { classification: string }) {
  const tone = classification === "emergency" ? "danger" : classification === "urgent" ? "warn" : classification === "standard" ? "good" : "default";
  return <Badge value={classification} tone={tone} />;
}
