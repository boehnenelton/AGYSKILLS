#!/usr/bin/env python3
"""
Name:           {{MODULE_NAME:-lib_record_writer}}
Description:    Policy §10.4 Owning Writer for BEJSON 104 {{ENTITY_NAME:-StandardRecord}} entity.
                Provides atomic persistence, dynamic O(1) field_map cache (Policy §6.2),
                and boundary-layer whitespace sanitization (Policy §10.9).
Version:        {{VERSION:-100}}
Release_Version: {{RELEASE_VERSION:-300}}
Date Created:   {{DATE:-2026-10-24}}
Author Credit:  Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  {{RELATIONAL_ID:-c1040000-0001-4000-8000-000000000001}}
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
RELEASE_VERSION: int = int("{{RELEASE_VERSION:-300}}")
RELATIONAL_ID: str = "{{RELATIONAL_ID:-c1040000-0001-4000-8000-000000000001}}"

LOG = logging.getLogger("{{MODULE_NAME:-lib_record_writer}}")


def get_script_path() -> Path:
    """Self-locating script path per Policy §4.1."""
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()
DEFAULT_STORE_PATH: Path = SCRIPT_PATH.parent / "{{DATA_FILE_PATH:-data/records.104.bejson}}"


def bejson_boundary_sanitize(data: Any) -> Any:
    """Strip boundary whitespace on dictionary keys and string values per Policy §10.9."""
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, list):
        return [bejson_boundary_sanitize(item) for item in data]
    if isinstance(data, dict):
        return {str(k).strip(): bejson_boundary_sanitize(v) for k, v in data.items()}
    return data


def bejson_get_field_map(doc: dict[str, Any]) -> dict[str, int]:
    """Compile O(1) field name to column index map per Policy §6.2."""
    fields = doc.get("Fields", [])
    field_map: dict[str, int] = {}
    for idx, field_def in enumerate(fields):
        if isinstance(field_def, dict) and "name" in field_def:
            clean_name = str(field_def["name"]).strip()
            field_map[clean_name] = idx
    return field_map


class OwningWriter104:
    """Exclusive Policy §10.4 Write-Owner for {{ENTITY_NAME:-StandardRecord}}."""

    def __init__(self, store_path: Optional[Path] = None) -> None:
        self.store_path = store_path or DEFAULT_STORE_PATH
        self._doc: Optional[dict[str, Any]] = None
        self._field_map: dict[str, int] = {}

    def load(self) -> dict[str, Any]:
        """Load and sanitize the BEJSON 104 document."""
        if not self.store_path.exists():
            LOG.error("Data store not found: %s", self.store_path)
            raise FileNotFoundError(f"Store file missing: {self.store_path}")
        with open(self.store_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._doc = bejson_boundary_sanitize(raw)
        self._field_map = bejson_get_field_map(self._doc)
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
        """Return all rows mapped to field names."""
        if self._doc is None:
            self.load()
        fmap = self._field_map
        rev_map = {idx: name for name, idx in fmap.items()}
        records: list[dict[str, Any]] = []
        for row in self._doc.get("Values", []):
            record = {rev_map[i]: row[i] for i in range(len(row)) if i in rev_map}
            records.append(record)
        return records

    def insert(self, record_data: dict[str, Any]) -> str:
        """Insert a new sanitized row into Values using field_map indices."""
        if self._doc is None:
            self.load()
        clean_input = bejson_boundary_sanitize(record_data)
        fmap = self._field_map
        row_len = len(self._doc.get("Fields", []))
        new_row: list[Any] = [None] * row_len

        # Populate ID and timestamp if absent
        id_field = "{{PREFIX:-rec}}_id"
        created_field = "{{PREFIX:-rec}}_created_at"
        record_id = clean_input.get(id_field) or str(uuid.uuid4())
        created_at = clean_input.get(created_field) or datetime.now(timezone.utc).isoformat()
        clean_input[id_field] = record_id
        clean_input[created_field] = created_at

        for col_name, col_idx in fmap.items():
            if col_name in clean_input:
                new_row[col_idx] = clean_input[col_name]

        self._doc.setdefault("Values", []).append(new_row)
        self.save()
        LOG.info("Inserted %s record: %s", "{{ENTITY_NAME:-StandardRecord}}", record_id)
        return record_id

    def get_by_id(self, record_id: str) -> Optional[dict[str, Any]]:
        """Query record by ID via field_map lookup."""
        if self._doc is None:
            self.load()
        id_field = "{{PREFIX:-rec}}_id"
        id_idx = self._field_map.get(id_field)
        if id_idx is None:
            return None
        rev_map = {idx: name for name, idx in self._field_map.items()}
        for row in self._doc.get("Values", []):
            if row[id_idx] == record_id:
                return {rev_map[i]: row[i] for i in range(len(row)) if i in rev_map}
        return None

    def update(self, record_id: str, updates: dict[str, Any]) -> bool:
        """Update fields for a specific record ID."""
        if self._doc is None:
            self.load()
        id_field = "{{PREFIX:-rec}}_id"
        id_idx = self._field_map.get(id_field)
        if id_idx is None:
            return False
        clean_updates = bejson_boundary_sanitize(updates)
        fmap = self._field_map
        updated = False
        for row in self._doc.get("Values", []):
            if row[id_idx] == record_id:
                for col_name, val in clean_updates.items():
                    if col_name in fmap:
                        row[fmap[col_name]] = val
                updated = True
                break
        if updated:
            self.save()
            LOG.info("Updated %s record: %s", "{{ENTITY_NAME:-StandardRecord}}", record_id)
        return updated

    def delete(self, record_id: str) -> bool:
        """Remove a record by ID."""
        if self._doc is None:
            self.load()
        id_field = "{{PREFIX:-rec}}_id"
        id_idx = self._field_map.get(id_field)
        if id_idx is None:
            return False
        initial_count = len(self._doc.get("Values", []))
        self._doc["Values"] = [r for r in self._doc.get("Values", []) if r[id_idx] != record_id]
        if len(self._doc["Values"]) < initial_count:
            self.save()
            LOG.info("Deleted %s record: %s", "{{ENTITY_NAME:-StandardRecord}}", record_id)
            return True
        return False
