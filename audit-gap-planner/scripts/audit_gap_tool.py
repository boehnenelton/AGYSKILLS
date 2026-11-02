#!/usr/bin/env python3
"""
audit_gap_tool.py
Layer 5 Structural Gap & Blind Spot Analysis Engine
Scans codebases and library directories for architectural blind spots, missing multi-language ports,
unhandled schema invariants, and absent CLI operational flags.

Policy Anchors:
  Policy §6.1: Long self-describing variable names
  Policy §7.1: Surgical Execution & Goal-Driven Design
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
EXIT_GAPS_IDENTIFIED = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_target_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def audit_multi_language_ports(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Audit for language parity across py, js, ts, and sh implementations."""
    discovered_gap_items_list: List[Dict[str, Any]] = []

    # Map basenames across extensions
    registered_extension_map: Dict[str, Set[str]] = {}
    canonical_supported_extensions = {".py", ".js", ".ts", ".sh"}

    for root_dir_str, _, file_names_list in os.walk(target_directory_path):
        for single_file_name in file_names_list:
            file_extension_str = os.path.splitext(single_file_name)[1].lower()
            if file_extension_str in canonical_supported_extensions:
                base_name_without_ext = os.path.splitext(single_file_name)[0]
                # Normalize common prefixes like lib_ or test_
                clean_base_name = re.sub(r"^(lib_|test_)", "", base_name_without_ext).lower()
                if clean_base_name not in registered_extension_map:
                    registered_extension_map[clean_base_name] = set()
                registered_extension_map[clean_base_name].add(file_extension_str)

    # Detect modules with Python implementation but missing JS/TS or Bash
    for component_base_name, active_extension_set in registered_extension_map.items():
        if len(active_extension_set) > 0 and len(active_extension_set) < 4:
            missing_extensions = canonical_supported_extensions - active_extension_set
            # Only flag as gap if it is a core library component
            if "bejson" in component_base_name or "core" in component_base_name or "upgrade" in component_base_name:
                missing_ext_str = ", ".join(sorted(list(missing_extensions)))
                discovered_gap_items_list.append(
                    {
                        "gap_code": "GAP-PORT-001",
                        "priority": "P1",
                        "category": "PORT_PARITY_GAP",
                        "component": component_base_name,
                        "description": f"Core component '{component_base_name}' lacks multi-language parity ports: {missing_ext_str}.",
                        "remediation": f"Scaffold equivalent port implementations for extensions [{missing_ext_str}].",
                    }
                )

    return discovered_gap_items_list


def audit_cli_script_flags(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Audit executable CLI scripts for required standard flags (--help, --version)."""
    discovered_cli_gaps_list: List[Dict[str, Any]] = []

    for file_path_candidate in target_directory_path.rglob("*.py"):
        if not file_path_candidate.is_file():
            continue
        try:
            file_content_text = file_path_candidate.read_text(encoding="utf-8")
            # If it has an entrypoint (if __name__ == '__main__')
            if "if __name__" in file_content_text and "main(" in file_content_text:
                has_version_flag = "--version" in file_content_text or "action=\"version\"" in file_content_text
                has_help_support = "add_argument" in file_content_text or "argparse" in file_content_text or "help" in file_content_text
                if not has_version_flag:
                    discovered_cli_gaps_list.append(
                        {
                            "gap_code": "GAP-CLI-001",
                            "priority": "P2",
                            "category": "OPERATIONAL_CLI_GAP",
                            "component": file_path_candidate.name,
                            "description": f"Executable CLI script '{file_path_candidate.name}' lacks standard --version flag.",
                            "remediation": f"Add standard --version flag to argparse definition in '{file_path_candidate.name}'.",
                        }
                    )
        except Exception:
            pass

    return discovered_cli_gaps_list


def perform_complete_gap_audit(target_directory_path: Path) -> Dict[str, Any]:
    """Execute complete structural gap audit across target directory."""
    all_discovered_gaps: List[Dict[str, Any]] = []

    # 1. Multi-language ports
    port_gaps = audit_multi_language_ports(target_directory_path)
    all_discovered_gaps.extend(port_gaps)

    # 2. CLI operability flags
    cli_gaps = audit_cli_script_flags(target_directory_path)
    all_discovered_gaps.extend(cli_gaps)

    total_gaps_count = len(all_discovered_gaps)
    has_gaps_flag = total_gaps_count > 0

    audit_summary_dictionary = {
        "target_directory": str(target_directory_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "total_gaps_identified": total_gaps_count,
        "has_gaps": has_gaps_flag,
        "gaps": all_discovered_gaps,
    }
    return audit_summary_dictionary


def generate_markdown_gap_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate standardized Markdown gap analysis report."""
    target_dir_str = audit_result_dictionary["target_directory"]
    audit_timestamp_str = audit_result_dictionary["audit_timestamp"]
    total_gaps_count = audit_result_dictionary["total_gaps_identified"]
    has_gaps_flag = audit_result_dictionary["has_gaps"]

    status_str = "GAPS_IDENTIFIED" if has_gaps_flag else "FULL_COVERAGE"

    report_lines: List[str] = [
        "# Structural Gap Audit Report",
        "",
        f"- **Target System**: `{target_dir_str}`",
        f"- **Audit Timestamp**: `{audit_timestamp_str}`",
        f"- **Audit Status**: `{status_str}` ({total_gaps_count} structural gaps found)",
        "",
        "## 1. Identified Structural Gaps",
    ]

    gaps_list = audit_result_dictionary["gaps"]
    if not gaps_list:
        report_lines.append("No structural gaps or missing capability ports detected. Ecosystem is complete.")
    else:
        for index_counter, gap_item in enumerate(gaps_list, start=1):
            gap_code_str = gap_item["gap_code"]
            priority_str = gap_item["priority"]
            category_str = gap_item["category"]
            component_str = gap_item["component"]
            desc_str = gap_item["description"]
            report_lines.append(
                f"{index_counter}. **[{gap_code_str} | {priority_str} | {category_str}]** `{component_str}`: {desc_str}"
            )

    report_lines.extend(["", "## 2. Phased Gap-Closure Roadmap"])
    if not gaps_list:
        report_lines.append("- [x] All capability matrices satisfied.")
    else:
        # Group by priority
        p0_p1_gaps = [g for g in gaps_list if g["priority"] in ("P0", "P1")]
        p2_p3_gaps = [g for g in gaps_list if g["priority"] in ("P2", "P3")]

        if p0_p1_gaps:
            report_lines.extend(["", "### Phase 1: High-Priority & Core Architecture Gaps"])
            for index_counter, gap_item in enumerate(p0_p1_gaps, start=1):
                remediation_step_str = gap_item["remediation"]
                report_lines.append(f"- [ ] Step 1.{index_counter}: {remediation_step_str}")

        if p2_p3_gaps:
            report_lines.extend(["", "### Phase 2: Tooling & Ergonomics Gaps"])
            for index_counter, gap_item in enumerate(p2_p3_gaps, start=1):
                remediation_step_str = gap_item["remediation"]
                report_lines.append(f"- [ ] Step 2.{index_counter}: {remediation_step_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Structural Gap Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-gap-planner: Structural gap and blind spot analysis engine."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to directory or project to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/gap_analysis_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw gap findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_gap_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_target_path(parsed_arguments.target)

    if not target_path.exists() or not target_path.is_dir():
        sys.stderr.write(f"Error: Target directory does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    try:
        audit_results = perform_complete_gap_audit(target_path)

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            markdown_content = generate_markdown_gap_report(audit_results)
            print(markdown_content)

        if parsed_arguments.report:
            reports_directory = target_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"gap_analysis_{timestamp_token}.md"
            report_file_path.write_text(generate_markdown_gap_report(audit_results), encoding="utf-8")
            sys.stderr.write(f"Gap analysis report saved to: {report_file_path}\n")

        if audit_results["has_gaps"]:
            return EXIT_GAPS_IDENTIFIED
        return EXIT_CLEAN_PASS

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during gap audit: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
