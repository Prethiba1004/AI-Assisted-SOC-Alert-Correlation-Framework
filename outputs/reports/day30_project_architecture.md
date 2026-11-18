# AI-Assisted SOC Alert Correlation Framework
## Day 30 - Project Architecture Documentation

### 1. Project Overview

This project is a research prototype for assisting Security Operations Center (SOC) analysts with security event correlation, MITRE ATT&CK enrichment, knowledge retrieval and AI-assisted investigation.

The framework combines Python-based event processing, machine-learning experiments, graph analysis, Retrieval-Augmented Generation (RAG), and a Large Language Model (LLM).

### 2. Data Sources and Environment

- Windows Sysmon security events
- Kali Linux system and authentication logs
- Elastic Security alerts
- Python 3.12
- Pandas, scikit-learn and NetworkX
- Sentence Transformers
- Gemini LLM integration
- MITRE ATT&CK knowledge data

The project uses lab-generated and normalized security events.

### 3. Architecture and Processing Stages

#### Stage 1: Log Normalization

Main module: `src/log_normalizer.py`

Purpose:
- Convert security log records into a common event structure.
- Standardize fields such as timestamp, source, hostname, username, event ID and description.
- Store normalized events in `data/normalized/normalized_events.csv`.

#### Stage 2: Event Correlation and Feature Engineering

Relevant modules include:
- `src/event_correlator.py`
- `src/alert_vectorizer.py`
- `src/candidate_pair_selector.py`
- `src/candidate_graph_builder.py`
- `src/hybrid_similarity.py`

Techniques:
- TF-IDF feature extraction
- Sentence-BERT semantic embeddings
- DBSCAN and HDBSCAN clustering experiments
- Graph-based event relationship analysis
- Candidate pair selection
- Hybrid similarity analysis

The initial event correlator creates graph relationships based on shared hostname, shared username or timestamps within a ten-minute window. Later modules perform additional correlation and similarity analysis.

#### Stage 3: Correlation Explanation and MITRE Enrichment

Relevant modules:
- `src/alert_correlation_explainer.py`
- `src/mitre_technique_mapper.py`
- `src/meta_alert_generator.py`

Purpose:
- Explain relationships between correlated events.
- Apply rule-based MITRE ATT&CK technique mapping.
- Preserve uncertainty when evidence is insufficient.
- Generate uniquely identified MITRE-enriched meta-alerts.

PowerShell-related evidence can produce a potential T1059.001 mapping. Authentication failure evidence alone does not automatically establish T1110.

Incident confirmation remains Not confirmed unless independently established.

#### Stage 4: RAG Knowledge Retrieval

Relevant modules:
- `src/rag_document_loader.py`
- `src/rag_text_chunker.py`
- `src/rag_retriever.py`

Knowledge source:
- `data/knowledge_base/mitre_attack_knowledge.json`

Retrieval methods:
- TF-IDF similarity
- Keyword scoring
- Hybrid scoring

The retriever ranks relevant knowledge chunks and returns the top results for investigation.

Sentence-BERT is used in earlier semantic feature and similarity experiments. It is not the retrieval algorithm implemented in the current `rag_retriever.py`.

#### Stage 5: LLM-Assisted SOC Investigation

Main modules:
- `src/rag_meta_alert_investigator.py`
- `src/llm_client.py`

The investigation process:
1. Load MITRE-enriched meta-alerts.
2. Retrieve relevant MITRE knowledge.
3. Recover the original evidence for referenced events.
4. Extract IP addresses from individual event descriptions.
5. Build an evidence-grounded investigation prompt.
6. Request structured analysis from Gemini.
7. Validate the JSON response.
8. Check IP attribution against individual event evidence.
9. Save successful investigations and processing errors.

The six generated investigation fields are:
- AI explanation
- Evidence analysis
- MITRE analysis
- Investigation steps
- Limitations
- AI incident assessment

#### Stage 6: Validation and Quality Evaluation

Validation modules:
- `src/rag_investigation_validator.py`
- `src/evidence_grounding_validator.py`
- `src/ai_quality_evaluator.py`

Validation coverage:
- 12 RAG investigation checks
- 15 evidence-grounding checks
- Total: 27 automated checks

AI quality evaluation criteria:
- Evidence accuracy
- Technical correctness
- MITRE relevance
- Investigation usefulness
- Clarity

The quality evaluator uses a curated ground-truth dataset and rule-based checks. Human review remains mandatory.

### 4. Main Data Flow

Security log sources
    |
    v
Log normalization
    |
    v
Feature extraction and event correlation
    |
    v
Similarity analysis and graph processing
    |
    v
Correlation explanations
    |
    v
MITRE technique mapping
    |
    v
MITRE-enriched meta-alert generation
    |
    v
RAG knowledge retrieval
    |
    v
Gemini-assisted investigation
    |
    v
JSON and event-level IP validation
    |
    v
Investigation quality evaluation
    |
    v
CSV and TXT investigation reports

### 5. Important Project Outputs

Normalized data:
- `data/normalized/normalized_events.csv`
- `data/normalized/tfidf_features.csv`
- `data/normalized/sentence_bert_embeddings.csv`

Correlation and MITRE:
- `outputs/graphs/`
- `outputs/explanations/`
- `outputs/mitre/`
- `outputs/meta_alerts/`

RAG investigations:
- `outputs/soc_investigations/rag_meta_alert_investigation.csv`
- `outputs/soc_investigations/rag_meta_alert_investigation.txt`

Evaluation:
- `outputs/reports/day28_ai_quality_evaluation.csv`
- `outputs/reports/day29_ai_quality_evaluation.csv`
- `outputs/soc_investigations/evidence_grounding_validation.csv`

### 6. Day 30 Verification Results

The reviewed project outputs contain:
- 4 normalized security events
- 3 MITRE-enriched meta-alerts
- 3 successful RAG investigations
- 3 successful knowledge retrievals
- 27 out of 27 automated validation checks passed
- Day 29 preliminary AI quality evaluation: 100% across 3 curated cases

### 7. Research Limitations

1. The current normalized dataset contains only four lab or synthetic events.
2. The current investigation output contains three meta-alerts.
3. The raw data directory was empty during the earlier pipeline review. A fresh raw-log-to-report replay was not performed during final verification.
4. The tests directory is currently empty. Validation scripts are implemented under src, but a separate independent unit-test suite has not been established.
5. The Day 29 AI quality score is based on three curated cases and rule-based evaluation. It does not represent real-world AI accuracy or generalization.
6. Automated validation checks structural consistency and selected evidence relationships. They cannot establish the truth of every AI-generated statement.
7. MITRE technique mappings and incident confirmation require analyst review.
8. The framework is a research prototype, not a production-ready SOC platform.

### 8. Future Improvements

- Collect a larger dataset of real or safely simulated security events.
- Implement an independent unit-test suite.
- Add broader event-level evidence validation.
- Evaluate the framework using more diverse ground-truth cases.
- Compare retrieval and correlation performance on larger datasets.
- Measure false positives, false negatives, precision and recall.
- Conduct structured human analyst evaluations.
- Test a complete raw-log-to-report pipeline replay.

### 9. Conclusion

The project demonstrates a research workflow combining security event correlation, MITRE ATT&CK enrichment, RAG-based knowledge retrieval and LLM-assisted SOC investigation.

The final verification confirms successful processing of the existing three meta-alerts and passing results across 27 automated validation checks. Further evaluation on larger datasets and independent analyst review are necessary before drawing conclusions about real-world effectiveness.
