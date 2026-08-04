# Data Classification & Handling Policy

**Document owner:** CISO | **Version:** 1.0 | **Effective:** 2026-08-01
**Review cycle:** Annual | **Classification:** Internal
**ISO 27001:2022 references:** A.5.12, A.5.13, A.5.14, A.8.10, A.8.11, A.8.12, A.8.24

## 1. Purpose

To ensure information is classified according to its sensitivity and
handled with controls commensurate with the risk of its disclosure,
alteration, or loss.

## 2. Classification Levels

| Level | Definition | Examples |
|---|---|---|
| **Public** | Approved for public release; no harm if disclosed | Marketing content, published reports |
| **Internal** | Default for business information; limited harm if disclosed | Internal memos, project plans |
| **Confidential** | Sensitive; significant harm if disclosed | Customer PII, financial data, contracts |
| **Restricted** | Highly sensitive; severe harm if disclosed | Payment/PHI data, secrets, credentials |

## 3. Handling Requirements by Level

| Control | Public | Internal | Confidential | Restricted |
|---|---|---|---|---|
| Encryption in transit | Optional | Required | Required | Required |
| Encryption at rest | Optional | Recommended | Required | Required |
| Access | Anyone | Employees | Need-to-know | Need-to-know + MFA |
| External sharing | Allowed | Approved only | Approved + encrypted | Prohibited except approved secure channel |
| Retention/disposal | Standard | Standard | Secure deletion | Secure deletion + verification |
| Logging of access | No | Recommended | Required | Required |

## 4. Policy Statements

1. **Ownership.** Every information asset has an owner responsible for its
   classification and periodic reclassification review.
2. **Labeling.** Confidential and Restricted information is labeled where
   technically feasible.
3. **Least privilege.** Access to Confidential/Restricted data follows the
   *Access Control Policy*.
4. **Data loss prevention.** Technical controls (DLP, egress monitoring)
   are applied to Confidential and Restricted data.
5. **Third parties.** Sharing Confidential/Restricted data with vendors
   requires a completed third-party risk assessment and contractual data
   protection terms.
6. **Disposal.** Media and data are securely disposed of at end of life,
   with verification for Restricted data.

## 5. Compliance

Mishandling of classified information is a violation handled under the
Information Security Policy and may carry legal and regulatory
consequences.
