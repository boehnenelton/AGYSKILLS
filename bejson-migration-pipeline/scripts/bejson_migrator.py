#!/usr/bin/env python3
"""
File:          bejson_migrator.py
Description:   Layer 3 BEJSON & MFDB Automated Ingestion Pipeline.
               Converts legacy SQLite databases, CSV spreadsheets, and raw JSON arrays
               into Foundational Era BEJSON 104a or Integrity Era Format 105a documents
               with automated type inference, boundary sanitization, and atomic writes.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("bejson_migrator requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [migrator]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("bejson_migrator")


def infer_primitive_type(values: List[Any]) -> str:
    """Infers canonical BEJSON type: integer, number, boolean, or string."""
    non_nulls = [v for v in values if v is not None and str(v).strip() != ""]
    if not non_nulls:
        return "string"

    # Check boolean
    is_bool = True
    for v in non_nulls:
        if isinstance(v, bool):
            continue
        if str(v).strip().lower() not in {"true", "false", "0", "1"}:
            is_bool = False
            break
    if is_bool:
        return "boolean"

    # Check integer
    is_int = True
    for v in non_nulls:
        s = str(v).strip()
        if not (s.isdigit() or (s.startswith("-") and s[1:].isdigit())):
            is_int = False
            break
    if is_int:
        return "integer"

    # Check number / float
    is_num = True
    for v in non_nulls:
        try:
            float(str(v).strip())
        except ValueError:
            is_num = False
            break
    if is_num:
        return "number"

    return "string"


def cast_value(val: Any, target_type: str) -> Any:
    """Casts raw cell value to matched BEJSON schema type with whitespace sanitization."""
    if val is None:
        return None
    if isinstance(val, str):
        val = val.strip()
        if val == "":
            return None

    try:
        if target_type == "integer":
            return int(val)
        elif target_type == "number":
            return float(val)
        elif target_type == "boolean":
            s = str(val).lower()
            return s in {"true", "1"}
        return str(val)
    except Exception:
        return str(val)


def migrate_csv(
    csv_path: Path,
    record_type: str = "ImportedRecord",
    format_version: str = "104a"
) -> Dict[str, Any]:
    """Migrates a CSV file to BEJSON document structure."""
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        headers = [h.strip() for h in next(reader, [])]
        raw_rows = [[cell.strip() if isinstance(cell, str) else cell for cell in row] for row in reader]

    fields = []
    for col_idx, col_name in enumerate(headers):
        col_samples = [row[col_idx] for row in raw_rows if col_idx < len(row)]
        inferred = infer_primitive_type(col_samples)
        f_entry: Dict[str, Any] = {"name": col_name, "type": inferred}
        if format_version == "105a":
            f_entry["field_uuid"] = str(uuid.uuid4())
        fields.append(f_entry)

    field_map = {f["name"]: idx for idx, f in enumerate(fields)}
    values = []
    for row in raw_rows:
        casted_row = []
        for col_idx, col_name in enumerate(headers):
            val = row[col_idx] if col_idx < len(row) else None
            casted_row.append(cast_value(val, fields[col_idx]["type"]))
        if format_version == "105a":
            casted_row.insert(0, str(uuid.uuid4()))
        values.append(casted_row)

    if format_version == "105a":
        fields.insert(0, {"name": "record_uuid", "type": "string", "field_uuid": str(uuid.uuid4())})

    return {
        "Format": "BEJSON",
        "Format_Version": format_version,
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [record_type],
        "Fields": fields,
        "Values": values
    }


def migrate_sqlite_table(
    db_path: Path,
    table_name: str,
    format_version: str = "104a"
) -> Dict[str, Any]:
    """Extracts a table from SQLite database and formats to BEJSON."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    col_info = cursor.fetchall()
    headers = [c[1].strip() for c in col_info]

    cursor.execute(f"SELECT * FROM {table_name}")
    raw_rows = cursor.fetchall()
    conn.close()

    fields = []
    for col_idx, col_name in enumerate(headers):
        col_samples = [r[col_idx] for r in raw_rows]
        inferred = infer_primitive_type(col_samples)
        f_entry = {"name": col_name, "type": inferred}
        if format_version == "105a":
            f_entry["field_uuid"] = str(uuid.uuid4())
        fields.append(f_entry)

    values = []
    for row in raw_rows:
        casted_row = [cast_value(row[i], fields[i]["type"]) for i in range(len(headers))]
        if format_version == "105a":
            casted_row.insert(0, str(uuid.uuid4()))
        values.append(casted_row)

    if format_version == "105a":
        fields.insert(0, {"name": "record_uuid", "type": "string", "field_uuid": str(uuid.uuid4())})

    return {
        "Format": "BEJSON",
        "Format_Version": format_version,
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [f"{table_name.capitalize()}Record"],
        "Fields": fields,
        "Values": values
    }


def write_bejson_atomic(target_path: Path, doc: Dict[str, Any]) -> None:
    """Writes document to temporary file and executes atomic POSIX replace."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.parent / f"{target_path.name}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    os.replace(tmp_path, target_path)
    logger.info(f"Committed atomic write: {target_path} ({len(doc.get('Values', []))} records)")


def update_migration_manifest(
    manifest_path: Path,
    record: Dict[str, Any]
) -> None:
    """Updates the migration tracking manifest."""
    manifest_data: Dict[str, Any] = {"Values": []}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception:
            manifest_data = {"Values": []}

    fields = manifest_data.get("Fields", [
        {"name": "migration_id", "type": "string"},
        {"name": "source_format", "type": "string"},
        {"name": "source_path", "type": "string"},
        {"name": "target_format", "type": "string"},
        {"name": "target_path", "type": "string"},
        {"name": "rows_migrated", "type": "integer"},
        {"name": "columns_count", "type": "integer"},
        {"name": "status", "type": "string"},
        {"name": "sha256_hash", "type": "string"},
        {"name": "migration_timestamp", "type": "string"}
    ])
    manifest_data["Fields"] = fields

    field_map = {f["name"]: idx for idx, f in enumerate(fields)}
    row = [None] * len(fields)
    for k, v in record.items():
        if k in field_map:
            row[field_map[k]] = v

    manifest_data.setdefault("Values", []).append(row)
    manifest_data["Format"] = "BEJSON"
    manifest_data["Format_Version"] = "104a"
    manifest_data["Format_Creator"] = "Elton Boehnen"
    manifest_data["Records_Type"] = ["MigrationRecord"]

    tmp_path = manifest_path.parent / f"{manifest_path.name}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.replace(tmp_path, manifest_path)
    logger.info(f"Updated migration registry: {manifest_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BEJSON & MFDB Automated Ingestion Pipeline"
    )
    parser.add_argument("source", type=Path, help="Source database file (.db) or CSV spreadsheet (.csv)")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Destination BEJSON filepath")
    parser.add_argument("--format-version", choices=["104a", "105a"], default="104a", help="Target BEJSON dialect (default: 104a)")
    parser.add_argument("--table", type=str, default=None, help="Table name (required when source is SQLite database)")
    parser.add_argument("--record-type", type=str, default="ImportedRecord", help="Records_Type descriptor")
    parser.add_argument("--manifest", type=Path, default=None, help="Optional BEJSON 104a manifest path to log migration")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.source.exists():
        logger.error(f"Source file not found: {args.source}")
        sys.exit(1)

    ext = args.source.suffix.lower()
    if ext in {".db", ".sqlite", ".sqlite3"}:
        if not args.table:
            logger.error("SQLite migration requires --table <table_name>")
            sys.exit(1)
        doc = migrate_sqlite_table(args.source, args.table, args.format_version)
        src_fmt = "sqlite"
    elif ext in {".csv", ".tsv"}:
        doc = migrate_csv(args.source, args.record_type, args.format_version)
        src_fmt = "csv"
    else:
        logger.error(f"Unsupported source format: {ext}. Supported: .csv, .db, .sqlite")
        sys.exit(1)

    write_bejson_atomic(args.output, doc)

    # Compute sha256
    hasher = hashlib.sha256()
    with open(args.output, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    sha_str = hasher.hexdigest()

    if args.manifest:
        update_migration_manifest(
            manifest_path=args.manifest,
            record={
                "migration_id": f"mig_{int(datetime.now(timezone.utc).timestamp())}",
                "source_format": src_fmt,
                "source_path": str(args.source),
                "target_format": args.format_version,
                "target_path": str(args.output),
                "rows_migrated": len(doc.get("Values", [])),
                "columns_count": len(doc.get("Fields", [])),
                "status": "SUCCESS",
                "sha256_hash": sha_str,
                "migration_timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
    logger.info("Migration completed successfully.")


if __name__ == "__main__":
    main()
