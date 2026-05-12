from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any


Document = dict[str, str]
Chunk = dict[str, Any]


def load_documents(input_dir: str | Path) -> list[Document]:
    input_path = Path(input_dir)
    documents: list[Document] = []

    for path in sorted(input_path.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            documents.append(
                {
                    "source_file": str(path),
                    "text": path.read_text(encoding="utf-8"),
                }
            )

    return documents


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    clean_text = text.strip()
    if not clean_text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(clean_text):
        end = start + chunk_size
        chunks.append(clean_text[start:end])

        if end >= len(clean_text):
            break

        start = end - overlap

    return chunks


def ingest_directory(input_dir: str | Path) -> list[Chunk]:
    chunks: list[Chunk] = []

    for document in load_documents(input_dir):
        document_chunks = chunk_text(document["text"])

        for chunk_index, text in enumerate(document_chunks):
            chunks.append(
                {
                    "chunk_id": f"{Path(document['source_file']).name}:{chunk_index}",
                    "source_file": document["source_file"],
                    "chunk_index": chunk_index,
                    "text": text,
                }
            )

    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest local text and markdown files.")
    parser.add_argument("input_dir", help="Directory containing .md or .txt files")
    args = parser.parse_args()

    documents = load_documents(args.input_dir)
    chunks = ingest_directory(args.input_dir)

    print(f"Loaded {len(documents)} documents")
    print(f"Created {len(chunks)} chunks")


if __name__ == "__main__":
    main()
