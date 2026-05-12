from __future__ import annotations

import argparse
import os
import re
from typing import Any

from docuverse.prompt import build_prompt
from docuverse.retrieve import retrieve_chunks


DEFAULT_LLM_MODEL = "gpt-4o-mini"
CITATION_PATTERN = re.compile(r"\[source:\s*([^\]]+)\]")


def extract_citations(answer_text: str) -> list[str]:
    return [match.strip() for match in CITATION_PATTERN.findall(answer_text)]


def _chunk_id(chunk: dict[str, Any]) -> str:
    return str(chunk.get("chunk_id") or chunk.get("id"))


def validate_citations(answer_text: str, chunks: list[dict[str, Any]]) -> list[str]:
    citations = extract_citations(answer_text)
    valid_chunk_ids = {_chunk_id(chunk) for chunk in chunks}
    invalid_citations = [
        citation for citation in citations if citation not in valid_chunk_ids
    ]

    if invalid_citations:
        raise ValueError(
            "Answer contains citations not found in retrieved chunks: "
            + ", ".join(invalid_citations)
        )

    return citations


def call_llm(prompt: str, model: str = DEFAULT_LLM_MODEL) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is required to generate answers. Set it before running "
            "python -m docuverse.answer."
        )

    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text


def generate_answer(question: str, top_k: int = 5) -> dict[str, Any]:
    chunks = retrieve_chunks(question, top_k=top_k)
    prompt = build_prompt(question, chunks)
    answer_text = call_llm(prompt)
    citations = validate_citations(answer_text, chunks)

    return {
        "answer": answer_text,
        "citations": citations,
        "sources": chunks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an answer with citations.")
    parser.add_argument("question", help="Question to answer")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to use")
    args = parser.parse_args()

    result = generate_answer(args.question, top_k=args.top_k)

    print(result["answer"])
    print()
    print("Citations:")
    for citation in result["citations"]:
        print(f"- {citation}")


if __name__ == "__main__":
    main()
