
import pandas as pd
from pathlib import Path

# ==========================================
# DAY 18: ALERT CORRELATION EXPLAINABILITY
# ==========================================

# 1. Define input and output paths

EVENT_FILE = Path("data/normalized/normalized_events.csv")
CANDIDATE_FILE = Path("outputs/similarity/candidate_pairs.csv")

SEMANTIC_FILE = Path(
    "outputs/similarity/semantic_similarity_matrix.csv"
)

GRAPH_FILE = Path(
    "outputs/similarity/graph_similarity_matrix.csv"
)

OUTPUT_DIR = Path("outputs/explanations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Define experimental weights

SEMANTIC_WEIGHT = 0.60
GRAPH_WEIGHT = 0.40

# 3. Validate input files

required_files = [
    EVENT_FILE,
    CANDIDATE_FILE,
    SEMANTIC_FILE,
    GRAPH_FILE
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required input file not found: {file_path}"
        )

# 4. Load datasets

events = pd.read_csv(EVENT_FILE)
candidates = pd.read_csv(CANDIDATE_FILE)

semantic_matrix = pd.read_csv(
    SEMANTIC_FILE, index_col=0
)

graph_matrix = pd.read_csv(
    GRAPH_FILE, index_col=0
)

# IMPORTANT:
# Convert matrix row and column labels to integers.
# This fixes the previous KeyError: '0'.

semantic_matrix.index = semantic_matrix.index.astype(int)
semantic_matrix.columns = semantic_matrix.columns.astype(int)

graph_matrix.index = graph_matrix.index.astype(int)
graph_matrix.columns = graph_matrix.columns.astype(int)

# 5. Validate dataset columns

required_event_columns = [
    "timestamp",
    "hostname",
    "username",
    "description"
]

required_candidate_columns = [
    "event_1",
    "event_2",
    "threshold",
    "similarity_score"
]

for column in required_event_columns:
    if column not in events.columns:
        raise ValueError(
            f"Missing event column: {column}"
        )

for column in required_candidate_columns:
    if column not in candidates.columns:
        raise ValueError(
            f"Missing candidate column: {column}"
        )

# 6. Create event lookup

events = events.reset_index(drop=True)

event_lookup = events.to_dict(orient="index")

# 7. Generate explanations

explanations = []

for _, pair in candidates.iterrows():

    event_a = int(pair["event_1"])
    event_b = int(pair["event_2"])

    threshold = float(pair["threshold"])
    original_score = float(pair["similarity_score"])

    # Check event IDs

    if event_a not in event_lookup:
        raise ValueError(f"Event {event_a} not found")

    if event_b not in event_lookup:
        raise ValueError(f"Event {event_b} not found")

    details_a = event_lookup[event_a]
    details_b = event_lookup[event_b]

    # Retrieve similarity scores using integer IDs

    semantic_score = float(
        semantic_matrix.loc[event_a, event_b]
    )

    graph_score = float(
        graph_matrix.loc[event_a, event_b]
    )

    # Calculate hybrid similarity

    hybrid_score = (
        SEMANTIC_WEIGHT * semantic_score
        + GRAPH_WEIGHT * graph_score
    )

    # Identify correlation evidence

    evidence = []

    evidence.append(
        "Semantic similarity detected"
    )

    if graph_score > 0:
        evidence.append(
            "Direct graph relationship detected"
        )
    else:
        evidence.append(
            "No direct graph edge detected"
        )

    # Hostname comparison

    if details_a["hostname"] == details_b["hostname"]:
        evidence.append("Same hostname")
    else:
        evidence.append("Different hostnames")

    # Username comparison

    if details_a["username"] == details_b["username"]:
        evidence.append("Same username")
    else:
        evidence.append("Different usernames")

    # Calculate timestamp difference

    time_a = pd.to_datetime(
        details_a["timestamp"],
        utc=True
    )

    time_b = pd.to_datetime(
        details_b["timestamp"],
        utc=True
    )

    time_difference = abs(
        (time_b - time_a).total_seconds()
    ) / 60

    # Determine selection status

    status = (
        "Selected"
        if hybrid_score >= threshold
        else "Not Selected"
    )

    # Verify against original candidate score

    score_difference = abs(
        hybrid_score - original_score
    )

    # Generate human-readable explanation

    explanation = (
        f"Event {event_a} ({details_a['description']}) "
        f"and Event {event_b} ({details_b['description']}) "
        f"have a hybrid similarity score of {hybrid_score:.4f}. "
        f"Semantic similarity: {semantic_score:.4f}. "
        f"Graph similarity: {graph_score:.4f}. "
        f"Selection threshold: {threshold:.2f}. "
        f"Evidence: {', '.join(evidence)}. "
        f"Time difference: {time_difference:.2f} minutes. "
        f"Selection result: {status}."
    )

    explanations.append({

        "event_1": event_a,
        "event_2": event_b,

        "description_1": details_a["description"],
        "description_2": details_b["description"],

        "semantic_similarity": round(
            semantic_score, 4
        ),

        "graph_similarity": round(
            graph_score, 4
        ),

        "hybrid_similarity": round(
            hybrid_score, 4
        ),

        "original_candidate_score": round(
            original_score, 4
        ),

        "score_difference": round(
            score_difference, 6
        ),

        "threshold": threshold,

        "time_difference_minutes": round(
            time_difference, 2
        ),

        "evidence": "; ".join(evidence),

        "selection_status": status,

        "explanation": explanation
    })

# 8. Create explanation DataFrame

explanation_df = pd.DataFrame(explanations)

# 9. Save CSV output

csv_path = (
    OUTPUT_DIR / "alert_correlation_explanations.csv"
)

explanation_df.to_csv(
    csv_path,
    index=False
)

# 10. Save text report

report_path = (
    OUTPUT_DIR / "alert_correlation_explanations.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "DAY 18: ALERT CORRELATION EXPLAINABILITY\n"
    )

    file.write("=" * 65 + "\n\n")

    file.write(
        f"Total candidate pairs: {len(explanation_df)}\n"
    )

    file.write(
        f"Semantic weight: {SEMANTIC_WEIGHT}\n"
    )

    file.write(
        f"Graph weight: {GRAPH_WEIGHT}\n\n"
    )

    for _, row in explanation_df.iterrows():

        file.write(
            f"Event Pair: {row['event_1']} - {row['event_2']}\n"
        )

        file.write(
            f"Description 1: {row['description_1']}\n"
        )

        file.write(
            f"Description 2: {row['description_2']}\n"
        )

        file.write(
            f"Semantic Similarity: {row['semantic_similarity']:.4f}\n"
        )

        file.write(
            f"Graph Similarity: {row['graph_similarity']:.4f}\n"
        )

        file.write(
            f"Hybrid Similarity: {row['hybrid_similarity']:.4f}\n"
        )

        file.write(
            f"Threshold: {row['threshold']:.2f}\n"
        )

        file.write(
            f"Time Difference: {row['time_difference_minutes']:.2f} minutes\n"
        )

        file.write(
            f"Evidence: {row['evidence']}\n"
        )

        file.write(
            f"Status: {row['selection_status']}\n"
        )

        file.write(
            f"Explanation: {row['explanation']}\n"
        )

        file.write("-" * 65 + "\n\n")

# 11. Display results

selected_count = (
    explanation_df["selection_status"] == "Selected"
).sum()

scores_match = (
    explanation_df["score_difference"] <= 0.0001
).all()

print("\nDAY 18: ALERT CORRELATION EXPLAINABILITY")
print("=" * 55)

print("Total candidate pairs:", len(explanation_df))
print("Selected pairs:", selected_count)

print("\nSimilarity results:")

print(
    explanation_df[
        [
            "event_1",
            "event_2",
            "semantic_similarity",
            "graph_similarity",
            "hybrid_similarity",
            "selection_status"
        ]
    ].to_string(index=False)
)

print("\nScore validation:")
print("Scores match candidate file:", scores_match)

print("\nOutput files:")
print("CSV:", csv_path)
print("Text report:", report_path)

print("\nDay 18 explanation generation completed.")
