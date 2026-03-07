from __future__ import annotations

import json

from fastapi import APIRouter, File, Form, Header, HTTPException, Request, UploadFile

from ..schemas.requests import ASRFileRequest

router = APIRouter(tags=["transcribe"])


@router.post("/internal/transcribe")
async def transcribe(
    request: Request,
    file: UploadFile | None = File(default=None),
    model: str = Form(default="auto"),
    task: str = Form(default="transcribe"),
    language: str = Form(default="auto"),
    timestamps: bool = Form(default=True),
    diarization: bool = Form(default=False),
    response_format: str = Form(default="json"),
    storage_mode: str = Form(default="persist"),
    metadata: str = Form(default="{}"),
    x_request_id: str = Header(alias="X-Request-Id"),
    x_session_id: str = Header(alias="X-Session-Id"),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    if file is None:
        raise HTTPException(status_code=400, detail="Multipart file upload is required for ASR transcribe")
    payload = await file.read()
    file_request = ASRFileRequest(
        request_id=x_request_id,
        session_id=x_session_id,
        tenant_id=x_tenant_id,
        model=model,
        task=task,
        language=language,
        timestamps=timestamps,
        diarization=diarization,
        response_format=response_format,
        storage_mode=storage_mode,
        metadata=json.loads(metadata) if metadata else {},
    )
    result = await request.app.state.transcription_service.transcribe(file_request, payload, format_hint=file.filename.split(".")[-1] if file.filename and "." in file.filename else None)
    return result.model_dump()
