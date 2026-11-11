
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# ==========================================
# DAY 13: HYBRID SIMILARITY CALCULATION
# ==========================================

# 1. Define input and output paths
FEATURE_FILE = "data/normalized/hybrid_features.csv"
GRAPH_FILE = "outputs/graphs/enhanced_event_correlation.graphml"
OUTPUT_DIR = Path("outputs/similarity")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Experimental weights
SEMANTIC_WEIGHT = 0.60
GRAPH_WEIGHT = 0.40

# Maximum possible graph correlation score
MAX_GRAPH_SCORE = 90.0

# 2. Load hybrid feature dataset
df = pd.read_csv(FEATURE_FILE)

# 3. Identify event IDs and embedding columns
event_ids = df["node_id"].astype(int).tolist()

embedding_columns = [
    column for column in df.columns
    if column.startswith("dimension_")
]

embeddings = df[embedding_columns].to_numpy(dtype=float)

# 4. Calculate semantic cosine similarity
semantic_raw = cosine_similarity(embeddings)

# Convert cosine similarity from [-1, 1] to [0, 1]
semantic_matrix = (semantic_raw + 1.0) / 2.0

semantic_matrix = np.clip(semantic_matrix, 0.0, 1.0)

# 5. Load enhanced event correlation graph
G = nx.read_graphml(GRAPH_FILE)

# 6. Initialize graph similarity matrix
event_count = len(event_ids)

graph_matrix = np.zeros((event_count, event_count))

# Self-similarity is always 1
np.fill_diagonal(graph_matrix, 1.0)

# 7. Populate graph relationships
for i, event_a in enumerate(event_ids):
    for j, event_b in enumerate(event_ids):

        if G.has_edge(str(event_a), str(event_b)):
            score = float(
                G[str(event_a)][str(event_b)]["correlation_score"]
            )

            normalized_score = score / MAX_GRAPH_SCORE

            graph_matrix[i, j] = np.clip(
                normalized_score, 0.0, 1.0
            )

# 8. Calculate hybrid similarity
hybrid_matrix = (
    SEMANTIC_WEIGHT * semantic_matrix
    + GRAPH_WEIGHT * graph_matrix
)

# Keep diagonal values at 1
np.fill_diagonal(hybrid_matrix, 1.0)

# 9. Convert matrices into DataFrames
semantic_df = pd.DataFrame(
    semantic_matrix,
    index=event_ids,
    columns=event_ids
)

graph_df = pd.DataFrame(
    graph_matrix,
    index=event_ids,
    columns=event_ids
)

hybrid_df = pd.DataFrame(
    hybrid_matrix,
    index=event_ids,
    columns=event_ids
)

semantic_df.index.name = "event_id"
graph_df.index.name = "event_id"
hybrid_df.index.name = "event_id"

# 10. Save output matrices
semantic_df.to_csv(
    OUTPUT_DIR / "semantic_similarity_matrix.csv"
)

graph_df.to_csv(
    OUTPUT_DIR / "graph_similarity_matrix.csv"
)

hybrid_df.to_csv(
    OUTPUT_DIR / "hybrid_similarity_matrix.csv"
)

# 11. Display results
print("\nDAY 13: HYBRID SIMILARITY CALCULATION")
print("=" * 50)

print("\nDataset shape:", df.shape)
print("Total events:", event_count)
print("Embedding dimensions:", len(embedding_columns))

print("\nExperimental weights:")
print("Semantic weight:", SEMANTIC_WEIGHT)
print("Graph weight:", GRAPH_WEIGHT)

print("\nSEMANTIC SIMILARITY MATRIX")
print(semantic_df.round(3))

print("\nGRAPH SIMILARITY MATRIX")
print(graph_df.round(3))

print("\nHYBRID SIMILARITY MATRIX")
print(hybrid_df.round(3))

print("\nOUTPUT FILES")
print("1. semantic_similarity_matrix.csv")
print("2. graph_similarity_matrix.csv")
print("3. hybrid_similarity_matrix.csv")

print("\nDay 13 calculation completed.")
