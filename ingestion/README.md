# Verity ingestion service

Turns raw files into versioned, permission-tagged, searchable chunks in Postgres + pgvector.

- Queue-driven worker plus a CLI; no HTTP API.
- Pipeline: register, detect, parse, clean, metadata, version, chunk, embed, store and activate.
- Formats: PDF (digital, scanned, mixed), DOCX, Markdown, CSV/XLSX, JSON tickets.

## Quick start

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/), Docker.

```bash
cd ingestion
uv sync
cp .env.example .env
docker compose up -d
uv run ingestion --help
uv run pytest
```

## Project layout

See [CLAUDE.md](CLAUDE.md) for the layout, pipeline stages, rules and conventions that every contributor follows.

## Common commands

| Task | Command |
| --- | --- |
| Install dependencies | `uv sync` |
| Add a dependency | `uv add <package>` (dev: `uv add --dev <package>`) |
| Start Postgres | `docker compose up -d` |
| Stop Postgres | `docker compose down` |
| Run tests | `uv run pytest` |
| Lint and format | `uv run ruff check . && uv run ruff format .` |
