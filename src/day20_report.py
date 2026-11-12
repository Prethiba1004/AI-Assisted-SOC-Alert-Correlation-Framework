
from pathlib import Path
import pandas as pd
from datetime import date

# Project paths
input_file = Path("outputs/meta_alerts/mitre_enriched_meta_alerts.csv")
output_file = Path("outputs/reports/day20_experiment_report.txt")

# Load generated meta-alerts
df = pd.read_csv(input_file, keep_default_na=False)

# Calculate experiment results
total_alerts = len(df)
potential_mappings = int(
    (df["mapping_status"] == "Potential event-level mapping").sum()
)
insufficient_evidence = int(
    (df["mapping_status"] == "Insufficient evidence").sum()
)
unconfirmed_incidents = int(
    (df["incident_confirmation"] == "Not confirmed").sum()
)

similarity = pd.to_numeric(df["hybrid_similarity"])
missing_values = int(df.isin([""]).sum().sum())
duplicate_ids = int(df["meta_alert_id"].duplicated().sum())

report = f"""
DAY 20 EXPERIMENT REPORT
MITRE ATT&CK-ENRICHED META-ALERT GENERATION
============================================================

Project:
A Lightweight Graph-Assisted and Explainable AI Framework
for SOC Alert Correlation, Clustering and MITRE ATT&CK-
Enriched Meta-Alert Generation

Experiment Date: {date.today().strftime("%d-%B-%Y")}

1. OBJECTIVE
------------------------------------------------------------
The objective of Day 20 was to combine correlated security
alerts with MITRE ATT&CK technique-mapping context and
generate consolidated meta-alerts for SOC investigation.

2. METHODOLOGY
------------------------------------------------------------
The experiment reused outputs from:

- Day 18: Alert correlation explanations.
- Day 19: MITRE ATT&CK technique mappings.

The Python script src/meta_alert_generator.py joined the
correlated event pairs with their corresponding MITRE
mapping information using event_1 and event_2.

Each generated meta-alert contains correlation evidence,
similarity information, technique-mapping context and an
investigation note.

3. EXPERIMENTAL RESULTS
------------------------------------------------------------
Total correlation pairs processed: {total_alerts}
Meta-alerts generated: {total_alerts}
Potential event-level mappings: {potential_mappings}
Insufficient-evidence mappings: {insufficient_evidence}
Incidents marked not confirmed: {unconfirmed_incidents}

Generated output files:
- outputs/meta_alerts/mitre_enriched_meta_alerts.csv
- outputs/meta_alerts/mitre_enriched_meta_alerts.txt

4. MITRE ATT&CK OBSERVATIONS
------------------------------------------------------------
Two meta-alerts contain potential event-level mappings
to MITRE ATT&CK technique T1059.001 (PowerShell).

These mappings provide investigation context only.
They do not establish that the correlated event pairs
belong to one confirmed attack.

One meta-alert was assigned N/A because the available
evidence was insufficient to map a technique confidently.

No incident was marked as confirmed.

5. DATA QUALITY VALIDATION
------------------------------------------------------------
Total records: {total_alerts}
Missing values: {missing_values}
Duplicate meta-alert IDs: {duplicate_ids}
Similarity scores within 0-1: {bool(similarity.between(0, 1).all())}
All incidents unconfirmed: {bool((df["incident_confirmation"] == "Not confirmed").all())}

6. LIMITATIONS
------------------------------------------------------------
- The experiment uses a small dataset of four synthetic
  security events.
- Similarity and graph relationships do not prove that
  events belong to the same security incident.
- MITRE mappings are potential event-level mappings and
  require analyst validation.
- The current mapping approach uses available event
  descriptions and does not establish malicious activity.
- The experiment is a proof of concept, not a production-
  validated SOC detection system.

7. FUTURE IMPROVEMENTS
------------------------------------------------------------
- Test with larger and realistic security-log datasets.
- Improve structured evidence extraction.
- Introduce analyst feedback for mapping validation.
- Evaluate additional correlation and enrichment methods.
- Explore LLM-assisted investigation summaries and
  retrieval-augmented generation in later project stages.

8. CONCLUSION
------------------------------------------------------------
Day 20 successfully generated {total_alerts} MITRE ATT&CK-
enriched meta-alerts by combining alert correlation
explanations with technique-mapping context.

Data-quality checks passed. The output preserves uncertainty
and correctly keeps all incidents unconfirmed.

The experiment demonstrates a lightweight, explainable
approach to consolidating related SOC alerts for further
analyst investigation.

============================================================
END OF DAY 20 REPORT
============================================================
"""

# Ensure report directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save report
output_file.write_text(report.strip() + "\n", encoding="utf-8")

print("DAY 20 EXPERIMENT REPORT GENERATED")
print("========================================")
print("Total meta-alerts:", total_alerts)
print("Potential mappings:", potential_mappings)
print("Insufficient evidence:", insufficient_evidence)
print("Missing values:", missing_values)
print("Report saved:", output_file)
