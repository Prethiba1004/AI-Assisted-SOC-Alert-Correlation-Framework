
import pandas as pd


def normalize_log(event):

    host = event.get("host", {})
    event_data = event.get("event", {})
    user = event.get("user", {})

    normalized_event = {
        "timestamp": (
            event.get("timestamp")
            or event.get("TimeCreated")
            or event.get("@timestamp")
        ),

        "source": event.get("source", "Unknown"),

        "hostname": (
            event.get("hostname")
            or event.get("Computer")
            or host.get("name", "Unknown")
        ),

        "username": (
            event.get("username")
            or user.get("name", "Unknown")
        ),

        "event_id": (
            event.get("event_id")
            or event.get("EventID")
            or event_data.get("code")
        ),

        "description": (
            event.get("description")
            or event.get("Message")
            or event.get("message", "No description")
        )
    }

    return normalized_event


if __name__ == "__main__":

    sample_events = [

        {
            "TimeCreated": "2026-11-04 10:30:00",
            "Computer": "WINDOWS-LAB",
            "EventID": 1,
            "source": "Windows Sysmon",
            "username": "labuser",
            "Message": "PowerShell process created"
        },

        {
            "timestamp": "2026-11-04 10:35:00",
            "hostname": "KALI-LAB",
            "event_id": "sshd",
            "source": "Kali Linux",
            "username": "kaliuser",
            "message": "Failed password from 192.168.1.50"
        },

        {
            "@timestamp": "2026-11-04T10:40:00Z",
            "host": {"name": "WINDOWS-LAB"},
            "event": {"code": "4625"},
            "source": "Elastic Security",
            "user": {"name": "administrator"},
            "message": "Failed logon attempt detected"
        },

        {
            "timestamp": "2026-11-04 11:00:00",
            "hostname": "LINUX-TEST",
            "event_id": "TEST-USER-01",
            "source": "Correlation Test",
            "username": "labuser",
            "message": "Testing same username correlation"
        }

    ]

    normalized_events = []

    for event in sample_events:
        result = normalize_log(event)
        normalized_events.append(result)

    df = pd.DataFrame(normalized_events)

    output_file = "data/normalized/normalized_events.csv"

    df.to_csv(output_file, index=False)

    print("Total events processed:", len(df))
    print("\nNormalized Events:")
    print(df)

    print("\nCSV file saved successfully:", output_file)
