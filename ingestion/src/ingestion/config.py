"""Service configuration, read from environment variables or a local .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="INGESTION_", extra="ignore")

    database_url: str = "postgresql://verity:verity@localhost:5432/verity"
    blob_dir: str = "data/blobs"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dim: int = 384
    job_max_attempts: int = 5
    job_visibility_timeout_s: int = 300


def get_settings() -> Settings:
    return Settings()
