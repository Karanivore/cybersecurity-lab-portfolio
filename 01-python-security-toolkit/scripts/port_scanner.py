#!/usr/bin/env python3
"""
TCP Port Scanner with banner grabbing and service fingerprinting.

Educational network reconnaissance tool for authorized security assessments.
Only scan hosts you own or have explicit written permission to test.

Usage:
    python3 port_scanner.py <host> [--ports 1-1024] [--threads 100] [--timeout 0.5]
    python3 port_scanner.py 127.0.0.1 --ports 20,21,22,80,443,3306,8080
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}


def parse_ports(port_spec: str) -> list[int]:
    ports: set[int] = set()
    for chunk in port_spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            start, end = chunk.split("-")
            ports.update(range(int(start), int(end) + 1))
        elif chunk:
            ports.add(int(chunk))
    return sorted(ports)


def grab_banner(sock: socket.socket) -> str:
    try:
        sock.settimeout(1.0)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner.splitlines()[0][:80] if banner else ""
    except Exception:
        return ""


def scan_port(host: str, port: int, timeout: float) -> dict | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                banner = grab_banner(sock)
                service = COMMON_SERVICES.get(port, "unknown")
                return {"port": port, "service": service, "banner": banner}
    except socket.error:
        return None
    return None


def scan(host: str, ports: list[int], threads: int, timeout: float) -> list[dict]:
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports, key=lambda r: r["port"])


def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner")
    parser.add_argument("host", help="Target host (IP or hostname)")
    parser.add_argument("--ports", default="1-1024", help="Port range/list, e.g. 1-1024 or 22,80,443")
    parser.add_argument("--threads", type=int, default=100, help="Concurrent scan threads")
    parser.add_argument("--timeout", type=float, default=0.5, help="Per-port connect timeout (seconds)")
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"[!] Could not resolve host: {args.host}")
        sys.exit(1)

    ports = parse_ports(args.ports)
    print(f"[*] Scanning {args.host} ({target_ip}) — {len(ports)} ports — started {datetime.now().isoformat(timespec='seconds')}")

    start = datetime.now()
    results = scan(target_ip, ports, args.threads, args.timeout)
    elapsed = (datetime.now() - start).total_seconds()

    print(f"\n{'PORT':<8}{'SERVICE':<12}BANNER")
    print("-" * 60)
    for r in results:
        print(f"{r['port']:<8}{r['service']:<12}{r['banner']}")

    print(f"\n[*] Scan complete: {len(results)} open port(s) found in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
