#!/usr/bin/env python3
"""
Attack Timeline Reconstruction.

Merges independent evidence sources (email gateway, EDR, file server
audit logs) into a single chronological timeline, tags each event with
its Cyber Kill Chain phase, and computes key IR metrics (dwell time,
time-to-first-detection, time-to-mass-impact) — the core analytical step
of any incident response investigation.

Usage:
    python3 timeline_reconstruction.py
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"

KILL_CHAIN_MAP = {
    "email_delivered": "Delivery",
    "attachment_opened_reported": "Exploitation",
    "suspicious_process_creation": "Exploitation",
    "network_connection": "Command & Control",
    "file_write": "Installation",
    "credential_access": "Actions on Objectives",
    "lateral_movement": "Actions on Objectives",
    "shadow_copy_deletion": "Actions on Objectives",
    "ransom_binary_execution": "Actions on Objectives",
    "mass_file_modification": "Actions on Objectives",
    "ransom_note_created": "Actions on Objectives",
}


def load_all_events():
    events = []
    for filename in ["email_gateway.json", "edr_alerts.json", "file_events.json"]:
        path = DATA_DIR / filename
        if path.exists():
            events.extend(json.loads(path.read_text()))
    for e in events:
        e["ts_parsed"] = datetime.fromisoformat(e["ts"])
        e["kill_chain_phase"] = KILL_CHAIN_MAP.get(e["event"], "Unclassified")
    return sorted(events, key=lambda e: e["ts_parsed"])


def compute_metrics(events):
    delivery = next((e for e in events if e["kill_chain_phase"] == "Delivery"), None)
    first_edr = next((e for e in events if e["source"] == "edr"), None)
    first_impact = next((e for e in events if e["event"] == "mass_file_modification"), None)

    metrics = {}
    if delivery and first_edr:
        metrics["time_to_first_detection"] = str(first_edr["ts_parsed"] - delivery["ts_parsed"])
    if delivery and first_impact:
        metrics["dwell_time_to_mass_impact"] = str(first_impact["ts_parsed"] - delivery["ts_parsed"])
    metrics["hosts_involved"] = sorted({e["host"] for e in events if "host" in e})
    metrics["sources_correlated"] = sorted({e["source"] for e in events})
    return metrics


def main():
    events = load_all_events()

    print(f"[*] Reconstructed timeline from {len(events)} events across {len({e['source'] for e in events})} independent sources\n")
    print(f"{'TIMESTAMP':<20}{'SOURCE':<14}{'KILL CHAIN PHASE':<22}{'EVENT'}")
    print("-" * 100)
    for e in events:
        ts = e["ts_parsed"].strftime("%H:%M:%S")
        print(f"{ts:<20}{e['source']:<14}{e['kill_chain_phase']:<22}{e['event']}")
        print(f"{'':<20}{'':<14}{'':<22}  {e['detail']}")
        if "mitre" in e:
            print(f"{'':<20}{'':<14}{'':<22}  MITRE ATT&CK: {e['mitre']}")

    metrics = compute_metrics(events)
    print("\n=== Incident Metrics ===")
    for k, v in metrics.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
