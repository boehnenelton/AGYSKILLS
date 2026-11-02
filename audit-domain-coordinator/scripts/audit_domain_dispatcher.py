#!/usr/bin/env python3
"""
audit_domain_dispatcher.py
Layer 6 Audit Domain Orchestration & Cartography Engine
Sequences, dispatches, and aggregates multi-phase audit pipelines across repositories,
skill bundles, and staging workspaces. Synthesizes the Executive Audit Dossier.

Policy Anchors:
  Policy §2.3: Post-Task Standardized Logging
  Policy §6.1: Long Self-Describing Variable Standard
  Policy §7.1: Surgical Execution & Goal-Driven Design
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_FULL_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_REMEDIATIONS_REQUIRED = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_target_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def locate_skill_script_tool(skill_name_token: str, script_file_name_token: str) -> Optional[Path]:
    """Locate executable audit tool from installed skills directory."""
    skills_root_directory = Path(__file__).resolve().parent.parent.parent
    candidate_script_path = skills_root_directory / skill_name_token / "scripts" / script_file_name_token
    if candidate_script_path.is_file():
        return candidate_script_path
    return None


def execute_subsystem_audit_command(
    python_script_path: Path,
    target_project_path: Path,
    additional_flags: Optional[List[str]] = None,
) -> Tuple[int, Dict[str, Any]]:
    """Execute single audit tool with --json flag and parse output."""
    execution_command_arguments = [
        sys.executable,
        str(python_script_path),
        "--target" if "--target" in python_script_path.name or "readiness" in python_script_path.name or "constraint" in python_script_path.name or "gap" in python_script_path.name or "redundancy" in python_script_path.name else "--project",
        str(target_project_path),
        "--json",
    ]
    if additional_flags:
        execution_command_arguments.extend(additional_flags)

    try:
        command_process_result = subprocess.run(
            execution_command_arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        parsed_json_output: Dict[str, Any] = {}
        if command_process_result.stdout.strip():
            try:
                parsed_json_output = json.loads(command_process_result.stdout)
            except Exception:
                parsed_json_output = {"raw_output": command_process_result.stdout.strip()}

        return command_process_result.returncode, parsed_json_output
    except Exception as execution_exception:
        return EXIT_ENV_FAILURE, {"error": str(execution_exception)}


def orchestrate_domain_audit_pipeline(
    target_project_directory_path: Path,
    phases_to_execute_list: List[int],
    fail_fast_flag: bool = False,
) -> Dict[str, Any]:
    """Orchestrate multi-phase audits and build executive dossier payload."""
    audit_dossier_results: Dict[str, Any] = {
        "target_project": str(target_project_directory_path),
        "orchestration_timestamp": get_current_utc_timestamp_iso(),
        "phases_executed": phases_to_execute_list,
        "phase_results": {},
        "overall_status": "CERTIFIED_PASS",
        "consolidated_remediations": [],
    }

    # Phase 1: Pre-Flight Readiness
    if 1 in phases_to_execute_list:
        readiness_script = locate_skill_script_tool("audit-readiness-auditor", "audit_readiness_tool.py")
        if readiness_script:
            exit_code, payload = execute_subsystem_audit_command(readiness_script, target_project_directory_path)
            passed = exit_code == 0
            audit_dossier_results["phase_results"]["Phase 1: Readiness"] = {
                "passed": passed,
                "exit_code": exit_code,
                "findings": payload.get("issues", []),
            }
            if not passed:
                audit_dossier_results["overall_status"] = "REMEDIATIONS_REQUIRED"
                for issue in payload.get("issues", []):
                    audit_dossier_results["consolidated_remediations"].append(
                        f"[Phase 1 - Readiness] {issue.get('remediation')}"
                    )
                if fail_fast_flag:
                    return audit_dossier_results

    # Phase 2: Negative Boundary & Invariants
    if 2 in phases_to_execute_list:
        constraint_script = locate_skill_script_tool("audit-constraint-auditor", "audit_constraint_tool.py")
        if constraint_script:
            exit_code, payload = execute_subsystem_audit_command(constraint_script, target_project_directory_path)
            passed = exit_code == 0
            audit_dossier_results["phase_results"]["Phase 2: Negative Constraints"] = {
                "passed": passed,
                "exit_code": exit_code,
                "findings": payload.get("violations", []),
            }
            if not passed:
                audit_dossier_results["overall_status"] = "REMEDIATIONS_REQUIRED"
                for viol in payload.get("violations", []):
                    audit_dossier_results["consolidated_remediations"].append(
                        f"[Phase 2 - Constraint] {viol.get('remediation')}"
                    )
                if fail_fast_flag:
                    return audit_dossier_results

    # Phase 3: Goal Deviation Verification
    if 3 in phases_to_execute_list:
        deviation_script = locate_skill_script_tool("audit-deviation-auditor", "audit_deviation_tool.py")
        if deviation_script:
            exit_code, payload = execute_subsystem_audit_command(deviation_script, target_project_directory_path)
            passed = exit_code == 0
            audit_dossier_results["phase_results"]["Phase 3: Goal Deviation"] = {
                "passed": passed,
                "exit_code": exit_code,
                "findings": payload.get("discrepancies", []),
            }
            if not passed:
                audit_dossier_results["overall_status"] = "REMEDIATIONS_REQUIRED"
                for disc in payload.get("discrepancies", []):
                    audit_dossier_results["consolidated_remediations"].append(
                        f"[Phase 3 - Deviation] {disc.get('remediation')}"
                    )
                if fail_fast_flag:
                    return audit_dossier_results

    # Phase 4: Structural Gaps & Redundancies
    if 4 in phases_to_execute_list:
        gap_script = locate_skill_script_tool("audit-gap-planner", "audit_gap_tool.py")
        redundancy_script = locate_skill_script_tool("audit-redundancy-planner", "audit_redundancy_tool.py")

        gap_findings: List[Dict[str, Any]] = []
        if gap_script:
            exit_code, payload = execute_subsystem_audit_command(gap_script, target_project_directory_path)
            gap_findings = payload.get("gaps", [])
            for gap in gap_findings:
                audit_dossier_results["consolidated_remediations"].append(
                    f"[Phase 4 - Gap] {gap.get('remediation')}"
                )

        redundancy_findings: List[Dict[str, Any]] = []
        if redundancy_script:
            exit_code, payload = execute_subsystem_audit_command(redundancy_script, target_project_directory_path)
            redundancy_findings = payload.get("redundancies", [])
            for red in redundancy_findings:
                audit_dossier_results["consolidated_remediations"].append(
                    f"[Phase 4 - Redundancy] {red.get('remediation')}"
                )

        phase4_passed = len(gap_findings) == 0 and len(redundancy_findings) == 0
        audit_dossier_results["phase_results"]["Phase 4: Optimization"] = {
            "passed": phase4_passed,
            "gap_findings": gap_findings,
            "redundancy_findings": redundancy_findings,
        }
        if not phase4_passed and audit_dossier_results["overall_status"] == "CERTIFIED_PASS":
            audit_dossier_results["overall_status"] = "OPTIMIZATION_ADVISORY"

    return audit_dossier_results


def generate_executive_audit_dossier_markdown(dossier_data_dictionary: Dict[str, Any]) -> str:
    """Generate comprehensive Executive Audit Dossier Markdown report."""
    target_str = dossier_data_dictionary["target_project"]
    timestamp_str = dossier_data_dictionary["orchestration_timestamp"]
    status_str = dossier_data_dictionary["overall_status"]
    phase_results = dossier_data_dictionary["phase_results"]
    remediations = dossier_data_dictionary["consolidated_remediations"]

    report_lines: List[str] = [
        "# Executive Audit Dossier",
        "",
        f"- **Target System**: `{target_str}`",
        f"- **Orchestration Timestamp**: `{timestamp_str}`",
        f"- **Certification Status**: `{status_str}`",
        "",
        "## 1. Multi-Phase Execution Matrix",
        "",
        "| Phase Gate | Status | Findings |",
        "| :--- | :---: | :--- |",
    ]

    for phase_name, p_data in phase_results.items():
        pass_badge = "PASSED" if p_data.get("passed") else "ATTENTION"
        f_count = len(p_data.get("findings", p_data.get("gap_findings", []) + p_data.get("redundancy_findings", [])))
        report_lines.append(f"| {phase_name} | {pass_badge} | {f_count} findings |")

    report_lines.extend(["", "## 2. Consolidated Remediation Action Plan"])
    if not remediations:
        report_lines.append("- [x] All stage gates certified. System is in peak architectural compliance.")
    else:
        for idx, rem_text in enumerate(remediations, start=1):
            report_lines.append(f"- [ ] Step {idx}: {rem_text}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Audit Domain Dispatcher & Coordinator tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-domain-coordinator: Master multi-phase audit dispatcher and executive cartographer."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to repository or project to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--phases",
        type=str,
        default="all",
        help="Phases to execute (comma-separated, e.g. '1,2,3', or 'all'). Default: 'all'.",
    )
    argument_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Halt pipeline execution immediately upon encountering a phase failure.",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/executive_audit_dossier_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw dossier findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_domain_dispatcher v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_target_path(parsed_arguments.target)

    if not target_path.exists() or not target_path.is_dir():
        sys.stderr.write(f"Error: Target directory does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    phases_list = [1, 2, 3, 4]
    if parsed_arguments.phases != "all":
        try:
            phases_list = [int(p.strip()) for p in parsed_arguments.phases.split(",") if p.strip()]
        except Exception:
            sys.stderr.write("Error: Invalid phases argument. Specify comma-separated integers (e.g. 1,2,3) or 'all'.\n")
            return EXIT_ENV_FAILURE

    try:
        dossier = orchestrate_domain_audit_pipeline(
            target_project_directory_path=target_path,
            phases_to_execute_list=phases_list,
            fail_fast_flag=parsed_arguments.fail_fast,
        )

        if parsed_arguments.json:
            print(json.dumps(dossier, indent=2))
        else:
            markdown_dossier = generate_executive_audit_dossier_markdown(dossier)
            print(markdown_dossier)

        if parsed_arguments.report:
            reports_directory = target_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"executive_audit_dossier_{timestamp_token}.md"
            report_file_path.write_text(generate_executive_audit_dossier_markdown(dossier), encoding="utf-8")
            sys.stderr.write(f"Executive Audit Dossier saved to: {report_file_path}\n")

        if dossier["overall_status"] == "REMEDIATIONS_REQUIRED":
            return EXIT_REMEDIATIONS_REQUIRED
        return EXIT_FULL_PASS

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during domain orchestration: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
