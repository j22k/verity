"""Shared data models (Pydantic).

TODO (milestone 3): define Block, Chunk and the job payload models here.
Parsers return list[Block]; every later stage works only with these models.
"""
from dataclasses import dataclass, field
from typing import Any
# ---------------------------------------------------------
# 1. Document-level metadata
# ---------------------------------------------------------

@dataclass
class DocumentMetadata:
    document_id: str | None
    filename: str
    source_path: str | None
    source_uri: str | None
    mimetype: str | None
    page_count: int
    schema_name: str | None
    docling_version: str | None

# ---------------------------------------------------------
# 2. Chunk-level metadata
# ---------------------------------------------------------

@dataclass
class ChunkMetadata:
    chunk_index: int

    headings: list[str] = field(default_factory=list)
    captions: list[str] = field(default_factory=list)

    page_numbers: list[int] = field(default_factory=list)

    item_types: list[str] = field(default_factory=list)
    item_refs: list[str] = field(default_factory=list)

    # Each entry contains the page number and bounding box
    # associated with an extracted document element.
    provenance: list[dict[str, Any]] = field(default_factory=list)

# ---------------------------------------------------------
# 3. Our application-level chunk representation
# ---------------------------------------------------------

@dataclass
class DocumentChunk:
    text: str
    raw_text: str
    token_count: int
    metadata: ChunkMetadata


# ---------------------------------------------------------
# 4. Complete chunking result
# ---------------------------------------------------------

@dataclass
class ChunkingResult:
    document: DocumentMetadata
    chunks: list[DocumentChunk]

