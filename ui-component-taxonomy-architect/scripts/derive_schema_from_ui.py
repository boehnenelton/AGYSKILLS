#!/usr/bin/env python3
"""
File_Name:          derive_schema_from_ui.py
Description:        Compiles backend BEJSON schemas (104, 104a, 105, 105a) directly from abstract UI component tree maps.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional
import uuid

VERSION = "100"
RELEASE_VERSION = "300"
RELATIONAL_ID = "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("derive_schema_from_ui")


def derive_prefix(entity_name: str) -> str:
    """Derives a clean 3-5 character snake_case prefix for an entity."""
    clean = re.sub(r"[^a-zA-Z]", "", entity_name).lower()
    if len(clean) <= 4:
        return f"{clean}_"
    # Take first 4 consonants/vowels or simple truncation
    return f"{clean[:4]}_"


def parse_ui_tree(tree_text: str) -> tuple[str, str, List[Dict[str, str]]]:
    """Parses an ASCII UI component tree into entity name, host entry point, and raw control items."""
    lines = [line.strip() for line in tree_text.splitlines() if line.strip()]
    if not lines:
        LOG.error("Empty UI component tree.")
        sys.exit(10)

    # Entry point
    entry_point = "App_Admin.py"
    m_root = re.search(r"\(([^)]+)\)", lines[0])
    if m_root:
        entry_point = m_root.group(1).strip()

    # Detect primary entity name
    entity_name = "Item"
    for line in lines:
        m_sec = re.search(r"\[(?:SECTION|CARD|PANEL)\]\s+([A-Za-z0-9_\s]+)", line)
        if m_sec:
            raw_sec = m_sec.group(1).strip()
            # Remove words like Management, Panel, Manager, Directory, Form
            clean_sec = re.sub(r"\b(Management|Panel|Manager|Directory|Form|Collection|Controls)\b", "", raw_sec, flags=re.IGNORECASE).strip()
            if clean_sec:
                entity_name = clean_sec.replace(" ", "")
                break

    prefix = derive_prefix(entity_name)

    # Parse controls
    controls: List[Dict[str, str]] = []
    seen_fields: set[str] = set()

    # Always ensure primary key exists
    pk_name = f"{prefix}uuid"
    seen_fields.add(pk_name)
    controls.append({
        "name": pk_name,
        "type": "string",
        "semantic_role": "primary_key",
        "is_pk": True,
    })

    for line in lines:
        clean_line = line.strip("|+-\t ")

        # Skip headers and toolbars
        if clean_line.startswith("[") or "APPLICATION ENTRY POINT" in clean_line:
            continue
        if "Action Bar" in clean_line or "Formatting" in clean_line or "Data Table:" in clean_line or "Metric Readout:" in clean_line:
            continue
        if "Button" in clean_line and ("Save" in clean_line or "Cancel" in clean_line or "Delete" in clean_line or "Create" in clean_line):
            continue

        # Extract field intention
        target_field: Optional[str] = None
        target_type = "string"
        role = "attribute"
        fk_target: Optional[str] = None

        if "Title Input" in clean_line or "Column: Title" in clean_line or "Page Title" in clean_line:
            target_field = f"{prefix}title"
            target_type = "string"
            role = "title"
        elif "Name Input" in clean_line or "Column: Identifier" in clean_line:
            target_field = f"{prefix}name"
            target_type = "string"
            role = "name"
        elif "Textarea" in clean_line or "Content Canvas" in clean_line or "Body" in clean_line:
            target_field = f"{prefix}content_body"
            target_type = "string"
            role = "content"
        elif "Summary" in clean_line or "Excerpt" in clean_line or "Description" in clean_line:
            target_field = f"{prefix}summary"
            target_type = "string"
            role = "summary"
        elif "Dropdown Selector" in clean_line or "Picker" in clean_line:
            m_fk = re.search(r"([A-Za-z0-9_]+)\s+(?:Dropdown Selector|Picker)", clean_line)
            fk_name = m_fk.group(1).lower() if m_fk else "target"
            target_field = f"{prefix}{fk_name}_id_fk"
            target_type = "string"
            role = "foreign_key"
            fk_target = m_fk.group(1).capitalize() if m_fk else "TargetEntity"
        elif "Checkbox Toggle" in clean_line or "Status Toggle" in clean_line or "Switch" in clean_line:
            target_field = f"{prefix}is_active"
            target_type = "boolean"
            role = "flag"
        elif "Status Badge" in clean_line or "Status" in clean_line:
            target_field = f"{prefix}status"
            target_type = "string"
            role = "status"
        elif "Number Input" in clean_line or "Metric" in clean_line or "Count" in clean_line:
            target_field = f"{prefix}metric_count"
            target_type = "integer"
            role = "metric"
        elif "URL Input" in clean_line or "Link" in clean_line:
            target_field = f"{prefix}url"
            target_type = "string"
            role = "url"
        elif "Date" in clean_line or "Timestamp" in clean_line:
            target_field = f"{prefix}created_at"
            target_type = "string"
            role = "timestamp"

        if target_field and target_field not in seen_fields:
            seen_fields.add(target_field)
            item = {
                "name": target_field,
                "type": target_type,
                "semantic_role": role,
                "is_pk": False,
            }
            if fk_target:
                item["fk_target"] = fk_target
            controls.append(item)

    # Ensure timestamp exists per Policy §10.2
    ts_name = f"{prefix}created_at"
    if ts_name not in seen_fields:
        controls.append({
            "name": ts_name,
            "type": "string",
            "semantic_role": "timestamp",
            "is_pk": False,
        })

    return entity_name, entry_point, controls


def generate_schema(
    entity_name: str,
    entry_point: str,
    controls: List[Dict[str, Any]],
    target_format: str,
) -> Dict[str, Any]:
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if target_format == "104a":
        fields = [{"name": c["name"], "type": c["type"]} for c in controls if c["type"] in ("string", "integer", "number", "boolean")]
        return {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": [entity_name],
            "Fields": fields,
            "Values": [],
        }

    if target_format == "105":
        fields = [
            {
                "name": "record_uuid",
                "type": "string",
                "field_uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{entity_name}.record_uuid")),
            }
        ]
        for c in controls:
            fld_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{entity_name}.{c['name']}"))
            f_obj: Dict[str, Any] = {
                "name": c["name"],
                "type": c["type"],
                "field_uuid": fld_uuid,
            }
            if c.get("semantic_role") == "foreign_key" and "fk_target" in c:
                f_obj["fk_target_entity"] = c["fk_target"]
                f_obj["fk_on_delete"] = "cascade"
            fields.append(f_obj)

        return {
            "Format": "BEJSON",
            "Format_Version": "105",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": [entity_name],
            "Fields": fields,
            "Values": [],
        }

    if target_format == "registry":
        # Schema registry 104a format (Policy §10.1)
        fields = [
            {"name": "entity_name", "type": "string"},
            {"name": "primary_key", "type": "string"},
            {"name": "entity_prefix", "type": "string"},
            {"name": "write_owner_module", "type": "string"},
            {"name": "fields_json", "type": "string"},
            {"name": "relationships_json", "type": "string"},
        ]
        prefix = controls[0]["name"].split("_")[0] + "_"
        field_list = [{"name": c["name"], "type": c["type"]} for c in controls]
        fks = [
            {"field": c["name"], "target": c.get("fk_target", "Target"), "on_delete": "cascade"}
            for c in controls
            if c.get("semantic_role") == "foreign_key"
        ]
        values = [
            [
                entity_name,
                f"{prefix}uuid",
                prefix,
                f"src/lib/lib_{prefix.strip('_')}_writer.py",
                json.dumps(field_list),
                json.dumps(fks),
            ]
        ]
        return {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Registry_Domain": "SchemaRegistry",
            "Records_Type": ["EntitySpecification"],
            "Fields": fields,
            "Values": values,
        }

    # Default: BEJSON 104
    fields = [{"name": c["name"], "type": c["type"]} for c in controls]
    return {
        "Format": "BEJSON",
        "Format_Version": "104",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [entity_name],
        "Fields": fields,
        "Values": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="derive_schema_from_ui",
        description="Synthesizes BEJSON data taxonomies and entity schemas from UI component trees.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Register script with master index.")
    parser.add_argument("--config", action="store_true", help="Display script configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")
    parser.add_argument("component_map", nargs="?", type=Path, help="Path to ASCII component map file.")
    parser.add_argument(
        "--format",
        "-f",
        choices=["104", "104a", "105", "registry"],
        default="104",
        help="Target schema format to emit (default: 104).",
    )
    parser.add_argument("--output", "-o", type=Path, help="Optional path to output generated BEJSON document.")

    args = parser.parse_args()

    if args.register:
        LOG.info("Registered derive_schema_from_ui v%s (%s)", VERSION, RELATIONAL_ID)
        return 0

    if args.config:
        cfg = {"version": VERSION, "release_version": RELEASE_VERSION, "author": "Elton Boehnen"}
        sys.stdout.write(json.dumps(cfg, indent=2) + "\n")
        return 0

    if args.reset:
        LOG.info("Reset state complete.")
        return 0

    if not args.component_map:
        parser.print_help()
        return 10

    if not args.component_map.exists():
        LOG.error("File not found: %s", args.component_map)
        return 20

    tree_text = args.component_map.read_text(encoding="utf-8")
    entity_name, entry_point, controls = parse_ui_tree(tree_text)

    schema_doc = generate_schema(entity_name, entry_point, controls, args.format)
    formatted_json = json.dumps(schema_doc, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(formatted_json, encoding="utf-8")
        LOG.info(
            "Synthesized %s schema for '%s' to %s (%d fields).",
            args.format,
            entity_name,
            args.output,
            len(schema_doc.get("Fields", [])),
        )
    else:
        sys.stdout.write(formatted_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
