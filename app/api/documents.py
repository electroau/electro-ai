from __future__ import annotations

import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import AuthUser, get_current_user
from app.db.session import get_db
from app.models import Document, ProcessingStatus
from app.schemas.document import DocumentResponse
from app.services.audit import log_upload_event
from app.services.processing import process_document
from app.services.storage import build_storage_path, read_upload_payload, validate_extension

router = APIRouter(prefix='/api/documents', tags=['documents'])


@router.post('/upload', response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Document:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Filename is required')

    file_type = validate_extension(file.filename)
    payload = await read_upload_payload(file)
    target_path, stored_name = build_storage_path(current_user.id, file.filename)
    target_path.write_bytes(payload)

    document = Document(
        original_name=file.filename,
        stored_name=stored_name,
        file_type=file_type,
        file_size=len(payload),
        uploaded_by=current_user.id,
        processing_status=ProcessingStatus.pending,
        vectorized=False,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    log_upload_event(str(document.id), str(current_user.id), document.original_name)
    background_tasks.add_task(process_document, document.id, payload)

    return document


@router.get('', response_model=list[DocumentResponse])
def list_documents(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Document]:
    query = select(Document)
    if current_user.role != 'admin':
        query = query.where(Document.uploaded_by == current_user.id)
    return list(db.scalars(query).all())


@router.get('/{document_id}', response_model=DocumentResponse)
def get_document(
    document_id: uuid.UUID,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    if current_user.role != 'admin' and document.uploaded_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    return document
