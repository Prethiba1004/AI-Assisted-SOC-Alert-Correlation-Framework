
import pandas as pd
from pathlib import Path

# Input file from Day 18
input_file = Path(
    "outputs/explanations/alert_correlation_explanations.csv"
)

# Output directory
output_dir = Path("outputs/mitre")
output_dir.mkdir(parents=True, exist_ok=True)

# Read correlated alert pairs
df = pd.read_csv(input_file)

results = []

for _, row in df.iterrows():

    event_1 = row["event_1"]
    event_2 = row["event_2"]

    desc_1 = str(row["description_1"])
    desc_2 = str(row["description_2"])

    descriptions = f"{desc_1} {desc_2}".lower()

    technique_id = "N/A"
    technique_name = "No confirmed technique"
    tactic = "N/A"
    mapping_status = "Insufficient evidence"
    evidence = descriptions
    reason = (
        "Available event descriptions do not establish "
        "a specific ATT&CK technique."
    )
    mitre_url = "N/A"

    # Potential PowerShell execution mapping
    if "powershell" in descriptions:

        technique_id = "T1059.001"
        technique_name = "PowerShell"
        tactic = "Execution"
        mapping_status = "Potential event-level mapping"

        evidence = "PowerShell process created"

        reason = (
            "PowerShell process creation is relevant to "
            "T1059.001, but process creation alone does "
            "not prove malicious execution. Pair linkage "
            "also requires analyst validation."
        )

        mitre_url = (
            "https://attack.mitre.org/techniques/T1059/001/"
        )

    # Do not automatically map one failed login to brute force
    elif (
        "failed password" in descriptions
        or "failed logon" in descriptions
    ):

        reason = (
            "Authentication failure was observed, but the "
            "available evidence does not establish repeated "
            "or systematic password guessing. T1110 is "
            "therefore not assigned."
        )

    results.append({
        "event_1": event_1,
        "event_2": event_2,
        "description_1": desc_1,
        "description_2": desc_2,
        "technique_id": technique_id,
        "technique_name": technique_name,
        "tactic": tactic,
        "mapping_status": mapping_status,
        "evidence": evidence,
        "reason": reason,
        "mitre_url": mitre_url
    })

# Create mapping DataFrame
mapping_df = pd.DataFrame(results)

# Save CSV
csv_file = output_dir / "mitre_technique_mappings.csv"
mapping_df.to_csv(csv_file, index=False)

# Generate text summary
txt_file = output_dir / "mitre_technique_mappings.txt"

with open(txt_file, "w", encoding="utf-8") as file:

    file.write("DAY 19: MITRE ATT&CK TECHNIQUE MAPPING\n")
    file.write("=" * 55 + "\n\n")

    file.write(f"Total correlated pairs: {len(mapping_df)}\n")
    file.write(
        "Potential technique mappings: "
        f"{(mapping_df['technique_id'] != 'N/A').sum()}\n\n"
    )

    for _, row in mapping_df.iterrows():

        file.write(
            f"Event Pair: {row['event_1']} - {row['event_2']}\n"
        )
        file.write(
            f"Descriptions: {row['description_1']} | "
            f"{row['description_2']}\n"
        )
        file.write(
            f"Technique: {row['technique_id']} - "
            f"{row['technique_name']}\n"
        )
        file.write(f"Tactic: {row['tactic']}\n")
        file.write(f"Status: {row['mapping_status']}\n")
        file.write(f"Evidence: {row['evidence']}\n")
        file.write(f"Reason: {row['reason']}\n")
        file.write(f"MITRE URL: {row['mitre_url']}\n")
        file.write("-" * 55 + "\n")

print("DAY 19: MITRE ATT&CK MAPPING COMPLETED")
print("=" * 55)
print("Total correlated pairs:", len(mapping_df))
print(
    "Potential mappings:",
    (mapping_df["technique_id"] != "N/A").sum()
)
print("CSV saved:", csv_file)
print("Text report saved:", txt_file)
