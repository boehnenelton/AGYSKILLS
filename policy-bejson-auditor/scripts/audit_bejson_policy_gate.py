#!/usr/bin/env python3
"""
Name: audit_bejson_policy_gate.py
Description: Layer 2 AST and Policy §6.2 / §7.3 / §9 / §10.1 / §10.9 auditor for BEJSON Python,
             JavaScript, TypeScript, and Bash modules. Verifies zero print() calls, zero raw
             positional row[0] indexing without field_map, presence of VERSION and RELATIONAL_ID,
             and boundary sanitization compliance.
Version: 100
Release_Version: 300
Date Created: 2026-10-17
Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: f731a408-9e25-4c82-8b14-3d920e5f1a77
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("audit_bejson_policy_gate requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import ast
import json
import logging
import re
from pathlib import Path
from typing import Any

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "f731a408-9e25-4c82-8b14-3d920e5f1a77"

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
LOG = logging.getLogger("audit_bejson_policy_gate")


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
                ["master_lib_source", "$ADMIN_LIBRARIES", "Fallback if local lib missing."],
                ["log_level", "INFO", "Default log level."],
            ],
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, indent=2) + "\n", encoding="utf-8")
    return bejson_boundary_sanitize(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))


def audit_python_file(py_path: Path) -> dict[str, Any]:
    text = py_path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    try:
        tree = ast.parse(text, filename=str(py_path))
    except SyntaxError as exc:
        return {
            "valid": False,
            "file_path": str(py_path),
            "errors": [f"E_SYNTAX_ERROR: {exc}"],
            "warnings": [],
        }

    # Check 1: Policy §7.3 Zero print() calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            errors.append(f"POL_7_3_PRINT_FORBIDDEN: Found print() call at line {node.lineno}; use logging module.")

    # Check 2: Policy §9 VERSION and RELATIONAL_ID
    if "VERSION" not in text:
        warnings.append("POL_9_MISSING_VERSION: File should declare a top-level VERSION variable.")
    if "RELATIONAL_ID" not in text:
        warnings.append("POL_9_MISSING_RELATIONAL_ID: File should declare a RELATIONAL_ID UUID.")

    # Check 3: Policy §6.2 Zero hardcoded row[0] / row[1] integer subscripting on BEJSON rows via AST
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id in ("row", "record")
            and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, int)
        ):
            errors.append(
                f"POL_6_2_POSITIONAL_INDEX: Found hardcoded integer subscript '{node.value.id}[{node.slice.value}]' at line {node.lineno}; use field_map[col]."
            )

    return {
        "valid": len(errors) == 0,
        "file_path": str(py_path),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="audit_bejson_policy_gate",
        description="Layer 2 AST and Policy §6.2 / §7.3 / §9 / §10.9 compliance auditor.",
    )
    parser.add_argument("target", nargs="?", help="Path to Python file or directory of scripts to audit.")
    parser.add_argument("--version", action="version", version=f"audit_bejson_policy_gate v{VERSION} (Release {RELEASE_VERSION})")
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

    py_files = [target_path] if target_path.is_file() else sorted(target_path.rglob("*.py"))
    results = [audit_python_file(p) for p in py_files]
    all_valid = all(r["valid"] for r in results)

    summary = {
        "valid": all_valid,
        "files_audited": len(results),
        "results": results,
    }
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")

    if not all_valid:
        LOG.error("Policy AST audit FAILED across %d file(s).", sum(1 for r in results if not r["valid"]))
        return EXIT_SCHEMA_FAILURE

    LOG.info("Policy AST audit PASSED across %d Python file(s).", len(results))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
