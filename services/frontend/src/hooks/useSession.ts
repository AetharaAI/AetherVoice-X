import { useEffect, useState } from "react";

import { fetchSessionDetail } from "../api/sessions";
import type { SessionDetail } from "../types/api";

export function useSession(sessionId?: string) {
  const [detail, setDetail] = useState<SessionDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) {
      setDetail(null);
      return;
    }
    setLoading(true);
    setError(null);
    fetchSessionDetail(sessionId)
      .then(setDetail)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [sessionId]);

  return { detail, loading, error };
}
