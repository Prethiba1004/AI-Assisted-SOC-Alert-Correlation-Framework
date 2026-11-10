import networkx as nx
import pandas as pd

# Step 1: Load the Day 10 enhanced correlation graph
input_file = "outputs/graphs/enhanced_event_correlation.graphml"
G = nx.read_graphml(input_file)

# Step 2: Calculate graph measurements
degree = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Step 3: Calculate weighted degree using correlation scores
weighted_degree = {}

for node in G.nodes():
    total_score = sum(
        float(data.get("correlation_score", 0))
        for _, _, data in G.edges(node, data=True)
    )
    weighted_degree[node] = total_score

# Step 4: Collect event details and graph features
results = []

for node, attributes in G.nodes(data=True):
    results.append({
        "node_id": node,
        "event_description": attributes.get("description", ""),
        "hostname": attributes.get("hostname", ""),
        "username": attributes.get("username", ""),
        "degree": degree[node],
        "degree_centrality": degree_centrality[node],
        "betweenness_centrality": betweenness_centrality[node],
        "closeness_centrality": closeness_centrality[node],
        "weighted_degree": weighted_degree[node]
    })

# Step 5: Save the results
df = pd.DataFrame(results)

output_file = "outputs/graphs/graph_features.csv"
df.to_csv(output_file, index=False)

print("GRAPH FEATURE EXTRACTION COMPLETED")
print("Total events:", len(df))
print("Total features:", len(df.columns) - 4)
print("\nExtracted Graph Features:")
print(df.to_string(index=False))
print("\nOutput saved to:", output_file)
