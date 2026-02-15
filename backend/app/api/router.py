from fastapi import APIRouter

from app.api.v1 import ai, audit, auth, files

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(files.router)
api_router.include_router(ai.router)
api_router.include_router(audit.router)
