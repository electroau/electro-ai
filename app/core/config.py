from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Electro AI Document Intelligence'
    database_url: str = Field(default='postgresql+psycopg2://postgres:postgres@postgres:5432/electro_ai')
    qdrant_url: str = Field(default='http://qdrant:6333')
    qdrant_collection: str = Field(default='document_embeddings')
    openai_api_key: str = Field(default='')
    openai_embedding_model: str = Field(default='text-embedding-3-small')
    upload_root: Path = Field(default=Path('data/uploads'))
    max_upload_size_mb: int = Field(default=50)


@lru_cache
def get_settings() -> Settings:
    return Settings()
