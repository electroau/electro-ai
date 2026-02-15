from qdrant_client import AsyncQdrantClient

from app.core.config import get_settings

settings = get_settings()
client = AsyncQdrantClient(url=settings.qdrant_url)


async def health() -> bool:
    try:
        await client.get_collections()
        return True
    except Exception:
        return False
