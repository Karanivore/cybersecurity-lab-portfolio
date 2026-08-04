# Lab 5 — Network Hardening & Intrusion Detection

Infrastructure-as-code for a segmented, default-deny network plus custom
network-layer IDS signatures — the network-security counterpart to Lab
2's host/application-layer SIEM detections. Same attack chain (brute
force, port scan, SQLi, directory traversal, lateral movement), detected
and blocked at a different layer of the stack.

## Contents

| File | Purpose |
|---|---|
| `network_segmentation_diagram.md` | Mermaid network diagram + design rationale: DMZ / Internal / Management / Security VLANs, zero-trust-leaning zone boundaries |
| `firewall/harden_firewall.nft` | nftables ruleset implementing default-deny inbound/forward chains, per-VLAN allow-lists, and drop logging — **syntax-validated** with `nft -c` |
| `ids/suricata_custom.rules` | 9 custom Suricata signatures (SSH brute force, port scan, SQLi, directory traversal, SMB lateral movement, known-C2 DNS query), each mapped to a MITRE ATT&CK technique |
| `scripts/validate_suricata_rules.py` | Structural rule-file validator (required options, duplicate-SID detection, header grammar) — **all 9 rules pass** |

## Usage

```bash
# Syntax-check the firewall ruleset (no changes applied)
nft -c -f firewall/harden_firewall.nft

# Apply it (requires root / a real interface layout — adjust interface
# and subnet names first)
sudo nft -f firewall/harden_firewall.nft

# Validate the IDS rule file structure
python3 scripts/validate_suricata_rules.py ids/suricata_custom.rules

# Load into a real Suricata sensor
suricata -T -c /etc/suricata/suricata.yaml -S ids/suricata_custom.rules
```

## Sample output

```
$ nft -c -f firewall/harden_firewall.nft
$ echo $?
0

$ python3 scripts/validate_suricata_rules.py ids/suricata_custom.rules
[*] Parsed 9 rule(s) from ids/suricata_custom.rules
  sid:1000001  [alert/tcp] LAB SSH Brute Force - Repeated Connection Attempts
  ...
[+] All rules structurally valid (header + required options present, no duplicate SIDs)
```

## Skills demonstrated

- Network segmentation design (DMZ / internal / management / security zones) and diagramming
- nftables firewall-as-code: default-deny chains, sets, zone-based allow-lists, structured logging for SIEM ingestion
- Suricata IDS signature authoring across TCP, HTTP, SMB, and DNS protocol keywords
- MITRE ATT&CK technique mapping at the network-detection layer
- Building a custom validation tool to enforce rule-authoring standards

## Resume bullet points

- *Designed a zero-trust-leaning network segmentation scheme (DMZ/Internal/Management/Security VLANs) and implemented it as a syntax-validated nftables default-deny ruleset.*
- *Authored 9 custom Suricata IDS signatures detecting brute force, port scanning, SQL injection, directory traversal, and SMB lateral movement, each mapped to MITRE ATT&CK.*
- *Built a Python validator enforcing Suricata rule-authoring standards (required fields, unique SIDs) across a custom signature set.*
