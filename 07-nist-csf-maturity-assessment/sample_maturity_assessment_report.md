# NIST CSF 2.0 Cybersecurity Maturity Assessment

**Client:** Contoso Financial Services (illustrative)  
**Prepared by:** GRC Advisory Practice  
**Framework:** NIST Cybersecurity Framework 2.0  
**Assessment date:** 2026-07-30

---

## 1. Executive Summary

This assessment evaluated the organization's cybersecurity program across all six NIST CSF 2.0 Functions and 22 categories, scoring each on a 1-5 maturity scale. The organization's **overall current maturity is 2.18 / 5.0** against a **target of 3.77 / 5.0**, an aggregate gap of **1.59**. The weakest Functions are **RECOVER and GOVERN**, driven largely by governance and supply-chain gaps. 13 categories carry a maturity gap of 2 or more tiers and should anchor the remediation roadmap in Section 4.

## 2. Maturity Scale

- **Tier 1** — Initial - ad hoc, undocumented, reactive
- **Tier 2** — Developing - some documentation, inconsistent execution
- **Tier 3** — Defined - documented, repeatable, consistently applied
- **Tier 4** — Managed - measured, monitored, and continuously reviewed
- **Tier 5** — Optimized - quantitatively managed and continuously improved

## 3. Function-Level Results

| Function | Current | Target | Gap |
|---|---|---|---|
| GOVERN | 1.83 | 3.67 | 1.84 |
| IDENTIFY | 2 | 3.67 | 1.67 |
| PROTECT | 2.6 | 4 | 1.4 |
| DETECT | 2.5 | 4 | 1.5 |
| RESPOND | 2.5 | 3.75 | 1.25 |
| RECOVER | 1.5 | 3.5 | 2.0 |
| **OVERALL** | **2.18** | **3.77** | **1.59** |

### Category detail

| Function | Category | Current | Target | Gap | Observation |
|---|---|---|---|---|---|
| GOVERN | GV.OC Organizational Context | 2 | 4 | 2 | Mission dependencies understood informally; not documented or reviewed. |
| GOVERN | GV.RM Risk Management Strategy | 2 | 4 | 2 | No board-approved risk appetite statement; risk decisions ad hoc. |
| GOVERN | GV.RR Roles, Responsibilities, and Authorities | 3 | 4 | 1 | CISO role defined; RACI exists but not consistently followed. |
| GOVERN | GV.PO Policy | 2 | 4 | 2 | Policies exist but are 3+ years stale and not centrally governed. |
| GOVERN | GV.OV Oversight | 1 | 3 | 2 | No formal program metrics reported to leadership. |
| GOVERN | GV.SC Cybersecurity Supply Chain Risk Management | 1 | 3 | 2 | No vendor risk program; onboarding lacks security review (see Lab 10). |
| IDENTIFY | ID.AM Asset Management | 2 | 4 | 2 | Partial CMDB; cloud and SaaS assets not fully inventoried. |
| IDENTIFY | ID.RA Risk Assessment | 2 | 4 | 2 | Annual assessment done but not maintained as a living risk register (see Lab 08). |
| IDENTIFY | ID.IM Improvement | 2 | 3 | 1 | Lessons-learned captured after incidents but not tracked to closure. |
| PROTECT | PR.AA Identity Management, Authentication & Access Control | 3 | 4 | 1 | MFA on most systems; privileged access not yet least-privilege (see Lab 6 findings). |
| PROTECT | PR.AT Awareness and Training | 3 | 4 | 1 | Annual training; phishing simulation program in place but not role-based. |
| PROTECT | PR.DS Data Security | 2 | 4 | 2 | Encryption in transit; at-rest encryption and DLP inconsistent. |
| PROTECT | PR.PS Platform Security | 3 | 4 | 1 | Baseline hardening exists; patch SLA not consistently met. |
| PROTECT | PR.IR Technology Infrastructure Resilience | 2 | 4 | 2 | Network segmentation partial (see Lab 5); no zero-trust roadmap. |
| DETECT | DE.CM Continuous Monitoring | 3 | 4 | 1 | SIEM deployed (see Lab 2); coverage gaps in cloud and OT. |
| DETECT | DE.AE Adverse Event Analysis | 2 | 4 | 2 | Alert triage reactive; limited detection engineering / tuning. |
| RESPOND | RS.MA Incident Management | 3 | 4 | 1 | IR playbooks exist (see Lab 4); not exercised regularly. |
| RESPOND | RS.AN Incident Analysis | 2 | 4 | 2 | Timeline reconstruction manual; no standardized forensics workflow. |
| RESPOND | RS.CO Incident Response Reporting and Communication | 2 | 3 | 1 | Internal comms templates exist; regulatory notification path unclear. |
| RESPOND | RS.MI Incident Mitigation | 3 | 4 | 1 | Containment via EDR available; automated isolation not enabled. |
| RECOVER | RC.RP Incident Recovery Plan Execution | 2 | 4 | 2 | Backups exist and are immutable; restore testing infrequent. |
| RECOVER | RC.CO Incident Recovery Communication | 1 | 3 | 2 | No defined stakeholder/customer recovery communication plan. |

## 4. Prioritized Remediation Roadmap

Initiatives are ordered by maturity gap (largest first), which also approximates risk-reduction leverage. Suggested phasing assumes a 12-month improvement program.

| Priority | Category | Current → Target | Recommended action | Suggested phase |
|---|---|---|---|---|
| 1 | GV.OC Organizational Context | 2 → 4 | Document mission dependencies, critical services, and their supporting assets | 0-3 months |
| 2 | GV.RM Risk Management Strategy | 2 → 4 | Draft a board-approved risk appetite statement and risk governance process | 0-3 months |
| 3 | GV.PO Policy | 2 → 4 | Refresh and centrally govern the policy suite on an annual review cycle | 0-3 months |
| 4 | ID.AM Asset Management | 2 → 4 | Complete a unified asset inventory covering cloud and SaaS | 3-6 months |
| 5 | ID.RA Risk Assessment | 2 → 4 | Convert the annual assessment into a maintained, living risk register | 3-6 months |
| 6 | PR.DS Data Security | 2 → 4 | Enforce at-rest encryption and deploy DLP on sensitive data stores | 3-6 months |
| 7 | PR.IR Technology Infrastructure Resilience | 2 → 4 | Define a segmentation/zero-trust target architecture and phased plan | 6-12 months |
| 8 | DE.AE Adverse Event Analysis | 2 → 4 | Establish a detection-engineering function with tuning and coverage metrics | 6-12 months |
| 9 | RS.AN Incident Analysis | 2 → 4 | Standardize a forensics/timeline workflow and evidence-handling procedure | 6-12 months |
| 10 | RC.RP Incident Recovery Plan Execution | 2 → 4 | Institute scheduled, tested restore drills with documented RTO/RPO validation | 6-12 months |
| 11 | GV.OV Oversight | 1 → 3 | Define program KPIs/KRIs and a quarterly cyber report to the board | 6-12 months |
| 12 | GV.SC Cybersecurity Supply Chain Risk Management | 1 → 3 | Stand up a third-party risk management program and vendor security review gate | 6-12 months |
| 13 | RC.CO Incident Recovery Communication | 1 → 3 | Document a stakeholder and customer recovery communication plan | 6-12 months |

## 5. Methodology

Each NIST CSF 2.0 category was scored 1-5 based on interviews, document review, and control inspection. Function scores are the mean of their category scores; the overall score is the mean across all categories. Target maturity reflects the organization's risk appetite and peer benchmark for its sector, not a blanket 'level 5 everywhere' goal — target tiers are deliberately set where the control's business value justifies the investment.

_Generated by `scripts/csf_maturity.py` from `sample_data/assessment_responses.json`._
