#!/usr/bin/env python3
"""
Name:           validate_master_keymap_105.py
Description:    Layer 2 Cross-Entity Referential Integrity and MasterKeyMap Validator for MFDB v1.40.
                Enforces E39 (E_MFDB_UNRESOLVED_FK) across all foreign key (_fk) columns referencing
                parent entity primary keys, validates Integrity Era E90-E95 UUID constraints,
                fk_on_delete policy declarations, and Web Crypto ENC:AES-GCM encrypted cell tags.
Version:        100
Release_Version: 300
Date Created:   2026-10-24
Author Credit:  Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  5e105000-0001-4000-8000-000000000001
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("validate_master_keymap_105 requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import base64
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "5e105000-0001-4000-8000-000000000001"

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

E_MFDB_MANIFEST_MISSING: int = 30
E_MFDB_TABLE_MISSING: int = 31
E_MFDB_UNRESOLVED_FK: int = 39
E_105_FIELD_UUID_MISSING: int = 90
E_105_RECORD_UUID_MISSING: int = 92
E_MFDB_ENCRYPTION_MALFORMED: int = 96

UUID_REGEX = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)
AES_GCM_TAG_REGEX = re.compile(r"^ENC:AES-GCM:([A-Za-z0-9+/=]+):([A-Za-z0-9+/=]+):([A-Za-z0-9+/=]+)$")
ALLOWED_ON_DELETE: Set[str] = {"cascade", "null", "default", "restrict"}


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
LOG = logging.getLogger("validate_master_keymap_105")


def bejson_boundary_sanitize(raw: Any) -> Any:
    """Strip boundary whitespace on keys and string values per Policy §10.9."""
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
                ["master_lib_source", "$ADMIN_LIBRARIES_105", "Fallback master library directory for Integrity Era."],
                ["log_level", "INFO", "Default operational log level."],
                ["enforce_fk_referential_integrity", "true", "Enforce E39 E_MFDB_UNRESOLVED_FK on all foreign keys."],
                ["verify_cell_encryption", "true", "Verify ENC:AES-GCM format tags on encrypted cells."],
            ],
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, indent=2) + "\n", encoding="utf-8")
    return bejson_boundary_sanitize(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))


def is_valid_uuid(val: Any) -> bool:
    if not isinstance(val, str):
        return False
    return bool(UUID_REGEX.match(val.strip()))


def validate_encrypted_cell(cell_value: str) -> bool:
    """Validate ENC:AES-GCM:<salt_b64>:<iv_b64>:<ciphertext_b64> format and base64 payloads."""
    match = AES_GCM_TAG_REGEX.match(cell_value)
    if not match:
        return False
    salt_b64, iv_b64, ct_b64 = match.groups()
    try:
        base64.b64decode(salt_b64)
        base64.b64decode(iv_b64)
        base64.b64decode(ct_b64)
        return True
    except Exception:
        return False


def load_bejson_file(file_path: Path) -> Tuple[Optional[dict[str, Any]], Optional[str]]:
    if not file_path.is_file():
        return None, f"File not found: {file_path}"
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return bejson_boundary_sanitize(data), None
    except Exception as exc:
        return None, f"JSON parse error in {file_path}: {exc}"


def audit_mfdb_v140_database(db_root: Path, manifest_file: Optional[Path] = None) -> Tuple[bool, list[str]]:
    """
    Audit an entire MFDB v1.40 database for:
    1. Central manifest discovery and entity registration.
    2. Format 105 UUID integrity (field_uuid and row-0 record_uuid).
    3. Cross-entity FK referential integrity (E39).
    4. fk_on_delete conformance.
    5. Web Crypto ENC:AES-GCM cell format verification.
    """
    errors: list[str] = []

    # 1. Manifest Discovery
    if manifest_file and manifest_file.is_file():
        target_manifest = manifest_file
    else:
        manifest_candidates = [
            db_root / "105a.mfdb.bejson",
            db_root / "104a.mfdb.bejson",
            db_root / "manifest.104a.bejson",
            db_root / "mfdb.bejson",
        ]
        target_manifest = None
        for cand in manifest_candidates:
            if cand.is_file():
                target_manifest = cand
                break

    if not target_manifest or not target_manifest.is_file():
        return False, [f"MFDB root manifest not found in {db_root} (checked 105a.mfdb.bejson, 104a.mfdb.bejson)."]

    manifest_doc, err = load_bejson_file(target_manifest)
    if err or not manifest_doc:
        return False, [f"Manifest error: {err}"]

    fmap_manifest = bejson_get_field_map(manifest_doc)
    rel_path_col = fmap_manifest.get("relative_path") or fmap_manifest.get("Relative_Path") or fmap_manifest.get("table_path")
    table_name_col = fmap_manifest.get("table_name") or fmap_manifest.get("Table_Name") or fmap_manifest.get("entity_name")

    if rel_path_col is None:
        return False, ["Manifest Fields missing required relative_path / Relative_Path column."]

    # 2. Load all entity tables
    loaded_entities: dict[str, dict[str, Any]] = {}
    entity_pks: dict[str, set[str]] = {}
    entity_records_map: dict[str, list[dict[str, Any]]] = {}

    for row in manifest_doc.get("Values", []):
        rel_path_str = str(row[rel_path_col]).strip() if row[rel_path_col] else ""
        tname = str(row[table_name_col]).strip() if (table_name_col is not None and row[table_name_col]) else Path(rel_path_str).stem
        entity_file = (db_root / rel_path_str).resolve()

        if not entity_file.is_file():
            errors.append(f"MFDB entity file declared in manifest not found on disk: {entity_file} (Table: {tname})")
            continue

        edoc, e_err = load_bejson_file(entity_file)
        if e_err or not edoc:
            errors.append(f"Entity table load failed for {entity_file}: {e_err}")
            continue

        loaded_entities[tname] = edoc
        fmap_entity = bejson_get_field_map(edoc)
        version = edoc.get("Format_Version")

        # In 105/105a: row[0] is record_uuid.
        # Primary key is either record_uuid or an id column ending in _id / _uuid
        pks: set[str] = set()
        records: list[dict[str, Any]] = []

        is_105_era = version in ("105", "105a", "105db")

        # Check field_uuid definitions in 105 era
        if is_105_era:
            for fld in edoc.get("Fields", []):
                if isinstance(fld, dict):
                    fname = fld.get("name", "")
                    fuuid = fld.get("field_uuid")
                    if not fuuid:
                        errors.append(f"{tname} (E90): Field '{fname}' missing mandatory 'field_uuid'.")
                    elif not is_valid_uuid(fuuid):
                        errors.append(f"{tname} (E91): Field '{fname}' has invalid 'field_uuid' '{fuuid}'.")

        for r_idx, erow in enumerate(edoc.get("Values", [])):
            if not isinstance(erow, list):
                continue

            rec_dict: dict[str, Any] = {}
            if is_105_era:
                rec_uuid = erow[0] if len(erow) > 0 else None
                if not is_valid_uuid(rec_uuid):
                    errors.append(f"{tname} row {r_idx} (E92): Invalid or missing record_uuid at index 0: '{rec_uuid}'")
                elif rec_uuid:
                    pks.add(str(rec_uuid).strip().lower())
                    rec_dict["record_uuid"] = str(rec_uuid).strip().lower()

                # Map data columns (+1 offset for 105)
                for fname, cidx in fmap_entity.items():
                    data_idx = cidx + 1 if is_105_era else cidx
                    if data_idx < len(erow):
                        rec_dict[fname] = erow[data_idx]
            else:
                for fname, cidx in fmap_entity.items():
                    if cidx < len(erow):
                        rec_dict[fname] = erow[cidx]
                id_val = rec_dict.get("id") or rec_dict.get(f"{tname}_id")
                if id_val:
                    pks.add(str(id_val).strip().lower())

            records.append(rec_dict)

        entity_pks[tname] = pks
        entity_records_map[tname] = records

    # 3. Cross-Entity FK Referential Integrity Audit (E39)
    for tname, records in entity_records_map.items():
        edoc = loaded_entities[tname]
        fields = edoc.get("Fields", [])

        # Find all _fk fields
        fk_fields: list[dict[str, Any]] = []
        for fld in fields:
            if isinstance(fld, dict):
                fname = fld.get("name", "")
                if fname.endswith("_fk") or fld.get("fk_target_entity"):
                    fk_fields.append(fld)

        for fk_def in fk_fields:
            fname = fk_def.get("name", "")
            target_entity = fk_def.get("fk_target_entity")
            on_delete = fk_def.get("fk_on_delete")

            if on_delete and on_delete not in ALLOWED_ON_DELETE:
                errors.append(
                    f"{tname}.{fname}: Invalid fk_on_delete policy '{on_delete}'. Allowed: {ALLOWED_ON_DELETE}"
                )

            # Infer target entity if omitted
            if not target_entity:
                clean_target = fname[:-3]  # strip _fk
                # Match against known entity table names
                matched_target = None
                for cand in entity_pks.keys():
                    if cand.lower() == clean_target.lower() or cand.lower().startswith(clean_target.lower()):
                        matched_target = cand
                        break
                target_entity = matched_target

            if not target_entity or target_entity not in entity_pks:
                errors.append(
                    f"{tname}.{fname} (E39): Cannot resolve target entity for foreign key '{fname}' (inferred target: '{target_entity}')."
                )
                continue

            parent_valid_pks = entity_pks[target_entity]

            for r_idx, rec in enumerate(records):
                fk_val = rec.get(fname)
                if fk_val is None or fk_val == "":
                    continue  # Null FK is permitted unless nullable=false

                clean_fk = str(fk_val).strip().lower()
                if clean_fk not in parent_valid_pks:
                    errors.append(
                        f"{tname} row {r_idx} (E39 E_MFDB_UNRESOLVED_FK): Field '{fname}' references non-existent parent PK '{fk_val}' in '{target_entity}'."
                    )

        # 4. Check encrypted cells
        for r_idx, rec in enumerate(records):
            for col_name, cell_val in rec.items():
                if isinstance(cell_val, str) and cell_val.startswith("ENC:AES-GCM:"):
                    if not validate_encrypted_cell(cell_val):
                        errors.append(
                            f"{tname} row {r_idx} col '{col_name}' (E96): Malformed ENC:AES-GCM encryption payload."
                        )

    is_valid = len(errors) == 0
    return is_valid, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_master_keymap_105",
        description="Layer 2 Cross-Entity Referential Integrity and MasterKeyMap Validator for MFDB v1.40.",
    )
    parser.add_argument("target", nargs="?", help="Path to MFDB database root directory or manifest file.")
    parser.add_argument("--manifest", help="Explicit path to manifest file (105a.mfdb.bejson / 104a.mfdb.bejson).")
    parser.add_argument("--version", action="version", version=f"validate_master_keymap_105 v{VERSION} (Release {RELEASE_VERSION})")
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

    db_root = target_path if target_path.is_dir() else target_path.parent
    manifest_path = Path(args.manifest).resolve() if args.manifest else (target_path if target_path.is_file() else None)

    valid, errors = audit_mfdb_v140_database(db_root, manifest_file=manifest_path)
    if not valid:
        LOG.error("MFDB v1.40 referential integrity validation failed (%d error(s)):", len(errors))
        for err in errors:
            LOG.error("  - %s", err)
        return EXIT_SCHEMA_FAILURE

    LOG.info("MFDB v1.40 referential integrity valid: 100%% cross-entity foreign keys resolved cleanly.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
