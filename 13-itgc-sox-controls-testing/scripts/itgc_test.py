#!/usr/bin/env python3
"""
IT General Controls (ITGC) / SOX Controls Testing Workpaper Generator.

Models the core deliverable of a Big Four technology-risk / IT-audit
engagement: testing IT General Controls across the four standard domains
(Access to Programs and Data, Program Changes, Program Development,
Computer Operations) that a financial-statement audit (SOX 404) or a
SOC 1 examination relies upon.

For each control it:
  * Checks the sample size against attribute-sampling guidance derived
    from control frequency (annual → 1, quarterly → 2, ... daily → 15,
    recurring/manual → 25) for a low expected deviation rate.
  * Concludes operating effectiveness from exceptions found in the sample.
  * Evaluates deficiency severity (Deficiency / Significant Deficiency /
    Material Weakness) considering whether it is a key control and whether
    a compensating control exists.
  * Rolls results up to an overall opinion on whether reliance on ITGC
    (and the automated/application controls that depend on them) is
    supported.

Usage:
    python3 itgc_test.py
    python3 itgc_test.py --report ../itgc_testing_summary.md
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "itgc_controls.json"

# Simplified attribute-sampling minimum sample sizes for a low expected
# deviation rate, keyed by control operating frequency.
MIN_SAMPLE = {
    "annual": 1,
    "quarterly": 2,
    "monthly": 2,
    "weekly": 5,
    "daily": 15,
    "recurring": 25,   # many times per day / manual recurring
}

DOMAIN_ORDER = [
    "Access to Programs and Data",
    "Program Changes",
    "Program Development",
    "Computer Operations",
]


def load():
    return json.loads(DATA.read_text())


def min_sample_for(frequency, population):
    minimum = MIN_SAMPLE.get(frequency, 25)
    # Can never test more items than exist in the population.
    return min(minimum, population)


def evaluate_control(c):
    freq = c["frequency"]
    required = min_sample_for(freq, c["population"])
    sample_ok = c["sample_tested"] >= required

    exceptions = c["exceptions"]
    tod = c.get("test_of_design", "Effective")

    # Operating effectiveness conclusion.
    if tod == "Deficient":
        conclusion = "Deficient"
    elif exceptions == 0 and sample_ok:
        conclusion = "Effective"
    elif exceptions == 0 and not sample_ok:
        conclusion = "Inconclusive (insufficient sample)"
    else:
        conclusion = "Deficient"

    severity = deficiency_severity(c, conclusion)
    return {
        "id": c["id"], "domain": c["domain"], "description": c["description"],
        "key_control": c["key_control"], "frequency": freq, "population": c["population"],
        "required_sample": required, "sample_tested": c["sample_tested"], "sample_ok": sample_ok,
        "exceptions": exceptions, "test_of_design": tod,
        "conclusion": conclusion, "severity": severity,
        "compensating_control": c.get("compensating_control", False),
    }


def deficiency_severity(c, conclusion):
    if conclusion in ("Effective", "Inconclusive (insufficient sample)"):
        return None
    # Deficiency present. Severity depends on key-control status and
    # whether a compensating control mitigates the exposure.
    if not c["key_control"]:
        return "Deficiency"
    if c.get("compensating_control", False):
        return "Deficiency"
    # Key control with no compensating control failing → elevate.
    # A high exception rate on a key control suggests pervasiveness.
    rate = c["exceptions"] / max(1, c["sample_tested"])
    if rate >= 0.20:
        return "Significant Deficiency (assess for Material Weakness)"
    return "Significant Deficiency"


def summarize(results):
    total = len(results)
    effective = sum(1 for r in results if r["conclusion"] == "Effective")
    deficient = [r for r in results if r["conclusion"] == "Deficient"]
    inconclusive = [r for r in results if r["conclusion"].startswith("Inconclusive")]
    sig_def = [r for r in results if r["severity"] and r["severity"].startswith("Significant")]
    key_deficient = [r for r in deficient if r["key_control"]]
    reliance = "Supported" if not sig_def and not inconclusive else "NOT supported without remediation / additional procedures"
    return {
        "total": total, "effective": effective, "deficient": deficient,
        "inconclusive": inconclusive, "significant": sig_def,
        "key_deficient": key_deficient, "reliance": reliance,
    }


def print_console(data, results, summ):
    eng = data["engagement"]
    print(f"ITGC / SOX Controls Testing — {eng['client']}")
    print(f"Period: {eng['period']} | Scope: {eng['scope']}\n")
    print(f"{'CONTROL':<13}{'KEY':<5}{'FREQ':<11}{'SAMPLE':<9}{'EXC':<5}{'CONCLUSION':<14}SEVERITY")
    print("-" * 90)
    for r in results:
        key = "Y" if r["key_control"] else "-"
        sample = f"{r['sample_tested']}/{r['required_sample']}"
        sev = r["severity"] or ""
        print(f"{r['id']:<13}{key:<5}{r['frequency']:<11}{sample:<9}{r['exceptions']:<5}{r['conclusion']:<14}{sev}")
    print("-" * 90)
    print(f"Effective: {summ['effective']}/{summ['total']}  |  Deficient: {len(summ['deficient'])}  |  "
          f"Significant deficiencies: {len(summ['significant'])}  |  Inconclusive: {len(summ['inconclusive'])}")
    print(f"\nReliance on ITGC for automated-control / SOC 1 purposes: {summ['reliance']}")


def generate_report(data, results, summ) -> str:
    eng = data["engagement"]
    L = []
    L.append("# IT General Controls (ITGC) Testing Summary\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Function:** {eng['auditor']}  ")
    L.append(f"**Scope:** {eng['scope']}  ")
    L.append(f"**Period:** {eng['period']}  ")
    L.append(f"**In-scope systems:** {', '.join(eng['in_scope_systems'])}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    L.append(
        f"IT General Controls were tested across the four standard domains supporting "
        f"the {eng['scope']}. Of {summ['total']} controls tested, "
        f"**{summ['effective']} operated effectively** and **{len(summ['deficient'])} were "
        f"deficient** ({len(summ['significant'])} rising to a significant deficiency). "
        f"Overall, reliance on ITGC to support automated application controls and the "
        f"financial-statement / SOC 1 audit is **{summ['reliance']}**. "
        f"{'The significant deficiency in change-management segregation of duties (ITGC-CM-02) is the primary driver and requires remediation plus expanded substantive testing.' if summ['significant'] else ''}\n")

    L.append("## 2. Results by ITGC Domain\n")
    by_domain = defaultdict(list)
    for r in results:
        by_domain[r["domain"]].append(r)
    L.append("| Domain | Controls | Effective | Deficient |")
    L.append("|---|---|---|---|")
    for d in DOMAIN_ORDER:
        rows = by_domain.get(d, [])
        if not rows:
            continue
        eff = sum(1 for r in rows if r["conclusion"] == "Effective")
        dfc = sum(1 for r in rows if r["conclusion"] == "Deficient")
        L.append(f"| {d} | {len(rows)} | {eff} | {dfc} |")
    L.append("")

    L.append("## 3. Control Testing Detail\n")
    L.append("| Control | Domain | Key | Freq | Sample (tested/req'd) | Exceptions | Conclusion | Severity |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        key = "Yes" if r["key_control"] else "No"
        sample = f"{r['sample_tested']}/{r['required_sample']}" + ("" if r["sample_ok"] else " ⚠")
        L.append(f"| {r['id']} | {r['domain']} | {key} | {r['frequency'].title()} | {sample} | "
                 f"{r['exceptions']} | {r['conclusion']} | {r['severity'] or '—'} |")
    L.append("")

    L.append("## 4. Exceptions & Deficiencies\n")
    deficiencies = [r for r in results if r["conclusion"] == "Deficient"]
    if not deficiencies:
        L.append("No deficiencies identified.\n")
    for r in deficiencies:
        L.append(f"### {r['id']} — {r['description']}\n")
        L.append(f"- **Domain:** {r['domain']} | **Key control:** {'Yes' if r['key_control'] else 'No'}")
        L.append(f"- **Testing:** {r['exceptions']} exception(s) in a sample of {r['sample_tested']} "
                 f"(minimum required {r['required_sample']} for a {r['frequency']} control)")
        L.append(f"- **Compensating control:** {'Yes' if r['compensating_control'] else 'None identified'}")
        L.append(f"- **Preliminary severity:** {r['severity']}")
        L.append(f"- **Recommendation:** {_recommendation(r)}\n")

    L.append("## 5. Impact on Audit Reliance\n")
    L.append(
        "Where a key ITGC is deficient, the automated application controls and "
        "system-generated reports that depend on it can no longer be relied upon "
        "without additional procedures. In this engagement:\n")
    if summ["key_deficient"]:
        for r in summ["key_deficient"]:
            L.append(f"- **{r['id']}** deficiency → expand substantive testing over affected "
                     f"processes and system-generated reports; assess management's remediation.")
    else:
        L.append("- No key controls were deficient; reliance on ITGC is supported.")
    L.append("")

    L.append("## 6. Methodology\n")
    L.append(
        "Each control was assessed for design (test of design) and operating "
        "effectiveness (test of operating effectiveness). Sample sizes were "
        "evaluated against attribute-sampling minimums for a low expected "
        "deviation rate (annual 1, quarterly 2, monthly 2, weekly 5, daily 15, "
        "recurring/manual 25), capped at population size. A control with any "
        "exception (or a failed design) is concluded Deficient; severity is "
        "elevated for key controls lacking a compensating control, with a high "
        "exception rate flagged for material-weakness assessment. This is the "
        "same evidence chain used for SOX 404 and SOC 1 (Type II) reporting.\n")
    L.append("_Generated by `scripts/itgc_test.py` from `sample_data/itgc_controls.json`._")
    return "\n".join(L)


def _recommendation(r):
    if "Segregation of duties" in r["description"] or "migrate their own" in r["description"]:
        return ("Enforce technical segregation so developers cannot deploy to production; "
                "route migrations through an independent release function and retain approval evidence.")
    if "terminat" in r["description"].lower():
        return ("Automate deprovisioning from the HR leaver feed and reconcile weekly; "
                "investigate the terminated users whose access persisted for residual risk.")
    if "Privileged" in r["description"]:
        return ("Complete the overdue privileged-access review and implement just-in-time elevation; "
                "the compensating logging control limits but does not eliminate the exposure.")
    if "back" in r["description"].lower():
        return "Perform and document the missed restoration test; add a calendar control with evidence retention."
    return "Remediate the control gap and retain evidence; re-test in the next period."


def main():
    parser = argparse.ArgumentParser(description="ITGC / SOX controls testing workpaper generator")
    parser.add_argument("--report", help="Write full Markdown workpaper to this path")
    args = parser.parse_args()

    data = load()
    results = [evaluate_control(c) for c in data["controls"]]
    summ = summarize(results)
    print_console(data, results, summ)

    if args.report:
        Path(args.report).write_text(generate_report(data, results, summ) + "\n")
        print(f"\n[+] Full ITGC testing summary written to {args.report}")


if __name__ == "__main__":
    main()
