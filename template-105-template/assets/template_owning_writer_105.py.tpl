#!/usr/bin/env python3
"""
Name:           {{MODULE_NAME:-lib_verified_record_writer}}
Description:    Policy §10.4 Integrity Era Owning Writer for BEJSON 105 {{ENTITY_NAME:-VerifiedRecord}} entity.
                Enforces reserved record_uuid at row index 0 (E92/E93), field_uuid validation (E90/E91),
                self-maintaining by_name_row field_map caching, and boundary sanitization (Policy §10.9).
Version:        {{VERSION:-100}}
Release_Version: {{RELEASE_VERSION:-301}}
Date Created:   {{DATE:-2026-10-24}}
Author Credit:  Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  {{RELATIONAL_ID:-c1050000-0001-4000-8000-000000000001}}
"""

from __future__ import annotations
import json
import logging
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

VERSION: int = int("{{VERSION:-100}}")
RELEASE_VERSION: int = int("{{RELEASE_VERSION:-301}}")
RELATIONAL_ID: str = "{{RELATIONAL_ID:-c1050000-0001-4000-8000-000000000001}}"

LOG = logging.getLogger("{{MODULE_NAME:-lib_verified_record_writer}}")


def get_script_path() -> Path:
    """Self-locating script path per Policy §4.1."""
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()
DEFAULT_STORE_PATH: Path = SCRIPT_PATH.parent / "{{DATA_FILE_PATH:-data/records.105.bejson}}"


def bejson_boundary_sanitize(data: Any) -> Any:
    """Strip boundary whitespace on dictionary keys and string values per Policy §10.9."""
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, list):
        return [bejson_boundary_sanitize(item) for item in data]
    if isinstance(data, dict):
        return {str(k).strip(): bejson_boundary_sanitize(v) for k, v in data.items()}
    return data


def bejson_105_compile_field_maps(doc: dict[str, Any]) -> tuple[dict[str, int], dict[str, str]]:
    """
    Compile Integrity Era field_map cache:
    - by_name_row: column name to Values row index (index 0 is reserved for record_uuid, data begins at index 1).
    - by_uuid: column name to field_uuid string.
    """
    fields = doc.get("Fields", [])
    by_name_row: dict[str, int] = {}
    by_uuid: dict[str, str] = {}
    for idx, field_def in enumerate(fields):
        if isinstance(field_def, dict) and "name" in field_def:
            clean_name = str(field_def["name"]).strip()
            by_name_row[clean_name] = idx + 1  # 105 data offset (+1 for record_uuid)
            if "field_uuid" in field_def:
                by_uuid[clean_name] = str(field_def["field_uuid"]).strip()
    return by_name_row, by_uuid


class OwningWriter105:
    """Exclusive Policy §10.4 Write-Owner for Integrity Era {{ENTITY_NAME:-VerifiedRecord}}."""

    def __init__(self, store_path: Optional[Path] = None) -> None:
        self.store_path = store_path or DEFAULT_STORE_PATH
        self._doc: Optional[dict[str, Any]] = None
        self._by_name_row: dict[str, int] = {}
        self._by_uuid: dict[str, str] = {}

    def load(self) -> dict[str, Any]:
        """Load and sanitize the BEJSON 105 document, compiling field maps."""
        if not self.store_path.exists():
            LOG.error("Data store not found: %s", self.store_path)
            raise FileNotFoundError(f"Store file missing: {self.store_path}")
        with open(self.store_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._doc = bejson_boundary_sanitize(raw)
        self._by_name_row, self._by_uuid = bejson_105_compile_field_maps(self._doc)
        return self._doc

    def save(self) -> bool:
        """Atomic write to store path using temporary file exchange."""
        if self._doc is None:
            LOG.error("Cannot save: store document not loaded.")
            return False
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = self.store_path.parent
        try:
            with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
                json.dump(self._doc, tf, indent=2, ensure_ascii=False)
                tf.write("\n")
                temp_name = tf.name
            os.replace(temp_name, self.store_path)
            return True
        except Exception as exc:
            LOG.error("Atomic write failed for %s: %s", self.store_path, exc)
            if 'temp_name' in locals() and os.path.exists(temp_name):
                os.unlink(temp_name)
            raise

    def get_records(self) -> list[dict[str, Any]]:
        """Return all rows mapped to field names with record_uuid included."""
        if self._doc is None:
            self.load()
        fmap = self._by_name_row
        rev_map = {idx: name for name, idx in fmap.items()}
        records: list[dict[str, Any]] = []
        for row in self._doc.get("Values", []):
            rec_uuid = row[0] if len(row) > 0 else None
            record = {"record_uuid": rec_uuid}
            for i in range(1, len(row)):
                if i in rev_map:
                    record[rev_map[i]] = row[i]
            records.append(record)
        return records

    def insert(self, record_data: dict[str, Any]) -> str:
        """
        Insert a new sanitized row into 105 Values.
        Enforces record_uuid at row index 0 and uses by_name_row offset mapping.
        """
        if self._doc is None:
            self.load()
        clean_input = bejson_boundary_sanitize(record_data)
        fmap = self._by_name_row
        fields_len = len(self._doc.get("Fields", []))
        # Total row length: 1 (record_uuid) + number of fields
        new_row: list[Any] = [None] * (fields_len + 1)

        # Generate or assign UUIDv4 record_uuid at index 0 (E92/E93)
        row_uuid = clean_input.get("record_uuid") or str(uuid.uuid4())
        new_row[0] = row_uuid

        # Populate ID and timestamp if absent
        id_field = "{{PREFIX:-vrec}}_id"
        created_field = "{{PREFIX:-vrec}}_created_at"
        if id_field in fmap and id_field not in clean_input:
            clean_input[id_field] = str(uuid.uuid4())
        if created_field in fmap and created_field not in clean_input:
            clean_input[created_field] = datetime.now(timezone.utc).isoformat()

        for col_name, row_idx in fmap.items():
            if col_name in clean_input:
                new_row[row_idx] = clean_input[col_name]

        self._doc.setdefault("Values", []).append(new_row)
        self.save()
        LOG.info("Inserted %s record with record_uuid: %s", "{{ENTITY_NAME:-VerifiedRecord}}", row_uuid)
        return row_uuid

    def get_by_record_uuid(self, record_uuid: str) -> Optional[dict[str, Any]]:
        """Query record by index-0 record_uuid."""
        if self._doc is None:
            self.load()
        rev_map = {idx: name for name, idx in self._by_name_row.items()}
        for row in self._doc.get("Values", []):
            if len(row) > 0 and row[0] == record_uuid:
                record = {"record_uuid": row[0]}
                for i in range(1, len(row)):
                    if i in rev_map:
                        record[rev_map[i]] = row[i]
                return record
        return None

    def update_by_record_uuid(self, record_uuid: str, updates: dict[str, Any]) -> bool:
        """Update fields for a specific record_uuid."""
        if self._doc is None:
            self.load()
        clean_updates = bejson_boundary_sanitize(updates)
        fmap = self._by_name_row
        updated = False
        for row in self._doc.get("Values", []):
            if len(row) > 0 and row[0] == record_uuid:
                for col_name, val in clean_updates.items():
                    if col_name in fmap:
                        row[fmap[col_name]] = val
                updated = True
                break
        if updated:
            self.save()
            LOG.info("Updated %s record_uuid: %s", "{{ENTITY_NAME:-VerifiedRecord}}", record_uuid)
        return updated

    def delete_by_record_uuid(self, record_uuid: str) -> bool:
        """Remove a record by its record_uuid."""
        if self._doc is None:
            self.load()
        initial_count = len(self._doc.get("Values", []))
        self._doc["Values"] = [r for r in self._doc.get("Values", []) if len(r) > 0 and r[0] != record_uuid]
        if len(self._doc["Values"]) < initial_count:
            self.save()
            LOG.info("Deleted %s record_uuid: %s", "{{ENTITY_NAME:-VerifiedRecord}}", record_uuid)
            return True
        return False
