import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Load normalized security events
df = pd.read_csv("data/normalized/normalized_events.csv")

# Step 2: Extract event descriptions
documents = df["description"].fillna("").astype(str)

# Step 3: Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Step 4: Convert text into numerical features
tfidf_matrix = vectorizer.fit_transform(documents)

# Step 5: Display vocabulary
print("TF-IDF Vocabulary:")
print(vectorizer.get_feature_names_out())

# Step 6: Display numerical matrix
print("\nTF-IDF Matrix:")
print(tfidf_matrix.toarray())

# Step 7: Display matrix dimensions
print("\nMatrix Shape:")
print(tfidf_matrix.shape)

# Step 8: Save TF-IDF features
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=vectorizer.get_feature_names_out()
)

tfidf_df.to_csv(
    "data/normalized/tfidf_features.csv",
    index=False
)

print("\nTF-IDF features saved successfully!")