import networkx as nx
import matplotlib.pyplot as plt

INPUT_FILE = "outputs/graphs/candidate_pair_graph.graphml"
OUTPUT_FILE = "outputs/graphs/graph_relationship_analysis.png"

G = nx.read_graphml(INPUT_FILE)

plt.figure(figsize=(10, 7))

pos = nx.spring_layout(G, seed=42)

node_degrees = dict(G.degree())

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=1800,
    node_color="skyblue",
    edgecolors="black"
)

nx.draw_networkx_edges(
    G,
    pos,
    width=2,
    edge_color="gray"
)

node_labels = {
    node: f"Event {node}\nDegree: {node_degrees[node]}"
    for node in G.nodes()
}

nx.draw_networkx_labels(
    G,
    pos,
    labels=node_labels,
    font_size=10,
    font_weight="bold"
)

edge_labels = {
    (u, v): f"{float(data['similarity_score']):.4f}"
    for u, v, data in G.edges(data=True)
}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=9
)

plt.title("Day 17: Candidate Event Relationship Graph")
plt.axis("off")
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.close()

print("Graph visualization generated successfully.")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())
print("Saved to:", OUTPUT_FILE)
