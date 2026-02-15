from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import engine
from app.services.vector_store import health as qdrant_health

settings = get_settings()
redis = Redis.from_url(settings.redis_url)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await redis.aclose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
async def health() -> dict:
    postgres_ok = True
    redis_ok = True

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        postgres_ok = False

    try:
        await redis.ping()
    except Exception:
        redis_ok = False

    return {
        "status": "ok" if all([postgres_ok, redis_ok]) else "degraded",
        "postgres": postgres_ok,
        "redis": redis_ok,
        "qdrant": await qdrant_health(),
    }
