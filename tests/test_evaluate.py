from pathlib import Path

import yaml

from docuverse import evaluate


def test_load_gold_set_reads_yaml_items(tmp_path: Path) -> None:
    gold_set_path = tmp_path / "gold.yaml"
    gold_set_path.write_text(
        yaml.safe_dump(
            [
                {
                    "id": "q1",
                    "question": "What is S3?",
                    "expected_facts": ["object storage"],
                    "expected_sources": ["s3.md"],
                }
            ]
        ),
        encoding="utf-8",
    )

    gold_set = evaluate.load_gold_set(gold_set_path)

    assert gold_set[0]["id"] == "q1"
    assert gold_set[0]["expected_sources"] == ["s3.md"]


def test_score_answer_scores_expected_facts_and_sources() -> None:
    score = evaluate.score_answer(
        answer="S3 is an object storage service for storing files.",
        expected_facts=["object storage service", "storing files"],
        citations=["s3.md:0"],
        expected_sources=["s3.md"],
    )

    assert score == {
        "fact_score": 1.0,
        "citation_score": 1.0,
        "invalid_citations": [],
    }


def test_score_answer_fails_item_for_invalid_citations() -> None:
    score = evaluate.score_answer(
        answer="S3 is an object storage service.",
        expected_facts=["object storage service"],
        citations=["iam.md:0"],
        expected_sources=["s3.md"],
    )

    assert score == {
        "fact_score": 0.0,
        "citation_score": 0.0,
        "invalid_citations": ["iam.md:0"],
    }


def test_run_evaluation_uses_generate_answer(monkeypatch, tmp_path: Path) -> None:
    gold_set_path = tmp_path / "gold.yaml"
    gold_set_path.write_text(
        yaml.safe_dump(
            [
                {
                    "id": "s3",
                    "question": "What is S3?",
                    "expected_facts": ["object storage service", "storing files"],
                    "expected_sources": ["s3.md"],
                },
                {
                    "id": "iam",
                    "question": "What is IAM?",
                    "expected_facts": ["access to AWS resources"],
                    "expected_sources": ["iam.md"],
                },
            ]
        ),
        encoding="utf-8",
    )

    answers = {
        "What is S3?": {
            "answer": "S3 is an object storage service for storing files.",
            "citations": ["s3.md:0"],
            "sources": [],
        },
        "What is IAM?": {
            "answer": "IAM controls access to AWS resources.",
            "citations": ["iam.md:0"],
            "sources": [],
        },
    }

    monkeypatch.setattr(
        evaluate,
        "generate_answer",
        lambda question: answers[question],
    )

    result = evaluate.run_evaluation(gold_set_path)

    assert result["total_questions"] == 2
    assert result["average_fact_score"] == 1.0
    assert result["average_citation_score"] == 1.0
    assert [item["id"] for item in result["results"]] == ["s3", "iam"]
