#!/usr/bin/env python3
"""
audit_readiness_tool.py
Layer 2 Pre-Flight Structural & Dependency Readiness Engine
Verifies directory topologies, configuration bootstrap files, environment stores,
executable permissions, and schema syntax before launching roadmaps or tasks.

Policy Anchors:
  Policy §1.1: Standardized Relative Subfolder Architecture
  Policy §4.4: Script Configuration (BEJSON 104a)
  Policy §4.5: Environment Sourcing Standards
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_READINESS_GO = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_READINESS_NO_GO = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_target_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def audit_standard_subdirectories(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Verify presence of Policy §1.1 standardized subdirectories."""
    discovered_readiness_issues: List[Dict[str, Any]] = []
    canonical_subdirectories = ["lib", "config", "data", "exports", "dev", "docs"]

    # Only enforce if project appears to be a standalone project root (contains src or scripts or bejson_project.json)
    is_project_root = (
        (target_directory_path / "bejson_project.json").exists()
        or (target_directory_path / "src").exists()
        or (target_directory_path / "scripts").exists()
    )

    if is_project_root:
        for single_subfolder_name in canonical_subdirectories:
            subfolder_path = target_directory_path / single_subfolder_name
            if not subfolder_path.exists():
                discovered_readiness_issues.append(
                    {
                        "dimension": "DIRECTORY_TOPOLOGY",
                        "code": "RDY-DIR-001",
                        "severity": "MEDIUM",
                        "item": single_subfolder_name,
                        "description": f"Standard subfolder '{single_subfolder_name}/' is missing in project root.",
                        "remediation": f"Scaffold missing directory: mkdir -p {subfolder_path}.",
                    }
                )

    return discovered_readiness_issues


def audit_executable_permissions(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Verify that executable entrypoint scripts have POSIX +x execution permissions."""
    discovered_permission_issues: List[Dict[str, Any]] = []

    for executable_candidate_path in target_directory_path.rglob("*"):
        if not executable_candidate_path.is_file():
            continue
        file_name_str = executable_candidate_path.name
        # Check files ending in .sh or files in scripts/ ending in .py
        is_script_candidate = file_name_str.endswith(".sh") or (
            "scripts" in executable_candidate_path.parts and file_name_str.endswith(".py")
        )
        if is_script_candidate:
            file_mode_bits = executable_candidate_path.stat().st_mode
            is_executable = bool(file_mode_bits & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            if not is_executable:
                rel_path = str(executable_candidate_path.relative_to(target_directory_path))
                discovered_permission_issues.append(
                    {
                        "dimension": "POSIX_PERMISSIONS",
                        "code": "RDY-PRM-001",
                        "severity": "HIGH",
                        "item": rel_path,
                        "description": f"Executable script '{rel_path}' lacks execute permission (+x).",
                        "remediation": f"Grant execute permission: chmod +x {executable_candidate_path}.",
                    }
                )

    return discovered_permission_issues


def audit_environment_stores() -> List[Dict[str, Any]]:
    """Verify access to canonical environment stores."""
    discovered_environment_issues: List[Dict[str, Any]] = []
    canonical_definitions_path = Path("/storage/emulated/0/.env/user/definitions.json")

    # In Termux/Android, verify definitions.json
    if os.path.exists("/storage/emulated/0"):
        if not canonical_definitions_path.is_file():
            discovered_environment_issues.append(
                {
                    "dimension": "ENVIRONMENT_STORES",
                    "code": "RDY-ENV-001",
                    "severity": "CRITICAL",
                    "item": str(canonical_definitions_path),
                    "description": "Canonical user definitions file is missing or unreadable.",
                    "remediation": f"Ensure {canonical_definitions_path} is accessible.",
                }
            )

    return discovered_environment_issues


def audit_companion_schema_syntax(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Pre-validate that all JSON and BEJSON configuration files parse without syntax errors."""
    discovered_syntax_issues: List[Dict[str, Any]] = []

    for json_candidate_path in target_directory_path.rglob("*.json"):
        if "__pycache__" in json_candidate_path.parts or ".git" in json_candidate_path.parts:
            continue
        try:
            with open(json_candidate_path, "r", encoding="utf-8") as file_read_handle:
                json.load(file_read_handle)
        except Exception as json_parse_exception:
            rel_path = str(json_candidate_path.relative_to(target_directory_path))
            discovered_syntax_issues.append(
                {
                    "dimension": "SCHEMA_SYNTAX",
                    "code": "RDY-SCH-001",
                    "severity": "CRITICAL",
                    "item": rel_path,
                    "description": f"Malformed JSON syntax in '{rel_path}': {json_parse_exception}",
                    "remediation": f"Fix syntax errors in '{rel_path}' prior to execution.",
                }
            )

    return discovered_syntax_issues


def perform_complete_readiness_audit(target_directory_path: Path) -> Dict[str, Any]:
    """Execute complete pre-flight readiness audit."""
    all_readiness_issues: List[Dict[str, Any]] = []

    # 1. Standard subdirectories
    subfolder_issues = audit_standard_subdirectories(target_directory_path)
    all_readiness_issues.extend(subfolder_issues)

    # 2. Executable permissions
    permission_issues = audit_executable_permissions(target_directory_path)
    all_readiness_issues.extend(permission_issues)

    # 3. Environment stores
    environment_issues = audit_environment_stores()
    all_readiness_issues.extend(environment_issues)

    # 4. JSON / Schema syntax
    syntax_issues = audit_companion_schema_syntax(target_directory_path)
    all_readiness_issues.extend(syntax_issues)

    # Classify blocker vs warning
    blocker_issues_list = [issue for issue in all_readiness_issues if issue["severity"] in ("CRITICAL", "HIGH")]
    has_blockers_flag = len(blocker_issues_list) > 0
    readiness_decision_token = "NO_GO" if has_blockers_flag else "GO"

    audit_summary_dictionary = {
        "target_directory": str(target_directory_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "readiness_decision": readiness_decision_token,
        "total_issues_identified": len(all_readiness_issues),
        "blockers_count": len(blocker_issues_list),
        "issues": all_readiness_issues,
    }
    return audit_summary_dictionary


def generate_markdown_readiness_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate standardized Markdown readiness report."""
    target_dir_str = audit_result_dictionary["target_directory"]
    audit_timestamp_str = audit_result_dictionary["audit_timestamp"]
    decision_str = audit_result_dictionary["readiness_decision"]
    total_issues = audit_result_dictionary["total_issues_identified"]
    blockers_count = audit_result_dictionary["blockers_count"]

    report_lines: List[str] = [
        "# Structural Readiness Audit Report",
        "",
        f"- **Target System**: `{target_dir_str}`",
        f"- **Audit Timestamp**: `{audit_timestamp_str}`",
        f"- **Readiness Gate**: `{decision_str}` ({blockers_count} blockers, {total_issues} total issues)",
        "",
        "## 1. Discovered Readiness Issues",
    ]

    issues_list = audit_result_dictionary["issues"]
    if not issues_list:
        report_lines.append("All pre-flight checks passed. Target workspace is fully ready for execution.")
    else:
        for index_counter, issue_item in enumerate(issues_list, start=1):
            dim_str = issue_item["dimension"]
            code_str = issue_item["code"]
            sev_str = issue_item["severity"]
            item_str = issue_item["item"]
            desc_str = issue_item["description"]
            report_lines.append(
                f"{index_counter}. **[{dim_str} | {code_str} | {sev_str}]** `{item_str}`: {desc_str}"
            )

    report_lines.extend(["", "## 2. Pre-Flight Remediation Actions"])
    if not issues_list:
        report_lines.append("- [x] Dependency chain verified. Safe to proceed.")
    else:
        for index_counter, issue_item in enumerate(issues_list, start=1):
            remediation_step_str = issue_item["remediation"]
            report_lines.append(f"- [ ] Action {index_counter}: {remediation_step_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Structural Readiness Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-readiness-auditor: Pre-flight structural and dependency readiness engine."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to repository or project to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/readiness_audit_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw readiness findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_readiness_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_target_path(parsed_arguments.target)

    if not target_path.exists() or not target_path.is_dir():
        sys.stderr.write(f"Error: Target directory does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    try:
        audit_results = perform_complete_readiness_audit(target_path)

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            markdown_content = generate_markdown_readiness_report(audit_results)
            print(markdown_content)

        if parsed_arguments.report:
            reports_directory = target_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"readiness_audit_{timestamp_token}.md"
            report_file_path.write_text(generate_markdown_readiness_report(audit_results), encoding="utf-8")
            sys.stderr.write(f"Readiness audit report saved to: {report_file_path}\n")

        if audit_results["readiness_decision"] == "NO_GO":
            return EXIT_READINESS_NO_GO
        return EXIT_READINESS_GO

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during readiness audit: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
