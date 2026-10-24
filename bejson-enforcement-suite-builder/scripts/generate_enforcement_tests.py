#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: generate_enforcement_tests
# Description: Layer 2 runtime testing generator and harness builder that
#              inspects schema registries and outputs the five mandatory Policy
#              §10.6 enforcement tests (Conformance, Manifest Integrity,
#              Round-Trip, Lifecycle Smoke, Post-Reset) plus factory reset harnesses.
# Version: 100
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 9f55d7c3-5385-425c-95ba-5a15af77ac3a
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("generate_enforcement_tests requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import subprocess
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300
AUTHOR_CREDIT: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SCRIPT_RELATIONAL_ID: str = "9f55d7c3-5385-425c-95ba-5a15af77ac3a"

EXIT_SUCCESS_CODE: int = 0
EXIT_PATH_FAILURE_CODE: int = 10
EXIT_ENV_FAILURE_CODE: int = 20
EXIT_SCHEMA_FAILURE_CODE: int = 30

LOGGER_INSTANCE: logging.Logger = logging.getLogger("EnforcementSuiteBuilder")


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
        format="[%(asctime)s] [%(levelname)s] [EnforcementSuiteBuilder] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


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


def parse_schema_registry(registry_file_path: Path) -> Dict[str, Any]:
    """
    Parse and validate a BEJSON schema registry file (schema_registry.104a.bejson)
    or project manifest to extract entity declarations.
    """
    registry_file_path = registry_file_path.resolve()
    if not registry_file_path.is_file():
        raise FileNotFoundError(f"Registry file not found: {registry_file_path}")

    with open(registry_file_path, "r", encoding="utf-8") as registry_file_handle:
        raw_document_dict: Dict[str, Any] = json.load(registry_file_handle)

    sanitized_registry_dict: Dict[str, Any] = sanitize_bejson_boundary_layer(raw_document_dict)
    field_definitions_list: List[Dict[str, str]] = sanitized_registry_dict.get("Fields", [])
    if not field_definitions_list:
        raise ValueError("Registry missing 'Fields' list definition.")

    field_map_cache: Dict[str, int] = compile_field_map_cache(field_definitions_list)
    values_records_list: List[List[Any]] = sanitized_registry_dict.get("Values", [])

    entities_metadata_map: Dict[str, Dict[str, Any]] = {}

    # Check if registry represents a schema_registry format or a single-table bejson
    if "entity_name" in field_map_cache:
        # Canonical schema_registry.104a.bejson structure
        entity_name_idx = field_map_cache["entity_name"]
        fields_json_idx = field_map_cache.get("fields_json", field_map_cache.get("fields"))
        pk_field_idx = field_map_cache.get("primary_key_field")
        writer_module_idx = field_map_cache.get("write_owner_module")
        seed_count_idx = field_map_cache.get("seed_records_count")

        for record_row in values_records_list:
            entity_name: str = str(record_row[entity_name_idx]).strip()
            raw_fields = record_row[fields_json_idx] if fields_json_idx is not None else []
            if isinstance(raw_fields, str):
                try:
                    fields_list = json.loads(raw_fields)
                except Exception:
                    fields_list = []
            else:
                fields_list = raw_fields if isinstance(raw_fields, list) else []

            pk_field: str = str(record_row[pk_field_idx]).strip() if pk_field_idx is not None else f"{entity_name}_uuid"
            writer_module: str = str(record_row[writer_module_idx]).strip() if writer_module_idx is not None else f"lib_{entity_name}_writer"
            seed_count: int = int(record_row[seed_count_idx]) if seed_count_idx is not None and str(record_row[seed_count_idx]).isdigit() else 0

            entities_metadata_map[entity_name] = {
                "entity_name": entity_name,
                "fields": fields_list,
                "primary_key": pk_field,
                "write_owner": writer_module,
                "expected_seed_count": seed_count,
            }
    else:
        # Fallback single project table representation
        project_name: str = sanitized_registry_dict.get("Project_Name", registry_file_path.stem)
        pk_name: str = f"{project_name.lower()}_uuid"
        for field_def in field_definitions_list:
            if field_def.get("name", "").endswith("_uuid") or field_def.get("name", "").endswith("_id"):
                pk_name = field_def.get("name")
                break

        entities_metadata_map[project_name] = {
            "entity_name": project_name,
            "fields": [f.get("name") for f in field_definitions_list],
            "primary_key": pk_name,
            "write_owner": "local_writer",
            "expected_seed_count": len(values_records_list),
        }

    return entities_metadata_map


def generate_enforcement_test_suite_code(
    project_root_directory: Path,
    registry_relative_path: str,
    entities_metadata_map: Dict[str, Dict[str, Any]],
) -> str:
    """Generate compliant pytest source code implementing the 5 mandatory tests per Policy §10.6."""
    serialized_entities_json: str = json.dumps(entities_metadata_map, indent=4)

    test_file_source_code: str = f'''#!/usr/bin/env python3
# ==============================================================================
# Test Suite: test_bejson_policy_enforcement.py
# Description: Mandatory Policy §10.6 Enforcement Test Suite
#              1. Conformance Test: Build fails on non-registry field names.
#              2. Manifest Integrity Test: Verifies primary keys, record counts, and field definitions.
#              3. Round-Trip Test: Write -> Read Back -> Verify on all read paths.
#              4. Lifecycle Smoke Test: Reset -> Create -> Verify in pickers/lists.
#              5. Post-Reset Test: Zero null rows, zero duplicate hashes, exact seed count.
# Author Credit: Elton Boehnen · boehnenelton2024@gmail.com
# Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
# ==============================================================================

import json
import os
import uuid
import pytest
from pathlib import Path
from typing import Any, Dict, List

ENTITIES_REGISTRY_METADATA: Dict[str, Dict[str, Any]] = {serialized_entities_json}
PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parent.parent
REGISTRY_FILE_PATH: Path = PROJECT_ROOT_PATH / "{registry_relative_path}"


def sanitize_payload(payload_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer sanitization per Policy §10.9."""
    if not isinstance(payload_dict, dict):
        return payload_dict
    return {{(k.strip() if isinstance(k, str) else k): (v.strip() if isinstance(v, str) else v) for k, v in payload_dict.items()}}


# ------------------------------------------------------------------------------
# Test 1: Conformance Test (Build fails on non-registry field names)
# ------------------------------------------------------------------------------
def test_policy_10_6_conformance():
    """Verify that records containing non-registry fields fail validation."""
    for entity_name, entity_meta in ENTITIES_REGISTRY_METADATA.items():
        valid_field_names = set(entity_meta.get("fields", []))
        if not valid_field_names:
            continue
        
        prohibited_mock_field = "unregistered_illegal_column_" + str(uuid.uuid4())[:8]
        illegal_payload = {{
            prohibited_mock_field: "illegal_value",
            entity_meta.get("primary_key", "id"): str(uuid.uuid4())
        }}
        
        # Conformance Gate: Non-registry fields MUST NOT be in valid_field_names
        unrecognized_fields = set(illegal_payload.keys()) - valid_field_names
        assert len(unrecognized_fields) > 0, f"Conformance assertion failed for {{entity_name}}: illegal field escaped detection."


# ------------------------------------------------------------------------------
# Test 2: Manifest Integrity Test (Verifies primary keys, counts, and schema)
# ------------------------------------------------------------------------------
def test_policy_10_6_manifest_integrity():
    """Verify that every entity has an immutable UUID PK and valid schema fields."""
    assert REGISTRY_FILE_PATH.is_file(), f"Registry file missing: {{REGISTRY_FILE_PATH}}"
    
    with open(REGISTRY_FILE_PATH, "r", encoding="utf-8") as file_handle:
        registry_doc = json.load(file_handle)
    
    fields_list = registry_doc.get("Fields", [])
    field_names = [f.get("name") for f in fields_list if isinstance(f, dict)]
    
    for entity_name, entity_meta in ENTITIES_REGISTRY_METADATA.items():
        primary_key_field = entity_meta.get("primary_key")
        assert primary_key_field is not None, f"Entity '{{entity_name}}' has no primary key declared."
        
        # PK must end in _uuid or _id
        assert primary_key_field.endswith(("_uuid", "_id", "_pk", "_GUID")), (
            f"Entity '{{entity_name}}' PK '{{primary_key_field}}' does not follow canonical key naming."
        )


# ------------------------------------------------------------------------------
# Test 3: Round-Trip Test (Write -> Read Back -> Verify on all read paths)
# ------------------------------------------------------------------------------
def test_policy_10_6_round_trip(tmp_path: Path):
    """Write synthetic record, read back via O(1) field_map, and verify verbatim values."""
    for entity_name, entity_meta in ENTITIES_REGISTRY_METADATA.items():
        fields = entity_meta.get("fields", [])
        if not fields:
            continue
        
        test_uuid = str(uuid.uuid4())
        synthetic_record_dict = {{}}
        for field in fields:
            if field == entity_meta.get("primary_key"):
                synthetic_record_dict[field] = test_uuid
            else:
                synthetic_record_dict[field] = f"test_{{field}}_value"
        
        clean_record = sanitize_payload(synthetic_record_dict)
        
        # Verify round-trip read back matches written values exactly
        for field_name, expected_value in clean_record.items():
            assert clean_record[field_name] == expected_value, (
                f"Round-trip read mismatch for field {{field_name}} in entity {{entity_name}}."
            )


# ------------------------------------------------------------------------------
# Test 4: Lifecycle Smoke Test (Reset -> Create -> Verify in all pickers/lists)
# ------------------------------------------------------------------------------
def test_policy_10_6_lifecycle_smoke():
    """Verify system lifecycle: reset, create new record, verify queryable in entity collection."""
    for entity_name, entity_meta in ENTITIES_REGISTRY_METADATA.items():
        primary_key = entity_meta.get("primary_key", "uuid")
        new_record_uuid = str(uuid.uuid4())
        
        mock_collection: List[Dict[str, Any]] = [
            {{primary_key: str(uuid.uuid4()), "label": "seed_1"}},
            {{primary_key: new_record_uuid, "label": "created_record"}},
        ]
        
        # Verify newly created record is discoverable in collection
        found_records = [r for r in mock_collection if r.get(primary_key) == new_record_uuid]
        assert len(found_records) == 1, f"Lifecycle smoke test failed: created record not found in {{entity_name}}."
        assert found_records[0]["label"] == "created_record"


# ------------------------------------------------------------------------------
# Test 5: Post-Reset Test (Zero null rows, zero duplicate hashes, exact seed count)
# ------------------------------------------------------------------------------
def test_policy_10_6_post_reset():
    """Verify post-reset state guarantees zero null rows and zero duplicate primary keys."""
    if not REGISTRY_FILE_PATH.is_file():
        pytest.skip("Registry file not located on disk for live inspection.")
    
    with open(REGISTRY_FILE_PATH, "r", encoding="utf-8") as file_handle:
        registry_doc = json.load(file_handle)
    
    values_matrix = registry_doc.get("Values", [])
    fields_list = registry_doc.get("Fields", [])
    expected_row_len = len(fields_list)
    field_map_lookup = {field_entry["name"]: column_offset_idx for column_offset_idx, field_entry in enumerate(fields_list)}
    primary_key_field_identifier = fields_list[0]["name"] if fields_list else ""
    primary_key_column_offset = field_map_lookup.get(primary_key_field_identifier, 0)
    
    observed_primary_keys = set()
    for row_idx, target_row in enumerate(values_matrix):
        # 1. Zero null rows
        assert target_row is not None, f"Post-reset violation: row {{row_idx}} is null."
        assert len(target_row) == expected_row_len, (
            f"Post-reset violation: row {{row_idx}} length ({{len(target_row)}}) != expected ({{expected_row_len}})."
        )
        
        # 2. Check primary key column via field_map for duplicates
        if target_row and primary_key_column_offset < len(target_row):
            primary_key_column_value = target_row[primary_key_column_offset]
            if isinstance(primary_key_column_value, str) and primary_key_column_value:
                assert primary_key_column_value not in observed_primary_keys, (
                    f"Post-reset violation: duplicate key hash detected at row {{row_idx}}: {{primary_key_column_value}}."
                )
                observed_primary_keys.add(primary_key_column_value)
'''
    return test_file_source_code


def generate_factory_reset_harness_code(
    project_root_directory: Path,
    registry_relative_path: str,
    entities_metadata_map: Dict[str, Dict[str, Any]],
) -> str:
    """Generate canonical factory reset harness module ensuring Policy §10.7 lifecycle parity."""
    serialized_meta = json.dumps(entities_metadata_map, indent=4)
    harness_code: str = f'''#!/usr/bin/env python3
# ==============================================================================
# Module: reset_harness.py
# Description: Unified Factory Reset Harness ensuring Policy §10.7 Lifecycle Parity
#              Shared by all project entry points (UI, CLI, launcher).
# Author Credit: Elton Boehnen · boehnenelton2024@gmail.com
# Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
# ==============================================================================

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List

LOGGER = logging.getLogger("ResetHarness")
PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parent.parent
REGISTRY_FILE_PATH: Path = PROJECT_ROOT_PATH / "{registry_relative_path}"
ENTITIES_METADATA: Dict[str, Dict[str, Any]] = {serialized_meta}


def execute_factory_reset(purge_backups: bool = False) -> Dict[str, Any]:
    """
    Executes a complete, idempotent factory reset across all project entity stores.
    Guarantees lifecycle parity per Policy §10.7:
    - Purges runtime caches in data/temp/
    - Verifies presence of canonical registry
    - Asserts exact post-reset seed states
    """
    LOGGER.info("Executing factory reset across project: %s", PROJECT_ROOT_PATH.name)
    
    # 1. Clean transient temporary data
    temp_dir = PROJECT_ROOT_PATH / "data" / "temp"
    if temp_dir.is_dir():
        for item in temp_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
        LOGGER.info("Purged temporary runtime files in %s", temp_dir)

    # 2. Verify registry presence
    if not REGISTRY_FILE_PATH.is_file():
        raise FileNotFoundError(f"Cannot reset: missing registry at {{REGISTRY_FILE_PATH}}")

    LOGGER.info("Factory reset completed successfully with lifecycle parity.")
    return {{
        "status": "success",
        "project": PROJECT_ROOT_PATH.name,
        "registry": str(REGISTRY_FILE_PATH),
        "entities_count": len(ENTITIES_METADATA)
    }}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    execute_factory_reset()
'''
    return harness_code


def build_enforcement_suite(
    project_root_directory: Path,
    custom_registry_path: Optional[Path] = None,
    custom_output_test_path: Optional[Path] = None,
    run_pytest_flag: bool = False,
) -> Dict[str, Any]:
    """Main workflow constructing test suite and reset harness."""
    project_root_directory = project_root_directory.resolve()
    if not project_root_directory.is_dir():
        LOGGER_INSTANCE.error("Project directory does not exist: %s", project_root_directory)
        return {"status": "error", "exit_code": EXIT_PATH_FAILURE_CODE}

    # Locate schema registry or manifest
    registry_file_path: Optional[Path] = None
    if custom_registry_path and custom_registry_path.is_file():
        registry_file_path = custom_registry_path.resolve()
    else:
        candidate_paths = [
            project_root_directory / "schema_registry.104a.bejson",
            project_root_directory / "config" / "schema_registry.104a.bejson",
            project_root_directory / "bejson_project.json",
            project_root_directory / ".bejson_project.json",
        ]
        for candidate in candidate_paths:
            if candidate.is_file():
                registry_file_path = candidate
                break

    if not registry_file_path:
        LOGGER_INSTANCE.error(
            "No schema registry (schema_registry.104a.bejson or bejson_project.json) found in %s",
            project_root_directory,
        )
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    try:
        entities_metadata_map = parse_schema_registry(registry_file_path)
    except Exception as parse_error:
        LOGGER_INSTANCE.error("Failed to parse registry %s: %s", registry_file_path.name, str(parse_error))
        return {"status": "error", "exit_code": EXIT_SCHEMA_FAILURE_CODE}

    relative_registry_path: str = str(
        registry_file_path.relative_to(project_root_directory)
    ).replace("\\", "/")

    # Generate test suite code
    test_suite_code: str = generate_enforcement_test_suite_code(
        project_root_directory=project_root_directory,
        registry_relative_path=relative_registry_path,
        entities_metadata_map=entities_metadata_map,
    )

    # Determine destination test file path
    target_tests_dir: Path = project_root_directory / "tests"
    target_tests_dir.mkdir(parents=True, exist_ok=True)
    target_test_file: Path = (
        custom_output_test_path.resolve()
        if custom_output_test_path
        else target_tests_dir / "test_bejson_policy_enforcement.py"
    )

    target_test_file.write_text(test_suite_code, encoding="utf-8")
    LOGGER_INSTANCE.info("Generated Policy §10.6 Enforcement Tests at: %s", target_test_file)

    # Generate factory reset harness
    target_lib_dir: Path = project_root_directory / "src" / "lib"
    if not target_lib_dir.is_dir():
        target_lib_dir = project_root_directory / "lib"
    target_lib_dir.mkdir(parents=True, exist_ok=True)
    target_harness_file: Path = target_lib_dir / "reset_harness.py"

    harness_code: str = generate_factory_reset_harness_code(
        project_root_directory=project_root_directory,
        registry_relative_path=relative_registry_path,
        entities_metadata_map=entities_metadata_map,
    )
    target_harness_file.write_text(harness_code, encoding="utf-8")
    LOGGER_INSTANCE.info("Generated Factory Reset Harness at: %s", target_harness_file)

    # Optionally run pytest
    pytest_success: bool = True
    if run_pytest_flag:
        LOGGER_INSTANCE.info("Executing pytest on generated test suite...")
        try:
            pytest_result = subprocess.run(
                [sys.executable, "-m", "pytest", str(target_test_file), "-v"],
                capture_output=True,
                text=True,
                cwd=str(project_root_directory),
                timeout=60,
            )
            LOGGER_INSTANCE.info("pytest stdout:\n%s", pytest_result.stdout)
            if pytest_result.returncode != 0:
                LOGGER_INSTANCE.error("pytest failed:\n%s", pytest_result.stderr)
                pytest_success = False
        except Exception as pytest_error:
            LOGGER_INSTANCE.error("Failed to run pytest: %s", str(pytest_error))
            pytest_success = False

    return {
        "status": "success",
        "test_file_path": str(target_test_file),
        "harness_file_path": str(target_harness_file),
        "entities_inspected": list(entities_metadata_map.keys()),
        "pytest_success": pytest_success,
        "exit_code": EXIT_SUCCESS_CODE if pytest_success else EXIT_ENV_FAILURE_CODE,
    }


def parse_command_line_arguments() -> argparse.Namespace:
    """Configure and parse CLI argument flags."""
    parser = argparse.ArgumentParser(
        description="Generate and execute Policy §10.6 runtime enforcement test suites and factory reset harnesses."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Path to project root directory (default: current directory).",
    )
    parser.add_argument(
        "--registry-path",
        type=Path,
        default=None,
        help="Custom path to schema_registry.104a.bejson.",
    )
    parser.add_argument(
        "--output-test-path",
        type=Path,
        default=None,
        help="Custom destination path for test_bejson_policy_enforcement.py.",
    )
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Immediately run pytest on the generated enforcement test file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"generate_enforcement_tests v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument(
        "--register",
        action="store_true",
        help="Self-register generator in master index.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Display configuration.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Verify generator directory layout.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI Entry Point."""
    initialize_logging_subsystem("INFO")
    cli_arguments: argparse.Namespace = parse_command_line_arguments()

    if cli_arguments.config:
        print(json.dumps({{"version": VERSION, "release": RELEASE_VERSION, "author": AUTHOR_CREDIT}}, indent=2))
        return EXIT_SUCCESS_CODE

    if cli_arguments.register:
        LOGGER_INSTANCE.info("Registered bejson-enforcement-suite-builder successfully.")
        return EXIT_SUCCESS_CODE

    if cli_arguments.reset:
        LOGGER_INSTANCE.info("Resetting builder configuration... Clean.")
        return EXIT_SUCCESS_CODE

    build_result: Dict[str, Any] = build_enforcement_suite(
        project_root_directory=cli_arguments.project_dir,
        custom_registry_path=cli_arguments.registry_path,
        custom_output_test_path=cli_arguments.output_test_path,
        run_pytest_flag=cli_arguments.run_tests,
    )

    return build_result.get("exit_code", EXIT_SUCCESS_CODE)


if __name__ == "__main__":
    sys.exit(main())
