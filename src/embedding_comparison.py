
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load TF-IDF embeddings
tfidf_file = "data/normalized/tfidf_features.csv"
tfidf_df = pd.read_csv(tfidf_file)

# Step 2: Load Sentence-BERT embeddings
bert_file = "data/normalized/sentence_bert_embeddings.csv"
bert_df = pd.read_csv(bert_file)

# Step 3: Extract numerical feature columns
tfidf_vectors = tfidf_df.select_dtypes(include="number").values

bert_vectors = bert_df.drop(columns=["event_index"]).values

# Step 4: Calculate cosine similarity
tfidf_similarity = cosine_similarity(tfidf_vectors)
bert_similarity = cosine_similarity(bert_vectors)

# Step 5: Display comparison
print("\nTF-IDF Cosine Similarity:")
print(tfidf_similarity.round(3))

print("\nSentence-BERT Cosine Similarity:")
print(bert_similarity.round(3))

# Step 6: Save similarity matrices
tfidf_output = pd.DataFrame(tfidf_similarity)
bert_output = pd.DataFrame(bert_similarity)

tfidf_output.to_csv(
    "outputs/clusters/tfidf_similarity_matrix.csv",
    index=False
)

bert_output.to_csv(
    "outputs/clusters/sentence_bert_similarity_matrix.csv",
    index=False
)

print("\nComparison Results Saved Successfully")
