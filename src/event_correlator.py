import pandas as pd
import networkx as nx

# Load normalized security events
df = pd.read_csv("data/normalized/normalized_events.csv")

# Convert timestamps into datetime format
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="mixed",
    utc=True
)

# Create an empty graph
G = nx.Graph()

# Add security events as nodes
for index, event in df.iterrows():

    G.add_node(
        index,
        timestamp=str(event["timestamp"]),
        source=event["source"],
        hostname=event["hostname"],
        username=event["username"],
        event_id=str(event["event_id"]),
        description=event["description"]
    )

# Compare every pair of events
for i in range(len(df)):

    for j in range(i + 1, len(df)):

        event1 = df.iloc[i]
        event2 = df.iloc[j]

        reasons = []

        # Condition 1: Same hostname
        if (
            event1["hostname"] == event2["hostname"]
            and event1["hostname"] != "Unknown"
        ):
            reasons.append("Same Hostname")

        # Condition 2: Same username
        if (
            event1["username"] == event2["username"]
            and event1["username"] != "Unknown"
        ):
            reasons.append("Same Username")

        # Condition 3: Events within 10 minutes
        time_difference = abs(
            (event1["timestamp"] - event2["timestamp"]).total_seconds()
        )

        if time_difference <= 600:
            reasons.append("Within 10 Minutes")

        # Create an edge if any condition matches
        if reasons:
            G.add_edge(
                i,
                j,
                relationship=", ".join(reasons),
                time_difference_seconds=time_difference
            )

# Display graph information
print("Total Events (Nodes):", G.number_of_nodes())
print("Total Relationships (Edges):", G.number_of_edges())

print("\nEvent Relationships:")

for edge in G.edges(data=True):
    print(edge)

# Save graph
nx.write_graphml(
    G,
    "outputs/graphs/event_correlation.graphml"
)

print("\nImproved correlation graph saved successfully!")
