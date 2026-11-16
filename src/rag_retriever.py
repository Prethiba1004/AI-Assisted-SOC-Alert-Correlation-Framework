
import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rag_text_chunker import chunk_documents
from rag_document_loader import load_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "rag_config.json"


def load_rag_config():
    """Load RAG retrieval configuration."""

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text):
    """Extract and normalize useful words."""

    stop_words = {
        "a", "an", "the", "was", "were", "is", "are",
        "from", "to", "and", "or", "of", "in", "on",
        "at", "by", "with", "this", "that", "may",
        "be", "as", "for", "their"
    }

    tokens = re.findall(r"[a-z0-9]+", text.lower())

    normalized = []

    for token in tokens:
        if token in stop_words:
            continue

        if token in {"used", "using", "uses"}:
            token = "use"

        # Simple plural normalization.
        elif token.endswith("s") and len(token) > 4:
            token = token[:-1]

        normalized.append(token)

    return set(normalized)


def extract_detection_text(document):
    """Extract technique name, description and detection clues."""

    fields = re.findall(
        r"^(?:Technique Name|Description|Detection Clues):\s*(.*)$",
        document,
        flags=re.MULTILINE
    )

    return " ".join(fields)


def calculate_keyword_score(query, document):
    """Calculate query keyword coverage against technique information."""

    query_terms = tokenize(query)
    document_terms = tokenize(extract_detection_text(document))

    if not query_terms:
        return 0.0

    matched_terms = query_terms.intersection(document_terms)

    return len(matched_terms) / len(query_terms)


def retrieve_relevant_chunks(query, top_k=3):
    """Retrieve relevant knowledge using TF-IDF or hybrid scoring."""

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    config = load_rag_config()

    retrieval_method = config.get("retrieval_method", "tfidf")
    keyword_boost = float(config.get("keyword_boost", 0.15))

    if retrieval_method not in {"tfidf", "hybrid"}:
        raise ValueError("Unsupported retrieval method")

    if not 0 <= keyword_boost <= 1:
        raise ValueError("keyword_boost must be between 0 and 1")

    documents = load_documents()
    chunks = chunk_documents(documents)

    if not chunks:
        return []

    chunk_texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(chunk_texts)
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    # Select the highest-scoring chunk from each document.
    best_results = {}

    for index, score in enumerate(similarities):
        if score <= 0:
            continue

        chunk = chunks[index]
        document_id = chunk["document_id"]

        if (
            document_id not in best_results
            or score > best_results[document_id]["tfidf_score"]
        ):
            best_results[document_id] = {
                "document_id": document_id,
                "chunk_id": chunk["chunk_id"],
                "tfidf_score": float(score),
                "text": chunk["text"]
            }

    # Combine TF-IDF and keyword scores.
    for document_id, result in best_results.items():

        original_document = documents[document_id - 1]

        keyword_score = calculate_keyword_score(
            query,
            original_document
        )

        tfidf_score = result["tfidf_score"]

        if retrieval_method == "hybrid":
            final_score = (
                (1 - keyword_boost) * tfidf_score
                + keyword_boost * keyword_score
            )
        else:
            final_score = tfidf_score

        result["keyword_score"] = round(keyword_score, 4)
        result["similarity_score"] = round(final_score, 4)
        result["tfidf_score"] = round(tfidf_score, 4)

    ranked_results = sorted(
        best_results.values(),
        key=lambda result: result["similarity_score"],
        reverse=True
    )

    return ranked_results[:top_k]


if __name__ == "__main__":

    alert = (
        "Multiple failed login attempts detected "
        "from a suspicious IP address."
    )

    print("SOC Alert:", alert)
    print("Retrieval method:", load_rag_config()["retrieval_method"])
    print("\nTop 3 relevant knowledge documents:")

    results = retrieve_relevant_chunks(alert, top_k=3)

    if not results:
        print("No relevant knowledge found.")

    else:
        for rank, result in enumerate(results, start=1):
            print(f"\n--- Result {rank} ---")
            print("Document ID:", result["document_id"])
            print("Chunk ID:", result["chunk_id"])
            print("TF-IDF Score:", result["tfidf_score"])
            print("Keyword Score:", result["keyword_score"])
            print("Hybrid Score:", result["similarity_score"])
            print("Knowledge:")
            print(result["text"])
