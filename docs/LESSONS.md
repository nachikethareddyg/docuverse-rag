# Lessons Learned

The biggest thing I learned is that a RAG project is mostly backend plumbing.
The LLM call is the visible part, but the quality of the answer depends on the
steps before it: how documents are chunked, what metadata survives, what gets
retrieved, and whether the final citations can be checked.

## Retrieval Depends On Chunking More Than I Expected

I started with character-based chunking because it is deterministic and easy to
test. That was the right choice for a first working version, but it also made
the limitation obvious. Chunk boundaries affect what gets embedded, what gets
retrieved, and what context the model sees.

The next version should use token-aware chunking and probably preserve more
document structure.

## Prompting Alone Is Not Enough

It is easy to tell a model to cite sources. That does not mean the citations are
valid. Adding citation validation made the system feel more real because the
answer has to cite chunk IDs that were actually retrieved.

This does not eliminate unsupported answers, but it reduces one concrete failure
mode: made-up or mismatched source references.

## Small Boundaries Made Testing Easier

Keeping ingestion, embedding, storage, retrieval, prompting, answering, API, UI,
and evaluation in separate modules made the project much easier to test. Most
tests do not need Postgres, a model download, or an OpenAI request.

Mocking those external systems kept CI reliable and made the unit tests fast.
That mattered a lot once the project had more than one moving piece.

## pgvector Was Enough For This Scope

A separate vector database would have been interesting, but it was not necessary
for this project. pgvector let me keep vectors, chunk text, source files, and
metadata in Postgres. For a portfolio-scale system, that was simpler and easier
to explain.

I would only reach for a separate vector store after the project has enough data
or operational needs to justify it.

## What I Would Improve Next

I would add token-aware chunking, PDF/table extraction, integration tests against
a real Postgres service, and evaluation output that can be tracked over time.
The current version is a small but complete baseline, which is exactly what I
wanted before making the retrieval logic more sophisticated.
