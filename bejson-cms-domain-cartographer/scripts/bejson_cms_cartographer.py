#!/usr/bin/env python3
"""bejson_cms_cartographer.py - Layer 6 BEJSON CMS Platform Discovery Engine.

Indexes CMS microservices, route blueprints, and data stores into
data/cms_service_map.104a.bejson.

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
LOG = logging.getLogger("bejson_cms_cartographer")


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


def parse_cms_service_file(service_path: Path, root_dir: Path) -> Dict[str, Any]:
    raw_bytes = service_path.read_bytes()
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode("utf-8", errors="replace")

    rel_path = str(service_path.relative_to(root_dir)) if service_path.is_relative_to(root_dir) else str(service_path)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    deterministic_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"agy.cms.{rel_path}"))

    flavor = "Standalone_BEJSON_CMS" if "BEJSON_CMS" in str(service_path) else "NewAgent_Integrated_CMS"
    route_matches = re.findall(r"@(?:[a-zA-Z0-9_]+)\.route\s*\(\s*['\"]([^'\"]+)['\"]", text)
    route_count = len(route_matches)

    stores = set()
    for m in re.findall(r"['\"]([a-zA-Z0-9_-]+\.bejson)['\"]", text):
        stores.add(m)
    stores_csv = ",".join(sorted(stores)) if stores else "pages_db.bejson"
    static_export = "export" in text.lower() or "publish" in text.lower()

    return {
        "service_entry_uuid": deterministic_uuid,
        "service_canonical_name": service_path.stem,
        "service_relative_path": rel_path,
        "cms_distribution_flavor": flavor,
        "http_routes_count": route_count,
        "underlying_stores_csv": stores_csv,
        "static_export_supported": static_export,
        "source_sha256_hash": sha256_hex,
        "indexed_at_timestamp": now_iso,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bejson_cms_cartographer",
        description="Scans and indexes BEJSON CMS microservices, routes, and stores into BEJSON 104a.",
    )
    parser.add_argument("--scan-root", help="Root directory to search for CMS service files.")
    parser.add_argument("--catalog", help="Target path for cms_service_map.104a.bejson.")
    parser.add_argument("--report", help="Optional target path for Markdown CMS topology report.")
    parser.add_argument("--version", action="version", version=f"bejson_cms_cartographer v{VERSION}")
    parser.add_argument("--config", action="store_true", help="Display configuration.")
    parser.add_argument("--register", action="store_true", help="Display registration.")

    args = parser.parse_args()
    if args.config or args.register:
        LOG.info("bejson_cms_cartographer v%d ready.", VERSION)
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
        "Registry_Domain": "BEJSON_CMS_Service_Cartography",
        "Schema_Version": "1.0.0",
        "Records_Type": ["CMSServiceEntry"],
        "Fields": [
            {"name": "service_entry_uuid", "type": "string"},
            {"name": "service_canonical_name", "type": "string"},
            {"name": "service_relative_path", "type": "string"},
            {"name": "cms_distribution_flavor", "type": "string"},
            {"name": "http_routes_count", "type": "integer"},
            {"name": "underlying_stores_csv", "type": "string"},
            {"name": "static_export_supported", "type": "boolean"},
            {"name": "source_sha256_hash", "type": "string"},
            {"name": "indexed_at_timestamp", "type": "string"},
        ],
        "Values": [],
    }
    fmap = bejson_core_get_field_map(catalog_doc)

    py_files = sorted(set(
        list(scan_dir.glob("**/routes*.py"))
        + list(scan_dir.glob("**/app*.py"))
        + list(scan_dir.glob("**/server*.py"))
        + list(scan_dir.glob("**/src/web/*.py"))
        + list(scan_dir.glob("**/BEJSON_CMS*.py"))
    ))
    for pf in py_files:
        if ".git" in pf.parts or "venv" in pf.parts or "__pycache__" in pf.parts:
            continue
        if "cms" in str(pf).lower() or "na-cms" in str(pf).lower():
            rec = parse_cms_service_file(pf, scan_dir)
            bejson_core_append_record(catalog_doc, fmap, rec)

    clean_doc = bejson_core_sanitize_doc(catalog_doc)
    bejson_core_atomic_write(catalog_path, clean_doc)
    LOG.info("Wrote %d CMS service records to %s", len(clean_doc["Values"]), catalog_path)

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# BEJSON CMS Microservices & Architecture Topology Report",
            "",
            f"> **Scanned Root:** `{scan_dir}`",
            f"> **Total Services Indexed:** {len(clean_doc['Values'])}",
            "",
            "| Service | Flavor | Routes | Underlying Stores | Static Export | Path |",
            "| :--- | :---: | :---: | :--- | :---: | :--- |",
        ]
        for row in clean_doc["Values"]:
            name = row[fmap["service_canonical_name"]]
            flavor = row[fmap["cms_distribution_flavor"]]
            rcnt = row[fmap["http_routes_count"]]
            stores = row[fmap["underlying_stores_csv"]]
            sexp = "YES" if row[fmap["static_export_supported"]] else "NO"
            rp = row[fmap["service_relative_path"]]
            lines.append(f"| `{name}` | `{flavor}` | {rcnt} | `{stores}` | `{sexp}` | `{rp}` |")
        lines.extend(["", "---", "", "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev", ""])
        report_path.write_text("\n".join(lines), encoding="utf-8")
        LOG.info("Wrote CMS topology report to %s", report_path)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
