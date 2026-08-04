# Network Segmentation Design

Zero-trust-leaning segmentation for a small corporate network: internet
traffic never reaches internal/management zones directly, east-west
traffic between zones is default-deny, and the management VLAN is
reachable only via a jump host.

```mermaid
flowchart TB
    Internet((Internet))

    subgraph Perimeter["Perimeter Firewall (default-deny, stateful)"]
        FW["Edge Firewall"]
    end

    subgraph DMZ["DMZ VLAN 10 — 10.10.10.0/24"]
        WEB["Web/App Servers"]
        MAIL["Mail Gateway"]
    end

    subgraph INTERNAL["Internal VLAN 20 — 10.10.20.0/24"]
        WKS["User Workstations"]
        FS["File Servers"]
    end

    subgraph MGMT["Management VLAN 30 — 10.10.30.0/24"]
        JUMP["Jump Host (bastion, MFA)"]
        ADMIN["Admin/EDR Console, Domain Controller"]
    end

    subgraph SEC["Security VLAN 40 — 10.10.40.0/24"]
        SIEM["SIEM / IDS Sensor"]
    end

    Internet -->|443/80 only| FW
    FW -->|allow inbound 443/80| WEB
    FW -->|allow inbound 25/587| MAIL
    FW -.->|deny by default| INTERNAL
    FW -.->|deny by default| MGMT

    WKS -->|outbound 443 via proxy| FW
    WEB <-.->|deny direct DMZ→Internal| FS
    WEB -->|explicit allow: app→DB port only| FS

    WKS -.->|deny direct| ADMIN
    JUMP -->|allow: SSH/RDP, MFA required| ADMIN
    WKS -->|allow: to jump host only| JUMP

    DMZ -->|mirrored/tap traffic| SIEM
    INTERNAL -->|mirrored/tap traffic| SIEM
    MGMT -->|mirrored/tap traffic| SIEM
```

## Design principles applied

1. **Default-deny at every boundary** — DMZ, Internal, and Management
   VLANs only accept the specific flows listed above; everything else is
   dropped and logged.
2. **No direct DMZ → Internal path** except the single explicit
   application-to-database port required by the web tier — this is the
   control that would have stopped the Lab 2 scenario's SQL injection
   from reaching internal systems even if the web app were compromised.
3. **Management plane isolation** — the Domain Controller and EDR
   console are only reachable via a bastion/jump host requiring MFA;
   workstations cannot reach them directly, containing the Lab 4
   ransomware scenario's lateral-movement path.
4. **Full traffic visibility** — every VLAN is mirrored to a dedicated
   security segment running the IDS sensor (`suricata_custom.rules`) and
   feeding the SIEM (Lab 2's detection engine).

See `firewall/harden_firewall.sh` for the nftables implementation of the
perimeter and inter-VLAN rules, and `ids/suricata_custom.rules` for the
IDS signatures monitoring each segment.
