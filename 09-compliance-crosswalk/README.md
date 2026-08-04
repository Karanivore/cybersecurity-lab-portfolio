# Lab 09 — Compliance Framework Crosswalk / Control Mapping Engine

*Consultant / GRC track.*

Answers the single most common client question in GRC consulting: *"We're
already doing X — how much of Y do we get for free?"* This engine maps a
shared set of control themes across five frameworks — **NIST CSF 2.0,
NIST SP 800-53, ISO/IEC 27001:2022, CIS Controls v8, and SOC 2 TSC** —
and reports per-framework coverage, gaps, and a reverse control lookup.

## Contents

| File | Purpose |
|---|---|
| `sample_data/control_crosswalk.json` | 16 control themes, each mapped to its control IDs in all five frameworks, plus an implementation status (implemented / partial / not implemented) |
| `scripts/crosswalk.py` | Coverage summary, per-framework gap list, and reverse lookup of any control ID across every framework; generates the full crosswalk report |
| `crosswalk_report.md` | The generated deliverable: coverage table, full crosswalk matrix, priority multi-framework gaps, usage guidance |

## Usage

```bash
python3 crosswalk.py                          # per-framework coverage summary
python3 crosswalk.py --lookup "A.8.8"         # find one control across all frameworks
python3 crosswalk.py --framework SOC2_TSC     # gap list for a specific framework
python3 crosswalk.py --report crosswalk_report.md
```

## Sample output

```
$ python3 crosswalk.py --lookup "A.8.8"
Theme: Vulnerability Management  (status: Partial)
  NIST_CSF      ID.RA-01, PR.PS-02
  NIST_800_53   RA-5, SI-2
  ISO_27001     A.8.8
  CIS_v8        7
  SOC2_TSC      CC7.1
```

> Theme-level mappings are illustrative and approximate — in a real
> engagement they'd be validated against the authoritative framework text
> before use in an audit. The engine and workflow are the deliverable.

## Skills demonstrated

- Cross-framework control mapping (the "implement once, comply many" strategy)
- Working knowledge of **NIST CSF 2.0, NIST 800-53, ISO 27001:2022 Annex A, CIS v8, and SOC 2 TSC** control structures
- Coverage/gap analysis driving remediation prioritization by multi-framework leverage
- Building a reusable GRC tooling asset that turns a spreadsheet exercise into a queryable engine

## Resume bullet points

- *Built a multi-framework control crosswalk engine mapping 16 control themes across NIST CSF 2.0, NIST 800-53, ISO 27001:2022, CIS v8, and SOC 2, computing per-framework coverage and gap analysis.*
- *Enabled "implement once, comply many" remediation prioritization by identifying the control gaps that simultaneously block multiple compliance frameworks.*
- *Delivered a reverse control-lookup capability letting stakeholders trace any single control requirement to its equivalents across all five frameworks.*
