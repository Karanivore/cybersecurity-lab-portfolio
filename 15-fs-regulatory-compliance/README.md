# Lab 15 — Financial-Services Regulatory Compliance (DORA + NYDFS 500)

*Consultant / GRC track — Financial Services regulatory focus.*

Financial services is KPMG's largest sector, and FS clients operate under
overlapping cyber regulations with real enforcement teeth. This lab
assesses implementation against two of the most consequential — the **EU
Digital Operational Resilience Act (DORA)** and **NYDFS 23 NYCRR Part
500** — computing per-regulation and per-pillar compliance and generating
a regulatory gap assessment with recommended sequencing.

## Contents

| File | Purpose |
|---|---|
| `sample_data/regulatory_requirements.json` | 20 requirements across DORA's 5 pillars and NYDFS Part 500, each with implementation status and control owner |
| `scripts/reg_compliance.py` | Computes per-regulation and per-pillar compliance, lists open requirements, generates the gap assessment (with a single-regulation filter) |
| `regulatory_gap_assessment.md` | The generated deliverable: executive summary, compliance by regulation & pillar, remediation backlog, recommended sequencing, methodology |

## Regulations covered

- **DORA** (EU Regulation 2022/2554): ICT Risk Management, ICT Incident Management, Digital Operational Resilience Testing (incl. TLPT), ICT Third-Party Risk, Information Sharing
- **NYDFS Part 500** (as amended): cybersecurity program & policy, CISO governance, MFA, penetration testing, access privileges, encryption, incident response, 72-hour notification

## Usage

```bash
python3 scripts/reg_compliance.py
python3 scripts/reg_compliance.py --regulation DORA
python3 scripts/reg_compliance.py --report regulatory_gap_assessment.md
```

## Sample output

```
REGULATION    COMPLIANCE  MET   PART  GAP   TOTAL
------------------------------------------------------
DORA          33.3%       1     4     4     9
NYDFS_500     72.7%       5     6     0     11

Open requirements (14):
  [Not met] DORA-4.1      Maintain a register of all ICT third-party service arrangements
  [Not met] DORA-3.2      Threat-Led Penetration Testing (TLPT) at least every 3 years ...
```

The results reflect a realistic FS posture: relatively mature under the
longer-established NYDFS regime, but materially behind on the newer DORA
requirements (third-party register, TLPT, asset mapping) — exactly the
structural, long-lead gaps an FS regulatory consultant prioritizes.

## Skills demonstrated

- Financial-services cyber regulatory knowledge (DORA 5 pillars, NYDFS Part 500)
- Multi-regulation gap assessment and per-pillar scoring
- Prioritizing structural, long-lead regulatory gaps ahead of enforcement deadlines
- Harmonizing overlapping obligations (e.g. DORA vs. NYDFS incident-notification workflows)

## Resume bullet points

- *Performed a financial-services cyber regulatory gap assessment against EU DORA and NYDFS 23 NYCRR Part 500, scoring per-regulation and per-pillar compliance across 20 requirements.*
- *Identified DORA's ICT third-party register, threat-led penetration testing, and asset-mapping obligations as the priority structural gaps ahead of enforcement deadlines.*
- *Recommended harmonizing overlapping DORA and NYDFS incident-notification requirements into a single reporting workflow to reduce duplicated effort.*
