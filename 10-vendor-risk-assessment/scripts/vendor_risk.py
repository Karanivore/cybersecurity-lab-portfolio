#!/usr/bin/env python3
"""
Third-Party / Vendor Risk Assessment Engine.

Scores vendors on two independent axes — the standard TPRM model:

  * Inherent risk  — how much damage this vendor *could* cause, driven by
    the data types they touch, their access level, and business
    criticality (independent of how good their security is).
  * Control maturity — how well they answered the security questionnaire,
    weighted by question importance.

Combining the two yields a residual risk tier and a recommended action
(approve / approve-with-conditions / remediate / reject), plus a
per-vendor list of the specific weak controls to push back on.

Usage:
    python3 vendor_risk.py
    python3 vendor_risk.py --report ../vendor_risk_report.md
"""

import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "sample_data"

DATA_TYPE_RISK = {"PHI": 3, "PII": 2, "financial": 2, "confidential": 1}
ACCESS_RISK = {"privileged_access": 3, "data_processor": 2, "network_access": 2, "read_only": 1, "no_access": 0}
CRITICALITY_RISK = {"high": 3, "medium": 2, "low": 1}


def load():
    q = json.loads((BASE / "questionnaire.json").read_text())
    vendors = json.loads((BASE / "vendor_responses.json").read_text())
    return q, vendors


def inherent_tier(inh):
    data_score = max((DATA_TYPE_RISK.get(d, 0) for d in inh.get("data_types", [])), default=0)
    access_score = ACCESS_RISK.get(inh.get("access_level", "no_access"), 0)
    crit_score = CRITICALITY_RISK.get(inh.get("business_criticality", "low"), 1)
    total = data_score + access_score + crit_score
    if total >= 7:
        return "Critical", total
    if total >= 5:
        return "High", total
    if total >= 3:
        return "Medium", total
    return "Low", total


def control_maturity(q, responses):
    scores = q["meta"]["response_scores"]
    earned = 0.0
    possible = 0.0
    weak = []
    for question in q["questions"]:
        resp = responses.get(question["id"], "no")
        val = scores.get(resp)
        if val is None:  # n/a — excluded from scoring
            continue
        w = question["weight"]
        possible += w
        earned += w * val
        if val < 1.0:
            weak.append({"id": question["id"], "domain": question["domain"], "text": question["text"], "response": resp})
    pct = round(100 * earned / possible, 1) if possible else 0.0
    return pct, weak


def residual_tier(inherent_label, maturity_pct):
    # Residual risk is inherent risk REDUCED by control strength — controls
    # can lower exposure but never raise it above what the vendor could
    # actually harm. A vendor with no data access stays Low no matter how
    # weak their security posture.
    inherent_rank = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}[inherent_label]
    if maturity_pct >= 85:
        reduction = 2
    elif maturity_pct >= 65:
        reduction = 1
    else:
        reduction = 0
    residual_rank = max(1, inherent_rank - reduction)  # floor Low, cap at inherent
    return {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}[residual_rank]


def recommendation(residual, maturity_pct):
    if residual == "Low":
        return "Approve"
    if residual == "Medium":
        return "Approve with conditions (remediation plan + annual reassessment)"
    if residual == "High":
        return "Remediate before onboarding (require fixes to critical-weight gaps)"
    return "Do not onboard / reject pending major security uplift"


def assess(q, vendors):
    rows = []
    for v in vendors:
        inh_label, inh_score = inherent_tier(v["inherent"])
        maturity, weak = control_maturity(q, v["responses"])
        residual = residual_tier(inh_label, maturity)
        rows.append({
            "vendor": v["vendor"], "service": v["service"],
            "inherent": inh_label, "inherent_score": inh_score,
            "maturity": maturity, "residual": residual,
            "recommendation": recommendation(residual, maturity), "weak": weak,
        })
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    rows.sort(key=lambda r: (order[r["residual"]], -r["inherent_score"]))
    return rows


def print_console(rows):
    print(f"{'VENDOR':<32}{'INHERENT':<10}{'CTRL%':<8}{'RESIDUAL':<10}RECOMMENDATION")
    print("-" * 100)
    for r in rows:
        print(f"{r['vendor']:<32}{r['inherent']:<10}{str(r['maturity']):<8}{r['residual']:<10}{r['recommendation']}")


def generate_report(rows) -> str:
    L = []
    L.append("# Third-Party Vendor Risk Assessment\n")
    L.append("**Prepared by:** GRC Advisory Practice  ")
    L.append("**Scope:** 5 vendors assessed via SIG-lite security questionnaire\n")
    L.append("---\n")

    crit_high = [r for r in rows if r["residual"] in ("Critical", "High")]
    L.append("## 1. Executive Summary\n")
    L.append(
        f"Five third parties were assessed on inherent risk (data sensitivity, "
        f"access level, business criticality) and control maturity (weighted "
        f"security questionnaire). **{len(crit_high)} vendor(s) rate High or "
        f"Critical residual risk** and should not be onboarded or renewed without "
        f"remediation. The highest-risk relationship is "
        f"**{rows[0]['vendor']}** — {rows[0]['residual']} residual risk driven by "
        f"{rows[0]['inherent'].lower()} inherent exposure combined with a "
        f"{rows[0]['maturity']}% control maturity score.\n")

    L.append("## 2. Vendor Risk Summary\n")
    L.append("| Vendor | Service | Inherent | Control maturity | Residual | Recommendation |")
    L.append("|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['vendor']} | {r['service']} | {r['inherent']} | {r['maturity']}% | {r['residual']} | {r['recommendation']} |")
    L.append("")

    L.append("## 3. Detailed Findings & Remediation Asks\n")
    for r in rows:
        L.append(f"### {r['vendor']} — Residual risk: {r['residual']}\n")
        L.append(f"- **Service / exposure:** {r['service']}")
        L.append(f"- **Inherent risk:** {r['inherent']} | **Control maturity:** {r['maturity']}%")
        L.append(f"- **Recommendation:** {r['recommendation']}")
        if r["weak"]:
            L.append(f"- **Controls to remediate ({len(r['weak'])}):**")
            for w in r["weak"]:
                L.append(f"    - [{w['domain']}] {w['text']} (answered: *{w['response']}*)")
        else:
            L.append("- **Controls to remediate:** none — all questionnaire items fully satisfied")
        L.append("")

    L.append("## 4. Methodology\n")
    L.append(
        "Inherent risk combines the most sensitive data type handled, the vendor's "
        "access level, and business criticality into a Low/Medium/High/Critical tier. "
        "Control maturity is the weighted percentage of security-questionnaire items "
        "satisfied (partial = half credit; N/A items excluded). Residual risk elevates "
        "inherent risk when control maturity is weak. Recommendations follow a standard "
        "approve / approve-with-conditions / remediate / reject decision model.\n")
    L.append("_Generated by `scripts/vendor_risk.py` from the questionnaire and vendor responses._")
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="Third-party vendor risk assessment engine")
    parser.add_argument("--report", help="Write full Markdown report to this path")
    args = parser.parse_args()

    q, vendors = load()
    rows = assess(q, vendors)
    print_console(rows)

    if args.report:
        Path(args.report).write_text(generate_report(rows) + "\n")
        print(f"\n[+] Full vendor risk report written to {args.report}")


if __name__ == "__main__":
    main()
