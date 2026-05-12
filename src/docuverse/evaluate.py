from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from docuverse.answer import generate_answer


def load_gold_set(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, list):
        raise ValueError("Gold set must be a list of evaluation items")

    return data


def score_answer(
    answer: str,
    expected_facts: list[str],
    citations: list[str],
    expected_sources: list[str],
) -> dict[str, Any]:
    invalid_citations = [
        citation
        for citation in citations
        if not any(citation.startswith(source) for source in expected_sources)
    ]

    if invalid_citations:
        return {
            "fact_score": 0.0,
            "citation_score": 0.0,
            "invalid_citations": invalid_citations,
        }

    answer_lower = answer.lower()
    matched_facts = [
        fact for fact in expected_facts if fact.lower() in answer_lower
    ]
    fact_score = (
        len(matched_facts) / len(expected_facts) if expected_facts else 1.0
    )
    citation_score = 1.0 if any(
        citation.startswith(source)
        for citation in citations
        for source in expected_sources
    ) else 0.0

    return {
        "fact_score": fact_score,
        "citation_score": citation_score,
        "invalid_citations": [],
    }


def run_evaluation(gold_set_path: str | Path) -> dict[str, Any]:
    gold_set = load_gold_set(gold_set_path)
    results = []

    for item in gold_set:
        generated = generate_answer(item["question"])
        score = score_answer(
            generated["answer"],
            item["expected_facts"],
            generated["citations"],
            item["expected_sources"],
        )
        results.append(
            {
                "id": item["id"],
                "question": item["question"],
                **score,
            }
        )

    total_questions = len(results)
    average_fact_score = (
        sum(result["fact_score"] for result in results) / total_questions
        if total_questions
        else 0.0
    )
    average_citation_score = (
        sum(result["citation_score"] for result in results) / total_questions
        if total_questions
        else 0.0
    )

    return {
        "total_questions": total_questions,
        "average_fact_score": average_fact_score,
        "average_citation_score": average_citation_score,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG answers.")
    parser.add_argument("gold_set_path", help="Path to a YAML gold set")
    args = parser.parse_args()

    evaluation = run_evaluation(args.gold_set_path)

    print(f"Total questions: {evaluation['total_questions']}")
    print(f"Average fact score: {evaluation['average_fact_score']:.2f}")
    print(f"Average citation score: {evaluation['average_citation_score']:.2f}")
    print()
    print("Per-question results:")

    for result in evaluation["results"]:
        print(
            f"- {result['id']}: "
            f"fact_score={result['fact_score']:.2f}, "
            f"citation_score={result['citation_score']:.2f}"
        )


if __name__ == "__main__":
    main()
