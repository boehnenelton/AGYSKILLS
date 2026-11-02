#!/usr/bin/env python3
"""
env_definitions_tool.py
Layer 3 Canonical Definitions Store Manager
Query, list, insert, and update environment definitions in definitions.json.

Policy Anchors:
  Policy §4.5: Environment Sourcing Standards
  Policy §6.1: Long Self-Describing Variable Standard
"""

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_ACTION_REJECTED = 30

DEFAULT_DEFINITIONS_PATH = Path("/storage/emulated/0/.env/user/definitions.json")


def sanitize_input_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def load_definitions_document(definitions_file_path: Path) -> Dict[str, Any]:
    """Load definitions document with schema preservation."""
    if not definitions_file_path.is_file():
        return {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": ["EnvironmentDefinition"],
            "Fields": [
                {"name": "name", "type": "string"},
                {"name": "value", "type": "string"},
                {"name": "description", "type": "string"},
                {"name": "Type", "type": "string"},
            ],
            "Values": [],
        }
    with open(definitions_file_path, "r", encoding="utf-8") as file_read_handle:
        return json.load(file_read_handle)


def query_definition_value(definitions_data: Dict[str, Any], key_name: str) -> Optional[Dict[str, Any]]:
    """Look up definition entry by exact key name."""
    fields = definitions_data.get("Fields", [])
    values = definitions_data.get("Values", [])
    if not fields or not values:
        return None

    field_names = [f["name"] if isinstance(f, dict) else str(f) for f in fields]
    field_map = {name: idx for idx, name in enumerate(field_names)}

    name_idx = field_map.get("name")
    val_idx = field_map.get("value")
    desc_idx = field_map.get("description")
    type_idx = field_map.get("Type")

    for row in values:
        if isinstance(row, list) and name_idx is not None and name_idx < len(row):
            if str(row[name_idx]).strip() == key_name:
                return {
                    "name": key_name,
                    "value": row[val_idx] if val_idx is not None and val_idx < len(row) else "",
                    "description": row[desc_idx] if desc_idx is not None and desc_idx < len(row) else "",
                    "Type": row[type_idx] if type_idx is not None and type_idx < len(row) else "",
                }
    return None


def list_definitions_entries(
    definitions_data: Dict[str, Any],
    filter_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List all definition entries matching optional Type filter."""
    fields = definitions_data.get("Fields", [])
    values = definitions_data.get("Values", [])
    if not fields or not values:
        return []

    field_names = [f["name"] if isinstance(f, dict) else str(f) for f in fields]
    field_map = {name: idx for idx, name in enumerate(field_names)}

    name_idx = field_map.get("name")
    val_idx = field_map.get("value")
    desc_idx = field_map.get("description")
    type_idx = field_map.get("Type")

    results_list: List[Dict[str, Any]] = []
    for row in values:
        if isinstance(row, list) and name_idx is not None and name_idx < len(row):
            entry_type = str(row[type_idx]) if type_idx is not None and type_idx < len(row) else ""
            if filter_type and entry_type.lower() != filter_type.lower():
                continue
            results_list.append(
                {
                    "name": str(row[name_idx]),
                    "value": str(row[val_idx]) if val_idx is not None and val_idx < len(row) else "",
                    "description": str(row[desc_idx]) if desc_idx is not None and desc_idx < len(row) else "",
                    "Type": entry_type,
                }
            )
    return results_list


def set_definition_entry(
    definitions_file_path: Path,
    key_name: str,
    key_value: str,
    key_type: str = "Path",
    description_text: str = "",
) -> bool:
    """Insert or update a definition with atomic file backup."""
    doc_data = load_definitions_document(definitions_file_path)
    fields = doc_data.get("Fields", [])
    values = doc_data.get("Values", [])

    field_names = [f["name"] if isinstance(f, dict) else str(f) for f in fields]
    field_map = {name: idx for idx, name in enumerate(field_names)}

    name_idx = field_map.get("name")
    val_idx = field_map.get("value")
    desc_idx = field_map.get("description")
    type_idx = field_map.get("Type")

    entry_updated = False
    for row in values:
        if isinstance(row, list) and name_idx is not None and name_idx < len(row):
            if str(row[name_idx]).strip() == key_name:
                if val_idx is not None and val_idx < len(row):
                    row[val_idx] = key_value
                if desc_idx is not None and desc_idx < len(row):
                    row[desc_idx] = description_text
                if type_idx is not None and type_idx < len(row):
                    row[type_idx] = key_type
                entry_updated = True
                break

    if not entry_updated:
        new_row = [key_name, key_value, description_text, key_type]
        values.append(new_row)

    # Atomic write
    temp_file_path = definitions_file_path.with_suffix(".tmp")
    definitions_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_file_path, "w", encoding="utf-8") as file_handle:
        json.dump(doc_data, file_handle, indent=2)
    os.replace(temp_file_path, definitions_file_path)
    return True


def main() -> int:
    """CLI entrypoint for Environment Definitions Manager tool."""
    argument_parser = argparse.ArgumentParser(
        description="env-definitions-manager: Canonical definitions.json store manager."
    )
    subparsers = argument_parser.add_subparsers(dest="subcommand", help="Operational action.")

    # get
    get_parser = subparsers.add_parser("get", help="Query definition by variable name.")
    get_parser.add_argument("key", type=str, help="Variable name to query.")

    # list
    list_parser = subparsers.add_parser("list", help="List registered definitions.")
    list_parser.add_argument("--type", type=str, default=None, help="Filter by Type (e.g. 'Path').")

    # set
    set_parser = subparsers.add_parser("set", help="Insert or update a definition.")
    set_parser.add_argument("key", type=str, help="Variable name.")
    set_parser.add_argument("value", type=str, help="Variable value.")
    set_parser.add_argument("--type", type=str, default="Path", help="Variable type (default: 'Path').")
    set_parser.add_argument("--desc", type=str, default="", help="Description text.")

    argument_parser.add_argument(
        "--definitions",
        type=str,
        default=str(DEFAULT_DEFINITIONS_PATH),
        help=f"Path to definitions.json (default: {DEFAULT_DEFINITIONS_PATH}).",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON results.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"env_definitions_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()

    if not parsed_arguments.subcommand:
        argument_parser.print_help()
        return EXIT_CLEAN_PASS

    definitions_path = sanitize_input_path(parsed_arguments.definitions)
    doc_data = load_definitions_document(definitions_path)

    if parsed_arguments.subcommand == "get":
        result = query_definition_value(doc_data, parsed_arguments.key)
        if not result:
            sys.stderr.write(f"Key not found: '{parsed_arguments.key}'\n")
            return EXIT_ACTION_REJECTED
        if parsed_arguments.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"{result['name']} = {result['value']} ({result['Type']})")
        return EXIT_CLEAN_PASS

    elif parsed_arguments.subcommand == "list":
        entries = list_definitions_entries(doc_data, filter_type=parsed_arguments.type)
        if parsed_arguments.json:
            print(json.dumps(entries, indent=2))
        else:
            print(f"Total definitions found: {len(entries)}")
            for e in entries:
                print(f"- {e['name']}: {e['value']} [{e['Type']}]")
        return EXIT_CLEAN_PASS

    elif parsed_arguments.subcommand == "set":
        success = set_definition_entry(
            definitions_file_path=definitions_path,
            key_name=parsed_arguments.key,
            key_value=parsed_arguments.value,
            key_type=parsed_arguments.type,
            description_text=parsed_arguments.desc,
        )
        if success:
            sys.stderr.write(f"Updated '{parsed_arguments.key}' in {definitions_path}\n")
            return EXIT_CLEAN_PASS
        return EXIT_ACTION_REJECTED

    return EXIT_CLEAN_PASS


if __name__ == "__main__":
    sys.exit(main())
