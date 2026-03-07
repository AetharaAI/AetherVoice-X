from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from aether_common.postgres import PostgresPool
from redis.asyncio import Redis


class SessionService:
    def __init__(self, db: PostgresPool, redis: Redis) -> None:
        self.db = db
        self.redis = redis

    async def create_session(
        self,
        session_id: str,
        tenant_id: str,
        session_type: str,
        model_requested: str,
        model_used: str,
        metadata: dict[str, Any],
    ) -> None:
        await self.db.execute(
            """
            INSERT INTO voice_sessions (
              id, tenant_id, session_type, model_requested, model_used, status, started_at, metadata
            ) VALUES (
              %(id)s, %(tenant_id)s, %(session_type)s, %(model_requested)s, %(model_used)s, 'active', %(started_at)s, %(metadata)s::jsonb
            )
            """,
            {
                "id": session_id,
                "tenant_id": tenant_id,
                "session_type": session_type,
                "model_requested": model_requested,
                "model_used": model_used,
                "started_at": datetime.now(timezone.utc),
                "metadata": json.dumps(metadata),
            },
        )
        await self.redis.hset(
            f"voice:session:{session_id}:meta",
            mapping={
                "session_id": session_id,
                "tenant_id": tenant_id,
                "type": session_type,
                "model": model_used,
                "status": "active",
                "started_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    async def record_request(
        self,
        request_id: str,
        session_id: str | None,
        request_type: str,
        route: str,
        model_requested: str,
        model_used: str,
        status: str,
        timings: dict[str, int],
        audio_duration_ms: int | None = None,
        fallback_used: bool = False,
        error_message: str | None = None,
    ) -> None:
        await self.db.execute(
            """
            INSERT INTO voice_requests (
              id, session_id, request_type, route, model_requested, model_used, status, audio_duration_ms,
              queue_ms, preprocess_ms, inference_ms, postprocess_ms, total_ms, fallback_used, error_message
            ) VALUES (
              %(id)s, %(session_id)s, %(request_type)s, %(route)s, %(model_requested)s, %(model_used)s,
              %(status)s, %(audio_duration_ms)s, %(queue_ms)s, %(preprocess_ms)s, %(inference_ms)s,
              %(postprocess_ms)s, %(total_ms)s, %(fallback_used)s, %(error_message)s
            )
            """,
            {
                "id": request_id,
                "session_id": session_id,
                "request_type": request_type,
                "route": route,
                "model_requested": model_requested,
                "model_used": model_used,
                "status": status,
                "audio_duration_ms": audio_duration_ms,
                "queue_ms": timings.get("queue_ms", 0),
                "preprocess_ms": timings.get("preprocess_ms", 0),
                "inference_ms": timings.get("inference_ms", 0),
                "postprocess_ms": timings.get("postprocess_ms", 0),
                "total_ms": timings.get("total_ms", 0),
                "fallback_used": fallback_used,
                "error_message": error_message,
            },
        )

    async def save_transcript(self, session_id: str, language_detected: str | None, text: str, segments: list[dict[str, Any]]) -> None:
        await self.db.execute(
            """
            INSERT INTO transcripts (id, session_id, language_detected, text, segments)
            VALUES (%(id)s, %(session_id)s, %(language_detected)s, %(text)s, %(segments)s::jsonb)
            """,
            {
                "id": f"{session_id}-transcript",
                "session_id": session_id,
                "language_detected": language_detected,
                "text": text,
                "segments": json.dumps(segments),
            },
        )
        await self.redis.set(f"voice:session:{session_id}:asr:final", json.dumps({"text": text, "segments": segments}))

    async def save_triage_result(self, session_id: str, result: dict[str, Any], domain: str) -> None:
        await self.db.execute(
            """
            INSERT INTO triage_results (
              id, session_id, domain, classification, priority, analysis, recommended_action, requires_human_review
            ) VALUES (
              %(id)s, %(session_id)s, %(domain)s, %(classification)s, %(priority)s, %(analysis)s, %(recommended_action)s, %(requires_human_review)s
            )
            """,
            {
                "id": result["request_id"],
                "session_id": session_id,
                "domain": domain,
                "classification": result["classification"],
                "priority": result["priority"],
                "analysis": result["analysis"],
                "recommended_action": result["recommended_action"],
                "requires_human_review": result["requires_human_review"],
            },
        )

    async def save_tts_output(self, session_id: str | None, model_used: str, voice: str, text_input: str, output_uri: str, duration_ms: int) -> None:
        await self.db.execute(
            """
            INSERT INTO tts_outputs (id, session_id, model_used, voice, text_input, output_uri, duration_ms)
            VALUES (%(id)s, %(session_id)s, %(model_used)s, %(voice)s, %(text_input)s, %(output_uri)s, %(duration_ms)s)
            """,
            {
                "id": f"tts_{datetime.now(timezone.utc).timestamp()}",
                "session_id": session_id,
                "model_used": model_used,
                "voice": voice,
                "text_input": text_input,
                "output_uri": output_uri,
                "duration_ms": duration_ms,
            },
        )

    async def list_sessions(self, limit: int = 50, status: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        query = """
            SELECT id, tenant_id, session_type, model_requested, model_used, status, started_at, ended_at, metadata
            FROM voice_sessions
        """
        if status:
            query += " WHERE status = %(status)s"
            params["status"] = status
        query += " ORDER BY started_at DESC LIMIT %(limit)s"
        return await self.db.fetch_all(query, params)

    async def get_session_detail(self, session_id: str) -> dict[str, Any] | None:
        session = await self.db.fetch_one(
            """
            SELECT id, tenant_id, session_type, model_requested, model_used, status, started_at, ended_at, metadata
            FROM voice_sessions
            WHERE id = %(id)s
            """,
            {"id": session_id},
        )
        if session is None:
            return None
        requests = await self.db.fetch_all("SELECT * FROM voice_requests WHERE session_id = %(session_id)s ORDER BY created_at DESC", {"session_id": session_id})
        transcripts = await self.db.fetch_all("SELECT * FROM transcripts WHERE session_id = %(session_id)s ORDER BY created_at DESC", {"session_id": session_id})
        triage_results = await self.db.fetch_all("SELECT * FROM triage_results WHERE session_id = %(session_id)s ORDER BY created_at DESC", {"session_id": session_id})
        tts_outputs = await self.db.fetch_all("SELECT * FROM tts_outputs WHERE session_id = %(session_id)s ORDER BY created_at DESC", {"session_id": session_id})
        return {
            "session": session,
            "requests": requests,
            "transcripts": transcripts,
            "triage_results": triage_results,
            "tts_outputs": tts_outputs,
        }

    async def end_session(self, session_id: str) -> None:
        await self.db.execute(
            """
            UPDATE voice_sessions
            SET status = 'ended', ended_at = %(ended_at)s
            WHERE id = %(id)s
            """,
            {"id": session_id, "ended_at": datetime.now(timezone.utc)},
        )
        await self.redis.hset(f"voice:session:{session_id}:meta", mapping={"status": "ended", "ended_at": datetime.now(timezone.utc).isoformat()})
