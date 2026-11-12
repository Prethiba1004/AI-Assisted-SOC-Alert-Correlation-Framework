import networkx as nx
import pandas as pd

INPUT_FILE = "outputs/graphs/candidate_pair_graph.graphml"
METRICS_FILE = "outputs/graphs/graph_relationship_metrics.csv"
REPORT_FILE = "outputs/reports/day17_experiment_report.txt"

G = nx.read_graphml(INPUT_FILE)

degree = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)
weighted_degree = dict(G.degree(weight="similarity_score"))

metrics = []

for node in G.nodes():
    metrics.append({
        "event_id": node,
        "degree": degree[node],
        "degree_centrality": round(degree_centrality[node], 4),
        "betweenness_centrality": round(betweenness[node], 4),
        "closeness_centrality": round(closeness[node], 4),
        "weighted_degree": round(weighted_degree[node], 4)
    })

df = pd.DataFrame(metrics)
df.to_csv(METRICS_FILE, index=False)

scores = [
    float(data["similarity_score"])
    for _, _, data in G.edges(data=True)
]

components = list(nx.connected_components(G))

most_connected = [
    node for node, value in degree.items()
    if value == max(degree.values())
]

report = [
    "DAY 17: GRAPH-BASED CANDIDATE RELATIONSHIP ANALYSIS",
    "=" * 55,
    "",
    "1. GRAPH OVERVIEW",
    f"Total nodes: {G.number_of_nodes()}",
    f"Total edges: {G.number_of_edges()}",
    f"Graph density: {nx.density(G):.4f}",
    f"Connected components: {len(components)}",
    f"Is graph connected: {nx.is_connected(G)}",
    "",
    "2. NODE CENTRALITY ANALYSIS",
    df.to_string(index=False),
    "",
    "3. EDGE SIMILARITY ANALYSIS",
    f"Highest similarity: {max(scores):.4f}",
    f"Lowest similarity: {min(scores):.4f}",
    f"Average similarity: {sum(scores) / len(scores):.4f}",
    "",
    "4. MOST CONNECTED EVENTS",
    ", ".join(most_connected),
    "",
    "5. CONNECTED COMPONENT DETAILS"
]

for index, component in enumerate(components, start=1):
    report.append(
        f"Component {index}: {sorted(component, key=int)}"
    )

report.extend([
    "",
    "6. CONCLUSION",
    "All four events belong to one connected component.",
    "Events 0 and 2 have the highest node degree.",
    "Graph connectivity represents candidate relationships,",
    "not proof of a confirmed security incident.",
    "",
    "7. LIMITATIONS",
    "The analysis uses only four synthetic security events.",
    "Results require validation with larger real-world datasets."
])

with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print("Day 17 graph analysis completed successfully.")
print("Metrics saved to:", METRICS_FILE)
print("Report saved to:", REPORT_FILE)
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())
print("Connected components:", len(components))
