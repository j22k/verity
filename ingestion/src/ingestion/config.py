from dataclasses import dataclass
import  os 
from pathlib import Path

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


@dataclass
class BlobSettings:
    STORAGE_BACKEND: str
    BLOBSTORE_ROOT: Path
    S3_BUCKET: str

def load_blob_settings() -> BlobSettings:
    project_root = Path(__file__).resolve().parents[1]
    return BlobSettings(
        STORAGE_BACKEND=os.environ.get("STORAGE_BACKEND", "local"),
        BLOBSTORE_ROOT=Path(os.environ.get("BLOBSTORE_ROOT", project_root / "data" / "blobs")),
        S3_BUCKET=os.environ.get("S3_BUCKET", "my-s3-bucket")
    )