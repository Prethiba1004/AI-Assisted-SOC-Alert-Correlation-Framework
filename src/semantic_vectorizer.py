
import pandas as pd
from sentence_transformers import SentenceTransformer

# Step 1: Load normalized security events
input_file = "data/normalized/normalized_events.csv"
df = pd.read_csv(input_file)

print("Security Events Loaded Successfully")
print("Total Events:", len(df))

# Step 2: Extract event descriptions
descriptions = df["description"].fillna("").astype(str).tolist()

# Step 3: Load Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 4: Generate semantic embeddings
embeddings = model.encode(
    descriptions,
    show_progress_bar=True
)

print("\nSemantic Embeddings Generated Successfully")
print("Embedding Shape:", embeddings.shape)

# Step 5: Convert embeddings into a DataFrame
embedding_columns = [
    f"dimension_{i}" for i in range(embeddings.shape[1])
]

embedding_df = pd.DataFrame(
    embeddings,
    columns=embedding_columns
)

# Step 6: Add event index
embedding_df.insert(0, "event_index", range(len(df)))

# Step 7: Save embeddings
output_file = "data/normalized/sentence_bert_embeddings.csv"
embedding_df.to_csv(output_file, index=False)

print("\nEmbeddings Saved Successfully")
print("Output File:", output_file)
