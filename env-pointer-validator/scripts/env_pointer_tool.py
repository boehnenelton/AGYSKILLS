#!/usr/bin/env python3
"""
env_pointer_tool.py
Layer 2 Policy §4.5 Pointer & Resolution Gate
Audits source code and configurations for hardcoded paths and verifies ENV:<var> pointer resolution.

Policy Anchors:
  Policy §4.5: Environment Sourcing Standards
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_VIOLATIONS_DETECTED = 30

DEFAULT_DEFINITIONS_PATH = Path("/storage/emulated/0/.env/user/definitions.json")


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_input_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def load_canonical_definitions_keys(definitions_file_path: Path) -> Set[str]:
    """Extract set of defined variable keys from definitions.json."""
    if not definitions_file_path.is_file():
        return set()
    try:
        with open(definitions_file_path, "r", encoding="utf-8") as file_read_handle:
            data = json.load(file_read_handle)
            values = data.get("Values", [])
            fields = data.get("Fields", [])
            key_names: Set[str] = set()

            if fields and values:
                field_names = [f["name"] if isinstance(f, dict) else str(f) for f in fields]
                name_idx = field_names.index("name") if "name" in field_names else 0
                for row in values:
                    if isinstance(row, list) and name_idx < len(row):
                        key_names.add(str(row[name_idx]))
            elif isinstance(data, dict):
                # Standard json dictionary fallback
                for k in data.keys():
                    key_names.add(k)
            return key_names
    except Exception:
        return set()


def audit_target_for_pointers_and_hardcodes(
    target_path: Path,
    known_definitions_keys: Set[str],
) -> Dict[str, Any]:
    """Scan target path for hardcoded paths and unresolvable ENV: pointers."""
    hardcoded_path_findings: List[Dict[str, Any]] = []
    pointer_findings: List[Dict[str, Any]] = []

    hardcoded_path_regex = re.compile(r"['\"](/storage/emulated/0/[^'\"]+)['\"]")
    pointer_token_regex = re.compile(r"ENV:([A-Za-z0-9_-]+)")

    files_to_scan = [target_path] if target_path.is_file() else list(target_path.rglob("*"))

    for single_file in files_to_scan:
        if not single_file.is_file():
            continue
        # Skip git, pycache, or definitions stores themselves
        if any(part in single_file.parts for part in (".git", "__pycache__", ".env")):
            continue
        if single_file.suffix.lower() not in (".py", ".sh", ".json", ".js", ".ts", ".md"):
            continue

        try:
            content_text = single_file.read_text(encoding="utf-8")
            rel_file_path = str(single_file.relative_to(target_path)) if target_path.is_dir() else single_file.name

            # 1. Hardcoded paths check (ignore markdown docs or references)
            if single_file.suffix.lower() in (".py", ".sh", ".json", ".js", ".ts"):
                for match in hardcoded_path_regex.finditer(content_text):
                    matched_path = match.group(1)
                    # Don't flag definitions.json path itself
                    if "definitions.json" not in matched_path and "secureenv_file" not in matched_path:
                        hardcoded_path_findings.append(
                            {
                                "file": rel_file_path,
                                "type": "HARDCODED_STORAGE_PATH",
                                "matched_string": matched_path,
                                "remediation": f"Replace hardcoded path '{matched_path}' with abstract ENV:<token> pointer.",
                            }
                        )

            # 2. Pointer resolution check
            for match in pointer_token_regex.finditer(content_text):
                token_name = match.group(1)
                is_resolved = token_name in known_definitions_keys
                if not is_resolved and len(known_definitions_keys) > 0:
                    pointer_findings.append(
                        {
                            "file": rel_file_path,
                            "type": "UNRESOLVED_POINTER",
                            "token": token_name,
                            "remediation": f"Register 'ENV:{token_name}' in definitions.json.",
                        }
                    )
        except Exception:
            pass

    has_violations = len(hardcoded_path_findings) > 0 or len(pointer_findings) > 0
    return {
        "target": str(target_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "has_violations": has_violations,
        "total_hardcoded_paths": len(hardcoded_path_findings),
        "total_unresolved_pointers": len(pointer_findings),
        "hardcoded_paths": hardcoded_path_findings,
        "unresolved_pointers": pointer_findings,
    }


def generate_pointer_report_markdown(audit_results: Dict[str, Any]) -> str:
    """Generate Markdown report for pointer audits."""
    target_str = audit_results["target"]
    timestamp_str = audit_results["audit_timestamp"]
    has_viol = audit_results["has_violations"]
    status_str = "VIOLATIONS_DETECTED" if has_viol else "CLEAN_COMPLIANT"

    report_lines: List[str] = [
        "# Environment Pointer Validation Report",
        "",
        f"- **Target**: `{target_str}`",
        f"- **Audit Timestamp**: `{timestamp_str}`",
        f"- **Validation Status**: `{status_str}`",
        "",
        "## 1. Audit Findings",
    ]

    hardcodes = audit_results.get("hardcoded_paths", [])
    pointers = audit_results.get("unresolved_pointers", [])

    if not hardcodes and not pointers:
        report_lines.append("All environment pointers resolve cleanly. Zero hardcoded paths discovered.")
    else:
        for idx, hc in enumerate(hardcodes, start=1):
            f_str = hc["file"]
            s_str = hc["matched_string"]
            report_lines.append(f"{idx}. **[HARDCODED_PATH]** `{f_str}`: `{s_str}`")

        for idx, ptr in enumerate(pointers, start=len(hardcodes) + 1):
            f_str = ptr["file"]
            t_str = ptr["token"]
            report_lines.append(f"{idx}. **[UNRESOLVED_POINTER]** `{f_str}`: `ENV:{t_str}`")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Environment Pointer Validator tool."""
    argument_parser = argparse.ArgumentParser(
        description="env-pointer-validator: Audits codebases for hardcoded paths and unresolvable ENV: pointers."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to project or directory to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--definitions",
        type=str,
        default=str(DEFAULT_DEFINITIONS_PATH),
        help=f"Path to canonical definitions.json (default: {DEFAULT_DEFINITIONS_PATH}).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Print markdown formatted report to stdout.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON summary to stdout.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"env_pointer_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    target_path = sanitize_input_path(parsed_arguments.target)
    defs_path = sanitize_input_path(parsed_arguments.definitions)

    if not target_path.exists():
        sys.stderr.write(f"Error: Target path does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    try:
        known_keys = load_canonical_definitions_keys(defs_path)
        audit_results = audit_target_for_pointers_and_hardcodes(target_path, known_keys)

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            report_text = generate_pointer_report_markdown(audit_results)
            print(report_text)

        if audit_results["has_violations"]:
            return EXIT_VIOLATIONS_DETECTED
        return EXIT_CLEAN_PASS

    except Exception as runtime_error:
        sys.stderr.write(f"Fatal error during pointer audit: {runtime_error}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
