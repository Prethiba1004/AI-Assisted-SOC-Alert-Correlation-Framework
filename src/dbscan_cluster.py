
import pandas as pd
from sklearn.cluster import DBSCAN

# Step 1: Load original security events
events_file = "data/normalized/normalized_events.csv"
events = pd.read_csv(events_file)

# Step 2: Load TF-IDF feature vectors
features_file = "data/normalized/tfidf_features.csv"
features = pd.read_csv(features_file)

print("Original Events Loaded:", len(events))
print("TF-IDF Features Loaded:", len(features))

# Step 3: Verify that both files have matching rows
if len(events) != len(features):
    raise ValueError("Event count and feature count do not match!")

# Step 4: Apply DBSCAN clustering
model = DBSCAN(
    eps=0.9,
    min_samples=2,
    metric="cosine"
)

cluster_labels = model.fit_predict(features)

# Step 5: Create clustering results
results = events.copy()

results.insert(0, "event_index", range(len(results)))

results["cluster_label"] = cluster_labels

results["event_type"] = results["cluster_label"].apply(
    lambda label: "Noise" if label == -1 else "Cluster"
)

# Step 6: Save basic clustering results
basic_results = pd.DataFrame({
    "event_index": range(len(events)),
    "cluster_label": cluster_labels
})

basic_results["event_type"] = basic_results["cluster_label"].apply(
    lambda label: "Noise" if label == -1 else "Cluster"
)

basic_results.to_csv(
    "data/normalized/dbscan_clusters.csv",
    index=False
)

# Step 7: Save detailed clustering results
output_file = "data/normalized/dbscan_clustered_events.csv"

results.to_csv(output_file, index=False)

# Step 8: Display results
print("\nDetailed DBSCAN Clustering Results:")
print(results.to_string(index=False))

print("\nTotal Clusters:",
      len(set(cluster_labels) - {-1}))

print("Noise Events:",
      list(cluster_labels).count(-1))

print("\nDetailed results saved successfully:", output_file)
