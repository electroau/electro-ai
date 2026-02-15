from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user
from app.ingestion.parsers import parse_excel, parse_pdf
from app.models.user import User
from app.services.audit import log_audit_event
from app.db.session import get_db

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/ingest")
async def ingest_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = parse_pdf(content)
    elif file.filename.endswith((".xlsx", ".xls")):
        text = parse_excel(content)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and Excel files are supported")

    await log_audit_event(db, user.email, "ingest_file", file.filename, {"chars": len(text)})
    return {"filename": file.filename, "characters": len(text)}
