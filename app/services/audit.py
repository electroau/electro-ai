import logging

logger = logging.getLogger('electro_ai.audit')


def log_upload_event(document_id: str, user_id: str, filename: str) -> None:
    logger.info('upload document_id=%s user_id=%s filename=%s', document_id, user_id, filename)


def log_processing_started(document_id: str) -> None:
    logger.info('processing_started document_id=%s', document_id)


def log_processing_completed(document_id: str, chunks: int) -> None:
    logger.info('processing_completed document_id=%s chunks=%s', document_id, chunks)


def log_processing_failed(document_id: str, error: str) -> None:
    logger.error('processing_failed document_id=%s error=%s', document_id, error)
