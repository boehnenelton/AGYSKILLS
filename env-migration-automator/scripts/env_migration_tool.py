#!/usr/bin/env python3
"""
env_migration_tool.py
Layer 3 Environment Store Deprecation Migration Engine
Scans and migrates references from deprecated paths.json to canonical definitions.json.

Policy Anchors:
  Policy §4.5: Environment Sourcing Standards
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import difflib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_MIGRATION_ERROR = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_input_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def scan_and_migrate_file(
    file_path: Path,
    apply_changes_flag: bool = False,
) -> Optional[Dict[str, Any]]:
    """Scan file for paths.json references and produce migration diff or apply changes."""
    if not file_path.is_file():
        return None
    if file_path.suffix.lower() not in (".py", ".sh", ".json", ".md", ".txt", ".js", ".ts"):
        return None
    if any(part in file_path.parts for part in (".git", "__pycache__", ".bak")):
        return None

    try:
        original_content = file_path.read_text(encoding="utf-8")
        if "paths.json" not in original_content and "PATHS_FILE" not in original_content:
            return None

        # Replace occurrences
        migrated_content = original_content.replace("paths.json", "definitions.json")
        migrated_content = migrated_content.replace("PATHS_FILE", "DEFINITIONS_FILE")

        if migrated_content == original_content:
            return None

        # Generate unified diff
        diff_lines = list(
            difflib.unified_diff(
                original_content.splitlines(keepends=True),
                migrated_content.splitlines(keepends=True),
                fromfile=f"a/{file_path.name}",
                tofile=f"b/{file_path.name}",
            )
        )

        diff_summary = "".join(diff_lines)

        if apply_changes_flag:
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            file_path.rename(backup_path)
            file_path.write_text(migrated_content, encoding="utf-8")

        return {
            "file": str(file_path),
            "applied": apply_changes_flag,
            "diff": diff_summary,
        }

    except Exception:
        return None


def execute_migration_pipeline(
    target_path: Path,
    apply_changes_flag: bool = False,
) -> Dict[str, Any]:
    """Execute scan and migration across target path."""
    target_files = [target_path] if target_path.is_file() else list(target_path.rglob("*"))
    migration_results_list: List[Dict[str, Any]] = []

    for f in target_files:
        res = scan_and_migrate_file(f, apply_changes_flag=apply_changes_flag)
        if res:
            migration_results_list.append(res)

    return {
        "target": str(target_path),
        "migration_timestamp": get_current_utc_timestamp_iso(),
        "applied": apply_changes_flag,
        "total_files_affected": len(migration_results_list),
        "results": migration_results_list,
    }


def generate_migration_report_markdown(migration_data: Dict[str, Any]) -> str:
    """Generate Markdown report for migration results."""
    target_str = migration_data["target"]
    timestamp_str = migration_data["migration_timestamp"]
    applied_flag = migration_data["applied"]
    total_files = migration_data["total_files_affected"]

    mode_label = "MIGRATION_APPLIED" if applied_flag else "DRY_RUN_PREVIEW"

    report_lines: List[str] = [
        "# Environment Migration Report (paths.json -> definitions.json)",
        "",
        f"- **Target**: `{target_str}`",
        f"- **Timestamp**: `{timestamp_str}`",
        f"- **Execution Mode**: `{mode_label}`",
        f"- **Total Files Modified/Pending**: `{total_files}`",
        "",
        "## 1. File Diffs",
    ]

    results = migration_data.get("results", [])
    if not results:
        report_lines.append("Zero legacy paths.json references discovered. System is fully modernized.")
    else:
        for idx, res in enumerate(results, start=1):
            f_str = res["file"]
            diff_text = res["diff"]
            report_lines.append(f"### {idx}. `{f_str}`\n```diff\n{diff_text}\n```\n")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Environment Migration Automator tool."""
    argument_parser = argparse.ArgumentParser(
        description="env-migration-automator: Automates migration from deprecated paths.json to definitions.json."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to file or directory to scan/migrate (default: current directory).",
    )
    argument_parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply modifications with .bak backup preservation (default is dry-run).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Print markdown formatted report to stdout.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON results to stdout.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"env_migration_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_input_path(parsed_arguments.target)

    if not target_path.exists():
        sys.stderr.write(f"Error: Target path does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    try:
        migration_data = execute_migration_pipeline(
            target_path=target_path,
            apply_changes_flag=parsed_arguments.apply,
        )

        if parsed_arguments.json:
            print(json.dumps(migration_data, indent=2))
        else:
            report_text = generate_migration_report_markdown(migration_data)
            print(report_text)

        return EXIT_CLEAN_PASS

    except Exception as runtime_error:
        sys.stderr.write(f"Fatal error during environment migration: {runtime_error}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
