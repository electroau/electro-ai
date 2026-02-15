from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog


async def log_audit_event(db: AsyncSession, actor_email: str, action: str, resource: str, metadata: dict | None = None) -> AuditLog:
    log = AuditLog(actor_email=actor_email, action=action, resource=resource, metadata=metadata or {})
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log
