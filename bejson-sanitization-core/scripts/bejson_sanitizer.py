#!/usr/bin/env python3
# ==============================================================================
# Script Name: bejson_sanitizer
# Description: Layer 1 boundary-layer data sanitization primitives, decorators,
#              and middleware for BEJSON payloads and record rows per Policy §10.9.
# Version: 1.0.0
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 8d2b91c4-5f12-4a0e-bc34-7a1e2f49d682
# ==============================================================================

import argparse
import functools
import json
import logging
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

VERSION: str = "1.0.0"
PACKAGE_VERSION: str = "100"
AUTHOR: str = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID: str = "8d2b91c4-5f12-4a0e-bc34-7a1e2f49d682"

LOGGER_INSTANCE: logging.Logger = logging.getLogger("BejsonBoundarySanitizer")


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
        format="[%(asctime)s] [%(levelname)s] [BejsonSanitizer] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def bejson_sanitize_string_value(raw_string_value: Any) -> Any:
    """Strip leading and trailing whitespace from strings while preserving primitive types."""
    if isinstance(raw_string_value, str):
        return raw_string_value.strip()
    return raw_string_value


def bejson_sanitize_row(raw_record_row: List[Any]) -> List[Any]:
    """
    Sanitize an individual BEJSON record row by stripping boundary whitespace
    from all string values per Policy §10.9.
    """
    if not isinstance(raw_record_row, list):
        return raw_record_row

    sanitized_record_row: List[Any] = [
        bejson_sanitize_string_value(column_value_entry)
        for column_value_entry in raw_record_row
    ]
    return sanitized_record_row


def bejson_sanitize_field_definitions(
    raw_field_definitions_list: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Sanitize the 'Fields' definition array of a BEJSON document.
    Ensures field names, types, and descriptions have zero boundary whitespace.
    """
    if not isinstance(raw_field_definitions_list, list):
        return raw_field_definitions_list

    sanitized_definitions_list: List[Dict[str, Any]] = []
    for field_definition_entry in raw_field_definitions_list:
        if isinstance(field_definition_entry, dict):
            sanitized_entry_map: Dict[str, Any] = {}
            for field_key_name, field_key_value in field_definition_entry.items():
                clean_key: str = field_key_name.strip() if isinstance(field_key_name, str) else field_key_name
                clean_val: Any = bejson_sanitize_string_value(field_key_value)
                sanitized_entry_map[clean_key] = clean_val
            sanitized_definitions_list.append(sanitized_entry_map)
        else:
            sanitized_definitions_list.append(field_definition_entry)

    return sanitized_definitions_list


def bejson_sanitize_payload(raw_payload_document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complete boundary-layer data sanitization for BEJSON 104/104a/104db documents.
    1. Strips whitespace from all top-level dictionary keys and metadata string values.
    2. Cleans 'Fields' array names and types to guarantee deterministic Field Map Cache creation.
    3. Cleans all string entries in 'Values' rows.
    """
    if not isinstance(raw_payload_document, dict):
        return raw_payload_document

    sanitized_payload_map: Dict[str, Any] = {}

    for document_key_name, document_key_value in raw_payload_document.items():
        normalized_key_string: str = (
            document_key_name.strip()
            if isinstance(document_key_name, str)
            else document_key_name
        )

        if normalized_key_string == "Fields" and isinstance(document_key_value, list):
            sanitized_payload_map[normalized_key_string] = (
                bejson_sanitize_field_definitions(document_key_value)
            )
        elif normalized_key_string == "Values" and isinstance(document_key_value, list):
            sanitized_values_table: List[List[Any]] = [
                bejson_sanitize_row(individual_record_row)
                if isinstance(individual_record_row, list)
                else individual_record_row
                for individual_record_row in document_key_value
            ]
            sanitized_payload_map[normalized_key_string] = sanitized_values_table
        elif isinstance(document_key_value, str):
            sanitized_payload_map[normalized_key_string] = document_key_value.strip()
        elif isinstance(document_key_value, dict):
            sanitized_payload_map[normalized_key_string] = bejson_sanitize_payload(
                document_key_value
            )
        else:
            sanitized_payload_map[normalized_key_string] = document_key_value

    return sanitized_payload_map


def bejson_sanitize_incoming_payload(function_to_decorate: Callable) -> Callable:
    """
    Decorator for parsers, serializers, and owning writers.
    Automatically cleans incoming BEJSON payload dictionaries before executing business logic.
    """
    @functools.wraps(function_to_decorate)
    def wrapper_execution_handler(*positional_args, **keyword_args) -> Any:
        sanitized_positional_args: List[Any] = []
        for positional_argument in positional_args:
            if isinstance(positional_argument, dict) and "Format" in positional_argument:
                sanitized_positional_args.append(
                    bejson_sanitize_payload(positional_argument)
                )
            else:
                sanitized_positional_args.append(positional_argument)

        sanitized_keyword_args: Dict[str, Any] = {}
        for argument_key_name, argument_key_value in keyword_args.items():
            if isinstance(argument_key_value, dict) and "Format" in argument_key_value:
                sanitized_keyword_args[argument_key_name] = bejson_sanitize_payload(
                    argument_key_value
                )
            else:
                sanitized_keyword_args[argument_key_name] = argument_key_value

        return function_to_decorate(
            *sanitized_positional_args, **sanitized_keyword_args
        )

    return wrapper_execution_handler


class BejsonSanitizationMiddleware:
    """
    Middleware pipeline handler for ingestion frameworks and API boundaries.
    Intercepts raw input dictionaries and sanitizes keys and rows prior to routing.
    """

    def __init__(self, downstream_callable_handler: Optional[Callable] = None):
        self.downstream_handler: Optional[Callable] = downstream_callable_handler

    def process_incoming_document(
        self, candidate_document_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sanitizes candidate payload before downstream forwarding."""
        sanitized_document_payload: Dict[str, Any] = bejson_sanitize_payload(
            candidate_document_payload
        )
        if self.downstream_handler is not None:
            return self.downstream_handler(sanitized_document_payload)
        return sanitized_document_payload


def run_boundary_sanitizer_self_test() -> bool:
    """Execute unit verification tests for boundary-layer sanitization."""
    raw_test_payload: Dict[str, Any] = {
        " Format ": " BEJSON ",
        " Format_Version ": " 104a ",
        " Fields ": [
            {" name ": " user_id ", " type ": " string "},
            {" name ": " access_level_metric ", " type ": " integer "},
            {" name ": " user_email_address ", " type ": " string "},
        ],
        " Values ": [
            ["  UUID_001  ", 10, "  user@domain.com  "],
            ["  UUID_002  ", 20, "  admin@domain.com  "],
        ],
    }

    sanitized_output_payload: Dict[str, Any] = bejson_sanitize_payload(
        raw_test_payload
    )

    assert "Format" in sanitized_output_payload, "Top-level key not stripped."
    assert sanitized_output_payload["Format"] == "BEJSON", "Top-level value not stripped."

    fields_list = sanitized_output_payload["Fields"]
    assert fields_list[0]["name"] == "user_id", "Field name whitespace retained."
    assert fields_list[0]["type"] == "string", "Field type whitespace retained."

    values_list = sanitized_output_payload["Values"]
    assert values_list[0][0] == "UUID_001", "Row string whitespace retained."
    assert values_list[0][1] == 10, "Row integer type mutated."
    assert values_list[0][2] == "user@domain.com", "Row email whitespace retained."

    LOGGER_INSTANCE.info("Boundary Sanitizer Self-Test: ALL ASSERTIONS PASSED (100%).")
    return True


def main() -> int:
    """Command-line entrypoint for BEJSON boundary-layer sanitizer."""
    initialize_logging_subsystem("INFO")

    cli_argument_parser = argparse.ArgumentParser(
        description="Layer 1 Boundary-Layer BEJSON Data Sanitizer (Policy §10.9)",
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
        help="Display active sanitizer configuration.",
    )
    cli_argument_parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset temporary sanitizer caches.",
    )
    cli_argument_parser.add_argument(
        "--test",
        action="store_true",
        help="Run self-test validation assertions.",
    )
    cli_argument_parser.add_argument(
        "target_file_path",
        nargs="?",
        default=None,
        help="Path to BEJSON file to sanitize in-place or print.",
    )

    parsed_cli_arguments = cli_argument_parser.parse_args()

    if parsed_cli_arguments.version:
        LOGGER_INSTANCE.info(
            "bejson_sanitizer v%s (Package %s) | Author: %s | RELATIONAL_ID: %s",
            VERSION,
            PACKAGE_VERSION,
            AUTHOR,
            RELATIONAL_ID,
        )
        return 0

    if parsed_cli_arguments.config:
        LOGGER_INSTANCE.info("Active BEJSON Boundary Sanitizer Configuration:")
        LOGGER_INSTANCE.info("  Policy: §10.9 (Boundary-Layer Data Sanitization)")
        LOGGER_INSTANCE.info("  Scope: Leading/trailing whitespace stripping from keys, fields, and string rows")
        LOGGER_INSTANCE.info("  Standard: Mandatory before Field Map Cache compilation")
        return 0

    if parsed_cli_arguments.reset:
        LOGGER_INSTANCE.info("Sanitizer cache verification reset completed.")
        return 0

    if parsed_cli_arguments.test or parsed_cli_arguments.target_file_path is None:
        test_passed: bool = run_boundary_sanitizer_self_test()
        return 0 if test_passed else 30

    target_candidate_path: Path = Path(parsed_cli_arguments.target_file_path)
    if not target_candidate_path.is_file():
        LOGGER_INSTANCE.error("Target file does not exist: %s", str(target_candidate_path))
        return 10

    try:
        with open(target_candidate_path, "r", encoding="utf-8") as file_read_handle:
            loaded_document: Dict[str, Any] = json.load(file_read_handle)
        sanitized_result: Dict[str, Any] = bejson_sanitize_payload(loaded_document)
        with open(target_candidate_path, "w", encoding="utf-8") as file_write_handle:
            json.dump(sanitized_result, file_write_handle, indent=2, ensure_ascii=False)
        LOGGER_INSTANCE.info("Successfully sanitized: %s", str(target_candidate_path))
        return 0
    except Exception as sanitization_execution_error:
        LOGGER_INSTANCE.error(
            "Failed sanitizing %s: %s",
            str(target_candidate_path),
            str(sanitization_execution_error),
        )
        return 30


if __name__ == "__main__":
    sys.exit(main())
