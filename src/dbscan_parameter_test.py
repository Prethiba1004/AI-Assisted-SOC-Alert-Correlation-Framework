
import pandas as pd
from sklearn.cluster import DBSCAN

# Load TF-IDF features
features = pd.read_csv(
    "data/normalized/tfidf_features.csv"
)

# Test different eps values
eps_values = [0.85, 0.90, 0.95]

experiment_results = []

for eps_value in eps_values:

    model = DBSCAN(
        eps=eps_value,
        min_samples=2,
        metric="cosine"
    )

    labels = model.fit_predict(features)

    total_clusters = len(set(labels) - {-1})
    noise_events = list(labels).count(-1)

    experiment_results.append({
        "eps": eps_value,
        "total_clusters": total_clusters,
        "noise_events": noise_events,
        "cluster_labels": [int(label) for label in labels]
    })

# Display comparison
results = pd.DataFrame(experiment_results)

print("\nDBSCAN Parameter Sensitivity Results:")
print(results.to_string(index=False))

# Save comparison
results.to_csv(
    "outputs/clusters/dbscan_parameter_comparison.csv",
    index=False
)

print("\nComparison saved successfully!")
