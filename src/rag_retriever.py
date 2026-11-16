from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rag_text_chunker import chunk_documents
from rag_document_loader import load_documents


def retrieve_relevant_chunks(query, top_k=3):
    """Retrieve the most relevant knowledge chunks for a SOC alert."""

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    documents = load_documents()
    chunks = chunk_documents(documents)

    chunk_texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(chunk_texts)
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        if similarities[index] <= 0:
            continue

        results.append({
            "document_id": chunks[index]["document_id"],
            "chunk_id": chunks[index]["chunk_id"],
            "similarity_score": round(float(similarities[index]), 4),
            "text": chunks[index]["text"]
        })

    return results


if __name__ == "__main__":
    alert = (
        "Multiple failed login attempts detected "
        "from a suspicious IP address."
    )

    print("SOC Alert:", alert)
    print("\nTop 3 relevant knowledge chunks:")

    results = retrieve_relevant_chunks(alert, top_k=3)

    if not results:
        print("No relevant knowledge found.")
    else:
        for rank, result in enumerate(results, start=1):
            print(f"\n--- Result {rank} ---")
            print("Document ID:", result["document_id"])
            print("Chunk ID:", result["chunk_id"])
            print("Similarity:", result["similarity_score"])
            print("Knowledge:")
            print(result["text"])
