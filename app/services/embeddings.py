from __future__ import annotations

import uuid

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.config import get_settings

settings = get_settings()


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    if not settings.openai_api_key:
        raise RuntimeError('OPENAI_API_KEY is not configured')
    client = OpenAI(api_key=settings.openai_api_key)
    vectors: list[list[float]] = []
    for chunk in chunks:
        response = client.embeddings.create(model=settings.openai_embedding_model, input=chunk)
        vectors.append(response.data[0].embedding)
    return vectors


def store_vectors(document_id: uuid.UUID, user_id: uuid.UUID, file_name: str, vectors: list[list[float]], chunks: list[str]) -> None:
    if not vectors:
        return

    client = QdrantClient(url=settings.qdrant_url)
    _ensure_collection(client, len(vectors[0]))

    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                'document_id': str(document_id),
                'user_id': str(user_id),
                'file_name': file_name,
                'chunk': chunk,
            },
        )
        for vector, chunk in zip(vectors, chunks, strict=True)
    ]
    client.upsert(collection_name=settings.qdrant_collection, points=points)


def _ensure_collection(client: QdrantClient, vector_size: int) -> None:
    try:
        client.get_collection(settings.qdrant_collection)
    except UnexpectedResponse:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
