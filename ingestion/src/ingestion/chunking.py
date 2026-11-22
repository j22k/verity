
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from docling.chunking import HybridChunker
from docling_core.types.doc import DoclingDocument


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


# ---------------------------------------------------------
# 5. Chunker
# ---------------------------------------------------------

_chunker = HybridChunker(merge_peers=True)


def extract_document_metadata(
    document: DoclingDocument,
    source_path: Path | None = None,
) -> DocumentMetadata:

    origin = document.origin

    # Prefer Docling's original filename when available.
    filename = (
        getattr(origin, "filename", None)
        if origin
        else None
    ) or document.name

    return DocumentMetadata(
        document_id=getattr(origin, "binary_hash", None),
        filename=filename,
        source_path=str(source_path) if source_path else None,
        source_uri=str(origin.uri) if origin and origin.uri else None,
        mimetype=getattr(origin, "mimetype", None) if origin else None,
        page_count=document.num_pages(),
        schema_name=document.schema_name,
        docling_version=document.version,
    )


def chunk_document(
    document: DoclingDocument,
    source_path: Path | None = None,
) -> ChunkingResult:

    document_metadata = extract_document_metadata(
        document,
        source_path,
    )

    output: list[DocumentChunk] = []

    for index, chunk in enumerate(_chunker.chunk(document)):

        # Text enriched with heading/caption context.
        contextualized_text = _chunker.contextualize(chunk)

        doc_items = chunk.meta.doc_items

        page_numbers: set[int] = set()
        item_types: set[str] = set()
        item_refs: list[str] = []
        provenance: list[dict[str, Any]] = []

        for item in doc_items:

            # Identify the type of document element.
            label = item.label
            item_types.add(
                label.value if hasattr(label, "value") else str(label)
            )

            # Reference to the original DoclingDocument element.
            item_refs.append(item.self_ref)

            # Extract source location information.
            for prov in item.prov:
                page_numbers.add(prov.page_no)

                provenance.append(
                    {
                        "page_no": prov.page_no,
                        "bbox": prov.bbox.model_dump(mode="json"),
                        "charspan": list(prov.charspan),
                    }
                )

        metadata = ChunkMetadata(
            chunk_index=index,
            headings=list(chunk.meta.headings or []),
            captions=list(chunk.meta.captions or []),
            page_numbers=sorted(page_numbers),
            item_types=sorted(item_types),
            item_refs=item_refs,
            provenance=provenance,
        )

        output.append(
            DocumentChunk(
                text=contextualized_text,
                raw_text=chunk.text,
                token_count=_chunker.tokenizer.count_tokens(
                    contextualized_text
                ),
                metadata=metadata,
            )
        )

    return ChunkingResult(
        document=document_metadata,
        chunks=output,
    )
