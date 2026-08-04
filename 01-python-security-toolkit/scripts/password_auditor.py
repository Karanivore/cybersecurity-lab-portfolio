#!/usr/bin/env python3
"""
Password Strength & Breach-Exposure Auditor.

Scores passwords on entropy/composition and checks them against a local
common-password corpus. Optionally checks live breach exposure via the
Have I Been Pwned k-anonymity API (no plaintext password ever leaves the
machine — only a 5-char SHA-1 prefix is sent).

Usage:
    python3 password_auditor.py "P@ssw0rd123"
    python3 password_auditor.py --file passwords.txt
    python3 password_auditor.py "hunter2" --check-hibp
"""

import argparse
import hashlib
import math
import re
import sys
from pathlib import Path

COMMON_LIST_PATH = Path(__file__).resolve().parent.parent / "sample_data" / "common_passwords.txt"

KEYBOARD_WALKS = ["qwerty", "asdfgh", "zxcvbn", "12345", "09876", "qazwsx"]


def load_common_passwords() -> set[str]:
    if not COMMON_LIST_PATH.exists():
        return set()
    return {line.strip().lower() for line in COMMON_LIST_PATH.read_text().splitlines() if line.strip()}


def shannon_entropy(password: str) -> float:
    """Approximate brute-force entropy in bits based on character pool size."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 33
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def has_keyboard_walk(password: str) -> bool:
    lowered = password.lower()
    return any(walk in lowered for walk in KEYBOARD_WALKS)


def has_repeated_chars(password: str) -> bool:
    return bool(re.search(r"(.)\1{2,}", password))


def check_hibp_k_anonymity(password: str) -> int | None:
    """Return breach count via HIBP k-anonymity API, or None if unreachable."""
    try:
        import requests
    except ImportError:
        return None
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        resp.raise_for_status()
    except Exception:
        return None
    for line in resp.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0


def audit_password(password: str, common: set[str], check_hibp: bool) -> dict:
    entropy = shannon_entropy(password)
    findings = []

    if len(password) < 12:
        findings.append("Below recommended minimum length (12 characters)")
    if password.lower() in common:
        findings.append("Found in common/breached password corpus")
    if has_keyboard_walk(password):
        findings.append("Contains a keyboard-walk pattern (e.g. qwerty)")
    if has_repeated_chars(password):
        findings.append("Contains 3+ repeated characters in a row")
    if not re.search(r"[A-Z]", password):
        findings.append("Missing uppercase letters")
    if not re.search(r"[0-9]", password):
        findings.append("Missing digits")
    if not re.search(r"[^a-zA-Z0-9]", password):
        findings.append("Missing special characters")

    if entropy >= 80 and not findings:
        verdict = "STRONG"
    elif entropy >= 50 and len(findings) <= 2:
        verdict = "MODERATE"
    else:
        verdict = "WEAK"

    result = {
        "password": password,
        "length": len(password),
        "entropy_bits": round(entropy, 1),
        "verdict": verdict,
        "findings": findings or ["No composition weaknesses detected"],
    }

    if check_hibp:
        breach_count = check_hibp_k_anonymity(password)
        if breach_count is None:
            result["hibp"] = "unreachable (offline or network blocked)"
        elif breach_count > 0:
            result["hibp"] = f"COMPROMISED — seen in {breach_count:,} known breaches"
            result["verdict"] = "WEAK"
        else:
            result["hibp"] = "not found in known breach corpus"

    return result


def print_result(result: dict) -> None:
    masked = result["password"][:2] + "*" * max(len(result["password"]) - 2, 0)
    print(f"\nPassword: {masked}  (len={result['length']}, entropy={result['entropy_bits']} bits)")
    print(f"Verdict:  {result['verdict']}")
    for f in result["findings"]:
        print(f"  - {f}")
    if "hibp" in result:
        print(f"  HIBP: {result['hibp']}")


def main():
    parser = argparse.ArgumentParser(description="Password strength & breach-exposure auditor")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("password", nargs="?", help="Password to audit")
    group.add_argument("--file", help="Path to newline-delimited password list to audit in bulk")
    parser.add_argument("--check-hibp", action="store_true", help="Check live breach exposure via HIBP k-anonymity API")
    args = parser.parse_args()

    common = load_common_passwords()

    if args.file:
        passwords = [l.strip() for l in Path(args.file).read_text().splitlines() if l.strip()]
    else:
        passwords = [args.password]

    weak_count = 0
    for pw in passwords:
        result = audit_password(pw, common, args.check_hibp)
        print_result(result)
        if result["verdict"] == "WEAK":
            weak_count += 1

    if len(passwords) > 1:
        print(f"\nSummary: {weak_count}/{len(passwords)} passwords flagged WEAK")

    sys.exit(1 if weak_count else 0)


if __name__ == "__main__":
    main()
