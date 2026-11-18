import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INVESTIGATION_FILE = ROOT / "outputs/soc_investigations/rag_meta_alert_investigation.csv"
DATASET_FILE = ROOT / "data/ground_truth/ai_quality_test_dataset.json"
CRITERIA_FILE = ROOT / "config/ai_quality_criteria.json"

OUTPUT_DIR = ROOT / "outputs/reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "day29_ai_quality_evaluation.csv"


def evaluate_case(row, ground_truth):
    case_id = row["meta_alert_id"]
    findings = ground_truth["expected_findings"]

    evidence_text = str(row["evidence_analysis"]).lower()
    explanation = str(row["ai_explanation"]).lower()
    steps = str(row["investigation_steps"]).lower()
    limitations = str(row["limitations"]).lower()
    mitre = str(row["mitre_analysis"]).lower()
    assessment = str(row["ai_incident_assessment"]).lower()

    all_text = " ".join([
        evidence_text, explanation, steps, limitations, mitre, assessment
    ])

    scores = {}
    notes = {}

    # 1. Evidence accuracy
    evidence_score = 2
    evidence_note = "No predefined evidence-attribution issue detected."

    if case_id == "META-001":
        if "failed logon attempts" in steps:
            evidence_score = 1
            evidence_note = (
                "Partially accurate: plural failed-logon wording was used "
                "although only one failed-logon event exists."
            )

    elif case_id == "META-003":
        if (
            "failed password and failed logon attempts originating "
            "from source ip" in evidence_text
            or "involving source ip 192.168.1.50" in explanation
        ):
            evidence_score = 1
            evidence_note = (
                "Partially accurate: Event 1 source IP was attributed "
                "to both authentication events."
            )

    scores["evidence_accuracy"] = evidence_score
    notes["evidence_accuracy"] = evidence_note

    # 2. Technical correctness
    if findings["incident_status"].lower() == "not confirmed":
        incident_preserved = (
            "unconfirmed" in assessment
            or "not confirmed" in assessment
        )
    else:
        incident_preserved = True

    if findings["mitre_status"] == "Potential event-level mapping":
        mapping_preserved = (
            "potential" in mitre
            and ("unconfirmed" in mitre or "do not constitute confirmed" in mitre or "not a confirmed mapping" in mitre)
        )
    elif findings["mitre_status"] == "Insufficient evidence":
        uncertainty_phrases = (
            "not a confirmed mapping",
            "not assigned",
            "without upgrading",
            "insufficient evidence",
            "does not establish",
            "not established",
            "unconfirmed"
        )
        mapping_preserved = (
            "insufficient evidence" in mitre
            and any(phrase in mitre for phrase in uncertainty_phrases)
        )
    else:
        mapping_preserved = True

    technical_score = 2 if incident_preserved and mapping_preserved else 1
    scores["technical_correctness"] = technical_score
    notes["technical_correctness"] = (
        "Incident and mapping uncertainty preserved."
        if technical_score == 2
        else "Manual review required for incident or mapping status."
    )

    # 3. MITRE relevance
    technique_id = str(row["technique_id"])
    technique_name = str(row["technique_name"]).lower()

    if technique_id == "N/A":
        mitre_relevant = (
            "t1110" in mitre
            and "candidate" in mitre
            and any(phrase in mitre for phrase in (
                "not a confirmed mapping",
                "not assigned",
                "without upgrading",
                "unconfirmed"
            ))
        )
    else:
        mitre_relevant = (
            technique_id.lower() in mitre
            and technique_name in mitre
        )

    mitre_score = 2 if mitre_relevant else 1
    scores["mitre_relevance"] = mitre_score
    notes["mitre_relevance"] = (
        "Original technique or candidate context handled appropriately."
        if mitre_relevant
        else "Review MITRE technique relevance and mapping language."
    )

    # 4. Investigation usefulness
    useful_terms = [
        "inspect", "review", "analyze", "analyse",
        "verify", "check", "determine"
    ]
    useful_count = sum(term in steps for term in useful_terms)

    investigation_score = 2 if useful_count >= 2 else (
        1 if useful_count == 1 else 0
    )
    scores["investigation_usefulness"] = investigation_score
    notes["investigation_usefulness"] = (
        f"Found {useful_count} investigation action keywords."
    )

    # 5. Clarity
    clarity_score = 2 if (
        len(str(row["ai_explanation"]).strip()) >= 50
        and len(str(row["limitations"]).strip()) >= 30
        and len(steps.strip()) >= 30
    ) else 1

    scores["clarity"] = clarity_score
    notes["clarity"] = (
        "Required explanation, steps and limitations are present."
        if clarity_score == 2
        else "One or more explanation fields need review."
    )

    return scores, notes


def main():
    with open(CRITERIA_FILE, encoding="utf-8-sig") as file:
        criteria = json.load(file)

    with open(DATASET_FILE, encoding="utf-8-sig") as file:
        dataset = json.load(file)

    investigations = pd.read_csv(
        INVESTIGATION_FILE, keep_default_na=False
    )

    ground_truth = {
        case["meta_alert_id"]: case
        for case in dataset["evaluation_cases"]
    }

    if len(investigations) != len(ground_truth):
        raise ValueError(
            "Investigation count does not match ground-truth test cases."
        )

    results = []

    for _, row in investigations.iterrows():
        case_id = row["meta_alert_id"]

        if case_id not in ground_truth:
            raise ValueError(f"Missing ground truth for {case_id}")

        scores, notes = evaluate_case(row, ground_truth[case_id])

        total_score = sum(scores.values())

        result = {
            "meta_alert_id": case_id,
            **scores,
            "total_score": total_score,
            "maximum_score": criteria["maximum_score"],
            "percentage": round(
                total_score / criteria["maximum_score"] * 100, 2
            ),
            "evidence_review_note": notes["evidence_accuracy"],
            "technical_review_note": notes["technical_correctness"],
            "mitre_review_note": notes["mitre_relevance"],
            "investigation_review_note": notes["investigation_usefulness"],
            "clarity_review_note": notes["clarity"],
            "human_review_required": True
        }

        results.append(result)

    output = pd.DataFrame(results)
    output.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("=" * 60)
    print("DAY 29 - AI INVESTIGATION QUALITY EVALUATION")
    print("=" * 60)
    print(output[
        ["meta_alert_id", "total_score", "maximum_score", "percentage"]
    ].to_string(index=False))

    print("\nAverage score:", round(output["total_score"].mean(), 2))
    print("Average percentage:", round(output["percentage"].mean(), 2), "%")
    print("Human review required for all investigations.")
    print("\nReport saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
