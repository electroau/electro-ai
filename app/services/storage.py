from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

settings = get_settings()
ALLOWED_EXTENSIONS = {'.xlsx', '.csv', '.pdf'}


def validate_extension(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unsupported file type')
    return suffix.lstrip('.')


async def read_upload_payload(file: UploadFile) -> bytes:
    max_size = settings.max_upload_size_mb * 1024 * 1024
    payload = await file.read(max_size + 1)
    if len(payload) > max_size:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='File exceeds max size of 50MB')
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Empty file')
    return payload


def build_storage_path(user_id: uuid.UUID, filename: str) -> tuple[Path, str]:
    now = datetime.now(timezone.utc)
    extension = Path(filename).suffix.lower()
    stored_name = f'{uuid.uuid4()}{extension}'
    target_dir = settings.upload_root / str(user_id) / str(now.year) / f'{now.month:02d}'
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / stored_name, stored_name
