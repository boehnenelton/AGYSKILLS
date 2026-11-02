#!/usr/bin/env python3
"""
log_analytics_tool.py
Layer 4 BEJSON Daily Log Analytics & Telemetry Engine
Aggregates, decomposes, and computes operational KPIs from historical daily logs.

Policy Anchors:
  Policy §2.3: Post-Task Global Standardized Logging Protocol
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_INGESTION_ERROR = 30

DEFAULT_GLOBAL_LOGS_DIRECTORY = Path("/storage/emulated/0/Admin/System/Global_Logs")


def sanitize_directory_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def parse_single_log_bejson(log_file_path: Path) -> List[Dict[str, Any]]:
    """Parse single daily log BEJSON file into list of row dictionaries."""
    if not log_file_path.is_file():
        return []
    try:
        with open(log_file_path, "r", encoding="utf-8") as file_read_handle:
            data = json.load(file_read_handle)
            fields = data.get("Fields", [])
            values = data.get("Values", [])
            if not fields or not values:
                return []
            field_names = [f["name"] if isinstance(f, dict) else str(f) for f in fields]
            row_dicts: List[Dict[str, Any]] = []
            for val_row in values:
                if isinstance(val_row, list) and len(val_row) == len(field_names):
                    row_dicts.append(dict(zip(field_names, val_row)))
            return row_dicts
    except Exception:
        return []


def decompose_log_analytics(
    global_logs_directory_path: Path,
    lookback_days_count: int = 7,
) -> Dict[str, Any]:
    """Aggregate log metrics across lookback window."""
    aggregated_metrics: Dict[str, Any] = {
        "analysis_timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lookback_days": lookback_days_count,
        "logs_directory": str(global_logs_directory_path),
        "total_files_analyzed": 0,
        "total_entries_count": 0,
        "level_distribution": {},
        "subsystem_distribution": {},
        "category_distribution": {},
        "error_entries_list": [],
    }

    if not global_logs_directory_path.exists():
        return aggregated_metrics

    # Find matching log files
    log_files_list = sorted(list(global_logs_directory_path.glob("Log-*.bejson")))
    if not log_files_list:
        return aggregated_metrics

    # Filter to lookback window
    recent_log_files = log_files_list[-lookback_days_count:]
    aggregated_metrics["total_files_analyzed"] = len(recent_log_files)

    level_counter = Counter()
    subsystem_counter = Counter()
    category_counter = Counter()
    errors_list: List[Dict[str, Any]] = []
    total_entries = 0

    for single_log_file in recent_log_files:
        row_entries = parse_single_log_bejson(single_log_file)
        for entry in row_entries:
            total_entries += 1
            lvl = str(entry.get("log_level") or entry.get("level") or "INFO").upper()
            sub = str(entry.get("subsystem") or "general")
            cat = str(entry.get("category") or "uncategorized")

            level_counter[lvl] += 1
            subsystem_counter[sub] += 1
            category_counter[cat] += 1

            if lvl in ("ERROR", "CRITICAL", "WARN"):
                errors_list.append(
                    {
                        "date": single_log_file.stem.replace("Log-", ""),
                        "level": lvl,
                        "subsystem": sub,
                        "message": entry.get("message", ""),
                    }
                )

    aggregated_metrics["total_entries_count"] = total_entries
    aggregated_metrics["level_distribution"] = dict(level_counter)
    aggregated_metrics["subsystem_distribution"] = dict(subsystem_counter.most_common(10))
    aggregated_metrics["category_distribution"] = dict(category_counter.most_common(10))
    aggregated_metrics["error_entries_list"] = errors_list[:20]

    return aggregated_metrics


def generate_analytics_markdown_report(metrics_dictionary: Dict[str, Any]) -> str:
    """Generate Markdown dashboard report from aggregated metrics."""
    timestamp_str = metrics_dictionary["analysis_timestamp"]
    files_analyzed = metrics_dictionary["total_files_analyzed"]
    total_entries = metrics_dictionary["total_entries_count"]
    levels = metrics_dictionary["level_distribution"]
    subsystems = metrics_dictionary["subsystem_distribution"]
    errors = metrics_dictionary["error_entries_list"]

    report_lines: List[str] = [
        "# Ecosystem Log Telemetry & KPI Report",
        "",
        f"- **Analysis Timestamp**: `{timestamp_str}`",
        f"- **Daily Sinks Analyzed**: `{files_analyzed}`",
        f"- **Total Operational Transactions**: `{total_entries}`",
        "",
        "## 1. Quality & Level Distribution",
        "",
        "| Log Level | Count | Share |",
        "| :--- | :---: | :---: |",
    ]

    for lvl, count in levels.items():
        share_pct = (count / total_entries * 100.0) if total_entries > 0 else 0.0
        report_lines.append(f"| `{lvl}` | {count} | {share_pct:.1f}% |")

    report_lines.extend(["", "## 2. Top Subsystems by Operational Volume", "", "| Subsystem | Actions Count |", "| :--- | :---: |"])
    for sub, count in subsystems.items():
        report_lines.append(f"| `{sub}` | {count} |")

    report_lines.extend(["", "## 3. Errors & Anomalies"])
    if not errors:
        report_lines.append("Zero runtime errors or critical warnings recorded in analysis window.")
    else:
        for err in errors:
            d_str = err.get("date")
            l_str = err.get("level")
            s_str = err.get("subsystem")
            m_str = err.get("message")
            report_lines.append(f"- **[{d_str} | {l_str} | {s_str}]**: {m_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Log Analytics Decomposer tool."""
    argument_parser = argparse.ArgumentParser(
        description="log-analytics-decomposer: Aggregates and decomposes historical daily BEJSON logs."
    )
    argument_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of lookback days to aggregate (default: 7).",
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
        help="Print raw JSON metrics to stdout.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"log_analytics_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    sink_path = sanitize_directory_path(parsed_arguments.sink_dir)

    try:
        metrics = decompose_log_analytics(sink_path, lookback_days_count=parsed_arguments.days)

        if parsed_arguments.json:
            print(json.dumps(metrics, indent=2))
        else:
            report_text = generate_analytics_markdown_report(metrics)
            print(report_text)

        return EXIT_CLEAN_PASS

    except Exception as general_error:
        sys.stderr.write(f"Fatal error during log analytics decomposition: {general_error}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
