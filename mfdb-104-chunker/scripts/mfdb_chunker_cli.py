#!/usr/bin/env python3
"""
File:          mfdb_chunker_cli.py
Description:   MFDB Chunked Container Packager and Sticky Mount Engine.
               Packages multi-file databases (104a.mfdb.bejson manifest + dense entity files)
               into single-file Chunked-104a (.mfdb132.bejson) or Chunked-105a (.mfdb140.bejson)
               containers with SHA-256 .mfdb132_lock verification, atomic commits, pre-write gates,
               and workspace resurrection per MFDB-132 Specification.
Version:       1.0.0
Date Created:  2026-10-24
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 8d1f2a3c-4b5e-4c6a-8f7e-1a2b3c4d5e6f
"""

import os
import sys
import json
import base64
import hashlib
import logging
import argparse
import tempfile
import shutil
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.0.0"

# ── Logging Configuration (Policy §7.3: NEVER print for logging) ─────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app_logger_instance: logging.Logger = logging.getLogger("mfdb_chunker_cli")

# ── Self-Locating Path (Policy §4.1) ──────────────────────────────────────────────
def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_DIRECTORY: Path = get_script_path()
SKILL_ROOT_DIRECTORY: Path = SCRIPT_DIRECTORY.parent

# ── Constants ───────────────────────────────────────────────────────────────────
MFDB_MANIFEST_FILENAME_104: str = "104a.mfdb.bejson"
MFDB_MANIFEST_FILENAME_105: str = "105a.mfdb.bejson"
MFDB_LOCK_FILENAME: str = ".mfdb132_lock"

CHUNKED_104_FIELDS: List[Dict[str, str]] = [
    {"name": "File_Name",      "type": "string"},
    {"name": "File_Extension", "type": "string"},
    {"name": "File_Content",   "type": "string"},
    {"name": "File_Version",   "type": "string"},
    {"name": "File_Hash",      "type": "string"},
    {"name": "Relative_Path",  "type": "string"},
    {"name": "Is_Binary",      "type": "boolean"},
    {"name": "Is_Mounted",     "type": "boolean"}
]

CHUNKED_105_FIELDS: List[Dict[str, str]] = [
    {"name": "record_uuid",    "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000001"},
    {"name": "File_Name",      "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000002"},
    {"name": "File_Extension", "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000003"},
    {"name": "File_Content",   "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000004"},
    {"name": "File_Version",   "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000005"},
    {"name": "File_Hash",      "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000006"},
    {"name": "Relative_Path",  "type": "string",  "field_uuid": "f0000000-0000-4000-8000-000000000007"},
    {"name": "Is_Binary",      "type": "boolean", "field_uuid": "f0000000-0000-4000-8000-000000000008"},
    {"name": "Is_Mounted",     "type": "boolean", "field_uuid": "f0000000-0000-4000-8000-000000000009"}
]

# ── Utility & Security Helpers ──────────────────────────────────────────────────
def bejson_safe_path_resolve(target_base_dir: Path, target_relative_path: str) -> Path:
    """Guards against path traversal attacks."""
    resolved_destination: Path = (target_base_dir / target_relative_path).resolve()
    resolved_base: Path = target_base_dir.resolve()
    if not str(resolved_destination).startswith(str(resolved_base)):
        raise ValueError(f"Path traversal security violation detected: {target_relative_path}")
    return resolved_destination

def calculate_file_sha256_hash(target_file_path: Path) -> str:
    sha256_calculator = hashlib.sha256()
    with open(target_file_path, "rb") as file_stream:
        while chunk_bytes := file_stream.read(65536):
            sha256_calculator.update(chunk_bytes)
    return sha256_calculator.hexdigest()

# ── Package Packaging Engine ───────────────────────────────────────────────────
def package_mfdb_database(target_mfdb_dir: Path, output_file_path: Optional[Path] = None, era: str = "104") -> Path:
    """Packages an MFDB directory into a single-file container."""
    manifest_file_candidate_104: Path = target_mfdb_dir / MFDB_MANIFEST_FILENAME_104
    manifest_file_candidate_105: Path = target_mfdb_dir / MFDB_MANIFEST_FILENAME_105

    selected_manifest_path: Optional[Path] = None
    if era == "105" and manifest_file_candidate_105.exists():
        selected_manifest_path = manifest_file_candidate_105
    elif manifest_file_candidate_104.exists():
        selected_manifest_path = manifest_file_candidate_104
    elif manifest_file_candidate_105.exists():
        selected_manifest_path = manifest_file_candidate_105
        era = "105"
    else:
        raise FileNotFoundError(f"No MFDB manifest ({MFDB_MANIFEST_FILENAME_104} or {MFDB_MANIFEST_FILENAME_105}) found in {target_mfdb_dir}")

    with open(selected_manifest_path, "r", encoding="utf-8") as manifest_stream:
        manifest_data: Dict[str, Any] = json.load(manifest_stream)

    database_name_identifier: str = manifest_data.get("DB_Name", target_mfdb_dir.name)
    database_version_string: str = manifest_data.get("MFDB_Version", "1.32" if era == "104" else "1.40")

    container_rows_collection: List[List[Any]] = []
    excluded_directory_names: set[str] = {".git", "__pycache__", ".pytest_cache", "node_modules", "data/temp"}

    for current_root_directory, directory_names_list, file_names_list in os.walk(target_mfdb_dir):
        directory_names_list[:] = [dir_name for dir_name in directory_names_list if dir_name not in excluded_directory_names]
        for current_file_name in file_names_list:
            if current_file_name == MFDB_LOCK_FILENAME or current_file_name.endswith(".tmp"):
                continue
            
            absolute_file_path: Path = Path(current_root_directory) / current_file_name
            relative_file_path: str = str(absolute_file_path.relative_to(target_mfdb_dir))
            raw_binary_content: bytes = absolute_file_path.read_bytes()

            is_binary_payload_flag: bool = False
            try:
                serialized_content_text: str = raw_binary_content.decode("utf-8")
            except UnicodeDecodeError:
                is_binary_payload_flag = True
                serialized_content_text = base64.b64encode(raw_binary_content).decode("ascii")

            content_sha256_hash: str = hashlib.sha256(raw_binary_content).hexdigest()

            if era == "105":
                container_rows_collection.append([
                    str(uuid.uuid4()),
                    current_file_name,
                    absolute_file_path.suffix.lstrip("."),
                    serialized_content_text,
                    database_version_string,
                    content_sha256_hash,
                    relative_file_path,
                    is_binary_payload_flag,
                    False
                ])
            else:
                container_rows_collection.append([
                    current_file_name,
                    absolute_file_path.suffix.lstrip("."),
                    serialized_content_text,
                    database_version_string,
                    content_sha256_hash,
                    relative_file_path,
                    is_binary_payload_flag,
                    False
                ])

    container_extension: str = ".mfdb140.bejson" if era == "105" else ".mfdb132.bejson"
    if output_file_path is None:
        destination_file_path = target_mfdb_dir.parent / f"{database_name_identifier}{container_extension}"
    else:
        destination_file_path = output_file_path

    destination_file_path.parent.mkdir(parents=True, exist_ok=True)

    package_document_payload: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "105a" if era == "105" else "104a",
        "Format_Creator": "Elton Boehnen",
        "Schema_Name": "MFDB-140" if era == "105" else "MFDB-132",
        "Schema_Version": "1.4.0" if era == "105" else "1.3.2",
        "Records_Type": ["MFDB-140" if era == "105" else "MFDB-132"],
        "MFDB_Version": database_version_string,
        "DB_Name": database_name_identifier,
        "Package_Format": "MFDB-Chunked-105a" if era == "105" else "MFDB-Chunked-104a",
        "Session_Is_Mounted": False,
        "Mount_Path": "",
        "Fields": CHUNKED_105_FIELDS if era == "105" else CHUNKED_104_FIELDS,
        "Values": container_rows_collection
    }

    temporary_file_descriptor, temporary_file_path_str = tempfile.mkstemp(suffix=container_extension)
    os.close(temporary_file_descriptor)
    try:
        with open(temporary_file_path_str, "w", encoding="utf-8") as temp_stream:
            json.dump(package_document_payload, temp_stream, indent=2)
        shutil.move(temporary_file_path_str, str(destination_file_path))
    finally:
        if os.path.exists(temporary_file_path_str):
            os.remove(temporary_file_path_str)

    app_logger_instance.info(f"Successfully packaged MFDB into {destination_file_path} ({len(container_rows_collection)} files)")
    return destination_file_path

# ── Sticky Mount Engine ─────────────────────────────────────────────────────────
def mount_mfdb_package(package_file_path: Path, workspace_directory_path: Path, force_reunpack: bool = False) -> Dict[str, Any]:
    """Mounts an MFDB container into a workspace with sticky-mount verification."""
    if not package_file_path.exists():
        raise FileNotFoundError(f"Package file does not exist: {package_file_path}")

    current_package_sha256_hash: str = calculate_file_sha256_hash(package_file_path)
    workspace_directory_path.mkdir(parents=True, exist_ok=True)
    lock_file_path: Path = workspace_directory_path / MFDB_LOCK_FILENAME

    if not force_reunpack and lock_file_path.exists():
        try:
            with open(lock_file_path, "r", encoding="utf-8") as lock_stream:
                lock_payload: Dict[str, Any] = json.load(lock_stream)
            if lock_payload.get("original_hash") == current_package_sha256_hash:
                app_logger_instance.info(f"Sticky mount validated against {MFDB_LOCK_FILENAME}. Workspace is up to date.")
                return {"status": "sticky_mount_reused", "workspace": str(workspace_directory_path), "files_unpacked": 0}
        except Exception as lock_read_error:
            app_logger_instance.warning(f"Failed to read existing lock file: {lock_read_error}. Performing clean unpack.")

    with open(package_file_path, "r", encoding="utf-8") as package_stream:
        package_document: Dict[str, Any] = json.load(package_stream)

    field_map_cache: Dict[str, int] = {
        field_definition["name"]: field_index
        for field_index, field_definition in enumerate(package_document.get("Fields", []))
    }

    relative_path_column_index: int = field_map_cache["Relative_Path"]
    is_binary_column_index: int = field_map_cache["Is_Binary"]
    file_content_column_index: int = field_map_cache["File_Content"]

    unpacked_files_count: int = 0
    for entity_row in package_document.get("Values", []):
        relative_file_path_value: str = entity_row[relative_path_column_index]
        is_binary_flag_value: bool = entity_row[is_binary_column_index]
        file_content_value: str = entity_row[file_content_column_index]

        resolved_target_file: Path = bejson_safe_path_resolve(workspace_directory_path, relative_file_path_value)
        resolved_target_file.parent.mkdir(parents=True, exist_ok=True)

        if is_binary_flag_value:
            resolved_target_file.write_bytes(base64.b64decode(file_content_value))
        else:
            resolved_target_file.write_text(file_content_value, encoding="utf-8")
        unpacked_files_count += 1

    lock_metadata_payload: Dict[str, Any] = {
        "chunk_doc_path": str(package_file_path.resolve()),
        "original_hash": current_package_sha256_hash,
        "mounted_at": str(workspace_directory_path.resolve()),
        "timestamp": os.path.getmtime(package_file_path)
    }
    with open(lock_file_path, "w", encoding="utf-8") as lock_write_stream:
        json.dump(lock_metadata_payload, lock_write_stream, indent=2)

    app_logger_instance.info(f"Unpacked {unpacked_files_count} files into workspace {workspace_directory_path}")
    return {"status": "unpacked", "workspace": str(workspace_directory_path), "files_unpacked": unpacked_files_count}

# ── Commit Engine with Pre-Write Validation Gate ───────────────────────────────
def commit_mfdb_workspace(workspace_directory_path: Path, output_file_path: Optional[Path] = None, validate: bool = True) -> Path:
    """Validates and re-packages workspace back to single-file container."""
    lock_file_path: Path = workspace_directory_path / MFDB_LOCK_FILENAME
    if not lock_file_path.exists():
        raise RuntimeError(f"Cannot commit: workspace is not mounted (missing {MFDB_LOCK_FILENAME})")

    with open(lock_file_path, "r", encoding="utf-8") as lock_stream:
        lock_metadata: Dict[str, Any] = json.load(lock_stream)

    destination_chunk_path: Path = output_file_path or Path(lock_metadata.get("chunk_doc_path", ""))
    if not destination_chunk_path:
        raise RuntimeError("Destination container path is unknown.")

    # ── Pre-Write Validation Gate ──────────────────────────────────────────────
    if validate:
        manifest_104_path: Path = workspace_directory_path / MFDB_MANIFEST_FILENAME_104
        manifest_105_path: Path = workspace_directory_path / MFDB_MANIFEST_FILENAME_105
        if not manifest_104_path.exists() and not manifest_105_path.exists():
            raise RuntimeError(f"Commit rejected by pre-write gate: Manifest missing in workspace.")

    era_choice: str = "105" if (workspace_directory_path / MFDB_MANIFEST_FILENAME_105).exists() else "104"
    packaged_result_path: Path = package_mfdb_database(workspace_directory_path, destination_chunk_path, era=era_choice)

    new_container_hash: str = calculate_file_sha256_hash(packaged_result_path)
    lock_metadata["original_hash"] = new_container_hash
    with open(lock_file_path, "w", encoding="utf-8") as lock_stream:
        json.dump(lock_metadata, lock_stream, indent=2)

    app_logger_instance.info(f"Workspace committed successfully to {packaged_result_path}")
    return packaged_result_path

# ── Validation Engine ──────────────────────────────────────────────────────────
def validate_mfdb_target(target_path: Path) -> Dict[str, Any]:
    """Validates an MFDB directory or container file."""
    if not target_path.exists():
        return {"valid": False, "errors": [f"Path not found: {target_path}"]}

    if target_path.is_file():
        try:
            with open(target_path, "r", encoding="utf-8") as doc_stream:
                doc_payload: Dict[str, Any] = json.load(doc_stream)
        except Exception as json_parse_error:
            return {"valid": False, "errors": [f"Invalid JSON: {json_parse_error}"]}

        schema_name_value: str = doc_payload.get("Schema_Name", "")
        if schema_name_value not in ("MFDB-132", "MFDB-140", "Chunked-104a"):
            return {"valid": False, "errors": [f"Unexpected schema name: {schema_name_value}"]}

        records_type_value: List[str] = doc_payload.get("Records_Type", [])
        if not ("MFDB-132" in records_type_value or "MFDB-140" in records_type_value or "Chunked" in records_type_value):
            return {"valid": False, "errors": [f"Unexpected Records_Type: {records_type_value}"]}

        return {"valid": True, "type": "container", "schema": schema_name_value, "records": len(doc_payload.get("Values", []))}

    manifest_file_104: Path = target_path / MFDB_MANIFEST_FILENAME_104
    manifest_file_105: Path = target_path / MFDB_MANIFEST_FILENAME_105
    if not manifest_file_104.exists() and not manifest_file_105.exists():
        return {"valid": False, "errors": [f"Missing manifest file in {target_path}"]}

    return {"valid": True, "type": "directory", "manifest": str(manifest_file_104 if manifest_file_104.exists() else manifest_file_105)}

# ── CLI Interface ──────────────────────────────────────────────────────────────
def build_argument_parser() -> argparse.ArgumentParser:
    cli_parser = argparse.ArgumentParser(
        description="MFDB Chunker CLI — Multi-File Database Container Packager & Sticky Mount Engine"
    )
    cli_parser.add_argument("--version", action="version", version=f"mfdb_chunker_cli {VERSION}")
    cli_parser.add_argument("--package", type=str, help="Package target MFDB directory into a container file")
    cli_parser.add_argument("--mount", type=str, help="Mount container file into workspace directory")
    cli_parser.add_argument("--workspace", type=str, help="Workspace directory for mount/commit/unmount operations")
    cli_parser.add_argument("--commit", type=str, help="Commit workspace directory back to container file")
    cli_parser.add_argument("--unmount", type=str, help="Safely unmount workspace (removes .mfdb132_lock)")
    cli_parser.add_argument("--validate", type=str, help="Validate MFDB directory or container file")
    cli_parser.add_argument("--out", type=str, help="Optional output container file path")
    cli_parser.add_argument("--era", type=str, choices=["104", "105"], default="104", help="BEJSON Era format (104 or 105)")
    cli_parser.add_argument("--force", action="store_true", help="Force re-unpacking during mount")
    return cli_parser

def main() -> int:
    cli_argument_parser = build_argument_parser()
    parsed_cli_arguments = cli_argument_parser.parse_args()

    try:
        if parsed_cli_arguments.package:
            target_directory_path = Path(parsed_cli_arguments.package).resolve()
            output_container_path = Path(parsed_cli_arguments.out).resolve() if parsed_cli_arguments.out else None
            packaged_file_path = package_mfdb_database(target_directory_path, output_container_path, era=parsed_cli_arguments.era)
            app_logger_instance.info(f"Package complete: {packaged_file_path}")
            return 0

        elif parsed_cli_arguments.mount:
            container_file_path = Path(parsed_cli_arguments.mount).resolve()
            if not parsed_cli_arguments.workspace:
                app_logger_instance.error("--mount requires --workspace <dir>")
                return 10
            target_workspace_path = Path(parsed_cli_arguments.workspace).resolve()
            mount_execution_result = mount_mfdb_package(container_file_path, target_workspace_path, force_reunpack=parsed_cli_arguments.force)
            app_logger_instance.info(f"Mount complete: {mount_execution_result['status']}")
            return 0

        elif parsed_cli_arguments.commit:
            target_workspace_path = Path(parsed_cli_arguments.commit).resolve()
            output_container_path = Path(parsed_cli_arguments.out).resolve() if parsed_cli_arguments.out else None
            committed_package_path = commit_mfdb_workspace(target_workspace_path, output_container_path)
            app_logger_instance.info(f"Commit complete: {committed_package_path}")
            return 0

        elif parsed_cli_arguments.unmount:
            target_workspace_path = Path(parsed_cli_arguments.unmount).resolve()
            target_lock_file = target_workspace_path / MFDB_LOCK_FILENAME
            if target_lock_file.exists():
                target_lock_file.unlink()
                app_logger_instance.info(f"Unmount complete: removed {MFDB_LOCK_FILENAME}")
            else:
                app_logger_instance.warning(f"No {MFDB_LOCK_FILENAME} found in workspace {target_workspace_path}")
            return 0

        elif parsed_cli_arguments.validate:
            target_path_to_validate = Path(parsed_cli_arguments.validate).resolve()
            validation_result_report = validate_mfdb_target(target_path_to_validate)
            if validation_result_report["valid"]:
                app_logger_instance.info(f"Validation PASSED: {validation_result_report}")
                return 0
            else:
                app_logger_instance.error(f"Validation FAILED: {validation_result_report['errors']}")
                return 30

        else:
            cli_argument_parser.print_help()
            return 0

    except Exception as runtime_execution_error:
        app_logger_instance.error(f"Operational error encountered: {runtime_execution_error}")
        return 10

if __name__ == "__main__":
    sys.exit(main())
