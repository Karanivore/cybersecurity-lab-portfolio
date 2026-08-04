# Lab 6 — Cloud (AWS) Security Audit Tool

An offline AWS security posture auditor: loads exported IAM and S3
configuration JSON and evaluates it against CIS AWS Foundations
Benchmark-aligned checks, the same approach open-source tools like
Prowler and ScoutSuite use. Runs with zero AWS credentials or live
account access, so it's fully reproducible and safe to demo.

## Contents

| File | Purpose |
|---|---|
| `scripts/cloud_audit.py` | Audits IAM users/keys/policies and S3 buckets against CIS-aligned checks; outputs severity-ranked findings (console + JSON) |
| `sample_data/iam_users.json` | 5 mock IAM users including root, a stale contractor account, and a service account — with MFA status and access key ages |
| `sample_data/iam_policies.json` | 4 mock IAM policies, including one full-administrator policy attached directly to a user |
| `sample_data/s3_buckets.json` | 5 mock S3 buckets, including one publicly accessible bucket with no encryption |
| `sample_cis_audit_report.md` | Full audit report: executive summary, deep-dives on the critical findings, prioritized remediation plan |

## Checks implemented (CIS AWS Foundations Benchmark-aligned)

| Control | Check |
|---|---|
| 1.4 / 1.5 | Root account has no access keys / has MFA enabled |
| 1.10 | Users with console access have MFA enabled |
| 1.12 | Access keys unused 45+ days are flagged for disabling |
| 1.14 | Access keys are rotated within 90 days |
| 1.15 / 1.16 | Policies attached to groups/roles, not directly to users; no wildcard (`Action:*, Resource:*`) admin policies |
| 2.1.1 / 2.1.2 | S3 Block Public Access enabled; no bucket policy allows public access |
| 2.1.3 | S3 bucket versioning enabled |
| 2.1.5 | S3 default encryption enabled |
| 2.6 | S3 access logging enabled |

## Usage

```bash
python3 scripts/cloud_audit.py
python3 scripts/cloud_audit.py --json findings.json
```

To run against a real AWS account, swap the JSON loaders in
`cloud_audit.py` for `boto3` calls (`iam.list_users`,
`iam.list_access_keys`, `iam.list_policies`, `s3.get_bucket_*`) using
read-only, least-privilege credentials — the check logic itself is
unchanged.

## Sample output

```
[*] Audited 5 IAM users, 4 IAM policies, 5 S3 buckets
[*] 19 finding(s)

[CRITICAL] CIS 1.4    resource=root
             Root account 'root' has an active access key — root should never have programmatic access keys.
[CRITICAL] CIS 2.1.2  resource=customer-invoice-exports
             S3 bucket 'customer-invoice-exports' has a bucket policy that allows public access.
...
Summary: CRITICAL=5, HIGH=5, MEDIUM=7, LOW=2
```

## Skills demonstrated

- Cloud security posture management (CSPM) methodology, CIS AWS Foundations Benchmark
- IAM least-privilege analysis (policy document parsing, wildcard-permission detection)
- S3 data-exposure risk assessment (public access, encryption, versioning, logging)
- Building an auditing tool designed to swap cleanly from mock data to live `boto3` calls
- Executive + technical report writing with prioritized, business-risk-ordered remediation

## Resume bullet points

- *Built a CIS AWS Foundations Benchmark-aligned cloud security audit tool in Python, evaluating IAM credential hygiene, least-privilege policy attachment, and S3 data-exposure risk from exported account configuration.*
- *Identified and reported a critical public S3 data exposure and a full-administrator IAM policy attached directly to a service account in a simulated cloud security audit, with a business-risk-prioritized remediation plan.*
- *Designed the audit tool's data layer to swap between offline JSON exports and live `boto3` API calls without changing check logic, supporting both point-in-time audits and continuous CSPM.*
