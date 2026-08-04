# IT General Controls (ITGC) Testing Summary

**Client:** Contoso Financial Services (illustrative)  
**Function:** Technology Risk / IT Audit  
**Scope:** IT General Controls supporting SOX 404 / SOC 1 reliance  
**Period:** FY2026 (2026-01-01 to 2026-12-31)  
**In-scope systems:** Oracle ERP, Active Directory, AWS Production, Payroll SaaS

---

## 1. Executive Summary

IT General Controls were tested across the four standard domains supporting the IT General Controls supporting SOX 404 / SOC 1 reliance. Of 13 controls tested, **8 operated effectively** and **5 were deficient** (2 rising to a significant deficiency). Overall, reliance on ITGC to support automated application controls and the financial-statement / SOC 1 audit is **NOT supported without remediation / additional procedures**. The significant deficiency in change-management segregation of duties (ITGC-CM-02) is the primary driver and requires remediation plus expanded substantive testing.

## 2. Results by ITGC Domain

| Domain | Controls | Effective | Deficient |
|---|---|---|---|
| Access to Programs and Data | 5 | 3 | 2 |
| Program Changes | 3 | 2 | 1 |
| Program Development | 2 | 2 | 0 |
| Computer Operations | 3 | 1 | 2 |

## 3. Control Testing Detail

| Control | Domain | Key | Freq | Sample (tested/req'd) | Exceptions | Conclusion | Severity |
|---|---|---|---|---|---|---|---|
| ITGC-AC-01 | Access to Programs and Data | Yes | Recurring | 25/25 | 0 | Effective | — |
| ITGC-AC-02 | Access to Programs and Data | Yes | Recurring | 25/25 | 3 | Deficient | Significant Deficiency |
| ITGC-AC-03 | Access to Programs and Data | Yes | Quarterly | 2/2 | 1 | Deficient | Deficiency |
| ITGC-AC-04 | Access to Programs and Data | Yes | Quarterly | 2/2 | 0 | Effective | — |
| ITGC-AC-05 | Access to Programs and Data | No | Annual | 1/1 | 0 | Effective | — |
| ITGC-CM-01 | Program Changes | Yes | Recurring | 25/25 | 0 | Effective | — |
| ITGC-CM-02 | Program Changes | Yes | Recurring | 25/25 | 5 | Deficient | Significant Deficiency (assess for Material Weakness) |
| ITGC-CM-03 | Program Changes | No | Monthly | 2/2 | 0 | Effective | — |
| ITGC-PD-01 | Program Development | Yes | Annual | 2/1 | 0 | Effective | — |
| ITGC-PD-02 | Program Development | No | Annual | 2/1 | 0 | Effective | — |
| ITGC-OP-01 | Computer Operations | Yes | Daily | 15/15 | 0 | Effective | — |
| ITGC-OP-02 | Computer Operations | Yes | Monthly | 2/2 | 1 | Deficient | Deficiency |
| ITGC-OP-03 | Computer Operations | No | Recurring | 25/25 | 2 | Deficient | Deficiency |

## 4. Exceptions & Deficiencies

### ITGC-AC-02 — User access is removed within 1 business day of termination.

- **Domain:** Access to Programs and Data | **Key control:** Yes
- **Testing:** 3 exception(s) in a sample of 25 (minimum required 25 for a recurring control)
- **Compensating control:** None identified
- **Preliminary severity:** Significant Deficiency
- **Recommendation:** Automate deprovisioning from the HR leaver feed and reconcile weekly; investigate the terminated users whose access persisted for residual risk.

### ITGC-AC-03 — Privileged (admin) access is restricted and reviewed quarterly.

- **Domain:** Access to Programs and Data | **Key control:** Yes
- **Testing:** 1 exception(s) in a sample of 2 (minimum required 2 for a quarterly control)
- **Compensating control:** Yes
- **Preliminary severity:** Deficiency
- **Recommendation:** Complete the overdue privileged-access review and implement just-in-time elevation; the compensating logging control limits but does not eliminate the exposure.

### ITGC-CM-02 — Segregation of duties: developers cannot migrate their own changes to production.

- **Domain:** Program Changes | **Key control:** Yes
- **Testing:** 5 exception(s) in a sample of 25 (minimum required 25 for a recurring control)
- **Compensating control:** None identified
- **Preliminary severity:** Significant Deficiency (assess for Material Weakness)
- **Recommendation:** Enforce technical segregation so developers cannot deploy to production; route migrations through an independent release function and retain approval evidence.

### ITGC-OP-02 — Production data is backed up and restoration is periodically tested.

- **Domain:** Computer Operations | **Key control:** Yes
- **Testing:** 1 exception(s) in a sample of 2 (minimum required 2 for a monthly control)
- **Compensating control:** Yes
- **Preliminary severity:** Deficiency
- **Recommendation:** Perform and document the missed restoration test; add a calendar control with evidence retention.

### ITGC-OP-03 — IT incidents are logged, prioritized, and resolved per SLA.

- **Domain:** Computer Operations | **Key control:** No
- **Testing:** 2 exception(s) in a sample of 25 (minimum required 25 for a recurring control)
- **Compensating control:** Yes
- **Preliminary severity:** Deficiency
- **Recommendation:** Remediate the control gap and retain evidence; re-test in the next period.

## 5. Impact on Audit Reliance

Where a key ITGC is deficient, the automated application controls and system-generated reports that depend on it can no longer be relied upon without additional procedures. In this engagement:

- **ITGC-AC-02** deficiency → expand substantive testing over affected processes and system-generated reports; assess management's remediation.
- **ITGC-AC-03** deficiency → expand substantive testing over affected processes and system-generated reports; assess management's remediation.
- **ITGC-CM-02** deficiency → expand substantive testing over affected processes and system-generated reports; assess management's remediation.
- **ITGC-OP-02** deficiency → expand substantive testing over affected processes and system-generated reports; assess management's remediation.

## 6. Methodology

Each control was assessed for design (test of design) and operating effectiveness (test of operating effectiveness). Sample sizes were evaluated against attribute-sampling minimums for a low expected deviation rate (annual 1, quarterly 2, monthly 2, weekly 5, daily 15, recurring/manual 25), capped at population size. A control with any exception (or a failed design) is concluded Deficient; severity is elevated for key controls lacking a compensating control, with a high exception rate flagged for material-weakness assessment. This is the same evidence chain used for SOX 404 and SOC 1 (Type II) reporting.

_Generated by `scripts/itgc_test.py` from `sample_data/itgc_controls.json`._
