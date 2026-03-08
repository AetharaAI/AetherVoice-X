const apiBase = (() => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL as string;
  }
  return `${window.location.origin}/api`;
})();

const wsBase = (() => {
  if (import.meta.env.VITE_WS_BASE_URL) {
    return (import.meta.env.VITE_WS_BASE_URL as string).replace(/\/$/, "");
  }
  const url = new URL(window.location.origin);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  return url.toString().replace(/\/$/, "");
})();

export function getApiBase(): string {
  return apiBase;
}

export function getWsBase(): string {
  return wsBase;
}

export function resolveWsUrl(path: string): string {
  if (/^wss?:\/\//.test(path)) {
    return path;
  }
  const url = new URL(wsBase);
  url.pathname = path.startsWith("/") ? path : `/${path}`;
  url.search = "";
  url.hash = "";
  return url.toString();
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, init);
  if (!response.ok) {
    throw new Error(await response.text());
  }
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    return (await response.json()) as T;
  }
  return (await response.text()) as T;
}
