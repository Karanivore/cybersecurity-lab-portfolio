# Lab 4 — Incident Response Playbook & Attack Timeline Reconstruction

A reusable, NIST SP 800-61-aligned ransomware IR playbook, plus a Python
timeline-reconstruction tool that merges independent evidence sources
(email gateway, EDR, file server audit logs) into a single chronological
attack narrative — the core analytical deliverable of any real incident
response engagement — applied to a simulated ransomware incident.

## Contents

| File | Purpose |
|---|---|
| `ransomware_ir_playbook.md` | Reusable playbook: roles, containment/eradication/recovery steps, decision tree, communication templates (NIST SP 800-61 lifecycle) |
| `scripts/generate_incident_data.py` | Generates three independent, timestamp-correlated synthetic evidence sources describing a phishing → macro → C2 → lateral movement → ransomware kill chain |
| `scripts/timeline_reconstruction.py` | Merges all sources into one chronological timeline, tags each event with its Cyber Kill Chain phase, computes dwell-time / time-to-detect metrics |
| `sample_data/*.json` | Generated evidence sources |
| `after_action_report.md` | Full after-action report applying the playbook to the reconstructed incident: root cause, metrics, corrective actions |

## Usage

```bash
python3 scripts/generate_incident_data.py     # regenerate evidence (already committed)
python3 scripts/timeline_reconstruction.py    # merge sources, print timeline + metrics
```

## Sample output

```
[*] Reconstructed timeline from 16 events across 3 independent sources

TIMESTAMP           SOURCE        KILL CHAIN PHASE      EVENT
----------------------------------------------------------------------------------------------------
09:02:00            email_gateway Delivery              email_delivered
                                                          Invoice_Overdue_June.docm delivered to j.rivera@corp.local ...
09:09:00            edr           Exploitation          suspicious_process_creation
                                                          WINWORD.EXE spawned powershell.exe -enc <base64> (macro-triggered)
                                                          MITRE ATT&CK: T1566.001 / T1059.001
...
=== Incident Metrics ===
  time_to_first_detection: 0:07:00
  dwell_time_to_mass_impact: 0:22:00
  hosts_involved: ['FS-01', 'WKS-0231']
  sources_correlated: ['edr', 'email_gateway', 'file_audit']
```

## Skills demonstrated

- Incident response process design aligned to NIST SP 800-61 (Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned)
- Multi-source evidence correlation and chronological timeline reconstruction
- Cyber Kill Chain phase classification and MITRE ATT&CK technique mapping
- Root-cause analysis and metric-driven after-action reporting (dwell time, time-to-detect)
- Playbook authorship usable by a real SOC/IR team, not just a one-off narrative

## Resume bullet points

- *Authored a NIST SP 800-61-aligned ransomware incident response playbook covering containment, eradication, recovery, and stakeholder communication templates.*
- *Built a Python tool that merges evidence from three independent sources (email gateway, EDR, file audit logs) into a unified, kill-chain-classified attack timeline, computing dwell-time and time-to-detect metrics automatically.*
- *Produced a full after-action report identifying standing privileged access as root cause of a simulated ransomware incident's lateral movement, with prioritized corrective actions.*
