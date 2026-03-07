from __future__ import annotations

from fastapi import UploadFile


async def read_upload(upload: UploadFile | None) -> tuple[bytes | None, str | None, str | None]:
    if upload is None:
        return None, None, None
    payload = await upload.read()
    return payload, upload.filename, upload.content_type
