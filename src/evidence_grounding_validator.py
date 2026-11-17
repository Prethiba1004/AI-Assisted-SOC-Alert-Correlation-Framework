import re
from pathlib import Path

import pandas as pd


ORIGINAL_FILE = Path(
    "outputs/meta_alerts/mitre_enriched_meta_alerts.csv"
)

RAG_OUTPUT_FILE = Path(
    "outputs/soc_investigations/rag_meta_alert_investigation.csv"
)

REPORT_FILE = Path(
    "outputs/soc_investigations/evidence_grounding_validation.csv"
)


SOURCE_FIELDS = [
    "alert_summary",
    "description_1",
    "description_2",
    "correlation_evidence",
    "mitre_evidence",
    "mapping_reason",
    "investigation_note"
]


def extract_ips(text):
    """Extract IPv4-looking addresses from source evidence."""
    return re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        str(text)
    )


def main():

    print("=" * 65)
    print("SOC AI EVIDENCE GROUNDING VALIDATION")
    print("=" * 65)

    original = pd.read_csv(
        ORIGINAL_FILE,
        keep_default_na=False
    )

    generated = pd.read_csv(
        RAG_OUTPUT_FILE,
        keep_default_na=False
    )

    original_index = original.set_index("meta_alert_id")
    generated_index = generated.set_index("meta_alert_id")

    results = []

    for meta_alert_id in original_index.index:

        checks = {}

        if meta_alert_id not in generated_index.index:
            print(f"\n{meta_alert_id}: MISSING FROM RAG OUTPUT")
            continue

        source = original_index.loc[meta_alert_id]
        ai = generated_index.loc[meta_alert_id]

        # 1. Incident status preservation
        checks["incident_status_preserved"] = (
            str(source["incident_confirmation"])
            == str(ai["incident_confirmation"])
            == str(ai["original_incident_confirmation"])
        )

        # 2. Original MITRE mapping preservation
        checks["technique_id_preserved"] = (
            str(source["technique_id"])
            == str(ai["technique_id"])
        )

        checks["mapping_status_preserved"] = (
            str(source["mapping_status"])
            == str(ai["mapping_status"])
        )

        # 3. Original IP traceability
        source_text = " ".join(
            str(source[field])
            for field in SOURCE_FIELDS
            if field in source.index
        )

        original_ips = sorted(set(extract_ips(source_text)))

        ai_evidence = str(ai.get("evidence_analysis", ""))

        if original_ips:
            ip_traceable = all(
                ip in ai_evidence
                for ip in original_ips
            )
        else:
            ip_traceable = True

        checks["original_ip_traceable"] = ip_traceable

        # 4. Required evidence analysis available
        checks["evidence_analysis_available"] = (
            bool(ai_evidence.strip())
        )

        passed = sum(checks.values())
        total = len(checks)

        result = {
            "meta_alert_id": meta_alert_id,
            "original_ips": ", ".join(original_ips) if original_ips else "N/A",
            **checks,
            "passed_checks": passed,
            "total_checks": total,
            "result": "PASS" if passed == total else "FAIL"
        }

        results.append(result)

        print(f"\n{meta_alert_id}")

        for name, status in checks.items():
            print(f"{name}: {'PASS' if status else 'FAIL'}")

        print(f"Result: {result['result']} ({passed}/{total})")

    report = pd.DataFrame(results)

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        REPORT_FILE,
        index=False
    )

    print("\n" + "=" * 65)
    print("EVIDENCE GROUNDING SUMMARY")
    print("=" * 65)

    print(f"Meta-alerts checked: {len(report)}")

    if not report.empty:
        print(f"Passed: {(report['result'] == 'PASS').sum()}")
        print(f"Failed: {(report['result'] == 'FAIL').sum()}")

        if (report["result"] == "PASS").all():
            print("\nFINAL RESULT: ALL EVIDENCE GROUNDING CHECKS PASSED")
        else:
            print("\nFINAL RESULT: REVIEW FAILED CHECKS")

    print(f"\nReport saved: {REPORT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    main()