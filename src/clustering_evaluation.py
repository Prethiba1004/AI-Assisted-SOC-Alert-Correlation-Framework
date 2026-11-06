import pandas as pd
from sklearn.metrics import silhouette_score

# Load embedding data
embeddings = pd.read_csv(
    "data/normalized/sentence_bert_embeddings.csv"
)

embedding_columns = [
    col for col in embeddings.columns
    if col.startswith("dimension_")
]

X = embeddings[embedding_columns].values

# Load clustering results
dbscan = pd.read_csv(
    "data/normalized/dbscan_clusters.csv"
)

hdbscan = pd.read_csv(
    "data/normalized/sentence_bert_hdbscan_clusters.csv"
)

def evaluate_clustering(name, labels, X):
    total_events = len(labels)
    noise_events = sum(labels == -1)
    clustered_events = total_events - noise_events

    valid_labels = labels[labels != -1]
    number_of_clusters = len(set(valid_labels))

    silhouette = "Not Applicable"

    if number_of_clusters >= 2:
        mask = labels != -1
        silhouette = round(
            silhouette_score(X[mask], labels[mask]), 4
        )

    return {
        "algorithm": name,
        "total_events": total_events,
        "clusters": number_of_clusters,
        "clustered_events": clustered_events,
        "noise_events": noise_events,
        "silhouette_score": silhouette
    }

# Evaluate both algorithms
results = []

results.append(
    evaluate_clustering(
        "DBSCAN",
        dbscan["cluster_label"].values,
        X
    )
)

results.append(
    evaluate_clustering(
        "HDBSCAN",
        hdbscan["cluster_label"].values,
        X
    )
)

# Create evaluation report
evaluation = pd.DataFrame(results)

output_file = "outputs/clusters/clustering_evaluation.csv"

evaluation.to_csv(output_file, index=False)

print("\nCLUSTERING EVALUATION RESULTS")
print(evaluation.to_string(index=False))

print("\nEvaluation saved to:", output_file)
