# Cybersecurity Portfolio Labs

This repository contains hands-on cybersecurity labs covering security automation, SOC analysis, vulnerability assessment, incident response, network hardening, cloud security, and governance, risk, and compliance.

Each lab includes documentation, sample data, and either runnable scripts or a written assessment deliverable. All sample organizations, users, systems, findings, and business data are fictional.

**Start with [`index.html`](./index.html)** for a visual overview of all 16 labs. The landing page can be opened locally or hosted through GitHub Pages.

The portfolio is organized into two tracks:

- **Consultant / GRC track (07–16):** risk assessments, compliance mapping, policy development, audit readiness, privacy, third-party risk, regulatory analysis, and security transformation.
- **Technical / Analyst track (01–06):** Python security automation, SOC log analysis, vulnerability assessment, incident response, network defense, and cloud security.

Most scripts use the Python 3.11 standard library. One optional feature uses `requests`, Lab 03 uses Docker, and Lab 05 includes `nftables` and Suricata configuration examples. No paid tools or live cloud accounts are required.

---

## Consultant / GRC Track

| # | Lab | Deliverable | Frameworks |
|---|---|---|---|
| [07](./07-nist-csf-maturity-assessment) | **NIST CSF 2.0 Maturity Assessment** | Maturity report, gap analysis, and remediation roadmap | NIST CSF 2.0 |
| [08](./08-cyber-risk-register) | **Cyber Risk Register and Quantification** | Risk register and FAIR-style Monte Carlo ALE report | 5×5 risk model, FAIR |
| [09](./09-compliance-crosswalk) | **Compliance Framework Crosswalk** | Multi-framework coverage report, gap analysis, and control lookup | NIST CSF, NIST 800-53, ISO 27001, CIS Controls v8, SOC 2 |
| [10](./10-vendor-risk-assessment) | **Third-Party Risk Assessment** | Vendor tiering report and remediation requirements | TPRM, SIG-lite |
| [11](./11-soc2-iso27001-readiness) | **SOC 2 and ISO 27001 Readiness Assessment** | Readiness score and phased remediation roadmap | SOC 2 TSC, ISO 27001:2022 |
| [12](./12-security-policy-suite) | **ISMS Security Policy Suite** | Five security policies and an Annex A coverage checker | ISO 27001:2022 |
| [13](./13-itgc-sox-controls-testing) | **ITGC and SOX Controls Testing** | IT audit workpaper covering sampling, exceptions, and deficiency evaluation | SOX 404, SOC 1, SOC 2, ITGC |
| [14](./14-privacy-gdpr-assessment) | **Privacy and Data Protection Assessment** | Privacy assessment covering DPIA, lawful basis, transfers, and DSAR processes | GDPR, CCPA/CPRA |
| [15](./15-fs-regulatory-compliance) | **Financial Services Regulatory Compliance** | DORA and NYDFS Part 500 gap assessment | DORA, NYDFS Part 500 |
| [16](./16-zero-trust-maturity) | **Zero Trust Maturity Assessment** | Current-state assessment, target-state scoring, and phased roadmap | CISA ZTMM 2.0 |

These labs focus on practical governance and technology-risk activities, including control assessment, risk documentation, policy development, audit testing, regulatory analysis, and remediation planning.

## Technical / Analyst Track

| # | Lab | Core Skill Area |
|---|---|---|
| [01](./01-python-security-toolkit) | **Python Security Automation Toolkit** | Network reconnaissance, password auditing, and hash analysis |
| [02](./02-soc-log-analysis-siem) | **SOC Log Analysis and SIEM Detection Engine** | Log correlation, detection engineering, and MITRE ATT&CK mapping |
| [03](./03-vulnerability-assessment-lab) | **Vulnerability Assessment Lab** | OWASP Top 10, custom scanning, and CVSS scoring |
| [04](./04-incident-response-playbook) | **Incident Response and Timeline Reconstruction** | Evidence correlation, incident documentation, and NIST SP 800-61 concepts |
| [05](./05-network-hardening-ids) | **Network Hardening and IDS** | Network segmentation, firewall configuration, and Suricata rules |
| [06](./06-cloud-security-audit) | **AWS Security Audit Tool** | IAM review, S3 posture analysis, and CIS AWS Benchmark checks |

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Karanivore/cybersecurity-lab-portfolio.git
cd cybersecurity-lab-portfolio
```

Generate a NIST CSF maturity assessment:

```bash
python3 07-nist-csf-maturity-assessment/scripts/csf_maturity.py
```

Generate an ITGC and SOX controls-testing workpaper:

```bash
python3 13-itgc-sox-controls-testing/scripts/itgc_test.py
```

Generate a quantified cyber risk register:

```bash
python3 08-cyber-risk-register/scripts/risk_analysis.py
```

Run the SOC detection engine:

```bash
python3 02-soc-log-analysis-siem/scripts/detection_engine.py
```

Each lab folder contains its own `README.md` with setup instructions, usage examples, sample output, technical notes, and key outcomes.

## How the Labs Connect

The two tracks are designed to show both technical and governance perspectives.

The technical labs generate findings such as suspicious authentication activity, software vulnerabilities, insecure cloud configurations, weak network controls, and incident evidence.

The GRC labs use similar findings as inputs for risk registers, maturity assessments, control testing, vendor reviews, compliance mapping, policy development, and remediation planning.

Together, the labs cover several parts of the security lifecycle:

- **Govern:** NIST CSF maturity, security policy, and Zero Trust planning
- **Assess:** risk analysis, vulnerability assessment, cloud review, privacy assessment, and regulatory gap analysis
- **Protect:** network hardening, firewall rules, identity controls, and security policies
- **Detect:** SOC log analysis, detection rules, and security automation
- **Respond:** incident-response planning, evidence review, and timeline reconstruction
- **Assure:** ITGC testing, compliance mapping, and audit-readiness assessment

## Financial Services and Technology-Risk Relevance

Several labs address security and control areas commonly encountered in financial-services and enterprise technology environments:

| Area | Relevant Labs |
|---|---|
| Cybersecurity governance and maturity | 07, 12, 16 |
| Cyber risk identification and quantification | 08 |
| Compliance and control mapping | 09, 11 |
| Third-party and vendor risk | 10 |
| IT general controls and audit testing | 13 |
| Privacy and data protection | 14 |
| Financial-services regulation | 15 |
| SOC monitoring and detection | 02 |
| Incident response | 04 |
| Cloud and infrastructure security | 05, 06 |
| Application and vulnerability assessment | 03 |
| Security automation | 01 |

## Ethical Use

All scanning, password auditing, hash analysis, exploitation, and security-testing tools in this repository are intended only for:

- Systems you own
- Systems you are explicitly authorized to test
- Local laboratory environments
- Purpose-built vulnerable applications
- Fictional datasets included in the repository

Do not run these tools against third-party systems, networks, accounts, or data without written authorization.

All client names, organizations, users, findings, and business scenarios included in the GRC labs are fictional and are provided only for educational and portfolio purposes.
