#!/usr/bin/env python3
"""
NIST CSF 2.0 Maturity Assessment Toolkit.

Ingests a category-level maturity assessment (current vs. target tier on
a 1-5 scale) across all six NIST CSF 2.0 Functions and produces the core
deliverable of a cyber maturity engagement:

  - Per-Function and overall current/target maturity scores
  - A gap analysis (target minus current) ranked by size
  - An ASCII maturity heat map
  - A prioritized, auto-generated client-ready Markdown report

This is the flagship artifact a security consultant delivers in a
posture/maturity assessment. Point it at a real client's scored
assessment JSON to generate their report.

Usage:
    python3 csf_maturity.py                                  # console summary
    python3 csf_maturity.py --report ../maturity_report.md   # write full report
"""

import argparse
import json
import statistics
from collections import OrderedDict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "assessment_responses.json"

FUNCTION_ORDER = ["GOVERN", "IDENTIFY", "PROTECT", "DETECT", "RESPOND", "RECOVER"]


def load():
    return json.loads(DATA.read_text())


def function_scores(categories):
    scores = OrderedDict()
    for fn in FUNCTION_ORDER:
        rows = [c for c in categories if c["function"] == fn]
        if not rows:
            continue
        scores[fn] = {
            "current": round(statistics.mean(c["current"] for c in rows), 2),
            "target": round(statistics.mean(c["target"] for c in rows), 2),
            "n": len(rows),
        }
        scores[fn]["gap"] = round(scores[fn]["target"] - scores[fn]["current"], 2)
    return scores


def overall(categories):
    cur = statistics.mean(c["current"] for c in categories)
    tgt = statistics.mean(c["target"] for c in categories)
    return round(cur, 2), round(tgt, 2), round(tgt - cur, 2)


def bar(value, width=20, maxv=5):
    filled = int(round((value / maxv) * width))
    return "█" * filled + "·" * (width - filled)


def priority_gaps(categories):
    ranked = sorted(categories, key=lambda c: (c["target"] - c["current"], c["target"]), reverse=True)
    return [c for c in ranked if c["target"] - c["current"] >= 2]


def print_console(data):
    cats = data["categories"]
    fscores = function_scores(cats)
    ocur, otgt, ogap = overall(cats)

    print(f"NIST CSF 2.0 Maturity Assessment — {data['engagement']['client']}")
    print(f"Assessment date: {data['engagement']['assessment_date']}\n")
    print(f"{'FUNCTION':<12}{'CURRENT':<9}{'TARGET':<8}{'GAP':<6}HEAT (current)")
    print("-" * 70)
    for fn, s in fscores.items():
        print(f"{fn:<12}{s['current']:<9}{s['target']:<8}{s['gap']:<6}{bar(s['current'])}")
    print("-" * 70)
    print(f"{'OVERALL':<12}{ocur:<9}{otgt:<8}{ogap:<6}{bar(ocur)}\n")

    print("Top priority gaps (target - current >= 2):")
    for c in priority_gaps(cats):
        print(f"  [{c['id']}] {c['name']:<45} {c['current']} -> {c['target']} (gap {c['target']-c['current']})")


def generate_report(data) -> str:
    cats = data["categories"]
    eng = data["engagement"]
    fscores = function_scores(cats)
    ocur, otgt, ogap = overall(cats)
    gaps = priority_gaps(cats)
    scale = data["engagement"]["maturity_scale"]

    lines = []
    lines.append(f"# NIST CSF 2.0 Cybersecurity Maturity Assessment")
    lines.append(f"\n**Client:** {eng['client']}  ")
    lines.append(f"**Prepared by:** {eng['assessor']}  ")
    lines.append(f"**Framework:** {eng['framework']}  ")
    lines.append(f"**Assessment date:** {eng['assessment_date']}\n")
    lines.append("---\n")

    lines.append("## 1. Executive Summary\n")
    lines.append(
        f"This assessment evaluated the organization's cybersecurity program across "
        f"all six NIST CSF 2.0 Functions and {len(cats)} categories, scoring each on a "
        f"1-5 maturity scale. The organization's **overall current maturity is {ocur} / 5.0** "
        f"against a **target of {otgt} / 5.0**, an aggregate gap of **{ogap}**. "
        f"The weakest Functions are **{_weakest(fscores)}**, driven largely by governance and "
        f"supply-chain gaps. {len(gaps)} categories carry a maturity gap of 2 or more tiers and "
        f"should anchor the remediation roadmap in Section 4.\n"
    )

    lines.append("## 2. Maturity Scale\n")
    for tier, desc in scale.items():
        lines.append(f"- **Tier {tier}** — {desc}")
    lines.append("")

    lines.append("## 3. Function-Level Results\n")
    lines.append("| Function | Current | Target | Gap |")
    lines.append("|---|---|---|---|")
    for fn, s in fscores.items():
        lines.append(f"| {fn} | {s['current']} | {s['target']} | {s['gap']} |")
    lines.append(f"| **OVERALL** | **{ocur}** | **{otgt}** | **{ogap}** |\n")

    lines.append("### Category detail\n")
    lines.append("| Function | Category | Current | Target | Gap | Observation |")
    lines.append("|---|---|---|---|---|---|")
    for c in cats:
        lines.append(f"| {c['function']} | {c['id']} {c['name']} | {c['current']} | {c['target']} | {c['target']-c['current']} | {c['notes']} |")
    lines.append("")

    lines.append("## 4. Prioritized Remediation Roadmap\n")
    lines.append(
        "Initiatives are ordered by maturity gap (largest first), which also "
        "approximates risk-reduction leverage. Suggested phasing assumes a "
        "12-month improvement program.\n")
    lines.append("| Priority | Category | Current → Target | Recommended action | Suggested phase |")
    lines.append("|---|---|---|---|---|")
    for i, c in enumerate(gaps, start=1):
        phase = "0-3 months" if i <= 3 else ("3-6 months" if i <= 6 else "6-12 months")
        lines.append(f"| {i} | {c['id']} {c['name']} | {c['current']} → {c['target']} | {_action_for(c)} | {phase} |")
    lines.append("")

    lines.append("## 5. Methodology\n")
    lines.append(
        "Each NIST CSF 2.0 category was scored 1-5 based on interviews, document "
        "review, and control inspection. Function scores are the mean of their "
        "category scores; the overall score is the mean across all categories. "
        "Target maturity reflects the organization's risk appetite and peer "
        "benchmark for its sector, not a blanket 'level 5 everywhere' goal — "
        "target tiers are deliberately set where the control's business value "
        "justifies the investment.\n")
    lines.append(
        "_Generated by `scripts/csf_maturity.py` from `sample_data/assessment_responses.json`._")
    return "\n".join(lines)


def _weakest(fscores):
    ranked = sorted(fscores.items(), key=lambda kv: kv[1]["current"])
    return " and ".join(fn for fn, _ in ranked[:2])


def _action_for(c):
    hints = {
        "GV.SC": "Stand up a third-party risk management program and vendor security review gate",
        "GV.OV": "Define program KPIs/KRIs and a quarterly cyber report to the board",
        "RC.CO": "Document a stakeholder and customer recovery communication plan",
        "GV.RM": "Draft a board-approved risk appetite statement and risk governance process",
        "GV.OC": "Document mission dependencies, critical services, and their supporting assets",
        "GV.PO": "Refresh and centrally govern the policy suite on an annual review cycle",
        "ID.AM": "Complete a unified asset inventory covering cloud and SaaS",
        "ID.RA": "Convert the annual assessment into a maintained, living risk register",
        "PR.DS": "Enforce at-rest encryption and deploy DLP on sensitive data stores",
        "PR.IR": "Define a segmentation/zero-trust target architecture and phased plan",
        "DE.AE": "Establish a detection-engineering function with tuning and coverage metrics",
        "RS.AN": "Standardize a forensics/timeline workflow and evidence-handling procedure",
        "RC.RP": "Institute scheduled, tested restore drills with documented RTO/RPO validation",
    }
    return hints.get(c["id"], f"Uplift {c['name']} controls to reach target tier {c['target']}")


def main():
    parser = argparse.ArgumentParser(description="NIST CSF 2.0 maturity assessment toolkit")
    parser.add_argument("--report", help="Write the full Markdown report to this path")
    args = parser.parse_args()

    data = load()
    print_console(data)

    if args.report:
        Path(args.report).write_text(generate_report(data) + "\n")
        print(f"\n[+] Full maturity report written to {args.report}")


if __name__ == "__main__":
    main()
