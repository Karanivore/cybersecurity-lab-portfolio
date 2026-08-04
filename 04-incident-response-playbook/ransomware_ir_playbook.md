# Incident Response Playbook — Ransomware

**Framework:** NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide)
**Scope:** Any confirmed or suspected ransomware activity (mass file
encryption, ransom note deployment, or precursor activity — e.g. known
ransomware-affiliated loader/dropper detected) on any corporate endpoint
or server.

---

## 1. Preparation

- **Roles:** Incident Commander (IC), SOC Analyst (triage/containment), IT Ops (isolation/recovery), Communications Lead (internal/legal/exec updates), optional external DFIR retainer.
- **Pre-staged tooling:** EDR isolation capability, offline/immutable backups verified restorable, network segmentation maps, current asset inventory, contact tree (24/7 on-call).
- **Pre-approved actions:** IC has standing authority to isolate any single host without additional approval; isolating a full subnet/VLAN requires IT Ops Manager sign-off; public communication requires Legal + Comms sign-off.

## 2. Identification

Triggers that open an incident ticket:
- EDR/AV alert for known ransomware family, dropper, or LOLBin abuse (e.g. `vssadmin delete shadows`, mass `certutil` downloads)
- Helpdesk reports of inaccessible files / ransom notes from multiple users
- Anomalous spike in file-modification rate on file servers (SIEM correlation rule)
- Phishing report immediately followed by EDR process-creation alert on the same host

**On trigger:** SOC Analyst validates the alert is not a false positive,
assigns severity, and pages the IC within 15 minutes for anything scoring
Medium or above.

## 3. Containment

**Short-term (minutes):**
1. Isolate affected host(s) from the network via EDR (keep powered on — do not shut down; volatile memory may hold keys/IOCs).
2. Disable the compromised user account(s) and force credential rotation.
3. Block identified C2 IPs/domains at the perimeter firewall/DNS sinkhole.
4. Snapshot/preserve affected systems for forensics before any remediation.

**Long-term:**
5. Identify patient zero and lateral-movement path via EDR process tree + auth logs.
6. Isolate the broader network segment if lateral movement beyond the initial host is confirmed.
7. Disable any scheduled tasks / persistence mechanisms found in the process tree.

## 4. Eradication

1. Remove malware/persistence artifacts identified during containment (scheduled tasks, registry run keys, dropped binaries).
2. Patch or reconfigure the initial access vector (e.g. disable macro execution, patch the exploited CVE, revoke the phished credential).
3. Rotate all credentials with any exposure on affected hosts, including service accounts.

## 5. Recovery

1. Restore encrypted data from the most recent verified-clean, immutable backup — never restore from backups taken after the estimated compromise time.
2. Rebuild affected hosts from known-good images rather than cleaning in place where feasible.
3. Re-enable network access in stages, monitoring closely for re-infection signals.
4. Validate business functions with system owners before declaring recovery complete.

## 6. Lessons Learned (post-incident, within 5 business days)

- Blameless retrospective: what detection worked, what was missed, and why.
- Update detection rules (see Lab 2's detection engine as an example of the artifact this produces) based on observed TTPs.
- Update this playbook with any process gaps found during the response.
- Track time-to-detect and time-to-contain as metrics for the after-action report.

## Decision Tree (abbreviated)

```
Alert fires
  ├─ Confirmed ransomware indicator (encryption, ransom note, known family)?
  │    ├─ YES → Immediate isolation, page IC, start incident ticket (Sev-1)
  │    └─ NO  → Precursor indicator only (dropper/LOLBin)?
  │              ├─ YES → Isolate host, investigate before wider declaration (Sev-2)
  │              └─ NO  → Standard alert triage (not this playbook)
```

## Communication templates

**Internal exec update (first hour):** "We have identified [ransomware
activity / precursor activity] on [N] host(s) in [environment]. Affected
systems have been isolated. No [confirmed data exfiltration /
confirmation pending]. Next update in [X] hours."

**Post-incident summary (to leadership):** Scope, timeline, root cause,
data impact, recovery time, cost estimate, and remediation commitments —
see `after_action_report.md` for a full example.
