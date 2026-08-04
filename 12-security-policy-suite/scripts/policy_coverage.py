#!/usr/bin/env python3
"""
ISMS Policy Coverage Checker.

A common ISO 27001 audit finding is a control theme with no owning
policy. This tool reads the Annex A → policy mapping, confirms every
referenced policy file actually exists on disk, and reports any Annex A
theme left without an owning policy (a documentation gap to close before
certification).

Usage:
    python3 policy_coverage.py
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MAPPING = BASE / "control_to_policy_mapping.json"
POLICY_DIR = BASE / "policies"


def main():
    data = json.loads(MAPPING.read_text())
    policies = data["policies"]
    themes = data["annex_a_themes"]

    # 1. Verify each referenced policy file exists.
    print("Policy files:")
    missing_files = []
    for code, filename in policies.items():
        exists = (POLICY_DIR / filename).exists()
        print(f"  {code:<5} {filename:<38} {'OK' if exists else 'MISSING'}")
        if not exists:
            missing_files.append(filename)

    # 2. Coverage of Annex A themes.
    covered = [t for t in themes if t["owning_policy"]]
    uncovered = [t for t in themes if not t["owning_policy"]]
    pct = round(100 * len(covered) / len(themes), 1)

    print(f"\nAnnex A theme coverage: {len(covered)}/{len(themes)} ({pct}%)\n")
    print(f"{'CONTROL':<9}{'OWNING POLICY':<16}THEME")
    print("-" * 70)
    for t in themes:
        owner = policies.get(t["owning_policy"], "— NONE —") if t["owning_policy"] else "— NONE —"
        flag = "" if t["owning_policy"] else "  <-- GAP"
        print(f"{t['control']:<9}{(t['owning_policy'] or 'none'):<16}{t['name']}{flag}")

    if uncovered:
        print(f"\n[!] {len(uncovered)} Annex A theme(s) have no owning policy — documentation gap:")
        for t in uncovered:
            print(f"    - {t['control']} {t['name']}")
        print("    Recommendation: add a Supplier Security Policy (A.5.19), a Threat")
        print("    Intelligence procedure (A.5.7), and a Backup Policy (A.8.13) to close these.")

    if missing_files:
        print(f"\n[!] {len(missing_files)} referenced policy file(s) missing from disk.")
        sys.exit(1)

    # Exit non-zero if documentation gaps exist (useful in CI for a real ISMS repo).
    sys.exit(1 if uncovered else 0)


if __name__ == "__main__":
    main()
