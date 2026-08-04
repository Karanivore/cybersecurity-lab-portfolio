#!/usr/bin/env python3
"""
SOC 2 / ISO 27001 Readiness Assessment & Remediation Roadmap.

Before a company pays for a SOC 2 Type II or ISO 27001 audit, a
consultant runs a readiness (gap) assessment: control-by-control, is it
Met / Partial / Not met, and is there audit-ready evidence? This tool
computes a readiness score, separates "control gap" from "evidence gap"
(a distinction auditors care about — a working control with no evidence
still fails), and generates a prioritized remediation roadmap sequenced
by risk and effort.

Usage:
    python3 readiness.py
    python3 readiness.py --report ../readiness_report.md
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "soc2_readiness.json"

STATUS_SCORE = {"met": 1.0, "partial": 0.5, "not_met": 0.0, "not_applicable": None}
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2}
STATUS_RANK = {"not_met": 0, "partial": 1, "met": 2}


def load():
    return json.loads(DATA.read_text())


def readiness_score(controls):
    scored = [c for c in controls if STATUS_SCORE[c["status"]] is not None]
    if not scored:
        return 0.0
    return round(100 * sum(STATUS_SCORE[c["status"]] for c in scored) / len(scored), 1)


def category_breakdown(controls):
    by_cat = defaultdict(list)
    for c in controls:
        by_cat[c["category"]].append(c)
    out = {}
    for cat, rows in by_cat.items():
        out[cat] = {"score": readiness_score(rows), "n": len(rows)}
    return out


def gaps(controls):
    control_gaps = [c for c in controls if c["status"] in ("not_met", "partial")]
    evidence_gaps = [c for c in controls if c["status"] in ("met", "partial") and not c["evidence"]]
    return control_gaps, evidence_gaps


def roadmap(controls):
    open_items = [c for c in controls if c["status"] != "met" or not c["evidence"]]
    # Sequence: worst control status first, then lowest effort (quick wins early within a tier).
    open_items.sort(key=lambda c: (STATUS_RANK[c["status"]], EFFORT_RANK[c["effort"]]))
    return open_items


def print_console(data):
    controls = data["controls"]
    score = readiness_score(controls)
    cg, eg = gaps(controls)
    print(f"SOC 2 / ISO 27001 Readiness — {data['engagement']['client']}  ({data['engagement']['date']})\n")
    print(f"Overall readiness score: {score}%")
    met = sum(1 for c in controls if c['status'] == 'met')
    print(f"Controls: {met} met / {sum(1 for c in controls if c['status']=='partial')} partial / "
          f"{sum(1 for c in controls if c['status']=='not_met')} not met  (of {len(controls)})")
    print(f"Control gaps: {len(cg)}   |   Evidence gaps (control OK but no evidence): {len(eg)}\n")

    print(f"{'CATEGORY':<30}{'SCORE':<8}CONTROLS")
    print("-" * 50)
    for cat, s in category_breakdown(controls).items():
        print(f"{cat:<30}{str(s['score'])+'%':<8}{s['n']}")


def phase_for(index):
    if index < 4:
        return "Phase 1 (0-30 days)"
    if index < 9:
        return "Phase 2 (30-90 days)"
    return "Phase 3 (90-180 days)"


def generate_report(data) -> str:
    eng = data["engagement"]
    controls = data["controls"]
    score = readiness_score(controls)
    cg, eg = gaps(controls)
    rm = roadmap(controls)

    L = []
    L.append("# SOC 2 / ISO 27001 Readiness Assessment\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Prepared by:** {eng['assessor']}  ")
    L.append(f"**Framework:** {eng['framework']}  ")
    L.append(f"**Assessment type:** {eng['assessment_type']}  ")
    L.append(f"**Date:** {eng['date']}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    L.append(
        f"The organization is **{score}% ready** for a SOC 2 Type II examination. "
        f"Of {len(controls)} in-scope criteria, {sum(1 for c in controls if c['status']=='met')} "
        f"are fully met, {sum(1 for c in controls if c['status']=='partial')} are partially "
        f"implemented, and {sum(1 for c in controls if c['status']=='not_met')} are not met. "
        f"There are **{len(cg)} control gaps** and **{len(eg)} evidence gaps** (controls that "
        f"appear to operate but lack the audit-ready evidence an examiner requires). We do not "
        f"recommend entering the audit window until Phase 1 and Phase 2 items below are closed; "
        f"proceeding now would risk qualified exceptions in the report.\n")

    L.append("## 2. Readiness by Category\n")
    L.append("| TSC Category | Readiness | Controls |")
    L.append("|---|---|---|")
    for cat, s in category_breakdown(controls).items():
        L.append(f"| {cat} | {s['score']}% | {s['n']} |")
    L.append(f"| **Overall** | **{score}%** | **{len(controls)}** |\n")

    L.append("## 3. Control Status Detail (with ISO 27001:2022 cross-reference)\n")
    L.append("| Criterion | Category | Status | Evidence | ISO 27001 ref | Owner |")
    L.append("|---|---|---|---|---|---|")
    for c in controls:
        ev = "✅" if c["evidence"] else "❌ missing"
        L.append(f"| {c['id']} | {c['category']} | {c['status'].replace('_',' ').title()} | {ev} | {c['iso_ref']} | {c['owner']} |")
    L.append("")

    L.append("## 4. Evidence Gaps (highest audit risk)\n")
    L.append("These controls may operate effectively but have **no audit-ready evidence** — an examiner will treat them as exceptions regardless of whether the control works:\n")
    for c in eg:
        L.append(f"- **{c['id']} {c['description']}** — owner: {c['owner']}. Produce and retain evidence (policy, ticket, log, or screenshot with date).")
    L.append("")

    L.append("## 5. Prioritized Remediation Roadmap\n")
    L.append("Sequenced by control status (not-met first) then effort (quick wins early). Assumes a 180-day runway to audit.\n")
    L.append("| # | Criterion | Description | Status | Effort | Owner | Phase |")
    L.append("|---|---|---|---|---|---|---|")
    for i, c in enumerate(rm):
        L.append(f"| {i+1} | {c['id']} | {c['description']} | {c['status'].replace('_',' ').title()} | {c['effort'].title()} | {c['owner']} | {phase_for(i)} |")
    L.append("")

    L.append("## 6. Methodology\n")
    L.append(
        "Each Trust Services Criterion in scope was rated Met / Partial / Not met and "
        "flagged for evidence availability. Readiness score = mean of status scores "
        "(Met=1.0, Partial=0.5, Not met=0.0; N/A excluded). The roadmap sequences open "
        "items by status severity then implementation effort, so quick wins land early "
        "and the highest-risk gaps are not deferred. ISO 27001:2022 Annex A references "
        "are provided so a single remediation effort can support both certifications.\n")
    L.append("_Generated by `scripts/readiness.py` from `sample_data/soc2_readiness.json`._")
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="SOC 2 / ISO 27001 readiness assessment + roadmap")
    parser.add_argument("--report", help="Write full Markdown report to this path")
    args = parser.parse_args()

    data = load()
    print_console(data)

    if args.report:
        Path(args.report).write_text(generate_report(data) + "\n")
        print(f"\n[+] Full readiness report written to {args.report}")


if __name__ == "__main__":
    main()
