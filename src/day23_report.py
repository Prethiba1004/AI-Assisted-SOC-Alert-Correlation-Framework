from pathlib import Path
from datetime import datetime


def generate_report():
    report = """
DAY 23 EXPERIMENT REPORT
Project: AI-Assisted SOC Alert Correlation Framework
Topic: Retrieval-Augmented Generation (RAG) Implementation

1. OBJECTIVE
Implement a lightweight RAG pipeline that retrieves relevant MITRE
ATT&CK knowledge and provides the retrieved context to Gemini for
SOC alert analysis.

2. IMPLEMENTED COMPONENTS

- RAG architecture configuration
- Curated MITRE ATT&CK knowledge base
- JSON document loader
- Character-based text chunking
- TF-IDF vectorization
- Cosine similarity retrieval
- Gemini LLM integration

3. KNOWLEDGE BASE

Total curated MITRE ATT&CK techniques: 5

Technique IDs:
- T1059.001: PowerShell
- T1110: Brute Force
- T1078: Valid Accounts
- T1059: Command and Scripting Interpreter
- T1021.001: Remote Desktop Protocol

4. DOCUMENT PROCESSING

Documents loaded: 5
Chunk size: 300 characters
Chunk overlap: 50 characters
Total chunks generated: 10

5. INFORMATION RETRIEVAL EXPERIMENT

Sample SOC alert:
Multiple failed login attempts detected from a suspicious IP address.

Retrieval method: TF-IDF
Similarity metric: Cosine Similarity
Top-K: 3

Results:
1. T1110 Brute Force: 0.4431
2. T1110 Brute Force: 0.2895
3. T1078 Valid Accounts: 0.1479

The highest-ranked result was T1110 Brute Force.

6. GEMINI INTEGRATION

Existing Gemini client reused.
Model: gemini-3.5-flash-lite

Integration result: Successful

Generated analysis included:
- Alert summary
- Relevant MITRE ATT&CK technique
- Evidence supporting the mapping
- Recommended investigation steps
- Limitations and uncertainties

7. OBSERVATIONS

The retriever ranked Brute Force knowledge first because the
alert mentioned multiple failed login attempts.

Gemini used the retrieved context to produce an explanation
and investigation guidance.

The model correctly identified that the available alert text
was insufficient to confirm a security incident.

8. LIMITATIONS

- Knowledge base contains only five curated techniques.
- Test uses a sample SOC alert.
- TF-IDF uses lexical similarity and may miss semantic matches.
- Character-based chunking can split words.
- Multiple retrieved chunks may belong to the same technique.
- LLM output requires human verification.
- No production deployment or real-time SOC integration tested.

9. CONCLUSION

A lightweight RAG prototype was implemented successfully.
The system loads curated MITRE knowledge, divides documents
into chunks, retrieves relevant information using TF-IDF and
cosine similarity, and supplies that context to Gemini.

The experiment demonstrates the basic RAG workflow for
assisting SOC alert analysis.

This prototype is experimental and is not a replacement
for security analyst investigation.

10. COMPLETION STATUS

Day 23 objectives: 6/6 completed
RAG retrieval test: Successful
Gemini integration test: Successful
""".strip()

    output_dir = Path("outputs/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "day23_experiment_report.txt"
    output_file.write_text(
        report + "\n",
        encoding="utf-8"
    )

    print("Day 23 report generated successfully.")
    print("Report location:", output_file.resolve())
    print("Report size:", output_file.stat().st_size, "bytes")


if __name__ == "__main__":
    generate_report()
