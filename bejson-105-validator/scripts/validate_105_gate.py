#!/usr/bin/env python3
"""
Name: validate_105_gate.py
Description: Layer 2 deterministic stage-gate validator for Integrity Era BEJSON 105, 105a,
             and 105db documents. Binds dynamically to libraries_105 (v3.5.3+), enforces E90-E95
             UUID integrity (field_uuid, record_uuid, and E95 Fail-on-Switch guard), self-maintaining
             by_name_row field_map cache verification, and boundary sanitization.
Version: 100
Release_Version: 300
Date Created: 2026-10-17
Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: d925b714-8a42-4e19-9c03-7b18e6f24a91
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("validate_105_gate requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "d925b714-8a42-4e19-9c03-7b18e6f24a91"

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()
BUNDLE_ROOT: Path = SCRIPT_PATH.parent
CONFIG_PATH: Path = BUNDLE_ROOT / "config" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("validate_105_gate")


def bejson_boundary_sanitize(raw: Any) -> Any:
    """Enforce Policy §10.9 boundary-layer whitespace stripping on keys and string values."""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        return [bejson_boundary_sanitize(item) for item in raw]
    if isinstance(raw, dict):
        return {str(k).strip(): bejson_boundary_sanitize(v) for k, v in raw.items()}
    return raw


def bejson_get_field_map(doc: dict[str, Any]) -> dict[str, int]:
    """Enforce Policy §6.2 mandatory O(1) Field Map Cache."""
    fields = doc.get("Fields", [])
    return {str(f["name"]).strip(): idx for idx, f in enumerate(fields) if isinstance(f, dict) and "name" in f}


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
                ["master_lib_source", "$ADMIN_LIBRARIES_105", "Fallback if local lib missing."],
                ["log_level", "INFO", "Default log level."],
            ],
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, indent=2) + "\n", encoding="utf-8")
    return bejson_boundary_sanitize(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))


def resolve_libraries_105_core() -> Path:
    """Resolve libraries_105/Lib_PY/Core dynamically via environment or relative workspace discovery."""
    env_lib = os.environ.get("ADMIN_LIBRARIES_105")
    candidates: list[Path] = []
    if env_lib:
        candidates.append(Path(env_lib) / "Lib_PY" / "Core")
        candidates.append(Path(env_lib) / "libraries_105" / "Lib_PY" / "Core")

    for parent in SCRIPT_PATH.parents:
        candidates.append(parent / "User" / "core" / "libraries" / "libraries_105" / "Lib_PY" / "Core")
        candidates.append(parent / "Admin" / "libraries" / "libraries_105" / "Lib_PY" / "Core")

    for cand in candidates:
        if (cand / "lib_bejson_Core_bejson_validator.py").exists():
            return cand

    raise FileNotFoundError("Unable to locate libraries_105/Lib_PY/Core/lib_bejson_Core_bejson_validator.py")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_105_gate",
        description="Layer 2 black-box stage-gate validator for BEJSON 105, 105a, and 105db documents.",
    )
    parser.add_argument("target", nargs="?", help="Path to .105.bejson / .105a.bejson / .105db.bejson file.")
    parser.add_argument("--expected-version", choices=["105", "105a", "105db"], help="Enforce exact 105 sub-variant.")
    parser.add_argument("--version", action="version", version=f"validate_105_gate v{VERSION} (Release {RELEASE_VERSION})")
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
    if not target_path.is_file():
        LOG.error("Target file not found: %s", target_path)
        return EXIT_PATH_FAILURE

    try:
        lib_105_core = resolve_libraries_105_core()
    except FileNotFoundError as exc:
        LOG.error("Environment sourcing failure: %s", exc)
        return EXIT_ENV_FAILURE

    sys.path.insert(0, str(lib_105_core))
    from lib_bejson_Core_bejson_validator import (  # type: ignore
        validate_bejson,
        bejson_validator_check_105_strict_integrity,
    )
    from lib_bejson_Core_bejson_core import bejson_core_get_field_map as get_105_field_map  # type: ignore

    try:
        raw_doc = json.loads(target_path.read_text(encoding="utf-8"))
    except Exception as exc:
        LOG.error("E01 E_INVALID_JSON in %s: %s", target_path.name, exc)
        return EXIT_SCHEMA_FAILURE

    fmt_ver = str(raw_doc.get("Format_Version", "")).strip()
    if fmt_ver in ("104", "104a", "104db"):
        LOG.error(
            "ERA_BOUNDARY_VIOLATION: '%s' has Format_Version='%s'. Use bejson-104-validator or upgrade via bejson-105-upgrade-automator.",
            target_path.name,
            fmt_ver,
        )
        return EXIT_SCHEMA_FAILURE

    if args.expected_version and fmt_ver != args.expected_version:
        LOG.error(
            "DIALECT_MISMATCH: Expected Format_Version='%s', got '%s' in %s.",
            args.expected_version,
            fmt_ver,
            target_path.name,
        )
        return EXIT_SCHEMA_FAILURE

    val_res = validate_bejson(str(target_path), is_file=True)
    strict_105_errors = bejson_validator_check_105_strict_integrity(raw_doc)
    combined_errors = list(val_res.errors)
    for err in strict_105_errors:
        if err not in combined_errors:
            combined_errors.append(err)

    row_fmap: dict[str, int] = {}
    if not combined_errors:
        row_fmap = get_105_field_map(raw_doc)

    report = {
        "valid": len(combined_errors) == 0 and bool(val_res.is_valid),
        "era": "libraries_105",
        "file_path": str(target_path),
        "format_version": fmt_ver,
        "field_count": len(raw_doc.get("Fields", [])) if isinstance(raw_doc.get("Fields"), list) else 0,
        "record_count": len(raw_doc.get("Values", [])) if isinstance(raw_doc.get("Values"), list) else 0,
        "by_name_row_map": row_fmap,
        "errors": combined_errors,
    }
    sys.stdout.write(json.dumps(report, indent=2) + "\n")

    if not report["valid"]:
        LOG.error("105 validation FAILED for %s with %d error(s).", target_path.name, len(combined_errors))
        return EXIT_SCHEMA_FAILURE

    LOG.info("105 validation PASSED for %s (Format_Version=%s, E90-E95 clean).", target_path.name, fmt_ver)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
