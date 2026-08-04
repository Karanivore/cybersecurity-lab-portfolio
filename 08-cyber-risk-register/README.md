# Lab 08 — Cyber Risk Register & Quantitative Risk Assessment

*Consultant / GRC track.*

The two risk views a consultant is expected to produce: a **qualitative
5×5 risk register** for the risk committee (inherent vs. residual,
likelihood × impact, heat map) *and* a **quantitative FAIR-style Monte
Carlo** estimate of each risk's Annualized Loss Expectancy (ALE) in
dollars for the CFO/board — so cyber risk can be compared directly to
the cost of controls.

## Contents

| File | Purpose |
|---|---|
| `sample_data/risk_register.json` | 7 enterprise cyber risks with 5×5 likelihood/impact, existing controls + assessed effectiveness, NIST CSF mapping, and FAIR parameters (TEF & loss-magnitude ranges) |
| `scripts/risk_analysis.py` | Computes inherent/residual ratings, runs a Monte Carlo ALE simulation, renders a residual heat map, and generates the full report |
| `risk_assessment_report.md` | The generated deliverable: executive summary, residual-ranked register, heat map, per-risk treatment, methodology |

## Usage

```bash
python3 scripts/risk_analysis.py
python3 scripts/risk_analysis.py --iterations 50000 --report risk_assessment_report.md
```

## Sample output

```
ID    RESID  LEVEL     MEAN ALE      P90 ALE       TITLE
----------------------------------------------------------------------------------
R-02  16.0   High      $1,794,888    $3,398,194    Public S3 bucket exposes customer PII
R-01  10.0   Medium    $1,346,947    $2,531,744    Ransomware via phishing ...
...
Portfolio residual Annualized Loss Expectancy — mean $5,624,233 | aggregated P90 $10,673,075
```

The sample risks deliberately cross-reference the technical labs (the
public S3 bucket from Lab 06, the SQLi-able web app from Lab 03, the
ransomware scenario from Lab 04) — showing how a consultant rolls
technical findings up into board-level risk language.

## Skills demonstrated

- Formal risk register construction (inherent vs. residual, control-effectiveness modelling)
- **Cyber risk quantification (CRQ)** with a FAIR-style Monte Carlo model — TEF × Loss Magnitude, expressed as an ALE distribution (mean/P50/P90)
- Qualitative 5×5 heat-mapping and risk-treatment decisions (mitigate / transfer / accept)
- Mapping technical findings to enterprise risks and NIST CSF categories
- Communicating risk in financial terms for executive decision-making

## Resume bullet points

- *Built an enterprise cyber risk register with inherent and residual 5×5 risk ratings and control-effectiveness modelling, mapped to NIST CSF categories.*
- *Developed a FAIR-style Monte Carlo risk-quantification tool estimating each risk's Annualized Loss Expectancy (mean/P50/P90), producing a defensible ~$5.6M residual loss-exposure figure for executive decision-making.*
- *Translated technical assessment findings (cloud misconfiguration, web app injection, ransomware exposure) into board-level risk language with recommended mitigate/transfer/accept treatments.*
