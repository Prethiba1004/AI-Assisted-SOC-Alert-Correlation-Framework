
import json
from pathlib import Path

import pandas as pd


ORIGINAL_FILE = Path(
    "outputs/meta_alerts/mitre_enriched_meta_alerts.csv"
)

RAG_OUTPUT_FILE = Path(
    "outputs/soc_investigations/rag_meta_alert_investigation.csv"
)

REQUIRED_FIELDS = [
    "ai_explanation",
    "evidence_analysis",
    "mitre_analysis",
    "investigation_steps",
    "limitations",
    "ai_incident_assessment"
]


def main():

    print("=" * 65)
    print("RAG SOC INVESTIGATION VALIDATION")
    print("=" * 65)

    original = pd.read_csv(
        ORIGINAL_FILE,
        keep_default_na=False
    )

    generated = pd.read_csv(
        RAG_OUTPUT_FILE,
        keep_default_na=False
    )

    checks = []

    # 1. Meta-alert count
    checks.append((
        "Meta-alert count",
        len(original) == len(generated)
    ))

    # 2. Duplicate IDs
    duplicate_valid = (
        not original["meta_alert_id"].duplicated().any()
        and not generated["meta_alert_id"].duplicated().any()
    )

    checks.append(("Duplicate IDs", duplicate_valid))

    # 3. Meta-alert ID consistency
    ids_valid = (
        set(original["meta_alert_id"])
        == set(generated["meta_alert_id"])
    )

    checks.append(("Meta-alert ID consistency", ids_valid))

    # 4. Required AI fields
    fields_exist = all(
        field in generated.columns
        for field in REQUIRED_FIELDS
    )

    checks.append(("Six AI fields present", fields_exist))

    # 5. Successful AI analysis
    status_valid = (
        "analysis_status" in generated.columns
        and (generated["analysis_status"] == "Success").all()
    )

    checks.append(("All analyses successful", status_valid))

    # 6. Retrieval status
    retrieval_valid = (
        "retrieval_status" in generated.columns
        and (generated["retrieval_status"] == "Success").all()
    )

    checks.append(("All retrievals successful", retrieval_valid))

    # 7. Retrieved chunk count
    chunk_valid = (
        "retrieved_chunk_count" in generated.columns
        and pd.to_numeric(
            generated["retrieved_chunk_count"],
            errors="coerce"
        ).gt(0).all()
    )

    checks.append(("Retrieved chunks available", chunk_valid))

    # 8. Retrieved context JSON
    context_valid = False

    if "retrieved_context" in generated.columns:

        context_valid = True

        for context in generated["retrieved_context"]:

            try:
                parsed = json.loads(context)

                if not isinstance(parsed, list) or not parsed:
                    context_valid = False
                    break

            except (json.JSONDecodeError, TypeError):
                context_valid = False
                break

    checks.append(("Retrieved context valid JSON", context_valid))

    # 9. Original evidence preservation
    evidence_valid = False

    if ids_valid:

        original_index = original.set_index("meta_alert_id")
        generated_index = generated.set_index("meta_alert_id")

        evidence_fields = [
            "technique_id",
            "technique_name",
            "mapping_status",
            "incident_confirmation"
        ]

        evidence_valid = all(
            field in original_index.columns
            and field in generated_index.columns
            and (
                original_index[field].astype(str)
                == generated_index[field].astype(str)
            ).all()
            for field in evidence_fields
        )

    checks.append((
        "Original MITRE and incident evidence preserved",
        evidence_valid
    ))

    # 10. Original incident confirmation preserved
    incident_valid = (
        "incident_confirmation" in generated.columns
        and "original_incident_confirmation" in generated.columns
        and (
            generated["incident_confirmation"].astype(str)
            == generated["original_incident_confirmation"].astype(str)
        ).all()
    )

    checks.append((
        "Original incident confirmation unchanged",
        incident_valid
    ))

    # 11. No empty AI fields
    missing_valid = False

    if fields_exist:

        missing_valid = (
            generated[REQUIRED_FIELDS]
            .apply(lambda column: column.str.strip().ne(""))
            .all()
            .all()
        )

    checks.append(("No empty AI analysis fields", missing_valid))

    # 12. No recorded processing errors
    error_valid = (
        "error" not in generated.columns
        or generated["error"].fillna("").astype(str).str.strip().eq("").all()
    )

    checks.append(("No processing errors recorded", error_valid))

    # Display results
    print("\nVALIDATION RESULTS\n")

    for name, passed in checks:

        status = "PASS" if passed else "FAIL"

        print(f"{name}: {status}")

    passed_count = sum(
        passed for _, passed in checks
    )

    failed_count = len(checks) - passed_count

    print("\n" + "=" * 65)

    print(f"Total checks: {len(checks)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    if failed_count == 0:

        print("\nFINAL RESULT: ALL VALIDATION CHECKS PASSED")

    else:

        print("\nFINAL RESULT: REVIEW FAILED CHECKS")

    print("=" * 65)


if __name__ == "__main__":
    main()
