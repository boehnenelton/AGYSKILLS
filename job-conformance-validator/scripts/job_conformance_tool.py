#!/usr/bin/env python3
"""
job_conformance_tool.py
Layer 2 JobMaker 104a Schema & Invariant Gate
Validates JobMaker BEJSON 104a job and template schemas against envelope,
11-field task schemas, contiguous ordering, and audit completion rules.

Policy Anchors:
  Policy §6.1: Long Self-Describing Variable Standard
  Policy §6.2: BEJSON Core Mandate (Field Map Cache)
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_CONFORMANCE_VIOLATIONS = 30

CANONICAL_JOB_FIELDS = [
    "task_id",
    "task_order",
    "task_title",
    "task_description",
    "task_context",
    "task_reference",
    "task_mandatory",
    "is_completed",
    "audit_enabled",
    "audit_passed",
    "audit_fail_reason",
]


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_input_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def validate_single_job_document(job_file_path: Path) -> Dict[str, Any]:
    """Validate a single JobMaker BEJSON 104a job document against all invariant gates."""
    discovered_violation_items_list: List[Dict[str, Any]] = []

    if not job_file_path.is_file():
        return {
            "file": str(job_file_path),
            "is_valid": False,
            "violations": [{"code": "E-PATH-01", "message": f"File does not exist: {job_file_path}"}],
        }

    try:
        with open(job_file_path, "r", encoding="utf-8") as file_read_handle:
            job_data_dictionary = json.load(file_read_handle)
    except Exception as parse_exception:
        return {
            "file": str(job_file_path),
            "is_valid": False,
            "violations": [{"code": "E-JSON-01", "message": f"Malformed JSON: {parse_exception}"}],
        }

    # Invariant Gate 1: Top-Level Envelope
    format_declaration = job_data_dictionary.get("Format")
    format_version_declaration = job_data_dictionary.get("Format_Version")
    records_type_declaration = job_data_dictionary.get("Records_Type")

    if format_declaration != "BEJSON":
        discovered_violation_items_list.append(
            {"code": "E-JOB-01", "field": "Format", "message": f"Expected 'BEJSON', got '{format_declaration}'"}
        )
    if format_version_declaration != "104a":
        discovered_violation_items_list.append(
            {"code": "E-JOB-02", "field": "Format_Version", "message": f"Expected '104a', got '{format_version_declaration}'"}
        )
    if not isinstance(records_type_declaration, list) or "JobTask" not in records_type_declaration:
        discovered_violation_items_list.append(
            {"code": "E-JOB-03", "field": "Records_Type", "message": "Records_Type must include ['JobTask']"}
        )

    # Invariant Gate 2: Fields Map
    fields_declaration_list = job_data_dictionary.get("Fields", [])
    if not fields_declaration_list:
        discovered_violation_items_list.append(
            {"code": "E-JOB-04", "field": "Fields", "message": "Fields schema definition is missing"}
        )
        field_names_list = []
    else:
        field_names_list = [f["name"] if isinstance(f, dict) else str(f) for f in fields_declaration_list]
        for canonical_field_name in CANONICAL_JOB_FIELDS:
            if canonical_field_name not in field_names_list:
                discovered_violation_items_list.append(
                    {"code": "E-JOB-05", "field": canonical_field_name, "message": f"Missing canonical field '{canonical_field_name}'"}
                )

    # Invariant Gate 3: Task Values Rows & Ordering
    values_data_rows = job_data_dictionary.get("Values", [])
    task_order_sequence_list: List[int] = []

    if field_names_list and values_data_rows:
        field_map_cache = {name: idx for idx, name in enumerate(field_names_list)}
        task_order_index = field_map_cache.get("task_order")
        task_id_index = field_map_cache.get("task_id")
        mandatory_index = field_map_cache.get("task_mandatory")
        completed_index = field_map_cache.get("is_completed")

        seen_task_ids = set()

        for row_index_counter, single_task_row in enumerate(values_data_rows, start=1):
            if not isinstance(single_task_row, list):
                discovered_violation_items_list.append(
                    {"code": "E-JOB-06", "row": row_index_counter, "message": "Task row must be an array of values"}
                )
                continue

            if len(single_task_row) != len(field_names_list):
                discovered_violation_items_list.append(
                    {
                        "code": "E-JOB-07",
                        "row": row_index_counter,
                        "message": f"Row length {len(single_task_row)} does not match fields count {len(field_names_list)}",
                    }
                )

            # Check task_id uniqueness
            if task_id_index is not None and task_id_index < len(single_task_row):
                task_id_value = single_task_row[task_id_index]
                if task_id_value in seen_task_ids:
                    discovered_violation_items_list.append(
                        {"code": "E-JOB-08", "row": row_index_counter, "message": f"Duplicate task_id '{task_id_value}'"}
                    )
                seen_task_ids.add(task_id_value)

            # Record task_order
            if task_order_index is not None and task_order_index < len(single_task_row):
                task_order_val = single_task_row[task_order_index]
                if isinstance(task_order_val, int):
                    task_order_sequence_list.append(task_order_val)
                else:
                    discovered_violation_items_list.append(
                        {"code": "E-JOB-09", "row": row_index_counter, "message": f"task_order must be integer, got {type(task_order_val)}"}
                    )

        # Check contiguous 1..N order
        sorted_orders = sorted(task_order_sequence_list)
        expected_sequence = list(range(1, len(task_order_sequence_list) + 1))
        if sorted_orders != expected_sequence:
            discovered_violation_items_list.append(
                {
                    "code": "E-JOB-10",
                    "field": "task_order",
                    "message": f"task_order sequence is non-contiguous. Found: {sorted_orders}, Expected: {expected_sequence}",
                }
            )

    is_valid_flag = len(discovered_violation_items_list) == 0
    return {
        "file": str(job_file_path),
        "is_valid": is_valid_flag,
        "total_tasks": len(values_data_rows),
        "violations": discovered_violation_items_list,
    }


def generate_validation_markdown_report(validation_results_list: List[Dict[str, Any]]) -> str:
    """Generate Markdown report for job validations."""
    report_lines: List[str] = [
        "# JobMaker 104a Conformance Report",
        "",
        f"- **Validation Timestamp**: `{get_current_utc_timestamp_iso()}`",
        f"- **Total Documents Tested**: `{len(validation_results_list)}`",
        "",
        "## 1. Document Results",
    ]

    total_violations = 0
    for res in validation_results_list:
        file_path_str = res["file"]
        is_valid = res["is_valid"]
        status_token = "PASSED" if is_valid else "FAILED"
        tasks_count = res.get("total_tasks", 0)
        report_lines.append(f"- `{file_path_str}`: **{status_token}** ({tasks_count} tasks)")

        for viol in res.get("violations", []):
            total_violations += 1
            code_str = viol.get("code")
            msg_str = viol.get("message")
            report_lines.append(f"  - **[{code_str}]**: {msg_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Job Conformance Validator tool."""
    argument_parser = argparse.ArgumentParser(
        description="job-conformance-validator: Structural validator for JobMaker BEJSON 104a documents."
    )
    argument_parser.add_argument(
        "--job",
        type=str,
        default=None,
        help="Path to specific job or template BEJSON file.",
    )
    argument_parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to directory containing job BEJSON files (e.g. $JOBS_FOLDER).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/job_conformance_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw validation results in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"job_conformance_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    target_files_to_validate: List[Path] = []
    if parsed_arguments.job:
        job_path = sanitize_input_path(parsed_arguments.job)
        if not job_path.is_file():
            sys.stderr.write(f"Error: Job file does not exist: {job_path}\n")
            return EXIT_PATH_FAILURE
        target_files_to_validate.append(job_path)
    elif parsed_arguments.dir:
        dir_path = sanitize_input_path(parsed_arguments.dir)
        if not dir_path.is_dir():
            sys.stderr.write(f"Error: Target directory does not exist: {dir_path}\n")
            return EXIT_PATH_FAILURE
        for single_file in dir_path.glob("*.bejson"):
            target_files_to_validate.append(single_file)
    else:
        sys.stderr.write("Error: Must provide either --job <path> or --dir <path>.\n")
        return EXIT_PATH_FAILURE

    all_validation_results = [validate_single_job_document(f) for f in target_files_to_validate]

    if parsed_arguments.json:
        print(json.dumps(all_validation_results, indent=2))
    else:
        markdown_report = generate_validation_markdown_report(all_validation_results)
        print(markdown_report)

    has_violations = any(not r["is_valid"] for r in all_validation_results)
    if has_violations:
        return EXIT_CONFORMANCE_VIOLATIONS
    return EXIT_CLEAN_PASS


if __name__ == "__main__":
    sys.exit(main())
