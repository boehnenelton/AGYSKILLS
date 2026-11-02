#!/usr/bin/env python3
"""mfdb_topology_cartographer.py - Layer 6 MFDB Cluster Discovery and Topology Engine.

Indexes MFDB database manifests, parent-child linkages, and entity distributions into
data/mfdb_topology_registry.104a.bejson.

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
LOG = logging.getLogger("mfdb_topology_cartographer")


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


def parse_manifest_file(manifest_path: Path, root_dir: Path) -> Dict[str, Any]:
    raw_bytes = manifest_path.read_bytes()
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    try:
        data = json.loads(raw_bytes.decode("utf-8"))
    except Exception:
        data = {}

    rel_path = str(manifest_path.relative_to(root_dir)) if manifest_path.is_relative_to(root_dir) else str(manifest_path)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    deterministic_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"agy.mfdb.{rel_path}"))

    db_name = data.get("Database_Name") or data.get("Project_Name") or manifest_path.parent.name
    fmt_ver = str(data.get("Format_Version", "104a"))
    era = "v1.40_Integrity_105" if "105" in fmt_ver or "105" in manifest_path.name else "v1.31_Foundational_104"
    role = data.get("Network_Role", "Master")
    entities = data.get("Entities", [])
    entity_count = len(entities) if isinstance(entities, list) else 0

    return {
        "cluster_entry_uuid": deterministic_uuid,
        "database_name": str(db_name),
        "manifest_relative_path": rel_path,
        "database_era_format": era,
        "database_network_role": str(role),
        "registered_entities_count": entity_count,
        "foreign_key_links_count": 0,
        "parent_hierarchy_resolved": bool(data.get("Parent_Hierarchy") or role == "Master"),
        "manifest_sha256_hash": sha256_hex,
        "indexed_at_timestamp": now_iso,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="mfdb_topology_cartographer",
        description="Scans and indexes MFDB database clusters and manifests into BEJSON 104a.",
    )
    parser.add_argument("--scan-root", help="Root directory to search for MFDB manifests.")
    parser.add_argument("--catalog", help="Target path for mfdb_topology_registry.104a.bejson.")
    parser.add_argument("--report", help="Optional target path for Markdown cluster topology report.")
    parser.add_argument("--version", action="version", version=f"mfdb_topology_cartographer v{VERSION}")
    parser.add_argument("--config", action="store_true", help="Display configuration.")
    parser.add_argument("--register", action="store_true", help="Display registration.")

    args = parser.parse_args()
    if args.config or args.register:
        LOG.info("mfdb_topology_cartographer v%d ready.", VERSION)
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
        "Registry_Domain": "MFDB_Topology_Cartography",
        "Schema_Version": "1.0.0",
        "Records_Type": ["MFDBTopologyEntry"],
        "Fields": [
            {"name": "cluster_entry_uuid", "type": "string"},
            {"name": "database_name", "type": "string"},
            {"name": "manifest_relative_path", "type": "string"},
            {"name": "database_era_format", "type": "string"},
            {"name": "database_network_role", "type": "string"},
            {"name": "registered_entities_count", "type": "integer"},
            {"name": "foreign_key_links_count", "type": "integer"},
            {"name": "parent_hierarchy_resolved", "type": "boolean"},
            {"name": "manifest_sha256_hash", "type": "string"},
            {"name": "indexed_at_timestamp", "type": "string"},
        ],
        "Values": [],
    }
    fmap = bejson_core_get_field_map(catalog_doc)

    manifest_files = sorted(
        list(scan_dir.glob("**/*.mfdb.bejson")) + list(scan_dir.glob("**/mfdb_manifest.json"))
    )
    for mf in manifest_files:
        if ".git" in mf.parts or "node_modules" in mf.parts:
            continue
        rec = parse_manifest_file(mf, scan_dir)
        bejson_core_append_record(catalog_doc, fmap, rec)

    clean_doc = bejson_core_sanitize_doc(catalog_doc)
    bejson_core_atomic_write(catalog_path, clean_doc)
    LOG.info("Wrote %d MFDB topology records to %s", len(clean_doc["Values"]), catalog_path)

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# MFDB Federated Database Topology Report",
            "",
            f"> **Scanned Root:** `{scan_dir}`",
            f"> **Total Clusters Indexed:** {len(clean_doc['Values'])}",
            "",
            "| Database | Era | Role | Entities | Parent Resolved | Path |",
            "| :--- | :---: | :---: | :---: | :---: | :--- |",
        ]
        for row in clean_doc["Values"]:
            name = row[fmap["database_name"]]
            era = row[fmap["database_era_format"]]
            role = row[fmap["database_network_role"]]
            ents = row[fmap["registered_entities_count"]]
            pres = "YES" if row[fmap["parent_hierarchy_resolved"]] else "NO"
            rp = row[fmap["manifest_relative_path"]]
            lines.append(f"| `{name}` | `{era}` | `{role}` | {ents} | `{pres}` | `{rp}` |")
        lines.extend(["", "---", "", "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev", ""])
        report_path.write_text("\n".join(lines), encoding="utf-8")
        LOG.info("Wrote cluster topology report to %s", report_path)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
