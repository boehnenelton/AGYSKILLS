#!/usr/bin/env python3
"""
job_template_tool.py
Layer 5 JobMaker 104a Template & DAG Composition Engine
Composes, parameterizes, and emits compliant JobMaker BEJSON 104a job documents.

Policy Anchors:
  Policy §6.1: Long Self-Describing Variable Standard
  Policy §6.2: BEJSON Core Mandate
"""

import argparse
import datetime
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_COMPOSITION_ERROR = 30


def get_current_date_string_iso() -> str:
    """Return formatted UTC date string YYYY-MM-DD."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def sanitize_output_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def slugify_string(text_string: str) -> str:
    """Convert string to safe kebab-case filename slug."""
    clean_text = re.sub(r"[^\w\s-]", "", text_string.lower())
    return re.sub(r"[-\s]+", "_", clean_text).strip("-_")[:48]


def compose_jobmaker_document(
    job_goal_text: str,
    job_type_token: str,
    task_titles_list: List[str],
    contextualize_plan_flag: bool = True,
    contextualize_last_flag: bool = True,
) -> Dict[str, Any]:
    """Compose complete JobMaker BEJSON 104a data dictionary."""
    creation_date_str = get_current_date_string_iso()

    canonical_fields_definition = [
        {"name": "task_id", "type": "string"},
        {"name": "task_order", "type": "integer"},
        {"name": "task_title", "type": "string"},
        {"name": "task_description", "type": "string"},
        {"name": "task_context", "type": "string"},
        {"name": "task_reference", "type": "string"},
        {"name": "task_mandatory", "type": "boolean"},
        {"name": "is_completed", "type": "boolean"},
        {"name": "audit_enabled", "type": "boolean"},
        {"name": "audit_passed", "type": "boolean"},
        {"name": "audit_fail_reason", "type": "string"},
    ]

    values_data_rows: List[List[Any]] = []
    for index_counter, single_title_text in enumerate(task_titles_list, start=1):
        task_uuid_string = f"task_{uuid.uuid4().hex[:12]}"
        task_row_item = [
            task_uuid_string,
            index_counter,
            single_title_text.strip(),
            f"Execute step {index_counter}: {single_title_text.strip()}.",
            "",
            "",
            True,
            False,
            True,
            None,
            "",
        ]
        values_data_rows.append(task_row_item)

    job_document_dictionary: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Schema_Name": "Job Schema",
        "Schema_Version": "1.0",
        "Records_Type": ["JobTask"],
        "Job_Goal": job_goal_text,
        "Job_Type": job_type_token,
        "Job_Subtype": "workflow",
        "Contextualize_Plan": contextualize_plan_flag,
        "Contextualize_Last": contextualize_last_flag,
        "Job_Complete": False,
        "Creation_Date": creation_date_str,
        "Completion_Date": "",
        "Fields": canonical_fields_definition,
        "Values": values_data_rows,
    }
    return job_document_dictionary


def main() -> int:
    """CLI entrypoint for Job Template Composer tool."""
    argument_parser = argparse.ArgumentParser(
        description="job-template-composer: Composes JobMaker BEJSON 104a templates and task DAGs."
    )
    argument_parser.add_argument(
        "--goal",
        type=str,
        required=True,
        help="High-level mission or goal description for the job.",
    )
    argument_parser.add_argument(
        "--type",
        type=str,
        default="coding",
        help="Primary domain classification (coding, writing, audit, media). Default: 'coding'.",
    )
    argument_parser.add_argument(
        "--tasks",
        type=str,
        default="",
        help="Comma-separated list of task titles.",
    )
    argument_parser.add_argument(
        "--from-file",
        type=str,
        default=None,
        help="Path to Markdown file containing task checklists (- [ ] Step).",
    )
    argument_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Target output file path (defaults to jobs/<slug>.bejson).",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Print composed BEJSON document to stdout.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"job_template_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    task_titles_list: List[str] = []
    if parsed_arguments.from_file:
        checklist_file_path = sanitize_output_path(parsed_arguments.from_file)
        if not checklist_file_path.is_file():
            sys.stderr.write(f"Error: Specified checklist file does not exist: {checklist_file_path}\n")
            return EXIT_PATH_FAILURE
        try:
            content_text = checklist_file_path.read_text(encoding="utf-8")
            extracted_tasks = re.findall(r"^[-*]\s*\[[ xX]?\]\s*(.+)$", content_text, re.MULTILINE)
            task_titles_list.extend([t.strip() for t in extracted_tasks if t.strip()])
        except Exception as read_exception:
            sys.stderr.write(f"Error reading checklist file: {read_exception}\n")
            return EXIT_PATH_FAILURE
    elif parsed_arguments.tasks:
        task_titles_list = [t.strip() for t in parsed_arguments.tasks.split(",") if t.strip()]

    if not task_titles_list:
        task_titles_list = ["Initialize environment", "Implement primary deliverable", "Validate output"]

    try:
        composed_doc = compose_jobmaker_document(
            job_goal_text=parsed_arguments.goal,
            job_type_token=parsed_arguments.type,
            task_titles_list=task_titles_list,
        )

        if parsed_arguments.json:
            print(json.dumps(composed_doc, indent=2))

        if parsed_arguments.output:
            output_file_path = sanitize_output_path(parsed_arguments.output)
        else:
            slug_token = slugify_string(parsed_arguments.goal)
            output_file_path = Path("jobs") / f"{slug_token}.bejson"

        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file_path, "w", encoding="utf-8") as file_write_handle:
            json.dump(composed_doc, file_write_handle, indent=2)

        sys.stderr.write(f"Composed JobMaker BEJSON 104a saved to: {output_file_path}\n")
        return EXIT_CLEAN_PASS

    except Exception as composition_exception:
        sys.stderr.write(f"Fatal error during job composition: {composition_exception}\n")
        return EXIT_COMPOSITION_ERROR


if __name__ == "__main__":
    sys.exit(main())
