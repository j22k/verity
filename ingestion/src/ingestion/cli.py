
import typer
from pathlib import Path

from ingestion.config import load_blob_settings
from ingestion.blobstore.factory import create_blobstore
from ingestion.parsers.pipeline import (
    extract_and_store,
    load_document_from_blobstore,
)
from ingestion.chunking import chunk_document

app = typer.Typer(
    name="ingestion",
    help="Document ingestion CLI",
    no_args_is_help=True
)


@app.callback()
def initialize(ctx: typer.Context):
    """
    Initialize dependencies when the CLI starts.
    """
    settings = load_blob_settings()
    blobstore = create_blobstore(settings)

    # Store the object in Typer's context
    ctx.obj = {
        "blobstore": blobstore
    }


@app.command()
def process(
    ctx: typer.Context,
    file_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    preview: bool = typer.Option(
        False,
        "--preview",
        help="Display extracted chunks"
    )
):
    try:
        # Retrieve the initialized blobstore
        blobstore = ctx.obj["blobstore"]

        typer.echo(f"Processing file: {file_path}")

        # 1. Extract document and persist it
        typer.echo("Extracting document...")

        document_key = extract_and_store(
            file_path=file_path,
            blobstore=blobstore
        )

        typer.echo(f"Document stored: {document_key}")

        # 2. Retrieve the DoclingDocument object
        document = load_document_from_blobstore(
            key=document_key,
            blobstore=blobstore
        )

        typer.echo(
            f"Extracted document: {document.name} "
            f"(version: {document.version})"
        )

        # 3. Generate chunks
        typer.echo("Generating chunks...")

        result = chunk_document(
            document=document,
            source_path=file_path
        )

        typer.echo("Chunking completed successfully.")
        typer.echo(f"Document: {result.document.filename}")
        typer.echo(f"Pages: {result.document.page_count}")
        typer.echo(f"Generated chunks: {len(result.chunks)}")

        # 4. Preview chunks
        if preview:
            for index, chunk in enumerate(result.chunks, start=1):
                typer.echo(f"\n{'=' * 50}")
                typer.echo(f"Chunk {index}")
                typer.echo(
                    f"Headings: {' > '.join(chunk.metadata.headings)}"
                )
                typer.echo(chunk.text)

        typer.echo("\nIngestion completed successfully.")

    except Exception as e:
        typer.echo(f"Error during ingestion: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
