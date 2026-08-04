#!/usr/bin/env python3
"""
Lightweight SIEM Detection Engine.

Parses SSH auth logs, firewall logs, and web access logs, then runs a
small rule set (modeled on Sigma-style detections) to surface:

  - Port-scan reconnaissance (many distinct destination ports, one source)
  - SSH brute-force attempts (N+ failed logins from one source in a window)
  - Successful login immediately following a brute-force burst (compromise indicator)
  - SQL injection attempts in web request lines
  - Directory traversal attempts in web request lines

Each finding is mapped to a MITRE ATT&CK technique and given a severity.
Correlates alerts by source IP into an overall incident summary — the
same triage step a SOC analyst performs across SIEM data sources.

Usage:
    python3 detection_engine.py
    python3 detection_engine.py --json alerts.json
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"

BRUTE_FORCE_THRESHOLD = 5      # failed logins
BRUTE_FORCE_WINDOW_SEC = 120
PORT_SCAN_THRESHOLD = 8        # distinct ports
PORT_SCAN_WINDOW_SEC = 30

SQLI_PATTERNS = [
    r"union\s+select", r"or\s+1=1", r"'\s*or\s*'1'\s*=\s*'1", r"drop\s+table",
    r"--\s*$", r"union%20select", r"select\s+null",
]
TRAVERSAL_PATTERNS = [r"\.\./\.\./", r"%2e%2e%2f", r"etc/passwd", r"etc/shadow"]


def parse_auth_log(path: Path, year: int = 2026):
    events = []
    pattern = re.compile(
        r"^(?P<ts>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+sshd\[\S+\]:\s+(?P<msg>.+)$"
    )
    for line in path.read_text().splitlines():
        m = pattern.match(line)
        if not m:
            continue
        ts = datetime.strptime(f"{year} {m.group('ts')}", "%Y %b %d %H:%M:%S")
        msg = m.group("msg")
        fail = re.search(r"Failed password for(?: invalid user)? (\S+) from (\S+) port (\d+)", msg)
        success = re.search(r"Accepted (password|publickey) for (\S+) from (\S+) port (\d+)", msg)
        if fail:
            events.append({"ts": ts, "type": "auth_failed", "user": fail.group(1), "src_ip": fail.group(2)})
        elif success:
            events.append({"ts": ts, "type": "auth_success", "method": success.group(1), "user": success.group(2), "src_ip": success.group(3)})
    return events


def parse_firewall_log(path: Path):
    events = []
    pattern = re.compile(
        r"^(?P<ts>[\d-]+ [\d:]+)\s+SRC=(?P<src>\S+)\s+DST=(?P<dst>\S+)\s+SPT=\d+\s+DPT=(?P<dport>\d+)\s+PROTO=\S+\s+ACTION=(?P<action>\S+)"
    )
    for line in path.read_text().splitlines():
        m = pattern.match(line)
        if not m:
            continue
        ts = datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S")
        events.append({"ts": ts, "src_ip": m.group("src"), "dst_ip": m.group("dst"),
                        "dport": int(m.group("dport")), "action": m.group("action")})
    return events


def parse_web_log(path: Path):
    events = []
    pattern = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] "(?P<method>\S+) (?P<path>\S.*?) HTTP/[\d.]+" (?P<status>\d+) \d+ "[^"]*" "(?P<agent>[^"]*)"'
    )
    for line in path.read_text().splitlines():
        m = pattern.match(line)
        if not m:
            continue
        ts = datetime.strptime(m.group("ts"), "%d/%b/%Y:%H:%M:%S %z")
        events.append({"ts": ts, "src_ip": m.group("ip"), "path": m.group("path"),
                        "status": int(m.group("status")), "agent": m.group("agent")})
    return events


def detect_brute_force(auth_events):
    alerts = []
    by_ip = defaultdict(list)
    for e in auth_events:
        if e["type"] == "auth_failed":
            by_ip[e["src_ip"]].append(e["ts"])

    for ip, timestamps in by_ip.items():
        timestamps.sort()
        window = []
        for ts in timestamps:
            window.append(ts)
            window = [t for t in window if (ts - t).total_seconds() <= BRUTE_FORCE_WINDOW_SEC]
            if len(window) >= BRUTE_FORCE_THRESHOLD:
                alerts.append({
                    "rule": "SSH Brute Force", "severity": "HIGH", "mitre": "T1110.001 (Brute Force: Password Guessing)",
                    "src_ip": ip, "detail": f"{len(window)} failed SSH logins within {BRUTE_FORCE_WINDOW_SEC}s",
                    "first_seen": window[0].isoformat(), "last_seen": ts.isoformat(),
                })
                break
    return alerts


def detect_brute_force_then_success(auth_events):
    alerts = []
    by_ip_failed = defaultdict(list)
    for e in auth_events:
        if e["type"] == "auth_failed":
            by_ip_failed[e["src_ip"]].append(e["ts"])

    for e in auth_events:
        if e["type"] != "auth_success":
            continue
        fails = [t for t in by_ip_failed.get(e["src_ip"], []) if t < e["ts"] and (e["ts"] - t).total_seconds() <= 300]
        if len(fails) >= BRUTE_FORCE_THRESHOLD:
            alerts.append({
                "rule": "Successful Login Following Brute Force", "severity": "CRITICAL",
                "mitre": "T1078 (Valid Accounts) following T1110 (Brute Force)",
                "src_ip": e["src_ip"], "detail": f"Login as '{e['user']}' succeeded after {len(fails)} failed attempts from same source — likely account compromise",
                "ts": e["ts"].isoformat(),
            })
    return alerts


def detect_port_scan(fw_events):
    alerts = []
    by_ip = defaultdict(list)
    for e in fw_events:
        by_ip[e["src_ip"]].append(e)

    for ip, events in by_ip.items():
        events.sort(key=lambda e: e["ts"])
        window = []
        for e in events:
            window.append(e)
            window = [w for w in window if (e["ts"] - w["ts"]).total_seconds() <= PORT_SCAN_WINDOW_SEC]
            distinct_ports = {w["dport"] for w in window}
            if len(distinct_ports) >= PORT_SCAN_THRESHOLD:
                alerts.append({
                    "rule": "Port Scan", "severity": "MEDIUM", "mitre": "T1046 (Network Service Discovery)",
                    "src_ip": ip, "detail": f"{len(distinct_ports)} distinct destination ports probed within {PORT_SCAN_WINDOW_SEC}s",
                    "first_seen": window[0]["ts"].isoformat(), "last_seen": e["ts"].isoformat(),
                })
                break
    return alerts


def detect_web_attacks(web_events):
    alerts = []
    for e in web_events:
        path_lower = e["path"].lower()
        if any(re.search(p, path_lower) for p in SQLI_PATTERNS):
            alerts.append({
                "rule": "SQL Injection Attempt", "severity": "HIGH", "mitre": "T1190 (Exploit Public-Facing Application)",
                "src_ip": e["src_ip"], "detail": f"Suspicious query string: {e['path']}", "ts": e["ts"].isoformat(),
            })
        if any(re.search(p, path_lower) for p in TRAVERSAL_PATTERNS):
            alerts.append({
                "rule": "Directory Traversal Attempt", "severity": "HIGH", "mitre": "T1190 (Exploit Public-Facing Application)",
                "src_ip": e["src_ip"], "detail": f"Path traversal payload: {e['path']}", "ts": e["ts"].isoformat(),
            })
    return alerts


def correlate(alerts):
    by_ip = defaultdict(list)
    for a in alerts:
        by_ip[a["src_ip"]].append(a["rule"])
    correlated = []
    for ip, rules in by_ip.items():
        if len(set(rules)) >= 2:
            correlated.append({"src_ip": ip, "distinct_rules_triggered": sorted(set(rules)), "alert_count": len(rules)})
    return sorted(correlated, key=lambda c: -c["alert_count"])


def main():
    parser = argparse.ArgumentParser(description="Lightweight SIEM detection engine")
    parser.add_argument("--json", help="Write full alert output to this JSON file")
    args = parser.parse_args()

    auth_events = parse_auth_log(DATA_DIR / "auth.log")
    fw_events = parse_firewall_log(DATA_DIR / "firewall.log")
    web_events = parse_web_log(DATA_DIR / "web_access.log")

    alerts = []
    alerts += detect_port_scan(fw_events)
    alerts += detect_brute_force(auth_events)
    alerts += detect_brute_force_then_success(auth_events)
    alerts += detect_web_attacks(web_events)
    alerts.sort(key=lambda a: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[a["severity"]])

    print(f"[*] Parsed {len(auth_events)} auth events, {len(fw_events)} firewall events, {len(web_events)} web events")
    print(f"[*] {len(alerts)} alert(s) generated\n")

    for a in alerts:
        print(f"[{a['severity']:<8}] {a['rule']:<38} src={a['src_ip']:<15} {a['mitre']}")
        print(f"             {a['detail']}")

    correlated = correlate(alerts)
    if correlated:
        print("\n=== Correlated Incidents (multiple rule types, same source) ===")
        for c in correlated:
            print(f"  {c['src_ip']}: {c['alert_count']} alerts across {c['distinct_rules_triggered']}")

    if args.json:
        Path(args.json).write_text(json.dumps({"alerts": alerts, "correlated_incidents": correlated}, indent=2))
        print(f"\n[+] Full alert set written to {args.json}")


if __name__ == "__main__":
    main()
