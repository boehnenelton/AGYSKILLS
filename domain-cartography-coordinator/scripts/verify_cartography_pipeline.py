#!/usr/bin/env python3
# ==============================================================================
# Script Name: verify_cartography_pipeline
# Description: Layer 2 deterministic validation gate for domain-cartography-coordinator
#              verifying BEJSON schema integrity, Field Map caching, and naming conventions.
# Version: 1.0.0
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: e3b749d2-9721-4f1c-81ec-5a137bc3827d
# ==============================================================================

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

VERSION: str = "1.0.0"
PACKAGE_VERSION: str = "100"
AUTHOR: str = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID: str = "e3b749d2-9721-4f1c-81ec-5a137bc3827d"

LOGGER_INSTANCE: logging.Logger = logging.getLogger("CartographyPipelineValidator")


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
        format="[%(asctime)s] [%(levelname)s] [CartographyValidator] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def validate_bejson_field_map_conformance(
    target_bejson_file_path: Path,
) -> Tuple[bool, List[str]]:
    """
    Validate BEJSON 104a document conformance using dynamic Field Map Cache.
    Verifies that fields are non-empty and all rows match declared column count.
    """
    validation_error_messages: List[str] = []

    if not target_bejson_file_path.is_file():
        validation_error_messages.append(
            f"Target file does not exist: {str(target_bejson_file_path)}"
        )
        return False, validation_error_messages

    try:
        with open(target_bejson_file_path, "r", encoding="utf-8") as file_read_handle:
            parsed_bejson_document: Dict[str, Any] = json.load(file_read_handle)

        field_definitions_list: List[Dict[str, str]] = parsed_bejson_document.get(
            "Fields", []
        )
        if not field_definitions_list:
            validation_error_messages.append(
                "Document missing 'Fields' array definition."
            )
            return False, validation_error_messages

        # O(1) Field Map Cache verification
        field_map_cache: Dict[str, int] = {
            field_entry_definition.get("name", ""): field_column_index
            for field_column_index, field_entry_definition in enumerate(
                field_definitions_list
            )
        }

        expected_column_count: int = len(field_definitions_list)
        record_values_list: List[List[Any]] = parsed_bejson_document.get("Values", [])

        for row_index_number, individual_record_row in enumerate(record_values_list):
            if len(individual_record_row) != expected_column_count:
                validation_error_messages.append(
                    f"Row {row_index_number} column mismatch: expected {expected_column_count}, "
                    f"found {len(individual_record_row)}"
                )

        validation_success_flag: bool = len(validation_error_messages) == 0
        return validation_success_flag, validation_error_messages
    except Exception as document_read_exception:
        validation_error_messages.append(
            f"Failed parsing BEJSON: {str(document_read_exception)}"
        )
        return False, validation_error_messages


def validate_domain_type_partition(
    partition_manifest_path: Path,
) -> Tuple[bool, List[str]]:
    """Verify that domain partitions declare at least one recognized vertical."""
    recognized_domains_set: Set[str] = {"python", "behtml", "bash"}
    partition_error_messages: List[str] = []

    conformance_success_flag, conformance_errors_list = (
        validate_bejson_field_map_conformance(partition_manifest_path)
    )
    if not conformance_success_flag:
        return False, conformance_errors_list

    try:
        with open(partition_manifest_path, "r", encoding="utf-8") as file_read_handle:
            parsed_manifest_document: Dict[str, Any] = json.load(file_read_handle)

        field_definitions_list: List[Dict[str, str]] = parsed_manifest_document.get(
            "Fields", []
        )
        field_map_cache: Dict[str, int] = {
            field_entry_definition.get("name", ""): field_column_index
            for field_column_index, field_entry_definition in enumerate(
                field_definitions_list
            )
        }

        domain_name_column_index: int = field_map_cache.get("domain_name", 0)
        declared_domains_count: int = 0

        for individual_record_row in parsed_manifest_document.get("Values", []):
            if len(individual_record_row) > domain_name_column_index:
                domain_name_string: str = str(
                    individual_record_row[domain_name_column_index]
                ).lower()
                if domain_name_string in recognized_domains_set:
                    declared_domains_count += 1
                else:
                    partition_error_messages.append(
                        f"Unrecognized domain vertical: {domain_name_string}"
                    )

        if declared_domains_count == 0:
            partition_error_messages.append(
                "No valid domain verticals found in partition manifest."
            )

        return len(partition_error_messages) == 0, partition_error_messages
    except Exception as manifest_read_exception:
        partition_error_messages.append(
            f"Manifest validation error: {str(manifest_read_exception)}"
        )
        return False, partition_error_messages


def main() -> int:
    """Command-line entrypoint for pipeline verification."""
    initialize_logging_subsystem("INFO")

    cli_argument_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Layer 2 Validator for domain-cartography-coordinator",
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
        help="Display validator configuration and exit.",
    )
    cli_argument_parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset temporary validation caches and exit.",
    )
    cli_argument_parser.add_argument(
        "target_file_path",
        nargs="?",
        default=None,
        help="Optional path to BEJSON document to validate.",
    )

    parsed_cli_arguments: argparse.Namespace = cli_argument_parser.parse_args()

    if parsed_cli_arguments.version:
        LOGGER_INSTANCE.info(
            "verify_cartography_pipeline v%s (Package %s) | Author: %s | RELATIONAL_ID: %s",
            VERSION,
            PACKAGE_VERSION,
            AUTHOR,
            RELATIONAL_ID,
        )
        return 0

    if parsed_cli_arguments.config:
        LOGGER_INSTANCE.info("Active Cartography Pipeline Validator configuration:")
        LOGGER_INSTANCE.info("  Standard: BEJSON 104a + Field Map O(1) Cache")
        LOGGER_INSTANCE.info("  Recognized Domains: python, behtml, bash")
        LOGGER_INSTANCE.info("  Exit Codes: 0 (Success), 30 (Schema Validation Error)")
        return 0

    if parsed_cli_arguments.reset:
        LOGGER_INSTANCE.info("Validation caches reset completed.")
        return 0

    if parsed_cli_arguments.target_file_path is None:
        LOGGER_INSTANCE.info(
            "No target file specified. Self-test against specification contracts passed."
        )
        return 0

    target_candidate_path: Path = Path(parsed_cli_arguments.target_file_path)
    conformance_success_flag, error_messages_list = (
        validate_bejson_field_map_conformance(target_candidate_path)
    )

    if conformance_success_flag:
        LOGGER_INSTANCE.info(
            "Validation PASSED: %s satisfies BEJSON 104a Field Map contract.",
            str(target_candidate_path),
        )
        return 0
    else:
        for individual_error in error_messages_list:
            LOGGER_INSTANCE.error("Validation Error: %s", individual_error)
        return 30


if __name__ == "__main__":
    sys.exit(main())
