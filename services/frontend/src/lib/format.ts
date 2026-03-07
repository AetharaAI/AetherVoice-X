export function formatDateTime(value?: string | null): string {
  if (!value) {
    return "n/a";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
}

export function formatMs(value?: number | null): string {
  if (value === undefined || value === null) {
    return "n/a";
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(2)}s`;
  }
  return `${value}ms`;
}

export function formatCount(value?: number | null): string {
  if (value === undefined || value === null) {
    return "0";
  }
  return Intl.NumberFormat().format(value);
}

export function formatValue(value: unknown): string {
  if (value === null || value === undefined || value === "") {
    return "n/a";
  }
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return JSON.stringify(value);
}

export function canPlayAudio(url?: string | null): boolean {
  if (!url) {
    return false;
  }
  return /^(https?:|blob:)/.test(url);
}
