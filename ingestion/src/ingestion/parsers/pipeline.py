import json
from pathlib import Path

from docling_core.types.doc import DoclingDocument
from .extraction import extract_document


def extract_and_store(file_path: Path, blobstore) -> str:

    document: DoclingDocument = extract_document(file_path)

    # Serialize
    document_data = document.export_to_dict()
    serialized = json.dumps(document_data).encode("utf-8")

    # Store
    key = f"extracted/{file_path.stem}.json"
    stored_key = blobstore.put(key, serialized)

    return stored_key


def load_document_from_blobstore(
    blobstore,
    key: str
) -> DoclingDocument:

    # Retrieve
    serialized = blobstore.get(key)

    # Deserialize
    document_data = json.loads(serialized.decode("utf-8"))

    # Reconstruct DoclingDocument
    document = DoclingDocument.model_validate(document_data)

    return document