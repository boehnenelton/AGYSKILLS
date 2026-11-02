#!/usr/bin/env python3
"""
audit_constraint_tool.py
Layer 2 Negative Constraint & Boundary Defense Engine
Audits git worktrees and file modifications against strict negative constraints (immutable libraries,
master policy files, single-letter variables) and audits rule files for defensive 'DO NOT' posture.

Policy Anchors:
  Policy §1.2: Override Protocol & Negative Constraints
  Policy §6.1: Long Self-Describing Variable Standard
  Policy §7.3: Negative Constraints
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_BREACHES_DETECTED = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_target_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def audit_git_modified_paths(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Scan git modifications against off-limits immutable files and directories."""
    discovered_breaches_list: List[Dict[str, Any]] = []

    git_dir = target_directory_path / ".git"
    if not git_dir.exists():
        return discovered_breaches_list

    try:
        git_command_execution = subprocess.run(
            ["git", "-C", str(target_directory_path), "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        if git_command_execution.returncode == 0:
            for raw_status_line in git_command_execution.stdout.splitlines():
                if not raw_status_line.strip():
                    continue
                file_relative_path_str = raw_status_line[3:].strip()

                # NC-001: Admin Libraries
                if "libraries_104" in file_relative_path_str or "libraries_105" in file_relative_path_str or "Admin/Libraries" in file_relative_path_str:
                    discovered_breaches_list.append(
                        {
                            "constraint_code": "NC-001",
                            "severity": "CRITICAL",
                            "category": "FORBIDDEN_PATH_TOUCH",
                            "item": file_relative_path_str,
                            "description": f"Modified immutable library '{file_relative_path_str}' without authorization.",
                            "remediation": f"Immediately revert modifications to '{file_relative_path_str}'.",
                        }
                    )

                # NC-002: Master Policy GEMINI.md
                if "GEMINI.md" in file_relative_path_str and not file_relative_path_str.startswith("dev/"):
                    discovered_breaches_list.append(
                        {
                            "constraint_code": "NC-002",
                            "severity": "CRITICAL",
                            "category": "MASTER_POLICY_TOUCH",
                            "item": file_relative_path_str,
                            "description": f"Modified master policy file '{file_relative_path_str}'.",
                            "remediation": f"Restore '{file_relative_path_str}' from git head or backup.",
                        }
                    )
    except Exception:
        pass

    return discovered_breaches_list


def audit_code_negative_constraints(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Scan python source files for banned single-letter loop or variable names (Policy §6.1)."""
    discovered_code_breaches_list: List[Dict[str, Any]] = []

    banned_single_letter_pattern = re.compile(
        r"^\s*for\s+([a-zA-Z])\s+in\s+",
        re.MULTILINE,
    )

    for python_file_path in target_directory_path.rglob("*.py"):
        if "__pycache__" in python_file_path.parts or ".git" in python_file_path.parts:
            continue
        try:
            file_content_text = python_file_path.read_text(encoding="utf-8")
            for match_item in banned_single_letter_pattern.finditer(file_content_text):
                single_letter_var = match_item.group(1)
                rel_path = str(python_file_path.relative_to(target_directory_path))
                discovered_code_breaches_list.append(
                    {
                        "constraint_code": "NC-003",
                        "severity": "HIGH",
                        "category": "BANNED_VARIABLE_CONVENTIONS",
                        "item": f"{rel_path}:{single_letter_var}",
                        "description": f"Banned single-letter variable '{single_letter_var}' used in loop in '{rel_path}'.",
                        "remediation": f"Refactor variable '{single_letter_var}' in '{rel_path}' to long self-describing name.",
                    }
                )
        except Exception:
            pass

    return discovered_code_breaches_list


def audit_rule_file_posture(rules_file_path: Path) -> List[Dict[str, Any]]:
    """Audit rule files (AGENTS.md, GEMINI.md) to ensure defensive negative constraints exist."""
    posture_findings_list: List[Dict[str, Any]] = []

    if not rules_file_path.is_file():
        return posture_findings_list

    try:
        text_content = rules_file_path.read_text(encoding="utf-8")
        negative_keywords = ["do not", "never", "must not", "prohibited", "strictly forbidden", "negative constraint"]

        negative_clauses_count = 0
        for single_keyword in negative_keywords:
            matches = re.findall(rf"\b{single_keyword}\b", text_content, re.IGNORECASE)
            negative_clauses_count += len(matches)

        if negative_clauses_count < 2:
            posture_findings_list.append(
                {
                    "constraint_code": "NC-RULE-001",
                    "severity": "HIGH",
                    "category": "DEFENSIVE_POSTURE_ABSENCE",
                    "item": rules_file_path.name,
                    "description": f"Rule file '{rules_file_path.name}' contains only {negative_clauses_count} negative constraints. High risk of unbounded agent drift.",
                    "remediation": f"Inject explicit 'DO NOT' boundary constraints into '{rules_file_path.name}'.",
                }
            )
    except Exception:
        pass

    return posture_findings_list


def perform_complete_constraint_audit(
    target_directory_path: Path,
    explicit_rules_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Execute complete negative constraint audit across physical repository and rule posture."""
    all_discovered_violations: List[Dict[str, Any]] = []

    # 1. Physical git path touch audit
    git_breaches = audit_git_modified_paths(target_directory_path)
    all_discovered_violations.extend(git_breaches)

    # 2. Code style negative constraints
    code_breaches = audit_code_negative_constraints(target_directory_path)
    all_discovered_violations.extend(code_breaches)

    # 3. Rule posture audit
    target_rules = explicit_rules_path or (target_directory_path / "AGENTS.md")
    if not target_rules.exists():
        target_rules = target_directory_path / "GEMINI.md"

    if target_rules.exists():
        rule_findings = audit_rule_file_posture(target_rules)
        all_discovered_violations.extend(rule_findings)

    total_violations_count = len(all_discovered_violations)
    has_violations_flag = total_violations_count > 0

    audit_summary_dictionary = {
        "target_directory": str(target_directory_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "total_violations_identified": total_violations_count,
        "has_violations": has_violations_flag,
        "violations": all_discovered_violations,
    }
    return audit_summary_dictionary


def generate_markdown_constraint_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate standardized Markdown negative constraint audit report."""
    target_dir_str = audit_result_dictionary["target_directory"]
    audit_timestamp_str = audit_result_dictionary["audit_timestamp"]
    total_violations_count = audit_result_dictionary["total_violations_identified"]
    has_violations_flag = audit_result_dictionary["has_violations"]

    status_str = "BREACHES_DETECTED" if has_violations_flag else "CLEAN_COMPLIANT"

    report_lines: List[str] = [
        "# Negative Constraint Audit Report",
        "",
        f"- **Target System**: `{target_dir_str}`",
        f"- **Audit Timestamp**: `{audit_timestamp_str}`",
        f"- **Audit Status**: `{status_str}` ({total_violations_count} violations identified)",
        "",
        "## 1. Discovered Boundary Breaches & Posture Warnings",
    ]

    violations_list = audit_result_dictionary["violations"]
    if not violations_list:
        report_lines.append("No negative constraint breaches or forbidden path touches detected. Defensive posture intact.")
    else:
        for index_counter, violation_item in enumerate(violations_list, start=1):
            code_str = violation_item["constraint_code"]
            severity_str = violation_item["severity"]
            category_str = violation_item["category"]
            item_str = violation_item["item"]
            desc_str = violation_item["description"]
            report_lines.append(
                f"{index_counter}. **[{code_str} | {severity_str} | {category_str}]** `{item_str}`: {desc_str}"
            )

    report_lines.extend(["", "## 2. Mandatory Containment Actions"])
    if not violations_list:
        report_lines.append("- [x] All negative architectural boundaries strictly respected.")
    else:
        for index_counter, violation_item in enumerate(violations_list, start=1):
            remediation_step_str = violation_item["remediation"]
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
    """CLI entrypoint for Negative Constraint Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-constraint-auditor: Negative constraint and architectural boundary defense engine."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to repository or project to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--rules",
        type=str,
        default=None,
        help="Path to explicit rules file to audit for negative constraints (e.g. AGENTS.md).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/constraint_audit_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw violation findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_constraint_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_target_path(parsed_arguments.target)

    if not target_path.exists() or not target_path.is_dir():
        sys.stderr.write(f"Error: Target directory does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    rules_path = None
    if parsed_arguments.rules:
        rules_path = sanitize_target_path(parsed_arguments.rules)
        if not rules_path.exists():
            sys.stderr.write(f"Error: Specified rules file does not exist: {rules_path}\n")
            return EXIT_PATH_FAILURE

    try:
        audit_results = perform_complete_constraint_audit(
            target_directory_path=target_path,
            explicit_rules_path=rules_path,
        )

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            markdown_content = generate_markdown_constraint_report(audit_results)
            print(markdown_content)

        if parsed_arguments.report:
            reports_directory = target_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"constraint_audit_{timestamp_token}.md"
            report_file_path.write_text(generate_markdown_constraint_report(audit_results), encoding="utf-8")
            sys.stderr.write(f"Constraint audit report saved to: {report_file_path}\n")

        if audit_results["has_violations"]:
            return EXIT_BREACHES_DETECTED
        return EXIT_CLEAN_PASS

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during constraint audit: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
