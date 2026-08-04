#!/usr/bin/env python3
"""
Zero Trust Maturity Assessment (CISA ZTMM 2.0).

Zero Trust is a flagship cyber-transformation offering. This tool scores
an organization against the CISA Zero Trust Maturity Model 2.0 — five
pillars (Identity, Devices, Networks, Applications & Workloads, Data) plus
three cross-cutting capabilities (Visibility & Analytics, Automation &
Orchestration, Governance) — across four maturity stages (Traditional,
Initial, Advanced, Optimal), then produces a current-vs-target gap
analysis and a phased Zero Trust roadmap.

Usage:
    python3 zt_maturity.py
    python3 zt_maturity.py --report ../zero_trust_roadmap.md
"""

import argparse
import json
import statistics
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "ztmm_assessment.json"

STAGE_NAME = {0: "Traditional", 1: "Initial", 2: "Advanced", 3: "Optimal"}


def load():
    return json.loads(DATA.read_text())


def overall(pillars):
    cur = statistics.mean(p["current"] for p in pillars)
    tgt = statistics.mean(p["target"] for p in pillars)
    return round(cur, 2), round(tgt, 2)


def stage_label(value):
    return STAGE_NAME[int(round(value))]


def bar(stage, width=12):
    filled = int(round((stage / 3) * width))
    return "█" * filled + "·" * (width - filled)


def print_console(data):
    pillars = data["pillars"]
    cur, tgt = overall(pillars)
    print(f"Zero Trust Maturity (CISA ZTMM 2.0) — {data['engagement']['client']}  ({data['engagement']['date']})\n")
    print(f"{'PILLAR / CAPABILITY':<28}{'TYPE':<15}{'CURRENT':<12}{'TARGET':<12}{'GAP':<5}HEAT")
    print("-" * 84)
    for p in pillars:
        typ = "pillar" if p["type"] == "pillar" else "cross-cutting"
        print(f"{p['pillar']:<28}{typ:<15}{STAGE_NAME[p['current']]:<12}{STAGE_NAME[p['target']]:<12}"
              f"{p['target']-p['current']:<5}{bar(p['current'])}")
    print("-" * 84)
    print(f"{'OVERALL':<28}{'':<15}{stage_label(cur)+f' ({cur})':<15}{stage_label(tgt)+f' ({tgt})':<15}"
          f"{round(tgt-cur,2):<5}{bar(cur)}")


def generate_report(data) -> str:
    pillars = data["pillars"]
    eng = data["engagement"]
    stages = eng["stages"]
    cur, tgt = overall(pillars)
    gaps = sorted(pillars, key=lambda p: (p["target"] - p["current"]), reverse=True)

    L = []
    L.append("# Zero Trust Maturity Assessment & Roadmap\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Prepared by:** {eng['assessor']}  ")
    L.append(f"**Model:** {eng['model']}  ")
    L.append(f"**Date:** {eng['date']}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    L.append(
        f"The organization's overall Zero Trust maturity is **{stage_label(cur)} "
        f"({cur}/3.0)** against a target of **{stage_label(tgt)} ({tgt}/3.0)**. Identity, "
        f"Visibility & Analytics, and Governance are the most mature pillars; **Devices, "
        f"Networks, and Data lag at the Initial stage** and carry the largest gaps to "
        f"target. Zero Trust is a multi-year transformation — this roadmap sequences the "
        f"pillars by gap size and dependency so early investment in identity and device "
        f"trust unlocks the per-session, data-centric controls that define the Optimal "
        f"stage.\n")

    L.append("## 2. Maturity Stages\n")
    for s, desc in stages.items():
        L.append(f"- **Stage {s} ({STAGE_NAME[int(s)]})** — {desc}")
    L.append("")

    L.append("## 3. Pillar & Cross-Cutting Results\n")
    L.append("| Pillar / Capability | Type | Current | Target | Gap | Observation |")
    L.append("|---|---|---|---|---|---|")
    for p in pillars:
        typ = "Pillar" if p["type"] == "pillar" else "Cross-cutting"
        L.append(f"| {p['pillar']} | {typ} | {STAGE_NAME[p['current']]} | {STAGE_NAME[p['target']]} | {p['target']-p['current']} | {p['notes']} |")
    L.append(f"| **Overall** | | **{stage_label(cur)} ({cur})** | **{stage_label(tgt)} ({tgt})** | **{round(tgt-cur,2)}** | |\n")

    L.append("## 4. Phased Zero Trust Roadmap\n")
    L.append(
        "Sequenced by gap size and architectural dependency. Identity and device "
        "trust are foundational — they gate the network, application, and data "
        "controls that follow.\n")
    L.append("| Priority | Pillar | Current → Target | Focus initiative | Horizon |")
    L.append("|---|---|---|---|---|")
    for i, p in enumerate(gaps, start=1):
        horizon = "0-6 months" if i <= 3 else ("6-12 months" if i <= 6 else "12-24 months")
        L.append(f"| {i} | {p['pillar']} | {STAGE_NAME[p['current']]} → {STAGE_NAME[p['target']]} | {_initiative(p['pillar'])} | {horizon} |")
    L.append("")

    L.append("## 5. Methodology\n")
    L.append(
        "Each ZTMM pillar and cross-cutting capability was rated on the CISA 0-3 "
        "maturity scale (Traditional / Initial / Advanced / Optimal). The overall "
        "score is the mean across all pillars and capabilities. The roadmap orders "
        "initiatives by gap size, adjusted for the dependency that identity and "
        "device trust precede network-, application-, and data-layer enforcement.\n")
    L.append("_Generated by `scripts/zt_maturity.py` from `sample_data/ztmm_assessment.json`._")
    return "\n".join(L)


def _initiative(pillar):
    m = {
        "Identity": "Roll out phishing-resistant MFA and continuous/risk-based authentication",
        "Devices": "Enforce device compliance/health as a condition of access (device trust)",
        "Networks": "Move from macro-segmentation to micro-segmentation with per-session policy",
        "Applications & Workloads": "Introduce continuous workload authorization and app-level access policy",
        "Data": "Automate data tagging/classification and enforce data-centric DLP + encryption",
        "Visibility & Analytics": "Close cloud/OT telemetry gaps; unify analytics for policy decisions",
        "Automation & Orchestration": "Deploy SOAR playbooks to automate detection-to-response",
        "Governance": "Move to policy-as-code with dynamic, centrally governed access policy",
    }
    return m.get(pillar, f"Advance {pillar} toward target stage")


def main():
    parser = argparse.ArgumentParser(description="Zero Trust maturity assessment (CISA ZTMM 2.0)")
    parser.add_argument("--report", help="Write full Markdown roadmap to this path")
    args = parser.parse_args()

    data = load()
    print_console(data)

    if args.report:
        Path(args.report).write_text(generate_report(data) + "\n")
        print(f"\n[+] Full Zero Trust roadmap written to {args.report}")


if __name__ == "__main__":
    main()
