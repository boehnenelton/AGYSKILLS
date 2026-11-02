#!/usr/bin/env python3
"""
Name:           council_plan_validator
File:           council_plan_validator.py
Description:    Deterministic Layer 5 validator and formatter for Council Advisory Plans
                (dev/council_advisory_plan.104a.bejson). Validates schema conformity,
                O(1) field map access, satisfaction status lifecycle ('Iterating',
                'Refining', 'Approved', 'Satisfied'), and council voice coverage.
Version:        100
Date Created:   2026-11-02
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  9b1f3c20-7a4e-4d82-8c33-2e6f7a8b9c01
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("council_plan_validator requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
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


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("council_plan_validator")

ALLOWED_SATISFACTION_STATUSES: Tuple[str, ...] = (
    "Iterating",
    "Refining",
    "Approved",
    "Satisfied",
)


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer sanitization per Policy Section 10.9."""
    if not isinstance(raw_doc, dict):
        return raw_doc
    clean_doc: Dict[str, Any] = {
        (k.strip() if isinstance(k, str) else k): v for k, v in raw_doc.items()
    }
    fields = clean_doc.get("Fields")
    if isinstance(fields, list):
        for fdef in fields:
            if isinstance(fdef, dict):
                for fkey in ("name", "type"):
                    if isinstance(fdef.get(fkey), str):
                        fdef[fkey] = fdef[fkey].strip()
    values = clean_doc.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for idx, val in enumerate(row):
                    if isinstance(val, str) and val and (val[0].isspace() or val[-1].isspace()):
                        row[idx] = val.strip()
    return clean_doc


def bejson_core_get_field_map(bejson_doc: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) lookup dictionary mapping field_name -> 0-based column index."""
    fields_list = bejson_doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}


def validate_council_plan(plan_path: Path) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Validates a Council Advisory Plan document."""
    errors: List[str] = []
    if not plan_path.exists():
        errors.append(f"Plan file not found: {plan_path}")
        return False, errors, {}

    try:
        raw_doc = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON parsing error: {exc}")
        return False, errors, {}

    doc = bejson_core_sanitize_doc(raw_doc)
    mandatory_keys = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")
    for mkey in mandatory_keys:
        if mkey not in doc:
            errors.append(f"Missing mandatory BEJSON header key: '{mkey}'")

    if doc.get("Format_Creator") != "Elton Boehnen":
        errors.append("Format_Creator must declare 'Elton Boehnen'.")

    fmap = bejson_core_get_field_map(doc)
    required_fields = [
        "plan_uuid",
        "plan_title",
        "iteration_cycle",
        "satisfaction_status",
        "council_perspectives",
        "strategic_suggestions",
        "target_file_scope",
        "negative_guardrails",
        "definition_of_done",
    ]
    for rf in required_fields:
        if rf not in fmap:
            errors.append(f"Missing required field in schema: '{rf}'")

    values = doc.get("Values", [])
    if not values or not isinstance(values[0], list):
        errors.append("Document Values array is empty or malformed.")
        return False, errors, {}

    row = values[0]
    expected_len = len(doc.get("Fields", []))
    if len(row) != expected_len:
        errors.append(f"Row column count ({len(row)}) != schema fields ({expected_len}).")

    parsed_plan: Dict[str, Any] = {}
    if not errors:
        for fname, idx in fmap.items():
            parsed_plan[fname] = row[idx]

        status = parsed_plan.get("satisfaction_status")
        if status not in ALLOWED_SATISFACTION_STATUSES:
            errors.append(
                f"Invalid satisfaction_status '{status}'. Allowed: {ALLOWED_SATISFACTION_STATUSES}"
            )

    is_valid = len(errors) == 0
    return is_valid, errors, parsed_plan


def format_plan_summary(plan: Dict[str, Any]) -> str:
    """Formats human-readable summary of the council plan."""
    lines: List[str] = [
        "=" * 64,
        "COUNCIL ADVISORY PLAN DOSSIER",
        "=" * 64,
        f"Plan Title:          {plan.get('plan_title', 'Untitled')}",
        f"Plan UUID:           {plan.get('plan_uuid', 'N/A')}",
        f"Iteration Cycle:     #{plan.get('iteration_cycle', 1)}",
        f"Satisfaction Status: {plan.get('satisfaction_status', 'Unknown')}",
        f"Updated At:          {plan.get('updated_at', 'N/A')}",
        f"Grounding Ref:       {plan.get('grounding_state_ref', 'N/A')}",
        "-" * 64,
        "COUNCIL PERSPECTIVES:",
    ]
    try:
        perspectives = json.loads(plan.get("council_perspectives", "{}"))
        for voice, pos in perspectives.items():
            lines.append(f"  * {voice}: {pos}")
    except Exception:
        lines.append(f"  {plan.get('council_perspectives')}")

    lines.append("-" * 64)
    lines.append("STRATEGIC SUGGESTIONS:")
    try:
        suggestions = json.loads(plan.get("strategic_suggestions", "[]"))
        for idx, s in enumerate(suggestions, 1):
            lines.append(f"  {idx}. {s}")
    except Exception:
        lines.append(f"  {plan.get('strategic_suggestions')}")

    lines.append("-" * 64)
    lines.append(f"Target File Scope:   {plan.get('target_file_scope')}")
    lines.append(f"Negative Guardrails: {plan.get('negative_guardrails')}")
    lines.append(f"Definition of Done:  {plan.get('definition_of_done')}")
    lines.append(f"Handoff Skills:      {plan.get('handoff_skills')}")
    lines.append("=" * 64)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Council Plan Validator: validates BEJSON 104a council advisory plans."
    )
    parser.add_argument("plan_file", type=Path, help="Path to council_advisory_plan.104a.bejson")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    args = parser.parse_args()

    is_valid, errors, plan = validate_council_plan(args.plan_file)

    if args.json:
        result = {"valid": is_valid, "errors": errors, "plan": plan}
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if is_valid:
            print(format_plan_summary(plan))
            LOG.info("Council advisory plan is valid.")
        else:
            print("Validation FAILED with errors:")
            for e in errors:
                print(f"  [ERROR] {e}")

    return EXIT_OK if is_valid else EXIT_SCHEMA_FAILURE


if __name__ == "__main__":
    sys.exit(main())
