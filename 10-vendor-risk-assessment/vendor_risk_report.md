# Third-Party Vendor Risk Assessment

**Prepared by:** GRC Advisory Practice  
**Scope:** 5 vendors assessed via SIG-lite security questionnaire

---

## 1. Executive Summary

Five third parties were assessed on inherent risk (data sensitivity, access level, business criticality) and control maturity (weighted security questionnaire). **2 vendor(s) rate High or Critical residual risk** and should not be onboarded or renewed without remediation. The highest-risk relationship is **DataStream Integration Hub** — Critical residual risk driven by critical inherent exposure combined with a 13.3% control maturity score.

## 2. Vendor Risk Summary

| Vendor | Service | Inherent | Control maturity | Residual | Recommendation |
|---|---|---|---|---|---|
| DataStream Integration Hub | API integration with admin access to production database | Critical | 13.3% | Critical | Do not onboard / reject pending major security uplift |
| QuickAnalytics Marketing Tool | Ingests customer contact lists for campaign analytics | High | 31.7% | High | Remediate before onboarding (require fixes to critical-weight gaps) |
| CloudPay Payroll SaaS | Processes employee payroll and PII | Critical | 96.7% | Medium | Approve with conditions (remediation plan + annual reassessment) |
| SecureDoc E-Signature | Handles contract execution; stores signed agreements | High | 93.3% | Low | Approve |
| OfficeSnacks Delivery | Office snack delivery; no system or data access | Low | 6.2% | Low | Approve |

## 3. Detailed Findings & Remediation Asks

### DataStream Integration Hub — Residual risk: Critical

- **Service / exposure:** API integration with admin access to production database
- **Inherent risk:** Critical | **Control maturity:** 13.3%
- **Recommendation:** Do not onboard / reject pending major security uplift
- **Controls to remediate (14):**
    - [Security Governance] Is there a formal, executive-sponsored information security program with a named owner? (answered: *partial*)
    - [Security Governance] Are security policies reviewed and approved at least annually? (answered: *no*)
    - [Certifications] Do you hold a current SOC 2 Type II or ISO/IEC 27001 certification? (answered: *no*)
    - [Access Control] Is MFA enforced for all remote and administrative access? (answered: *no*)
    - [Access Control] Is access granted on a least-privilege basis and reviewed periodically? (answered: *no*)
    - [Data Protection] Is customer data encrypted at rest and in transit with modern algorithms? (answered: *partial*)
    - [Data Protection] Is data segregated logically or physically between tenants/customers? (answered: *no*)
    - [Vulnerability Management] Do you perform regular vulnerability scanning and remediate to a defined SLA? (answered: *no*)
    - [Vulnerability Management] Is an independent penetration test conducted at least annually? (answered: *no*)
    - [Incident Response] Do you have a documented incident response plan with defined breach-notification timelines? (answered: *partial*)
    - [Incident Response] Will you notify customers of a security incident affecting their data within a contractual timeframe? (answered: *no*)
    - [Resilience] Are backups performed, tested, and are RTO/RPO objectives defined? (answered: *no*)
    - [Fourth-Party Risk] Do you assess and monitor the security of your own subprocessors/vendors? (answered: *no*)
    - [Awareness] Is security awareness training mandatory for all staff at least annually? (answered: *no*)

### QuickAnalytics Marketing Tool — Residual risk: High

- **Service / exposure:** Ingests customer contact lists for campaign analytics
- **Inherent risk:** High | **Control maturity:** 31.7%
- **Recommendation:** Remediate before onboarding (require fixes to critical-weight gaps)
- **Controls to remediate (14):**
    - [Security Governance] Is there a formal, executive-sponsored information security program with a named owner? (answered: *partial*)
    - [Security Governance] Are security policies reviewed and approved at least annually? (answered: *partial*)
    - [Certifications] Do you hold a current SOC 2 Type II or ISO/IEC 27001 certification? (answered: *no*)
    - [Access Control] Is MFA enforced for all remote and administrative access? (answered: *partial*)
    - [Access Control] Is access granted on a least-privilege basis and reviewed periodically? (answered: *no*)
    - [Data Protection] Is customer data encrypted at rest and in transit with modern algorithms? (answered: *partial*)
    - [Data Protection] Is data segregated logically or physically between tenants/customers? (answered: *partial*)
    - [Vulnerability Management] Do you perform regular vulnerability scanning and remediate to a defined SLA? (answered: *partial*)
    - [Vulnerability Management] Is an independent penetration test conducted at least annually? (answered: *no*)
    - [Incident Response] Do you have a documented incident response plan with defined breach-notification timelines? (answered: *partial*)
    - [Incident Response] Will you notify customers of a security incident affecting their data within a contractual timeframe? (answered: *no*)
    - [Resilience] Are backups performed, tested, and are RTO/RPO objectives defined? (answered: *partial*)
    - [Fourth-Party Risk] Do you assess and monitor the security of your own subprocessors/vendors? (answered: *no*)
    - [Awareness] Is security awareness training mandatory for all staff at least annually? (answered: *partial*)

### CloudPay Payroll SaaS — Residual risk: Medium

- **Service / exposure:** Processes employee payroll and PII
- **Inherent risk:** Critical | **Control maturity:** 96.7%
- **Recommendation:** Approve with conditions (remediation plan + annual reassessment)
- **Controls to remediate (1):**
    - [Fourth-Party Risk] Do you assess and monitor the security of your own subprocessors/vendors? (answered: *partial*)

### SecureDoc E-Signature — Residual risk: Low

- **Service / exposure:** Handles contract execution; stores signed agreements
- **Inherent risk:** High | **Control maturity:** 93.3%
- **Recommendation:** Approve
- **Controls to remediate (2):**
    - [Access Control] Is access granted on a least-privilege basis and reviewed periodically? (answered: *partial*)
    - [Vulnerability Management] Is an independent penetration test conducted at least annually? (answered: *partial*)

### OfficeSnacks Delivery — Residual risk: Low

- **Service / exposure:** Office snack delivery; no system or data access
- **Inherent risk:** Low | **Control maturity:** 6.2%
- **Recommendation:** Approve
- **Controls to remediate (8):**
    - [Security Governance] Is there a formal, executive-sponsored information security program with a named owner? (answered: *no*)
    - [Security Governance] Are security policies reviewed and approved at least annually? (answered: *no*)
    - [Certifications] Do you hold a current SOC 2 Type II or ISO/IEC 27001 certification? (answered: *no*)
    - [Vulnerability Management] Do you perform regular vulnerability scanning and remediate to a defined SLA? (answered: *no*)
    - [Vulnerability Management] Is an independent penetration test conducted at least annually? (answered: *no*)
    - [Incident Response] Do you have a documented incident response plan with defined breach-notification timelines? (answered: *no*)
    - [Resilience] Are backups performed, tested, and are RTO/RPO objectives defined? (answered: *partial*)
    - [Awareness] Is security awareness training mandatory for all staff at least annually? (answered: *no*)

## 4. Methodology

Inherent risk combines the most sensitive data type handled, the vendor's access level, and business criticality into a Low/Medium/High/Critical tier. Control maturity is the weighted percentage of security-questionnaire items satisfied (partial = half credit; N/A items excluded). Residual risk elevates inherent risk when control maturity is weak. Recommendations follow a standard approve / approve-with-conditions / remediate / reject decision model.

_Generated by `scripts/vendor_risk.py` from the questionnaire and vendor responses._
