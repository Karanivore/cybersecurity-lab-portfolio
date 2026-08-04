#!/usr/bin/env python3
"""
Cyber Risk Register & Quantitative Risk Assessment.

Two complementary views a consultant delivers to different audiences:

  1. Qualitative (for the risk committee): a 5x5 likelihood x impact
     register with inherent and residual risk ratings and a heat map.
  2. Quantitative (for the CFO/board): a FAIR-style Monte Carlo estimate
     of each risk's Annualized Loss Expectancy (ALE) — expressed as a
     distribution (mean, P50, P90) in dollars, so risk can be compared
     to the cost of controls.

Residual risk = inherent risk reduced by the assessed effectiveness of
existing controls. Monte Carlo uses triangular distributions for Threat
Event Frequency (events/year) and Loss Magnitude ($/event); pure stdlib.

Usage:
    python3 risk_analysis.py
    python3 risk_analysis.py --iterations 50000 --report ../risk_assessment_report.md
"""

import argparse
import json
import random
import statistics
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "sample_data" / "risk_register.json"

random.seed(2026)


def risk_level(score: float) -> str:
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Medium"
    return "Low"


def residual_scores(risk):
    inh = risk["inherent_likelihood"] * risk["inherent_impact"]
    eff = risk.get("control_effectiveness", 0.0)
    # Controls primarily reduce likelihood of a successful event.
    res_likelihood = max(1.0, risk["inherent_likelihood"] * (1 - eff))
    res = round(res_likelihood * risk["inherent_impact"], 1)
    return inh, res


def triangular(p):
    return random.triangular(p["tef_min"], p["tef_max"], p["tef_mode"])


def monte_carlo_ale(risk, iterations, control_effectiveness):
    fair = risk.get("fair")
    if not fair:
        return None
    losses = []
    for _ in range(iterations):
        tef = random.triangular(fair["tef_min"], fair["tef_max"], fair["tef_mode"])
        # Residual: controls reduce the frequency of loss events landing.
        tef_residual = tef * (1 - control_effectiveness)
        lm = random.triangular(fair["lm_min"], fair["lm_max"], fair["lm_mode"])
        losses.append(tef_residual * lm)
    losses.sort()
    n = len(losses)
    return {
        "mean_ale": statistics.mean(losses),
        "p50": losses[int(0.50 * n)],
        "p90": losses[int(0.90 * n)],
    }


def money(v):
    return f"${v:,.0f}"


def analyze(data, iterations):
    rows = []
    for r in data["risks"]:
        inh, res = residual_scores(r)
        ale = monte_carlo_ale(r, iterations, r.get("control_effectiveness", 0.0))
        rows.append({"risk": r, "inherent": inh, "residual": res,
                     "inherent_level": risk_level(inh), "residual_level": risk_level(res),
                     "ale": ale})
    rows.sort(key=lambda x: x["residual"], reverse=True)
    return rows


def print_console(data, rows):
    print(f"Cyber Risk Assessment — {data['engagement']['client']}  ({data['engagement']['date']})\n")
    print(f"{'ID':<6}{'RESID':<7}{'LEVEL':<10}{'MEAN ALE':<14}{'P90 ALE':<14}TITLE")
    print("-" * 100)
    for row in rows:
        r = row["risk"]
        ale = row["ale"]
        mean_ale = money(ale["mean_ale"]) if ale else "n/a"
        p90 = money(ale["p90"]) if ale else "n/a"
        print(f"{r['id']:<6}{row['residual']:<7}{row['residual_level']:<10}{mean_ale:<14}{p90:<14}{r['title'][:45]}")

    total_mean = sum(row["ale"]["mean_ale"] for row in rows if row["ale"])
    total_p90 = sum(row["ale"]["p90"] for row in rows if row["ale"])
    print("-" * 100)
    print(f"Portfolio residual Annualized Loss Expectancy — mean {money(total_mean)} | aggregated P90 {money(total_p90)}")


def generate_report(data, rows, iterations) -> str:
    eng = data["engagement"]
    total_mean = sum(row["ale"]["mean_ale"] for row in rows if row["ale"])
    crit_high = [row for row in rows if row["residual_level"] in ("Critical", "High")]

    L = []
    L.append("# Cyber Risk Assessment & Risk Register\n")
    L.append(f"**Client:** {eng['client']}  ")
    L.append(f"**Prepared by:** {eng['assessor']}  ")
    L.append(f"**Date:** {eng['date']}\n")
    L.append("---\n")

    L.append("## 1. Executive Summary\n")
    L.append(
        f"This assessment documents {len(rows)} enterprise cyber risks in a formal "
        f"register, rating each on a 5x5 likelihood-impact scale (inherent and "
        f"residual) and quantifying loss exposure via a {iterations:,}-iteration "
        f"Monte Carlo (FAIR-style) simulation. **{len(crit_high)} risks rate High or "
        f"Critical on a residual basis.** The estimated **portfolio residual "
        f"Annualized Loss Expectancy is approximately {money(total_mean)}**, "
        f"concentrated in ransomware (R-01) and customer-data exposure (R-02). "
        f"These figures let leadership compare risk exposure directly against the "
        f"cost of the controls proposed in the remediation roadmap.\n")

    L.append("## 2. Risk Register (residual-ranked)\n")
    L.append("| ID | Risk | Asset | Inherent | Residual | Residual level | Mean ALE | P90 ALE |")
    L.append("|---|---|---|---|---|---|---|---|")
    for row in rows:
        r = row["risk"]
        ale = row["ale"]
        L.append(f"| {r['id']} | {r['title']} | {r['asset']} | {row['inherent']} | {row['residual']} | "
                 f"{row['residual_level']} | {money(ale['mean_ale']) if ale else 'n/a'} | {money(ale['p90']) if ale else 'n/a'} |")
    L.append("")

    L.append("## 3. Qualitative Heat Map (residual)\n")
    L.append("```")
    L.append(_heatmap(rows))
    L.append("```\n")

    L.append("## 4. Risk Detail & Treatment\n")
    for row in rows:
        r = row["risk"]
        ale = row["ale"]
        L.append(f"### {r['id']} — {r['title']}\n")
        L.append(f"- **Threat / vulnerability:** {r['threat']} exploiting {r['vulnerability']}")
        L.append(f"- **NIST CSF categories:** {', '.join(r.get('nist_csf', []))}")
        L.append(f"- **Inherent risk:** {row['inherent']} ({row['inherent_level']}) → **Residual:** {row['residual']} ({row['residual_level']})")
        L.append(f"- **Existing controls:** {', '.join(r['existing_controls'])} (assessed effectiveness {int(r.get('control_effectiveness',0)*100)}%)")
        if ale:
            L.append(f"- **Quantified exposure:** mean ALE {money(ale['mean_ale'])}, P50 {money(ale['p50'])}, P90 {money(ale['p90'])}")
        L.append(f"- **Recommended treatment:** {_treatment(row)}\n")

    L.append("## 5. Methodology\n")
    L.append(
        "Inherent risk = likelihood x impact on a 5x5 scale. Residual risk applies "
        "assessed control effectiveness as a reduction to event likelihood. "
        "Quantitative exposure follows a FAIR-style model: Threat Event Frequency "
        "(events/year) and Loss Magnitude ($/event) are each sampled from triangular "
        f"distributions (min/most-likely/max) over {iterations:,} iterations; residual "
        "ALE applies the same control-effectiveness reduction to frequency. Aggregate "
        "portfolio figures are the sum of per-risk means (mean) — an approximation, as "
        "risks are treated as independent.\n")
    L.append("_Generated by `scripts/risk_analysis.py` from `sample_data/risk_register.json`._")
    return "\n".join(L)


def _heatmap(rows):
    grid = {(likelihood, impact): [] for likelihood in range(1, 6) for impact in range(1, 6)}
    for row in rows:
        r = row["risk"]
        eff = r.get("control_effectiveness", 0.0)
        res_l = max(1, round(r["inherent_likelihood"] * (1 - eff)))
        grid[(res_l, r["inherent_impact"])].append(r["id"])
    out = []
    out.append("Likelihood")
    for likelihood in range(5, 0, -1):
        cells = []
        for impact in range(1, 6):
            ids = ",".join(grid[(likelihood, impact)])
            cells.append(f"{ids:^9}")
        out.append(f"  {likelihood} |" + "|".join(cells) + "|")
    out.append("    +" + "+".join(["---------"] * 5) + "+")
    out.append("     " + "".join(f"{i:^10}" for i in range(1, 6)) + "  Impact")
    return "\n".join(out)


def _treatment(row):
    level = row["residual_level"]
    if level in ("Critical", "High"):
        return "Mitigate — prioritize control uplift this quarter; track to closure on the risk committee agenda."
    if level == "Medium":
        return "Mitigate or transfer — schedule control improvement and evaluate cyber-insurance coverage."
    return "Accept with monitoring — document acceptance and review at next assessment cycle."


def main():
    parser = argparse.ArgumentParser(description="Cyber risk register + FAIR-style Monte Carlo quantification")
    parser.add_argument("--iterations", type=int, default=20000)
    parser.add_argument("--report", help="Write full Markdown report to this path")
    args = parser.parse_args()

    data = json.loads(DATA.read_text())
    rows = analyze(data, args.iterations)
    print_console(data, rows)

    if args.report:
        Path(args.report).write_text(generate_report(data, rows, args.iterations) + "\n")
        print(f"\n[+] Full risk assessment report written to {args.report}")


if __name__ == "__main__":
    main()
