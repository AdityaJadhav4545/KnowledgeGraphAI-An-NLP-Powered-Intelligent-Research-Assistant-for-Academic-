import csv

from KnowledgeGraphAI.backend.api import evaluation


def test_annotation_counts_ignore_assisted_only_suggestions(tmp_path, monkeypatch):
    rows = [
        {
            "human_label": "",
            "relevance_judgment": "",
            "automated_label": "relevant",
            "independent_review_attested": "",
        },
        {
            "human_label": "relevant",
            "relevance_judgment": "relevant",
            "automated_label": "not_relevant",
            "independent_review_attested": "yes",
        },
        {
            "human_label": "",
            "relevance_judgment": "not_relevant",
            "automated_label": "not_relevant",
            "independent_review_attested": "false",
        },
    ]
    for kind in ("paper", "chunk"):
        path = tmp_path / f"{kind}_judgments.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    monkeypatch.setattr(evaluation, "_BENCHMARK", tmp_path)

    summary = evaluation._annotation_summary()

    assert summary["paper"] == {
        "candidate_count": 3,
        "human_judgment_count": 2,
        "unjudged_count": 1,
        "independent_review_count": 1,
    }
    assert summary["chunk"] == summary["paper"]
