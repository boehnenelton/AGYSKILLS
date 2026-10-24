#!/usr/bin/env python3
"""
Scaffold Fluff & Zero-Filler Linter
Audits template code files (HTML, BEHTML, JSON, Python, Bash) for compliance with
Zero Filler Content, Strictly Functional Placeholders, and Invisible Architecture rules.

Creator: Elton Boehnen
Release Version: 300
Policy Binding: Policy §7.3 Negative Constraints & §12.4
"""

import sys
import re
from pathlib import Path

VERSION = "1.0.0"

BANNED_FILLER_PATTERNS = [
    r"\blorem\b",
    r"\bipsum\b",
    r"\bdolor\s+sit\b",
    r"\bconsectetur\b",
    r"\bsample\s+text\b",
    r"\bdummy\s+text\b",
    r"\bplaceholder\s+text\b",
    r"\bwelcome\s+to\b",
    r"\bour\s+services\b",
    r"\btestimonials?\b",
]

BANNED_FRAMEWORK_PATTERNS = [
    r"grid\s+space\s+activated",
    r"framework\s+loaded",
    r"lane\s+\d+\s+to\s+\d+\s+active",
    r"container\s+wrapper\s+rendered",
    r"breakpoint\s+triggered",
]

BANNED_IMAGE_HOSTS = [
    r"via\.placeholder\.com",
    r"placeholder\.com",
    r"picsum\.photos",
    r"unsplash\.com",
]


def audit_template_file(file_path: Path) -> list:
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return [f"Unable to read {file_path}: {exc}"]

    # 1. Check for lorem ipsum and generic copy filler
    for pattern in BANNED_FILLER_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings.append(f"Contains banned copy filler matching '{pattern}': count={len(matches)}")

    # 2. Check for framework telemetry leakage
    for pattern in BANNED_FRAMEWORK_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings.append(f"Contains banned framework telemetry leak matching '{pattern}': count={len(matches)}")

    # 3. Check for external mock image services
    for host in BANNED_IMAGE_HOSTS:
        matches = re.findall(host, content, re.IGNORECASE)
        if matches:
            findings.append(f"References banned external placeholder image host '{host}': count={len(matches)}")

    return findings


def main():
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

    if not target_path.exists():
        print(f"Error: Target path does not exist: {target_path}", file=sys.stderr)
        return 2

    files_to_audit = []
    if target_path.is_file():
        files_to_audit.append(target_path)
    else:
        for ext in ["*.html", "*.htm", "*.json", "*.py", "*.sh", "*.md"]:
            files_to_audit.extend(target_path.rglob(ext))

    total_violations = 0
    audited_count = 0

    print(f"Auditing {len(files_to_audit)} files for Zero Filler and Invisible Architecture...")

    for fpath in files_to_audit:
        # Skip pycache, git, backups
        if any(part in fpath.parts for part in [".git", "__pycache__", ".pytest_cache", "node_modules"]):
            continue

        audited_count += 1
        violations = audit_template_file(fpath)
        if violations:
            total_violations += len(violations)
            print(f"\n[FAIL] {fpath}")
            for v in violations:
                print(f"  - {v}")

    print(f"\nAudit complete: {audited_count} files checked.")
    if total_violations > 0:
        print(f"FAILED: {total_violations} filler/telemetry violations detected.")
        return 1

    print("PASS: Zero filler or telemetry violations detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
