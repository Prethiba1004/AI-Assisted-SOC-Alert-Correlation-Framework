import pandas as pd

dbscan_file = "data/normalized/dbscan_clusters.csv"
hdbscan_file = "data/normalized/sentence_bert_hdbscan_clusters.csv"

dbscan = pd.read_csv(dbscan_file)
hdbscan = pd.read_csv(hdbscan_file)

comparison = pd.DataFrame({
    "event_index": dbscan["event_index"],
    "dbscan_label": dbscan["cluster_label"],
    "hdbscan_label": hdbscan["cluster_label"]
})

comparison["dbscan_type"] = comparison["dbscan_label"].apply(
    lambda x: "Noise" if x == -1 else "Cluster"
)

comparison["hdbscan_type"] = comparison["hdbscan_label"].apply(
    lambda x: "Noise" if x == -1 else "Cluster"
)

output_file = "outputs/clusters/dbscan_hdbscan_comparison.csv"
comparison.to_csv(output_file, index=False)

print("\nDBSCAN VS HDBSCAN COMPARISON")
print(comparison.to_string(index=False))

print("\nComparison saved to:", output_file)
