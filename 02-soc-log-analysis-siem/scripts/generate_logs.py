#!/usr/bin/env python3
"""
Synthetic log generator for the SOC Log Analysis lab.

Produces three realistic, timestamp-correlated log sources under
../sample_data/ that together tell a single incident story:

  1. A reconnaissance port scan against a web server (firewall.log)
  2. An SSH brute-force attack that succeeds (auth.log)
  3. A web application SQL-injection / directory-traversal probe (web_access.log)

...interleaved with benign background traffic, so the detection engine
in detection_engine.py has to separate signal from noise — same as a
real SIEM feed.

Deterministic (fixed random seed) so the lab is reproducible.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(1337)

OUT_DIR = Path(__file__).resolve().parent.parent / "sample_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_TIME = datetime(2026, 7, 22, 3, 10, 0)

ATTACKER_IP = "203.0.113.55"
SCANNER_IP = "198.51.100.7"
BENIGN_IPS = ["10.0.1.14", "10.0.1.22", "10.0.1.9", "192.168.1.44", "172.16.5.3"]
USERS = ["root", "admin", "administrator", "test", "ubuntu", "oracle", "guest"]

auth_lines = []
firewall_lines = []
web_lines = []


def ts_auth(t: datetime) -> str:
    return t.strftime("%b %d %H:%M:%S").replace(" 0", "  ", 1) if t.day < 10 else t.strftime("%b %d %H:%M:%S")


def ts_fw(t: datetime) -> str:
    return t.strftime("%Y-%m-%d %H:%M:%S")


def ts_web(t: datetime) -> str:
    return t.strftime("%d/%b/%Y:%H:%M:%S +0000")


# --- 1. Port scan reconnaissance against the host (firewall.log) ---
scan_start = BASE_TIME
common_ports = [21, 22, 23, 25, 80, 110, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080]
t = scan_start
for port in common_ports:
    t += timedelta(milliseconds=random.randint(80, 300))
    action = "ACCEPT" if port == 22 else "DROP"
    firewall_lines.append(f"{ts_fw(t)} SRC={SCANNER_IP} DST=10.0.0.5 SPT={random.randint(40000,60000)} DPT={port} PROTO=TCP ACTION={action}")

# --- 2. SSH brute force from the same actor (a few minutes later), then success ---
brute_start = BASE_TIME + timedelta(minutes=3)
t = brute_start
for i in range(9):
    t += timedelta(seconds=random.randint(4, 12))
    user = random.choice(USERS)
    port = random.randint(40000, 60000)
    auth_lines.append(f"{ts_auth(t)} web01 sshd[master]: Failed password for invalid user {user} from {ATTACKER_IP} port {port} ssh2")
    firewall_lines.append(f"{ts_fw(t)} SRC={ATTACKER_IP} DST=10.0.0.5 SPT={port} DPT=22 PROTO=TCP ACTION=ACCEPT")

t += timedelta(seconds=8)
success_port = random.randint(40000, 60000)
auth_lines.append(f"{ts_auth(t)} web01 sshd[master]: Accepted password for root from {ATTACKER_IP} port {success_port} ssh2")
firewall_lines.append(f"{ts_fw(t)} SRC={ATTACKER_IP} DST=10.0.0.5 SPT={success_port} DPT=22 PROTO=TCP ACTION=ACCEPT")
t += timedelta(seconds=2)
auth_lines.append(f"{ts_auth(t)} web01 sshd[master]: pam_unix(sshd:session): session opened for user root by (uid=0)")

# --- 3. Web app attack: SQLi + directory traversal probing (web_access.log) ---
web_attack_start = BASE_TIME + timedelta(minutes=6)
t = web_attack_start
sqli_payloads = [
    "/product?id=1 UNION SELECT username,password FROM users--",
    "/login?user=admin' OR '1'='1&pass=x",
    "/search?q=1%27%20UNION%20SELECT%20NULL,version()--",
    "/product?id=1;DROP TABLE orders--",
]
traversal_payloads = [
    "/download?file=../../../../etc/passwd",
    "/static/../../../etc/shadow",
]
for payload in sqli_payloads:
    t += timedelta(milliseconds=random.randint(300, 900))
    web_lines.append(f'{ATTACKER_IP} - - [{ts_web(t)}] "GET {payload} HTTP/1.1" 200 612 "-" "sqlmap/1.7"')
for payload in traversal_payloads:
    t += timedelta(milliseconds=random.randint(300, 900))
    web_lines.append(f'{ATTACKER_IP} - - [{ts_web(t)}] "GET {payload} HTTP/1.1" 403 218 "-" "sqlmap/1.7"')

# --- Benign background noise across the whole window (auth + web + firewall) ---
window_start = BASE_TIME
window_end = BASE_TIME + timedelta(minutes=20)
t = window_start
paths = ["/", "/products", "/about", "/api/health", "/cart", "/checkout", "/static/logo.png"]
while t < window_end:
    t += timedelta(seconds=random.randint(5, 45))
    ip = random.choice(BENIGN_IPS)
    web_lines.append(f'{ip} - - [{ts_web(t)}] "GET {random.choice(paths)} HTTP/1.1" 200 {random.randint(200,4000)} "-" "Mozilla/5.0"')
    firewall_lines.append(f"{ts_fw(t)} SRC={ip} DST=10.0.0.5 SPT={random.randint(40000,60000)} DPT=443 PROTO=TCP ACTION=ACCEPT")
    if random.random() < 0.1:
        auth_lines.append(f"{ts_auth(t)} web01 sshd[master]: Accepted publickey for deploy from {ip} port {random.randint(40000,60000)} ssh2")

auth_lines.sort()
firewall_lines.sort()
web_lines.sort(key=lambda l: l.split("[")[1].split("]")[0])

(OUT_DIR / "auth.log").write_text("\n".join(auth_lines) + "\n")
(OUT_DIR / "firewall.log").write_text("\n".join(firewall_lines) + "\n")
(OUT_DIR / "web_access.log").write_text("\n".join(web_lines) + "\n")

print(f"[+] Generated {len(auth_lines)} auth.log lines")
print(f"[+] Generated {len(firewall_lines)} firewall.log lines")
print(f"[+] Generated {len(web_lines)} web_access.log lines")
print(f"[+] Written to {OUT_DIR}")
