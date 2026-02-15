from datetime import datetime
from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: int
    actor_email: str
    action: str
    resource: str
    metadata: dict
    created_at: datetime

    class Config:
        from_attributes = True
