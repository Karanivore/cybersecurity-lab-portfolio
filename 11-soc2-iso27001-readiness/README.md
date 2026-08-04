# Lab 11 — SOC 2 / ISO 27001 Readiness Assessment & Remediation Roadmap

*Consultant / GRC track.*

The engagement a consultant runs *before* a client pays for a SOC 2 Type
II or ISO 27001 audit: a control-by-control readiness (gap) assessment
that scores audit-readiness, separates **control gaps** from **evidence
gaps** (a working control with no evidence still fails an audit), and
lays out a phased remediation roadmap sequenced to a 180-day audit runway.

## Contents

| File | Purpose |
|---|---|
| `sample_data/soc2_readiness.json` | 22 SOC 2 Trust Services Criteria (CC1–CC9, plus Availability & Confidentiality) with Met/Partial/Not-met status, evidence flag, owner, effort, and ISO 27001:2022 cross-reference |
| `scripts/readiness.py` | Computes overall + per-category readiness, separates control gaps from evidence gaps, generates the report + prioritized roadmap |
| `readiness_report.md` | The generated deliverable: executive summary, readiness by category, control status detail, evidence-gap list, phased remediation roadmap, methodology |

## Usage

```bash
python3 scripts/readiness.py
python3 scripts/readiness.py --report readiness_report.md
```

## Sample output

```
Overall readiness score: 54.5%
Controls: 6 met / 12 partial / 4 not met  (of 22)
Control gaps: 16   |   Evidence gaps (control OK but no evidence): 6

CATEGORY                      SCORE   CONTROLS
--------------------------------------------------
Control Environment           100.0%  2
Monitoring Activities         0.0%    1
Logical & Physical Access     50.0%   5
Risk Mitigation               25.0%   2
...
```

## Skills demonstrated

- SOC 2 Trust Services Criteria and ISO 27001:2022 Annex A control knowledge
- Readiness / gap assessment methodology ahead of a formal audit
- The auditor-critical distinction between **control effectiveness** and **evidence availability**
- Building a phased, owner-assigned, effort-sequenced remediation roadmap
- Dual-framework efficiency (one remediation supporting both SOC 2 and ISO 27001)

## Resume bullet points

- *Performed a SOC 2 Type II readiness assessment across 22 Trust Services Criteria, quantifying 54% audit-readiness and separating control gaps from evidence gaps ahead of a formal examination.*
- *Built a readiness-scoring tool that generates a phased, owner-assigned remediation roadmap sequenced by control severity and implementation effort against a 180-day audit runway.*
- *Cross-referenced every SOC 2 criterion to ISO 27001:2022 Annex A so a single remediation program advances both certifications simultaneously.*
