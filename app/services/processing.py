from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Document, ProcessingStatus
from app.services.audit import (
    log_processing_completed,
    log_processing_failed,
    log_processing_started,
)
from app.services.embeddings import embed_chunks, store_vectors
from app.services.parsing import chunk_text, parse_document


def process_document(document_id: uuid.UUID, payload: bytes) -> None:
    db: Session = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if document is None:
            return

        document.processing_status = ProcessingStatus.processing
        db.commit()
        log_processing_started(str(document_id))

        normalized = parse_document(document.file_type, payload)
        chunks = chunk_text(normalized)
        vectors = embed_chunks(chunks)
        store_vectors(
            document_id=document.id,
            user_id=document.uploaded_by,
            file_name=document.original_name,
            vectors=vectors,
            chunks=chunks,
        )

        document.processing_status = ProcessingStatus.completed
        document.vectorized = bool(vectors)
        db.commit()
        log_processing_completed(str(document_id), len(chunks))
    except Exception as exc:  # noqa: BLE001
        document = db.get(Document, document_id)
        if document is not None:
            document.processing_status = ProcessingStatus.failed
            db.commit()
        log_processing_failed(str(document_id), str(exc))
    finally:
        db.close()
