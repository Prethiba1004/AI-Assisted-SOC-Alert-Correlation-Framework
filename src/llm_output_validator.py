
import pandas as pd

INPUT_FILE = "outputs/meta_alerts/mitre_enriched_meta_alerts.csv"
LLM_OUTPUT_FILE = "outputs/llm_analysis/llm_meta_alert_analysis.csv"

REQUIRED_FIELDS = [
    "ai_explanation",
    "evidence_analysis",
    "mitre_analysis",
    "investigation_steps",
    "limitations",
    "ai_incident_assessment"
]


def main():
    print("=" * 55)
    print("SOC AI LLM OUTPUT VALIDATION")
    print("=" * 55)

    original = pd.read_csv(INPUT_FILE, keep_default_na=False)
    generated = pd.read_csv(LLM_OUTPUT_FILE, keep_default_na=False)

    checks = []

    checks.append(
        ("Meta-alert count", len(original) == len(generated))
    )

    duplicate_valid = (
        not original["meta_alert_id"].duplicated().any()
        and not generated["meta_alert_id"].duplicated().any()
    )
    checks.append(("Duplicate IDs", duplicate_valid))

    ids_valid = (
        set(original["meta_alert_id"])
        == set(generated["meta_alert_id"])
    )
    checks.append(("Meta-alert ID consistency", ids_valid))

    fields_exist = all(
        field in generated.columns
        for field in REQUIRED_FIELDS
    )
    checks.append(("Six AI fields present", fields_exist))

    status_valid = (
        "analysis_status" in generated.columns
        and (generated["analysis_status"] == "Success").all()
    )
    checks.append(("All analyses successful", status_valid))

    # Compare original and generated records by meta-alert ID.
    preserved_valid = False

    if ids_valid:
        original_index = original.set_index("meta_alert_id")
        generated_index = generated.set_index("meta_alert_id")

        technique_valid = (
            original_index["technique_id"].astype(str)
            == generated_index["technique_id"].astype(str)
        ).all()

        mapping_valid = (
            original_index["mapping_status"].astype(str)
            == generated_index["mapping_status"].astype(str)
        ).all()

        incident_valid = (
            original_index["incident_confirmation"].astype(str)
            == generated_index[
                "original_incident_confirmation"
            ].astype(str)
        ).all()

        preserved_valid = (
            technique_valid and mapping_valid and incident_valid
        )

    checks.append(
        ("Original MITRE and incident status preserved",
         preserved_valid)
    )

    missing_valid = False

    if fields_exist:
        missing_valid = (
            generated[REQUIRED_FIELDS]
            .apply(lambda column: column.str.strip().ne(""))
            .all()
            .all()
        )

    checks.append(("No empty AI analysis fields", missing_valid))

    print("\nVALIDATION RESULTS\n")

    for name, passed in checks:
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    passed_count = sum(passed for _, passed in checks)
    failed_count = len(checks) - passed_count

    print("\n" + "=" * 55)
    print(f"Total checks: {len(checks)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    if failed_count == 0:
        print("FINAL RESULT: ALL VALIDATION CHECKS PASSED")
    else:
        print("FINAL RESULT: REVIEW FAILED CHECKS")

    print("=" * 55)


if __name__ == "__main__":
    main()
