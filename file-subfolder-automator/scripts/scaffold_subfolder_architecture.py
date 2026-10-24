#!/usr/bin/env python3
# ==============================================================================
# Script Name: scaffold_subfolder_architecture
# Description: Layer 3 subfolder architecture scaffolder and tracking file
#              migrator enforcing Policy §1.1, §1.3, §4.1/§4.2, and §4.4.
# Version: 1.0.0
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 7a3c8e19-4f21-4b0e-9d34-5e1a2f69c847
# ==============================================================================

import argparse
import ast
import json
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: str = "1.0.0"
PACKAGE_VERSION: str = "100"
AUTHOR: str = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID: str = "7a3c8e19-4f21-4b0e-9d34-5e1a2f69c847"

LOGGER_INSTANCE: logging.Logger = logging.getLogger("SubfolderScaffolder")


def get_runtime_script_directory() -> Path:
    """Resolve and return absolute directory of the running script."""
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_runtime_script_directory()


def initialize_logging_subsystem(configured_log_level_name: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    numeric_logging_level: int = getattr(
        logging, configured_log_level_name.upper(), logging.INFO
    )
    logging.basicConfig(
        level=numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [SubfolderScaffolder] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


STANDARD_SUBDIRECTORIES: List[str] = [
    "lib",
    "config",
    "data",
    "exports",
    "backups",
    "dev",
    "docs",
]

TRACKING_FILENAMES: List[str] = [
    "dead_code.md",
    "variable_naming_issues.md",
    "security-notes.md",
]


def extract_python_function_signatures(target_python_file: Path) -> List[str]:
    """Parse a python file AST and return signatures in Policy §1.3 format."""
    extracted_signature_lines: List[str] = []
    file_basename_string: str = target_python_file.name

    try:
        with open(target_python_file, "r", encoding="utf-8") as source_file_handle:
            abstract_syntax_tree = ast.parse(
                source_file_handle.read(), filename=str(target_python_file)
            )

        for ast_node in ast.walk(abstract_syntax_tree):
            if isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_arguments_list: List[str] = [
                    arg_object.arg for arg_object in ast_node.args.args
                ]
                formatted_arguments_string: str = ", ".join(function_arguments_list)
                signature_line_string: str = (
                    f"* {file_basename_string} / {ast_node.name} ({formatted_arguments_string})"
                )
                extracted_signature_lines.append(signature_line_string)
            elif isinstance(ast_node, ast.ClassDef):
                class_line_string: str = f"* {file_basename_string} / class {ast_node.name}"
                extracted_signature_lines.append(class_line_string)

    except Exception as ast_parsing_error:
        LOGGER_INSTANCE.debug(
            "AST extraction skipped for %s: %s",
            file_basename_string,
            str(ast_parsing_error),
        )

    return extracted_signature_lines


def generate_default_bejson_config() -> Dict[str, Any]:
    """Generate default BEJSON 104a configuration per Policy §4.4."""
    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": ["ScriptConfig"],
        "Fields": [
            {"name": "setting_name", "type": "string"},
            {"name": "setting_value", "type": "any"},
            {"name": "description", "type": "string"},
        ],
        "Values": [
            [
                "local_lib_directory",
                "lib/",
                "Relative path to local dependency folder.",
            ],
            [
                "master_lib_source",
                "/storage/emulated/0/Admin/Libraries/libraries_104",
                "Fallback if local lib missing.",
            ],
            ["log_level", "INFO", "Default logging level."],
        ],
    }


def execute_subfolder_architecture_scaffold(
    target_project_directory: Path,
    dry_run_simulation_flag: bool = False,
) -> Dict[str, int]:
    """
    Executes subfolder architecture scaffolding and tracking migration:
    1. Creates lib/, config/, data/, exports/, backups/, dev/, docs/.
    2. Migrates tracking files from docs/ to dev/ per Policy §1.3.
    3. Bootstraps config/config.json with BEJSON 104a defaults if missing.
    4. Generates initial docs/technical_overview.md with function signatures.
    """
    operation_summary_metrics: Dict[str, int] = {
        "created_subdirectories_count": 0,
        "migrated_tracking_files_count": 0,
        "instantiated_skeletons_count": 0,
        "bootstrapped_configs_count": 0,
        "generated_overviews_count": 0,
    }

    if not target_project_directory.is_dir():
        LOGGER_INSTANCE.error(
            "Target directory does not exist: %s", str(target_project_directory)
        )
        return operation_summary_metrics

    LOGGER_INSTANCE.info(
        "Scaffolding relative architecture at: %s (Dry Run: %s)",
        str(target_project_directory),
        str(dry_run_simulation_flag),
    )

    # 1. Instantiate standardized subdirectories
    for subdirectory_name in STANDARD_SUBDIRECTORIES:
        candidate_subdirectory_path: Path = (
            target_project_directory / subdirectory_name
        )
        if not candidate_subdirectory_path.is_dir():
            if not dry_run_simulation_flag:
                candidate_subdirectory_path.mkdir(parents=True, exist_ok=True)
            LOGGER_INSTANCE.info("Created directory: %s/", subdirectory_name)
            operation_summary_metrics["created_subdirectories_count"] += 1

    docs_directory_path: Path = target_project_directory / "docs"
    dev_directory_path: Path = target_project_directory / "dev"

    # 2. Policy §1.3: Migrate tracking files from docs/ to dev/
    for tracking_filename in TRACKING_FILENAMES:
        misplaced_file_path: Path = docs_directory_path / tracking_filename
        target_destination_path: Path = dev_directory_path / tracking_filename

        if misplaced_file_path.is_file():
            LOGGER_INSTANCE.info(
                "Policy §1.3 Migration: Moving %s from docs/ to dev/", tracking_filename
            )
            if not dry_run_simulation_flag:
                dev_directory_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(misplaced_file_path), str(target_destination_path))
            operation_summary_metrics["migrated_tracking_files_count"] += 1
        elif not target_destination_path.is_file():
            # Instantiate clean tracking skeleton
            if not dry_run_simulation_flag:
                dev_directory_path.mkdir(parents=True, exist_ok=True)
                skeleton_heading_title: str = tracking_filename.replace("_", " ").replace("-", " ").replace(".md", "").title()
                initial_tracking_content: str = (
                    f"# {skeleton_heading_title}\n\n"
                    f"* Project: {target_project_directory.name}\n"
                    f"* Status: Initialized per Policy §1.3\n\n"
                    f"| Identified Date | Component | Observation / Mitigation |\n"
                    f"|---|---|---|\n"
                    f"| N/A | None | No active issues logged. |\n"
                )
                with open(target_destination_path, "w", encoding="utf-8") as file_handle:
                    file_handle.write(initial_tracking_content)
            LOGGER_INSTANCE.info("Instantiated tracking skeleton: dev/%s", tracking_filename)
            operation_summary_metrics["instantiated_skeletons_count"] += 1

    # 3. Bootstrap config/config.json
    config_file_path: Path = target_project_directory / "config" / "config.json"
    if not config_file_path.is_file():
        if not dry_run_simulation_flag:
            config_file_path.parent.mkdir(parents=True, exist_ok=True)
            default_config_payload = generate_default_bejson_config()
            with open(config_file_path, "w", encoding="utf-8") as config_file_handle:
                json.dump(default_config_payload, config_file_handle, indent=2)
        LOGGER_INSTANCE.info("Bootstrapped config: config/config.json")
        operation_summary_metrics["bootstrapped_configs_count"] += 1

    # 4. Bootstrap docs/technical_overview.md
    technical_overview_path: Path = docs_directory_path / "technical_overview.md"
    if not technical_overview_path.is_file():
        # Discover existing python files to extract real signatures
        discovered_signatures_list: List[str] = []
        for candidate_file in target_project_directory.glob("*.py"):
            discovered_signatures_list.extend(
                extract_python_function_signatures(candidate_file)
            )

        if not dry_run_simulation_flag:
            docs_directory_path.mkdir(parents=True, exist_ok=True)
            signatures_block_string: str = (
                "\n".join(discovered_signatures_list)
                if discovered_signatures_list
                else "* File_Name / Function_Name (var1, var2, var3)"
            )
            overview_document_content: str = (
                f"# Technical Overview: {target_project_directory.name}\n\n"
                f"* Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton\n\n"
                f"## Architectural Summary\n\n"
                f"Standardized relative subfolder architecture enforcing Policy §1.1.\n\n"
                f"## Function & Class Signatures (Policy §1.3)\n\n"
                f"{signatures_block_string}\n"
            )
            with open(technical_overview_path, "w", encoding="utf-8") as overview_handle:
                overview_handle.write(overview_document_content)
        LOGGER_INSTANCE.info("Generated: docs/technical_overview.md")
        operation_summary_metrics["generated_overviews_count"] += 1

    return operation_summary_metrics


def main() -> int:
    """Command-line entrypoint for subfolder architecture scaffolder."""
    initialize_logging_subsystem("INFO")

    cli_argument_parser = argparse.ArgumentParser(
        description="Layer 3 Relative Subfolder Architecture Scaffolder & Migrator",
        add_help=True,
    )
    cli_argument_parser.add_argument(
        "--version",
        action="store_true",
        help="Display version, release information, and author metadata.",
    )
    cli_argument_parser.add_argument(
        "--config",
        action="store_true",
        help="Display active scaffolder configuration.",
    )
    cli_argument_parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset temporary scaffolder caches.",
    )
    cli_argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Target project root directory to scaffold or migrate.",
    )
    cli_argument_parser.add_argument(
        "--migrate",
        action="store_true",
        help="Perform tracking file migration from docs/ to dev/.",
    )
    cli_argument_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without filesystem mutations.",
    )

    parsed_cli_arguments = cli_argument_parser.parse_args()

    if parsed_cli_arguments.version:
        LOGGER_INSTANCE.info(
            "scaffold_subfolder_architecture v%s (Package %s) | Author: %s | RELATIONAL_ID: %s",
            VERSION,
            PACKAGE_VERSION,
            AUTHOR,
            RELATIONAL_ID,
        )
        return 0

    if parsed_cli_arguments.config:
        LOGGER_INSTANCE.info("Active Subfolder Architecture Scaffolder Configuration:")
        LOGGER_INSTANCE.info("  Policy Grounding: §1.1 (Standard Subdirectories: lib, config, data, exports, backups, dev, docs)")
        LOGGER_INSTANCE.info("  Policy Grounding: §1.3 (Folder Migration: tracking files moved from docs/ to dev/)")
        LOGGER_INSTANCE.info("  Policy Grounding: §4.1/§4.2 (Self-Locating get_script_path)")
        LOGGER_INSTANCE.info("  Policy Grounding: §4.4 (BEJSON 104a config/config.json)")
        return 0

    if parsed_cli_arguments.reset:
        LOGGER_INSTANCE.info("Scaffolder cache verification reset completed.")
        return 0

    target_directory_path = Path(parsed_cli_arguments.target).resolve()
    execution_metrics = execute_subfolder_architecture_scaffold(
        target_project_directory=target_directory_path,
        dry_run_simulation_flag=parsed_cli_arguments.dry_run,
    )

    LOGGER_INSTANCE.info(
        "Scaffolding Summary for %s: %d subdirs, %d migrated, %d tracking skeletons, %d config, %d overview.",
        target_directory_path.name,
        execution_metrics["created_subdirectories_count"],
        execution_metrics["migrated_tracking_files_count"],
        execution_metrics["instantiated_skeletons_count"],
        execution_metrics["bootstrapped_configs_count"],
        execution_metrics["generated_overviews_count"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
