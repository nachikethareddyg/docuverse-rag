# Lessons Learned

Building docuverse-rag reinforced that a useful RAG system is less about a
single clever prompt and more about careful interfaces between ordinary pieces
of software.

## Grounding Needs Structure

It is easy to ask a model to cite sources. It is more useful to make citations a
contract. By carrying stable chunk IDs from ingestion through retrieval and into
the prompt, the answer layer can validate whether cited sources were actually
available to the model.

That validation is intentionally simple, but it changes the shape of the system:
answers are no longer just text, they are text plus evidence.

## Small Models Are Useful Defaults

`BAAI/bge-small-en-v1.5` is not the largest embedding model available, and that
is part of why it is a good default here. It keeps the local developer workflow
reasonable while still producing useful semantic vectors for a prototype-scale
corpus.

The lesson is not that small is always better. It is that model choice should
fit the operating constraints of the project.

## Postgres Is a Strong Starting Point

Using pgvector keeps metadata, text, and embeddings in one database. For this
project, that made the system easier to run, test, and explain. A dedicated
vector database may make sense later, but adding one before it is needed would
increase operational complexity without improving the core learning goal.

## Evaluation Should Start Early

The evaluation harness is intentionally modest: expected facts, expected
sources, and deterministic scoring. Even so, it creates a useful habit. Each new
retrieval or prompting change can be checked against a known set of questions.

That matters because RAG regressions are often subtle. The system may still
return fluent answers while quietly retrieving worse context or dropping
citations.

## Boundaries Make the Project Easier to Grow

The project is split into ingestion, embedding, storage, retrieval, prompting,
answering, API, UI, and evaluation modules. That separation made it possible to
test most of the behavior without real OpenAI calls, real model downloads, or a
running database.

The main takeaway: clean boundaries are not just architecture polish. They make
the day-to-day engineering loop faster and safer.
