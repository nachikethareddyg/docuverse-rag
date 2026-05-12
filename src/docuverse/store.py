from __future__ import annotations

import argparse
import os
from typing import Any

from docuverse.embed import embed_chunks
from docuverse.ingest import Chunk, ingest_directory


DEFAULT_DATABASE_URL = "postgresql://docuverse:docuverse@localhost:5432/docuverse"

CREATE_EXTENSION_SQL = "CREATE EXTENSION IF NOT EXISTS vector;"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL
);
"""

RESET_CHUNKS_SQL = "TRUNCATE TABLE document_chunks;"

INSERT_CHUNK_SQL = """
INSERT INTO document_chunks (id, source_file, chunk_index, text, embedding)
VALUES (%s, %s, %s, %s, %s::vector)
ON CONFLICT (id) DO UPDATE SET
    source_file = EXCLUDED.source_file,
    chunk_index = EXCLUDED.chunk_index,
    text = EXCLUDED.text,
    embedding = EXCLUDED.embedding;
"""

COUNT_CHUNKS_SQL = "SELECT COUNT(*) FROM document_chunks;"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def connect() -> Any:
    import psycopg

    return psycopg.connect(get_database_url())


def create_schema() -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EXTENSION_SQL)
            cursor.execute(CREATE_TABLE_SQL)


def reset_chunks() -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(RESET_CHUNKS_SQL)


def _format_vector(values: list[float]) -> str:
    return "[" + ",".join(str(float(value)) for value in values) + "]"


def store_chunks(chunks: list[Chunk]) -> None:
    rows = [
        (
            chunk["chunk_id"],
            chunk["source_file"],
            chunk["chunk_index"],
            chunk["text"],
            _format_vector(chunk["embedding"]),
        )
        for chunk in chunks
    ]

    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(INSERT_CHUNK_SQL, rows)


def count_chunks() -> int:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_CHUNKS_SQL)
            result = cursor.fetchone()

    if result is None:
        return 0

    return int(result[0])


def main() -> None:
    parser = argparse.ArgumentParser(description="Store embedded chunks in pgvector.")
    parser.add_argument("input_dir", help="Directory containing .md or .txt files")
    args = parser.parse_args()

    chunks = ingest_directory(args.input_dir)
    embedded_chunks = embed_chunks(chunks)

    create_schema()
    reset_chunks()
    store_chunks(embedded_chunks)

    print(f"Stored {count_chunks()} chunks")


if __name__ == "__main__":
    main()
