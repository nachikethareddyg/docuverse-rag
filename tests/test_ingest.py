from pathlib import Path

from docuverse.ingest import chunk_text, ingest_directory, load_documents


def test_load_documents_reads_markdown_and_text_files(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# A\nMarkdown document", encoding="utf-8")
    (tmp_path / "b.txt").write_text("Text document", encoding="utf-8")
    (tmp_path / "ignore.json").write_text("{}", encoding="utf-8")

    documents = load_documents(tmp_path)

    assert len(documents) == 2
    assert [Path(doc["source_file"]).name for doc in documents] == ["a.md", "b.txt"]
    assert documents[0]["text"] == "# A\nMarkdown document"


def test_chunk_text_uses_overlap() -> None:
    chunks = chunk_text("abcdefghijklmnopqrstuvwxyz", chunk_size=10, overlap=3)

    assert chunks == ["abcdefghij", "hijklmnopq", "opqrstuvwx", "vwxyz"]


def test_ingest_directory_returns_chunks(tmp_path: Path) -> None:
    (tmp_path / "sample.md").write_text("abcdefghijklmnopqrstuvwxyz", encoding="utf-8")

    chunks = ingest_directory(tmp_path)

    assert len(chunks) == 1
    assert chunks[0]["chunk_id"] == "sample.md:0"
    assert Path(chunks[0]["source_file"]).name == "sample.md"
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["text"] == "abcdefghijklmnopqrstuvwxyz"
