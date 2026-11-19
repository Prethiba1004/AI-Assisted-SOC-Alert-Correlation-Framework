# Synthetic SOC Incident Confirmation Workflow

## 1. Purpose
This module demonstrates how a SOC analyst can evaluate multiple related security events before assigning an incident confirmation status.

## 2. Synthetic Event Scenario
The positive test contains five manually created events:
- Three failed Windows logon events (Event ID 4625).
- One successful Windows logon event (Event ID 4624).
- One PowerShell process execution event (Sysmon Event ID 1).

All events use the same synthetic account, hostname, and source IP.

## 3. Confirmation Conditions
The demonstration engine evaluates four conditions:

1. At least three failed logins.
2. A successful login after previous failed logins for the same account and host.
3. The failed and successful logins share the same account, host, and source IP.
4. PowerShell execution occurs after the successful login for the same account and host.

All four conditions must pass for the synthetic scenario to receive the status Confirmed.

The three-failure threshold is a configurable demonstration rule, not a universal SOC standard.

## 4. Test Results

| Test | Events | Result |
|---|---:|---|
| Positive synthetic scenario | 5 | Confirmed |
| Negative synthetic scenario | 3 | Not confirmed |

Positive test: all four conditions passed.

Negative test: only one failed login was present. The threshold condition failed, while the other three conditions passed.

## 5. Output Files
- data/synthetic/confirmed_incident_events.csv
- data/synthetic/negative_test_events.csv
- outputs/synthetic_incidents/incident_confirmation_results.csv
- outputs/synthetic_incidents/incident_confirmation_results.json
- outputs/synthetic_incidents/negative_test_results.csv
- outputs/synthetic_incidents/negative_test_results.json

## 6. Relationship to the Main SOC Pipeline
This is a separate synthetic demonstration module. It does not overwrite or automatically confirm the three existing MITRE-enriched meta-alerts.

The original meta-alerts remain Not confirmed because their available evidence does not satisfy the synthetic demonstration conditions or establish a real incident.

## 7. Limitations and Safety
- The events are manually authored synthetic records, not live security telemetry.
- The engine uses predefined rule-based conditions.
- A successful login after failed attempts does not independently prove account compromise.
- PowerShell execution requires further investigation to establish malicious intent.
- The current engine is an educational prototype, not a production incident-response decision system.
- Human analyst review is required before any operational incident declaration.

## 8. Conclusion
The demonstration shows how multiple related events can be evaluated together, how missing evidence can prevent confirmation, and why a SOC analyst must preserve uncertainty and validate evidence before declaring an incident.
