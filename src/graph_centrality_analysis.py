import pandas as pd
import networkx as nx

# Step 1: Load the existing event correlation graph
G = nx.read_graphml("outputs/graphs/event_correlation.graphml")

# Step 2: Calculate centrality metrics
degree = nx.degree(G)
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Step 3: Prepare graph analysis results
results = []

for node in G.nodes():

    results.append({
        "node_id": node,
        "event_description": G.nodes[node]["description"],
        "degree": degree[node],
        "degree_centrality": degree_centrality[node],
        "betweenness_centrality": betweenness_centrality[node],
        "closeness_centrality": closeness_centrality[node]
    })

# Step 4: Convert results into a DataFrame
df = pd.DataFrame(results)

# Step 5: Save results into CSV
output_file = "outputs/graphs/graph_centrality_metrics.csv"
df.to_csv(output_file, index=False)

print("Graph centrality analysis completed!")
print("Total nodes analyzed:", len(df))
print("Output saved:", output_file)

# Step 6: Display results
print("\nCENTRALITY METRICS")
print(df.to_string(index=False))
