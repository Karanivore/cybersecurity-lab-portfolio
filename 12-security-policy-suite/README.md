# Lab 12 — ISMS Information Security Policy Suite (ISO 27001-aligned)

*Consultant / GRC track.*

A security policy document set demonstrates the skill consulting clients
value most in an advisor: translating framework requirements into clear,
enforceable, business-appropriate governance. This lab is a compact
**Information Security Management System (ISMS)** policy suite aligned to
ISO/IEC 27001:2022, plus a tool that verifies every Annex A control theme
has an owning policy.

## Contents

| File | Purpose |
|---|---|
| `policies/information_security_policy.md` | Apex ISMS policy — management direction, scope, roles, framework alignment |
| `policies/access_control_policy.md` | Least privilege, MFA, RBAC, access reviews, non-human identities (A.5.15–A.8.5) |
| `policies/acceptable_use_policy.md` | Acceptable/prohibited use, email/phishing, BYOD (A.5.10, A.6.3, A.8.7) |
| `policies/incident_response_policy.md` | NIST 800-61-aligned IR requirements, breach notification, testing (A.5.24–A.6.8) |
| `policies/data_classification_policy.md` | 4-tier classification + a handling-requirements matrix (A.5.12–A.8.24) |
| `control_to_policy_mapping.json` | ISO 27001:2022 Annex A theme → owning policy mapping |
| `scripts/policy_coverage.py` | Verifies each policy file exists and reports Annex A themes with no owning policy |

## Usage

```bash
python3 scripts/policy_coverage.py
```

## Sample output

```
Annex A theme coverage: 20/23 (87.0%)
...
[!] 3 Annex A theme(s) have no owning policy — documentation gap:
    - A.5.7 Threat intelligence
    - A.5.19 Information security in supplier relationships
    - A.8.13 Information backup
```

The tool exits non-zero when documentation gaps exist — the same signal
you'd wire into CI for a real policy-as-code ISMS repository. The
deliberate gaps show the reviewer knows a 5-policy starter set does *not*
cover all of Annex A, and names exactly what's still needed.

## Skills demonstrated

- Security governance and policy authorship (the core of GRC advisory work)
- ISO/IEC 27001:2022 ISMS structure and Annex A control coverage
- Translating framework controls into enforceable, role-assigned policy language
- Policy-as-code thinking: machine-checkable control-to-policy coverage
- Professional technical writing bridging security and business audiences

## Resume bullet points

- *Authored an ISO/IEC 27001:2022-aligned ISMS policy suite (information security, access control, acceptable use, incident response, data classification) covering 20 Annex A control themes.*
- *Built a policy-coverage checker that maps ISO 27001 Annex A controls to owning policies and fails CI on documentation gaps, applying a policy-as-code approach to governance.*
- *Produced enforceable, role-assigned security policies translating framework requirements into business-appropriate governance language.*
