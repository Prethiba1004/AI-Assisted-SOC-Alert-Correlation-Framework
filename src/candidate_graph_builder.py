
import pandas as pd
import networkx as nx
from pathlib import Path

print("Day 16: Candidate Pair Graph Construction")

# Define input and output files
INPUT_FILE = Path("outputs/similarity/candidate_pairs.csv")
OUTPUT_DIR = Path("outputs/graphs")

GRAPH_FILE = OUTPUT_DIR / "candidate_pair_graph.graphml"
SUMMARY_FILE = OUTPUT_DIR / "candidate_pair_graph_summary.txt"

# Load candidate pairs
df = pd.read_csv(INPUT_FILE)

# Create an undirected graph
G = nx.Graph()

# Add event nodes and relationship edges
for _, row in df.iterrows():

    event_1 = str(int(row["event_1"]))
    event_2 = str(int(row["event_2"]))
    score = float(row["similarity_score"])

    # Add nodes
    G.add_node(event_1, event_type="Security Event")
    G.add_node(event_2, event_type="Security Event")

    # Add weighted edge
    G.add_edge(
        event_1,
        event_2,
        similarity_score=score,
        semantic_weight=float(row["semantic_weight"]),
        graph_weight=float(row["graph_weight"]),
        threshold=float(row["threshold"])
    )

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Save graph in GraphML format
nx.write_graphml(G, GRAPH_FILE)

# Calculate graph statistics
node_count = G.number_of_nodes()
edge_count = G.number_of_edges()
component_count = nx.number_connected_components(G)

# Create graph summary
summary = [
    "DAY 16: CANDIDATE PAIR GRAPH SUMMARY",
    "====================================",
    "",
    f"Total nodes: {node_count}",
    f"Total edges: {edge_count}",
    f"Connected components: {component_count}",
    f"Graph density: {nx.density(G):.4f}",
    "",
    "EVENT NODES:",
]

for node, attributes in G.nodes(data=True):
    summary.append(f"Event {node}: {attributes}")

summary.append("")
summary.append("CANDIDATE EDGES:")

for source, target, attributes in G.edges(data=True):
    summary.append(
        f"Event {source} - Event {target}: "
        f"Similarity = {attributes['similarity_score']:.4f}"
    )

summary.append("")
summary.append("STATUS: GRAPH CONSTRUCTION COMPLETED")

SUMMARY_FILE.write_text("\n".join(summary), encoding="utf-8")

# Display results
print("\nGraph Construction Results")
print("Total nodes:", node_count)
print("Total edges:", edge_count)
print("Connected components:", component_count)
print("Graph density:", round(nx.density(G), 4))

print("\nGraph saved to:", GRAPH_FILE)
print("Summary saved to:", SUMMARY_FILE)

print("\nDay 16 graph construction completed successfully.")
