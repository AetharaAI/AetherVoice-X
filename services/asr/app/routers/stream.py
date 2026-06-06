from __future__ import annotations

import json
from contextlib import suppress

from fastapi import APIRouter, Header, HTTPException, Request, WebSocket, WebSocketDisconnect

from ..logging import logger
from ..schemas.requests import ASRStreamStartRequest, AudioFrame

router = APIRouter(tags=["stream"])


@router.post("/internal/stream/start")
async def start_stream(
    payload: dict,
    request: Request,
    x_request_id: str = Header(alias="X-Request-Id"),
    x_session_id: str = Header(alias="X-Session-Id"),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    stream_request = ASRStreamStartRequest(
        request_id=x_request_id,
        session_id=x_session_id,
        tenant_id=x_tenant_id,
        **payload,
    )
    try:
        return await request.app.state.streaming_service.start(stream_request)
    except RuntimeError as exc:
        logger.error(
            "stream_start_failed",
            extra={
                "request_id": x_request_id,
                "session_id": x_session_id,
                "tenant_id": x_tenant_id,
                "route": "/internal/stream/start",
                "error": str(exc),
            },
        )
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.websocket("/internal/stream/{session_id}")
async def websocket_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    logger.info("stream_websocket_accepted", extra={"session_id": session_id, "route": "/internal/stream"})
    finished = False
    try:
        while True:
            message = await websocket.receive_text()
            payload = json.loads(message)
            if payload["type"] == "audio_frame":
                events = await websocket.app.state.streaming_service.push(session_id, AudioFrame.model_validate(payload))
                for event in events:
                    await websocket.send_json(event)
            elif payload["type"] == "end_stream":
                result = await websocket.app.state.streaming_service.finish(session_id)
                finished = True
                await websocket.send_json(
                    {
                        "type": "final_transcript",
                        "session_id": session_id,
                        "stable": True,
                        "text": result.text,
                        "segments": [segment.model_dump() for segment in result.segments],
                    }
                )
                break
    except WebSocketDisconnect:
        logger.info("stream_websocket_disconnected", extra={"session_id": session_id, "route": "/internal/stream"})
    except Exception as exc:
        # Log and clean up instead of re-raising: a dead socket is not a server
        # fault, and the finally block guarantees the session is torn down so the
        # upstream realtime slot is never leaked.
        logger.error(
            "stream_websocket_failed",
            extra={"session_id": session_id, "route": "/internal/stream", "error": repr(exc)},
        )
    finally:
        if not finished:
            with suppress(Exception):
                await websocket.app.state.streaming_service.abort(session_id)
