import logging

from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.models import Document, User  # noqa: F401

settings = get_settings()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name)
app.include_router(documents_router)


@app.on_event('startup')
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}
