#!/usr/bin/env python3
"""
Generates a synthetic, multi-source ransomware incident dataset used by
timeline_reconstruction.py — three independent JSON sources (email
gateway, EDR, file server audit) that must be merged and ordered to
reconstruct the attack, mirroring how a real IR engagement pulls
evidence from disconnected tools.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "sample_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

T0 = datetime(2026, 6, 14, 9, 2, 0)

email_gateway = [
    {"ts": (T0).isoformat(), "source": "email_gateway", "event": "email_delivered",
     "detail": "Invoice_Overdue_June.docm delivered to j.rivera@corp.local from spoofed sender 'accounts@vendor-billing.com'",
     "user": "j.rivera", "host": "WKS-0231"},
    {"ts": (T0 + timedelta(minutes=6)).isoformat(), "source": "email_gateway", "event": "attachment_opened_reported",
     "detail": "User later reported opening the attachment and enabling macros to 'view the invoice'",
     "user": "j.rivera", "host": "WKS-0231"},
]

edr_alerts = [
    {"ts": (T0 + timedelta(minutes=7)).isoformat(), "source": "edr", "event": "suspicious_process_creation",
     "detail": "WINWORD.EXE spawned powershell.exe -enc <base64> (macro-triggered)", "user": "j.rivera", "host": "WKS-0231", "mitre": "T1566.001 / T1059.001"},
    {"ts": (T0 + timedelta(minutes=8)).isoformat(), "source": "edr", "event": "network_connection",
     "detail": "powershell.exe established outbound connection to 185.220.101.47:443 (known C2 infrastructure)", "user": "j.rivera", "host": "WKS-0231", "mitre": "T1071.001"},
    {"ts": (T0 + timedelta(minutes=9)).isoformat(), "source": "edr", "event": "file_write",
     "detail": "Dropped payload C:\\Users\\j.rivera\\AppData\\Local\\Temp\\svchost_update.exe", "user": "j.rivera", "host": "WKS-0231", "mitre": "T1105"},
    {"ts": (T0 + timedelta(minutes=11)).isoformat(), "source": "edr", "event": "credential_access",
     "detail": "LSASS memory access attempt by svchost_update.exe (Mimikatz-like behavior)", "user": "j.rivera", "host": "WKS-0231", "mitre": "T1003.001"},
    {"ts": (T0 + timedelta(minutes=18)).isoformat(), "source": "edr", "event": "lateral_movement",
     "detail": "SMB admin-share connection from WKS-0231 to FS-01 using j.rivera domain-admin-delegated credentials", "user": "j.rivera", "host": "FS-01", "mitre": "T1021.002"},
    {"ts": (T0 + timedelta(minutes=20)).isoformat(), "source": "edr", "event": "shadow_copy_deletion",
     "detail": "vssadmin.exe delete shadows /all /quiet executed on FS-01", "user": "j.rivera", "host": "FS-01", "mitre": "T1490"},
    {"ts": (T0 + timedelta(minutes=21)).isoformat(), "source": "edr", "event": "ransom_binary_execution",
     "detail": "Execution of unsigned binary crypt_locker.exe on FS-01", "user": "SYSTEM", "host": "FS-01", "mitre": "T1486"},
]

file_events = [
    {"ts": (T0 + timedelta(minutes=22, seconds=i * 3)).isoformat(), "source": "file_audit", "event": "mass_file_modification",
     "detail": f"Batch {i+1}: 500 files renamed with .locked extension under \\\\FS-01\\shared\\finance", "user": "SYSTEM", "host": "FS-01"}
    for i in range(6)
]
file_events.append({
    "ts": (T0 + timedelta(minutes=23)).isoformat(), "source": "file_audit", "event": "ransom_note_created",
    "detail": "README_TO_DECRYPT.txt written to 14 network share root directories", "user": "SYSTEM", "host": "FS-01",
})

(OUT_DIR / "email_gateway.json").write_text(json.dumps(email_gateway, indent=2))
(OUT_DIR / "edr_alerts.json").write_text(json.dumps(edr_alerts, indent=2))
(OUT_DIR / "file_events.json").write_text(json.dumps(file_events, indent=2))

print(f"[+] Wrote {len(email_gateway)} email events, {len(edr_alerts)} EDR events, {len(file_events)} file events to {OUT_DIR}")
