from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.openai_service import ask_assistant
from app.auth.deps import get_current_user
from app.models.user import User
from app.services.audit import log_audit_event
from app.db.session import get_db

router = APIRouter(prefix="/ai", tags=["ai"])


class PromptIn(BaseModel):
    prompt: str


@router.post("/chat")
async def chat(payload: PromptIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    answer = await ask_assistant(payload.prompt)
    await log_audit_event(db, user.email, "ai_chat", "assistant", {"prompt_chars": len(payload.prompt)})
    return {"answer": answer}
