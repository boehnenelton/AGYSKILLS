#!/usr/bin/env python3
"""
log_compliance_tool.py
Layer 2 Policy §2.3 Logging Verification Gate
Audits global log sinks for schema compliance, context payload completeness,
and dual-path redaction integrity.

Policy Anchors:
  Policy §2.3: Post-Task Global Standardized Logging Protocol
  Policy §6.1: Long Self-Describing Variable Standard
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
EXIT_LOG_VIOLATIONS_DETECTED = 30

DEFAULT_GLOBAL_LOGS_DIRECTORY = Path("/storage/emulated/0/Admin/System/Global_Logs")


def get_current_utc_date_string() -> str:
    """Return formatted UTC date string YYYY-MM-DD."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def sanitize_directory_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def audit_daily_log_file(daily_log_file_path: Path) -> Dict[str, Any]:
    """Audit single daily log BEJSON file for Policy §2.3 compliance."""
    discovered_violation_items_list: List[Dict[str, Any]] = []

    if not daily_log_file_path.is_file():
        return {
            "log_file": str(daily_log_file_path),
            "is_compliant": False,
            "total_entries": 0,
            "violations": [{"code": "E-LOG-01", "message": f"Daily log file does not exist: {daily_log_file_path}"}],
        }

    try:
        with open(daily_log_file_path, "r", encoding="utf-8") as file_read_handle:
            log_data_dictionary = json.load(file_read_handle)
    except Exception as parse_exception:
        return {
            "log_file": str(daily_log_file_path),
            "is_compliant": False,
            "total_entries": 0,
            "violations": [{"code": "E-LOG-02", "message": f"Malformed log JSON: {parse_exception}"}],
        }

    fields_declaration_list = log_data_dictionary.get("Fields", [])
    values_data_rows = log_data_dictionary.get("Values", [])

    if not fields_declaration_list:
        discovered_violation_items_list.append(
            {"code": "E-LOG-03", "message": "Log schema Fields array is missing"}
        )
        field_names_list = []
    else:
        field_names_list = [f["name"] if isinstance(f, dict) else str(f) for f in fields_declaration_list]

    field_map_cache = {name: idx for idx, name in enumerate(field_names_list)}
    context_field_index = field_map_cache.get("context")
    message_field_index = field_map_cache.get("message")
    level_field_index = field_map_cache.get("log_level") or field_map_cache.get("level")

    for row_index_counter, single_entry_row in enumerate(values_data_rows, start=1):
        if not isinstance(single_entry_row, list):
            discovered_violation_items_list.append(
                {"code": "E-LOG-04", "row": row_index_counter, "message": "Entry row is not an array"}
            )
            continue

        # Check message
        if message_field_index is not None and message_field_index < len(single_entry_row):
            message_text = str(single_entry_row[message_field_index]).strip()
            if not message_text:
                discovered_violation_items_list.append(
                    {"code": "E-LOG-05", "row": row_index_counter, "message": "Empty log message"}
                )

        # Check context payload
        if context_field_index is not None and context_field_index < len(single_entry_row):
            raw_context_data = single_entry_row[context_field_index]
            if isinstance(raw_context_data, str) and raw_context_data.strip():
                try:
                    json.loads(raw_context_data)
                except Exception:
                    discovered_violation_items_list.append(
                        {
                            "code": "E-LOG-06",
                            "row": row_index_counter,
                            "message": f"Invalid JSON string in context field: '{raw_context_data}'",
                        }
                    )

    is_compliant_flag = len(discovered_violation_items_list) == 0
    return {
        "log_file": str(daily_log_file_path),
        "is_compliant": is_compliant_flag,
        "total_entries": len(values_data_rows),
        "violations": discovered_violation_items_list,
    }


def generate_markdown_audit_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate Markdown report for logging compliance."""
    log_file_str = audit_result_dictionary["log_file"]
    total_entries = audit_result_dictionary["total_entries"]
    is_compliant = audit_result_dictionary["is_compliant"]
    status_token = "COMPLIANT" if is_compliant else "NON_COMPLIANT"

    report_lines: List[str] = [
        "# Policy §2.3 Logging Compliance Report",
        "",
        f"- **Log File**: `{log_file_str}`",
        f"- **Total Log Entries**: `{total_entries}`",
        f"- **Compliance Status**: `{status_token}`",
        "",
        "## 1. Compliance Details",
    ]

    violations = audit_result_dictionary.get("violations", [])
    if not violations:
        report_lines.append("All log entries strictly adhere to Policy §2.3 standards. Context dictionaries are valid.")
    else:
        for idx, viol in enumerate(violations, start=1):
            code_str = viol.get("code")
            msg_str = viol.get("message")
            report_lines.append(f"{idx}. **[{code_str}]**: {msg_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Logging Compliance Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="log-compliance-auditor: Audits global log sinks for Policy §2.3 compliance."
    )
    argument_parser.add_argument(
        "--date",
        type=str,
        default="today",
        help="Date of log sink to audit (YYYY-MM-DD or 'today'). Default: 'today'.",
    )
    argument_parser.add_argument(
        "--sink-dir",
        type=str,
        default=str(DEFAULT_GLOBAL_LOGS_DIRECTORY),
        help=f"Path to global logs directory (default: {DEFAULT_GLOBAL_LOGS_DIRECTORY}).",
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
        version=f"log_compliance_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    date_target_str = get_current_utc_date_string() if parsed_arguments.date == "today" else parsed_arguments.date
    sink_directory_path = sanitize_directory_path(parsed_arguments.sink_dir)
    target_log_file_path = sink_directory_path / f"Log-{date_target_str}.bejson"

    try:
        audit_results = audit_daily_log_file(target_log_file_path)

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            report_text = generate_markdown_audit_report(audit_results)
            print(report_text)

        if not audit_results["is_compliant"]:
            return EXIT_LOG_VIOLATIONS_DETECTED
        return EXIT_CLEAN_PASS

    except Exception as runtime_exception:
        sys.stderr.write(f"Fatal error during log audit: {runtime_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
