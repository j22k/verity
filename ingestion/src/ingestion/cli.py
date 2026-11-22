import typer
from pathlib import Path

from ingestion.parsers.extraction import extract_document
from ingestion.chunking import chunk_document

app = typer.Typer(
    name="ingestion",
    help="Document ingestion CLI",
    no_args_is_help=True
)


@app.command()
def process(
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
        typer.echo(f"Processing file: {file_path}")
        document = extract_document(file_path)
        typer.echo(f"Extracted document: {document.name} (version: {document.version})")
        typer.echo("Generating chunks...")
        result = chunk_document(
            document=document,
            source_path=file_path
        )
        typer.echo("Chunking completed successfully.")
        typer.echo(f"Document: {result.document.filename}")
        typer.echo(f"Pages: {result.document.page_count}")
        typer.echo(f"Generated chunks: {len(result.chunks)}")

        if preview:
            for index, chunk in enumerate(result.chunks, start=1):
                typer.echo(f"\n{'=' * 50}")
                typer.echo(f"Chunk {index}")
                typer.echo(f"Headings: {' > '.join(chunk.metadata.headings)}")
                typer.echo(chunk.text)

        typer.echo("\nIngestion completed successfully.")
    except Exception as e:
        typer.echo(f"Error during ingestion: {e}", err=True)
        raise typer.Exit(code=1)
    
if __name__ == "__main__":
    app()