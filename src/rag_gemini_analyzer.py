from rag_retriever import retrieve_relevant_chunks
from llm_client import generate_llm_response


def analyze_alert_with_rag(alert, top_k=3):
    """Analyze a SOC alert using retrieved MITRE knowledge and Gemini."""

    if not alert or not alert.strip():
        raise ValueError("SOC alert cannot be empty")

    retrieved_chunks = retrieve_relevant_chunks(alert, top_k=top_k)

    if not retrieved_chunks:
        return {
            "retrieved_context": [],
            "analysis": "Insufficient relevant knowledge was retrieved. Human investigation is required."
        }

    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    prompt = f"""
You are assisting a Security Operations Center (SOC) analyst.

Analyze the following security alert using ONLY the supplied
knowledge context as the reference for MITRE ATT&CK information.

SOC ALERT:
{alert}

RETRIEVED KNOWLEDGE CONTEXT:
{context}

Provide your response under these headings:

1. Alert Summary
2. Relevant MITRE ATT&CK Technique
3. Evidence Supporting the Mapping
4. Recommended Investigation Steps
5. Limitations and Uncertainties

Important rules:
- Do not invent evidence that is not present in the alert.
- Do not claim an attack is confirmed based only on text similarity.
- Clearly distinguish retrieved knowledge from observed alert evidence.
- If evidence is insufficient, say so.
- Recommend human analyst verification.
"""

    analysis = generate_llm_response(prompt)

    return {
        "retrieved_context": retrieved_chunks,
        "analysis": analysis
    }


if __name__ == "__main__":
    sample_alert = (
        "Multiple failed login attempts detected "
        "from a suspicious IP address."
    )

    print("SOC ALERT:")
    print(sample_alert)

    print("\nRunning RAG + Gemini analysis...")

    result = analyze_alert_with_rag(sample_alert)

    print("\nRETRIEVED KNOWLEDGE:")
    for item in result["retrieved_context"]:
        print(
            f"\nDocument {item['document_id']}, "
            f"Chunk {item['chunk_id']}, "
            f"Similarity: {item['similarity_score']}"
        )

    print("\nGEMINI SOC ANALYSIS:")
    print(result["analysis"])
