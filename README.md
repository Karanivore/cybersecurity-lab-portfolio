# Cybersecurity Portfolio Labs

A portfolio of hands on cybersecurity labs  each with **working code you
can run**, realistic data, and a **client ready written deliverable**
(assessment, report, roadmap, or policy) in the exact format employers
and consulting clients expect.

**Start with [`index.html`](./index.html)** — a visual landing page
indexing all 16 labs by track (open it locally, or host it free via
GitHub Pages: *Settings → Pages → Deploy from branch → root*).

The labs are organized into two tracks:

- **Consultant / GRC track (07–16)** — risk, compliance, and advisory
  work: the frameworks, assessments, and deliverables a **cybersecurity
  consultant** produces. *Start here if you're targeting advisory/GRC
  roles.*
- **Technical / Analyst track (01–06)** — offensive and defensive
  hands on labs (SOC, pentest, IR, cloud) that give the consultant track
  its technical credibility.

Every script runs on Python 3.11's standard library alone (one optional
feature uses `requests`; Lab 03 uses Docker; Lab 05 uses `nft`/Suricata
syntax). Nothing requires paid tools or a live cloud account.

---

## Consultant / GRC track

| # | Lab | Deliverable | Frameworks |
|---|---|---|---|
| [07](./07-nist-csf-maturity-assessment) | **NIST CSF 2.0 Maturity Assessment** | Maturity report + gap analysis + remediation roadmap | NIST CSF 2.0 |
| [08](./08-cyber-risk-register) | **Cyber Risk Register & Quantification** | Risk register + FAIR-style Monte Carlo ALE report | 5×5 risk model, FAIR |
| [09](./09-compliance-crosswalk) | **Compliance Framework Crosswalk** | Multi-framework coverage/gap report + control lookup | CSF, 800-53, ISO 27001, CIS v8, SOC 2 |
| [10](./10-vendor-risk-assessment) | **Third-Party / Vendor Risk Assessment** | Vendor tiering report + remediation asks | TPRM, SIG-lite |
| [11](./11-soc2-iso27001-readiness) | **SOC 2 / ISO 27001 Readiness Assessment** | Readiness score + phased remediation roadmap | SOC 2 TSC, ISO 27001:2022 |
| [12](./12-security-policy-suite) | **ISMS Security Policy Suite** | 5 policies + Annex A coverage checker | ISO 27001:2022 |
| [13](./13-itgc-sox-controls-testing) | **ITGC / SOX Controls Testing** | IT-audit workpaper: sampling, exceptions, deficiency evaluation | SOX 404, SOC 1/SOC 2, ITGC |
| [14](./14-privacy-gdpr-assessment) | **Privacy & Data Protection Assessment** | GDPR/CCPA assessment: DPIA, lawful basis, transfers, DSAR | GDPR, CCPA/CPRA |
| [15](./15-fs-regulatory-compliance) | **FS Regulatory Compliance** | DORA + NYDFS 500 gap assessment by regulation & pillar | DORA, NYDFS Part 500 |
| [16](./16-zero-trust-maturity) | **Zero Trust Maturity Assessment** | ZTMM current-vs-target + phased Zero Trust roadmap | CISA ZTMM 2.0 |

**Why this track for a consultant résumé:** advisory work is judged on
framework fluency, risk quantification, compliance mapping, and clear
written deliverables — not on running exploits. These ten labs produce the
actual artifacts of a consulting engagement (maturity assessment,
quantified risk register, control crosswalk, vendor assessment, audit
readiness, policy suite, ITGC/SOX controls testing, privacy assessment,
regulatory gap analysis, and a Zero Trust roadmap), and the sample data
deliberately cross-references the technical labs so findings roll up into
board-level risk language.

## Technical / Analyst track

| # | Lab | Core skill area |
|---|---|---|
| [01](./01-python-security-toolkit) | Python Security Automation Toolkit | Network recon, password auditing, hash analysis |
| [02](./02-soc-log-analysis-siem) | SOC Log Analysis & SIEM Detection Engine | Log correlation, detection engineering, MITRE ATT&CK |
| [03](./03-vulnerability-assessment-lab) | Vulnerability Assessment Lab | OWASP Top 10, custom scanning, CVSS scoring |
| [04](./04-incident-response-playbook) | Incident Response & Timeline Reconstruction | NIST SP 800-61 IR, evidence correlation |
| [05](./05-network-hardening-ids) | Network Hardening & IDS | Segmentation, firewall-as-code, Suricata rules |
| [06](./06-cloud-security-audit) | Cloud (AWS) Security Audit Tool | CIS AWS Benchmark, IAM/S3 posture auditing |

---

## Quick start

```bash
git clone <this-repo>
cd Cybersecurity

# Consultant track — generate a NIST CSF maturity assessment:
python3 07-nist-csf-maturity-assessment/scripts/csf_maturity.py

# ...an ITGC/SOX controls-testing workpaper (Big Four IT-audit):
python3 13-itgc-sox-controls-testing/scripts/itgc_test.py

# ...or a quantified cyber risk register:
python3 08-cyber-risk-register/scripts/risk_analysis.py

# Technical track — run the SIEM detection engine:
python3 02-soc-log-analysis-siem/scripts/detection_engine.py
```

Each lab folder has its own `README.md` with usage, sample output, skills
demonstrated, and **ready-to-paste résumé bullet points**.

## How the two tracks fit a consultant résumé

A strong consulting candidate shows **advisory depth** *and* the
**technical credibility** to back the advice. The consultant track (07–16)
demonstrates you can run an engagement end to end; the technical track
(01–06) demonstrates you understand what you're advising on. Together they
cover the security lifecycle — **govern** (07, 12), **assess** (08–11, 14,
15, 03, 06), **assure** (13), **transform** (16), **detect** (01, 02),
**protect** (05), and **respond** (04) — which is a far stronger signal
than several projects in one narrow niche.

## Alignment to Big Four cyber & technology-risk service lines

The consultant track maps directly onto how a Big Four advisory practice
(e.g. KPMG) structures its cyber and technology-risk work:

| Service line (typical) | Relevant labs |
|---|---|
| **Cyber strategy & transformation** (maturity, target operating model, Zero Trust, roadmaps) | 07 (CSF maturity), 08 (risk quantification), 16 (Zero Trust) |
| **Governance, risk & compliance** (framework alignment, policy, regulatory readiness) | 09 (crosswalk), 11 (SOC 2 / ISO 27001), 12 (ISMS policy) |
| **Technology risk & controls assurance** (SOX ITGC, SOC 1/SOC 2 attestation, IT audit) | 13 (ITGC/SOX testing), 11 (readiness) |
| **Privacy & data protection** (GDPR/CCPA, DPIA, data governance) | 14 (privacy assessment) |
| **Financial-services regulatory** (DORA, NYDFS, resilience) | 15 (FS regulatory) |
| **Third-party / supply-chain risk** | 10 (vendor risk) |
| **Cyber defense & managed services** (SOC, detection, IR, cloud) | 01, 02, 04, 06 |
| **Application & infrastructure security testing** | 03 (web app / OWASP), 05 (network/IDS) |

Interviewing for a Big Four technology-risk or cyber role, the
highest-signal labs are **13 (ITGC/SOX controls testing)** — because
IT-audit and SOC attestation are core to a licensed audit firm —
**07/08/16 (maturity, risk quantification, Zero Trust)** for cyber
transformation advisory, and **14/15 (privacy, FS regulatory)** which
match KPMG's large privacy and financial-services regulatory practices.
Each is a talking point you can walk an interviewer through end to end.

## Ethical use

All scanning, cracking, and exploitation tooling here is for systems you
own or are explicitly authorized to test — the Docker target in Lab 03,
your own local host, or a sanctioned lab. All "client" data in the
consultant track is illustrative and fictional. None of this code should
be pointed at third-party systems without written authorization.
