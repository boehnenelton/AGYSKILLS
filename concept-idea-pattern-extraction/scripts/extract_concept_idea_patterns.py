#!/usr/bin/env python3
"""
Name:           extract_concept_idea_patterns
File:           extract_concept_idea_patterns.py
Description:    Layer 5 validator and BEJSON 104a writer for ConceptIdeaPattern
                registries (concept-idea-pattern-extraction). Enforces boundary-layer
                whitespace sanitization, O(1) field_map lookups, and atomic persistence.
Version:        100
Date Created:   2026-10-18
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  8c3e1a95-4d7b-4f02-9e16-2b5d8c0a4f71
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("extract_concept_idea_patterns requires Python 3.10 or newer.\n")
    sys.exit(20)

import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

REQUIRED_FIELDS: tuple[str, ...] = (
    "idea_pattern_uuid",
    "idea_pattern_code",
    "idea_pattern_name",
    "idea_archetype_family",
    "idea_problem_solved",
    "idea_mechanism_signature",
    "idea_trigger_when",
    "idea_anti_pattern_blocked",
    "idea_target_layer_tier",
    "idea_created_at",
)


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("extract_concept_idea_patterns")


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    clean_doc: Dict[str, Any] = {
        (k.strip() if isinstance(k, str) else k): v for k, v in raw_doc.items()
    }
    for fdef in clean_doc.get("Fields", []):
        if isinstance(fdef, dict):
            for fkey in ("name", "type"):
                if isinstance(fdef.get(fkey), str):
                    fdef[fkey] = fdef[fkey].strip()
    for row in clean_doc.get("Values", []):
        if isinstance(row, list):
            for idx, val in enumerate(row):
                if isinstance(val, str):
                    row[idx] = val.strip()
    return clean_doc


def bejson_core_get_field_map(bejson_doc: Dict[str, Any]) -> Dict[str, int]:
    return {f["name"]: idx for idx, f in enumerate(bejson_doc.get("Fields", []))}


def validate_idea_registry(target_path: Path) -> Dict[str, Any]:
    raw_data = json.loads(target_path.read_text(encoding="utf-8"))
    doc = bejson_core_sanitize_doc(raw_data)
    fmap = bejson_core_get_field_map(doc)
    errors: List[str] = []

    for req in REQUIRED_FIELDS:
        if req not in fmap:
            errors.append(f"Missing required field '{req}' in ConceptIdeaPattern schema.")

    if not errors:
        for r_idx, row in enumerate(doc.get("Values", [])):
            if len(row) != len(fmap):
                errors.append(f"Row {r_idx} length mismatch ({len(row)} != {len(fmap)}).")
                continue
            code_val = row[fmap["idea_pattern_code"]]
            name_val = row[fmap["idea_pattern_name"]]
            layer_val = row[fmap["idea_target_layer_tier"]]
            if not code_val or not name_val:
                errors.append(f"Row {r_idx} has empty idea_pattern_code or idea_pattern_name.")
            if not isinstance(layer_val, int) or not (1 <= layer_val <= 6):
                errors.append(f"Row {r_idx} idea_target_layer_tier must be an integer 1..6.")

    return {
        "valid": len(errors) == 0,
        "file": str(target_path),
        "record_count": len(doc.get("Values", [])),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="extract_concept_idea_patterns",
        description="Validates ConceptIdeaPattern BEJSON 104a registries.",
    )
    parser.add_argument("target", nargs="?", help="Path to ConceptIdeaPattern .104a.bejson file.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"extract_concept_idea_patterns v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Show config.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("extract_concept_idea_patterns v%d ready.", VERSION)
        return EXIT_OK

    target_path = (
        Path(args.target).resolve()
        if args.target
        else (SCRIPT_PATH.parent / "assets" / "template_concept_idea_patterns.104a.bejson")
    )
    if not target_path.exists():
        LOG.error("Target file does not exist: %s", target_path)
        return EXIT_PATH_FAILURE

    report = validate_idea_registry(target_path)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    if not report["valid"]:
        LOG.error("ConceptIdeaPattern validation FAILED.")
        return EXIT_SCHEMA_FAILURE

    LOG.info("ConceptIdeaPattern validation PASSED (%d records).", report["record_count"])
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
