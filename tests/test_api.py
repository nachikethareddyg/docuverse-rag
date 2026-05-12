from fastapi.testclient import TestClient

from docuverse import api


def test_health_returns_ok() -> None:
    client = TestClient(api.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer_using_generate_answer(monkeypatch) -> None:
    def fake_generate_answer(question: str, top_k: int):
        assert question == "What is AWS S3?"
        assert top_k == 3
        return {
            "answer": "S3 stores objects [source: s3.md:0].",
            "citations": ["s3.md:0"],
            "sources": [
                {
                    "id": "s3.md:0",
                    "source_file": "s3.md",
                    "chunk_index": 0,
                    "text": "S3 stores objects.",
                    "score": 0.92,
                }
            ],
        }

    monkeypatch.setattr(api, "generate_answer", fake_generate_answer)
    client = TestClient(api.app)

    response = client.post(
        "/ask",
        json={"question": "What is AWS S3?", "top_k": 3},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "S3 stores objects [source: s3.md:0].",
        "citations": ["s3.md:0"],
        "sources": [
            {
                "id": "s3.md:0",
                "source_file": "s3.md",
                "chunk_index": 0,
                "text": "S3 stores objects.",
                "score": 0.92,
            }
        ],
    }


def test_ask_rejects_empty_question() -> None:
    client = TestClient(api.app)

    response = client.post("/ask", json={"question": "", "top_k": 5})

    assert response.status_code == 422


def test_ask_rejects_invalid_top_k() -> None:
    client = TestClient(api.app)

    low_response = client.post("/ask", json={"question": "What is S3?", "top_k": 0})
    high_response = client.post("/ask", json={"question": "What is S3?", "top_k": 21})

    assert low_response.status_code == 422
    assert high_response.status_code == 422
