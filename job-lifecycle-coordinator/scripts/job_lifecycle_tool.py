#!/usr/bin/env python3
"""
job_lifecycle_tool.py
Layer 6 JobMaker Lifecycle & Archive Orchestrator
Sweeps $JOBS_FOLDER, coordinates pre-flight validation, tracks task execution,
archives finished jobs to $COMPLETED_JOBS_FOLDER, and writes daily logs.

Policy Anchors:
  Policy § URGENT JOBS
  Policy §2.3: Post-Task Standardized Logging
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_JOB_FAILURES_DETECTED = 30

DEFAULT_JOBS_FOLDER = Path("/storage/emulated/0/Admin/System/Job_Management/Jobs")
DEFAULT_COMPLETED_FOLDER = Path("/storage/emulated/0/Admin/System/Job_Management/Completed_Jobs")
DEFAULT_LOGS_FOLDER = Path("/storage/emulated/0/Admin/System/Job_Management/Logs")


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_directory_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def locate_conformance_tool() -> Optional[Path]:
    """Locate job_conformance_tool.py from sibling skill."""
    skills_root_dir = Path(__file__).resolve().parent.parent.parent
    candidate_tool_path = skills_root_dir / "job-conformance-validator" / "scripts" / "job_conformance_tool.py"
    if candidate_tool_path.is_file():
        return candidate_tool_path
    return None


def execute_job_conformance_check(job_file_path: Path) -> Tuple[bool, List[str]]:
    """Run job conformance validator on candidate job file."""
    conformance_tool_path = locate_conformance_tool()
    if not conformance_tool_path:
        return True, []

    try:
        command_process = subprocess.run(
            [sys.executable, str(conformance_tool_path), "--job", str(job_file_path), "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        if command_process.stdout.strip():
            results = json.loads(command_process.stdout)
            if isinstance(results, list) and len(results) > 0:
                is_valid = results[0].get("is_valid", False)
                violations = [v.get("message", "") for v in results[0].get("violations", [])]
                return is_valid, violations
        return command_process.returncode == 0, []
    except Exception as exec_error:
        return False, [str(exec_error)]


def sweep_and_process_jobs_folder(
    jobs_directory_path: Path,
    completed_directory_path: Path,
    logs_directory_path: Path,
) -> Dict[str, Any]:
    """Scan jobs directory, validate, and summarize job queue state."""
    lifecycle_sweep_results: Dict[str, Any] = {
        "sweep_timestamp": get_current_utc_timestamp_iso(),
        "jobs_folder": str(jobs_directory_path),
        "total_jobs_found": 0,
        "completed_jobs_moved": 0,
        "pending_jobs_count": 0,
        "invalid_jobs_count": 0,
        "job_details": [],
    }

    if not jobs_directory_path.exists():
        return lifecycle_sweep_results

    jobs_directory_path.mkdir(parents=True, exist_ok=True)
    completed_directory_path.mkdir(parents=True, exist_ok=True)
    logs_directory_path.mkdir(parents=True, exist_ok=True)

    job_files_list = sorted(list(jobs_directory_path.glob("*.bejson")))
    lifecycle_sweep_results["total_jobs_found"] = len(job_files_list)

    for single_job_path in job_files_list:
        is_valid, violations = execute_job_conformance_check(single_job_path)

        job_info_item: Dict[str, Any] = {
            "file_name": single_job_path.name,
            "is_valid": is_valid,
            "violations": violations,
            "is_complete": False,
            "action_taken": "PENDING_EXECUTION",
        }

        if not is_valid:
            lifecycle_sweep_results["invalid_jobs_count"] += 1
            job_info_item["action_taken"] = "INVALID_SCHEMA_HALT"
        else:
            try:
                with open(single_job_path, "r", encoding="utf-8") as file_read_handle:
                    job_data = json.load(file_read_handle)
                    job_complete_flag = job_data.get("Job_Complete", False)
                    job_info_item["is_complete"] = job_complete_flag

                    if job_complete_flag:
                        destination_path = completed_directory_path / single_job_path.name
                        shutil.move(str(single_job_path), str(destination_path))
                        job_info_item["action_taken"] = f"MOVED_TO_COMPLETED ({destination_path})"
                        lifecycle_sweep_results["completed_jobs_moved"] += 1
                    else:
                        lifecycle_sweep_results["pending_jobs_count"] += 1
            except Exception as read_exception:
                job_info_item["action_taken"] = f"READ_ERROR ({read_exception})"
                lifecycle_sweep_results["invalid_jobs_count"] += 1

        lifecycle_sweep_results["job_details"].append(job_info_item)

    # Log to daily_log if any completed jobs moved
    if lifecycle_sweep_results["completed_jobs_moved"] > 0:
        date_stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
        daily_log_path = logs_directory_path / f"daily_log-{date_stamp}.md"
        with open(daily_log_path, "a", encoding="utf-8") as log_file_handle:
            log_file_handle.write(
                f"\n### Job Lifecycle Run at {lifecycle_sweep_results['sweep_timestamp']}\n"
                f"- Moved {lifecycle_sweep_results['completed_jobs_moved']} completed jobs to {completed_directory_path}\n"
            )

    return lifecycle_sweep_results


def generate_lifecycle_markdown_report(sweep_results: Dict[str, Any]) -> str:
    """Generate Markdown report for job sweep results."""
    timestamp_str = sweep_results["sweep_timestamp"]
    total_jobs = sweep_results["total_jobs_found"]
    completed_moved = sweep_results["completed_jobs_moved"]
    pending_count = sweep_results["pending_jobs_count"]
    invalid_count = sweep_results["invalid_jobs_count"]

    report_lines: List[str] = [
        "# Job Lifecycle Coordinator Report",
        "",
        f"- **Sweep Timestamp**: `{timestamp_str}`",
        f"- **Total Jobs In Intake**: `{total_jobs}`",
        f"- **Completed & Archived**: `{completed_moved}`",
        f"- **Pending Execution**: `{pending_count}`",
        f"- **Invalid / Flagged**: `{invalid_count}`",
        "",
        "## 1. Job Queue Status",
    ]

    details = sweep_results["job_details"]
    if not details:
        report_lines.append("No jobs found in intake folder. Queue is empty.")
    else:
        for idx, item in enumerate(details, start=1):
            name_str = item["file_name"]
            action_str = item["action_taken"]
            report_lines.append(f"{idx}. `{name_str}` -> **{action_str}**")
            for viol in item.get("violations", []):
                report_lines.append(f"   - *Violation*: {viol}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Job Lifecycle Coordinator tool."""
    argument_parser = argparse.ArgumentParser(
        description="job-lifecycle-coordinator: Autonomous JobMaker lifecycle and archival manager."
    )
    argument_parser.add_argument(
        "--sweep",
        action="store_true",
        help="Scan and sweep the jobs folder for pending/completed jobs.",
    )
    argument_parser.add_argument(
        "--jobs-dir",
        type=str,
        default=str(DEFAULT_JOBS_FOLDER),
        help=f"Path to jobs intake directory (default: {DEFAULT_JOBS_FOLDER}).",
    )
    argument_parser.add_argument(
        "--completed-dir",
        type=str,
        default=str(DEFAULT_COMPLETED_FOLDER),
        help=f"Path to completed jobs directory (default: {DEFAULT_COMPLETED_FOLDER}).",
    )
    argument_parser.add_argument(
        "--logs-dir",
        type=str,
        default=str(DEFAULT_LOGS_FOLDER),
        help=f"Path to job logs directory (default: {DEFAULT_LOGS_FOLDER}).",
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
        version=f"job_lifecycle_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    jobs_path = sanitize_directory_path(parsed_arguments.jobs_dir)
    completed_path = sanitize_directory_path(parsed_arguments.completed_dir)
    logs_path = sanitize_directory_path(parsed_arguments.logs_dir)

    try:
        results = sweep_and_process_jobs_folder(
            jobs_directory_path=jobs_path,
            completed_directory_path=completed_path,
            logs_directory_path=logs_path,
        )

        if parsed_arguments.json:
            print(json.dumps(results, indent=2))
        else:
            report_markdown = generate_lifecycle_markdown_report(results)
            print(report_markdown)

        if results["invalid_jobs_count"] > 0:
            return EXIT_JOB_FAILURES_DETECTED
        return EXIT_CLEAN_PASS

    except Exception as runtime_error:
        sys.stderr.write(f"Fatal error during job lifecycle sweep: {runtime_error}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
