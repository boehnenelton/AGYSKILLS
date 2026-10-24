#!/usr/bin/env python3
# ==============================================================================
# Script Name: bejson_delivery_packager
# Description: Layer 6 packaging and delivery automator that increments package
#              versions, stamps Versioned_UUID and file RELATIONAL_IDs, enforces
#              .beignore exclusion rules, builds release ZIPs, and executes
#              master index registration per Policy §3, §4.6, §4.7, and §9.
# Version: 100
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 332bae05-431f-4e96-a547-f1e0eadd9686
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("bejson_delivery_packager requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import fnmatch
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300
AUTHOR_CREDIT: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SCRIPT_RELATIONAL_ID: str = "332bae05-431f-4e96-a547-f1e0eadd9686"

EXIT_SUCCESS_CODE: int = 0
EXIT_PATH_FAILURE_CODE: int = 10
EXIT_ENV_FAILURE_CODE: int = 20
EXIT_SCHEMA_FAILURE_CODE: int = 30

LOGGER_INSTANCE: logging.Logger = logging.getLogger("BejsonDeliveryPackager")


def get_runtime_script_directory() -> Path:
    """Resolve and return absolute directory of the running script."""
    return Path(__file__).resolve().parent


SCRIPT_DIRECTORY_PATH: Path = get_runtime_script_directory()


def initialize_logging_subsystem(configured_log_level_name: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    numeric_logging_level: int = getattr(
        logging, configured_log_level_name.upper(), logging.INFO
    )
    logging.basicConfig(
        level=numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [BejsonDeliveryPackager] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def resolve_canonical_environment_paths() -> Dict[str, Path]:
    """
    Resolve paths from canonical paths.json or apply standard system defaults.
    Never hardcode storage paths in runtime business logic.
    """
    system_paths_map: Dict[str, Path] = {
        "DOWNLOAD_ROOT": Path("/storage/emulated/0/Download"),
        "PROJECTS_ARCHIVE_ROOT": Path("/storage/emulated/0/Admin/Core/Projects_Archive"),
        "INTERNAL_STORAGE": Path("/storage/emulated/0"),
        "PROJECT_INDEX_ROOT": Path("/storage/emulated/0/Admin/System/tools"),
    }

    user_paths_config_path: Path = Path("/storage/emulated/0/.env/user/paths.json")
    if user_paths_config_path.is_file():
        try:
            with open(user_paths_config_path, "r", encoding="utf-8") as paths_file_handle:
                parsed_bejson_document: Dict[str, Any] = json.load(paths_file_handle)

            field_definitions_list: List[Dict[str, str]] = parsed_bejson_document.get("Fields", [])
            field_map_cache: Dict[str, int] = {
                field_entry.get("name", ""): field_index
                for field_index, field_entry in enumerate(field_definitions_list)
            }
            var_name_column_index: int = field_map_cache.get("var_name", 0)
            var_value_column_index: int = field_map_cache.get("var_value", 1)

            for record_row in parsed_bejson_document.get("Values", []):
                variable_name_string: str = str(record_row[var_name_column_index])
                variable_value_string: str = str(record_row[var_value_column_index])
                if variable_name_string in system_paths_map:
                    system_paths_map[variable_name_string] = Path(variable_value_string)
                elif variable_name_string == "INTERNAL_STORAGE":
                    system_paths_map["INTERNAL_STORAGE"] = Path(variable_value_string)
                    system_paths_map["DOWNLOAD_ROOT"] = Path(variable_value_string) / "Download"
        except Exception as paths_resolution_exception:
            LOGGER_INSTANCE.warning(
                "Unable to parse paths.json (%s). Using fallback paths.",
                str(paths_resolution_exception),
            )

    return system_paths_map


def sanitize_bejson_boundary_layer(raw_document_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize boundary-layer BEJSON payload dictionary keys and values per Policy §10.9."""
    if not isinstance(raw_document_dict, dict):
        return raw_document_dict

    sanitized_document_dict: Dict[str, Any] = {
        (key_string.strip() if isinstance(key_string, str) else key_string): value_element
        for key_string, value_element in raw_document_dict.items()
    }

    field_definitions_list = sanitized_document_dict.get("Fields")
    if isinstance(field_definitions_list, list):
        for field_entry_dict in field_definitions_list:
            if isinstance(field_entry_dict, dict):
                for field_key_name in ("name", "type"):
                    field_value_str = field_entry_dict.get(field_key_name)
                    if isinstance(field_value_str, str):
                        field_entry_dict[field_key_name] = field_value_str.strip()

    values_records_list = sanitized_document_dict.get("Values")
    if isinstance(values_records_list, list):
        for record_row_list in values_records_list:
            if isinstance(record_row_list, list):
                for column_cell_index, cell_value in enumerate(record_row_list):
                    if isinstance(cell_value, str) and cell_value and (cell_value[0].isspace() or cell_value[-1].isspace()):
                        record_row_list[column_cell_index] = cell_value.strip()

    return sanitized_document_dict


def compile_field_map_cache(field_definitions_list: List[Dict[str, str]]) -> Dict[str, int]:
    """Build O(1) field name to column index lookup map per Policy §6.2."""
    return {
        field_definition_dict.get("name", ""): column_index
        for column_index, field_definition_dict in enumerate(field_definitions_list)
    }


def write_bejson_document_atomically(target_file_path: Path, document_payload_dict: Dict[str, Any]) -> None:
    """Atomic write via temporary file, fsync, and atomic rename to guarantee data integrity."""
    target_file_path = target_file_path.resolve()
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_file_descriptor, temporary_file_path_string = tempfile.mkstemp(
        prefix=f".bejson_pkg_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_file_path.parent),
    )
    temporary_file_path: Path = Path(temporary_file_path_string)
    try:
        with os.fdopen(temporary_file_descriptor, "w", encoding="utf-8") as temporary_file_handle:
            json.dump(document_payload_dict, temporary_file_handle, indent=2, ensure_ascii=False)
            temporary_file_handle.write("\n")
            temporary_file_handle.flush()
            os.fsync(temporary_file_handle.fileno())
        os.replace(str(temporary_file_path), str(target_file_path))
    except Exception:
        if temporary_file_path.exists():
            temporary_file_path.unlink(missing_ok=True)
        raise


def format_solid_integer_version(raw_version_string: str) -> str:
    """Format solid integer version per Policy §3.1 (e.g. '1.0.0' -> '100', '1.1.16' -> '10116')."""
    version_digits_list: List[str] = re.findall(r"\d+", raw_version_string)
    if not version_digits_list:
        return "100"
    if len(version_digits_list) == 1:
        return version_digits_list[0]
    major_segment: str = version_digits_list[0]
    minor_segment: str = version_digits_list[1] if len(version_digits_list) > 1 else "0"
    patch_segment: str = version_digits_list[2] if len(version_digits_list) > 2 else "0"
    # Canonical solid mapping: 1.0.0 -> 100, 1.2.3 -> 123
    return f"{major_segment}{minor_segment}{patch_segment}"


def load_beignore_patterns(project_root_directory: Path) -> List[str]:
    """Load exclusion patterns from .beignore or return standard default exclusion patterns."""
    standard_exclusion_patterns: List[str] = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        "*.lock",
        "*.tmp",
        ".tmp*",
        ".bejson_*",
        ".git",
        ".gitignore",
        ".gitattributes",
        ".DS_Store",
        "Thumbs.db",
        "data/temp",
        "data/temp/*",
        "exports",
        "exports/*",
        "backups",
        "backups/*",
        "*.bak",
    ]

    custom_beignore_file_path: Path = project_root_directory / ".beignore"
    if custom_beignore_file_path.is_file():
        try:
            with open(custom_beignore_file_path, "r", encoding="utf-8") as beignore_file_handle:
                for line_content in beignore_file_handle:
                    stripped_pattern: str = line_content.strip()
                    if stripped_pattern and not stripped_pattern.startswith("#"):
                        standard_exclusion_patterns.append(stripped_pattern)
        except Exception as file_read_exception:
            LOGGER_INSTANCE.warning(
                "Unable to read .beignore (%s). Using standard patterns.",
                str(file_read_exception),
            )

    return standard_exclusion_patterns


def should_exclude_path(
    candidate_relative_path: Path, exclusion_patterns_list: List[str]
) -> bool:
    """Check if candidate relative path matches any exclusion rule."""
    path_segments_list: List[str] = candidate_relative_path.parts
    path_string: str = str(candidate_relative_path).replace("\\", "/")

    for pattern in exclusion_patterns_list:
        normalized_pattern: str = pattern.strip("/")
        if fnmatch.fnmatch(path_string, pattern) or fnmatch.fnmatch(
            candidate_relative_path.name, pattern
        ):
            return True
        for segment in path_segments_list:
            if fnmatch.fnmatch(segment, normalized_pattern):
                return True

    return False


def update_source_file_headers(
    source_file_path: Path, new_version_value: str, new_relational_id: str
) -> bool:
    """Update top-level VERSION variable and RELATIONAL_ID in source script header."""
    try:
        file_text_content: str = source_file_path.read_text(encoding="utf-8")
    except Exception:
        return False

    content_modified_flag: bool = False
    new_text_content: str = file_text_content

    # Match: VERSION: int = 100 or VERSION = "1.0.0" or VERSION: str = "1.0.0"
    version_regex_pattern = r'^(VERSION(?:\s*:\s*(?:int|str))?\s*=\s*)([0-9]+|"[^"]*"|\'[^\']*\')'
    if re.search(version_regex_pattern, new_text_content, re.MULTILINE):
        # Determine if integer or string
        def replace_version(match_object: re.Match) -> str:
            prefix: str = match_object.group(1)
            original_val: str = match_object.group(2)
            if original_val.isdigit():
                return f"{prefix}{format_solid_integer_version(new_version_value)}"
            return f'{prefix}"{new_version_value}"'

        new_text_content = re.sub(
            version_regex_pattern, replace_version, new_text_content, count=1, flags=re.MULTILINE
        )
        content_modified_flag = True

    # Match: RELATIONAL_ID = "..." or # RELATIONAL_ID: ...
    relational_id_header_pattern = r"(RELATIONAL_ID(?:\s*:\s*str)?\s*[:=]\s*[\"']?)([0-9a-fA-F-]{36})([\"']?)"
    if re.search(relational_id_header_pattern, new_text_content):
        new_text_content = re.sub(
            relational_id_header_pattern,
            rf"\g<1>{new_relational_id}\g<3>",
            new_text_content,
            count=1,
        )
        content_modified_flag = True

    if content_modified_flag and new_text_content != file_text_content:
        try:
            source_file_path.write_text(new_text_content, encoding="utf-8")
            return True
        except Exception as write_error:
            LOGGER_INSTANCE.warning(
                "Could not update header in %s: %s", source_file_path.name, str(write_error)
            )
            return False

    return False


def compute_sha256_checksum(target_file_path: Path) -> str:
    """Calculate SHA-256 hexadecimal hash of given file."""
    hash_algorithm = hashlib.sha256()
    with open(target_file_path, "rb") as binary_file_handle:
        for chunk_buffer in iter(lambda: binary_file_handle.read(65536), b""):
            hash_algorithm.update(chunk_buffer)
    return hash_algorithm.hexdigest()


def execute_master_project_registration(
    project_root_directory: Path, project_index_root_path: Path
) -> Tuple[bool, str]:
    """Execute master registration script if available."""
    registration_script_path: Path = project_index_root_path / "cli_project_register.py"
    if not registration_script_path.is_file():
        return False, f"Registration script not found at {registration_script_path}"

    try:
        command_arguments: List[str] = [
            sys.executable,
            str(registration_script_path),
            "--register",
            str(project_root_directory),
        ]
        process_result = subprocess.run(
            command_arguments,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if process_result.returncode == 0:
            return True, "Registered successfully."
        return False, f"Registration exited with code {process_result.returncode}: {process_result.stderr.strip()}"
    except Exception as execution_exception:
        return False, f"Registration error: {str(execution_exception)}"


def package_and_deliver_project(
    project_root_directory: Path,
    custom_output_directory: Optional[Path] = None,
    changelog_entry_string: Optional[str] = None,
    skip_master_registration: bool = False,
    dry_run_flag: bool = False,
) -> Dict[str, Any]:
    """
    Main packaging workflow executing version bump, UUID generation,
    .beignore filtering, ZIP creation, checksum hashing, and registration.
    """
    project_root_directory = project_root_directory.resolve()
    if not project_root_directory.is_dir():
        LOGGER_INSTANCE.error("Project directory does not exist: %s", project_root_directory)
        return {"status": "error", "exit_code": EXIT_PATH_FAILURE_CODE}

    # Locate manifest: bejson_project.json or .bejson_project.json
    manifest_file_path: Path = project_root_directory / "bejson_project.json"
    if not manifest_file_path.is_file():
        manifest_file_path = project_root_directory / ".bejson_project.json"
    if not manifest_file_path.is_file():
        LOGGER_INSTANCE.error(
            "bejson_project.json not found in root directory: %s", project_root_directory
        )
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    try:
        with open(manifest_file_path, "r", encoding="utf-8") as manifest_file_handle:
            raw_manifest_dict: Dict[str, Any] = json.load(manifest_file_handle)
    except Exception as parse_exception:
        LOGGER_INSTANCE.error("Failed to parse %s: %s", manifest_file_path.name, str(parse_exception))
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    sanitized_manifest_dict: Dict[str, Any] = sanitize_bejson_boundary_layer(raw_manifest_dict)
    field_definitions_list: List[Dict[str, str]] = sanitized_manifest_dict.get("Fields", [])
    if not field_definitions_list:
        LOGGER_INSTANCE.error("Manifest missing 'Fields' definition list.")
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    field_map_cache: Dict[str, int] = compile_field_map_cache(field_definitions_list)

    values_records_list: List[List[Any]] = sanitized_manifest_dict.get("Values", [])
    if not values_records_list or not isinstance(values_records_list[0], list):
        LOGGER_INSTANCE.error("Manifest missing valid 'Values' row matrix.")
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    project_record_row: List[Any] = values_records_list[0]

    # Resolve field values
    def get_field_val(field_name: str, fallback_default: Any = "") -> Any:
        column_index = field_map_cache.get(field_name)
        if column_index is not None and column_index < len(project_record_row):
            return project_record_row[column_index]
        return fallback_default

    def set_field_val(field_name: str, new_val: Any) -> None:
        column_index = field_map_cache.get(field_name)
        if column_index is not None and column_index < len(project_record_row):
            project_record_row[column_index] = new_val

    project_name: str = str(get_field_val("Project_Name", project_root_directory.name)).strip()
    project_version: str = str(get_field_val("Project_Version", "1.0.0")).strip()
    current_package_version_str: str = str(get_field_val("Package_Version", "100")).strip()

    # Bump Package Version by +1
    try:
        current_pkg_int: int = int(re.sub(r"\D", "", current_package_version_str) or "100")
        new_package_version_int: int = current_pkg_int + 1
    except ValueError:
        new_package_version_int = 101
    new_package_version_str: str = str(new_package_version_int)

    # Generate fresh Versioned_UUID and recency timestamp
    new_versioned_uuid: str = str(uuid.uuid4())
    current_date_iso_utc: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Solid numeric integer version format
    solid_project_version_token: str = format_solid_integer_version(project_version)
    archive_filename: str = f"{project_name}-V{solid_project_version_token}-PKG{new_package_version_str}.zip"

    # Append change log entry
    current_change_log: str = str(get_field_val("Change_Log", "")).strip()
    new_changelog_entry: str = changelog_entry_string or f"Release package version bump to PKG{new_package_version_str}."
    formatted_changelog_entry: str = f"{project_version} | {current_date_iso_utc} | {new_changelog_entry}"
    updated_change_log: str = (
        f"{current_change_log}\n{formatted_changelog_entry}"
        if current_change_log
        else formatted_changelog_entry
    )

    LOGGER_INSTANCE.info(
        "Preparing Release: %s (Version: %s, Package: %s -> %s)",
        project_name,
        project_version,
        current_package_version_str,
        new_package_version_str,
    )
    LOGGER_INSTANCE.info("New Versioned_UUID: %s", new_versioned_uuid)
    LOGGER_INSTANCE.info("Target Archive: %s", archive_filename)

    if dry_run_flag:
        LOGGER_INSTANCE.info("[DRY RUN] Simulation complete. No changes written to disk.")
        return {
            "status": "dry_run",
            "project_name": project_name,
            "project_version": project_version,
            "package_version": new_package_version_str,
            "archive_filename": archive_filename,
            "versioned_uuid": new_versioned_uuid,
            "exit_code": EXIT_SUCCESS_CODE,
        }

    # Update top-level manifest keys
    sanitized_manifest_dict["Package_Version"] = new_package_version_str
    sanitized_manifest_dict["Versioned_UUID"] = new_versioned_uuid
    sanitized_manifest_dict["Project_Modified_Date"] = current_date_iso_utc

    # Update row-level fields in Values[0]
    set_field_val("Package_Version", new_package_version_str)
    set_field_val("Versioned_UUID", new_versioned_uuid)
    set_field_val("Package_Date", current_date_iso_utc)
    set_field_val("Project_Modified_Date", current_date_iso_utc)
    set_field_val("Archive_Filename", archive_filename)
    set_field_val("Change_Log", updated_change_log)

    # Update source script headers
    source_files_updated_count: int = 0
    for root_dirpath, _, filenames_list in os.walk(project_root_directory):
        for single_filename in filenames_list:
            if single_filename.endswith((".py", ".sh", ".bash", ".js", ".ts")):
                file_candidate_path: Path = Path(root_dirpath) / single_filename
                if update_source_file_headers(
                    file_candidate_path, project_version, new_versioned_uuid
                ):
                    source_files_updated_count += 1

    LOGGER_INSTANCE.info(
        "Updated headers across %d source script(s).", source_files_updated_count
    )

    # Load exclusion rules
    exclusion_patterns_list: List[str] = load_beignore_patterns(project_root_directory)

    # Determine destination folder for output archive
    canonical_env_paths: Dict[str, Path] = resolve_canonical_environment_paths()
    export_destination_directory: Path
    if custom_output_directory:
        export_destination_directory = custom_output_directory.resolve()
    elif (project_root_directory / "exports").is_dir():
        export_destination_directory = project_root_directory / "exports"
    elif canonical_env_paths["DOWNLOAD_ROOT"].is_dir():
        export_destination_directory = canonical_env_paths["DOWNLOAD_ROOT"]
    else:
        export_destination_directory = project_root_directory

    export_destination_directory.mkdir(parents=True, exist_ok=True)
    target_archive_path: Path = export_destination_directory / archive_filename

    # Save manifest prior to packaging
    write_bejson_document_atomically(manifest_file_path, sanitized_manifest_dict)

    # Build ZIP archive atomically
    temporary_zip_fd, temporary_zip_path_str = tempfile.mkstemp(
        prefix=f".pkg_{os.getpid()}_",
        suffix=".zip",
        dir=str(export_destination_directory),
    )
    os.close(temporary_zip_fd)
    temporary_zip_path: Path = Path(temporary_zip_path_str)

    archived_files_count: int = 0
    try:
        with zipfile.ZipFile(
            temporary_zip_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zip_archive_handle:
            for root_dirpath, dirnames_list, filenames_list in os.walk(project_root_directory):
                current_directory_path = Path(root_dirpath)
                relative_directory_path = current_directory_path.relative_to(project_root_directory)

                # Filter directories in-place to prevent traversing excluded trees
                dirnames_list[:] = [
                    d
                    for d in dirnames_list
                    if not should_exclude_path(
                        relative_directory_path / d, exclusion_patterns_list
                    )
                ]

                for filename in filenames_list:
                    relative_file_path = relative_directory_path / filename
                    if should_exclude_path(relative_file_path, exclusion_patterns_list):
                        continue

                    absolute_file_path = project_root_directory / relative_file_path
                    zip_archive_handle.write(
                        str(absolute_file_path),
                        arcname=str(relative_file_path).replace("\\", "/"),
                    )
                    archived_files_count += 1

        os.replace(str(temporary_zip_path), str(target_archive_path))
    except Exception as zip_creation_error:
        if temporary_zip_path.exists():
            temporary_zip_path.unlink(missing_ok=True)
        LOGGER_INSTANCE.error("Failed to construct ZIP archive: %s", str(zip_creation_error))
        return {"status": "error", "exit_code": EXIT_PATH_FAILURE_CODE}

    # Compute SHA-256 checksum and update manifest with hash
    package_checksum_sha256: str = compute_sha256_checksum(target_archive_path)
    set_field_val("Package_Checksum_SHA256", package_checksum_sha256)
    write_bejson_document_atomically(manifest_file_path, sanitized_manifest_dict)

    LOGGER_INSTANCE.info(
        "Archive built successfully: %s (%d files, SHA256: %s)",
        target_archive_path.name,
        archived_files_count,
        package_checksum_sha256[:16] + "...",
    )

    # Master index registration
    registration_status_message: str = "Skipped by flag."
    registration_success_flag: bool = False
    if not skip_master_registration:
        registration_success_flag, registration_status_message = (
            execute_master_project_registration(
                project_root_directory, canonical_env_paths["PROJECT_INDEX_ROOT"]
            )
        )
        set_field_val("Is_Registered", registration_success_flag)
        write_bejson_document_atomically(manifest_file_path, sanitized_manifest_dict)
        LOGGER_INSTANCE.info("Master Registration: %s", registration_status_message)

    return {
        "status": "success",
        "project_name": project_name,
        "project_version": project_version,
        "package_version": new_package_version_str,
        "archive_path": str(target_archive_path),
        "archive_filename": archive_filename,
        "package_checksum_sha256": package_checksum_sha256,
        "versioned_uuid": new_versioned_uuid,
        "archived_files_count": archived_files_count,
        "is_registered": registration_success_flag,
        "registration_message": registration_status_message,
        "exit_code": EXIT_SUCCESS_CODE,
    }


def parse_command_line_arguments() -> argparse.Namespace:
    """Configure and parse CLI argument flags."""
    parser = argparse.ArgumentParser(
        description="Package and deliver compliant project releases per Policy §3, §4.6, §4.7, and §9."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Path to project root directory containing bejson_project.json (default: current directory).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Destination directory for output ZIP package.",
    )
    parser.add_argument(
        "--change-log",
        type=str,
        default=None,
        help="Custom changelog note appended to bejson_project.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate version bumping and packaging without modifying disk.",
    )
    parser.add_argument(
        "--skip-register",
        action="store_true",
        help="Skip triggering master project database registration.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"bejson_delivery_packager v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument(
        "--register",
        action="store_true",
        help="Self-register packager utility in master index.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Print current environment and configuration paths.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Verify and reset default packaging directories.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI Entry Point."""
    initialize_logging_subsystem("INFO")
    cli_arguments: argparse.Namespace = parse_command_line_arguments()

    if cli_arguments.config:
        env_paths = resolve_canonical_environment_paths()
        print(json.dumps({k: str(v) for k, v in env_paths.items()}, indent=2))
        return EXIT_SUCCESS_CODE

    if cli_arguments.register:
        env_paths = resolve_canonical_environment_paths()
        success, message = execute_master_project_registration(
            SCRIPT_DIRECTORY_PATH.parent, env_paths["PROJECT_INDEX_ROOT"]
        )
        LOGGER_INSTANCE.info("Packager Registration: %s", message)
        return EXIT_SUCCESS_CODE if success else EXIT_ENV_FAILURE_CODE

    if cli_arguments.reset:
        LOGGER_INSTANCE.info("Resetting packager runtime paths...")
        env_paths = resolve_canonical_environment_paths()
        env_paths["DOWNLOAD_ROOT"].mkdir(parents=True, exist_ok=True)
        env_paths["PROJECTS_ARCHIVE_ROOT"].mkdir(parents=True, exist_ok=True)
        LOGGER_INSTANCE.info("Packager runtime directory verification complete.")
        return EXIT_SUCCESS_CODE

    delivery_result: Dict[str, Any] = package_and_deliver_project(
        project_root_directory=cli_arguments.project_dir,
        custom_output_directory=cli_arguments.output_dir,
        changelog_entry_string=cli_arguments.change_log,
        skip_master_registration=cli_arguments.skip_register,
        dry_run_flag=cli_arguments.dry_run,
    )

    return delivery_result.get("exit_code", EXIT_SUCCESS_CODE)


if __name__ == "__main__":
    sys.exit(main())
