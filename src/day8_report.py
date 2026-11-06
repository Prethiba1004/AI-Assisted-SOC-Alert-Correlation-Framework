import pandas as pd

# Load evaluation results
evaluation = pd.read_csv(
    "outputs/clusters/clustering_evaluation.csv"
)

# Load event-level comparison
comparison = pd.read_csv(
    "outputs/clusters/dbscan_hdbscan_comparison.csv"
)

# Generate report
report = []

report.append("DBSCAN VS HDBSCAN EXPERIMENTAL REPORT")
report.append("=" * 50)

report.append("\n1. DATASET INFORMATION")
report.append("Total synthetic security events: 4")
report.append("Feature extraction: Sentence-BERT")
report.append("Embedding dimensions: 384")

report.append("\n2. CLUSTERING EVALUATION")
report.append(evaluation.to_string(index=False))

report.append("\n3. EVENT-LEVEL COMPARISON")
report.append(comparison.to_string(index=False))

report.append("\n4. RESEARCH OBSERVATIONS")
report.append(
    "- DBSCAN identified one cluster containing two events."
)
report.append(
    "- HDBSCAN classified all four events as noise."
)
report.append(
    "- Both algorithms identified two events as noise in DBSCAN, "
    "while HDBSCAN identified all four as noise."
)
report.append(
    "- Silhouette Score was not applicable because neither "
    "algorithm produced at least two non-noise clusters."
)

report.append("\n5. RESEARCH LIMITATIONS")
report.append(
    "- The experiment uses only four synthetic security events."
)
report.append(
    "- Results are proof-of-concept observations."
)
report.append(
    "- Larger datasets and parameter experiments are required."
)
report.append(
    "- Noise events must be preserved for SOC analyst review."
)
report.append(
    "- Similarity or clustering does not prove a common incident."
)

report.append("\n6. CONCLUSION")
report.append(
    "DBSCAN and HDBSCAN demonstrated different clustering "
    "behaviour on the current Sentence-BERT embeddings. "
    "Further experiments with larger datasets are required "
    "before drawing general performance conclusions."
)

output_file = "outputs/reports/day8_clustering_comparison_report.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print("Day 8 experimental report created successfully.")
print("Saved to:", output_file)
