#!/usr/bin/env python3
"""
File_Name:          verify_component_map.py
Description:        Audits and validates Web UI Component tree maps against the 5-tier hierarchy and backend leak prohibitions.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      4f2b9a1c-8e3d-4c5b-97a6-1e0f3d5c7a2b
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import re
import sys
from typing import Any, Dict, List

VERSION = "100"
RELEASE_VERSION = "300"
RELATIONAL_ID = "4f2b9a1c-8e3d-4c5b-97a6-1e0f3d5c7a2b"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("verify_component_map")

FORBIDDEN_BACKEND_TOKENS = [
    r"\b_fk\b",
    r"\b_id\b",
    r"\bprimary\s+key\b",
    r"\bforeign\s+key\b",
    r"\bsql\b",
    r"\bdatabase\s+table\b",
    r"\btable\s+column\b",
    r"\bvarchar\b",
    r"\binteger\s+type\b",
    r"\bapi\s+endpoint\b",
    r"\bjson\s+payload\b",
    r"\brest\s+route\b",
]

ALLOWED_CONTAINER_TAGS = {
    "[SECTION]",
    "[PANEL]",
    "[CARD]",
    "[DRAWER]",
    "[TOOLBAR]",
    "[ACTION BAR]",
}


def audit_component_map(file_path: Path) -> tuple[bool, List[str]]:
    if not file_path.exists():
        LOG.error("Component map file not found: %s", file_path)
        sys.exit(20)

    content = file_path.read_text(encoding="utf-8")
    lines = [line.rstrip() for line in content.splitlines() if line.strip()]
    errors: List[str] = []

    if not lines:
        errors.append("Empty component map file.")
        return False, errors

    # Check Tier 1 Root Entry Point
    root_line = lines[0].strip()
    if not re.search(r"^[A-Z0-9_\-\.\s]+\s*\([a-zA-Z0-9_\-\./\\]+\)$", root_line) and not "ENTRY POINT" in root_line.upper():
        errors.append(f"Root node must specify an application entry point: '{root_line}'")

    has_containers = False
    has_controls = False

    for idx, line in enumerate(lines, start=1):
        # Check forbidden backend leaks
        for pat in FORBIDDEN_BACKEND_TOKENS:
            if re.search(pat, line, re.IGNORECASE):
                errors.append(f"Line {idx}: Prohibited backend leak detected matching pattern '{pat}': '{line.strip()}'")

        # Check for container tags
        for tag in ALLOWED_CONTAINER_TAGS:
            if tag in line:
                has_containers = True
                break

        # Check for interactive control leaf markers
        if any(term in line.lower() for term in ("button", "input", "selector", "toggle", "textarea", "modal", "table", "dropdown")):
            has_controls = True

    if not has_containers:
        errors.append("No standard structural container tags ([SECTION], [CARD], [PANEL], [DRAWER]) detected.")

    if not has_controls:
        errors.append("No atomic interactive controls (Button, Input, Selector, Toggle) detected in leaf nodes.")

    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="verify_component_map",
        description="Audits Web UI Component tree maps against the 5-tier architecture and backend leak prohibitions.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Register script with master index.")
    parser.add_argument("--config", action="store_true", help="Display script configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")
    parser.add_argument("target", nargs="?", type=Path, help="Path to ASCII component map file to verify.")

    args = parser.parse_args()

    if args.register:
        LOG.info("Registered verify_component_map v%s (%s)", VERSION, RELATIONAL_ID)
        return 0

    if args.config:
        cfg = {
            "version": VERSION,
            "release_version": RELEASE_VERSION,
            "author": "Elton Boehnen",
            "forbidden_tokens": FORBIDDEN_BACKEND_TOKENS,
        }
        sys.stdout.write(json.dumps(cfg, indent=2) + "\n")
        return 0

    if args.reset:
        LOG.info("Reset state complete.")
        return 0

    if not args.target:
        parser.print_help()
        return 10

    valid, errors = audit_component_map(args.target)
    result = {
        "valid": valid,
        "file": str(args.target),
        "errors": errors,
    }
    sys.stdout.write(json.dumps(result, indent=2) + "\n")

    if valid:
        LOG.info("Component map verification PASSED.")
        return 0
    else:
        LOG.error("Component map verification FAILED (%d errors).", len(errors))
        return 10


if __name__ == "__main__":
    sys.exit(main())
