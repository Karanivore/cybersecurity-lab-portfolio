# Lab 2 — SOC Log Analysis & SIEM Detection Engine

A miniature SIEM built from scratch: a synthetic multi-source log
generator, a Python detection/correlation engine implementing five
Sigma-style rules mapped to MITRE ATT&CK, and a full incident report
written from the engine's output — the actual deliverable a SOC Tier 1/2
analyst produces.

## Contents

| File | Purpose |
|---|---|
| `scripts/generate_logs.py` | Deterministically generates realistic, timestamp-correlated `auth.log`, `firewall.log`, and `web_access.log` containing one embedded attack chain plus benign background traffic |
| `scripts/detection_engine.py` | Parses all three log sources, applies detection rules, correlates alerts by source IP, outputs a triaged alert list (console + JSON) |
| `sample_data/*.log` | Generated log files used by the engine |
| `incident_report_sample.md` | Full incident report (executive summary, timeline, IOCs, MITRE mapping, NIST 800-61 remediation) written from the engine's findings |

## The scenario

A single attacker (`203.0.113.55`) port-scans a web host, brute-forces SSH,
successfully logs in as `root`, then pivots to attacking the web app with
`sqlmap`-driven SQL injection and directory traversal — a realistic,
compressed kill chain interleaved with normal user/admin traffic so
detections have to separate signal from noise, exactly like a live SIEM feed.

## Detection rules implemented

| Rule | MITRE ATT&CK | Severity |
|---|---|---|
| SSH Brute Force (5+ failures / 2 min, one source) | T1110.001 | HIGH |
| Successful login immediately following brute force | T1078 | CRITICAL |
| Port scan (8+ distinct ports / 30s, one source) | T1046 | MEDIUM |
| SQL injection in web request (`UNION SELECT`, `OR 1=1`, `DROP TABLE`, etc.) | T1190 | HIGH |
| Directory traversal in web request (`../../`, `/etc/passwd`) | T1190 | HIGH |

Alerts from the same source IP across multiple rule types are automatically
correlated into a single incident, mirroring how a SOC analyst pivots from
isolated alerts to a confirmed compromise narrative.

## Usage

```bash
# 1. Regenerate the synthetic log corpus (optional — already committed)
python3 scripts/generate_logs.py

# 2. Run detection + correlation
python3 scripts/detection_engine.py
python3 scripts/detection_engine.py --json alerts.json
```

## Sample output

```
[*] Parsed 15 auth events, 74 firewall events, 50 web events
[*] 9 alert(s) generated

[CRITICAL] Successful Login Following Brute Force src=203.0.113.55    T1078 (Valid Accounts) following T1110 (Brute Force)
             Login as 'root' succeeded after 9 failed attempts from same source — likely account compromise
[HIGH    ] SSH Brute Force                        src=203.0.113.55    T1110.001 (Brute Force: Password Guessing)
             5 failed SSH logins within 120s
[HIGH    ] SQL Injection Attempt                  src=203.0.113.55    T1190 (Exploit Public-Facing Application)
             Suspicious query string: /product?id=1 UNION SELECT username,password FROM users--
...
=== Correlated Incidents (multiple rule types, same source) ===
  203.0.113.55: 8 alerts across ['Directory Traversal Attempt', 'SQL Injection Attempt', 'SSH Brute Force', 'Successful Login Following Brute Force']
```

See [`incident_report_sample.md`](./incident_report_sample.md) for the
full write-up produced from this output.

## Skills demonstrated

- Log parsing across heterogeneous formats (syslog, iptables/netfilter, combined log format) with regex
- Time-windowed correlation logic (sliding window brute-force / port-scan detection)
- Detection engineering — writing and tuning rules, mapping to MITRE ATT&CK
- Multi-source alert correlation and incident triage
- Incident report writing aligned to NIST SP 800-61 (containment / eradication / recovery)

## Resume bullet points

- *Built a Python-based log correlation engine parsing SSH, firewall, and web server logs to detect brute-force, port-scan, and web-application attacks, mapping each detection to MITRE ATT&CK techniques.*
- *Implemented sliding-window correlation logic that automatically links reconnaissance, credential compromise, and web exploitation alerts from disparate log sources into a single incident timeline.*
- *Authored a full incident response report (executive summary, IOC list, NIST 800-61-aligned remediation plan) from raw log data for a simulated SSH brute-force-to-compromise scenario.*
