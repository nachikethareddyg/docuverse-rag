from docuverse import embed


class FakeEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        return [
            [float(index), float(len(text))]
            for index, text in enumerate(texts)
        ]


def test_embed_texts_uses_model_and_returns_float_lists(monkeypatch) -> None:
    def fake_load_embedding_model(model_name: str) -> FakeEmbeddingModel:
        assert model_name == "fake-model"
        return FakeEmbeddingModel()

    monkeypatch.setattr(embed, "load_embedding_model", fake_load_embedding_model)

    embeddings = embed.embed_texts(["alpha", "beta"], model_name="fake-model")

    assert embeddings == [[0.0, 5.0], [1.0, 4.0]]
    assert all(isinstance(value, float) for row in embeddings for value in row)


def test_embed_chunks_adds_embedding_without_mutating_chunks(monkeypatch) -> None:
    def fake_embed_texts(
        texts: list[str],
        model_name: str = embed.DEFAULT_EMBEDDING_MODEL,
    ) -> list[list[float]]:
        assert texts == ["first chunk", "second chunk"]
        assert model_name == "fake-model"
        return [[0.1, 0.2], [0.3, 0.4]]

    chunks = [
        {
            "chunk_id": "doc.md:0",
            "source_file": "doc.md",
            "chunk_index": 0,
            "text": "first chunk",
        },
        {
            "chunk_id": "doc.md:1",
            "source_file": "doc.md",
            "chunk_index": 1,
            "text": "second chunk",
        },
    ]

    monkeypatch.setattr(embed, "embed_texts", fake_embed_texts)

    embedded_chunks = embed.embed_chunks(chunks, model_name="fake-model")

    assert embedded_chunks[0]["embedding"] == [0.1, 0.2]
    assert embedded_chunks[1]["embedding"] == [0.3, 0.4]
    assert "embedding" not in chunks[0]
