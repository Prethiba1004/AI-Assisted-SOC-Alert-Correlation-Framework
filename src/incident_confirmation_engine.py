import re
import json
import sys
from pathlib import Path

import pandas as pd

INPUT_FILE = Path(
    sys.argv[1] if len(sys.argv) > 1
    else "data/synthetic/confirmed_incident_events.csv"
)

OUTPUT_DIR = Path("outputs/synthetic_incidents")
CSV_OUTPUT = OUTPUT_DIR / "incident_confirmation_results.csv"
JSON_OUTPUT = OUTPUT_DIR / "incident_confirmation_results.json"


def extract_ip(description):
    match = re.search(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        str(description)
    )
    return match.group(0) if match else None


def main():
    print("\nSYNTHETIC SOC INCIDENT CONFIRMATION ENGINE")
    print("=" * 55)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    events = pd.read_csv(
        INPUT_FILE,
        encoding="utf-8-sig",
        keep_default_na=False
    )

    required = [
        "timestamp", "source", "hostname",
        "username", "event_id", "description"
    ]

    if not all(column in events.columns for column in required):
        raise ValueError("Synthetic event dataset has missing columns.")

    events["timestamp"] = pd.to_datetime(
        events["timestamp"], errors="raise", utc=True
    )
    events["event_id"] = events["event_id"].astype(str)

    failed = events[events["event_id"] == "4625"].copy()
    successful = events[events["event_id"] == "4624"].copy()

    powershell = events[
        (events["event_id"] == "1")
        & events["description"].str.contains(
            "powershell", case=False, na=False
        )
    ].copy()

    failed["source_ip"] = failed["description"].apply(extract_ip)
    successful["source_ip"] = successful["description"].apply(extract_ip)

    candidates = []

    for _, login in successful.iterrows():
        identity_failures = failed[
            (failed["username"] == login["username"])
            & (failed["hostname"] == login["hostname"])
            & (failed["timestamp"] <= login["timestamp"])
        ]

        related_failures = identity_failures[
            (identity_failures["source_ip"] == login["source_ip"])
            & (identity_failures["source_ip"].notna())
            & (login["source_ip"] is not None)
        ]

        related_powershell = powershell[
            (powershell["username"] == login["username"])
            & (powershell["hostname"] == login["hostname"])
            & (powershell["timestamp"] > login["timestamp"])
        ]

        candidates.append({
            "username": login["username"],
            "hostname": login["hostname"],
            "source_ip": login["source_ip"],
            "failed_login_count": len(related_failures),
            "has_failed_login": len(identity_failures) > 0,
            "has_matching_ip_failure": len(related_failures) > 0,
            "has_powershell": len(related_powershell) > 0,
            "successful_login_time": login["timestamp"].isoformat(),
            "powershell_times": [
                item.isoformat()
                for item in related_powershell["timestamp"]
            ]
        })

    checks = {
        "at_least_three_failed_logins": any(
            item["failed_login_count"] >= 3 for item in candidates
        ),
        "successful_login_after_failures": any(
            item["has_failed_login"] for item in candidates
        ),
        "same_account_host_and_source_ip": any(
            item["has_matching_ip_failure"]
            for item in candidates
        ),
        "powershell_after_successful_login": any(
            item["has_powershell"] for item in candidates
        )
    }

    confirmed = all(checks.values())

    matching_sequences = []

    if confirmed:
        for item in candidates:
            if (
                item["failed_login_count"] >= 3
                and item["has_failed_login"]
                and item["has_matching_ip_failure"]
                and item["has_powershell"]
            ):
                matching_sequences.append({
                    "username": item["username"],
                    "hostname": item["hostname"],
                    "source_ip": item["source_ip"],
                    "failed_login_count": item["failed_login_count"],
                    "successful_login_time": item["successful_login_time"],
                    "powershell_times": item["powershell_times"]
                })

    best_candidate = max(
        candidates,
        key=lambda item: item["failed_login_count"],
        default={}
    )

    result = {
        "incident_id": (
            "SYNTHETIC-INCIDENT-001"
            if "confirmed" in INPUT_FILE.name
            else "SYNTHETIC-NEGATIVE-TEST-001"
        ),
        "scenario_type": "Synthetic lab demonstration",
        "incident_confirmation": (
            "Confirmed" if confirmed else "Not confirmed"
        ),
        "confirmation_basis": (
            "All predefined synthetic evidence conditions passed."
            if confirmed else
            "One or more required evidence conditions were not met."
        ),
        "checks": checks,
        "matching_sequences": matching_sequences,
        "total_events_reviewed": len(events),
        "failed_login_count": best_candidate.get(
            "failed_login_count", 0
        ),
        "source_ip": best_candidate.get(
            "source_ip"
        ) or "Not established",
        "analyst_review_required": True,
        "real_world_incident": False
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if "negative_test" in INPUT_FILE.name:
        csv_output = OUTPUT_DIR / "negative_test_results.csv"
        json_output = OUTPUT_DIR / "negative_test_results.json"
    else:
        csv_output = CSV_OUTPUT
        json_output = JSON_OUTPUT

    pd.DataFrame([{
        key: value
        for key, value in result.items()
        if key not in ("checks", "matching_sequences")
    }]).to_csv(csv_output, index=False)

    with open(json_output, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print("Input dataset:", INPUT_FILE)
    print("Events reviewed:", len(events))
    print("\nConfirmation checks:")

    for check, passed in checks.items():
        print(f"{check}: {'PASS' if passed else 'FAIL'}")

    print("\nIncident confirmation:", result["incident_confirmation"])
    print("Analyst review required:", result["analyst_review_required"])
    print("Real-world incident:", result["real_world_incident"])
    print("\nCSV saved:", csv_output)
    print("JSON saved:", json_output)


if __name__ == "__main__":
    main()
