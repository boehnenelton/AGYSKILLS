#!/usr/bin/env python3
"""
File_Name:          project_schema_to_ui.py
Description:        Synthesizes database-agnostic ASCII UI Component tree maps directly from backend BEJSON schemas.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      7a1e94bc-2f3d-4c8a-b9e1-6d0f8a5c2b3e
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

VERSION = "100"
RELEASE_VERSION = "300"
RELATIONAL_ID = "7a1e94bc-2f3d-4c8a-b9e1-6d0f8a5c2b3e"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("project_schema_to_ui")


def sanitize_val(val: Any) -> Any:
    if isinstance(val, str):
        return val.strip()
    return val


def load_schema(schema_path: Path) -> Dict[str, Any]:
    if not schema_path.exists():
        LOG.error("Schema file not found: %s", schema_path)
        sys.exit(20)

    try:
        data = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        LOG.error("JSON parsing error: %s", exc)
        sys.exit(30)

    return data


def classify_field(field_name: str, field_type: str) -> Dict[str, str]:
    """Classifies a schema field into presentation and form control roles based on semantic suffixes."""
    fname = field_name.lower()
    clean_label = " ".join(word.capitalize() for word in field_name.replace("_", " ").split())

    # Primary key
    if fname.endswith("_id") or fname.endswith("_uuid"):
        if not fname.endswith("_fk"):
            return {
                "field": field_name,
                "view": f"Column: {clean_label} Display",
                "form": f"{clean_label} Identifier Badge (Read-only)",
            }

    # Foreign key
    if fname.endswith("_fk"):
        target_name = clean_label.replace(" Fk", "").replace(" Id", "")
        return {
            "field": field_name,
            "view": f"Column: {target_name} Link Badge",
            "form": f"{target_name} Dropdown Selector",
        }

    # Titles and names
    if any(fname.endswith(s) for s in ("_title", "_name", "_label", "_heading")):
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Display",
            "form": f"{clean_label} Input Box",
        }

    # Content and long text
    if any(fname.endswith(s) for s in ("_desc", "_description", "_content", "_body", "_text", "_notes", "_summary")):
        return {
            "field": field_name,
            "view": f"Content Snippet: {clean_label} Excerpt",
            "form": f"{clean_label} Textarea Editor",
        }

    # Boolean flags
    if fname.startswith("is_") or fname.startswith("has_") or fname.endswith("_flag"):
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Status Badge",
            "form": f"{clean_label} Checkbox Toggle",
        }

    # Status / Enum
    if fname.endswith("_status") or fname.endswith("_state") or fname.endswith("_type") or fname.endswith("_role"):
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Status Badge",
            "form": f"{clean_label} Dropdown Selector",
        }

    # Metrics and counts
    if any(fname.endswith(s) for s in ("_count", "_total", "_metric", "_rate", "_amount", "_price", "_bytes")):
        return {
            "field": field_name,
            "view": f"Metric Readout: {clean_label} Display",
            "form": f"{clean_label} Number Input Box",
        }

    # URLs and links
    if any(fname.endswith(s) for s in ("_url", "_link", "_href", "_path")):
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Shortcut Link",
            "form": f"{clean_label} URL Input Box",
        }

    # Timestamps
    if any(fname.endswith(s) for s in ("_created_at", "_date", "_timestamp", "_modified_date")):
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Timestamp Readout",
            "form": f"{clean_label} Date Picker Input Box",
        }

    # Array / Object
    if field_type == "array":
        return {
            "field": field_name,
            "view": f"Column: {clean_label} Tag Row",
            "form": f"{clean_label} Tag Input Box",
        }
    if field_type == "object":
        return {
            "field": field_name,
            "view": f"Expandable Row: {clean_label} Details",
            "form": f"{clean_label} Configuration Editor Modal Overlay",
        }

    # Default fallback
    return {
        "field": field_name,
        "view": f"Column: {clean_label} Display",
        "form": f"{clean_label} Input Box",
    }


def project_entity_schema_to_ascii(
    entity_name: str,
    fields: List[Dict[str, Any]],
    entry_point: str,
) -> str:
    classified = [classify_field(f.get("name", "unknown"), f.get("type", "string")) for f in fields]

    table_columns = [c["view"] for c in classified if c["view"].startswith("Column:")]
    metric_readouts = [c["view"] for c in classified if c["view"].startswith("Metric Readout:")]
    form_inputs = [c["form"] for c in classified]

    lines: List[str] = [
        f"APPLICATION ENTRY POINT ({entry_point})",
        "|",
        f"+-- [SECTION] {entity_name} Management",
        f"|   +-- [CARD] {entity_name} Directory Panel",
    ]

    for m in metric_readouts:
        lines.append(f"|   |   +-- {m}")

    lines.extend([
        f"|   |   +-- [TOOLBAR] {entity_name} Action Bar",
        f"|   |   |   +-- Create {entity_name} Action Button",
        f"|   |   |   +-- Search Filter Input Box",
        f"|   |   +-- Data Table: {entity_name} Collection",
    ])

    for col in table_columns:
        lines.append(f"|   |       +-- {col}")
    lines.append(f"|   |       +-- Column: Inline Actions Group (Edit {entity_name} Button, Delete Action Button)")
    lines.append("|   |")

    # Form Editor
    lines.extend([
        f"|   +-- [SECTION] {entity_name} Editor Form",
        f"|   |   +-- Input Group: Metadata Controls",
    ])

    for fi in form_inputs:
        if "Textarea" not in fi and "Modal" not in fi:
            lines.append(f"|   |   |   +-- {fi}")

    textareas = [fi for fi in form_inputs if "Textarea" in fi]
    if textareas:
        lines.append(f"|   |   +-- Input Group: Content Canvas")
        lines.append(f"|   |   |   +-- [TOOLBAR] Formatting Action Bar (Heading Buttons, Bold Button, Link Button)")
        for ta in textareas:
            lines.append(f"|   |   |   +-- {ta}")

    modals = [fi for fi in form_inputs if "Modal" in fi]
    for mo in modals:
        lines.append(f"|   |   +-- Modal: {mo}")

    lines.extend([
        f"|   |   +-- Action Footer (Save Changes Confirm Button, Cancel Button)",
        "|   |",
        f"|   +-- [SECTION] Operations & Overlays",
        f"|       +-- Confirmation Dialog (Warning Banner, Text Confirmation Input Box, Execute Action Button)",
    ])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="project_schema_to_ui",
        description="Synthesizes clean ASCII UI Component Tree Maps from BEJSON data schemas.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Register script with master index.")
    parser.add_argument("--config", action="store_true", help="Display script configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")
    parser.add_argument("schema", nargs="?", type=Path, help="Path to BEJSON schema file.")
    parser.add_argument("--entry-point", "-e", type=str, default="App_Admin.py", help="Entry surface host file.")
    parser.add_argument("--output", "-o", type=Path, help="Optional output file path for ASCII map.")

    args = parser.parse_args()

    if args.register:
        LOG.info("Registered project_schema_to_ui v%s (%s)", VERSION, RELATIONAL_ID)
        return 0

    if args.config:
        cfg = {"version": VERSION, "release_version": RELEASE_VERSION, "author": "Elton Boehnen"}
        sys.stdout.write(json.dumps(cfg, indent=2) + "\n")
        return 0

    if args.reset:
        LOG.info("Reset state complete.")
        return 0

    if not args.schema:
        parser.print_help()
        return 10

    doc = load_schema(args.schema)
    records_type = doc.get("Records_Type", ["Entity"])
    entity_name = sanitize_val(records_type[0]) if isinstance(records_type, list) and records_type else "Entity"
    fields = doc.get("Fields", [])

    if not fields:
        LOG.error("Schema contains no fields in 'Fields' array.")
        return 30

    ascii_tree = project_entity_schema_to_ascii(entity_name, fields, args.entry_point)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(ascii_tree + "\n", encoding="utf-8")
        LOG.info("Wrote component map to %s (%d fields mapped).", args.output, len(fields))
    else:
        sys.stdout.write(ascii_tree + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
