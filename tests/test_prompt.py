from docuverse.prompt import (
    INSUFFICIENT_CONTEXT_RESPONSE,
    build_context,
    build_prompt,
)


def test_build_context_formats_chunks_with_source_markers() -> None:
    chunks = [
        {"id": "s3.md:0", "text": "S3 stores objects."},
        {"id": "iam.md:0", "text": "IAM controls access."},
    ]

    context = build_context(chunks)

    assert "[source: s3.md:0]\nS3 stores objects." in context
    assert "[source: iam.md:0]\nIAM controls access." in context


def test_build_prompt_includes_grounding_and_citation_rules() -> None:
    prompt = build_prompt("What is S3?", [{"id": "s3.md:0", "text": "S3 text"}])

    assert "Answer only from the provided context." in prompt
    assert "Cite sources using [source: chunk_id]." in prompt
    assert INSUFFICIENT_CONTEXT_RESPONSE in prompt
    assert "Question:\nWhat is S3?" in prompt
    assert "[source: s3.md:0]" in prompt
