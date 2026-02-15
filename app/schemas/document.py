import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.document import ProcessingStatus


class DocumentResponse(BaseModel):
    id: uuid.UUID
    original_name: str
    file_type: str
    file_size: int
    uploaded_by: uuid.UUID
    uploaded_at: datetime
    processing_status: ProcessingStatus
    vectorized: bool

    class Config:
        from_attributes = True
