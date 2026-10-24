#!/usr/bin/env python3
"""
Name:           verify_behtml_preferences
File:           verify_behtml_preferences.py
Description:    Deterministic Layer 4 verification script for BEHTML design preferences.
                Verifies Policy 8.1 Tri-Color tokens (#DE2626), Ry=32px vertical quantization,
                viewport lock, contained scrollbars, and archetype-specific invariants across
                Web Documents (with shelf and widgetless), Standard Pages, Feeds, and Dashboards.
Version:        101
Date Created:   2026-10-18
Last Modified:  2026-10-19
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  8d2f4a19-7c3e-4b05-9a61-2e5c8d0f3b14
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("verify_behtml_preferences requires Python 3.10 or newer.\n")
    sys.exit(20)

import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION: int = 101
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("verify_behtml_preferences")

# Foundational tokens required across all BEHTML files
CORE_TOKENS: Tuple[Tuple[str, str], ...] = (
    ("box-sizing: border-box", "Universal box-sizing reset"),
    ("-webkit-tap-highlight-color: transparent", "Touch tap highlight reset"),
    ("overflow: hidden", "Window scroll lock on body"),
    ("--ry-unit", "Ry vertical quantization custom property or 32px unit"),
    ("#DE2626", "Policy 8.1 Red accent token"),
    ("::-webkit-scrollbar", "Contained scrollbar definition"),
)

ARCHETYPE_TOKENS: Dict[str, Tuple[Tuple[str, str], ...]] = {
    "document": (
        ("6.25%", "16-sublane horizontal partitioning (6.25% gutters)"),
        ("grid-row: 1 / span 1", "Row 1 title bar placement"),
        ("grid-row: 20 / span 5", "Row 20 span 5 widget shelf placement"),
        ("150px", "150x150px widget slot dimensions"),
    ),
    "document-widgetless": (
        ("6.25%", "16-sublane horizontal partitioning (6.25% gutters)"),
        ("grid-row: 1 / span 1", "Row 1 title bar placement"),
        ("gutter-left", "Left edge gutter"),
        ("gutter-right", "Right edge gutter"),
        ("author-null-footer", "Monospace author null footer"),
    ),
    "standard-page": (
        ("behtml-header", "Top docked header component"),
        ("behtml-sidebar", "Collapsible navigation sidebar drawer"),
        ("behtml-surface", "Main design surface"),
        ("behtml-card", "Modular content card"),
        ("behtml-auditor-hud", "Anti-drift auditor HUD"),
    ),
    "feed": (
        ("feed-header", "Top feed control header"),
        ("feed-card", "Modular feed card component"),
        ("feed-filter-bar", "Category/tag filter bar"),
        ("feed-grid", "8-lane or 16-sublane card stream grid"),
    ),
    "dashboard": (
        ("dashboard-header", "Top docked dashboard control hub"),
        ("behtml-dashboard-canvas", "Spatial canvas"),
        ("behtml-dash-cell", "Deterministic spatial cell"),
        ("repeat(8, 1fr)", "8-lane spatial grid columns"),
    ),
}


def detect_archetype(content: str) -> str:
    if "widget-shelf" in content or "grid-row: 20 / span 5" in content:
        return "document"
    if "gutter-left" in content and "behtml-title-bar" in content and "widget-shelf" not in content:
        return "document-widgetless"
    if "behtml-sidebar" in content and "behtml-surface" in content:
        return "standard-page"
    if "feed-card" in content or "feed-stream" in content:
        return "feed"
    if "behtml-dashboard-canvas" in content or "behtml-dash-cell" in content:
        return "dashboard"
    return "core"


def verify_html_file(html_path: Path, archetype: str = "auto") -> Dict[str, Any]:
    if not html_path.exists():
        return {
            "valid": False,
            "file": str(html_path),
            "errors": [f"File not found: {html_path}"],
        }
    content = html_path.read_text(encoding="utf-8")
    errors: List[str] = []

    # Verify core tokens
    for token, desc in CORE_TOKENS:
        if token not in content:
            errors.append(f"Missing core BEHTML token '{token}' ({desc}).")

    target_arch = detect_archetype(content) if archetype == "auto" else archetype

    # Verify archetype-specific tokens
    if target_arch in ARCHETYPE_TOKENS:
        for token, desc in ARCHETYPE_TOKENS[target_arch]:
            if token not in content:
                errors.append(f"Missing archetype '{target_arch}' requirement '{token}' ({desc}).")

    return {
        "valid": len(errors) == 0,
        "file": str(html_path),
        "detected_archetype": target_arch,
        "checked_invariants": len(CORE_TOKENS) + len(ARCHETYPE_TOKENS.get(target_arch, ())),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="verify_behtml_preferences",
        description="Verifies HTML documents and applications against BEHTML design preferences.",
    )
    parser.add_argument("target", nargs="?", help="Path to HTML file to verify.")
    parser.add_argument(
        "--archetype",
        choices=["auto", "core", "document", "document-widgetless", "standard-page", "feed", "dashboard"],
        default="auto",
        help="Target archetype schema to verify against (default: auto).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"verify_behtml_preferences v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Show config.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("verify_behtml_preferences v%d ready.", VERSION)
        return EXIT_OK

    target_path = (
        Path(args.target).resolve()
        if args.target
        else (SCRIPT_PATH.parent / "assets" / "Template_HTML_Document.html")
    )
    if not target_path.exists():
        LOG.error("Target HTML file not found: %s", target_path)
        return EXIT_PATH_FAILURE

    report = verify_html_file(target_path, archetype=args.archetype)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    if not report["valid"]:
        LOG.error("BEHTML design preferences check FAILED with %d error(s).", len(report["errors"]))
        return EXIT_SCHEMA_FAILURE

    LOG.info(
        "BEHTML design preferences check PASSED for archetype '%s' (%d invariants verified).",
        report["detected_archetype"],
        report["checked_invariants"],
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
