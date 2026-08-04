#!/usr/bin/env python3
"""
AWS Cloud Security Audit Tool (offline mode).

Audits exported IAM and S3 configuration JSON against CIS AWS
Foundations Benchmark-aligned checks — the same approach tools like
Prowler/ScoutSuite use, run here against static exports so the lab needs
no live AWS credentials. Swap the JSON loaders for `boto3` calls
(iam.list_users, iam.list_policies, s3.get_bucket_*) to run it live
against a real account with read-only IAM/S3 permissions.

Usage:
    python3 cloud_audit.py
    python3 cloud_audit.py --json findings.json
"""

import argparse
import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"

KEY_ROTATION_DAYS = 90
CREDENTIAL_UNUSED_DAYS = 45
ADMIN_ACTION_PATTERNS = {"*", "iam:*"}


def load(name: str):
    return json.loads((DATA_DIR / name).read_text())


def days_since(date_str: str) -> int:
    return (date.today() - datetime.strptime(date_str, "%Y-%m-%d").date()).days


def audit_iam_users(users: list[dict]) -> list[dict]:
    findings = []
    for u in users:
        if u["is_root"]:
            if u["access_keys"]:
                findings.append(mk("1.4", "CRITICAL", f"Root account '{u['username']}' has an active access key — root should never have programmatic access keys.", u["username"]))
            if not u["mfa_enabled"]:
                findings.append(mk("1.5", "CRITICAL", f"Root account '{u['username']}' does not have MFA enabled.", u["username"]))
            continue

        if u["has_console_password"] and not u["mfa_enabled"]:
            findings.append(mk("1.10", "HIGH", f"IAM user '{u['username']}' has console access but MFA is not enabled.", u["username"]))

        for key in u["access_keys"]:
            if not key["active"]:
                continue
            age = days_since(key["created_date"])
            if age > KEY_ROTATION_DAYS:
                findings.append(mk("1.14", "MEDIUM", f"Access key {key['id']} for '{u['username']}' is {age} days old (exceeds {KEY_ROTATION_DAYS}-day rotation policy).", u["username"]))
            idle = days_since(key["last_used_date"])
            if idle > CREDENTIAL_UNUSED_DAYS:
                findings.append(mk("1.12", "HIGH", f"Access key {key['id']} for '{u['username']}' unused for {idle} days (exceeds {CREDENTIAL_UNUSED_DAYS}-day threshold) — should be disabled.", u["username"]))
    return findings


def is_admin_statement(stmt: dict) -> bool:
    if stmt.get("Effect") != "Allow":
        return False
    actions = stmt.get("Action")
    actions = [actions] if isinstance(actions, str) else actions
    return any(a in ADMIN_ACTION_PATTERNS for a in actions) and stmt.get("Resource") == "*"


def audit_iam_policies(policies: list[dict]) -> list[dict]:
    findings = []
    for p in policies:
        statements = p["document"].get("Statement", [])
        if any(is_admin_statement(s) for s in statements):
            severity = "CRITICAL" if p["attached_to_type"] == "user" else "HIGH"
            findings.append(mk("1.16", severity,
                f"Policy '{p['policy_name']}' grants full administrative privileges (Action:*, Resource:*) and is attached directly to {p['attached_to_type']} '{p['attached_to']}'.",
                p["attached_to"]))
        if p["attached_to_type"] == "user":
            findings.append(mk("1.15", "LOW",
                f"Policy '{p['policy_name']}' is attached directly to user '{p['attached_to']}' instead of a group or role — harder to audit/manage at scale.",
                p["attached_to"]))
    return findings


def audit_s3_buckets(buckets: list[dict]) -> list[dict]:
    findings = []
    for b in buckets:
        name = b["bucket_name"]
        pab = b["public_access_block"]
        if not all(pab.values()):
            findings.append(mk("2.1.1", "CRITICAL", f"S3 bucket '{name}' does not have all four Block Public Access settings enabled.", name))
        if b["bucket_policy_allows_public"]:
            findings.append(mk("2.1.2", "CRITICAL", f"S3 bucket '{name}' has a bucket policy that allows public access.", name))
        if not b["encryption_enabled"]:
            findings.append(mk("2.1.5", "HIGH", f"S3 bucket '{name}' does not have default server-side encryption enabled.", name))
        if not b["versioning_enabled"]:
            findings.append(mk("2.1.3", "MEDIUM", f"S3 bucket '{name}' does not have versioning enabled (no protection against accidental/malicious overwrite or delete).", name))
        if not b["logging_enabled"]:
            findings.append(mk("2.6", "MEDIUM", f"S3 bucket '{name}' does not have access logging enabled.", name))
    return findings


def mk(control: str, severity: str, detail: str, resource: str) -> dict:
    return {"cis_control": control, "severity": severity, "detail": detail, "resource": resource}


def main():
    parser = argparse.ArgumentParser(description="Offline AWS IAM/S3 security audit against CIS AWS Foundations Benchmark")
    parser.add_argument("--json", help="Write full findings to this JSON file")
    args = parser.parse_args()

    users = load("iam_users.json")
    policies = load("iam_policies.json")
    buckets = load("s3_buckets.json")

    findings = audit_iam_users(users) + audit_iam_policies(policies) + audit_s3_buckets(buckets)
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda f: sev_order[f["severity"]])

    print(f"[*] Audited {len(users)} IAM users, {len(policies)} IAM policies, {len(buckets)} S3 buckets")
    print(f"[*] {len(findings)} finding(s)\n")

    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        print(f"[{f['severity']:<8}] CIS {f['cis_control']:<6} resource={f['resource']}")
        print(f"             {f['detail']}\n")

    print("Summary:", ", ".join(f"{sev}={n}" for sev, n in sorted(counts.items(), key=lambda kv: sev_order[kv[0]])))

    if args.json:
        Path(args.json).write_text(json.dumps(findings, indent=2))
        print(f"\n[+] Written to {args.json}")


if __name__ == "__main__":
    main()
