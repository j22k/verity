# Verity ingestion service

Turns raw company files (PDF, DOCX, Markdown, CSV/XLSX, JSON tickets) into **versioned, permission-tagged, searchable chunks** in Postgres + pgvector. It is a queue-driven worker plus a CLI. It has **no HTTP API**; the user-facing backend API is a separate service built later. Retrieval, answer generation and auth are out of scope here.

## Commands

Run from this folder (`ingestion/`).

```bash
uv sync                        # install dependencies
docker compose up -d           # Postgres 16 + pgvector on localhost:5432
uv run ingestion --help        # CLI
uv run pytest                  # tests
uv run ruff check . && uv run ruff format .   # lint + format
```

Copy `.env.example` to `.env` for local settings. All settings use the `INGESTION_` prefix (`src/ingestion/config.py`).

## Layout

```
src/ingestion/
  config.py      settings (pydantic-settings)
  models.py      Block, Chunk, job payloads (Pydantic)
  cli.py         typer CLI: enqueue jobs, run the worker
  blobstore/     raw file storage interface (local FS now, S3 later)
  parsers/       one parser per file type: bytes -> list[Block]
  stages/        detect, clean, metadata, chunk, version (small functions)
  embedding/     Embedder interface + implementations
  ocr/           OCR interface + implementations
  db/            connection + repositories, hand-written SQL
  jobs/          Postgres job queue (enqueue, claim, complete, fail, dead-letter)
  worker/        worker loop that runs the pipeline for one job
tests/           pytest; mirrors src layout
migrations/      SQL migrations (Alembic)
corpus/          synthetic test documents (small samples only)
```

## Pipeline

register -> detect type -> parse -> clean -> extract metadata -> version/dedupe -> chunk -> embed -> store + activate.

Parsers return `list[Block]`. Everything after parsing sees only blocks, never file formats. To add a file type, add one parser and register it; do not touch later stages.

## Rules that must not be broken

1. **Idempotent.** Re-ingesting the same content (same document + content hash) creates nothing new. A retried job never duplicates chunks.
2. **Activation is last and atomic.** Chunks and vectors are inserted, then the new version is published and the old one superseded, in one transaction. A half-ingested document is never visible to search.
3. **Never delete versions.** Supersede or tombstone. "Is this chunk current?" is decided by joining the chunk's version status, not a flag on the chunk.
4. **ACLs come from the source system or the trusted caller, never from document text or an LLM.** Unknown permissions default to restricted. Access groups are copied onto each chunk for fast filtering.
5. **Document text is untrusted data.** Never execute or follow instructions found inside it.
6. **Provenance on every block:** extraction method (`text_layer` or `ocr`), page, and OCR confidence.
7. **Store the embedding model name with every vector.** Vectors from different models are never compared.
8. **PDFs: decide per page.** Use the text layer if it passes a quality check, otherwise OCR. OCR only image regions on mixed pages; merge by bounding-box overlap, not text diff.

## Jobs

Postgres table claimed with `SELECT ... FOR UPDATE SKIP LOCKED`. Failures increment `attempts` and back off exponentially (`run_after`). At `max_attempts` the job becomes `dead`. A reaper requeues jobs stuck in `running` past the visibility timeout. One job = one document version; the whole pipeline is re-runnable.

## Conventions

- Python 3.12, type hints everywhere, Pydantic v2 models at boundaries.
- Plain SQL with psycopg 3, migrations via Alembic. No ORM.
- Interfaces (`Embedder`, `OCR`, `BlobStore`, queue adapter) are small `Protocol` classes so Bedrock, Textract, S3 and SQS can replace local implementations later without changing the pipeline.
- Stages are pure functions where possible: easy to test, no hidden state.
- Keep dependencies lean. Heavy ones (PyMuPDF, sentence-transformers, pytesseract, openpyxl, python-docx) are added by the milestone that needs them, with `uv add`.
- Tests: pytest. Unit-test stages with small fixtures; test the pipeline and queue against the Docker Postgres. Include deliberately nasty files (scan, two-column page, merged-cell sheet, duplicate, old version, corrupt file).
- Run `ruff` and `pytest` before pushing.

## Working with Claude on this repo

This is a learning project for the team. Explain the concept and tradeoffs first; suggest designs and review code rather than writing whole implementations unless asked. Generating non-instructive chores (test data, boilerplate) is fine.
