# SOC 2 / ISO 27001 Readiness Assessment

**Client:** Contoso Financial Services (illustrative)  
**Prepared by:** GRC Advisory Practice  
**Framework:** AICPA SOC 2 (Security / Common Criteria) with ISO 27001:2022 cross-reference  
**Assessment type:** Type II readiness (gap assessment prior to audit)  
**Date:** 2026-07-30

---

## 1. Executive Summary

The organization is **54.5% ready** for a SOC 2 Type II examination. Of 22 in-scope criteria, 6 are fully met, 12 are partially implemented, and 4 are not met. There are **16 control gaps** and **6 evidence gaps** (controls that appear to operate but lack the audit-ready evidence an examiner requires). We do not recommend entering the audit window until Phase 1 and Phase 2 items below are closed; proceeding now would risk qualified exceptions in the report.

## 2. Readiness by Category

| TSC Category | Readiness | Controls |
|---|---|---|
| Control Environment | 100.0% | 2 |
| Communication & Information | 50.0% | 2 |
| Risk Assessment | 50.0% | 2 |
| Monitoring Activities | 0.0% | 1 |
| Control Activities | 50.0% | 1 |
| Logical & Physical Access | 50.0% | 5 |
| System Operations | 75.0% | 4 |
| Change Management | 100.0% | 1 |
| Risk Mitigation | 25.0% | 2 |
| Availability | 50.0% | 1 |
| Confidentiality | 0.0% | 1 |
| **Overall** | **54.5%** | **22** |

## 3. Control Status Detail (with ISO 27001:2022 cross-reference)

| Criterion | Category | Status | Evidence | ISO 27001 ref | Owner |
|---|---|---|---|---|---|
| CC1.1 | Control Environment | Met | ✅ | A.5.1, Clause 5 | CISO |
| CC1.4 | Control Environment | Met | ✅ | A.6.3 | HR/Security |
| CC2.2 | Communication & Information | Partial | ❌ missing | A.5.1 | CISO |
| CC2.3 | Communication & Information | Partial | ❌ missing | A.5.5 | Legal |
| CC3.1 | Risk Assessment | Partial | ❌ missing | Clause 6.1 | CISO |
| CC3.2 | Risk Assessment | Partial | ✅ | Clause 6.1, A.5.7 | Risk |
| CC4.1 | Monitoring Activities | Not Met | ❌ missing | Clause 9.1 | Internal Audit |
| CC5.2 | Control Activities | Partial | ✅ | A.8.9 | IT Ops |
| CC6.1 | Logical & Physical Access | Partial | ✅ | A.5.15, A.8.5 | IT Ops |
| CC6.2 | Logical & Physical Access | Met | ✅ | A.5.16, A.5.18 | IT Ops |
| CC6.3 | Logical & Physical Access | Not Met | ❌ missing | A.5.18 | IT Ops |
| CC6.6 | Logical & Physical Access | Partial | ✅ | A.8.20, A.8.22 | Network |
| CC6.7 | Logical & Physical Access | Partial | ❌ missing | A.8.24 | IT Ops |
| CC7.1 | System Operations | Partial | ✅ | A.8.8 | Security |
| CC7.2 | System Operations | Met | ✅ | A.8.15, A.8.16 | SOC |
| CC7.3 | System Operations | Met | ✅ | A.5.24-A.5.26 | SOC |
| CC7.4 | System Operations | Partial | ❌ missing | A.5.24-A.5.28 | SOC |
| CC8.1 | Change Management | Met | ✅ | A.8.32 | Eng |
| CC9.1 | Risk Mitigation | Partial | ❌ missing | Clause 6.1 | Risk |
| CC9.2 | Risk Mitigation | Not Met | ❌ missing | A.5.19-A.5.22 | Procurement |
| A1.2 | Availability | Partial | ✅ | A.8.13, A.8.14 | IT Ops |
| C1.1 | Confidentiality | Not Met | ❌ missing | A.5.12, A.5.13 | Data Owner |

## 4. Evidence Gaps (highest audit risk)

These controls may operate effectively but have **no audit-ready evidence** — an examiner will treat them as exceptions regardless of whether the control works:

- **CC2.2 Internal communication of security responsibilities** — owner: CISO. Produce and retain evidence (policy, ticket, log, or screenshot with date).
- **CC2.3 External communication (customers, regulators)** — owner: Legal. Produce and retain evidence (policy, ticket, log, or screenshot with date).
- **CC3.1 Objectives specified to enable risk identification** — owner: CISO. Produce and retain evidence (policy, ticket, log, or screenshot with date).
- **CC6.7 Encryption of data at rest and in transit** — owner: IT Ops. Produce and retain evidence (policy, ticket, log, or screenshot with date).
- **CC7.4 Incident response program execution and testing** — owner: SOC. Produce and retain evidence (policy, ticket, log, or screenshot with date).
- **CC9.1 Risk mitigation activities (incl. insurance)** — owner: Risk. Produce and retain evidence (policy, ticket, log, or screenshot with date).

## 5. Prioritized Remediation Roadmap

Sequenced by control status (not-met first) then effort (quick wins early). Assumes a 180-day runway to audit.

| # | Criterion | Description | Status | Effort | Owner | Phase |
|---|---|---|---|---|---|---|
| 1 | CC6.3 | Role-based access and periodic access reviews | Not Met | Medium | IT Ops | Phase 1 (0-30 days) |
| 2 | C1.1 | Confidential information identified and protected | Not Met | Medium | Data Owner | Phase 1 (0-30 days) |
| 3 | CC4.1 | Ongoing evaluations of control effectiveness | Not Met | High | Internal Audit | Phase 1 (0-30 days) |
| 4 | CC9.2 | Vendor and business partner risk management | Not Met | High | Procurement | Phase 1 (0-30 days) |
| 5 | CC2.2 | Internal communication of security responsibilities | Partial | Low | CISO | Phase 2 (30-90 days) |
| 6 | CC2.3 | External communication (customers, regulators) | Partial | Medium | Legal | Phase 2 (30-90 days) |
| 7 | CC3.1 | Objectives specified to enable risk identification | Partial | Medium | CISO | Phase 2 (30-90 days) |
| 8 | CC3.2 | Risks identified and analyzed (risk register) | Partial | Medium | Risk | Phase 2 (30-90 days) |
| 9 | CC5.2 | Technology general controls over infrastructure | Partial | Medium | IT Ops | Phase 2 (30-90 days) |
| 10 | CC6.1 | Logical access security (least privilege, MFA) | Partial | Medium | IT Ops | Phase 3 (90-180 days) |
| 11 | CC6.7 | Encryption of data at rest and in transit | Partial | Medium | IT Ops | Phase 3 (90-180 days) |
| 12 | CC7.1 | Vulnerability detection and configuration monitoring | Partial | Medium | Security | Phase 3 (90-180 days) |
| 13 | CC7.4 | Incident response program execution and testing | Partial | Medium | SOC | Phase 3 (90-180 days) |
| 14 | CC9.1 | Risk mitigation activities (incl. insurance) | Partial | Medium | Risk | Phase 3 (90-180 days) |
| 15 | A1.2 | Backup, recovery, and environmental protections | Partial | Medium | IT Ops | Phase 3 (90-180 days) |
| 16 | CC6.6 | Boundary protection / network segmentation | Partial | High | Network | Phase 3 (90-180 days) |

## 6. Methodology

Each Trust Services Criterion in scope was rated Met / Partial / Not met and flagged for evidence availability. Readiness score = mean of status scores (Met=1.0, Partial=0.5, Not met=0.0; N/A excluded). The roadmap sequences open items by status severity then implementation effort, so quick wins land early and the highest-risk gaps are not deferred. ISO 27001:2022 Annex A references are provided so a single remediation effort can support both certifications.

_Generated by `scripts/readiness.py` from `sample_data/soc2_readiness.json`._
