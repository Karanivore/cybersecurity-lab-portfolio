# After-Action Report — INC-2026-0614-RANSOM

**Incident type:** Ransomware (phishing-initiated)
**Severity:** Sev-1 (confirmed mass encryption)
**Duration:** Delivery to mass impact in 22 minutes
**Playbook applied:** `ransomware_ir_playbook.md`

---

## Summary

A phishing email delivered a macro-enabled Word document to
`j.rivera@corp.local` at 09:02. The user enabled macros at 09:08, which
launched an obfuscated PowerShell command, established C2 to
`185.220.101.47`, dropped a secondary payload, harvested credentials from
LSASS, moved laterally to file server `FS-01` using delegated
domain-admin credentials, deleted volume shadow copies, and executed a
ransomware binary — encrypting 3,000 files across the finance share
within 5 minutes and dropping ransom notes at 14 share roots. Total dwell
time from delivery to mass impact was **22 minutes**; EDR raised its
first alert 7 minutes after delivery.

## Timeline

Reconstructed by `scripts/timeline_reconstruction.py` from three
independent sources (email gateway, EDR, file server audit) — see full
output in that script's usage section of the README. Key milestones:

| Time | Phase | Event |
|---|---|---|
| 09:02 | Delivery | Phishing email delivered |
| 09:08 | Exploitation | Macro enabled by user |
| 09:09 | Exploitation | PowerShell spawned from Word |
| 09:10 | Command & Control | C2 beacon established |
| 09:13 | Actions on Objectives | Credential access (LSASS) |
| 09:20 | Actions on Objectives | Lateral movement to FS-01 |
| 09:22 | Actions on Objectives | Shadow copies deleted |
| 09:23 | Actions on Objectives | Ransomware executed |
| 09:24–09:25 | Actions on Objectives | Mass encryption + ransom notes |

## Response Actions Taken (mapped to playbook phases)

- **Containment:** WKS-0231 and FS-01 isolated via EDR at T+26 min; `j.rivera` account disabled and credentials rotated; C2 IP blocked at the perimeter.
- **Eradication:** Dropped binaries and scheduled-task persistence removed from both hosts; macro execution policy tightened org-wide.
- **Recovery:** Finance share restored from the last verified-clean backup (T-18 hours, predates compromise); FS-01 rebuilt from a known-good image rather than cleaned in place.

## Root Cause

A domain user's account held **delegated domain-admin rights** it did
not need for daily work, which the attacker used to move laterally to
the file server within 12 minutes of initial exploitation. Macro
execution was permitted from internet-sourced documents with no
attachment sandboxing at the email gateway.

## Key Metrics

| Metric | Value |
|---|---|
| Time to first detection (EDR alert after delivery) | 7 minutes |
| Dwell time to mass impact | 22 minutes |
| Hosts affected | 2 (WKS-0231, FS-01) |
| Files encrypted | ~3,000 |
| Data restored from backup | 100% (no ransom paid) |
| Estimated recovery time | 6 hours (rebuild + restore) |

## Corrective Actions (owners assigned in original engagement)

1. **Remove standing domain-admin delegation** from individual user accounts; require just-in-time elevation (PAM solution). — *Highest priority, addresses root cause.*
2. **Block macro execution** for Office files originating from the internet by default (Group Policy / ASR rules).
3. **Add email attachment sandboxing** at the gateway for `.docm`/`.xlsm`/other macro-enabled formats.
4. **Add SIEM detection rule** for `vssadmin delete shadows` and similar shadow-copy-deletion commands (immediate Sev-1 trigger) — extends the detection engine built in Lab 2.
5. **Reduce EDR-to-containment time**: 26 minutes from first EDR alert to isolation is too slow for ransomware; target automated isolation on high-confidence ransomware precursor alerts.

## Lessons Learned

Time-to-detect (7 min) was reasonable, but time-to-contain (26 min from
first alert) allowed the attacker to complete the entire kill chain
before isolation. The single highest-leverage fix is removing standing
privileged access, which would have stopped lateral movement to FS-01
even if every earlier step succeeded.
