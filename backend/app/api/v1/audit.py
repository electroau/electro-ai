from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import require_role
from app.db.session import get_db
from app.models.audit import AuditLog
from app.models.user import UserRole
from app.schemas.audit import AuditLogOut

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=list[AuditLogOut])
async def get_logs(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role(UserRole.ADMIN)),
) -> list[AuditLogOut]:
    logs = (await db.execute(select(AuditLog).order_by(desc(AuditLog.created_at)).limit(100))).scalars().all()
    return [AuditLogOut.model_validate(item) for item in logs]
