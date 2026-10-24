#!/usr/bin/env python3
"""
Name:           verify_zero_filler
File:           verify_zero_filler.py
Description:    Deterministic Layer 4 verification tool enforcing Policy §12
                Zero-Filler Skeleton Law & Literal Placeholder Rule.
Version:        100
Date Created:   2026-10-19
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  5c8d2f19-3b4e-4f01-9a72-8e1b6d0c4a35
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("verify_zero_filler requires Python 3.10 or newer.\n")
    sys.exit(20)

import re
import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("verify_zero_filler")

FORBIDDEN_FILLER_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"\blorem\b", "Pseudo-Latin 'lorem' detected"),
    (r"\bipsum\b", "Pseudo-Latin 'ipsum' detected"),
    (r"\bdolor\b", "Pseudo-Latin 'dolor' detected"),
    (r"\bconsectetur\b", "Pseudo-Latin 'consectetur' detected"),
    (r"\badipiscing\b", "Pseudo-Latin 'adipiscing' detected"),
    (r"\bsed do eiusmod\b", "Pseudo-Latin filler snippet detected"),
    (r"\bhere is where\b", "Conversational filler detected"),
    (r"\breplace this with\b", "Conversational placeholder fluff detected"),
    (r"\bexample text\b", "Filler phrase 'example text' detected"),
    (r"\bsample description\b", "Filler phrase 'sample description' detected"),
)


def verify_template_file(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        return {
            "valid": False,
            "file": str(file_path),
            "errors": [f"File not found: {file_path}"],
        }

    content = file_path.read_text(encoding="utf-8")
    content_lower = content.lower()
    errors: List[str] = []

    for pattern, desc in FORBIDDEN_FILLER_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            errors.append(f"Forbidden filler pattern: {desc} (matched '{match.group(0)}')")

    return {
        "valid": len(errors) == 0,
        "file": str(file_path),
        "checked_patterns": len(FORBIDDEN_FILLER_PATTERNS),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="verify_zero_filler",
        description="Verifies templates enforce the Zero-Filler Skeleton Law (Policy §12).",
    )
    parser.add_argument("target", help="Path to template file to verify.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"verify_zero_filler v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Show config.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("verify_zero_filler v%d ready.", VERSION)
        return EXIT_OK

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        LOG.error("Target file not found: %s", target_path)
        return EXIT_PATH_FAILURE

    report = verify_template_file(target_path)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    if not report["valid"]:
        LOG.error("Zero-filler template verification FAILED with %d error(s).", len(report["errors"]))
        return EXIT_SCHEMA_FAILURE

    LOG.info("Zero-filler template verification PASSED (%d rules verified).", report["checked_patterns"])
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
