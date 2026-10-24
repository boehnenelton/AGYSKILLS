#!/usr/bin/env python3
"""
Name:           cms_database_chunker
File:           cms_database_chunker.py
Description:    Custom skill-specific variant of Simple Chunker engineered for BEJSON CMS.
                Specialized for full database staging, single-file Chunked-104a snapshotting,
                and atomic database restoration with SHA-256 verification.
Version:        100
Date Created:   2026-10-21
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("cms_database_chunker requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import json
import logging
import hashlib
import tempfile
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("cms_database_chunker")


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


def get_default_cms_root() -> Path:
    env_root = os.environ.get("CMS_DATA_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root)
    # Default to standard development repo storage location
    default_dev_storage = Path("/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/storage")
    if default_dev_storage.exists():
        return default_dev_storage
    return Path.cwd() / "storage"


def get_default_chunks_dir() -> Path:
    default_dir = Path("/storage/emulated/0/Admin/Resources/Chunks")
    if default_dir.exists():
        return default_dir
    fallback = Path.home() / "Chunks"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


CHUNKED_104_FIELDS: List[Dict[str, str]] = [
    {"name": "File_Name", "type": "string"},
    {"name": "File_Extension", "type": "string"},
    {"name": "File_Content", "type": "string"},
    {"name": "File_Version", "type": "string"},
    {"name": "File_Hash", "type": "string"},
    {"name": "Relative_Path", "type": "string"},
    {"name": "Is_Binary", "type": "boolean"},
    {"name": "Is_Mounted", "type": "boolean"},
]


def bejson_core_get_field_map(doc: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) lookup dictionary mapping field_name -> 0-based column index."""
    fields_list = doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}


def compute_sha256(data_bytes: bytes) -> str:
    return hashlib.sha256(data_bytes).hexdigest()


def atomic_write_json(target_path: Path, doc_data: Dict[str, Any]) -> None:
    target_path = target_path.resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".chunk_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_path.parent),
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out_file:
            json.dump(doc_data, out_file, indent=2, ensure_ascii=False)
            out_file.write("\n")
            out_file.flush()
            os.fsync(out_file.fileno())
        os.replace(str(tmp_path), str(target_path))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def is_binary_file(filepath: Path) -> bool:
    known_binary_exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pdf", ".zip", ".pyc"}
    if filepath.suffix.lower() in known_binary_exts:
        return True
    try:
        sample = filepath.open("rb").read(1024)
        return b"\x00" in sample
    except Exception:
        return True


def create_database_snapshot(
    mfdb_root: Path,
    output_chunk_path: Optional[Path] = None,
    context_note: str = "BEJSON CMS Full Database Stage and Snapshot",
    include_binary: bool = False,
    site_master_only: bool = False,
) -> Tuple[int, str]:
    target_scan_dir = mfdb_root / "site_master" if site_master_only else mfdb_root
    if not target_scan_dir.exists() or not target_scan_dir.is_dir():
        LOG.error("Target scan directory not found: %s", target_scan_dir)
        return EXIT_PATH_FAILURE, ""

    manifest_file = mfdb_root / "site_master" / "104a.mfdb.bejson"
    if not manifest_file.exists():
        LOG.error("Central manifest not found at: %s", manifest_file)
        return EXIT_SCHEMA_FAILURE, ""

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_stamp = now_iso[:10]
    time_stamp_compact = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    if output_chunk_path is None:
        chunks_dir = get_default_chunks_dir()
        prefix = "Chunked_BEJSON_CMS_SiteMaster" if site_master_only else "Chunked_BEJSON_CMS_DB"
        output_chunk_path = chunks_dir / f"{prefix}_{time_stamp_compact}.104a.bejson.txt"

    LOG.info("Staging database files from: %s", target_scan_dir)
    values: List[List[Any]] = []

    # Gather database files (.bejson, .json, .txt)
    import base64
    for root, dirs, files in os.walk(target_scan_dir):
        dirs.sort()
        # Exclude temp and lock directories
        dirs[:] = [d for d in dirs if not d.endswith(".lock") and d != "tmp"]
        files.sort()
        for fname in files:
            if fname.endswith(".tmp") or fname.endswith(".lock"):
                continue
            file_path = Path(root) / fname
            rel_path = file_path.relative_to(mfdb_root)
            try:
                raw_bytes = file_path.read_bytes()
                sha256_hash = compute_sha256(raw_bytes)
                is_bin = is_binary_file(file_path)

                if is_bin:
                    if not include_binary:
                        continue
                    content = base64.b64encode(raw_bytes).decode("ascii")
                else:
                    content = file_path.read_text(encoding="utf-8")

                values.append(
                    [
                        file_path.name,
                        file_path.suffix,
                        content,
                        "100",
                        sha256_hash,
                        str(rel_path),
                        is_bin,
                        False,
                    ]
                )
            except Exception as read_exc:
                LOG.warning("Could not stage file %s: %s", rel_path, read_exc)

    chunked_doc: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Schema_Name": "Chunked-104a",
        "Schema_Version": "1.0.1",
        "Schema_Description": "BEJSON CMS Full Database Stage and Snapshot Archive.",
        "Chunk_Date-YYYY-MM-DD": date_stamp,
        "Snapshot_Timestamp": now_iso,
        "Context_Note": context_note,
        "Source_MFDB_Path": str(mfdb_root),
        "Is_Mounted": "False",
        "Mount_Path": "",
        "Records_Type": ["Chunked"],
        "Fields": CHUNKED_104_FIELDS,
        "Values": values,
    }

    try:
        atomic_write_json(output_chunk_path, chunked_doc)
        LOG.info(
            "Snapshot successfully written to: %s (%d files staged)",
            output_chunk_path,
            len(values),
        )
        return EXIT_OK, str(output_chunk_path)
    except Exception as write_exc:
        LOG.error("Failed to write snapshot archive: %s", write_exc)
        return EXIT_ENV_FAILURE, ""


def restore_database_snapshot(
    chunk_file_path: Path,
    target_restore_dir: Path,
) -> int:
    if not chunk_file_path.exists():
        LOG.error("Snapshot archive not found: %s", chunk_file_path)
        return EXIT_PATH_FAILURE

    try:
        doc = json.loads(chunk_file_path.read_text(encoding="utf-8"))
    except Exception as exc:
        LOG.error("Failed to parse snapshot JSON: %s", exc)
        return EXIT_SCHEMA_FAILURE

    if doc.get("Format") != "BEJSON" or doc.get("Format_Version") != "104a":
        LOG.error("File is not a valid BEJSON 104a archive.")
        return EXIT_SCHEMA_FAILURE

    field_map = bejson_core_get_field_map(doc)
    required_cols = ("File_Name", "File_Content", "File_Hash", "Relative_Path")
    for rcol in required_cols:
        if rcol not in field_map:
            LOG.error("Snapshot is missing required schema column: %s", rcol)
            return EXIT_SCHEMA_FAILURE

    rows = doc.get("Values", [])
    LOG.info("Restoring %d database records to: %s", len(rows), target_restore_dir)
    target_restore_dir.mkdir(parents=True, exist_ok=True)

    rel_idx = field_map["Relative_Path"]
    content_idx = field_map["File_Content"]
    hash_idx = field_map["File_Hash"]

    restored_count = 0
    for row in rows:
        rel_str = row[rel_idx]
        content_str = row[content_idx]
        expected_hash = row[hash_idx]

        dest_file = target_restore_dir / rel_str
        # Verify directory safety
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        content_bytes = content_str.encode("utf-8")
        actual_hash = compute_sha256(content_bytes)
        if actual_hash != expected_hash:
            LOG.error("SHA-256 hash mismatch on %s! Corrupted snapshot.", rel_str)
            return EXIT_SCHEMA_FAILURE

        dest_file.write_bytes(content_bytes)
        restored_count += 1

    LOG.info("Successfully restored %d database files.", restored_count)
    return EXIT_OK


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cms_database_chunker",
        description="Custom skill-specific variant of Simple Chunker for BEJSON CMS database staging.",
    )
    parser.add_argument(
        "--stage",
        action="store_true",
        help="Stage and snapshot the live CMS MFDB database into a Chunked-104a flat file.",
    )
    parser.add_argument(
        "--restore",
        type=str,
        help="Path to a .104a.bejson.txt snapshot archive to restore.",
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Destination path for the snapshot file (on stage) or target directory (on restore).",
    )
    parser.add_argument(
        "--context",
        type=str,
        default="BEJSON CMS Full Database Stage and Snapshot",
        help="Descriptive context note to embed in the snapshot header.",
    )
    parser.add_argument(
        "--site-master",
        action="store_true",
        help="Stage and snapshot only the site_master directory (manifest and 10 entity tables).",
    )
    parser.add_argument(
        "--include-binary",
        action="store_true",
        help="Include and base64-encode binary assets (PNG, WebP, PDF) in the snapshot.",
    )

    args = parser.parse_args()

    cms_storage = get_default_cms_root()
    mfdb_dir = cms_storage / "mfdb"

    if args.restore:
        chunk_path = Path(args.restore).resolve()
        restore_target = Path(args.dest).resolve() if args.dest else mfdb_dir
        exit_code = restore_database_snapshot(chunk_path, restore_target)
        sys.exit(exit_code)

    # Default to staging database snapshot
    dest_path = Path(args.dest).resolve() if args.dest else None
    exit_code, out_file = create_database_snapshot(
        mfdb_dir,
        dest_path,
        args.context,
        include_binary=args.include_binary,
        site_master_only=args.site_master,
    )
    if exit_code == EXIT_OK:
        LOG.info("Database staging completed successfully: %s", out_file)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
