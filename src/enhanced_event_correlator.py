import pandas as pd
import networkx as nx

# Step 1: Load normalized security events
df = pd.read_csv("data/normalized/normalized_events.csv")

# Step 2: Convert timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="mixed",
    utc=True
)

# Step 3: Create an empty graph
G = nx.Graph()

# Step 4: Add security events as graph nodes
for index, event in df.iterrows():

    G.add_node(
        index,
        timestamp=str(event["timestamp"]),
        source=str(event["source"]),
        hostname=str(event["hostname"]),
        username=str(event["username"]),
        event_id=str(event["event_id"]),
        description=str(event["description"])
    )

# Step 5: Compare every pair of events
for i in range(len(df)):

    for j in range(i + 1, len(df)):

        event1 = df.iloc[i]
        event2 = df.iloc[j]

        reasons = []
        score = 0

        # Condition 1: Same known hostname
        if (
            pd.notna(event1["hostname"])
            and pd.notna(event2["hostname"])
            and event1["hostname"] != "Unknown"
            and event2["hostname"] != "Unknown"
            and event1["hostname"] == event2["hostname"]
        ):
            score += 40
            reasons.append("Same Hostname (+40)")

        # Condition 2: Same known username
        if (
            pd.notna(event1["username"])
            and pd.notna(event2["username"])
            and event1["username"] != "Unknown"
            and event2["username"] != "Unknown"
            and event1["username"] == event2["username"]
        ):
            score += 30
            reasons.append("Same Username (+30)")

        # Condition 3: Time-based correlation
        time_difference = abs(
            (event1["timestamp"] - event2["timestamp"]).total_seconds()
        )

        if time_difference <= 300:
            score += 20
            reasons.append("Within 5 Minutes (+20)")

        elif time_difference <= 600:
            score += 10
            reasons.append("Within 10 Minutes (+10)")

        # Step 6: Classify relationship
        if score >= 60:
            relationship_strength = "Strong"

        elif score >= 30:
            relationship_strength = "Moderate"

        elif score > 0:
            relationship_strength = "Weak"

        else:
            relationship_strength = "No Relationship"

        # Step 7: Add edge when a relationship exists
        if score > 0:

            G.add_edge(
                i,
                j,
                correlation_score=score,
                relationship_strength=relationship_strength,
                relationship=", ".join(reasons),
                time_difference_seconds=time_difference
            )

# Step 8: Display results
print("ENHANCED EVENT CORRELATION ANALYSIS")
print("=" * 50)

print("Total Events (Nodes):", G.number_of_nodes())
print("Total Relationships (Edges):", G.number_of_edges())

print("\nEVENT RELATIONSHIPS")

for source, target, data in G.edges(data=True):

    print("\nEvent", source, "<-> Event", target)
    print("Score:", data["correlation_score"])
    print("Strength:", data["relationship_strength"])
    print("Reasons:", data["relationship"])
    print("Time Difference:", data["time_difference_seconds"], "seconds")

# Step 9: Save enhanced graph
output_file = "outputs/graphs/enhanced_event_correlation.graphml"

nx.write_graphml(G, output_file)

print("\nEnhanced correlation graph saved successfully!")
print("Output:", output_file)

