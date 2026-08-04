# Lab 16 — Zero Trust Maturity Assessment (CISA ZTMM 2.0)

*Consultant / GRC track — Cyber Transformation focus.*

Zero Trust is a flagship cyber-transformation offering at every major
consultancy. This lab scores an organization against the **CISA Zero
Trust Maturity Model 2.0** — five pillars plus three cross-cutting
capabilities, across four maturity stages — and produces a
current-vs-target gap analysis and a phased, dependency-aware Zero Trust
roadmap.

## The model

- **Pillars:** Identity · Devices · Networks · Applications & Workloads · Data
- **Cross-cutting:** Visibility & Analytics · Automation & Orchestration · Governance
- **Stages:** Traditional (0) → Initial (1) → Advanced (2) → Optimal (3)

## Contents

| File | Purpose |
|---|---|
| `sample_data/ztmm_assessment.json` | Current/target stage per pillar and cross-cutting capability, with observations that reference the other labs |
| `scripts/zt_maturity.py` | Scores each pillar, computes overall maturity + gaps, and generates the roadmap report |
| `zero_trust_roadmap.md` | The generated deliverable: executive summary, stage definitions, pillar results, phased roadmap, methodology |

## Usage

```bash
python3 scripts/zt_maturity.py
python3 scripts/zt_maturity.py --report zero_trust_roadmap.md
```

## Sample output

```
PILLAR / CAPABILITY         TYPE           CURRENT     TARGET      GAP  HEAT
------------------------------------------------------------------------------------
Identity                    pillar         Advanced    Optimal     1    ████████····
Devices                     pillar         Initial     Optimal     2    ████········
Networks                    pillar         Initial     Optimal     2    ████········
Data                        pillar         Initial     Optimal     2    ████········
...
OVERALL                                    Initial (1.38) Optimal (2.88) 1.5  ██████······
```

The roadmap is sequenced by gap size **and architectural dependency** —
identity and device trust are foundational and gate the network,
application, and data controls that follow — which is the judgment that
separates a real Zero Trust plan from a checklist.

## Skills demonstrated

- CISA Zero Trust Maturity Model 2.0 (5 pillars + 3 cross-cutting capabilities, 4 stages)
- Current-vs-target maturity scoring and gap analysis
- Dependency-aware transformation roadmapping (identity/device trust before network/data enforcement)
- Connecting a strategic ZT target state to concrete pillar initiatives

## Resume bullet points

- *Assessed Zero Trust maturity against the CISA ZTMM 2.0 model across five pillars and three cross-cutting capabilities, quantifying a 1.5-stage gap from Initial to a target Optimal posture.*
- *Produced a dependency-aware, phased Zero Trust roadmap sequencing identity and device trust ahead of network-, application-, and data-layer enforcement.*
- *Linked each maturity gap to a concrete initiative (phishing-resistant MFA, device-compliance-based access, micro-segmentation, automated data classification, SOAR).*
