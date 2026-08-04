# Security Incident Report — INC-2026-0722-01

**Classification:** Confirmed Compromise
**Severity:** Critical
**Analyst:** SOC Log Analysis Lab (automated detection engine + manual triage)
**Date of report:** 2026-07-22
**Affected asset:** `web01` (10.0.0.5)

---

## 1. Executive Summary

Between 03:10 and 03:16 UTC on 2026-07-22, source IP `203.0.113.55` conducted
a full attack chain against `web01`: a TCP port scan for reconnaissance, an
SSH brute-force attack that succeeded in compromising the `root` account, and
a follow-on web application attack (SQL injection and directory traversal
probing) using automated tooling (`sqlmap`). All four stages were detected
and correlated to a single source IP by the SIEM detection engine
(`scripts/detection_engine.py`), producing 9 alerts across firewall, SSH
auth, and web access logs.

**Impact:** Root-level SSH access was obtained. Treat as full host
compromise until forensic validation proves otherwise.

## 2. Timeline (UTC)

| Time | Source | Event |
|---|---|---|
| 03:10:00 – 03:10:04 | firewall.log | 20-port TCP scan from `198.51.100.7` (scanning tool, separate recon source) |
| 03:13:11 – 03:14:12 | auth.log | 9 failed SSH logins from `203.0.113.55` against `ubuntu`, `root`, `oracle`, `admin` |
| 03:14:20 | auth.log | **Successful SSH login as `root`** from `203.0.113.55` — brute force succeeded |
| 03:14:22 | auth.log | Interactive session opened for `root` |
| 03:16:00 – 03:16:02 | web_access.log | 4x SQL injection payloads (`UNION SELECT`, `OR '1'='1'`, `DROP TABLE`) via `sqlmap/1.7` user agent, from the same source IP |
| 03:16:02 | web_access.log | Directory traversal attempt for `/etc/passwd` (403, blocked) |

## 3. Detection Coverage

| Detection Rule | MITRE ATT&CK | Severity | Result |
|---|---|---|---|
| SSH Brute Force | T1110.001 – Brute Force: Password Guessing | HIGH | Triggered — 9 failures in <70s |
| Successful Login Following Brute Force | T1078 – Valid Accounts | CRITICAL | Triggered — root login 8s after last failure |
| SQL Injection Attempt | T1190 – Exploit Public-Facing Application | HIGH | Triggered — 4 payloads |
| Directory Traversal Attempt | T1190 – Exploit Public-Facing Application | HIGH | Triggered — 2 payloads |
| Port Scan (separate actor) | T1046 – Network Service Discovery | MEDIUM | Triggered — 8+ distinct ports in 30s |

## 4. Indicators of Compromise (IOCs)

- `203.0.113.55` — brute force + web attack source (block at perimeter, hunt for lateral movement)
- `198.51.100.7` — reconnaissance scanner (monitor / block)
- User agent `sqlmap/1.7` on inbound web requests
- SSH auth success for `root` at `03:14:20` from an external IP outside the corporate allow-list

## 5. Root Cause

- SSH exposed to the internet with password authentication enabled and no
  account lockout / rate limiting, allowing an unthrottled brute-force
  attempt to succeed against a weak `root` credential.
- Web application does not parameterize the `id`, `user`, and `q` query
  parameters, permitting SQL injection.

## 6. Remediation (mapped to NIST SP 800-61 containment/eradication/recovery)

1. **Contain:** Block `203.0.113.55` and `198.51.100.7` at the perimeter firewall; force-terminate active sessions for `root` on `web01`.
2. **Eradicate:** Rotate all credentials on `web01`, especially `root`; audit for added SSH keys, cron jobs, or new user accounts left by the attacker.
3. **Recover:** Disable SSH password authentication (key-based only), enforce `fail2ban`/rate limiting, and disable direct `root` SSH login (`PermitRootLogin no`).
4. **Application fix:** Parameterize all SQL queries / use an ORM; add WAF rules for the `UNION SELECT`, `OR 1=1`, and `../` traversal patterns.
5. **Detection improvement:** Alert threshold of 5 failed logins/2 min proved effective — tune down to 3/min for internet-facing hosts and add automatic IP blocking on trigger.

## 7. Lessons Learned

The port scan at 03:10 and the brute force at 03:13 originated from
different source IPs, suggesting either two separate actors or scan/attack
infrastructure separation — correlation logic should not assume a single
actor IP across the full kill chain, but should still flag temporal
proximity across sources against the same destination as a compound risk
signal for future tuning.
