"""Command-line entry point: `uv run ingestion --help`.

Ingestion has no HTTP API. Work arrives as jobs; the CLI enqueues them and runs the worker.
"""

import typer

from ingestion import __version__

app = typer.Typer(help="Verity ingestion service", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Verity ingestion service."""


@app.command()
def version() -> None:
    """Print the service version."""
    typer.echo(__version__)
