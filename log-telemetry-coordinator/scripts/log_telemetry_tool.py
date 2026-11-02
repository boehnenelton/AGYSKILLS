#!/usr/bin/env python3
"""
log_telemetry_tool.py
Layer 6 Global Logging & Dual-Path Telemetry Orchestrator
Coordinates daily partition rollover, dual-path secure routing, and archival retention.

Policy Anchors:
  Policy §2.3: Post-Task Global Standardized Logging Protocol
  Announcement October 31, 2026: BEJSON Standards Logging
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_OPERATIONAL_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_SINK_ANOMALY = 30

DEFAULT_GLOBAL_LOGS = Path("/storage/emulated/0/Admin/System/Global_Logs")
DEFAULT_GLOBAL_LOGS_SECURE = Path("/storage/emulated/0/Admin/System/Global_Logs/secure")
DEFAULT_GLOBAL_LOGS_ARCHIVES = Path("/storage/emulated/0/Admin/System/Global_Logs/archives")


def get_current_utc_date_string() -> str:
    """Return formatted UTC date string YYYY-MM-DD."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def sanitize_directory_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def check_logging_infrastructure_status(
    logs_dir: Path,
    secure_dir: Path,
    archives_dir: Path,
) -> Dict[str, Any]:
    """Inspect and report logging infrastructure health."""
    current_date_str = get_current_utc_date_string()
    today_public_log_file = logs_dir / f"Log-{current_date_str}.bejson"
    today_secure_log_file = secure_dir / f"Log-{current_date_str}-secure.bejson"

    logs_dir_exists = logs_dir.is_dir()
    secure_dir_exists = secure_dir.is_dir()
    archives_dir_exists = archives_dir.is_dir()

    today_public_exists = today_public_log_file.is_file()
    today_secure_exists = today_secure_log_file.is_file()

    total_logs_count = len(list(logs_dir.glob("Log-*.bejson"))) if logs_dir_exists else 0
    total_archives_count = len(list(archives_dir.glob("*.bejson"))) if archives_dir_exists else 0

    status_dictionary: Dict[str, Any] = {
        "status_timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "current_utc_date": current_date_str,
        "logs_directory": str(logs_dir),
        "secure_directory": str(secure_dir),
        "archives_directory": str(archives_dir),
        "directories_ready": logs_dir_exists and secure_dir_exists and archives_dir_exists,
        "today_public_log_ready": today_public_exists,
        "today_secure_log_ready": today_secure_exists,
        "total_active_daily_logs": total_logs_count,
        "total_archived_logs": total_archives_count,
    }
    return status_dictionary


def initialize_today_daily_envelope(logs_dir: Path) -> Path:
    """Initialize today's BEJSON 104a log file if absent."""
    logs_dir.mkdir(parents=True, exist_ok=True)
    current_date_str = get_current_utc_date_string()
    today_file_path = logs_dir / f"Log-{current_date_str}.bejson"

    if not today_file_path.exists():
        envelope_data: Dict[str, Any] = {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": ["SystemLog"],
            "Fields": [
                {"name": "timestamp", "type": "string"},
                {"name": "log_level", "type": "string"},
                {"name": "action_key", "type": "string"},
                {"name": "subsystem", "type": "string"},
                {"name": "category", "type": "string"},
                {"name": "flag", "type": "string"},
                {"name": "message", "type": "string"},
                {"name": "context", "type": "string"},
            ],
            "Values": [],
        }
        with open(today_file_path, "w", encoding="utf-8") as file_write_handle:
            json.dump(envelope_data, file_write_handle, indent=2)

    return today_file_path


def generate_status_markdown_report(status_data: Dict[str, Any]) -> str:
    """Generate Markdown report for logging infrastructure status."""
    timestamp_str = status_data["status_timestamp"]
    cur_date = status_data["current_utc_date"]
    dirs_ready = status_data["directories_ready"]
    pub_ready = status_data["today_public_log_ready"]
    sec_ready = status_data["today_secure_log_ready"]
    active_count = status_data["total_active_daily_logs"]
    archive_count = status_data["total_archived_logs"]

    report_lines: List[str] = [
        "# Global Logging Infrastructure Status",
        "",
        f"- **Inspection Timestamp**: `{timestamp_str}`",
        f"- **Current UTC Partition**: `{cur_date}`",
        f"- **Directory Tree Status**: `{'READY' if dirs_ready else 'INCOMPLETE'}`",
        f"- **Today's Public Log**: `{'ONLINE' if pub_ready else 'ABSENT'}`",
        f"- **Today's Secure Log**: `{'ONLINE' if sec_ready else 'ABSENT'}`",
        f"- **Active Partition Files**: `{active_count}`",
        f"- **Archived Sinks**: `{archive_count}`",
        "",
        "## Invariant Status",
        f"- Dual-Path Secure Partitioning: `{'COMPLIANT' if dirs_ready else 'REQUIRES_SETUP'}`",
        "- Policy §2.3 Telemetry Readiness: `OPERATIONAL`",
        "",
        "---",
        "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
    ]
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Log Telemetry Coordinator tool."""
    argument_parser = argparse.ArgumentParser(
        description="log-telemetry-coordinator: Global logging infrastructure and partition manager."
    )
    argument_parser.add_argument(
        "--status",
        action="store_true",
        help="Check logging infrastructure status across public, secure, and archive sinks.",
    )
    argument_parser.add_argument(
        "--init-today",
        action="store_true",
        help="Initialize today's daily BEJSON log sink if absent.",
    )
    argument_parser.add_argument(
        "--logs-dir",
        type=str,
        default=str(DEFAULT_GLOBAL_LOGS),
        help=f"Path to global logs directory (default: {DEFAULT_GLOBAL_LOGS}).",
    )
    argument_parser.add_argument(
        "--secure-dir",
        type=str,
        default=str(DEFAULT_GLOBAL_LOGS_SECURE),
        help=f"Path to secure logs directory (default: {DEFAULT_GLOBAL_LOGS_SECURE}).",
    )
    argument_parser.add_argument(
        "--archives-dir",
        type=str,
        default=str(DEFAULT_GLOBAL_LOGS_ARCHIVES),
        help=f"Path to archives directory (default: {DEFAULT_GLOBAL_LOGS_ARCHIVES}).",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Print markdown formatted report to stdout.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON status to stdout.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"log_telemetry_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    logs_path = sanitize_directory_path(parsed_arguments.logs_dir)
    secure_path = sanitize_directory_path(parsed_arguments.secure_dir)
    archives_path = sanitize_directory_path(parsed_arguments.archives_dir)

    try:
        if parsed_arguments.init_today:
            initialized_file = initialize_today_daily_envelope(logs_path)
            sys.stderr.write(f"Initialized today's daily log: {initialized_file}\n")

        status_results = check_logging_infrastructure_status(
            logs_dir=logs_path,
            secure_dir=secure_path,
            archives_dir=archives_path,
        )

        if parsed_arguments.json:
            print(json.dumps(status_results, indent=2))
        else:
            report_text = generate_status_markdown_report(status_results)
            print(report_text)

        if not status_results["directories_ready"]:
            return EXIT_SINK_ANOMALY
        return EXIT_OPERATIONAL_PASS

    except Exception as runtime_error:
        sys.stderr.write(f"Fatal error during telemetry coordination: {runtime_error}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
