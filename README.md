# Verity

Permission-aware, cited answers from a company's own knowledge.

Employees ask questions in plain words. Verity finds the right, current documents they are allowed to see, writes a short answer, and shows exactly which source each fact came from. When evidence is missing or documents conflict, it says so instead of guessing.

## The problem it solves

Company knowledge is scattered across an HR portal, a wiki, a help center, a ticket system and shared drives. Old and new versions disagree, some documents are restricted, scanned files hide their text, and a plain chatbot will confidently quote the wrong or private thing. Verity builds the infrastructure that makes a knowledge assistant trustworthy: ingestion, retrieval, grounding, security, evaluation, observability and deployment.

## Services

| Service | Folder | Status |
| --- | --- | --- |
| Ingestion | [`ingestion/`](ingestion/) | In progress (Phase 1) |
| Retrieval, answering, backend API, evaluation | not started | Later phases |

## Phases

1. Ingestion: parse, clean, chunk, label and store documents
2. Retrieval: vector, keyword, hybrid search and reranking
3. Answer generation with citations and abstention
4. Security: SSO, roles, document-level access
5. Evaluation and automated regression tests
6. Multi-agent supervisor
7. Observability
8. AWS deployment

## Getting started

Each service has its own README. For ingestion, see [`ingestion/README.md`](ingestion/README.md).

## Repository notes

Personal working notes and planning documents (`notes/`, `docs/`) are kept locally and are not tracked in git.
