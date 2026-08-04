# Lab 07 — NIST CSF 2.0 Cybersecurity Maturity Assessment

*Consultant / GRC track.*

The flagship deliverable of a cyber advisory engagement: a maturity
assessment scoring an organization against the **NIST Cybersecurity
Framework 2.0** (all six Functions — Govern, Identify, Protect, Detect,
Respond, Recover), with a gap analysis and a prioritized remediation
roadmap. The Python toolkit ingests a scored assessment and
auto-generates the client-ready report.

## Contents

| File | Purpose |
|---|---|
| `sample_data/assessment_responses.json` | Category-level maturity scores (current vs. target, 1-5 scale) across all 22 NIST CSF 2.0 categories, with assessor observations |
| `scripts/csf_maturity.py` | Computes Function/overall scores, ranks gaps, renders a heat map, and generates the full Markdown report |
| `sample_maturity_assessment_report.md` | The generated client deliverable: executive summary, results, category detail, 12-month remediation roadmap, methodology |

## Usage

```bash
python3 scripts/csf_maturity.py                                   # console summary + heat map
python3 scripts/csf_maturity.py --report sample_maturity_assessment_report.md
```

Point `assessment_responses.json` at a real client's scored assessment
to generate their report — the tool is data-driven and framework-complete.

## Sample output

```
FUNCTION    CURRENT  TARGET  GAP   HEAT (current)
----------------------------------------------------------------------
GOVERN      1.83     3.67    1.84  ███████·············
RECOVER     1.5      3.5     2.0   ██████··············
...
OVERALL     2.18     3.77    1.59  █████████···········
```

## Skills demonstrated

- Working fluency with **NIST CSF 2.0** structure (Functions → Categories) including the new **Govern** function
- Maturity modelling (1-5 CMMI-style scale) and current-vs-target gap analysis
- Translating assessment findings into a **prioritized, phased remediation roadmap** tied to risk-reduction leverage
- Producing a professional, client-facing advisory deliverable
- Building data-driven tooling that scales a manual consulting artifact

## Resume bullet points

- *Conducted a NIST CSF 2.0 cybersecurity maturity assessment across all six Functions and 22 categories, scoring current-vs-target maturity and quantifying an aggregate 1.6-tier program gap.*
- *Built a Python toolkit that automates maturity scoring, gap analysis, and generation of a client-ready assessment report with a prioritized 12-month remediation roadmap.*
- *Translated framework gaps into phased, business-justified remediation initiatives rather than a blanket "level 5 everywhere" target, aligning uplift to risk appetite and sector benchmarks.*
