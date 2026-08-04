#!/usr/bin/env python3
"""
Lightweight structural validator for Suricata rule files.

Not a substitute for `suricata -T -S rules.file` (the real syntax
checker), but catches the most common authoring mistakes — missing
required options, duplicate SIDs, malformed header — without needing a
full Suricata install. Used here to self-check ids/suricata_custom.rules.

Usage:
    python3 validate_suricata_rules.py ../ids/suricata_custom.rules
"""

import argparse
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(
    r"^(?P<action>alert|drop|pass|reject)\s+"
    r"(?P<proto>\S+)\s+"
    r"(?P<src>\S+)\s+(?P<sport>\S+)\s+"
    r"(?P<dir>->|<>)\s+"
    r"(?P<dst>\S+)\s+(?P<dport>\S+)\s+"
    r"\((?P<options>.*)\)\s*$"
)

REQUIRED_OPTIONS = ["msg", "sid"]


def parse_rule_line(line: str, lineno: int) -> dict:
    m = HEADER_RE.match(line.strip())
    if not m:
        return {"lineno": lineno, "error": "Does not match Suricata rule header grammar", "raw": line}

    options_str = m.group("options")
    options = {}
    for part in options_str.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            key, _, val = part.partition(":")
            options[key.strip()] = val.strip()
        else:
            options[part] = True

    missing = [opt for opt in REQUIRED_OPTIONS if opt not in options]
    errors = []
    if missing:
        errors.append(f"Missing required option(s): {', '.join(missing)}")
    if "sid" in options and not re.match(r"^\d+$", options["sid"]):
        errors.append(f"sid value is not numeric: {options['sid']!r}")

    return {
        "lineno": lineno, "action": m.group("action"), "proto": m.group("proto"),
        "sid": options.get("sid"), "msg": options.get("msg", "").strip('"'),
        "errors": errors, "raw": line,
    }


def join_continuations(raw_lines: list[str]) -> list[tuple[int, str]]:
    """Join backslash line-continuations, remembering the starting line number of each logical rule."""
    joined = []
    buf = ""
    start_lineno = None
    for lineno, line in enumerate(raw_lines, start=1):
        if start_lineno is None:
            start_lineno = lineno
        stripped = line.rstrip()
        if stripped.endswith("\\"):
            buf += stripped[:-1] + " "
        else:
            buf += stripped
            joined.append((start_lineno, buf))
            buf = ""
            start_lineno = None
    if buf:
        joined.append((start_lineno, buf))
    return joined


def validate(path: Path) -> tuple[list[dict], list[str]]:
    rules = []
    global_errors = []
    seen_sids = set()

    for lineno, logical_line in join_continuations(path.read_text().splitlines()):
        stripped = logical_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        rule = parse_rule_line(stripped, lineno)
        if "error" in rule:
            global_errors.append(f"Line {lineno}: {rule['error']}")
            continue
        if rule["errors"]:
            for e in rule["errors"]:
                global_errors.append(f"Line {lineno} (sid {rule.get('sid')}): {e}")
        if rule["sid"]:
            if rule["sid"] in seen_sids:
                global_errors.append(f"Line {lineno}: duplicate sid {rule['sid']}")
            seen_sids.add(rule["sid"])
        rules.append(rule)

    return rules, global_errors


def main():
    parser = argparse.ArgumentParser(description="Structural validator for Suricata rule files")
    parser.add_argument("rules_file")
    args = parser.parse_args()

    path = Path(args.rules_file)
    rules, errors = validate(path)

    print(f"[*] Parsed {len(rules)} rule(s) from {path}\n")
    for r in rules:
        print(f"  sid:{r['sid']:<8} [{r['action']}/{r['proto']}] {r['msg']}")

    if errors:
        print(f"\n[!] {len(errors)} issue(s) found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n[+] All rules structurally valid (header + required options present, no duplicate SIDs)")


if __name__ == "__main__":
    main()
