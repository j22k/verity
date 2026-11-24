from pathlib import Path
from .base import BlobStore


class LocalBlobStore(BlobStore):

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes) -> str:

        file_path = self.root / key

        # Create nested directories if necessary
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("wb") as f:
            f.write(data)

        return key

    def get(self, key: str) -> bytes:

        file_path = self.root / key

        if not file_path.exists():
            raise FileNotFoundError(f"Blob '{key}' does not exist")

        return file_path.read_bytes()

    def delete(self, key: str) -> None:

        file_path = self.root / key

        if not file_path.exists():
            raise FileNotFoundError(f"Blob '{key}' does not exist")

        file_path.unlink()

    def exists(self, key: str) -> bool:

        return (self.root / key).is_file()