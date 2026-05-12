from docuverse import retrieve


class FakeCursor:
    def __init__(self, rows=None) -> None:
        self.rows = rows or []
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def execute(self, sql: str, params: tuple) -> None:
        self.executed.append((sql, params))

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def cursor(self) -> FakeCursor:
        return self._cursor


def test_embed_query_embeds_single_query(monkeypatch) -> None:
    def fake_embed_texts(texts: list[str], model_name: str) -> list[list[float]]:
        assert texts == ["What is AWS S3?"]
        assert model_name == "fake-model"
        return [[0.1, 0.2, 0.3]]

    monkeypatch.setattr(retrieve, "embed_texts", fake_embed_texts)

    assert retrieve.embed_query("What is AWS S3?", model_name="fake-model") == [
        0.1,
        0.2,
        0.3,
    ]


def test_search_similar_chunks_queries_pgvector(monkeypatch) -> None:
    cursor = FakeCursor(
        rows=[
            ("s3.md:0", "s3.md", 0, "S3 stores objects in buckets.", 0.92),
            ("iam.md:0", "iam.md", 0, "IAM manages access.", 0.74),
        ]
    )
    monkeypatch.setattr(retrieve, "connect", lambda: FakeConnection(cursor))

    results = retrieve.search_similar_chunks([0.1, 0.2, 0.3], top_k=2)

    sql, params = cursor.executed[0]

    assert "embedding <=> %s::vector" in sql
    assert "1 - (embedding <=> %s::vector) AS similarity" in sql
    assert params == ("[0.1,0.2,0.3]", "[0.1,0.2,0.3]", 2)
    assert results == [
        {
            "id": "s3.md:0",
            "source_file": "s3.md",
            "chunk_index": 0,
            "text": "S3 stores objects in buckets.",
            "score": 0.92,
        },
        {
            "id": "iam.md:0",
            "source_file": "iam.md",
            "chunk_index": 0,
            "text": "IAM manages access.",
            "score": 0.74,
        },
    ]


def test_retrieve_chunks_embeds_query_then_searches(monkeypatch) -> None:
    calls = []

    def fake_embed_query(query: str) -> list[float]:
        calls.append(("embed", query))
        return [0.4, 0.5]

    def fake_search_similar_chunks(query_embedding: list[float], top_k: int):
        calls.append(("search", query_embedding, top_k))
        return [{"id": "s3.md:0", "score": 0.91}]

    monkeypatch.setattr(retrieve, "embed_query", fake_embed_query)
    monkeypatch.setattr(retrieve, "search_similar_chunks", fake_search_similar_chunks)

    results = retrieve.retrieve_chunks("What is AWS S3?", top_k=3)

    assert results == [{"id": "s3.md:0", "score": 0.91}]
    assert calls == [
        ("embed", "What is AWS S3?"),
        ("search", [0.4, 0.5], 3),
    ]
