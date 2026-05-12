from __future__ import annotations

import argparse
from typing import Any

from docuverse.embed import DEFAULT_EMBEDDING_MODEL, embed_texts
from docuverse.store import _format_vector, connect


SEARCH_SIMILAR_CHUNKS_SQL = """
SELECT
    id,
    source_file,
    chunk_index,
    text,
    1 - (embedding <=> %s::vector) AS similarity
FROM document_chunks
ORDER BY embedding <=> %s::vector
LIMIT %s;
"""


def embed_query(
    query: str,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> list[float]:
    return embed_texts([query], model_name=model_name)[0]


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 5,
) -> list[dict[str, Any]]:
    vector = _format_vector(query_embedding)

    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_SIMILAR_CHUNKS_SQL, (vector, vector, top_k))
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "source_file": row[1],
            "chunk_index": row[2],
            "text": row[3],
            "score": float(row[4]),
        }
        for row in rows
    ]


def retrieve_chunks(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    query_embedding = embed_query(query)
    return search_similar_chunks(query_embedding, top_k=top_k)


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve similar chunks from pgvector.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to return")
    args = parser.parse_args()

    results = retrieve_chunks(args.query, top_k=args.top_k)

    print(f"Query: {args.query}")
    print()
    print("Top Results:")
    for index, result in enumerate(results, start=1):
        print(f"[{index}] {result['source_file']} (score={result['score']:.2f})")
        print(result["text"])
        print()


if __name__ == "__main__":
    main()
