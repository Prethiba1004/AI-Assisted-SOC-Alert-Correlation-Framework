import pandas as pd
import hdbscan

# Step 1: Load Sentence-BERT embeddings
input_file = "data/normalized/sentence_bert_embeddings.csv"
df = pd.read_csv(input_file)

# Step 2: Select only the 384 embedding dimensions
embedding_columns = [
    col for col in df.columns if col.startswith("dimension_")
]

X = df[embedding_columns].values

# Step 3: Configure HDBSCAN
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=2,
    min_samples=1,
    metric="euclidean",
    cluster_selection_method="eom"
)

# Step 4: Perform clustering
labels = clusterer.fit_predict(X)

# Step 5: Create results
results = pd.DataFrame({
    "event_index": df["event_index"],
    "cluster_label": labels
})

results["event_type"] = results["cluster_label"].apply(
    lambda label: "Noise" if label == -1 else "Cluster"
)

# Step 6: Save results
output_file = "data/normalized/sentence_bert_hdbscan_clusters.csv"
results.to_csv(output_file, index=False)

# Step 7: Display results
print("\nHDBSCAN CLUSTERING RESULTS")
print(results.to_string(index=False))

print("\nTotal events:", len(results))
print("Number of clusters:", results.loc[
    results["cluster_label"] != -1, "cluster_label"
].nunique())
print("Noise events:", (results["cluster_label"] == -1).sum())

print("\nResults saved to:", output_file)
