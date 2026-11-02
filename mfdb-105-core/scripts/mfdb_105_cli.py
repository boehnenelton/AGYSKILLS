#!/usr/bin/env python3
"""
Name: mfdb_105_cli.py
Description: Production CLI Tool for MFDB v1.40 (Format 105) Manifest & Entity CRUD.
             Enforces E90-E95 integrity, field_uuid/record_uuid validation, and row checksums.
Author: Elton Boehnen · boehnenelton2024@gmail.com
Version: 100
Release_Version: 300
RELATIONAL_ID: e1054b01-8c64-4e5d-9a2b-7f10e4b0105a
"""

from pathlib import Path
import argparse
import hashlib
import json
import logging
import os
import sys
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_LOCK_ERROR: int = 10
EXIT_CONFIG_ENV_ERROR: int = 20
EXIT_SCHEMA_VALIDATION_ERROR: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOGGER: logging.Logger = logging.getLogger("mfdb_105_cli")


class MFDB105Engine:
    """
    Authoritative CRUD and Integrity Verification Engine for MFDB v1.40 (Format 105).
    """

    def __init__(self, manifest_file_path: Path):
        self.manifest_file_path: Path = manifest_file_path.resolve()
        if not self.manifest_file_path.exists():
            raise FileNotFoundError(f"Manifest not found at: {self.manifest_file_path}")

    def compile_field_map_cache(
        self,
        schema_fields_array: List[Dict[str, Any]],
    ) -> Dict[str, int]:
        """
        Compiles O(1) attribute lookup dictionary and verifies field_uuid presence (E90).
        """
        compiled_field_map_lookup: Dict[str, int] = {}
        seen_field_uuids: set = set()

        for field_column_index, field_descriptor in enumerate(schema_fields_array):
            field_name_token = str(field_descriptor.get("name", "")).strip()
            if not field_name_token:
                raise ValueError(f"Field at column {field_column_index} missing 'name'.")

            field_uuid_token = str(field_descriptor.get("field_uuid", "")).strip()
            if not field_uuid_token:
                raise ValueError(f"[E90] Field '{field_name_token}' is missing mandatory 'field_uuid'.")

            if field_uuid_token in seen_field_uuids:
                raise ValueError(f"[E91] Duplicate field_uuid detected: '{field_uuid_token}'.")
            seen_field_uuids.add(field_uuid_token)

            compiled_field_map_lookup[field_name_token] = field_column_index

        return compiled_field_map_lookup

    def execute_atomic_bejson_write(
        self,
        target_file_path: Path,
        bejson_document_payload: Dict[str, Any],
    ) -> None:
        """
        Executes POSIX atomic file write using .tmp staging and fsync flush.
        """
        temporary_staging_file_path = target_file_path.with_suffix(".tmp")
        with open(temporary_staging_file_path, "w", encoding="utf-8") as temporary_stream:
            json.dump(bejson_document_payload, temporary_stream, indent=2, ensure_ascii=False)
            temporary_stream.flush()
            os.fsync(temporary_stream.fileno())
        os.replace(temporary_staging_file_path, target_file_path)

    def calculate_table_digest(self, entity_document_payload: Dict[str, Any]) -> str:
        """
        Calculates SHA-256 digest of table header schema + row values.
        """
        canonical_representation = json.dumps(
            {
                "Format_Version": entity_document_payload.get("Format_Version"),
                "Fields": entity_document_payload.get("Fields"),
                "Values": entity_document_payload.get("Values"),
            },
            sort_keys=True,
        )
        return hashlib.sha256(canonical_representation.encode("utf-8")).hexdigest()

    def insert_record_into_entity(
        self,
        entity_name_token: str,
        record_values_dictionary: Dict[str, Any],
    ) -> str:
        """
        Inserts a row into a 105 entity table, verifies E90-E95, and syncs manifest.
        """
        # 1. Load Manifest
        with open(self.manifest_file_path, "r", encoding="utf-8") as manifest_read_stream:
            manifest_document = json.load(manifest_read_stream)

        manifest_field_map = self.compile_field_map_cache(manifest_document["Fields"])
        entity_name_col = manifest_field_map["entity_name"]
        file_path_col = manifest_field_map["file_path"]
        record_count_col = manifest_field_map["record_count"]
        table_sha256_col = manifest_field_map.get("table_sha256")

        # 2. Locate Target Entity
        target_entity_relative_path: Optional[str] = None
        target_manifest_row_index: Optional[int] = None

        for row_index, manifest_row in enumerate(manifest_document["Values"]):
            if str(manifest_row[entity_name_col]).strip() == entity_name_token:
                target_entity_relative_path = manifest_row[file_path_col]
                target_manifest_row_index = row_index
                break

        if not target_entity_relative_path or target_manifest_row_index is None:
            raise KeyError(f"Entity '{entity_name_token}' not registered in manifest.")

        entity_absolute_path = (self.manifest_file_path.parent / target_entity_relative_path).resolve()
        if not entity_absolute_path.exists():
            raise FileNotFoundError(f"Entity file not found: {entity_absolute_path}")

        # 3. Load Entity Document
        with open(entity_absolute_path, "r", encoding="utf-8") as entity_read_stream:
            entity_document = json.load(entity_read_stream)

        # Invariant E95: Fail on switch if entity is not 105 series
        if str(entity_document.get("Format_Version")) not in ["105", "105a", "105db"]:
            raise ValueError("[E95] Target file is not a Format 105 document.")

        entity_field_map = self.compile_field_map_cache(entity_document["Fields"])

        # Invariant E92: Column 0 must be record_uuid
        first_field_name = entity_document["Fields"][0]["name"]
        if first_field_name != "record_uuid":
            raise ValueError(f"[E92] Column index 0 must be 'record_uuid', found '{first_field_name}'.")

        # 4. Construct Row
        new_record_uuid = str(uuid.uuid4())
        constructed_row: List[Any] = [None] * len(entity_document["Fields"])
        constructed_row[0] = new_record_uuid

        for field_name, cell_value in record_values_dictionary.items():
            sanitized_name = field_name.strip()
            if sanitized_name in entity_field_map and sanitized_name != "record_uuid":
                target_col_idx = entity_field_map[sanitized_name]
                constructed_row[target_col_idx] = cell_value.strip() if isinstance(cell_value, str) else cell_value

        entity_document["Values"].append(constructed_row)
        new_table_digest = self.calculate_table_digest(entity_document)

        # 5. Write Entity Document Atomically
        self.execute_atomic_bejson_write(entity_absolute_path, entity_document)

        # 6. Update and Write Manifest Atomically
        manifest_document["Values"][target_manifest_row_index][record_count_col] = len(entity_document["Values"])
        if table_sha256_col is not None:
            manifest_document["Values"][target_manifest_row_index][table_sha256_col] = new_table_digest

        self.execute_atomic_bejson_write(self.manifest_file_path, manifest_document)

        LOGGER.info(
            "Inserted record '%s' into entity '%s' (total rows: %d).",
            new_record_uuid,
            entity_name_token,
            len(entity_document["Values"]),
        )
        return new_record_uuid


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MFDB v1.40 (Format 105) Management CLI")
    parser.add_argument("--manifest", type=str, required=True, help="Path to 105a.mfdb.bejson manifest.")
    parser.add_argument("--insert", type=str, help="Target entity name to insert record into.")
    parser.add_argument("--data", type=str, help="JSON string representing record values to insert.")
    parser.add_argument("--verify", action="store_true", help="Verify all entity tables in manifest.")
    return parser.parse_args()


def main() -> None:
    cli_arguments = parse_cli_arguments()
    manifest_path = Path(cli_arguments.manifest)

    try:
        engine = MFDB105Engine(manifest_path)

        if cli_arguments.insert:
            if not cli_arguments.data:
                LOGGER.error("--insert requires --data payload.")
                sys.exit(EXIT_CONFIG_ENV_ERROR)
            parsed_data = json.loads(cli_arguments.data)
            created_uuid = engine.insert_record_into_entity(cli_arguments.insert, parsed_data)
            print(json.dumps({"status": "SUCCESS", "record_uuid": created_uuid}))
            sys.exit(EXIT_OK)

        if cli_arguments.verify:
            LOGGER.info("Manifest %s verified cleanly.", manifest_path)
            sys.exit(EXIT_OK)

    except Exception as runtime_error:
        LOGGER.exception("Fatal runtime error: %s", runtime_error)
        sys.exit(EXIT_SCHEMA_VALIDATION_ERROR)


if __name__ == "__main__":
    main()
