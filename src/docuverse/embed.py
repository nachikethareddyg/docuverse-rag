from __future__ import annotations

import argparse
from typing import Any

from docuverse.ingest import Chunk, ingest_directory


DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


def load_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL) -> Any:
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def _to_float_list(vector: Any) -> list[float]:
    if hasattr(vector, "tolist"):
        vector = vector.tolist()

    return [float(value) for value in vector]


def embed_texts(
    texts: list[str],
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> list[list[float]]:
    model = load_embedding_model(model_name)
    embeddings = model.encode(texts)

    return [_to_float_list(embedding) for embedding in embeddings]


def embed_chunks(
    chunks: list[Chunk],
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> list[Chunk]:
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts, model_name=model_name)

    return [
        {
            **chunk,
            "embedding": embedding,
        }
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed ingested document chunks.")
    parser.add_argument("input_dir", help="Directory containing .md or .txt files")
    parser.add_argument(
        "--model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Sentence Transformers model name",
    )
    args = parser.parse_args()

    chunks = ingest_directory(args.input_dir)
    embedded_chunks = embed_chunks(chunks, model_name=args.model)
    embedding_dimension = (
        len(embedded_chunks[0]["embedding"]) if embedded_chunks else 0
    )

    print(f"Loaded {len(chunks)} chunks")
    print(f"Created {len(embedded_chunks)} embeddings")
    print(f"Embedding dimension: {embedding_dimension}")


if __name__ == "__main__":
    main()
