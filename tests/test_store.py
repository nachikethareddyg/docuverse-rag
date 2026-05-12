from docuverse import store


class FakeCursor:
    def __init__(self, fetchone_result=None) -> None:
        self.statements = []
        self.executemany_calls = []
        self.fetchone_result = fetchone_result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def execute(self, sql: str) -> None:
        self.statements.append(sql)

    def executemany(self, sql: str, rows: list[tuple]) -> None:
        self.executemany_calls.append((sql, rows))

    def fetchone(self):
        return self.fetchone_result


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def cursor(self) -> FakeCursor:
        return self._cursor


def test_get_database_url_uses_environment(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://example/test")

    assert store.get_database_url() == "postgresql://example/test"


def test_create_schema_enables_vector_and_creates_table(monkeypatch) -> None:
    cursor = FakeCursor()
    monkeypatch.setattr(store, "connect", lambda: FakeConnection(cursor))

    store.create_schema()

    assert cursor.statements[0] == store.CREATE_EXTENSION_SQL
    assert "CREATE TABLE IF NOT EXISTS document_chunks" in cursor.statements[1]
    assert "embedding VECTOR(384) NOT NULL" in cursor.statements[1]


def test_reset_chunks_truncates_table(monkeypatch) -> None:
    cursor = FakeCursor()
    monkeypatch.setattr(store, "connect", lambda: FakeConnection(cursor))

    store.reset_chunks()

    assert cursor.statements == [store.RESET_CHUNKS_SQL]


def test_store_chunks_inserts_vector_rows(monkeypatch) -> None:
    cursor = FakeCursor()
    monkeypatch.setattr(store, "connect", lambda: FakeConnection(cursor))

    store.store_chunks(
        [
            {
                "chunk_id": "doc.md:0",
                "source_file": "doc.md",
                "chunk_index": 0,
                "text": "hello",
                "embedding": [0.1, 0.2, 0.3],
            }
        ]
    )

    sql, rows = cursor.executemany_calls[0]

    assert sql == store.INSERT_CHUNK_SQL
    assert rows == [("doc.md:0", "doc.md", 0, "hello", "[0.1,0.2,0.3]")]


def test_count_chunks_returns_count(monkeypatch) -> None:
    cursor = FakeCursor(fetchone_result=(3,))
    monkeypatch.setattr(store, "connect", lambda: FakeConnection(cursor))

    assert store.count_chunks() == 3
    assert cursor.statements == [store.COUNT_CHUNKS_SQL]
