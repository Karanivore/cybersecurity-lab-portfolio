# Lab 14 — Privacy & Data Protection Assessment (GDPR / CCPA)

*Consultant / GRC track — Privacy practice focus.*

Privacy is one of KPMG's largest advisory practices. This lab works from
a **Records of Processing Activities** register (GDPR Art. 30) and
evaluates each activity against the core data-protection requirements —
lawful basis, DPIA necessity, international-transfer safeguards,
retention — then assesses the data-subject-rights (DSAR) program and
generates a data protection assessment report.

## Contents

| File | Purpose |
|---|---|
| `sample_data/processing_activities.json` | A 6-activity RoPA (payroll, credit scoring, marketing analytics, CCTV, health underwriting, web form) plus a DSAR program record |
| `scripts/privacy_assessment.py` | Checks lawful basis (Art. 6/9), DPIA triggers & completion (Art. 35), transfer safeguards (Art. 44-49), retention (Art. 5), and DSAR timeliness; generates the report |
| `privacy_assessment_report.md` | The generated deliverable: executive summary, per-activity findings, DSAR review, priority remediation, methodology |

## Usage

```bash
python3 scripts/privacy_assessment.py
python3 scripts/privacy_assessment.py --report privacy_assessment_report.md
```

## Sample output

```
ACTIVITY  SEVERITY  DPIA                FINDINGS
--------------------------------------------------------------------------------
PA-02     HIGH      REQUIRED/MISSING    1
PA-03     HIGH      REQUIRED/MISSING    4
PA-05     none      required/done       0
--------------------------------------------------------------------------------
Compliant activities: 3/6  |  Privacy compliance score: 44.0%

DSAR program issues (2):
  - Average DSAR response time (41d) exceeds the 30-day statutory limit.
  - Rights not yet supported: objection.
```

The marketing-analytics activity (PA-03) correctly surfaces the classic
stacked failure — no lawful basis, missing DPIA for large-scale
profiling, an unsafeguarded international transfer, and no retention
period — the exact pattern a privacy assessor flags as top priority.

## Skills demonstrated

- GDPR fluency: Art. 6/9 lawful basis, Art. 35 DPIA triggers, Art. 44-49 transfers, Art. 5 storage limitation, Art. 30 RoPA
- Data-subject-rights (DSAR) program evaluation against the statutory clock
- Privacy risk triage across a processing-activity inventory
- Producing a data protection assessment deliverable with prioritized remediation

## Resume bullet points

- *Conducted a GDPR/CCPA data protection assessment across a Records of Processing Activities register, evaluating lawful basis, DPIA necessity, international-transfer safeguards, and retention for each activity.*
- *Identified high-risk processing (large-scale profiling without a DPIA or lawful basis and an unsafeguarded cross-border transfer) and prioritized remediation to bring the program into compliance.*
- *Assessed the data-subject-rights program against the statutory response clock and rights coverage, flagging a 41-day average response against the 30-day limit.*
