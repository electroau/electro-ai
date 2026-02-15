import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint_shape():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get('/health')
    assert response.status_code == 200
    body = response.json()
    assert {"status", "postgres", "redis", "qdrant"}.issubset(body.keys())
