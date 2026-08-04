#!/usr/bin/env python3
"""
Financial-Services Regulatory Compliance Gap Assessment.

Financial services is KPMG's largest sector, and FS clients live under
overlapping cyber regulations. This tool assesses implementation status
against two of the most consequential — the **EU Digital Operational
Resilience Act (DORA)** and **NYDFS 23 NYCRR Part 500** — computing
per-regulation and per-pillar compliance, listing the gaps, and
generating a regulatory gap assessment with a remediation view.

Usage:
    python3 reg_compliance.py
    python3 reg_compliance.py --regulation DORA
    python3 reg_compliance.py --report ../regulatory_gap_assessment.md
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "regulatory_requirements.json"

STATUS_SCORE = {"met": 1.0, "partial": 0.5, "not_met": 0.0}
STATUS_LABEL = {"met": "Met", "partial": "Partial", "not_met": "Not met"}


def load():
    return json.loads(DATA.read_text())


def compliance_by_regulation(reqs):
    by_reg = defaultdict(list)
    for r in reqs:
        by_reg[r["regulation"]].append(r)
    out = {}
    for reg, rows in by_reg.items():
        score = sum(STATUS_SCORE[r["status"]] for r in rows)
        out[reg] = {
            "pct": round(100 * score / len(rows), 1),
            "met": sum(1 for r in rows if r["status"] == "met"),
            "partial": sum(1 for r in rows if r["status"] == "partial"),
            "not_met": sum(1 for r in rows if r["status"] == "not_met"),
            "total": len(rows),
        }
    return out


def compliance_by_pillar(reqs, regulation=None):
    by_pillar = defaultdict(list)
    for r in reqs:
        if regulation and r["regulation"] != regulation:
            continue
        by_pillar[(r["regulation"], r["pillar"])].append(r)
    out = {}
    for key, rows in by_pillar.items():
        score = sum(STATUS_SCORE[r["status"]] for r in rows)
        out[key] = round(100 * score / len(rows), 1)
    return out


def gaps(reqs, regulation=None):
    g = [r for r in reqs if r["status"] != "met" and (not regulation or r["regulation"] == regulation)]
    g.sort(key=lambda r: (STATUS_SCORE[r["status"]], r["id"]))
    return g


def print_console(data, regulation=None):
    reqs = data["requirements"]
    print(f"FS Regulatory Compliance — {data['engagement']['client']}  ({data['engagement']['date']})\n")
    cov = compliance_by_regulation(reqs)
    print(f"{'REGULATION':<14}{'COMPLIANCE':<12}{'MET':<6}{'PART':<6}{'GAP':<6}TOTAL")
    print("-" * 54)
    for reg, s in cov.items():
        if regulation and reg != regulation:
            continue
        print(f"{reg:<14}{str(s['pct'])+'%':<12}{s['met']:<6}{s['partial']:<6}{s['not_met']:<6}{s['total']}")

    g = gaps(reqs, regulation)
    print(f"\nOpen requirements ({len(g)}):")
    for r in g:
        print(f"  [{STATUS_LABEL[r['status']]:<7}] {r['id']:<14}{r['requirement'][:60]}")


def generate_report(data) -> str:
    reqs = data["requirements"]
    eng = data["engagement"]
    regs = data["regulations"]
    cov = compliance_by_regulation(reqs)
    pillars = compliance_by_pillar(reqs)

    L = []
    L.append("# Financial-Services Regulatory Compliance Gap Assessment\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Prepared by:** {eng['assessor']}  ")
    L.append(f"**Date:** {eng['date']}\n")
    L.append("**Regulations in scope:**  ")
    for k, v in regs.items():
        L.append(f"- **{k}** — {v}")
    L.append("\n---\n")

    L.append("## 1. Executive Summary\n")
    worst = min(cov.items(), key=lambda kv: kv[1]["pct"])
    total_gaps = sum(1 for r in reqs if r["status"] != "met")
    not_met = sum(1 for r in reqs if r["status"] == "not_met")
    L.append(
        f"This assessment measured implementation against {len(reqs)} requirements drawn "
        f"from DORA and NYDFS Part 500. Overall, **{worst[0]} is the weaker posture at "
        f"{worst[1]['pct']}%**. Across both regimes there are **{total_gaps} open "
        f"requirements ({not_met} entirely unmet)**. The unmet items cluster in DORA's "
        f"ICT third-party register, threat-led penetration testing, and asset mapping — "
        f"structural gaps that typically take the longest to close and should start now "
        f"given DORA's enforcement posture.\n")

    L.append("## 2. Compliance by Regulation\n")
    L.append("| Regulation | Compliance | Met | Partial | Not met | Total |")
    L.append("|---|---|---|---|---|---|")
    for reg, s in cov.items():
        L.append(f"| {reg} | {s['pct']}% | {s['met']} | {s['partial']} | {s['not_met']} | {s['total']} |")
    L.append("")

    L.append("## 3. Compliance by Pillar\n")
    L.append("| Regulation | Pillar | Compliance |")
    L.append("|---|---|---|")
    for (reg, pillar), pct in sorted(pillars.items()):
        L.append(f"| {reg} | {pillar} | {pct}% |")
    L.append("")

    L.append("## 4. Open Requirements (remediation backlog)\n")
    L.append("| Requirement | Regulation | Pillar | Status | Owner | Summary |")
    L.append("|---|---|---|---|---|---|")
    for r in gaps(reqs):
        L.append(f"| {r['id']} | {r['regulation']} | {r['pillar']} | {STATUS_LABEL[r['status']]} | {r['control_owner']} | {r['requirement']} |")
    L.append("")

    L.append("## 5. Recommended Sequencing\n")
    L.append(
        "1. **Structural 'not met' items first** — ICT third-party register (DORA-4.1), "
        "ICT asset mapping (DORA-1.2), and TLPT programme (DORA-3.2). These are "
        "foundational and long-lead.\n"
        "2. **Notification & reporting readiness** — align DORA major-incident reporting "
        "(DORA-2.2) and NYDFS 72-hour notification (NYDFS-500.17) into one incident "
        "workflow.\n"
        "3. **Access & encryption uplift** — close MFA (NYDFS-500.12), least-privilege "
        "(NYDFS-500.07), and encryption (NYDFS-500.15) gaps, which also advance the "
        "cross-framework crosswalk in Lab 09.\n"
        "4. **Testing cadence** — formalize pen-test/vulnerability cadence (NYDFS-500.05) "
        "within the DORA resilience-testing programme (DORA-3.1).\n")

    L.append("## 6. Methodology\n")
    L.append(
        "Each requirement was rated Met / Partial / Not met. Compliance percentages are "
        "the mean status score (Met=1.0, Partial=0.5, Not met=0.0) per regulation and "
        "per pillar. Requirement text is summarized for assessment purposes and should "
        "be read against the authoritative regulation with legal counsel.\n")
    L.append("_Generated by `scripts/reg_compliance.py` from the requirements register._")
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="FS regulatory compliance gap assessment (DORA + NYDFS 500)")
    parser.add_argument("--regulation", help="Filter console view to one regulation (DORA or NYDFS_500)")
    parser.add_argument("--report", help="Write full Markdown report to this path")
    args = parser.parse_args()

    data = load()
    print_console(data, args.regulation)

    if args.report:
        Path(args.report).write_text(generate_report(data) + "\n")
        print(f"\n[+] Full regulatory gap assessment written to {args.report}")


if __name__ == "__main__":
    main()
