import pandas as pd
from pathlib import Path

# Step 1: Define input and output files
graph_file = "outputs/graphs/graph_features.csv"
embedding_file = "data/normalized/sentence_bert_embeddings.csv"
output_file = "data/normalized/hybrid_features.csv"

# Step 2: Load datasets
graph_df = pd.read_csv(graph_file)
embedding_df = pd.read_csv(embedding_file)

print("GRAPH FEATURES:", graph_df.shape)
print("SENTENCE-BERT EMBEDDINGS:", embedding_df.shape)

# Step 3: Validate identifiers
if graph_df["node_id"].duplicated().any():
    raise ValueError("Duplicate node IDs found in graph features.")

if embedding_df["event_index"].duplicated().any():
    raise ValueError("Duplicate event indexes found in embeddings.")

graph_ids = set(graph_df["node_id"])
embedding_ids = set(embedding_df["event_index"])

if graph_ids != embedding_ids:
    raise ValueError("Graph node IDs and embedding event indexes do not match.")

# Step 4: Rename the embedding identifier
embedding_df = embedding_df.rename(columns={"event_index": "node_id"})

# Step 5: Select semantic embedding columns
embedding_columns = [
    column for column in embedding_df.columns
    if column.startswith("dimension_")
]

if len(embedding_columns) != 384:
    raise ValueError(
        f"Expected 384 embedding dimensions, found {len(embedding_columns)}."
    )

# Step 6: Merge graph and semantic features
hybrid_df = pd.merge(
    graph_df,
    embedding_df[["node_id"] + embedding_columns],
    on="node_id",
    how="inner",
    validate="one_to_one"
)

# Step 7: Validate the hybrid dataset
if len(hybrid_df) != len(graph_df):
    raise ValueError("Some graph events were lost during integration.")

if hybrid_df.isnull().sum().sum() > 0:
    raise ValueError("Missing values found in the hybrid dataset.")

# Step 8: Save output
Path(output_file).parent.mkdir(parents=True, exist_ok=True)
hybrid_df.to_csv(output_file, index=False)

# Step 9: Display results
print("\nHYBRID FEATURE INTEGRATION COMPLETED")
print("Output file:", output_file)
print("Dataset shape:", hybrid_df.shape)
print("Total events:", len(hybrid_df))
print("Graph feature columns:", len(graph_df.columns) - 1)
print("Semantic embedding columns:", len(embedding_columns))
print("Missing values:", hybrid_df.isnull().sum().sum())
print("Event IDs:", hybrid_df["node_id"].tolist())
print("\nSelected columns:")
print(hybrid_df[["node_id", "event_description", "degree", "weighted_degree"]].to_string(index=False))
