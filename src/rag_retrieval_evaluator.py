
import csv
import json
import re
from pathlib import Path

from rag_retriever import retrieve_relevant_chunks
from rag_document_loader import load_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT / "data" / "ground_truth" / "rag_test_dataset.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "outputs" / "reports"
    / "day24_retrieval_evaluation.csv"
)

K_VALUES = [1, 3, 5]


def get_technique_id(document):
    """Extract the MITRE technique ID from a knowledge document."""

    match = re.search(
        r"Technique ID:\s*([A-Za-z0-9.]+)",
        document
    )

    return match.group(1) if match else None


def evaluate_retrieval():
    """Evaluate RAG retrieval using the ground-truth dataset."""

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    documents = load_documents()

    technique_by_document = {
        index: get_technique_id(document)
        for index, document in enumerate(documents, start=1)
    }

    evaluation_rows = []

    for test_case in test_cases:
        expected_id = test_case["expected_technique_id"]

        results = retrieve_relevant_chunks(
            test_case["alert"],
            top_k=5
        )

        retrieved_ids = [
            technique_by_document.get(result["document_id"])
            for result in results
        ]

        retrieved_ids = [
            technique_id
            for technique_id in retrieved_ids
            if technique_id is not None
        ]

        expected_rank = (
            retrieved_ids.index(expected_id) + 1
            if expected_id in retrieved_ids
            else ""
        )

        row = {
            "test_id": test_case["test_id"],
            "expected_technique_id": expected_id,
            "expected_technique_name": test_case[
                "expected_technique_name"
            ],
            "top1_predicted_technique_id": (
                retrieved_ids[0] if retrieved_ids else ""
            ),
            "expected_rank": expected_rank,
            "retrieved_technique_ids": ";".join(retrieved_ids),
            "top1_correct": (
                retrieved_ids[0] == expected_id
                if retrieved_ids else False
            )
        }

        for k in K_VALUES:
            top_k_ids = retrieved_ids[:k]
            hit = expected_id in top_k_ids

            # Precision@K uses K as the denominator.
            row[f"precision_at_{k}"] = (
                1 / k if hit else 0
            )

            # There is one expected relevant technique per alert.
            row[f"recall_at_{k}"] = (
                1.0 if hit else 0.0
            )

        evaluation_rows.append(row)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(evaluation_rows[0].keys())

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evaluation_rows)

    total_tests = len(evaluation_rows)

    print("RAG RETRIEVAL EVALUATION")
    print("=" * 40)
    print("Total test cases:", total_tests)

    for k in K_VALUES:
        precision = sum(
            row[f"precision_at_{k}"]
            for row in evaluation_rows
        ) / total_tests

        recall = sum(
            row[f"recall_at_{k}"]
            for row in evaluation_rows
        ) / total_tests

        print(f"\nPrecision@{k}: {precision:.4f}")
        print(f"Recall@{k}:    {recall:.4f}")

    top1_accuracy = sum(
        row["top1_correct"]
        for row in evaluation_rows
    ) / total_tests

    print(f"\nTop-1 Accuracy: {top1_accuracy:.4f}")

    print("\nIndividual Test Results")
    print("-" * 40)

    for row in evaluation_rows:
        print(
            row["test_id"],
            "| Expected:", row["expected_technique_id"],
            "| Predicted:", row["top1_predicted_technique_id"],
            "| Rank:", row["expected_rank"]
        )

    print("\nEvaluation CSV saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    evaluate_retrieval()
