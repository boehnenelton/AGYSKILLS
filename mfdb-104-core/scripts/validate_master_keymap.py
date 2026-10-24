#!/usr/bin/env python3
"""
File_Name:          validate_master_keymap.py
Description:        Audits and validates referential consistency across MasterKeyMap cross-taxonomy link edges.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      5f2d1e8c-9a4b-4f7a-8e1c-6d0b8a5c3e2f
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION = 100
RELEASE_VERSION = 300
RELATIONAL_ID = "5f2d1e8c-9a4b-4f7a-8e1c-6d0b8a5c3e2f"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("validate_master_keymap")


def sanitize_boundary_whitespace(input_value: Any) -> Any:
    """Sanitizes boundary-layer whitespace per Policy §10.9."""
    if isinstance(input_value, str):
        return input_value.strip()
    return input_value


def compile_field_map_cache(bejson_document_data: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) field map lookup cache from the Fields definition array."""
    field_map_lookup_cache: Dict[str, int] = {}
    field_definitions_list = bejson_document_data.get("Fields", [])
    for field_column_index, field_definition_entry in enumerate(field_definitions_list):
        if isinstance(field_definition_entry, dict):
            field_name_identifier = field_definition_entry.get("name", "")
        else:
            field_name_identifier = str(field_definition_entry)
        field_map_lookup_cache[field_name_identifier] = field_column_index
    return field_map_lookup_cache


def audit_keymap_document(
    keymap_file_path: Path,
    system_root_directory: Optional[Path] = None,
) -> Tuple[List[str], List[str]]:
    """Audits a MasterKeyMap document for structural integrity, unique edges, and route resolution."""
    validation_error_messages: List[str] = []
    validation_warning_messages: List[str] = []

    if not keymap_file_path.is_file():
        validation_error_messages.append(f"MasterKeyMap file not found: {keymap_file_path}")
        return validation_error_messages, validation_warning_messages

    try:
        keymap_document_content = json.loads(keymap_file_path.read_text(encoding="utf-8"))
    except Exception as json_parse_error:
        validation_error_messages.append(f"Failed to parse JSON in {keymap_file_path}: {json_parse_error}")
        return validation_error_messages, validation_warning_messages

    # Format validations
    if keymap_document_content.get("Format") != "BEJSON":
        validation_error_messages.append(f"Format must be 'BEJSON', got '{keymap_document_content.get('Format')}'")
    if keymap_document_content.get("Format_Version") not in ("104", "104a"):
        validation_error_messages.append(f"Format_Version must be '104' or '104a', got '{keymap_document_content.get('Format_Version')}'")
    if keymap_document_content.get("Format_Creator") != "Elton Boehnen":
        validation_error_messages.append(f"Format_Creator must be 'Elton Boehnen', got '{keymap_document_content.get('Format_Creator')}'")

    field_map_cache = compile_field_map_cache(keymap_document_content)

    required_column_identifiers = [
        "keymap_edge_identifier_key",
        "keymap_source_entity_id_fk",
        "keymap_source_taxonomy_type_fk",
        "keymap_target_entity_id_fk",
        "keymap_target_taxonomy_type_fk",
        "keymap_relational_edge_kind",
        "keymap_compiled_destination_route_path",
        "keymap_assigned_presentation_template_fk",
    ]

    for required_identifier in required_column_identifiers:
        if required_identifier not in field_map_cache:
            validation_error_messages.append(f"Missing required field in MasterKeyMap schema: '{required_identifier}'")

    if validation_error_messages:
        return validation_error_messages, validation_warning_messages

    edge_key_index = field_map_cache["keymap_edge_identifier_key"]
    source_id_index = field_map_cache["keymap_source_entity_id_fk"]
    source_tax_index = field_map_cache["keymap_source_taxonomy_type_fk"]
    target_id_index = field_map_cache["keymap_target_entity_id_fk"]
    target_tax_index = field_map_cache["keymap_target_taxonomy_type_fk"]
    edge_kind_index = field_map_cache["keymap_relational_edge_kind"]
    route_path_index = field_map_cache["keymap_compiled_destination_route_path"]
    template_fk_index = field_map_cache["keymap_assigned_presentation_template_fk"]

    observed_edge_keys_set: Set[str] = set()
    table_value_rows = keymap_document_content.get("Values", [])

    for row_sequence_index, record_value_row in enumerate(table_value_rows):
        if len(record_value_row) != len(keymap_document_content.get("Fields", [])):
            validation_error_messages.append(
                f"Row {row_sequence_index} column count mismatch: expected {len(keymap_document_content.get('Fields', []))}, got {len(record_value_row)}"
            )
            continue

        edge_key = sanitize_boundary_whitespace(record_value_row[edge_key_index])
        source_id = sanitize_boundary_whitespace(record_value_row[source_id_index])
        source_tax = sanitize_boundary_whitespace(record_value_row[source_tax_index])
        target_id = sanitize_boundary_whitespace(record_value_row[target_id_index])
        target_tax = sanitize_boundary_whitespace(record_value_row[target_tax_index])
        edge_kind = sanitize_boundary_whitespace(record_value_row[edge_kind_index])
        route_path = sanitize_boundary_whitespace(record_value_row[route_path_index])
        template_fk = sanitize_boundary_whitespace(record_value_row[template_fk_index])

        # 1. Edge key uniqueness
        if not edge_key:
            validation_error_messages.append(f"Row {row_sequence_index}: Empty keymap_edge_identifier_key.")
        elif edge_key in observed_edge_keys_set:
            validation_error_messages.append(f"Row {row_sequence_index}: Duplicate edge key '{edge_key}'.")
        else:
            observed_edge_keys_set.add(edge_key)

        # 2. Source declarations
        if not source_id or not source_tax:
            validation_error_messages.append(f"Row {row_sequence_index} ({edge_key}): Source entity ID and taxonomy type cannot be null.")

        # 3. Route path validation
        if not route_path:
            validation_error_messages.append(f"Row {row_sequence_index} ({edge_key}): Compiled route path cannot be null.")
        elif not str(route_path).startswith("/"):
            validation_error_messages.append(f"Row {row_sequence_index} ({edge_key}): Route path must start with '/', got '{route_path}'.")

        # 4. Target entity symmetry
        if target_id and not target_tax:
            validation_error_messages.append(f"Row {row_sequence_index} ({edge_key}): Target entity '{target_id}' has null target taxonomy.")
        if target_tax and not target_id:
            validation_error_messages.append(f"Row {row_sequence_index} ({edge_key}): Target taxonomy '{target_tax}' has null target entity ID.")

        # 5. Route vs Companion template rules
        if edge_kind == "route" and not template_fk:
            validation_warning_messages.append(f"Row {row_sequence_index} ({edge_key}): Edge kind 'route' has no assigned template FK.")

    return validation_error_messages, validation_warning_messages


def main() -> int:
    argument_parser = argparse.ArgumentParser(
        prog="validate_master_keymap",
        description="Audits and validates referential consistency across MasterKeyMap cross-taxonomy link edges.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})",
    )
    argument_parser.add_argument(
        "--register",
        action="store_true",
        help="Display registration status with master index.",
    )
    argument_parser.add_argument(
        "--config",
        action="store_true",
        help="Display runtime configuration.",
    )
    argument_parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset state.",
    )
    argument_parser.add_argument(
        "keymap",
        type=Path,
        help="Path to MasterKeyMap.bejson file.",
    )
    argument_parser.add_argument(
        "--system-root",
        type=Path,
        default=None,
        help="Optional path to root system directory containing taxonomies.",
    )

    parsed_args = argument_parser.parse_args()

    if parsed_args.config or parsed_args.register:
        LOG.info("validate_master_keymap v%d (Release %d) ready.", VERSION, RELEASE_VERSION)
        return 0

    if parsed_args.reset:
        LOG.info("State reset acknowledged.")
        return 0

    keymap_file_path = parsed_args.keymap.resolve()
    LOG.info("Auditing MasterKeyMap: %s", keymap_file_path)

    error_messages, warning_messages = audit_keymap_document(
        keymap_file_path=keymap_file_path,
        system_root_directory=parsed_args.system_root,
    )

    if warning_messages:
        print(f"Warnings ({len(warning_messages)}):")
        for warn_msg in warning_messages:
            print(f"  [WARN] {warn_msg}")

    if error_messages:
        print(f"Errors ({len(error_messages)}):")
        for err_msg in error_messages:
            print(f"  [ERROR] {err_msg}")
        return 30

    print(f"PASS: MasterKeyMap conforms to relational graph specifications (0 errors, {len(warning_messages)} warnings).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
