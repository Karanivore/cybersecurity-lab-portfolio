# Cyber Risk Assessment & Risk Register

**Client:** Contoso Financial Services (illustrative)  
**Prepared by:** GRC Advisory Practice  
**Date:** 2026-07-30

---

## 1. Executive Summary

This assessment documents 7 enterprise cyber risks in a formal register, rating each on a 5x5 likelihood-impact scale (inherent and residual) and quantifying loss exposure via a 20,000-iteration Monte Carlo (FAIR-style) simulation. **1 risks rate High or Critical on a residual basis.** The estimated **portfolio residual Annualized Loss Expectancy is approximately $5,624,233**, concentrated in ransomware (R-01) and customer-data exposure (R-02). These figures let leadership compare risk exposure directly against the cost of the controls proposed in the remediation roadmap.

## 2. Risk Register (residual-ranked)

| ID | Risk | Asset | Inherent | Residual | Residual level | Mean ALE | P90 ALE |
|---|---|---|---|---|---|---|---|
| R-02 | Public S3 bucket exposes customer PII | Customer invoice data (S3) | 20 | 16.0 | High | $1,794,888 | $3,398,194 |
| R-03 | Credential compromise of over-privileged service account | AWS control plane | 15 | 10.5 | Medium | $856,746 | $1,655,375 |
| R-01 | Ransomware via phishing leads to business interruption | Endpoints, file servers | 20 | 10.0 | Medium | $1,346,947 | $2,531,744 |
| R-04 | Third-party breach cascades to Contoso data | Data shared with vendors | 12 | 8.4 | Medium | $342,228 | $641,036 |
| R-05 | Unpatched internet-facing web app exploited (SQLi) | Customer web application | 16 | 7.2 | Medium | $901,820 | $1,702,620 |
| R-07 | Insider data exfiltration by departing employee | Intellectual property, customer lists | 8 | 5.2 | Low | $147,825 | $282,578 |
| R-06 | Regulatory penalty from delayed breach notification | Compliance posture | 8 | 4.8 | Low | $233,778 | $461,527 |

## 3. Qualitative Heat Map (residual)

```
Likelihood
  5 |         |         |         |         |         |
  4 |         |         |         |         |         |
  3 |         |         |         |         |  R-02   |
  2 |         |         |         |R-04,R-05|R-03,R-01|
  1 |         |         |         |R-07,R-06|         |
    +---------+---------+---------+---------+---------+
         1         2         3         4         5       Impact
```

## 4. Risk Detail & Treatment

### R-02 — Public S3 bucket exposes customer PII

- **Threat / vulnerability:** Opportunistic external actor / researcher exploiting Bucket public-access misconfiguration (see Lab 6)
- **NIST CSF categories:** PR.DS, PR.AA
- **Inherent risk:** 20 (Critical) → **Residual:** 16.0 (High)
- **Existing controls:** CSPM alerts (assessed effectiveness 20%)
- **Quantified exposure:** mean ALE $1,794,888, P50 $1,536,093, P90 $3,398,194
- **Recommended treatment:** Mitigate — prioritize control uplift this quarter; track to closure on the risk committee agenda.

### R-03 — Credential compromise of over-privileged service account

- **Threat / vulnerability:** External attacker / insider exploiting Wildcard admin policy on service account (see Lab 6)
- **NIST CSF categories:** PR.AA, GV.RR
- **Inherent risk:** 15 (High) → **Residual:** 10.5 (Medium)
- **Existing controls:** CloudTrail logging (assessed effectiveness 30%)
- **Quantified exposure:** mean ALE $856,746, P50 $720,431, P90 $1,655,375
- **Recommended treatment:** Mitigate or transfer — schedule control improvement and evaluate cyber-insurance coverage.

### R-01 — Ransomware via phishing leads to business interruption

- **Threat / vulnerability:** Ransomware operator exploiting Macro execution allowed; standing privileged access
- **NIST CSF categories:** PR.AT, PR.PS, RC.RP
- **Inherent risk:** 20 (Critical) → **Residual:** 10.0 (Medium)
- **Existing controls:** EDR, Immutable backups, Email filtering (assessed effectiveness 50%)
- **Quantified exposure:** mean ALE $1,346,947, P50 $1,154,566, P90 $2,531,744
- **Recommended treatment:** Mitigate or transfer — schedule control improvement and evaluate cyber-insurance coverage.

### R-04 — Third-party breach cascades to Contoso data

- **Threat / vulnerability:** Compromised supplier exploiting No vendor risk program (see Lab 10)
- **NIST CSF categories:** GV.SC
- **Inherent risk:** 12 (High) → **Residual:** 8.4 (Medium)
- **Existing controls:** Contractual DPA clauses (assessed effectiveness 30%)
- **Quantified exposure:** mean ALE $342,228, P50 $292,820, P90 $641,036
- **Recommended treatment:** Mitigate or transfer — schedule control improvement and evaluate cyber-insurance coverage.

### R-05 — Unpatched internet-facing web app exploited (SQLi)

- **Threat / vulnerability:** Automated exploitation / scanner exploiting Unparameterized queries (see Lab 3)
- **NIST CSF categories:** PR.PS, DE.CM
- **Inherent risk:** 16 (High) → **Residual:** 7.2 (Medium)
- **Existing controls:** WAF, SIEM detection (Lab 2) (assessed effectiveness 55%)
- **Quantified exposure:** mean ALE $901,820, P50 $763,564, P90 $1,702,620
- **Recommended treatment:** Mitigate or transfer — schedule control improvement and evaluate cyber-insurance coverage.

### R-07 — Insider data exfiltration by departing employee

- **Threat / vulnerability:** Malicious insider exploiting No DLP; broad data access
- **NIST CSF categories:** PR.DS, DE.AE
- **Inherent risk:** 8 (Medium) → **Residual:** 5.2 (Low)
- **Existing controls:** Offboarding checklist (assessed effectiveness 35%)
- **Quantified exposure:** mean ALE $147,825, P50 $124,757, P90 $282,578
- **Recommended treatment:** Accept with monitoring — document acceptance and review at next assessment cycle.

### R-06 — Regulatory penalty from delayed breach notification

- **Threat / vulnerability:** Regulator exploiting Unclear regulatory notification path (see Lab 7 RS.CO gap)
- **NIST CSF categories:** RS.CO, GV.OV
- **Inherent risk:** 8 (Medium) → **Residual:** 4.8 (Low)
- **Existing controls:** Legal on retainer (assessed effectiveness 40%)
- **Quantified exposure:** mean ALE $233,778, P50 $192,499, P90 $461,527
- **Recommended treatment:** Accept with monitoring — document acceptance and review at next assessment cycle.

## 5. Methodology

Inherent risk = likelihood x impact on a 5x5 scale. Residual risk applies assessed control effectiveness as a reduction to event likelihood. Quantitative exposure follows a FAIR-style model: Threat Event Frequency (events/year) and Loss Magnitude ($/event) are each sampled from triangular distributions (min/most-likely/max) over 20,000 iterations; residual ALE applies the same control-effectiveness reduction to frequency. Aggregate portfolio figures are the sum of per-risk means (mean) — an approximation, as risks are treated as independent.

_Generated by `scripts/risk_analysis.py` from `sample_data/risk_register.json`._
