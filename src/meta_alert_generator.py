
import os
import pandas as pd

# ==========================================
# DAY 20: MITRE-ENRICHED META-ALERT GENERATOR
# ==========================================

CORRELATION_FILE = (
    "outputs/explanations/"
    "alert_correlation_explanations.csv"
)

MITRE_FILE = (
    "outputs/mitre/"
    "mitre_technique_mappings.csv"
)

OUTPUT_DIR = "outputs/meta_alerts"

CSV_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "mitre_enriched_meta_alerts.csv"
)

TEXT_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "mitre_enriched_meta_alerts.txt"
)


def generate_investigation_note(row):
    """Generate an investigation note based on mapping status."""

    status = row["mapping_status"]

    if status == "Potential event-level mapping":
        return (
            "Validate the PowerShell command line, process ancestry, "
            "and available execution logs. Confirm whether the two "
            "events are genuinely related before treating them as "
            "one incident."
        )

    elif status == "Insufficient evidence":
        return (
            "Review authentication history, source IP, affected "
            "accounts, and repeated failure patterns. Additional "
            "evidence is required before assigning a MITRE technique."
        )

    return (
        "Review the available event evidence and validate the "
        "technique mapping with a SOC analyst."
    )


def main():

    print("\nDAY 20: MITRE-ENRICHED META-ALERT GENERATION")
    print("=" * 55)

    # Step 1: Validate input files
    if not os.path.exists(CORRELATION_FILE):
        raise FileNotFoundError(CORRELATION_FILE)

    if not os.path.exists(MITRE_FILE):
        raise FileNotFoundError(MITRE_FILE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 2: Read input CSV files
    correlations = pd.read_csv(
        CORRELATION_FILE,
        keep_default_na=False
    )

    mappings = pd.read_csv(
        MITRE_FILE,
        keep_default_na=False
    )

    # Step 3: Validate required columns
    required_correlation = [
        "event_1",
        "event_2",
        "description_1",
        "description_2",
        "hybrid_similarity",
        "evidence",
        "selection_status"
    ]

    required_mapping = [
        "event_1",
        "event_2",
        "technique_id",
        "technique_name",
        "tactic",
        "mapping_status",
        "evidence",
        "reason",
        "mitre_url"
    ]

    for column in required_correlation:
        if column not in correlations.columns:
            raise ValueError(
                f"Missing correlation column: {column}"
            )

    for column in required_mapping:
        if column not in mappings.columns:
            raise ValueError(
                f"Missing MITRE column: {column}"
            )

    # Step 4: Check duplicate event pairs
    pair_columns = ["event_1", "event_2"]

    if correlations.duplicated(pair_columns).any():
        raise ValueError(
            "Duplicate event pairs found in Day 18 data."
        )

    if mappings.duplicated(pair_columns).any():
        raise ValueError(
            "Duplicate event pairs found in Day 19 data."
        )

    # Step 5: Merge correlation and MITRE information
    merged = correlations.merge(
        mappings,
        on=pair_columns,
        how="left",
        suffixes=("_correlation", "_mitre"),
        validate="one_to_one",
        indicator=True
    )

    if not (merged["_merge"] == "both").all():
        raise ValueError(
            "Some correlation pairs have no matching MITRE record."
        )

    merged = merged.drop(columns=["_merge"])

    # Step 6: Generate meta-alert records
    meta_alerts = []

    for index, row in merged.iterrows():

        description_1 = row["description_1_correlation"]
        description_2 = row["description_2_correlation"]

        meta_alert = {
            "meta_alert_id": f"META-{index + 1:03d}",
            "event_1": row["event_1"],
            "event_2": row["event_2"],

            "alert_summary": (
                f"{description_1} + {description_2}"
            ),

            "description_1": description_1,
            "description_2": description_2,

            "hybrid_similarity": row["hybrid_similarity"],

            "correlation_evidence": (
                row["evidence_correlation"]
            ),

            "correlation_status": (
                row["selection_status"]
            ),

            "technique_id": row["technique_id"],
            "technique_name": row["technique_name"],
            "tactic": row["tactic"],
            "mapping_status": row["mapping_status"],

            "mitre_evidence": row["evidence_mitre"],
            "mapping_reason": row["reason"],
            "mitre_url": row["mitre_url"],

            "investigation_note": (
                generate_investigation_note(row)
            ),

            "incident_confirmation": "Not confirmed"
        }

        meta_alerts.append(meta_alert)

    result = pd.DataFrame(meta_alerts)

    # Step 7: Export CSV
    result.to_csv(
        CSV_OUTPUT,
        index=False
    )

    # Step 8: Export readable text report
    with open(
        TEXT_OUTPUT,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "DAY 20: MITRE-ENRICHED META-ALERT REPORT\n"
        )

        report.write("=" * 60 + "\n\n")

        report.write(
            f"Total meta-alerts generated: {len(result)}\n"
        )

        report.write(
            "Incident confirmation: None confirmed\n\n"
        )

        for _, row in result.iterrows():

            report.write("-" * 60 + "\n")

            for column, value in row.items():
                report.write(
                    f"{column}: {value}\n"
                )

            report.write("\n")

    # Step 9: Display results
    print("Total correlation pairs:", len(correlations))
    print("Total MITRE mappings:", len(mappings))
    print("Meta-alerts generated:", len(result))

    print("\nMapping status summary:")

    print(
        result["mapping_status"].value_counts().to_string()
    )

    print("\nCSV saved:", CSV_OUTPUT)
    print("Text report saved:", TEXT_OUTPUT)

    print("\nDay 20 meta-alert generation completed.")


if __name__ == "__main__":
    main()
