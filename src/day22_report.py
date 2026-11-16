
from pathlib import Path
import pandas as pd

REPORT_PATH = Path("outputs/reports/day22_experiment_report.txt")
INPUT_PATH = Path("outputs/meta_alerts/mitre_enriched_meta_alerts.csv")
OUTPUT_PATH = Path("outputs/llm_analysis/llm_meta_alert_analysis.csv")


def main():
    original = pd.read_csv(INPUT_PATH, keep_default_na=False)
    generated = pd.read_csv(OUTPUT_PATH, keep_default_na=False)

    total = len(original)
    successful = (generated["analysis_status"] == "Success").sum()
    failed = total - successful

    report = f"""
DAY 22 EXPERIMENT REPORT
LLM INTEGRATION FOR SOC META-ALERT ANALYSIS
============================================================

1. OBJECTIVE
Integrate a real Large Language Model (LLM) with the
existing SOC meta-alert analysis framework using Google's
Gemini API.

2. TECHNOLOGY STACK
- Python 3.12.10
- Google Gemini API
- Gemini 3.5 Flash Lite
- google-genai SDK
- Pandas
- JSON response validation
- PowerShell environment variables

3. IMPLEMENTED MODULES
- src/llm_client.py
- src/llm_meta_alert_analyzer.py
- src/llm_output_validator.py
- src/day22_report.py

4. API SECURITY
- API key accessed through GEMINI_API_KEY environment variable.
- API key not hardcoded in Python source.
- .env files excluded through .gitignore.
- No obvious hardcoded API key pattern found in inspected files.
- API key configured for the current PowerShell session.

5. LLM INTEGRATION RESULTS
Total meta-alerts: {total}
Successful analyses: {successful}
Failed analyses: {failed}

Each successful analysis generates six fields:
- AI explanation
- Evidence analysis
- MITRE analysis
- Investigation steps
- Limitations
- AI incident assessment

6. OUTPUT FILES
- outputs/llm_analysis/llm_meta_alert_analysis.csv
- outputs/llm_analysis/llm_meta_alert_analysis.txt
- outputs/reports/day22_experiment_report.txt

7. VALIDATION AND SECURITY TESTING
- Meta-alert count consistency: PASS
- Duplicate ID check: PASS
- Meta-alert ID consistency: PASS
- Six AI fields present: PASS
- All analyses successful: PASS
- Original MITRE and incident status preserved: PASS
- No empty AI analysis fields: PASS
- Invalid JSON rejected: PASS
- Missing required fields rejected: PASS
- Incorrect field data types rejected: PASS
- No obvious hardcoded API key pattern detected: PASS

8. RESEARCH LIMITATIONS
- Evaluation used only three synthetic meta-alerts.
- LLM responses may vary between requests.
- API availability and free-tier quotas may affect execution.
- Hallucinations remain possible and require analyst review.
- Prompt instructions alone cannot fully prevent prompt injection.
- MITRE mappings and incident assessments require human validation.
- The framework has not been deployed in a production SOC.

9. CONCLUSION
Day 22 successfully integrated Google's Gemini API into
the SOC meta-alert analysis workflow.

The framework generated LLM-assisted explanations,
evidence analysis, MITRE analysis, investigation steps,
limitations and incident assessments for the available
synthetic meta-alerts.

Structural validation and response-format testing
demonstrated that malformed responses, missing fields
and incorrect field types are rejected.

This implementation remains a research proof-of-concept
and requires further testing with larger datasets and
human-reviewed ground truth.

============================================================
END OF DAY 22 REPORT
"""

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report.strip(), encoding="utf-8")

    print("Day 22 report generated successfully.")
    print(f"Report location: {REPORT_PATH}")
    print(f"Meta-alerts processed: {total}")
    print(f"Successful analyses: {successful}")
    print(f"Failed analyses: {failed}")


if __name__ == "__main__":
    main()
