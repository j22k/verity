
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument


# Keep one converter instance and reuse it.
# Docling can reuse initialized pipelines across conversions.
_converter = DocumentConverter(
    allowed_formats=[
        InputFormat.PDF,
        InputFormat.DOCX,
        InputFormat.PPTX,
        InputFormat.HTML,
    ]
)


def extract_document(file_path: Path) -> DoclingDocument:
    """
    Convert a supported source file into a structured DoclingDocument.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Expected a file, received: {file_path}")

    result = _converter.convert(file_path)

    document = result.document

    if document is None:
        raise RuntimeError(
            f"Docling could not extract a document from: {file_path}"
        )

    return document
