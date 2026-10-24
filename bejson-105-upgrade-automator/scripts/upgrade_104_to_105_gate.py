#!/usr/bin/env python3
"""
Name: upgrade_104_to_105_gate.py
Description: Layer 3 cross-era atomic migration script wrapping libraries_105
             lib_bejson_Core_bejson_upgrade.py. Executes bejson_core_upgrade_dry_run() first,
             backs up the 104/104a/104db source file verbatim to Backups/<filename>.104.bak,
             compiles UUIDv4 field_uuid and record_uuid columns, validates against E90-E95,
             and atomically swaps via .105tmp + os.fsync + os.replace.
Version: 100
Release_Version: 300
Date Created: 2026-10-17
Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: e816c309-2b74-4f11-8d39-5a09d4c17e62
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("upgrade_104_to_105_gate requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "e816c309-2b74-4f11-8d39-5a09d4c17e62"

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
LOG = logging.getLogger("upgrade_104_to_105_gate")


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
        if (cand / "lib_bejson_Core_bejson_upgrade.py").exists():
            return cand

    raise FileNotFoundError("Unable to locate libraries_105/Lib_PY/Core/lib_bejson_Core_bejson_upgrade.py")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="upgrade_104_to_105_gate",
        description="Sanctioned atomic upgrader from BEJSON 104/104a/104db to Format 105/105a/105db.",
    )
    parser.add_argument("target", nargs="?", help="Path to 104, 104a, or 104db file to upgrade.")
    parser.add_argument("--dry-run", action="store_true", help="Run in-memory 105 build and E90-E95 check without touching disk.")
    parser.add_argument("--version", action="version", version=f"upgrade_104_to_105_gate v{VERSION} (Release {RELEASE_VERSION})")
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
        LOG.error("Source file not found: %s", target_path)
        return EXIT_PATH_FAILURE

    try:
        lib_105_core = resolve_libraries_105_core()
    except FileNotFoundError as exc:
        LOG.error("Environment sourcing failure: %s", exc)
        return EXIT_ENV_FAILURE

    sys.path.insert(0, str(lib_105_core))
    from lib_bejson_Core_bejson_upgrade import (  # type: ignore
        bejson_core_upgrade_dry_run,
        bejson_core_upgrade_to_105,
        BEJSONUpgradeError,
    )

    try:
        raw_doc = bejson_boundary_sanitize(json.loads(target_path.read_text(encoding="utf-8")))
    except Exception as exc:
        LOG.error("E01 E_INVALID_JSON in %s: %s", target_path.name, exc)
        return EXIT_SCHEMA_FAILURE

    try:
        dry_report = bejson_core_upgrade_dry_run(raw_doc, str(target_path))
    except BEJSONUpgradeError as exc:
        LOG.error("Upgrade dry-run failed for %s: %s", target_path.name, exc)
        return EXIT_SCHEMA_FAILURE

    if not dry_report.get("validation_pass"):
        sys.stdout.write(json.dumps(dry_report, indent=2) + "\n")
        LOG.error("Dry-run validation failed with errors: %s", dry_report.get("errors"))
        return EXIT_SCHEMA_FAILURE

    if args.dry_run:
        sys.stdout.write(json.dumps(dry_report, indent=2) + "\n")
        LOG.info(
            "Dry-run PASSED for %s (%s -> %s, %d fields, %d records).",
            target_path.name,
            raw_doc.get("Format_Version"),
            dry_report["target_version"],
            dry_report["field_count"],
            dry_report["record_count"],
        )
        return EXIT_OK

    try:
        upgraded_doc = bejson_core_upgrade_to_105(raw_doc, str(target_path))
    except BEJSONUpgradeError as exc:
        LOG.error("Atomic upgrade failed for %s: %s", target_path.name, exc)
        return EXIT_SCHEMA_FAILURE

    backup_path = target_path.parent / "Backups" / f"{target_path.name}.104.bak"
    result_payload = {
        "upgraded": True,
        "source_path": str(target_path),
        "backup_path": str(backup_path),
        "previous_version": raw_doc.get("Format_Version"),
        "new_version": upgraded_doc.get("Format_Version"),
        "field_count": len(upgraded_doc.get("Fields", [])),
        "record_count": len(upgraded_doc.get("Values", [])),
    }
    sys.stdout.write(json.dumps(result_payload, indent=2) + "\n")
    LOG.info(
        "Atomic upgrade COMPLETED: %s (%s -> %s, backup=%s).",
        target_path.name,
        raw_doc.get("Format_Version"),
        upgraded_doc.get("Format_Version"),
        backup_path.name,
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
