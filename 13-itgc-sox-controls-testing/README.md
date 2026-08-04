# Lab 13 — IT General Controls (ITGC) / SOX Controls Testing

*Consultant / GRC track — Big Four technology-risk & assurance focus.*

The single most common deliverable in a Big Four (KPMG / Deloitte / EY /
PwC) **technology-risk and IT-audit** engagement: testing **IT General
Controls** across the four standard domains that a SOX 404 financial-
statement audit or a **SOC 1 / SOC 2** examination relies upon. This tool
tests each control, applies attribute-sampling sample-size guidance,
tracks exceptions, evaluates deficiency severity, and generates an
auditor workpaper-style summary.

## The four ITGC domains

1. **Access to Programs and Data** — provisioning, deprovisioning, access reviews, privileged access, segregation of duties
2. **Program Changes** — change authorization, testing, approval, dev/prod segregation
3. **Program Development** — SDLC, UAT sign-off, data conversion for new systems
4. **Computer Operations** — job scheduling, backup/recovery, incident management

## Contents

| File | Purpose |
|---|---|
| `sample_data/itgc_controls.json` | 13 ITGC controls across all four domains with testing results (population, sample, exceptions), key-control and compensating-control flags |
| `scripts/itgc_test.py` | Checks sample adequacy, concludes operating effectiveness, evaluates deficiency severity, rolls up an audit-reliance opinion, generates the workpaper |
| `itgc_testing_summary.md` | The generated deliverable: executive summary, results by domain, testing detail, deficiency write-ups, impact on audit reliance, methodology |

## Usage

```bash
python3 scripts/itgc_test.py
python3 scripts/itgc_test.py --report itgc_testing_summary.md
```

## Sample output

```
CONTROL      KEY  FREQ       SAMPLE   EXC  CONCLUSION    SEVERITY
------------------------------------------------------------------------------------
ITGC-AC-02   Y    recurring  25/25    3    Deficient     Significant Deficiency
ITGC-CM-02   Y    recurring  25/25    5    Deficient     Significant Deficiency (assess for Material Weakness)
ITGC-OP-02   Y    monthly    2/2      1    Deficient     Deficiency
...
Reliance on ITGC for automated-control / SOC 1 purposes: NOT supported without remediation / additional procedures
```

## Why this matters for a Big Four / KPMG role

KPMG is a licensed audit firm; its technology-risk practice runs heavily
on **ITGC testing for SOX** and **SOC 1/SOC 2 attestation**. This lab
demonstrates the *auditor* perspective — sampling methodology, the
design-vs-operating-effectiveness distinction, deficiency severity
evaluation (deficiency → significant deficiency → material weakness), and
how a deficient key control breaks reliance on the automated controls and
system-generated reports that depend on it.

## Skills demonstrated

- IT General Controls testing across all four SOX/SOC ITGC domains
- Attribute-sampling methodology (frequency-driven sample sizing for low expected deviation)
- Test of design vs. test of operating effectiveness
- SOX deficiency evaluation: deficiency / significant deficiency / material weakness
- Translating a control exception into its impact on financial-statement / SOC audit reliance

## Resume bullet points

- *Tested IT General Controls across access, change, development, and operations domains supporting SOX 404 / SOC 1 reliance, concluding on operating effectiveness for 13 controls using attribute-sampling methodology.*
- *Identified a change-management segregation-of-duties significant deficiency and evaluated its escalation toward material weakness, documenting the impact on reliance over automated controls and system-generated reports.*
- *Built a controls-testing tool that automates sample-adequacy checks, deficiency-severity evaluation, and generation of an IT-audit workpaper summary aligned to SOX 404 and SOC 1/SOC 2 examinations.*
