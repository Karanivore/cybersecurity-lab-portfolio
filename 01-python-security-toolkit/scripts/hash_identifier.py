#!/usr/bin/env python3
"""
Hash Identifier & Dictionary-Attack Demonstrator.

Identifies likely hash algorithm(s) by length/charset, and — for
educational purposes — attempts to recover plaintext for unsalted
fast hashes (MD5/SHA1/SHA256/SHA512) against a wordlist. This mirrors
the first move an attacker (or a pentester validating password policy)
makes against a dumped, unsalted hash list. Never use against hashes
you don't own or have authorization to test.

Usage:
    python3 hash_identifier.py --identify 5f4dcc3b5aa765d61d8327deb882cf99
    python3 hash_identifier.py --crack 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist ../sample_data/common_passwords.txt
"""

import argparse
import hashlib
import re
from pathlib import Path

HASH_SIGNATURES = [
    (32, r"^[a-f0-9]{32}$", ["MD5", "NTLM"]),
    (40, r"^[a-f0-9]{40}$", ["SHA-1"]),
    (56, r"^[a-f0-9]{56}$", ["SHA-224", "SHA3-224"]),
    (64, r"^[a-f0-9]{64}$", ["SHA-256", "SHA3-256"]),
    (96, r"^[a-f0-9]{96}$", ["SHA-384", "SHA3-384"]),
    (128, r"^[a-f0-9]{128}$", ["SHA-512", "SHA3-512"]),
]

HASHLIB_ALGOS = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-384": hashlib.sha384,
    "SHA-512": hashlib.sha512,
}


def identify_hash(h: str) -> list[str]:
    h = h.strip().lower()
    if h.startswith("$2a$") or h.startswith("$2b$") or h.startswith("$2y$"):
        return ["bcrypt"]
    if h.startswith("$1$"):
        return ["MD5-crypt"]
    if h.startswith("$6$"):
        return ["SHA-512-crypt"]
    for length, pattern, names in HASH_SIGNATURES:
        if len(h) == length and re.match(pattern, h):
            return names
    return ["unknown"]


def crack_hash(target_hash: str, wordlist_path: str) -> tuple[str | None, str | None, int]:
    """Try every candidate algorithm against every word in the wordlist."""
    target = target_hash.strip().lower()
    candidates = [name for name in identify_hash(target) if name in HASHLIB_ALGOS]
    if not candidates:
        candidates = list(HASHLIB_ALGOS.keys())

    words_tried = 0
    with open(wordlist_path, "r", errors="ignore") as f:
        words = [w.strip() for w in f if w.strip()]

    for algo_name in candidates:
        algo = HASHLIB_ALGOS[algo_name]
        for word in words:
            words_tried += 1
            if algo(word.encode()).hexdigest() == target:
                return word, algo_name, words_tried
    return None, None, words_tried


def main():
    parser = argparse.ArgumentParser(description="Hash identifier and dictionary-attack demonstrator")
    parser.add_argument("--identify", metavar="HASH", help="Identify the likely algorithm for a hash")
    parser.add_argument("--crack", metavar="HASH", help="Attempt to recover plaintext via dictionary attack")
    parser.add_argument("--wordlist", default=str(Path(__file__).resolve().parent.parent / "sample_data" / "common_passwords.txt"))
    args = parser.parse_args()

    if args.identify:
        matches = identify_hash(args.identify)
        print(f"Hash:      {args.identify}")
        print(f"Length:    {len(args.identify.strip())} chars")
        print(f"Likely algorithm(s): {', '.join(matches)}")

    if args.crack:
        print(f"[*] Attempting dictionary attack on {args.crack}")
        print(f"[*] Wordlist: {args.wordlist}")
        plaintext, algo, tried = crack_hash(args.crack, args.wordlist)
        if plaintext:
            print(f"[+] CRACKED after {tried} attempts: '{plaintext}' ({algo})")
        else:
            print(f"[-] Not found after {tried} attempts. Password not in wordlist or hash is salted.")

    if not args.identify and not args.crack:
        parser.print_help()


if __name__ == "__main__":
    main()
