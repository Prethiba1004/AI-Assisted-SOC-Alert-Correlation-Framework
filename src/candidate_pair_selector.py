
import pandas as pd
from pathlib import Path

# Day 15: Candidate Pair Selection

print("Day 15: Similarity-Based Candidate Pair Selection")

# Selected experimental configuration
SEMANTIC_WEIGHT = 0.60
GRAPH_WEIGHT = 0.40
SIMILARITY_THRESHOLD = 0.40
CONFIG_NAME = "B_60_40"

# File paths
INPUT_FILE = Path("outputs/similarity/weight_comparison.csv")
OUTPUT_FILE = Path("outputs/similarity/candidate_pairs.csv")

# Load Day 14 similarity results
df = pd.read_csv(INPUT_FILE)

# Validate required columns
required_columns = ["event_1", "event_2", CONFIG_NAME]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

# Check missing values
if df[required_columns].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Select candidate pairs using threshold
candidates = df[df[CONFIG_NAME] >= SIMILARITY_THRESHOLD].copy()

# Prepare output
candidates = candidates.rename(
    columns={CONFIG_NAME: "similarity_score"}
)

candidates["semantic_weight"] = SEMANTIC_WEIGHT
candidates["graph_weight"] = GRAPH_WEIGHT
candidates["threshold"] = SIMILARITY_THRESHOLD
candidates["selection_status"] = "Selected"

# Keep required output columns
candidates = candidates[
    [
        "event_1",
        "event_2",
        "semantic_weight",
        "graph_weight",
        "similarity_score",
        "threshold",
        "selection_status"
    ]
]

# Validate duplicate pairs
if candidates.duplicated(subset=["event_1", "event_2"]).any():
    raise ValueError("Duplicate candidate pairs detected.")

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
candidates.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\nSelected Configuration:", CONFIG_NAME)
print("Semantic Weight:", SEMANTIC_WEIGHT)
print("Graph Weight:", GRAPH_WEIGHT)
print("Similarity Threshold:", SIMILARITY_THRESHOLD)

print("\nTotal Event Pairs:", len(df))
print("Selected Candidate Pairs:", len(candidates))

print("\nCandidate Pair Results:")
print(candidates.to_string(index=False))

print("\nOutput saved to:", OUTPUT_FILE)
print("\nDay 15 candidate selection completed successfully.")
