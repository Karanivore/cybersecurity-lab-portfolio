#!/usr/bin/env python3
"""
Compliance Framework Crosswalk / Control Mapping Engine.

Consultants constantly answer "we're ISO 27001 certified — how much of
SOC 2 / NIST CSF / CIS do we already cover?" This engine maps a single
set of control themes across five frameworks (NIST CSF 2.0, NIST SP
800-53, ISO/IEC 27001:2022, CIS Controls v8, SOC 2 TSC) and reports:

  - Per-framework implementation coverage (implement once, satisfy many)
  - The specific control gaps blocking each framework
  - A reverse lookup: given a control ID in any framework, show its
    equivalents in every other framework

Usage:
    python3 crosswalk.py                                  # coverage summary
    python3 crosswalk.py --lookup "A.8.8"                # find a control across frameworks
    python3 crosswalk.py --framework ISO_27001           # gap list for one framework
    python3 crosswalk.py --report ../crosswalk_report.md
"""

import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "control_crosswalk.json"

STATUS_WEIGHT = {"implemented": 1.0, "partial": 0.5, "not_implemented": 0.0}
STATUS_LABEL = {"implemented": "Implemented", "partial": "Partial", "not_implemented": "Not implemented"}


def load():
    return json.loads(DATA.read_text())


def coverage(data):
    frameworks = data["meta"]["frameworks"]
    controls = data["controls"]
    result = {}
    for fw in frameworks:
        mapped = [c for c in controls if c["map"].get(fw)]
        if not mapped:
            continue
        score = sum(STATUS_WEIGHT[c["status"]] for c in mapped)
        result[fw] = {
            "coverage_pct": round(100 * score / len(mapped), 1),
            "implemented": sum(1 for c in mapped if c["status"] == "implemented"),
            "partial": sum(1 for c in mapped if c["status"] == "partial"),
            "gap": sum(1 for c in mapped if c["status"] == "not_implemented"),
            "total": len(mapped),
        }
    return result


def gaps_for_framework(data, fw):
    return [c for c in data["controls"] if c["map"].get(fw) and c["status"] != "implemented"]


def lookup(data, control_id):
    q = control_id.strip().lower()
    hits = []
    for c in data["controls"]:
        for fw, ids in c["map"].items():
            if q in ids.lower():
                hits.append(c)
                break
    return hits


def print_coverage(data):
    cov = coverage(data)
    print(f"{data['meta']['title']}\n")
    print(f"{'FRAMEWORK':<14}{'COVERAGE':<11}{'IMPL':<6}{'PART':<6}{'GAP':<5}{'TOTAL'}")
    print("-" * 52)
    for fw, s in cov.items():
        print(f"{fw:<14}{str(s['coverage_pct'])+'%':<11}{s['implemented']:<6}{s['partial']:<6}{s['gap']:<5}{s['total']}")
    print("\nInterpretation: implementing the shared control themes below satisfies")
    print("multiple frameworks at once. Focus remediation on themes marked 'Not implemented'.")


def generate_report(data) -> str:
    cov = coverage(data)
    controls = data["controls"]
    L = []
    L.append(f"# {data['meta']['title']}\n")
    L.append(f"> {data['meta']['note']}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    worst = min(cov.items(), key=lambda kv: kv[1]["coverage_pct"])
    best = max(cov.items(), key=lambda kv: kv[1]["coverage_pct"])
    not_impl = [c for c in controls if c["status"] == "not_implemented"]
    L.append(
        f"This crosswalk maps {len(controls)} control themes across "
        f"{len(cov)} frameworks. Implementation coverage ranges from "
        f"**{worst[1]['coverage_pct']}% ({worst[0]})** to "
        f"**{best[1]['coverage_pct']}% ({best[0]})**. Because the themes are shared, "
        f"the {len(not_impl)} not-yet-implemented themes "
        f"({', '.join(c['theme'] for c in not_impl)}) are the highest-leverage "
        f"remediation targets — each one closes a gap in every framework simultaneously.\n")

    L.append("## 2. Per-Framework Coverage\n")
    L.append("| Framework | Coverage | Implemented | Partial | Gap | Total mapped |")
    L.append("|---|---|---|---|---|---|")
    for fw, s in cov.items():
        L.append(f"| {fw} | {s['coverage_pct']}% | {s['implemented']} | {s['partial']} | {s['gap']} | {s['total']} |")
    L.append("")

    L.append("## 3. Full Crosswalk Matrix\n")
    fws = data["meta"]["frameworks"]
    L.append("| Control theme | Status | " + " | ".join(fws) + " |")
    L.append("|---|---|" + "|".join(["---"] * len(fws)) + "|")
    for c in controls:
        row = " | ".join(c["map"].get(fw, "—") for fw in fws)
        L.append(f"| {c['theme']} | {STATUS_LABEL[c['status']]} | {row} |")
    L.append("")

    L.append("## 4. Priority Gaps (multi-framework impact)\n")
    L.append("Themes not yet implemented, with the frameworks each one blocks:\n")
    for c in controls:
        if c["status"] == "not_implemented":
            fwlist = ", ".join(f"{fw} {c['map'][fw]}" for fw in fws if c["map"].get(fw))
            L.append(f"- **{c['theme']}** — closing this addresses: {fwlist}")
    L.append("")

    L.append("## 5. How to Use This Crosswalk\n")
    L.append(
        "1. Pick the framework you are certifying against (e.g. SOC 2 for a "
        "customer requirement).\n"
        "2. Read its coverage row — partial/gap themes are your audit findings.\n"
        "3. Prioritize the 'Not implemented' themes: each satisfies a requirement "
        "in *every* mapped framework, so the same remediation dollar counts "
        "multiple times toward your compliance obligations.\n")
    L.append("_Generated by `scripts/crosswalk.py` from `sample_data/control_crosswalk.json`._")
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="Multi-framework control crosswalk / mapping engine")
    parser.add_argument("--lookup", help="Control ID to find across all frameworks (e.g. 'A.8.8', 'AC-2', 'CC6.1')")
    parser.add_argument("--framework", help="Show the gap list for one framework")
    parser.add_argument("--report", help="Write the full crosswalk report to this path")
    args = parser.parse_args()

    data = load()

    if args.lookup:
        hits = lookup(data, args.lookup)
        if not hits:
            print(f"No control theme references '{args.lookup}'.")
        for c in hits:
            print(f"\nTheme: {c['theme']}  (status: {STATUS_LABEL[c['status']]})")
            for fw, ids in c["map"].items():
                print(f"  {fw:<14}{ids}")
        return

    if args.framework:
        fw = args.framework
        gaps = gaps_for_framework(data, fw)
        print(f"Open items for {fw} ({len(gaps)} theme(s) not fully implemented):\n")
        for c in gaps:
            print(f"  [{STATUS_LABEL[c['status']]:<15}] {c['theme']:<40} -> {c['map'].get(fw)}")
        return

    print_coverage(data)

    if args.report:
        Path(args.report).write_text(generate_report(data) + "\n")
        print(f"\n[+] Full crosswalk report written to {args.report}")


if __name__ == "__main__":
    main()
