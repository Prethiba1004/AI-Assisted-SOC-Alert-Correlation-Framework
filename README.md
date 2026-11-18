# AI-Assisted SOC Alert Correlation Framework

A Python-based research prototype combining security event correlation, machine-learning experiments, MITRE ATT&CK enrichment, RAG, and LLM-assisted SOC investigation.

## Objectives
- Normalize security events from different sources.
- Correlate events using graph analysis and similarity techniques.
- Experiment with TF-IDF, Sentence-BERT, DBSCAN, and HDBSCAN.
- Generate MITRE ATT&CK-enriched meta-alerts.
- Retrieve cybersecurity knowledge using RAG.
- Generate evidence-grounded LLM investigation reports.
- Validate evidence relationships and evaluate investigation quality.

## Technologies
- Python 3.12, Pandas, Scikit-learn, NetworkX
- TF-IDF, cosine similarity, Sentence Transformers
- DBSCAN and HDBSCAN
- MITRE ATT&CK
- RAG and Gemini LLM
- Windows Sysmon, Kali Linux logs, Elastic Security
- Git and GitHub

## Architecture
Security Events -> Normalization -> Feature Extraction -> Event Correlation -> MITRE Enrichment -> Meta-Alerts -> RAG Retrieval -> LLM Investigation -> Evidence Validation -> Reports

## Key Components
1. Log normalization: standardizes event records.
2. Event correlation: identifies relationships between security events.
3. Machine-learning experiments: explores clustering and similarity methods.
4. MITRE enrichment: applies rule-based potential technique mappings.
5. RAG investigation: retrieves relevant knowledge for LLM analysis.
6. Evidence validation: checks event-level IP attribution and preserves original evidence.
7. Quality evaluation: scores investigations against curated test cases.

## Project Results
- 4 normalized events.
- 3 MITRE-enriched meta-alerts.
- 3 successful RAG investigations.
- 3 successful knowledge retrievals.
- 27/27 automated validation checks passed.
- Day 29 preliminary quality score: 100% across 3 curated cases.

The 100% score is from a small rule-based evaluation. It does not represent real-world AI accuracy.

## Limitations
- Small dataset of four lab or synthetic events.
- Only three meta-alert investigations.
- Raw data directory was empty during final review; no fresh raw-to-report replay was performed.
- Independent unit-test suite is not yet available.
- Automated checks do not prove every AI-generated statement is correct.
- Human analyst review is required.
- Research prototype, not a production-ready SOC platform.

## Validation Commands
```powershell
python src\rag_investigation_validator.py
python src\evidence_grounding_validator.py
python src\ai_quality_evaluator.py
```

## Research Reference
Ferazza, Melella, and Mersinas, From logs to tactics: Unsupervised reconstruction of APT campaigns with MITRE-enriched meta-alerts, International Journal of Information Security, 2026.
https://doi.org/10.1007/s10207-026-01254-w

Independent educational research implementation. Not an official implementation of the referenced paper.

## Disclaimer
For educational and research purposes. Review all outputs before using them for operational security decisions.
