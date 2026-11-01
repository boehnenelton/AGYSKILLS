#!/data/data/com.termux/files/usr/bin/python3
"""
Name:           simple_chunker.py
Family:         Simple_Chunker
Description:    Dedicated CLI tool for non-archiving quick chunks. Serializes directory
                trees or file lists into standalone flat BEJSON 104a text containers
                (.104a.bejson.txt) and restores them without touching project archives,
                without modifying master project registries, and without chunk history tracking.
Version:        1.0.0
Date:           2026-10-30
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  7f8a1e2c-3d4b-4a5f-9e6b-8c1d2e3f4a5b
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple
import zipfile

VERSION = "1.0.0"

# ── Canonical Chunked-104a Schema Definition ─────────────────────────────────
CHUNKED_104A_FIELDS = [
    {"name": "File_Name", "type": "string"},
    {"name": "File_Extension", "type": "string"},
    {"name": "File_Content", "type": "string"},
    {"name": "File_Version", "type": "string"},
    {"name": "File_Hash", "type": "string"},
    {"name": "Relative_Path", "type": "string"},
    {"name": "Is_Binary", "type": "boolean"},
    {"name": "Is_Mounted", "type": "boolean"},
]

DEFAULT_EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".cache",
    "target",
}

DEFAULT_EXCLUDED_FILE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
    ".lock",
    ".tmp",
    ".swp",
}


def compute_bytes_sha1_hash(target_bytes_payload: bytes) -> str:
    """Computes a SHA-1 hex digest for a bytes payload per Chunked-104 standard."""
    return hashlib.sha1(target_bytes_payload).hexdigest()


def detect_file_is_binary_payload(file_system_path: Path) -> bool:
    """Detects whether a file contains raw binary null bytes or non-text content."""
    try:
        with open(file_system_path, "rb") as sample_file_descriptor:
            chunk_byte_sample = sample_file_descriptor.read(8192)
            if b"\x00" in chunk_byte_sample:
                return True
            try:
                chunk_byte_sample.decode("utf-8")
                return False
            except UnicodeDecodeError:
                return True
    except Exception:
        return True


def create_bejson_field_map_cache(bejson_document_data: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) field name to column index lookup cache."""
    fields_list = bejson_document_data.get("Fields", [])
    field_map_lookup_table: Dict[str, int] = {}
    for column_index_offset, single_field_descriptor in enumerate(fields_list):
        if isinstance(single_field_descriptor, dict) and "name" in single_field_descriptor:
            field_map_lookup_table[single_field_descriptor["name"]] = column_index_offset
    return field_map_lookup_table


def write_atomic_file_payload(destination_file_path: Path, file_text_content: str) -> None:
    """Writes a text payload to disk atomically using a temporary replacement file."""
    destination_file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_file_path = destination_file_path.with_suffix(destination_file_path.suffix + f".tmp_{os.getpid()}")
    try:
        with open(temporary_file_path, "w", encoding="utf-8") as temp_file_handle:
            temp_file_handle.write(file_text_content)
            temp_file_handle.flush()
            os.fsync(temp_file_handle.fileno())
        os.replace(temporary_file_path, destination_file_path)
    except Exception as atomic_write_exception:
        if temporary_file_path.exists():
            try:
                temporary_file_path.unlink()
            except OSError:
                pass
        raise atomic_write_exception


def generate_quick_chunk_document(
    source_target_directory: Path,
    chunk_context_instruction: Optional[str] = None,
    allowed_file_extensions: Optional[Sequence[str]] = None,
    custom_excluded_directories: Optional[Sequence[str]] = None,
    include_binary_files_flag: bool = False,
    document_version_label: str = "latest",
) -> Dict[str, Any]:
    """
    Serializes a directory into a flat BEJSON 104a Chunked document.
    Does not register or mutate any persistent archive or database index.
    """
    resolved_root_path = source_target_directory.resolve()
    if not resolved_root_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {resolved_root_path}")

    excluded_dirs_set = set(DEFAULT_EXCLUDED_DIRECTORY_NAMES)
    if custom_excluded_directories:
        excluded_dirs_set.update(custom_excluded_directories)

    normalized_allowed_extensions: Optional[set[str]] = None
    if allowed_file_extensions:
        normalized_allowed_extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in allowed_file_extensions
        }

    chunk_record_values_matrix: List[List[Any]] = []

    # Inject context note as the very first record (sorting index 0 with !- prefix)
    if chunk_context_instruction:
        context_bytes = chunk_context_instruction.encode("utf-8")
        chunk_record_values_matrix.append([
            "!-CONTEXT.txt",
            ".txt",
            chunk_context_instruction,
            document_version_label,
            compute_bytes_sha1_hash(context_bytes),
            "!-CONTEXT.txt",
            False,
            False,
        ])

    if resolved_root_path.is_file():
        # Single-file chunking mode
        is_binary_file = detect_file_is_binary_payload(resolved_root_path)
        if not is_binary_file or include_binary_files_flag:
            file_bytes_payload = resolved_root_path.read_bytes()
            if is_binary_file:
                file_content_string = base64.b64encode(file_bytes_payload).decode("ascii")
            else:
                file_content_string = resolved_root_path.read_text(encoding="utf-8", errors="replace")

            chunk_record_values_matrix.append([
                resolved_root_path.name,
                resolved_root_path.suffix,
                file_content_string,
                document_version_label,
                compute_bytes_sha1_hash(file_bytes_payload),
                resolved_root_path.name,
                is_binary_file,
                False,
            ])
    else:
        # Directory tree walk mode
        for current_walk_root, directory_names_list, file_names_list in os.walk(resolved_root_path):
            directory_names_list.sort()
            directory_names_list[:] = [
                dir_entry for dir_entry in directory_names_list if dir_entry not in excluded_dirs_set
            ]
            file_names_list.sort()

            for single_file_name in file_names_list:
                current_file_path = Path(current_walk_root) / single_file_name
                file_extension_lower = current_file_path.suffix.lower()

                if file_extension_lower in DEFAULT_EXCLUDED_FILE_EXTENSIONS:
                    continue

                if normalized_allowed_extensions and file_extension_lower not in normalized_allowed_extensions:
                    continue

                try:
                    relative_file_path_object = current_file_path.relative_to(resolved_root_path)
                    is_binary_file = detect_file_is_binary_payload(current_file_path)

                    if is_binary_file:
                        if not include_binary_files_flag:
                            continue
                        file_bytes_payload = current_file_path.read_bytes()
                        file_content_string = base64.b64encode(file_bytes_payload).decode("ascii")
                    else:
                        file_bytes_payload = current_file_path.read_bytes()
                        file_content_string = current_file_path.read_text(encoding="utf-8", errors="replace")

                    file_sha1_hash = compute_bytes_sha1_hash(file_bytes_payload)

                    chunk_record_values_matrix.append([
                        current_file_path.name,
                        current_file_path.suffix,
                        file_content_string,
                        document_version_label,
                        file_sha1_hash,
                        str(relative_file_path_object),
                        is_binary_file,
                        False,
                    ])
                except Exception as file_read_error:
                    sys.stderr.write(f"[WARNING] Skipping unreadable file {current_file_path}: {file_read_error}\n")
                    continue

    current_timestamp_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Schema_Name": "Chunked-104a",
        "Schema_Version": "1.0.1",
        "Schema_Description": "Lightweight non-archiving quick chunk container.",
        "Chunk_Date-YYYY-MM-DD": current_timestamp_iso,
        "Is_Mounted": "False",
        "Mount_Path": "",
        "Records_Type": ["Chunked"],
        "Fields": CHUNKED_104A_FIELDS,
        "Values": chunk_record_values_matrix,
    }


def execute_quick_chunk_command(
    target_path: str,
    output_path: Optional[str] = None,
    context_note: Optional[str] = None,
    patterns: Optional[str] = None,
    exclude_patterns: Optional[str] = None,
    include_binary: bool = False,
    stdout_mode: bool = False,
) -> int:
    """Executes a quick, non-archiving chunk operation."""
    target_dir = Path(target_path).resolve()
    if not target_dir.exists():
        sys.stderr.write(f"Error: Target path '{target_path}' does not exist.\n")
        return 1

    allowed_exts = [p.strip() for p in patterns.split(",") if p.strip()] if patterns else None
    excl_dirs = [p.strip() for p in exclude_patterns.split(",") if p.strip()] if exclude_patterns else None

    chunk_document = generate_quick_chunk_document(
        source_target_directory=target_dir,
        chunk_context_instruction=context_note,
        allowed_file_extensions=allowed_exts,
        custom_excluded_directories=excl_dirs,
        include_binary_files_flag=include_binary,
    )

    serialized_json_content = json.dumps(chunk_document, indent=2, ensure_ascii=False)

    if stdout_mode:
        sys.stdout.write(serialized_json_content)
        return 0

    target_name = target_dir.name or "project"
    if output_path:
        out_path = Path(output_path).resolve()
        if out_path.is_dir() or output_path.endswith(os.sep) or output_path.endswith("/"):
            out_file = out_path / f"Chunked_{target_name}.104a.bejson.txt"
        else:
            out_file = out_path
    else:
        # Default in-place/cwd non-archiving quick chunk
        out_file = Path.cwd() / f"Chunked_{target_name}.104a.bejson.txt"

    write_atomic_file_payload(out_file, serialized_json_content)

    records_count = len(chunk_document.get("Values", []))
    file_size_bytes = out_file.stat().st_size
    file_size_human = (
        f"{file_size_bytes / (1024 * 1024):.2f} MB"
        if file_size_bytes > 1024 * 1024
        else f"{file_size_bytes / 1024:.1f} KB"
    )

    print(f"[SUCCESS] Quick chunk created:")
    print(f"  Target:  {target_dir}")
    print(f"  Output:  {out_file}")
    print(f"  Files:   {records_count} records")
    print(f"  Size:    {file_size_human}")
    return 0


def execute_inspect_chunk_info(chunk_file_path: str) -> int:
    """Inspects a BEJSON chunk and prints a high-signal summary without extracting files."""
    chunk_path = Path(chunk_file_path).resolve()
    if not chunk_path.exists():
        sys.stderr.write(f"Error: Chunk file '{chunk_file_path}' does not exist.\n")
        return 1

    try:
        with open(chunk_path, "r", encoding="utf-8") as file_handle:
            chunk_doc = json.load(file_handle)
    except Exception as parse_error:
        sys.stderr.write(f"Error parsing BEJSON document: {parse_error}\n")
        return 1

    field_map = create_bejson_field_map_cache(chunk_doc)
    values = chunk_doc.get("Values", [])
    format_val = chunk_doc.get("Format", "Unknown")
    version_val = chunk_doc.get("Format_Version", "Unknown")
    schema_val = chunk_doc.get("Schema_Name", "Unknown")
    date_val = chunk_doc.get("Chunk_Date-YYYY-MM-DD", "Unknown")

    rel_idx = field_map.get("Relative_Path", 5)
    size_idx = field_map.get("File_Content", 2)
    bin_idx = field_map.get("Is_Binary", 6)

    print(f"================================================================================")
    print(f" BEJSON Quick Chunk Inspector: {chunk_path.name}")
    print(f" Format: {format_val} {version_val} | Schema: {schema_val} | Date: {date_val}")
    print(f" Total Records: {len(values)} | Chunk File Size: {chunk_path.stat().st_size / 1024:.1f} KB")
    print(f"================================================================================")

    context_note = ""
    extension_counts: Dict[str, int] = {}
    total_uncompressed_bytes = 0

    for row in values:
        if len(row) <= max(rel_idx, size_idx, bin_idx):
            continue
        rel_p = str(row[rel_idx])
        content = row[size_idx] or ""
        is_bin = bool(row[bin_idx])

        if rel_p == "!-CONTEXT.txt":
            context_note = content
            continue

        ext = Path(rel_p).suffix.lower() or "(no-ext)"
        extension_counts[ext] = extension_counts.get(ext, 0) + 1
        content_len = len(content) if not is_bin else len(base64.b64decode(content.encode("ascii"), validate=False))
        total_uncompressed_bytes += content_len

    if context_note:
        print(f"\n[INJECTED CONTEXT NOTE]")
        print(f"  {context_note.strip()}\n")

    print(f"{'Extension':<15} | {'File Count':<12}")
    print(f"{'-' * 15}-+-{'-' * 12}")
    for ext_name, ext_count in sorted(extension_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{ext_name:<15} | {ext_count:<12}")

    print(f"{'-' * 30}")
    print(f"Total Uncompressed Payload: {total_uncompressed_bytes / 1024:.1f} KB\n")

    print(f"Sample Files (first 10):")
    for display_counter, row in enumerate(values[:10], 1):
        rel_p = str(row[rel_idx]) if len(row) > rel_idx else "unknown"
        is_bin = " (binary)" if len(row) > bin_idx and row[bin_idx] else ""
        print(f"  {display_counter:2d}. {rel_p}{is_bin}")
    if len(values) > 10:
        print(f"  ... and {len(values) - 10} more files.")
    return 0


def execute_cat_file_content(chunk_file_path: str, relative_file_target: str) -> int:
    """Reads out the content of a single file from within a chunk to stdout without extracting."""
    chunk_path = Path(chunk_file_path).resolve()
    if not chunk_path.exists():
        sys.stderr.write(f"Error: Chunk file '{chunk_file_path}' does not exist.\n")
        return 1

    try:
        with open(chunk_path, "r", encoding="utf-8") as file_handle:
            chunk_doc = json.load(file_handle)
    except Exception as parse_error:
        sys.stderr.write(f"Error parsing BEJSON document: {parse_error}\n")
        return 1

    field_map = create_bejson_field_map_cache(chunk_doc)
    values = chunk_doc.get("Values", [])
    rel_idx = field_map.get("Relative_Path", 5)
    content_idx = field_map.get("File_Content", 2)
    bin_idx = field_map.get("Is_Binary", 6)

    normalized_target = relative_file_target.strip().lstrip("./")

    for row in values:
        if len(row) > max(rel_idx, content_idx):
            current_rel = str(row[rel_idx]).lstrip("./")
            if current_rel == normalized_target or Path(current_rel).name == normalized_target:
                is_bin = bool(row[bin_idx]) if len(row) > bin_idx else False
                content = str(row[content_idx])
                if is_bin:
                    sys.stdout.buffer.write(base64.b64decode(content.encode("ascii")))
                else:
                    sys.stdout.write(content)
                    if not content.endswith("\n"):
                        sys.stdout.write("\n")
                return 0

    sys.stderr.write(f"Error: File '{relative_file_target}' not found in chunk '{chunk_path.name}'.\n")
    return 1


def execute_unchunk_command(
    chunk_file_path: str,
    output_destination: Optional[str] = None,
    zip_output_flag: bool = False,
) -> int:
    """Restores files from a BEJSON chunk back into loose files or a zip archive."""
    chunk_path = Path(chunk_file_path).resolve()
    if not chunk_path.exists():
        sys.stderr.write(f"Error: Chunk file '{chunk_file_path}' does not exist.\n")
        return 1

    try:
        with open(chunk_path, "r", encoding="utf-8") as file_handle:
            chunk_doc = json.load(file_handle)
    except Exception as parse_error:
        sys.stderr.write(f"Error parsing BEJSON document: {parse_error}\n")
        return 1

    field_map = create_bejson_field_map_cache(chunk_doc)
    values = chunk_doc.get("Values", [])

    rel_idx = field_map.get("Relative_Path", 5)
    content_idx = field_map.get("File_Content", 2)
    bin_idx = field_map.get("Is_Binary", 6)

    chunk_stem_name = chunk_path.stem
    if chunk_stem_name.endswith(".104a.bejson"):
        chunk_stem_name = chunk_stem_name[:-12]
    elif chunk_stem_name.endswith(".bejson"):
        chunk_stem_name = chunk_stem_name[:-7]
    if chunk_stem_name.startswith("Chunked_"):
        chunk_stem_name = chunk_stem_name[8:]

    if output_destination:
        out_root = Path(output_destination).resolve()
    else:
        out_root = Path.cwd() / f"restored_{chunk_stem_name}"

    out_root.mkdir(parents=True, exist_ok=True)
    extracted_counter = 0

    for row in values:
        if len(row) <= max(rel_idx, content_idx):
            continue
        rel_p = str(row[rel_idx])
        if not rel_p or rel_p.startswith("/"):
            rel_p = rel_p.lstrip("/")

        target_file_path = out_root / rel_p
        target_file_path.parent.mkdir(parents=True, exist_ok=True)

        is_bin = bool(row[bin_idx]) if len(row) > bin_idx else False
        content = row[content_idx] or ""

        try:
            if is_bin:
                target_file_path.write_bytes(base64.b64decode(content.encode("ascii")))
            else:
                target_file_path.write_text(str(content), encoding="utf-8")
            extracted_counter += 1
        except Exception as write_err:
            sys.stderr.write(f"[WARNING] Could not write {target_file_path}: {write_err}\n")

    if zip_output_flag:
        zip_target_file = out_root.with_suffix(".zip")
        with zipfile.ZipFile(zip_target_file, "w", zipfile.ZIP_DEFLATED) as zip_archive:
            for root, _, files in os.walk(out_root):
                for f in files:
                    full_p = Path(root) / f
                    zip_archive.write(full_p, full_p.relative_to(out_root))
        shutil.rmtree(out_root)
        print(f"[SUCCESS] Unchunked {extracted_counter} files directly to ZIP archive:")
        print(f"  Archive: {zip_target_file}")
    else:
        print(f"[SUCCESS] Unchunked {extracted_counter} files:")
        print(f"  Location: {out_root}")

    return 0


def build_command_line_argument_parser() -> argparse.ArgumentParser:
    """Builds the CLI options parser."""
    parser = argparse.ArgumentParser(
        prog="simple_chunker.py",
        description="Simple_Chunker: Fast, Non-Archiving Single-File BEJSON Project Chunker & Restorer.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--chunk", "-c",
        metavar="TARGET_PATH",
        help="Chunk a directory or file into a flat BEJSON 104a text container (.104a.bejson.txt).",
    )
    group.add_argument(
        "--unchunk", "-u",
        metavar="CHUNK_FILE",
        help="Unchunk/extract files from a BEJSON chunk file back to disk.",
    )
    group.add_argument(
        "--info", "-i",
        metavar="CHUNK_FILE",
        help="Inspect a BEJSON chunk (lists file types, count, size, and context) without unchunking.",
    )
    group.add_argument(
        "--cat",
        nargs=2,
        metavar=("CHUNK_FILE", "FILE_PATH"),
        help="Output the raw content of a specific file inside the chunk to stdout.",
    )

    parser.add_argument(
        "--output", "--dest", "-o",
        dest="output",
        help="Destination path for output chunk file or unchunk directory. Defaults to CWD.",
    )
    parser.add_argument(
        "--context",
        help="Context note to embed as '!-CONTEXT.txt' (the very first record in the chunk) without modifying disk.",
    )
    parser.add_argument(
        "--patterns",
        help="Comma-separated file extensions to include (e.g. '.py,.json,.md'). Defaults to all text files.",
    )
    parser.add_argument(
        "--exclude-patterns",
        help="Comma-separated directory names to exclude (e.g. '.git,node_modules,build').",
    )
    parser.add_argument(
        "--include-binary",
        action="store_true",
        help="Include binary files as Base64-encoded records (default: False, binaries skipped).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Emit BEJSON chunk text directly to standard output (useful for piping into LLMs or tools).",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="When unchunking, compress the restored folder directly into a .zip archive.",
    )

    return parser


def main() -> int:
    parser = build_command_line_argument_parser()
    args = parser.parse_args()

    if args.chunk:
        return execute_quick_chunk_command(
            target_path=args.chunk,
            output_path=args.output,
            context_note=args.context,
            patterns=args.patterns,
            exclude_patterns=args.exclude_patterns,
            include_binary=args.include_binary,
            stdout_mode=args.stdout,
        )
    elif args.unchunk:
        return execute_unchunk_command(
            chunk_file_path=args.unchunk,
            output_destination=args.output,
            zip_output_flag=args.zip,
        )
    elif args.info:
        return execute_inspect_chunk_info(chunk_file_path=args.info)
    elif args.cat:
        chunk_file, target_file = args.cat
        return execute_cat_file_content(chunk_file_path=chunk_file, relative_file_target=target_file)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
