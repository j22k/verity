import json
from pathlib import Path

from docling_core.types.doc import DoclingDocument
from .extraction import extract_document


def store_original(file_path: Path, blobstore)-> str:
    key = f"original/{file_path.name}"

    stored_key= blobstore.put(key, file_path.read_bytes())

    return stored_key


def extract_and_store(file_path: Path, blobstore) -> str:

    document: DoclingDocument = extract_document(file_path)

    # Serialize
    document_data = document.export_to_dict()
    serialized = json.dumps(document_data).encode("utf-8")

    # Store
    key = f"extracted/{file_path.stem}.json"
    stored_key = blobstore.put(key, serialized)

    return stored_key


def process_and_store(file_path: Path, blobstore) -> str:

    # 1. Store original
    original_key = store_original(file_path, blobstore)

    # 2. Extract and store
    extracted_key = extract_and_store(file_path, blobstore)

    return extracted_key
            



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