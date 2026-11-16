
import pandas as pd
from pathlib import Path


INPUT_FILE = Path("outputs/meta_alerts/mitre_enriched_meta_alerts.csv")
OUTPUT_DIR = Path("outputs/summaries")

OUTPUT_CSV = OUTPUT_DIR / "meta_alert_summaries.csv"
OUTPUT_TXT = OUTPUT_DIR / "meta_alert_summaries.txt"


def generate_summary(alert):
    alert_id = alert["meta_alert_id"]

    event_1 = alert["description_1"]
    event_2 = alert["description_2"]

    similarity = alert["hybrid_similarity"]
    evidence = alert["correlation_evidence"]

    technique_id = alert["technique_id"]
    technique_name = alert["technique_name"]
    tactic = alert["tactic"]

    mapping_status = alert["mapping_status"]
    mapping_reason = alert["mapping_reason"]
    investigation_note = alert["investigation_note"]

    incident_status = alert["incident_confirmation"]

    if technique_id and technique_id != "N/A":
        mitre_details = (
            f"Potential MITRE ATT&CK mapping: "
            f"{technique_id} ({technique_name}), "
            f"associated with the {tactic} tactic."
        )
    else:
        mitre_details = (
            "No specific MITRE ATT&CK technique "
            "could be assigned from the available evidence."
        )

    summary = (
        f"Meta-alert {alert_id} contains two correlated events: "
        f"{event_1} and {event_2}. "
        f"The hybrid similarity score is {similarity}. "
        f"Correlation evidence: {evidence}. "
        f"{mitre_details} "
        f"Mapping status: {mapping_status}. "
        f"Mapping limitation: {mapping_reason} "
        f"Incident status: {incident_status}. "
        f"Recommended investigation: {investigation_note}"
    )

    return summary


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE, keep_default_na=False)

    required_columns = [
        "meta_alert_id",
        "description_1",
        "description_2",
        "hybrid_similarity",
        "correlation_evidence",
        "technique_id",
        "technique_name",
        "tactic",
        "mapping_status",
        "mapping_reason",
        "investigation_note",
        "incident_confirmation",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["investigation_summary"] = df.apply(
        generate_summary, axis=1
    )

    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as file:
        file.write("DAY 21: AI-ASSISTED META-ALERT SUMMARIES\n")
        file.write("=" * 55 + "\n\n")

        for _, alert in df.iterrows():
            file.write(
                f"META-ALERT: {alert['meta_alert_id']}\n"
            )
            file.write("-" * 55 + "\n")
            file.write(
                alert["investigation_summary"] + "\n\n"
            )

    print("DAY 21 SUMMARIZATION COMPLETED")
    print("=" * 45)
    print(f"Total meta-alerts processed: {len(df)}")
    print(f"CSV saved: {OUTPUT_CSV}")
    print(f"Text report saved: {OUTPUT_TXT}")


if __name__ == "__main__":
    main()
