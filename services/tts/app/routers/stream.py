from __future__ import annotations

import json
from contextlib import suppress

from fastapi import APIRouter, Header, Request, WebSocket, WebSocketDisconnect

from ..pipeline.audio_encode import audio_to_b64
from ..schemas.requests import TTSStreamStartRequest

router = APIRouter(tags=["stream"])


@router.post("/internal/stream/start")
async def start_stream(
    payload: dict,
    request: Request,
    x_request_id: str = Header(alias="X-Request-Id"),
    x_session_id: str = Header(alias="X-Session-Id"),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    stream_request = TTSStreamStartRequest(
        request_id=x_request_id,
        session_id=x_session_id,
        tenant_id=x_tenant_id,
        **payload,
    )
    return await request.app.state.streaming_service.start(stream_request)


@router.websocket("/internal/stream/{session_id}")
async def websocket_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            payload = json.loads(message)
            if payload["type"] == "text_chunk":
                events = await websocket.app.state.streaming_service.push(session_id, payload["text"])
                for event in events:
                    await websocket.send_json(event)
            elif payload["type"] == "end_stream":
                result, audio_bytes = await websocket.app.state.streaming_service.finish(session_id)
                await websocket.send_json(
                    {
                        "type": "final_audio",
                        "session_id": session_id,
                        "audio_b64": audio_to_b64(audio_bytes),
                        "format": result.artifacts.get("format", "wav"),
                        "metadata": {
                            "audio_url": result.audio_url,
                            "runtime": result.artifacts.get("runtime"),
                            "live_chunk_source_route": result.artifacts.get("live_chunk_source_route"),
                            "final_artifact_source_route": result.artifacts.get("final_artifact_source_route"),
                            "fallback_route_used": result.artifacts.get("fallback_route_used"),
                        },
                    }
                )
                break
    except WebSocketDisconnect:
        return
    except Exception as exc:
        with suppress(Exception):
            await websocket.send_json({"type": "error", "session_id": session_id, "message": str(exc)})
            await websocket.close(code=1011)
