import pytest

from docuverse import answer


def test_extract_citations_returns_source_ids() -> None:
    answer_text = "S3 stores objects [source: s3.md:0]. IAM manages access [source: iam.md:1]."

    assert answer.extract_citations(answer_text) == ["s3.md:0", "iam.md:1"]


def test_validate_citations_allows_retrieved_sources() -> None:
    chunks = [{"id": "s3.md:0", "text": "S3 stores objects."}]
    answer_text = "S3 stores objects [source: s3.md:0]."

    assert answer.validate_citations(answer_text, chunks) == ["s3.md:0"]


def test_validate_citations_rejects_unknown_sources() -> None:
    chunks = [{"id": "s3.md:0", "text": "S3 stores objects."}]
    answer_text = "IAM controls access [source: iam.md:0]."

    with pytest.raises(ValueError, match="iam.md:0"):
        answer.validate_citations(answer_text, chunks)


def test_call_llm_requires_openai_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        answer.call_llm("prompt")


def test_generate_answer_retrieves_builds_prompts_and_validates(monkeypatch) -> None:
    chunks = [{"id": "s3.md:0", "text": "S3 stores objects."}]
    calls = []

    def fake_retrieve_chunks(question: str, top_k: int):
        calls.append(("retrieve", question, top_k))
        return chunks

    def fake_build_prompt(question: str, retrieved_chunks):
        calls.append(("prompt", question, retrieved_chunks))
        return "built prompt"

    def fake_call_llm(prompt: str) -> str:
        calls.append(("llm", prompt))
        return "S3 stores objects [source: s3.md:0]."

    monkeypatch.setattr(answer, "retrieve_chunks", fake_retrieve_chunks)
    monkeypatch.setattr(answer, "build_prompt", fake_build_prompt)
    monkeypatch.setattr(answer, "call_llm", fake_call_llm)

    result = answer.generate_answer("What is AWS S3?", top_k=3)

    assert result == {
        "answer": "S3 stores objects [source: s3.md:0].",
        "citations": ["s3.md:0"],
        "sources": chunks,
    }
    assert calls == [
        ("retrieve", "What is AWS S3?", 3),
        ("prompt", "What is AWS S3?", chunks),
        ("llm", "built prompt"),
    ]
