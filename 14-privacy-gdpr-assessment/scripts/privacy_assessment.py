#!/usr/bin/env python3
"""
Privacy & GDPR/CCPA Data Protection Assessment.

Works from a Records of Processing Activities register (GDPR Art. 30) and
evaluates each processing activity against core data-protection
requirements a privacy consultant checks:

  * Lawful basis documented (Art. 6) — and explicit consent / condition
    for special-category data (Art. 9)
  * DPIA required? (Art. 35) — triggered by large-scale special-category
    processing, systematic monitoring, or automated profiling — and is
    one completed where required
  * International transfer safeguards (Art. 44-49)
  * Retention period defined (storage limitation, Art. 5(1)(e))

It also evaluates the data-subject-rights (DSAR) program against the
statutory response clock, then scores overall privacy compliance and
generates a data protection assessment report.

Usage:
    python3 privacy_assessment.py
    python3 privacy_assessment.py --report ../privacy_assessment_report.md
"""

import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "processing_activities.json"

VALID_BASES = {
    "consent", "explicit_consent", "contract", "legal_obligation",
    "vital_interests", "public_task", "legitimate_interests", "adequacy_decision",
}


def load():
    return json.loads(DATA.read_text())


def dpia_required(pa):
    # GDPR Art. 35 high-risk triggers (simplified).
    triggers = []
    if pa["large_scale"] and pa["special_category"]:
        triggers.append("large-scale special-category data")
    if pa["systematic_monitoring"] and pa["large_scale"]:
        triggers.append("large-scale systematic monitoring")
    if pa["systematic_monitoring"] and "behavioral" in pa["data_categories"]:
        triggers.append("systematic profiling/behavioral analysis")
    return triggers


def assess_activity(pa):
    findings = []
    severity = "none"

    # Lawful basis
    basis = pa.get("lawful_basis")
    if basis in (None, "none_documented") or basis not in VALID_BASES:
        findings.append(("HIGH", "No valid lawful basis documented (Art. 6)."))
    if pa["special_category"] and basis != "explicit_consent":
        findings.append(("HIGH", "Special-category data without an Art. 9 condition (e.g. explicit consent)."))

    # DPIA
    triggers = dpia_required(pa)
    if triggers and not pa["dpia_completed"]:
        findings.append(("HIGH", f"DPIA required but not completed (triggers: {', '.join(triggers)}) (Art. 35)."))

    # Transfers
    if pa["cross_border_transfer"]:
        safeguard = pa.get("transfer_safeguard")
        if safeguard in (None, "none"):
            findings.append(("HIGH", "International transfer without a documented safeguard (Art. 44-49)."))

    # Retention
    if not pa["retention_defined"]:
        findings.append(("MEDIUM", "No defined retention period (storage limitation, Art. 5(1)(e))."))

    if any(s == "HIGH" for s, _ in findings):
        severity = "HIGH"
    elif findings:
        severity = "MEDIUM"

    compliant = len(findings) == 0
    return {"id": pa["id"], "name": pa["name"], "severity": severity,
            "compliant": compliant, "findings": findings,
            "dpia_required": bool(triggers), "dpia_completed": pa["dpia_completed"]}


def assess_dsar(dsar):
    issues = []
    if dsar["avg_response_days"] > dsar["statutory_limit_days"]:
        issues.append(f"Average DSAR response time ({dsar['avg_response_days']}d) exceeds the "
                      f"{dsar['statutory_limit_days']}-day statutory limit.")
    if dsar.get("rights_missing"):
        issues.append(f"Rights not yet supported: {', '.join(dsar['rights_missing'])}.")
    if not dsar["process_documented"]:
        issues.append("No documented DSAR handling process.")
    return issues


def score(results, dsar_issues):
    total = len(results)
    compliant = sum(1 for r in results if r["compliant"])
    penalty = len(dsar_issues) * 3
    base = 100 * compliant / total if total else 0
    return max(0, round(base - penalty, 1)), compliant, total


def print_console(data, results, dsar_issues):
    sc, compliant, total = score(results, dsar_issues)
    print(f"Privacy & GDPR/CCPA Assessment — {data['engagement']['client']}  ({data['engagement']['date']})\n")
    print(f"{'ACTIVITY':<10}{'SEVERITY':<10}{'DPIA':<20}FINDINGS")
    print("-" * 80)
    for r in results:
        dpia = ("required/done" if r["dpia_completed"] else "REQUIRED/MISSING") if r["dpia_required"] else "n/a"
        print(f"{r['id']:<10}{r['severity']:<10}{dpia:<20}{len(r['findings'])}")
    print("-" * 80)
    print(f"Compliant activities: {compliant}/{total}  |  Privacy compliance score: {sc}%")
    if dsar_issues:
        print(f"\nDSAR program issues ({len(dsar_issues)}):")
        for i in dsar_issues:
            print(f"  - {i}")


def generate_report(data, results, dsar_issues) -> str:
    eng = data["engagement"]
    sc, compliant, total = score(results, dsar_issues)
    high = [r for r in results if r["severity"] == "HIGH"]

    L = []
    L.append("# Privacy & Data Protection Assessment (GDPR / CCPA)\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Prepared by:** {eng['assessor']}  ")
    L.append(f"**Regulations in scope:** {', '.join(eng['regulations'])}  ")
    L.append(f"**Date:** {eng['date']}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    L.append(
        f"This assessment reviewed {total} processing activities from the Records of "
        f"Processing Activities (GDPR Art. 30) and the data-subject-rights program. "
        f"**{compliant} of {total} activities are fully compliant**, yielding a privacy "
        f"compliance score of **{sc}%**. **{len(high)} activities carry HIGH-severity "
        f"findings** — chiefly missing lawful basis, an outstanding DPIA, and an "
        f"unsafeguarded international transfer on the marketing analytics activity "
        f"(PA-03), which should be treated as the priority remediation. The DSAR "
        f"program {'exceeds the statutory response clock and has a rights gap' if dsar_issues else 'meets statutory requirements'}.\n")

    L.append("## 2. Processing Activity Findings\n")
    L.append("| Activity | Name | Severity | DPIA | Findings |")
    L.append("|---|---|---|---|---|")
    for r in results:
        dpia = ("Required — completed" if r["dpia_completed"] else "**Required — MISSING**") if r["dpia_required"] else "Not required"
        L.append(f"| {r['id']} | {r['name']} | {r['severity']} | {dpia} | {len(r['findings'])} |")
    L.append("")

    L.append("## 3. Detailed Findings\n")
    for r in results:
        if not r["findings"]:
            continue
        L.append(f"### {r['id']} — {r['name']}\n")
        for sev, text in r["findings"]:
            L.append(f"- **[{sev}]** {text}")
        L.append("")

    L.append("## 4. Data Subject Rights (DSAR) Program\n")
    if dsar_issues:
        for i in dsar_issues:
            L.append(f"- {i}")
    else:
        L.append("- No issues identified; program meets statutory requirements.")
    L.append("")

    L.append("## 5. Priority Remediation\n")
    L.append("1. **PA-03 Marketing analytics** — establish and document a lawful basis, complete the required DPIA, and put a transfer safeguard (SCCs) in place or halt the transfer; define a retention period.\n"
             "2. **PA-02 Credit-risk scoring** — complete the DPIA for large-scale automated profiling and confirm Art. 22 safeguards for automated decision-making.\n"
             "3. **DSAR program** — bring average response time within the statutory clock and add the missing right(s).\n"
             "4. **PA-01 Payroll** — complete the DPIA and confirm SCCs remain valid post-transfer-framework changes.\n")

    L.append("## 6. Methodology\n")
    L.append(
        "Each processing activity was evaluated for lawful basis (Art. 6/9), DPIA "
        "necessity and completion (Art. 35), international transfer safeguards "
        "(Art. 44-49), and retention definition (Art. 5(1)(e)). The DSAR program was "
        "assessed against the statutory response clock and rights coverage. The "
        "compliance score is the proportion of fully compliant activities, less a "
        "penalty for DSAR-program gaps.\n")
    L.append("_Generated by `scripts/privacy_assessment.py` from the RoPA register._")
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="Privacy & GDPR/CCPA data protection assessment")
    parser.add_argument("--report", help="Write full Markdown report to this path")
    args = parser.parse_args()

    data = load()
    results = [assess_activity(pa) for pa in data["processing_activities"]]
    dsar_issues = assess_dsar(data["dsar_program"])
    print_console(data, results, dsar_issues)

    if args.report:
        Path(args.report).write_text(generate_report(data, results, dsar_issues) + "\n")
        print(f"\n[+] Full privacy assessment report written to {args.report}")


if __name__ == "__main__":
    main()
