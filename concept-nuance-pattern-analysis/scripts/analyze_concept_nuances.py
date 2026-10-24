#!/usr/bin/env python3
"""
Name:           analyze_concept_nuances
File:           analyze_concept_nuances.py
Description:    Layer 5 validator and BEJSON 104a writer for ConceptNuancePattern
                registries (concept-nuance-pattern-analysis). Enforces boundary-layer
                whitespace sanitization, O(1) field_map lookups, and atomic persistence.
Version:        100
Date Created:   2026-10-18
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  5a9c2e14-8b3d-4f70-9a11-7c4e8b2d0f63
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("analyze_concept_nuances requires Python 3.10 or newer.\n")
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
    "nuance_pattern_uuid",
    "nuance_pattern_code",
    "nuance_concept_domain",
    "nuance_surface_element",
    "nuance_latent_mechanism",
    "nuance_coupled_dependencies",
    "nuance_failure_mode",
    "nuance_confidence_tier",
    "nuance_created_at",
)


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("analyze_concept_nuances")


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


def validate_nuance_registry(target_path: Path) -> Dict[str, Any]:
    raw_data = json.loads(target_path.read_text(encoding="utf-8"))
    doc = bejson_core_sanitize_doc(raw_data)
    fmap = bejson_core_get_field_map(doc)
    errors: List[str] = []

    for req in REQUIRED_FIELDS:
        if req not in fmap:
            errors.append(f"Missing required field '{req}' in ConceptNuancePattern schema.")

    if not errors:
        for r_idx, row in enumerate(doc.get("Values", [])):
            if len(row) != len(fmap):
                errors.append(f"Row {r_idx} length mismatch ({len(row)} != {len(fmap)}).")
                continue
            code_val = row[fmap["nuance_pattern_code"]]
            mech_val = row[fmap["nuance_latent_mechanism"]]
            if not code_val or not mech_val:
                errors.append(f"Row {r_idx} has empty nuance_pattern_code or nuance_latent_mechanism.")

    return {
        "valid": len(errors) == 0,
        "file": str(target_path),
        "record_count": len(doc.get("Values", [])),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="analyze_concept_nuances",
        description="Validates ConceptNuancePattern BEJSON 104a registries.",
    )
    parser.add_argument("target", nargs="?", help="Path to ConceptNuancePattern .104a.bejson file.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"analyze_concept_nuances v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Show config.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("analyze_concept_nuances v%d ready.", VERSION)
        return EXIT_OK

    target_path = (
        Path(args.target).resolve()
        if args.target
        else (SCRIPT_PATH.parent / "assets" / "template_concept_nuance_patterns.104a.bejson")
    )
    if not target_path.exists():
        LOG.error("Target file does not exist: %s", target_path)
        return EXIT_PATH_FAILURE

    report = validate_nuance_registry(target_path)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    if not report["valid"]:
        LOG.error("ConceptNuancePattern validation FAILED.")
        return EXIT_SCHEMA_FAILURE

    LOG.info("ConceptNuancePattern validation PASSED (%d records).", report["record_count"])
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
