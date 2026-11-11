import pandas as pd
import numpy as np
from itertools import combinations
from pathlib import Path

print("Day 14: Similarity Weighting and Threshold Testing")
print("Required libraries imported successfully.")

# Define experimental weight combinations
weight_configs = {
    "A_80_20": {"semantic": 0.80, "graph": 0.20},
    "B_60_40": {"semantic": 0.60, "graph": 0.40},
    "C_50_50": {"semantic": 0.50, "graph": 0.50},
    "D_40_60": {"semantic": 0.40, "graph": 0.60},
    "E_20_80": {"semantic": 0.20, "graph": 0.80}
}

print("\nWeight configurations:")
for name, weights in weight_configs.items():
    print(
        name,
        "Semantic:", weights["semantic"],
        "Graph:", weights["graph"]
    )

# Load Day 13 similarity matrices
output_dir = Path("outputs/similarity")

semantic_matrix = pd.read_csv(
    output_dir / "semantic_similarity_matrix.csv",
    index_col=0
)

graph_matrix = pd.read_csv(
    output_dir / "graph_similarity_matrix.csv",
    index_col=0
)

# Validate matrices
if semantic_matrix.shape != graph_matrix.shape:
    raise ValueError("Matrix dimensions do not match.")

if list(semantic_matrix.index) != list(graph_matrix.index):
    raise ValueError("Event IDs do not match.")

if semantic_matrix.isnull().values.any() or graph_matrix.isnull().values.any():
    raise ValueError("Missing values detected in similarity matrices.")

print("\nMatrix validation successful.")
print("Semantic matrix shape:", semantic_matrix.shape)
print("Graph matrix shape:", graph_matrix.shape)
print("Total events:", len(semantic_matrix))

# Calculate hybrid similarity for all five configurations
weight_results = []

event_ids = semantic_matrix.index.tolist()

for config_name, weights in weight_configs.items():

    hybrid_matrix = (
        weights["semantic"] * semantic_matrix +
        weights["graph"] * graph_matrix
    )

    # Extract unique event pairs, excluding self-comparisons
    for event_a, event_b in combinations(event_ids, 2):

        score = hybrid_matrix.loc[event_a, str(event_b)]

        weight_results.append({
            "event_1": event_a,
            "event_2": event_b,
            "experiment": config_name,
            "semantic_weight": weights["semantic"],
            "graph_weight": weights["graph"],
            "hybrid_score": round(float(score), 4)
        })

print("\nHybrid weight calculations completed.")
print("Total pair-score calculations:", len(weight_results))
print("Total experiments:", len(weight_configs))

# Save weight comparison results
weight_df = pd.DataFrame(weight_results)

weight_pivot = weight_df.pivot(
    index=["event_1", "event_2"],
    columns="experiment",
    values="hybrid_score"
).reset_index()

weight_pivot.columns.name = None

weight_file = output_dir / "weight_comparison.csv"
weight_pivot.to_csv(weight_file, index=False)

print("\nWeight comparison saved successfully.")
print("File:", weight_file)
print("\nWeight comparison results:")
print(weight_pivot.to_string(index=False))

# Define experimental thresholds
thresholds = [0.30, 0.40, 0.50, 0.60, 0.70]

print("\nThreshold configurations:")
for threshold in thresholds:
    print("Threshold:", threshold)

# Perform threshold comparison experiments
threshold_results = []

for config_name in weight_configs:

    for threshold in thresholds:

        candidate_pairs = []

        for _, row in weight_pivot.iterrows():

            score = row[config_name]

            if score >= threshold:
                candidate_pairs.append(
                    f"{int(row['event_1'])}-{int(row['event_2'])}"
                )

        threshold_results.append({
            "experiment": config_name,
            "threshold": threshold,
            "candidate_pair_count": len(candidate_pairs),
            "candidate_pairs": ", ".join(candidate_pairs) if candidate_pairs else "No candidate pairs"
        })

print("\nThreshold experiments completed.")
print("Total threshold experiments:", len(threshold_results))

# Save threshold comparison results
threshold_df = pd.DataFrame(threshold_results)

threshold_file = output_dir / "threshold_comparison.csv"

threshold_df.to_csv(threshold_file, index=False)

print("\nThreshold comparison saved successfully.")
print("File:", threshold_file)
print("\nThreshold comparison results:")
print(threshold_df.to_string(index=False))

# Generate Day 14 experiment report
report_dir = Path("outputs/reports")
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / "day14_experiment_report.txt"

report_lines = [
    "DAY 14: SIMILARITY WEIGHTING AND THRESHOLD TESTING",
    "=" * 60,
    "",
    "OBJECTIVE",
    "Evaluate how different semantic and graph similarity weights",
    "affect event-pair scores and threshold-based candidate selection.",
    "",
    "DATASET",
    "Total events: 4",
    "Unique event pairs: 6",
    "Weight configurations: 5",
    "Threshold values: 0.30, 0.40, 0.50, 0.60, 0.70",
    "Total weight-threshold experiments: 25",
    "",
    "WEIGHT CONFIGURATIONS",
]

for name, weights in weight_configs.items():
    report_lines.append(
        f"{name}: Semantic={weights['semantic']:.0%}, "
        f"Graph={weights['graph']:.0%}"
    )

report_lines.extend([
    "",
    "HIGHEST SCORING EVENT PAIR PER CONFIGURATION",
])

for config_name in weight_configs:
    best_row = weight_pivot.loc[weight_pivot[config_name].idxmax()]
    report_lines.append(
        f"{config_name}: Event pair {int(best_row['event_1'])}-"
        f"{int(best_row['event_2'])}, score={best_row[config_name]:.4f}"
    )

report_lines.extend([
    "",
    "THRESHOLD EXPERIMENT RESULTS",
])

for config_name in weight_configs:
    report_lines.append(f"\n{config_name}:")
    config_results = threshold_df[
        threshold_df["experiment"] == config_name
    ]

    for _, row in config_results.iterrows():
        report_lines.append(
            f"Threshold {row['threshold']:.2f}: "
            f"{row['candidate_pair_count']} candidate pairs"
        )

report_lines.extend([
    "",
    "KEY OBSERVATIONS",
    "1. Semantic-heavy weighting gives greater influence to text meaning.",
    "2. Graph-heavy weighting gives greater influence to graph relationships.",
    "3. Event pair 1-2 has the highest score in configuration A_80_20.",
    "4. Event pair 0-2 has the highest score in configuration E_20_80.",
    "5. Candidate counts change when weights and thresholds change.",
    "",
    "METHODOLOGICAL LIMITATIONS",
    "1. The dataset contains only four synthetic events.",
    "2. The weight values and thresholds are experimental choices.",
    "3. No ground-truth incident labels are available for validation.",
    "4. A high similarity score does not prove a shared security incident.",
    "5. Accuracy, precision, recall, and production performance have not",
    "   been established by these experiments.",
    "",
    "OUTPUT FILES",
    "outputs/similarity/weight_comparison.csv",
    "outputs/similarity/threshold_comparison.csv",
    "outputs/reports/day14_experiment_report.txt",
    "",
    "CONCLUSION",
    "Day 14 completed the experimental comparison of five hybrid",
    "similarity weighting configurations across five thresholds.",
    "The results provide a basis for selecting candidate settings",
    "for further testing with a larger labelled dataset.",
])

report_file.write_text("\n".join(report_lines), encoding="utf-8")

print("\nDay 14 report generated successfully.")
print("Report:", report_file)


