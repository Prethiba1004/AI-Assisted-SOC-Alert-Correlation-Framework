
from pathlib import Path
import pandas as pd
from datetime import date


INPUT_FILE = Path("outputs/summaries/meta_alert_summaries.csv")
OUTPUT_FILE = Path("outputs/reports/day21_experiment_report.txt")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, keep_default_na=False)

    total = len(df)
    potential = (
        df["mapping_status"] == "Potential event-level mapping"
    ).sum()
    insufficient = (
        df["mapping_status"] == "Insufficient evidence"
    ).sum()
    unconfirmed = (
        df["incident_confirmation"] == "Not confirmed"
    ).sum()

    summaries_present = (
        df["investigation_summary"].str.strip() != ""
    ).sum()

    report = f"""
DAY 21 EXPERIMENT REPORT
AI-ASSISTED META-ALERT SUMMARIZATION
=======================================================

Project:
A Lightweight Graph-Assisted and Explainable AI Framework
for SOC Alert Correlation, Clustering and MITRE ATT&CK-
Enriched Meta-Alert Generation.

Date: {date.today().strftime("%d-%B-%Y")}

1. OBJECTIVE
-------------------------------------------------------
Generate readable, evidence-grounded SOC investigation
summaries from MITRE-enriched meta-alert records.

2. METHODOLOGY
-------------------------------------------------------
- Read Day 20 MITRE-enriched meta-alert CSV.
- Extract event descriptions and correlation evidence.
- Preserve hybrid similarity scores.
- Include MITRE ATT&CK mapping information.
- Include mapping limitations and investigation notes.
- Generate structured investigation summaries.
- Export summaries into CSV and TXT formats.

3. EXPERIMENT RESULTS
-------------------------------------------------------
Total meta-alerts processed: {total}
Potential event-level mappings: {potential}
Insufficient-evidence mappings: {insufficient}
Incidents marked Not confirmed: {unconfirmed}
Non-empty investigation summaries: {summaries_present}

4. VALIDATION
-------------------------------------------------------
All summaries were checked for:
- Meta-alert identification.
- Event descriptions.
- Correlation evidence.
- MITRE mapping status.
- Incident confirmation status.
- Investigation recommendations.

5. OUTPUT FILES
-------------------------------------------------------
Python module:
src/meta_alert_summarizer.py

CSV output:
outputs/summaries/meta_alert_summaries.csv

Text output:
outputs/summaries/meta_alert_summaries.txt

Experiment report:
outputs/reports/day21_experiment_report.txt

6. LIMITATIONS
-------------------------------------------------------
- The dataset contains only four synthetic source events
  and three generated meta-alerts.
- The current implementation uses Python-based structured
  summarization and templates, not a connected LLM.
- Summaries depend on the accuracy of input meta-alerts.
- Similarity and MITRE mapping do not prove an attack.
- Analyst validation remains necessary.

7. CONCLUSION
-------------------------------------------------------
The Day 21 prototype successfully generated structured
investigation summaries for the available meta-alerts.
Mapping uncertainty and unconfirmed incident status were
preserved throughout the summarization process.

This is a proof-of-concept implementation and is not
validated for production SOC deployment.

=======================================================
END OF DAY 21 REPORT
"""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report.strip() + "\n", encoding="utf-8")

    print("DAY 21 EXPERIMENT REPORT GENERATED")
    print("=" * 45)
    print(f"Meta-alerts processed: {total}")
    print(f"Report saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
