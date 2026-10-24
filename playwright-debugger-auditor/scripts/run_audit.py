#!/usr/bin/env python3
"""
Name: Playwright_Debugger_Auditor_CLI
Description: Layer 2 black-box Playwright diagnostic auditor CLI for web applications, SPAs, and JS games.
Version: 1.0.0
Date Created: 2026-10-23
Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 4a9f1b28-7e33-4c92-b062-8e12d4a51980
"""

import argparse
import asyncio
import datetime
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

VERSION = "1.0.0"

# Self-locating preamble adhering to Policy 4.1
def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()

# Link to core debugger library located in downloads/Playwright_Debugger
CORE_DEBUGGER_PATH = Path.home() / "downloads" / "Playwright_Debugger"
if CORE_DEBUGGER_PATH.exists():
    sys.path.insert(0, str(CORE_DEBUGGER_PATH))

from lib.browser_prober import HeadlessBrowserProber
from lib.diagnostic_analyzer import WebGameDiagnosticAnalyzer
from lib.report_generator import DiagnosticReportGenerator
from lib.server_manager import LocalHttpServerManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Playwright_Debugger_Auditor")


def discover_html_entrypoint(search_root_directory: Path) -> Tuple[Optional[Path], Optional[Path]]:
    if not search_root_directory.exists():
        return None, None
    candidate_filenames = ["play.html", "index.html", "game.html", "app.html", "main.html"]
    for candidate_name in candidate_filenames:
        direct_file_match = search_root_directory / candidate_name
        if direct_file_match.is_file():
            return direct_file_match, search_root_directory
    for candidate_name in candidate_filenames:
        recursive_matches = list(search_root_directory.rglob(candidate_name))
        if len(recursive_matches) > 0:
            return recursive_matches[0], search_root_directory
    any_html_files = list(search_root_directory.rglob("*.html"))
    if len(any_html_files) > 0:
        return any_html_files[0], search_root_directory
    return None, None


async def execute_audit(
    target_path_input: str,
    explicit_file_entrypoint: Optional[str] = None,
    custom_query_string: Optional[str] = None,
    test_file_protocol_direct: bool = False,
    output_directory_override: Optional[str] = None,
) -> int:
    target_path = Path(target_path_input).resolve()
    if not target_path.exists():
        logger.error("Target path not found: %s", target_path)
        return 30

    entrypoint_html: Optional[Path] = None
    server_root: Optional[Path] = None

    if target_path.is_file():
        entrypoint_html = target_path
        server_root = target_path.parent
    elif explicit_file_entrypoint:
        candidate_file = target_path / explicit_file_entrypoint
        if candidate_file.is_file():
            entrypoint_html = candidate_file
            server_root = target_path
    else:
        entrypoint_html, server_root = discover_html_entrypoint(target_path)

    if entrypoint_html is None or server_root is None:
        logger.error("No valid HTML entrypoint found in %s", target_path)
        return 30

    output_base_dir = Path(output_directory_override) if output_directory_override else (CORE_DEBUGGER_PATH / "exports")
    screenshot_dir = output_base_dir / "screenshots"
    report_dir = output_base_dir / "reports"
    telemetry_dir = CORE_DEBUGGER_PATH / "data"

    session_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    server_instance: Optional[LocalHttpServerManager] = None
    target_url: str = ""

    if test_file_protocol_direct:
        target_url = f"file://{entrypoint_html}"
        if custom_query_string:
            target_url += f"?{custom_query_string.lstrip('?')}"
    else:
        server_instance = LocalHttpServerManager(target_serving_directory=str(server_root), preferred_server_port=8089)
        bound_port = server_instance.start_local_server()
        relative_path = entrypoint_html.relative_to(server_root).as_posix()
        target_url = f"http://127.0.0.1:{bound_port}/{relative_path}"
        if custom_query_string:
            target_url += f"?{custom_query_string.lstrip('?')}"

    prober = HeadlessBrowserProber(output_screenshot_directory=str(screenshot_dir), operation_timeout_ms=30000)

    try:
        telemetry_outcome = await prober.execute_probing_cycle(
            navigation_target_url=target_url,
            simulate_user_interactions=True,
            settle_delay_seconds=1.5,
        )
        analyzer = WebGameDiagnosticAnalyzer()
        diagnostic_outcome = analyzer.analyze_session_telemetry(telemetry_outcome)

        reporter = DiagnosticReportGenerator(exports_report_directory=str(report_dir), data_telemetry_directory=str(telemetry_dir))
        reporter.print_terminal_summary(telemetry_outcome, diagnostic_outcome)
        reporter.generate_markdown_report(telemetry_outcome, diagnostic_outcome, session_timestamp)
        reporter.generate_bejson_telemetry_file(telemetry_outcome, diagnostic_outcome, session_timestamp)

        if diagnostic_outcome.diagnostic_severity_level == "CRITICAL":
            return 20
        elif diagnostic_outcome.diagnostic_severity_level == "WARNING":
            return 10
        return 0

    finally:
        if server_instance is not None:
            server_instance.stop_local_server()


def main() -> None:
    parser = argparse.ArgumentParser(prog="run_audit.py", description="Execute Playwright L2 diagnostic audit on any target.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("target", type=str, help="Path to target directory, HTML file, or project")
    parser.add_argument("--file", type=str, default=None, help="Explicit HTML entrypoint")
    parser.add_argument("--query", type=str, default=None, help="Query parameters (e.g. 'mfdb=/path/to/db.json')")
    parser.add_argument("--direct-file", action="store_true", help="Audit via direct file:// protocol")
    parser.add_argument("--output", type=str, default=None, help="Override output directory")

    args = parser.parse_args()
    exit_code = asyncio.run(
        execute_audit(
            target_path_input=args.target,
            explicit_file_entrypoint=args.file,
            custom_query_string=args.query,
            test_file_protocol_direct=args.direct_file,
            output_directory_override=args.output,
        )
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
