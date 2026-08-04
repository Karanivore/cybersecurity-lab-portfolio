# Lab 10 — Third-Party / Vendor Risk Assessment Engine

*Consultant / GRC track.*

Third-party risk management (TPRM) is one of the fastest-growing lines of
security consulting work. This engine scores vendors on the standard
two-axis model — **inherent risk** (how much harm the vendor *could*
cause) versus **control maturity** (how well they answered the security
questionnaire) — and produces a residual risk tier, an onboarding
recommendation, and the specific weak controls to push back on.

## Contents

| File | Purpose |
|---|---|
| `sample_data/questionnaire.json` | A 14-question, weighted SIG-lite security questionnaire across 8 domains (governance, certs, access, data protection, vuln mgmt, IR, resilience, fourth-party) |
| `sample_data/vendor_responses.json` | 5 vendors with distinct risk profiles (a locked-down payroll SaaS, a weak marketing tool, an over-privileged integration vendor, a no-access snack supplier, etc.) |
| `scripts/vendor_risk.py` | Computes inherent tier, weighted control maturity, residual tier, recommendation, and per-vendor remediation asks; generates the report |
| `vendor_risk_report.md` | The generated deliverable: executive summary, vendor risk summary table, detailed findings & remediation asks, methodology |

## Usage

```bash
python3 scripts/vendor_risk.py
python3 scripts/vendor_risk.py --report vendor_risk_report.md
```

## Sample output

```
VENDOR                          INHERENT  CTRL%   RESIDUAL  RECOMMENDATION
----------------------------------------------------------------------------------
DataStream Integration Hub      Critical  13.3    Critical  Do not onboard / reject ...
QuickAnalytics Marketing Tool   High      31.7    High      Remediate before onboarding ...
CloudPay Payroll SaaS           Critical  96.7    Medium    Approve with conditions ...
SecureDoc E-Signature           High      93.3    Low       Approve
OfficeSnacks Delivery           Low       6.2     Low       Approve
```

Note the model correctly caps residual risk at inherent risk: the
no-data-access snack vendor stays Low despite a weak questionnaire score,
while the over-privileged integration vendor with poor controls is the
top risk — the same judgment a TPRM analyst applies manually.

## Skills demonstrated

- Third-party risk management (TPRM) methodology and vendor tiering
- Inherent-vs-residual risk modelling with control-maturity scoring
- Designing a weighted security questionnaire (SIG-lite style)
- Risk-based vendor onboarding decisions (approve / conditions / remediate / reject)
- Producing actionable, per-vendor remediation asks for procurement and security review

## Resume bullet points

- *Built a third-party risk assessment engine scoring vendors on inherent risk and weighted security-questionnaire control maturity, producing residual risk tiers and onboarding recommendations.*
- *Designed a SIG-lite vendor security questionnaire across 8 domains and automated the scoring, tiering, and remediation-ask generation for a portfolio of vendors.*
- *Implemented a defensible residual-risk model that caps exposure at inherent risk, correctly prioritizing an over-privileged integration vendor over low-impact suppliers.*
