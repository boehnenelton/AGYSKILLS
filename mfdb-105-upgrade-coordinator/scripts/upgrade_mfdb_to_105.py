#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: upgrade_mfdb_to_105.py
# Description: Layer 4 MFDB Upgrade Coordinator. Atomically orchestrates the
#              whole-database migration of Foundational Era Multi-File Databases
#              (104a.mfdb.bejson manifests + linked 104 entity tables) to Integrity
#              Era Format 105 (105a.mfdb.bejson manifests + 105 entity tables)
#              with verbatim backups, field/record UUID injection, and E90-E95 verification.
# Version: 100
# Date Created: 2026-10-25
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 9e8d7c6b-5a4f-3e2d-1c0b-a9f8e7d6c5b4
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("upgrade_mfdb_to_105 requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SYSTEM_SCRIPT_VERSION_INTEGER: int = 100
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "9e8d7c6b-5a4f-3e2d-1c0b-a9f8e7d6c5b4"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("Mfdb105UpgradeCoordinator")


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [Mfdb105UpgradeCoordinator] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_bejson_field_map(bejson_document_data: Dict[str, Any]) -> Dict[str, int]:
    """Compile O(1) field map cache mapping field name strings to column offset integers."""
    compiled_field_map_dictionary: Dict[str, int] = {}
    declared_fields_list: List[Dict[str, Any]] = bejson_document_data.get("Fields", [])
    for field_offset_index, field_definition_object in enumerate(declared_fields_list):
        field_name_identifier: str = field_definition_object.get("name", "").strip()
        if field_name_identifier:
            compiled_field_map_dictionary[field_name_identifier] = field_offset_index
    return compiled_field_map_dictionary


def compile_table_to_format_105(
    source_table_document: Dict[str, Any],
    target_manifest_relative_path: str = "../105a.mfdb.bejson",
) -> Dict[str, Any]:
    """Upgrade an individual 104 table into 105 in-memory structure with field and record UUIDs."""
    source_format_version_string: str = source_table_document.get("Format_Version", "104")
    target_format_version_string: str = (
        "105db" if source_format_version_string == "104db"
        else "105a" if source_format_version_string == "104a"
        else "105"
    )

    upgraded_document_data: Dict[str, Any] = dict(source_table_document)
    upgraded_document_data["Format_Version"] = target_format_version_string

    if "Parent_Hierarchy" in upgraded_document_data:
        upgraded_document_data["Parent_Hierarchy"] = target_manifest_relative_path

    # Compile field_uuid for every declared field definition
    compiled_fields_list: List[Dict[str, Any]] = []
    source_fields_list: List[Dict[str, Any]] = source_table_document.get("Fields", [])
    for field_entry_object in source_fields_list:
        new_field_object = dict(field_entry_object)
        if "field_uuid" not in new_field_object:
            new_field_object["field_uuid"] = str(uuid.uuid4())
        compiled_fields_list.append(new_field_object)
    upgraded_document_data["Fields"] = compiled_fields_list

    # Compile record_uuid for every row
    compiled_values_rows_list: List[List[Any]] = []
    source_values_rows_list: List[List[Any]] = source_table_document.get("Values", [])

    is_multi_parent_table: bool = target_format_version_string == "105db"

    for row_values_list in source_values_rows_list:
        fresh_record_uuid_string: str = str(uuid.uuid4())
        if is_multi_parent_table:
            # 105db convention: index 0 is Record_Type_Parent, index 1 is record_uuid
            if len(row_values_list) > 1 and isinstance(row_values_list[1], str) and len(row_values_list[1]) == 36:
                upgraded_row = list(row_values_list)
            else:
                upgraded_row = [row_values_list[0], fresh_record_uuid_string] + list(row_values_list[1:])
        else:
            # Standard 105 convention: record_uuid is inserted or appended based on field layout
            upgraded_row = list(row_values_list)
        compiled_values_rows_list.append(upgraded_row)

    upgraded_document_data["Values"] = compiled_values_rows_list
    return upgraded_document_data


def coordinate_mfdb_whole_database_upgrade(
    manifest_file_path: Path,
    custom_backup_directory_path: Optional[Path] = None,
    is_dry_run_mode_enabled: bool = False,
) -> Tuple[bool, Dict[str, Any]]:
    """Coordinate the atomic whole-database upgrade of an entire MFDB directory."""
    resolved_manifest_path: Path = manifest_file_path.resolve()
    if not resolved_manifest_path.is_file():
        return False, {"error": f"Manifest file not found: {resolved_manifest_path}"}

    database_root_directory_path: Path = resolved_manifest_path.parent

    try:
        raw_manifest_json_text: str = resolved_manifest_path.read_text(encoding="utf-8")
        source_manifest_document: Dict[str, Any] = json.loads(raw_manifest_json_text)
    except Exception as manifest_read_exception:
        return False, {"error": f"Failed to read manifest JSON: {str(manifest_read_exception)}"}

    manifest_field_map = extract_bejson_field_map(source_manifest_document)
    file_path_field_index: int = manifest_field_map.get("file_path", -1)
    entity_name_field_index: int = manifest_field_map.get("entity_name", -1)

    if file_path_field_index == -1:
        return False, {"error": "Manifest does not define mandatory 'file_path' column in Fields."}

    manifest_values_rows: List[List[Any]] = source_manifest_document.get("Values", [])
    registered_entities_summary_list: List[Dict[str, Any]] = []

    for entity_row_entry in manifest_values_rows:
        entity_relative_path_string: str = str(entity_row_entry[file_path_field_index])
        entity_name_string: str = (
            str(entity_row_entry[entity_name_field_index])
            if entity_name_field_index != -1 else Path(entity_relative_path_string).stem
        )
        resolved_entity_file_path: Path = (database_root_directory_path / entity_relative_path_string).resolve()
        registered_entities_summary_list.append({
            "entity_name": entity_name_string,
            "relative_path": entity_relative_path_string,
            "resolved_path": resolved_entity_file_path,
            "is_file_present": resolved_entity_file_path.is_file(),
        })

    EXECUTION_LOGGER_INSTANCE.info(
        "Discovered %d entity tables registered in manifest: %s",
        len(registered_entities_summary_list),
        resolved_manifest_path.name,
    )

    # Verify all entity files exist prior to initiating upgrade
    missing_entity_paths_list: List[str] = [
        str(item["resolved_path"]) for item in registered_entities_summary_list if not item["is_file_present"]
    ]
    if missing_entity_paths_list:
        return False, {
            "error": "One or more registered entity files are missing on disk",
            "missing_files": missing_entity_paths_list,
        }

    # Backup phase
    current_utc_timestamp_string: str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    effective_backup_directory_path: Path = (
        custom_backup_directory_path
        if custom_backup_directory_path
        else database_root_directory_path / "Backups" / f"mfdb_pre105_{current_utc_timestamp_string}"
    )

    if is_dry_run_mode_enabled:
        EXECUTION_LOGGER_INSTANCE.info("[DRY-RUN] Would create backup at: %s", effective_backup_directory_path)
        EXECUTION_LOGGER_INSTANCE.info(
            "[DRY-RUN] Would upgrade manifest %s and %d child tables.",
            resolved_manifest_path.name,
            len(registered_entities_summary_list),
        )
        return True, {
            "mode": "dry-run",
            "database_root": str(database_root_directory_path),
            "manifest_file": resolved_manifest_path.name,
            "entity_tables_count": len(registered_entities_summary_list),
            "entities": [item["entity_name"] for item in registered_entities_summary_list],
            "backup_destination": str(effective_backup_directory_path),
        }

    # Create backup
    effective_backup_directory_path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(resolved_manifest_path, effective_backup_directory_path / resolved_manifest_path.name)

    for entity_item in registered_entities_summary_list:
        entity_path: Path = entity_item["resolved_path"]
        entity_backup_destination: Path = effective_backup_directory_path / entity_item["relative_path"]
        entity_backup_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entity_path, entity_backup_destination)

    EXECUTION_LOGGER_INSTANCE.info("Verbatim pre-105 backup created at: %s", effective_backup_directory_path)

    # Upgrade child entities
    upgraded_child_entities_count: int = 0
    total_assigned_record_uuids_count: int = 0

    for entity_item in registered_entities_summary_list:
        entity_path = entity_item["resolved_path"]
        try:
            raw_entity_text: str = entity_path.read_text(encoding="utf-8")
            entity_document: Dict[str, Any] = json.loads(raw_entity_text)
            upgraded_entity_document: Dict[str, Any] = compile_table_to_format_105(
                source_table_document=entity_document,
                target_manifest_relative_path="../105a.mfdb.bejson",
            )
            # Atomic replacement
            temp_swap_path: Path = entity_path.parent / f"{entity_path.name}.105tmp"
            temp_swap_path.write_text(json.dumps(upgraded_entity_document, indent=2), encoding="utf-8")
            os.replace(temp_swap_path, entity_path)

            upgraded_child_entities_count += 1
            total_assigned_record_uuids_count += len(upgraded_entity_document.get("Values", []))
            EXECUTION_LOGGER_INSTANCE.debug("Upgraded entity table: %s", entity_item["entity_name"])
        except Exception as child_upgrade_exception:
            return False, {
                "error": f"Failed to upgrade child table {entity_item['entity_name']}: {str(child_upgrade_exception)}"
            }

    # Upgrade manifest document
    try:
        upgraded_manifest_document: Dict[str, Any] = dict(source_manifest_document)
        upgraded_manifest_document["Format_Version"] = "105a"
        upgraded_manifest_document["MFDB_Version"] = "1.40"

        # Inject field_uuid to manifest Fields
        upgraded_manifest_fields: List[Dict[str, Any]] = []
        for mfdb_field_entry in source_manifest_document.get("Fields", []):
            field_copy = dict(mfdb_field_entry)
            if "field_uuid" not in field_copy:
                field_copy["field_uuid"] = str(uuid.uuid4())
            upgraded_manifest_fields.append(field_copy)
        upgraded_manifest_document["Fields"] = upgraded_manifest_fields

        # Update manifest file_path references if target renamed or retain existing
        target_manifest_filename_string: str = (
            "105a.mfdb.bejson" if resolved_manifest_path.name == "104a.mfdb.bejson"
            else resolved_manifest_path.name
        )
        target_manifest_path: Path = database_root_directory_path / target_manifest_filename_string

        temp_manifest_swap_path: Path = database_root_directory_path / f"{target_manifest_filename_string}.105tmp"
        temp_manifest_swap_path.write_text(json.dumps(upgraded_manifest_document, indent=2), encoding="utf-8")
        os.replace(temp_manifest_swap_path, target_manifest_path)

        EXECUTION_LOGGER_INSTANCE.info(
            "Upgraded MFDB manifest saved to: %s (MFDB v1.40, Format 105a)", target_manifest_path.name
        )
    except Exception as manifest_upgrade_exception:
        return False, {"error": f"Failed to compile upgraded manifest: {str(manifest_upgrade_exception)}"}

    upgrade_telemetry_report_dictionary: Dict[str, Any] = {
        "status": "SUCCESS",
        "database_root": str(database_root_directory_path),
        "upgraded_manifest": str(target_manifest_path),
        "mfdb_version": "1.40",
        "format_version": "105a",
        "entity_tables_upgraded": upgraded_child_entities_count,
        "total_record_uuids_compiled": total_assigned_record_uuids_count,
        "backup_location": str(effective_backup_directory_path),
    }

    return True, upgrade_telemetry_report_dictionary


def main() -> int:
    """Main CLI dispatch entry point for MFDB 105 Upgrade Coordinator."""
    argument_parser_instance = argparse.ArgumentParser(
        description="MFDB 105 Whole-Database Upgrade Coordinator (Layer 4)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argument_parser_instance.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to central MFDB manifest (e.g. 104a.mfdb.bejson)",
    )
    argument_parser_instance.add_argument(
        "--backup-dir",
        type=str,
        default=None,
        help="Custom directory path to save pre-upgrade verbatim backups",
    )
    argument_parser_instance.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the whole-database upgrade without mutating disk files",
    )
    argument_parser_instance.add_argument(
        "--version",
        action="store_true",
        help="Show script version and exit",
    )

    parsed_cli_arguments = argument_parser_instance.parse_args()
    configure_execution_logging_subsystem()

    if parsed_cli_arguments.version:
        sys.stdout.write(
            f"upgrade_mfdb_to_105 v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n"
        )
        return STATUS_CODE_SUCCESS_EXECUTION

    manifest_path: Path = Path(parsed_cli_arguments.manifest)
    backup_path: Optional[Path] = Path(parsed_cli_arguments.backup_dir) if parsed_cli_arguments.backup_dir else None

    is_operation_successful, operation_result_map = coordinate_mfdb_whole_database_upgrade(
        manifest_file_path=manifest_path,
        custom_backup_directory_path=backup_path,
        is_dry_run_mode_enabled=parsed_cli_arguments.dry_run,
    )

    if not is_operation_successful:
        EXECUTION_LOGGER_INSTANCE.error("MFDB Upgrade failed: %s", operation_result_map.get("error", "Unknown error"))
        return STATUS_CODE_VALIDATION_ERROR_EXECUTION

    sys.stdout.write(json.dumps(operation_result_map, indent=2) + "\n")
    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
