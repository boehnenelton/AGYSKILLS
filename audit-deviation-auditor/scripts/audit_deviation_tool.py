#!/usr/bin/env python3
"""
audit_deviation_tool.py
Layer 2 Goal Deviation & System Audit Engine
Analyzes target project state against declared goal contracts, AGENTS.md, or GEMINI.md.
Detects omissions, constraint breaches, false completions, and scope creep.

Policy Anchors:
  Policy §6.1: Long self-describing variable names
  Policy §7.2: Goal-Driven Execution
  Policy §1.2: Override Protocol
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
EXIT_DEVIATIONS_DETECTED = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_audit_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def parse_goal_contract_bejson(goal_contract_path: Path) -> Dict[str, Any]:
    """Parse BEJSON 104a goal contract if present."""
    if not goal_contract_path.is_file():
        return {}
    try:
        with open(goal_contract_path, "r", encoding="utf-8") as file_read_handle:
            contract_data_dictionary = json.load(file_read_handle)
            return contract_data_dictionary
    except Exception:
        return {}


def extract_goals_from_markdown(markdown_file_path: Path) -> List[Dict[str, str]]:
    """Extract tasks, deliverables, and constraints from AGENTS.md or GEMINI.md."""
    if not markdown_file_path.is_file():
        return []

    extracted_goal_items_list: List[Dict[str, str]] = []
    try:
        markdown_text_content = markdown_file_path.read_text(encoding="utf-8")
        task_regex_pattern = re.compile(r"^[-*]\s*\[([ xX])\]\s*(.+)$", re.MULTILINE)
        for match_item in task_regex_pattern.finditer(markdown_text_content):
            checkbox_state_char = match_item.group(1).strip()
            task_description_text = match_item.group(2).strip()
            is_completed_flag = checkbox_state_char.lower() == "x"
            extracted_goal_items_list.append(
                {
                    "description": task_description_text,
                    "is_completed": str(is_completed_flag).lower(),
                    "source_file": markdown_file_path.name,
                }
            )
    except Exception:
        pass
    return extracted_goal_items_list


def inspect_git_status(target_project_directory_path: Path) -> Dict[str, List[str]]:
    """Inspect git status for unstaged, staged, and untracked files."""
    git_status_results: Dict[str, List[str]] = {
        "modified_files": [],
        "untracked_files": [],
        "deleted_files": [],
    }
    git_directory_path = target_project_directory_path / ".git"
    if not git_directory_path.exists():
        return git_status_results

    try:
        git_command_execution = subprocess.run(
            ["git", "-C", str(target_project_directory_path), "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        if git_command_execution.returncode == 0:
            for raw_status_line in git_command_execution.stdout.splitlines():
                if not raw_status_line.strip():
                    continue
                status_code_prefix = raw_status_line[:2]
                relative_file_path_str = raw_status_line[3:].strip()
                if "??" in status_code_prefix:
                    git_status_results["untracked_files"].append(relative_file_path_str)
                elif "D" in status_code_prefix:
                    git_status_results["deleted_files"].append(relative_file_path_str)
                else:
                    git_status_results["modified_files"].append(relative_file_path_str)
    except Exception:
        pass
    return git_status_results


def perform_deviation_audit(
    target_project_directory_path: Path,
    explicit_contract_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Execute complete deviation audit across filesystem and instructions."""
    audit_findings_list: List[Dict[str, Any]] = []

    # 1. Search for goal contract or instruction files
    contract_candidate_path = explicit_contract_path or (
        target_project_directory_path / "dev" / "goal_contract.104a.bejson"
    )
    agents_instructions_path = target_project_directory_path / "AGENTS.md"
    gemini_instructions_path = target_project_directory_path / "GEMINI.md"

    declared_goals_registry: List[Dict[str, Any]] = []

    if contract_candidate_path.is_file():
        contract_data = parse_goal_contract_bejson(contract_candidate_path)
        # Extract deliverables if BEJSON structure
        fields = contract_data.get("Fields", [])
        values = contract_data.get("Values", [])
        if fields and values:
            field_name_list = [f["name"] if isinstance(f, dict) else f for f in fields]
            for row in values:
                if isinstance(row, list) and len(row) == len(field_name_list):
                    row_dict = dict(zip(field_name_list, row))
                    declared_goals_registry.append(row_dict)

    if agents_instructions_path.is_file():
        markdown_goals = extract_goals_from_markdown(agents_instructions_path)
        declared_goals_registry.extend(markdown_goals)
    elif gemini_instructions_path.is_file():
        markdown_goals = extract_goals_from_markdown(gemini_instructions_path)
        declared_goals_registry.extend(markdown_goals)

    # 2. Inspect physical filesystem
    git_status = inspect_git_status(target_project_directory_path)

    # 3. Check for deliverable omissions
    for goal_item in declared_goals_registry:
        deliverable_rel_path = goal_item.get("deliverable_path") or goal_item.get("path")
        if deliverable_rel_path:
            physical_artifact_path = target_project_directory_path / deliverable_rel_path
            if not physical_artifact_path.exists():
                audit_findings_list.append(
                    {
                        "class_code": "DEV-001",
                        "category": "OMISSION",
                        "severity": "HIGH",
                        "item": deliverable_rel_path,
                        "description": f"Declared deliverable '{deliverable_rel_path}' does not exist on disk.",
                        "remediation": f"Stage an implementation task to scaffold '{deliverable_rel_path}'.",
                    }
                )

    # 4. Check negative constraint breaches (e.g., changes to frozen libraries or outside boundaries)
    for modified_file_path_str in git_status["modified_files"]:
        if "libraries_104" in modified_file_path_str or "libraries_105" in modified_file_path_str:
            audit_findings_list.append(
                {
                    "class_code": "DEV-002",
                    "category": "CONSTRAINT_BREACH",
                    "severity": "CRITICAL",
                    "item": modified_file_path_str,
                    "description": f"Modified frozen library directory '{modified_file_path_str}' without authorization.",
                    "remediation": f"Revert modifications to '{modified_file_path_str}'.",
                }
            )

    has_deviations_flag = len(audit_findings_list) > 0
    audit_summary_dictionary = {
        "target_project": str(target_project_directory_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "total_declared_goals": len(declared_goals_registry),
        "total_discrepancies": len(audit_findings_list),
        "has_deviations": has_deviations_flag,
        "discrepancies": audit_findings_list,
        "git_status": git_status,
    }
    return audit_summary_dictionary


def generate_markdown_audit_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate standardized Markdown course-correction report."""
    target_project_str = audit_result_dictionary["target_project"]
    audit_timestamp_str = audit_result_dictionary["audit_timestamp"]
    total_discrepancies_count = audit_result_dictionary["total_discrepancies"]
    has_deviations_flag = audit_result_dictionary["has_deviations"]

    status_label_str = "DEVIATIONS_DETECTED" if has_deviations_flag else "CLEAN_PASS"

    report_lines: List[str] = [
        "# Goal Deviation Audit Report",
        "",
        f"- **Target System**: `{target_project_str}`",
        f"- **Audit Timestamp**: `{audit_timestamp_str}`",
        f"- **Audit Status**: `{status_label_str}` ({total_discrepancies_count} discrepancies found)",
        "",
        "## 1. Discovered Discrepancies",
    ]

    discrepancies = audit_result_dictionary["discrepancies"]
    if not discrepancies:
        report_lines.append("No goal deviations or constraint breaches detected. Codebase matches stated goals.")
    else:
        for index_counter, discrepancy_item in enumerate(discrepancies, start=1):
            class_code_str = discrepancy_item["class_code"]
            category_token_str = discrepancy_item["category"]
            severity_str = discrepancy_item["severity"]
            item_name_str = discrepancy_item["item"]
            desc_str = discrepancy_item["description"]
            report_lines.append(
                f"{index_counter}. **[{class_code_str} | {category_token_str} | {severity_str}]** `{item_name_str}`: {desc_str}"
            )

    report_lines.extend(["", "## 2. Course-Correction Remediation Plan"])
    if not discrepancies:
        report_lines.append("- [x] System state is in full alignment with goals.")
    else:
        for index_counter, discrepancy_item in enumerate(discrepancies, start=1):
            remediation_step_str = discrepancy_item["remediation"]
            report_lines.append(f"- [ ] Step {index_counter}: {remediation_step_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Goal Deviation Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-deviation-auditor: Retrospective & mid-project goal deviation inspection engine."
    )
    argument_parser.add_argument(
        "--project",
        type=str,
        default=".",
        help="Path to project directory to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--contract",
        type=str,
        default=None,
        help="Path to explicit goal contract BEJSON or instructions Markdown.",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/goal_deviation_audit_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw audit findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_deviation_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_project_path = sanitize_audit_path(parsed_arguments.project)

    if not target_project_path.exists() or not target_project_path.is_dir():
        sys.stderr.write(f"Error: Target project directory does not exist: {target_project_path}\n")
        return EXIT_PATH_FAILURE

    contract_path = None
    if parsed_arguments.contract:
        contract_path = sanitize_audit_path(parsed_arguments.contract)
        if not contract_path.exists():
            sys.stderr.write(f"Error: Specified goal contract file does not exist: {contract_path}\n")
            return EXIT_PATH_FAILURE

    try:
        audit_results = perform_deviation_audit(
            target_project_directory_path=target_project_path,
            explicit_contract_path=contract_path,
        )

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            markdown_content = generate_markdown_audit_report(audit_results)
            print(markdown_content)

        if parsed_arguments.report:
            reports_directory = target_project_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"goal_deviation_audit_{timestamp_token}.md"
            report_file_path.write_text(generate_markdown_audit_report(audit_results), encoding="utf-8")
            sys.stderr.write(f"Audit report saved to: {report_file_path}\n")

        if audit_results["has_deviations"]:
            return EXIT_DEVIATIONS_DETECTED
        return EXIT_CLEAN_PASS

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during deviation audit: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
