# docuverse-rag

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-similarity_search-5f43b2)](https://github.com/pgvector/pgvector)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](.github/workflows/ci.yml)

docuverse-rag is a compact, end-to-end RAG system for asking citation-grounded
questions over local documents. It ingests markdown/text files, chunks them,
generates local embeddings, stores vectors in PostgreSQL with pgvector, retrieves
similar chunks, validates citations, serves answers through FastAPI, and includes
a Streamlit interface plus a small evaluation harness.

This repository is intentionally small, but it is built like a real system:
separate pipeline stages, testable boundaries, deterministic unit tests, and a
database schema that can support the next layer of product work.

## Problem Statement

Teams often have useful information scattered across internal markdown files,
runbooks, notes, and cloud documentation. A basic chat interface over those files
is not enough: answers need to be traceable, retrieval needs to be inspectable,
and regressions need to be measurable.

docuverse-rag solves a focused version of that problem. It creates a searchable
document QA pipeline where every generated answer is expected to cite the chunks
that support it.

## Key Features

- Local document ingestion for markdown and text files
- Overlapping text chunking with stable chunk metadata
- Sentence Transformers embeddings using `BAAI/bge-small-en-v1.5`
- PostgreSQL 16 plus pgvector storage for vector similarity search
- Cosine-similarity retrieval over stored chunks
- Citation-grounded answer generation with OpenAI `gpt-4o-mini`
- FastAPI `/health` and `/ask` endpoints
- Streamlit UI for visual question answering
- YAML-based evaluation harness with deterministic fact and citation scoring
- CI-friendly tests with mocked model, database, and LLM calls

## Architecture Overview

```mermaid
flowchart LR
    A["Local markdown/text files"] --> B["Ingestion<br/>load + chunk"]
    B --> C["Embedding<br/>bge-small-en-v1.5"]
    C --> D["Postgres 16<br/>pgvector table"]
    E["Question"] --> F["Query embedding"]
    F --> G["pgvector similarity search"]
    D --> G
    G --> H["Prompt builder<br/>context + citation rules"]
    H --> I["OpenAI gpt-4o-mini"]
    I --> J["Citation validation"]
    J --> K["FastAPI /ask<br/>Streamlit UI<br/>CLI"]
    L["Gold set YAML"] --> M["Evaluation harness"]
    K --> M
```

For more detail, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Retrieval Flow

1. `docuverse.ingest` reads `.md` and `.txt` files from a local directory.
2. Documents are split into overlapping chunks with `chunk_id`, `source_file`,
   `chunk_index`, and `text`.
3. `docuverse.embed` embeds chunk text with `BAAI/bge-small-en-v1.5`.
4. `docuverse.store` creates the pgvector schema and stores chunk embeddings.
5. `docuverse.retrieve` embeds the user query and searches with pgvector cosine
   distance.
6. `docuverse.prompt` builds a constrained prompt from retrieved context.
7. `docuverse.answer` calls the LLM, extracts citations, and rejects citations
   that do not match retrieved chunks.

## Tech Stack

| Layer | Choice |
| --- | --- |
| Runtime | Python 3.11 |
| API | FastAPI, Pydantic |
| UI | Streamlit |
| Embeddings | Sentence Transformers, `BAAI/bge-small-en-v1.5` |
| Vector storage | PostgreSQL 16, pgvector |
| LLM | OpenAI SDK, `gpt-4o-mini` |
| Evaluation | PyYAML gold set, deterministic scoring |
| Tests | pytest, FastAPI TestClient, monkeypatch-based fakes |
| Dev ops | Docker Compose, GitHub Actions |

## Why These Design Choices?

**pgvector** keeps vector search close to relational metadata. For a small RAG
system, this avoids introducing a separate vector database before the product
needs one, while still supporting real cosine-similarity retrieval.

**`BAAI/bge-small-en-v1.5`** is a practical local embedding model: small enough
for developer machines, strong enough for semantic search prototypes, and widely
used enough to be a reasonable default.

**Citation validation** turns citation format from a prompt suggestion into a
runtime contract. The answer layer checks that cited chunk IDs were actually
retrieved, which reduces unsupported source references.

**FastAPI** gives the project a clean service boundary, typed request/response
models, validation, and easy testability with `TestClient`.

**Evaluation harness** makes quality visible. The current scorer is deliberately
simple, but it creates a place to track facts, citations, and regressions as the
corpus grows.

## Evaluation Harness

The evaluation harness lives in [eval/gold_set.yaml](eval/gold_set.yaml). It
contains 10 questions over the sample AWS corpus, each with expected facts and
expected source files.

Run it with:

```powershell
python -m docuverse.evaluate eval/gold_set.yaml
```

Current scoring is deterministic:

- `fact_score`: percentage of expected facts found in the answer text
- `citation_score`: `1` when at least one expected source is cited, otherwise `0`
- invalid citations fail the item

This is not meant to replace human review. It is a lightweight regression
signal that can evolve into richer retrieval and answer-quality checks.

## Local Setup

Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Run tests:

```powershell
python -m pytest
```

Start Postgres with pgvector:

```powershell
docker compose up -d postgres
```

Load the sample AWS corpus into pgvector:

```powershell
python -m docuverse.store data/corpus_aws
```

Set your OpenAI API key:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

## API Usage

Start the API:

```powershell
python -m uvicorn docuverse.api:app --reload
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Ask a question:

```powershell
$body = @{
    question = "What is AWS S3?"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/ask `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected response shape:

```json
{
  "answer": "S3 is an object storage service... [source: s3.md:0]",
  "citations": ["s3.md:0"],
  "sources": [
    {
      "id": "s3.md:0",
      "source_file": "data/corpus_aws/s3.md",
      "chunk_index": 0,
      "text": "...",
      "score": 0.92
    }
  ]
}
```

## Streamlit Demo

Run the UI:

```powershell
streamlit run src/docuverse/ui.py
```

The UI provides a question box, a `top_k` slider, answer display, citations, and
an expandable source inspection area. It also surfaces common setup errors such
as a missing `OPENAI_API_KEY`, an unavailable database, or an empty chunk store.

## Project Structure

```text
docuverse-rag/
|-- data/corpus_aws/          # Small sample markdown corpus
|-- docker/postgres/init.sql  # pgvector extension initialization
|-- docs/                     # Architecture and learning notes
|-- eval/gold_set.yaml        # Evaluation questions and expected facts
|-- src/docuverse/
|   |-- api.py                # FastAPI service
|   |-- answer.py             # LLM answer generation and citation validation
|   |-- embed.py              # Sentence Transformers embedding layer
|   |-- evaluate.py           # Evaluation harness
|   |-- ingest.py             # Local document loading and chunking
|   |-- prompt.py             # Context and prompt construction
|   |-- retrieve.py           # pgvector similarity retrieval
|   |-- store.py              # Postgres/pgvector persistence
|   `-- ui.py                 # Streamlit interface
`-- tests/                    # Unit tests with mocked external systems
```

## Future Improvements

- Add migration tooling for schema changes
- Store document-level metadata separately from chunk rows
- Add hybrid search with keyword plus vector ranking
- Track evaluation results over time in CI artifacts
- Add integration tests behind an optional Postgres service
- Support PDF ingestion and richer document parsing
- Add streaming answer responses in the API and UI
- Improve scoring with semantic similarity and citation coverage checks

## Lessons Learned

RAG quality is mostly a systems problem. The model call is only one part of the
pipeline; chunking, metadata, retrieval, citation contracts, and evaluation all
shape whether the final answer is trustworthy.

The most useful pattern in this project was keeping each stage small and
testable. Ingestion, embedding, storage, retrieval, prompting, answering, and
evaluation can all be reasoned about independently, which makes the project easy
to extend without hiding bugs behind a single end-to-end script.

For a more personal write-up, see [docs/LESSONS.md](docs/LESSONS.md).
