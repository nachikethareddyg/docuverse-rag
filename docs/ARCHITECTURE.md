# Architecture

docuverse-rag is organized as a set of small pipeline stages rather than one
large application script. Each stage has a narrow responsibility and a test
surface that avoids real network calls, model downloads, and database access in
unit tests.

## Components

| Module | Responsibility |
| --- | --- |
| `docuverse.ingest` | Load local markdown/text files and create overlapping chunks |
| `docuverse.embed` | Generate embeddings with Sentence Transformers |
| `docuverse.store` | Create the pgvector schema and persist embedded chunks |
| `docuverse.retrieve` | Embed queries and search similar chunks in Postgres |
| `docuverse.prompt` | Build constrained prompts from retrieved context |
| `docuverse.answer` | Call the LLM, extract citations, and validate sources |
| `docuverse.api` | Expose `/health` and `/ask` through FastAPI |
| `docuverse.ui` | Provide a Streamlit question-answering interface |
| `docuverse.evaluate` | Score answers against a YAML gold set |

## Data Model

The main storage table is `document_chunks`:

```sql
CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL
);
```

The `id` field is intentionally stable and human-readable, such as `s3.md:0`.
That same ID is used in prompts and answer citations, which keeps the retrieval
and validation layers aligned.

## Retrieval Query

Retrieval uses pgvector cosine distance:

```sql
SELECT
    id,
    source_file,
    chunk_index,
    text,
    1 - (embedding <=> %s::vector) AS similarity
FROM document_chunks
ORDER BY embedding <=> %s::vector
LIMIT %s;
```

The result returns both the chunk text and a similarity score. The score is used
for source inspection in the CLI/API/UI, not as a guarantee of answer quality.

## Citation Contract

The prompt asks the model to cite sources using `[source: chunk_id]`. The answer
layer then extracts those citations and checks that each cited ID exists in the
retrieved chunks. If the model cites a chunk that was not retrieved, the answer
is rejected.

This design does not prove every sentence is grounded, but it prevents a common
failure mode: citations that look plausible but do not map to the actual context
used for generation.

## Testing Strategy

The test suite uses mocks and fakes for boundaries that are slow, expensive, or
environment-dependent:

- Embedding tests fake the Sentence Transformers model.
- Store and retrieval tests fake the database connection and cursor.
- Answer tests mock retrieval and the LLM call.
- API tests monkeypatch `generate_answer`.
- Evaluation tests mock generated answers.

That keeps CI fast while still testing the code paths and contracts that matter.

Integration tests with a real Postgres service would be a good next step, but
they should be separate from the default unit test run.
