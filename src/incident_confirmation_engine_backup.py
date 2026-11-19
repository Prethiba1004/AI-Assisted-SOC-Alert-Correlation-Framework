import re
import json
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/synthetic/confirmed_incident_events.csv")
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
        events["timestamp"],
        errors="raise",
        utc=True
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

    matching_sequences = []

    for _, login in successful.iterrows():
        related_failures = failed[
            (failed["username"] == login["username"])
            & (failed["hostname"] == login["hostname"])
            & (failed["source_ip"] == login["source_ip"])
            & (failed["timestamp"] <= login["timestamp"])
        ]

        related_powershell = powershell[
            (powershell["username"] == login["username"])
            & (powershell["hostname"] == login["hostname"])
            & (powershell["timestamp"] > login["timestamp"])
        ]

        for _, process in related_powershell.iterrows():
            if (
                login["source_ip"]
                and len(related_failures) >= 3
            ):
                matching_sequences.append({
                    "username": login["username"],
                    "hostname": login["hostname"],
                    "source_ip": login["source_ip"],
                    "failed_login_count": len(related_failures),
                    "successful_login_time": login["timestamp"].isoformat(),
                    "powershell_time": process["timestamp"].isoformat()
                })

    confirmed = len(matching_sequences) > 0

    checks = {
        "at_least_three_failed_logins": any(
            item["failed_login_count"] >= 3
            for item in matching_sequences
        ),
        "successful_login_after_failures": confirmed,
        "same_account_host_and_source_ip": confirmed,
        "powershell_after_successful_login": confirmed
    }

    result = {
        "incident_id": "SYNTHETIC-INCIDENT-001",
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
        "analyst_review_required": True,
        "real_world_incident": False
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([{
        "incident_id": result["incident_id"],
        "scenario_type": result["scenario_type"],
        "incident_confirmation": result["incident_confirmation"],
        "confirmation_basis": result["confirmation_basis"],
        "failed_login_count": max(
            [x["failed_login_count"] for x in matching_sequences],
            default=0
        ),
        "source_ip": (
            matching_sequences[0]["source_ip"]
            if matching_sequences else "Not established"
        ),
        "analyst_review_required": result["analyst_review_required"],
        "real_world_incident": result["real_world_incident"]
    }]).to_csv(CSV_OUTPUT, index=False)

    with open(JSON_OUTPUT, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print("Events reviewed:", len(events))
    print("\nConfirmation checks:")

    for check, passed in checks.items():
        print(f"{check}: {'PASS' if passed else 'FAIL'}")

    print("\nIncident confirmation:", result["incident_confirmation"])
    print("Scenario:", result["scenario_type"])
    print("Analyst review required:", result["analyst_review_required"])
    print("Real-world incident:", result["real_world_incident"])
    print("\nCSV saved:", CSV_OUTPUT)
    print("JSON saved:", JSON_OUTPUT)


if __name__ == "__main__":
    main()
