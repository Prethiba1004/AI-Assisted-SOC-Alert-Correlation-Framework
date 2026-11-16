import json
from pathlib import Path


def load_documents(file_path="data/knowledge_base/mitre_attack_knowledge.json"):
    """Load MITRE ATT&CK knowledge entries as text documents."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Knowledge base not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        techniques = json.load(file)

    documents = []

    for technique in techniques:
        document = (
            f"Technique ID: {technique['technique_id']}\n"
            f"Technique Name: {technique['technique_name']}\n"
            f"Description: {technique['description']}\n"
            f"Detection Clues: {technique['detection_clues']}\n"
            f"Analyst Guidance: {technique['analyst_guidance']}"
        )

        documents.append(document)

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print("Total documents loaded:", len(docs))

    for index, document in enumerate(docs, start=1):
        print(f"\n--- Document {index} ---")
        print(document)
