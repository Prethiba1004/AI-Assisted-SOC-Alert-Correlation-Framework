
from rag_document_loader import load_documents


def split_into_chunks(text, chunk_size=300, overlap=50):
    """Split text into overlapping chunks without cutting words."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Move the end forward to the next whitespace boundary.
        if end < text_length:
            while end < text_length and not text[end].isspace():
                end += 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Calculate the next starting point using the overlap.
        next_start = max(0, end - overlap)

        # Move forward to the next word boundary.
        while next_start < end and not text[next_start].isspace():
            next_start += 1

        while next_start < end and text[next_start].isspace():
            next_start += 1

        if next_start <= start:
            break

        start = next_start

    return chunks


def chunk_documents(documents, chunk_size=300, overlap=50):
    """Split multiple documents into word-aware chunks."""

    all_chunks = []

    for document_id, document in enumerate(documents, start=1):
        chunks = split_into_chunks(document, chunk_size, overlap)

        for chunk_id, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "document_id": document_id,
                "chunk_id": chunk_id,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)

    print("Total documents:", len(documents))
    print("Total chunks:", len(chunks))

    for chunk in chunks:
        print(
            f"\nDocument {chunk['document_id']} "
            f"| Chunk {chunk['chunk_id']}"
        )
        print(chunk["text"])
