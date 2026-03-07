from __future__ import annotations

import json

from fastapi import APIRouter, Header, Request, WebSocket, WebSocketDisconnect

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
    return await request.app.state.streaming_service.start(stream_request)


@router.websocket("/internal/stream/{session_id}")
async def websocket_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    logger.info("stream_websocket_accepted", extra={"session_id": session_id, "route": "/internal/stream"})
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
        return
    except Exception as exc:
        logger.error(
            "stream_websocket_failed",
            extra={"session_id": session_id, "route": "/internal/stream", "error": repr(exc)},
        )
        raise
