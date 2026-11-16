from rag_document_loader import load_documents


def split_into_chunks(text, chunk_size=300, overlap=50):
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_documents(documents, chunk_size=300, overlap=50):
    """Split multiple documents into smaller chunks."""

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
