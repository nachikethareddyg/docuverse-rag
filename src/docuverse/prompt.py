from __future__ import annotations

from typing import Any


INSUFFICIENT_CONTEXT_RESPONSE = "I don't know based on the provided documents."


def _chunk_id(chunk: dict[str, Any]) -> str:
    return str(chunk.get("chunk_id") or chunk.get("id"))


def build_context(chunks: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        f"[source: {_chunk_id(chunk)}]\n{chunk['text']}"
        for chunk in chunks
    )


def build_prompt(question: str, chunks: list[dict[str, Any]]) -> str:
    context = build_context(chunks)

    return f"""You are a careful document question-answering assistant.

Answer only from the provided context.
Cite sources using [source: chunk_id].
If the context is insufficient, say "{INSUFFICIENT_CONTEXT_RESPONSE}"

Context:
{context}

Question:
{question}

Answer:"""
