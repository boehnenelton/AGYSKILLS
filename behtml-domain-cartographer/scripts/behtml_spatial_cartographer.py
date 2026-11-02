#!/usr/bin/env python3
"""behtml_spatial_cartographer.py - Layer 6 BEHTML Spatial Discovery and Indexing Engine.

Indexes BEHTML documents, OptionSets, and spatial layout coordinate bounds into
data/behtml_spatial_registry.104a.bejson.

Author: Elton Boehnen
Standards: BEJSON 104a, Field Map Caching, Boundary Sanitization
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid
from typing import Any, Dict, List, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("behtml_spatial_cartographer")


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    clean_doc: Dict[str, Any] = {
        (k.strip() if isinstance(k, str) else k): v for k, v in raw_doc.items()
    }
    values = clean_doc.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for idx, val in enumerate(row):
                    if isinstance(val, str) and val and (val[0].isspace() or val[-1].isspace()):
                        row[idx] = val.strip()
    return clean_doc


def bejson_core_get_field_map(bejson_doc: Dict[str, Any]) -> Dict[str, int]:
    fields_list = bejson_doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}


def bejson_core_append_record(
    bejson_doc: Dict[str, Any], field_map: Dict[str, int], record_payload: Dict[str, Any]
) -> None:
    row: List[Any] = [None] * len(field_map)
    for fname, fval in record_payload.items():
        if fname not in field_map:
            raise KeyError(f"E_CORE_UNKNOWN_FIELD (21): Unknown field '{fname}'.")
        row[field_map[fname]] = fval.strip() if isinstance(fval, str) else fval
    bejson_doc["Values"].append(row)


def bejson_core_atomic_write(target_file_path: Path, bejson_doc: Dict[str, Any]) -> None:
    target_file_path = target_file_path.resolve()
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".bejson_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_file_path.parent),
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
            json.dump(bejson_doc, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(str(tmp_path), str(target_file_path))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def parse_behtml_file(file_path: Path, root_dir: Path) -> Dict[str, Any]:
    raw_bytes = file_path.read_bytes()
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode("utf-8", errors="replace")

    rel_path = str(file_path.relative_to(root_dir)) if file_path.is_relative_to(root_dir) else str(file_path)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    deterministic_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"agy.behtml.{rel_path}"))

    archetype = "Unknown"
    if "data-archetype=\"shelf\"" in text or "Shelf" in text:
        archetype = "Document_Shelf"
    elif "data-archetype=\"dashboard\"" in text or "Dashboard" in text:
        archetype = "Dashboard"
    elif "data-archetype=\"feed\"" in text or "Feed" in text:
        archetype = "Feed"
    elif "<article" in text or "document" in file_path.name.lower():
        archetype = "Document_Standard"
    else:
        archetype = "Generic_Page"

    element_count = len(re.findall(r"class=[\"'][^\"']*behtml-element[^\"']*[\"']", text))
    if element_count == 0:
        element_count = len(re.findall(r"<div|<section|<article|<card", text))

    optionset = "v1" if ("SCHEMA_OPTIONSET" in text or "optionset" in text.lower()) else "default"
    tri_color = ("#DE2626" in text or "#de2626" in text) or ("--accent:" in text)

    return {
        "spatial_entry_uuid": deterministic_uuid,
        "document_canonical_name": file_path.stem,
        "document_relative_path": rel_path,
        "archetype_kind": archetype,
        "optionset_schema_version": optionset,
        "element_record_count": element_count,
        "max_y_quantized_px": max(32, (element_count * 32)),
        "lane_span_coverage": "1..8",
        "tri_color_compliant_flag": tri_color,
        "sha256_checksum_hash": sha256_hex,
        "indexed_at_timestamp": now_iso,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="behtml_spatial_cartographer",
        description="Scans and indexes BEHTML spatial layouts and templates into BEJSON 104a.",
    )
    parser.add_argument("--scan-root", help="Root directory to search for HTML/BEHTML files.")
    parser.add_argument("--catalog", help="Target path for behtml_spatial_registry.104a.bejson.")
    parser.add_argument("--report", help="Optional target path for Markdown topology report.")
    parser.add_argument("--version", action="version", version=f"behtml_spatial_cartographer v{VERSION}")
    parser.add_argument("--config", action="store_true", help="Display configuration.")
    parser.add_argument("--register", action="store_true", help="Display registration.")

    args = parser.parse_args()
    if args.config or args.register:
        LOG.info("behtml_spatial_cartographer v%d ready.", VERSION)
        return EXIT_OK

    if not args.scan_root or not args.catalog:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    scan_dir = Path(args.scan_root).resolve()
    catalog_path = Path(args.catalog).resolve()
    if not scan_dir.is_dir():
        LOG.error("Scan root does not exist: %s", scan_dir)
        return EXIT_PATH_FAILURE

    catalog_doc: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Registry_Domain": "BEHTML_Spatial_Cartography",
        "Schema_Version": "1.0.0",
        "Records_Type": ["BEHTMLSpatialEntry"],
        "Fields": [
            {"name": "spatial_entry_uuid", "type": "string"},
            {"name": "document_canonical_name", "type": "string"},
            {"name": "document_relative_path", "type": "string"},
            {"name": "archetype_kind", "type": "string"},
            {"name": "optionset_schema_version", "type": "string"},
            {"name": "element_record_count", "type": "integer"},
            {"name": "max_y_quantized_px", "type": "integer"},
            {"name": "lane_span_coverage", "type": "string"},
            {"name": "tri_color_compliant_flag", "type": "boolean"},
            {"name": "sha256_checksum_hash", "type": "string"},
            {"name": "indexed_at_timestamp", "type": "string"},
        ],
        "Values": [],
    }
    fmap = bejson_core_get_field_map(catalog_doc)

    html_files = sorted(list(scan_dir.glob("**/*.html")) + list(scan_dir.glob("**/*.behtml")))
    for hf in html_files:
        if ".git" in hf.parts or "node_modules" in hf.parts:
            continue
        rec = parse_behtml_file(hf, scan_dir)
        bejson_core_append_record(catalog_doc, fmap, rec)

    clean_doc = bejson_core_sanitize_doc(catalog_doc)
    bejson_core_atomic_write(catalog_path, clean_doc)
    LOG.info("Wrote %d BEHTML spatial records to %s", len(clean_doc["Values"]), catalog_path)

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# BEHTML Spatial Layout & Architecture Topology Report",
            "",
            f"> **Scanned Root:** `{scan_dir}`",
            f"> **Total Layouts Indexed:** {len(clean_doc['Values'])}",
            "",
            "| Document | Archetype | Elements | Max Quantized Y | Tri-Color | Path |",
            "| :--- | :---: | :---: | :---: | :---: | :--- |",
        ]
        for row in clean_doc["Values"]:
            name = row[fmap["document_canonical_name"]]
            arch = row[fmap["archetype_kind"]]
            cnt = row[fmap["element_record_count"]]
            max_y = row[fmap["max_y_quantized_px"]]
            tc = "YES" if row[fmap["tri_color_compliant_flag"]] else "NO"
            rp = row[fmap["document_relative_path"]]
            lines.append(f"| `{name}` | `{arch}` | {cnt} | {max_y}px | `{tc}` | `{rp}` |")
        lines.extend(["", "---", "", "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev", ""])
        report_path.write_text("\n".join(lines), encoding="utf-8")
        LOG.info("Wrote spatial topology report to %s", report_path)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
