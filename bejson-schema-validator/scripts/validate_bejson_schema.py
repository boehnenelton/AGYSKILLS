#!/usr/bin/env python3
"""
Name:           validate_bejson_schema.py
Description:    Layer 2 Era-Neutral Stage-Gate Validator and Dispatcher for BEJSON Documents.
                Inspects Format_Version and routes validation across Foundational Era (104, 104a, 104db)
                and Integrity Era (105, 105a, 105db) invariants. Supports standalone execution with
                embedded validation primitives and dynamic library discovery.
Version:        100
Release_Version: 300
Date Created:   2026-10-24
Author Credit:  Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  b201a000-0001-4000-8000-000000000001
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("validate_bejson_schema requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "b201a000-0001-4000-8000-000000000001"

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

MANDATORY_KEYS: Set[str] = {
    "Format",
    "Format_Version",
    "Format_Creator",
    "Records_Type",
    "Fields",
    "Values",
}

VALID_104_VERSIONS: Set[str] = {"104", "104a", "104db"}
VALID_105_VERSIONS: Set[str] = {"105", "105a", "105db"}
ALL_VALID_VERSIONS: Set[str] = VALID_104_VERSIONS | VALID_105_VERSIONS

VALID_FIELD_TYPES: Set[str] = {
    "string",
    "integer",
    "number",
    "boolean",
    "array",
    "object",
    "any",
}
PRIMITIVE_TYPES: Set[str] = {"string", "integer", "number", "boolean"}

UUID_REGEX = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


def get_script_path() -> Path:
    """Self-locating script path per Policy §4.1."""
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()
BUNDLE_ROOT: Path = SCRIPT_PATH.parent
CONFIG_PATH: Path = BUNDLE_ROOT / "config" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("validate_bejson_schema")


def bejson_boundary_sanitize(raw: Any) -> Any:
    """Strip boundary whitespace on dictionary keys and string values per Policy §10.9."""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        return [bejson_boundary_sanitize(item) for item in raw]
    if isinstance(raw, dict):
        return {str(k).strip(): bejson_boundary_sanitize(v) for k, v in raw.items()}
    return raw


def bejson_get_field_map(doc: dict[str, Any]) -> dict[str, int]:
    """Compile O(1) field name to column index map per Policy §6.2."""
    fields = doc.get("Fields", [])
    field_map: dict[str, int] = {}
    for idx, field_def in enumerate(fields):
        if isinstance(field_def, dict) and "name" in field_def:
            clean_name = str(field_def["name"]).strip()
            field_map[clean_name] = idx
    return field_map


def ensure_config_104a() -> dict[str, Any]:
    """Generate or load BEJSON 104a ScriptConfig per Policy §4.4."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_cfg = {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": ["ScriptConfig"],
            "Fields": [
                {"name": "setting_name", "type": "string"},
                {"name": "setting_value", "type": "string"},
                {"name": "description", "type": "string"},
            ],
            "Values": [
                ["local_lib_directory", "lib/", "Relative path to local dep folder."],
                ["master_lib_source", "$ADMIN_LIBRARIES", "Fallback master library directory."],
                ["log_level", "INFO", "Default operational log level."],
                ["strict_mode", "true", "Enforce strict era-specific validation rules."],
            ],
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, indent=2) + "\n", encoding="utf-8")
    return bejson_boundary_sanitize(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))


def is_valid_uuid(val: Any) -> bool:
    """Validate string representation of UUID."""
    if not isinstance(val, str):
        return False
    return bool(UUID_REGEX.match(val.strip()))


def validate_field_type(val: Any, expected_type: str) -> bool:
    """Type check a cell value against declared BEJSON field type."""
    if val is None:
        return True
    if expected_type == "string":
        return isinstance(val, str)
    if expected_type == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if expected_type == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if expected_type == "boolean":
        return isinstance(val, bool)
    if expected_type == "array":
        return isinstance(val, list)
    if expected_type == "object":
        return isinstance(val, dict)
    if expected_type == "any":
        return True
    return False


def validate_bejson_document(raw_doc: Any, target_label: str = "<memory>") -> Tuple[bool, list[str]]:
    """
    Era-neutral validator logic:
    Checks mandatory keys, format integrity, and era-specific invariants.
    """
    errors: list[str] = []

    if not isinstance(raw_doc, dict):
        return False, [f"{target_label}: Root payload must be a JSON object."]

    doc = bejson_boundary_sanitize(raw_doc)

    # 1. Mandatory top-level keys
    for k in MANDATORY_KEYS:
        if k not in doc:
            errors.append(f"{target_label}: Missing mandatory key '{k}'.")

    if errors:
        return False, errors

    # 2. Format & Creator
    if doc.get("Format") != "BEJSON":
        errors.append(f"{target_label}: 'Format' must be 'BEJSON', got '{doc.get('Format')}'.")

    creator = doc.get("Format_Creator")
    if not isinstance(creator, str) or not creator.strip():
        errors.append(f"{target_label}: 'Format_Creator' must be a non-empty string.")

    # 3. Format_Version check
    version = str(doc.get("Format_Version", "")).strip()
    if version not in ALL_VALID_VERSIONS:
        errors.append(
            f"{target_label}: Unsupported 'Format_Version' '{version}'. Allowed: {sorted(ALL_VALID_VERSIONS)}."
        )
        return False, errors

    # 4. Records_Type check
    records_type = doc.get("Records_Type")
    if not isinstance(records_type, list) or not records_type:
        errors.append(f"{target_label}: 'Records_Type' must be a non-empty array of record type names.")

    # 5. Fields schema check
    fields = doc.get("Fields")
    if not isinstance(fields, list):
        errors.append(f"{target_label}: 'Fields' must be an array.")
        return False, errors

    field_names: list[str] = []
    field_types: list[str] = []
    field_uuids: list[str] = []

    is_105_era = version in VALID_105_VERSIONS
    is_104a = version == "104a"
    is_105a = version == "105a"
    is_db = version in {"104db", "105db"}

    for idx, fld in enumerate(fields):
        if not isinstance(fld, dict):
            errors.append(f"{target_label}: Field at index {idx} must be an object.")
            continue
        fname = fld.get("name")
        ftype = fld.get("type")
        if not isinstance(fname, str) or not fname.strip():
            errors.append(f"{target_label}: Field at index {idx} missing valid 'name'.")
        else:
            clean_name = fname.strip()
            if clean_name.startswith("_"):
                errors.append(f"{target_label}: Field '{clean_name}' cannot start with reserved '_' (E10).")
            field_names.append(clean_name)

        if ftype not in VALID_FIELD_TYPES:
            errors.append(f"{target_label}: Field '{fname}' has invalid type '{ftype}'.")
        else:
            field_types.append(ftype)
            # POL-002: 104a and 105a require primitive types only
            if (is_104a or is_105a) and ftype not in PRIMITIVE_TYPES:
                errors.append(
                    f"{target_label}: Format {version} Field '{fname}' must be primitive ({PRIMITIVE_TYPES}), got '{ftype}'."
                )

        # 105 Era Integrity invariants: E90/E91 field_uuid
        if is_105_era:
            fuuid = fld.get("field_uuid")
            if not fuuid:
                errors.append(f"{target_label}: Integrity Era field '{fname}' missing mandatory 'field_uuid' (E90).")
            elif not is_valid_uuid(fuuid):
                errors.append(f"{target_label}: Field '{fname}' field_uuid '{fuuid}' is not a valid UUIDv4 (E91).")
            else:
                clean_uuid = str(fuuid).strip().lower()
                if clean_uuid in field_uuids:
                    errors.append(f"{target_label}: Duplicate field_uuid '{clean_uuid}' detected on '{fname}' (E91).")
                field_uuids.append(clean_uuid)

    # Check duplicate field names
    if len(field_names) != len(set(field_names)):
        errors.append(f"{target_label}: Duplicate field names detected in 'Fields'.")

    # 6. Values records check
    values = doc.get("Values")
    if not isinstance(values, list):
        errors.append(f"{target_label}: 'Values' must be an array.")
        return False, errors

    expected_data_len = len(fields)
    record_uuids: set[str] = set()

    for r_idx, row in enumerate(values):
        if not isinstance(row, list):
            errors.append(f"{target_label}: Row {r_idx} in 'Values' must be an array.")
            continue

        # Format 104 / 104a
        if version in {"104", "104a"}:
            if len(row) != expected_data_len:
                errors.append(
                    f"{target_label}: Row {r_idx} length {len(row)} does not match Fields count {expected_data_len}."
                )
            else:
                for c_idx, cell in enumerate(row):
                    if not validate_field_type(cell, field_types[c_idx]):
                        errors.append(
                            f"{target_label}: Row {r_idx} col {c_idx} ('{field_names[c_idx]}') type mismatch: expected {field_types[c_idx]}, got {type(cell).__name__}."
                        )

        # Format 104db: Row has [Record_Type_Parent, ...fields]
        elif version == "104db":
            if len(row) != expected_data_len + 1:
                errors.append(
                    f"{target_label}: 104db Row {r_idx} length {len(row)} must be {expected_data_len + 1} (discriminator + fields)."
                )
            else:
                parent_disc = row[0]
                if not isinstance(parent_disc, str) or parent_disc not in records_type:
                    errors.append(
                        f"{target_label}: 104db Row {r_idx} discriminator '{parent_disc}' not in Records_Type {records_type}."
                    )
                for c_idx, cell in enumerate(row[1:]):
                    if not validate_field_type(cell, field_types[c_idx]):
                        errors.append(
                            f"{target_label}: 104db Row {r_idx} col {c_idx+1} ('{field_names[c_idx]}') type mismatch."
                        )

        # Format 105 / 105a: Row has [record_uuid, ...fields]
        elif version in {"105", "105a"}:
            if len(row) != expected_data_len + 1:
                errors.append(
                    f"{target_label}: 105 Row {r_idx} length {len(row)} must be {expected_data_len + 1} (record_uuid + fields)."
                )
            else:
                row_uuid = row[0]
                if not is_valid_uuid(row_uuid):
                    errors.append(
                        f"{target_label}: 105 Row {r_idx} index 0 must be a valid UUIDv4 record_uuid (E92), got '{row_uuid}'."
                    )
                else:
                    clean_ruuid = str(row_uuid).strip().lower()
                    if clean_ruuid in record_uuids:
                        errors.append(f"{target_label}: Duplicate record_uuid '{clean_ruuid}' at row {r_idx} (E93).")
                    record_uuids.add(clean_ruuid)

                for c_idx, cell in enumerate(row[1:]):
                    if not validate_field_type(cell, field_types[c_idx]):
                        errors.append(
                            f"{target_label}: 105 Row {r_idx} col {c_idx+1} ('{field_names[c_idx]}') type mismatch."
                        )

        # Format 105db: Row has [Record_Type_Parent, record_uuid, ...fields]
        elif version == "105db":
            if len(row) != expected_data_len + 2:
                errors.append(
                    f"{target_label}: 105db Row {r_idx} length {len(row)} must be {expected_data_len + 2}."
                )
            else:
                parent_disc = row[0]
                if not isinstance(parent_disc, str) or parent_disc not in records_type:
                    errors.append(
                        f"{target_label}: 105db Row {r_idx} discriminator '{parent_disc}' not in Records_Type."
                    )
                row_uuid = row[1]
                if not is_valid_uuid(row_uuid):
                    errors.append(
                        f"{target_label}: 105db Row {r_idx} index 1 must be a valid UUIDv4 record_uuid (E92)."
                    )
                for c_idx, cell in enumerate(row[2:]):
                    if not validate_field_type(cell, field_types[c_idx]):
                        errors.append(
                            f"{target_label}: 105db Row {r_idx} col {c_idx+2} ('{field_names[c_idx]}') type mismatch."
                        )

    return len(errors) == 0, errors


def validate_file(file_path: Path, expected_era: Optional[str] = None) -> bool:
    """Validate a single BEJSON file on disk."""
    if not file_path.is_file():
        LOG.error("Target file does not exist: %s", file_path)
        return False

    try:
        raw_text = file_path.read_text(encoding="utf-8")
        raw_doc = json.loads(raw_text)
    except Exception as exc:
        LOG.error("Failed to parse JSON in %s: %s", file_path, exc)
        return False

    version = raw_doc.get("Format_Version") if isinstance(raw_doc, dict) else None
    if expected_era:
        if expected_era == "104" and version not in VALID_104_VERSIONS:
            LOG.error("Expected Era 104 but file %s has Format_Version '%s'", file_path, version)
            return False
        if expected_era == "105" and version not in VALID_105_VERSIONS:
            LOG.error("Expected Era 105 but file %s has Format_Version '%s'", file_path, version)
            return False

    valid, errors = validate_bejson_document(raw_doc, target_label=str(file_path.name))
    if not valid:
        LOG.error("Validation failed for %s (%s errors):", file_path, len(errors))
        for err in errors:
            LOG.error("  - %s", err)
        return False

    LOG.info("Valid BEJSON (%s): %s [%d records]", version, file_path.name, len(raw_doc.get("Values", [])))
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_bejson_schema",
        description="Layer 2 Era-Neutral Stage-Gate Validator for BEJSON 104 and 105 Documents.",
    )
    parser.add_argument("target", nargs="?", help="Path to .bejson file or directory of BEJSON files.")
    parser.add_argument("--expected-era", choices=["104", "105"], help="Enforce specific era (104 or 105).")
    parser.add_argument("--version", action="version", version=f"validate_bejson_schema v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Display project registration command.")
    parser.add_argument("--config", action="store_true", help="Initialize and display 104a ScriptConfig.")
    parser.add_argument("--reset", action="store_true", help="Reset config/config.json to canonical defaults.")

    args = parser.parse_args()
    if args.reset and CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
    cfg = ensure_config_104a()
    fmap = bejson_get_field_map(cfg)

    if args.config:
        settings = {row[fmap["setting_name"]]: row[fmap["setting_value"]] for row in cfg.get("Values", [])}
        LOG.info("Active 104a ScriptConfig: %s", json.dumps(settings))
        return EXIT_OK
    if args.register:
        LOG.info("Registration: python3 $PROJECT_INDEX_ROOT/cli_project_register.py --register \"%s\"", BUNDLE_ROOT)
        return EXIT_OK
    if not args.target:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        LOG.error("Target path not found: %s", target_path)
        return EXIT_PATH_FAILURE

    if target_path.is_file():
        files_to_check = [target_path]
    else:
        files_to_check = sorted(
            [p for p in target_path.rglob("*.bejson")]
        )
        if not files_to_check:
            LOG.warning("No .bejson files found in directory: %s", target_path)
            return EXIT_OK

    all_passed = True
    for f in files_to_check:
        if not validate_file(f, expected_era=args.expected_era):
            all_passed = False

    return EXIT_OK if all_passed else EXIT_SCHEMA_FAILURE


if __name__ == "__main__":
    sys.exit(main())
