# Lessons Learned

The main lesson from docuverse-rag is that the hard part of RAG is not wiring an
LLM call. The hard part is making the path to that call understandable: where
the text came from, how it was chunked, which chunks were retrieved, what the
prompt contained, and whether the final answer cited real sources.

## Grounding Needs A Contract

Asking a model to cite sources is easy. Making those citations verifiable is the
more important engineering step. Carrying stable chunk IDs through ingestion,
retrieval, prompting, and answer validation gave the project a simple contract:
if an answer cites `[source: s3.md:0]`, that ID must exist in the retrieved
context.

The validation is intentionally narrow, but it catches a practical failure mode:
answers that look sourced while pointing to chunks the system never retrieved.

## Simple First Versions Are Useful

The project starts with character-based chunking. Token-aware chunking would be
more sophisticated, but character chunking made the first retrieval pipeline
deterministic and easy to test. That was a good tradeoff for the first complete
version because it made the behavior inspectable.

The same thinking applies to the evaluation harness. It does not try to judge
answer quality like a human would. It checks expected facts and expected
citations, which is enough to create an early regression signal.

## Infrastructure Should Match The Scope

pgvector was a good fit because it kept text, metadata, and embeddings in
Postgres. For a small portfolio-scale RAG system, adding a separate vector
database would have made the project harder to run without proving much more
about the retrieval design.

That does not mean pgvector is always the final answer. It means the storage
choice should match the current operating constraints.

## Boundaries Made The Project Easier To Build

Splitting the code into ingestion, embedding, storage, retrieval, prompting,
answering, API, UI, and evaluation modules kept each piece small enough to test.
Most tests do not need a running database, model download, or OpenAI request.

That made the development loop much faster and kept failures local. When a test
breaks, it is usually clear which layer changed.

## What I Would Improve Next

The next improvements would be token-aware chunking, richer document parsing,
integration tests against a real Postgres service, and evaluation output that can
be tracked over time. Those changes would build on the current shape rather than
replace it.
