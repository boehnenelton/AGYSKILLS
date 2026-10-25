#!/usr/bin/env python3
"""
Tool:            marry_taxonomy_to_template.py
Skill:           template-taxonomy-template (Layer 4)
Description:     Deterministic compiler that marries backend data taxonomies directly to BEHTML templates.
                 Ingests BEJSON schemas and generates production-ready templates with Zero Unmapped Fields.
Version:         1.0.0
Release_Version: 300
Date Created:    2026-10-24
Author:          Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Format_Creator:  Elton Boehnen
RELATIONAL_ID:   c95e1b40-3a2d-4b8c-b10f-7e0a9d8c2345
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION = "1.0.0"
RELEASE_VERSION = "300"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app_logger = logging.getLogger("marry_taxonomy_to_template")


def sanitize_string(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    return str(value) if value is not None else ""


def parse_bejson_fields(schema_path: Path) -> Tuple[str, List[Dict[str, str]]]:
    """Extracts entity name and field definitions from a BEJSON document."""
    if not schema_path.exists():
        app_logger.error("Schema file not found: %s", schema_path)
        sys.exit(10)

    try:
        doc = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        app_logger.error("Failed to parse schema JSON: %s", exc)
        sys.exit(30)

    # Detect entity name
    entity_name = doc.get("Project_Name") or doc.get("Entity_Name") or schema_path.stem.split(".")[0]
    raw_fields = doc.get("Fields", [])
    fields_list = []

    for item in raw_fields:
        if isinstance(item, dict):
            fname = sanitize_string(item.get("name", ""))
            ftype = sanitize_string(item.get("type", "string")).lower()
            if fname and fname != "Record_Type_Parent":
                fields_list.append({"name": fname, "type": ftype})
        elif isinstance(item, str):
            clean_name = sanitize_string(item)
            if clean_name and clean_name != "Record_Type_Parent":
                fields_list.append({"name": clean_name, "type": "string"})

    if not fields_list:
        app_logger.error("No valid fields found in schema: %s", schema_path)
        sys.exit(30)

    return entity_name, fields_list


def classify_field_marriage(field_name: str, field_type: str) -> Dict[str, str]:
    """Classifies a taxonomy field into its married presentation and interactive control slots."""
    clean_name = field_name.strip()
    clean_label = " ".join(word.capitalize() for word in clean_name.replace("_", " ").split())
    fname_lower = clean_name.lower()

    # Suffix mapping
    if fname_lower.endswith("_id") or fname_lower.endswith("_uuid"):
        if fname_lower.endswith("_fk"):
            return {
                "field": clean_name,
                "label": clean_label,
                "view_type": "Relational Foreign Key Link",
                "view_markup": f'<span class="behtml-fk-badge" style="color: #DE2626; font-family: monospace; font-size: 11px;">→ {{{{{clean_name}}}}}</span>',
                "form_type": "Foreign Key Dropdown",
                "form_markup": f'<select style="width: 100%; padding: 6px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 11px;"><option>Select {clean_label} (FK)</option></select>'
            }
        else:
            return {
                "field": clean_name,
                "label": clean_label,
                "view_type": "Primary Identifier Badge",
                "view_markup": f'<span class="behtml-id-badge" style="color: #71717a; font-family: monospace; font-size: 10px;">ID: {{{{{clean_name}}}}}</span>',
                "form_type": "Read-Only ID Display",
                "form_markup": f'<input type="text" readonly value="{{{{{clean_name}}}}}" style="width: 100%; padding: 6px; background: #050508; border: 1px solid #1a1a22; color: #71717a; font-family: monospace; font-size: 11px;">'
            }

    if fname_lower.endswith("_title") or fname_lower.endswith("_name"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "Card Header Title",
            "view_markup": f'<h3 style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px 0;">{{{{{clean_name}}}}}</h3>',
            "form_type": "Text Input Box",
            "form_markup": f'<input type="text" placeholder="{clean_label}" style="width: 100%; padding: 8px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 12px;">'
        }

    if fname_lower.endswith("_desc") or fname_lower.endswith("_content") or fname_lower.endswith("_body"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "Prose Excerpt Container",
            "view_markup": f'<div style="font-size: 12px; line-height: 1.5; color: #d4d4d8; margin-bottom: 8px;">{{{{{clean_name}}}}}</div>',
            "form_type": "Textarea Editor",
            "form_markup": f'<textarea rows="4" placeholder="{clean_label}" style="width: 100%; padding: 8px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 12px; font-family: inherit; resize: vertical;"></textarea>'
        }

    if fname_lower.endswith("_metric") or fname_lower.endswith("_count") or field_type in ("integer", "number", "int"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "KPI Metric Stat Box",
            "view_markup": f'<div style="background: #09090d; border: 1px solid #1c1c24; padding: 8px; border-left: 3px solid #DE2626;"><div style="font-size: 9px; color: #71717a; text-transform: uppercase;">{clean_label}</div><div style="font-size: 18px; font-weight: 700; font-family: monospace; color: #FFFFFF;">{{{{{clean_name}}}}}</div></div>',
            "form_type": "Numeric Input Box",
            "form_markup": f'<input type="number" placeholder="0" style="width: 100%; padding: 6px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 12px; font-family: monospace;">'
        }

    if fname_lower.endswith("_flag") or fname_lower.startswith("is_") or field_type in ("boolean", "bool"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "Status Toggle Indicator",
            "view_markup": f'<span style="padding: 2px 6px; font-size: 10px; font-weight: 600; text-transform: uppercase; background: rgba(222, 38, 38, 0.15); color: #DE2626; border: 1px solid #DE2626;">{{{{{clean_name}}}}}</span>',
            "form_type": "Checkbox Toggle",
            "form_markup": f'<label style="display: flex; align-items: center; gap: 8px; font-size: 11px; cursor: pointer;"><input type="checkbox" style="accent-color: #DE2626;"> <span>Enable {clean_label}</span></label>'
        }

    if fname_lower.endswith("_url") or fname_lower.endswith("_link"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "Hyperlink Action",
            "view_markup": f'<a href="{{{{{clean_name}}}}}" style="font-size: 11px; color: #DE2626; text-decoration: none;" target="_blank">View {clean_label} →</a>',
            "form_type": "URL Input Box",
            "form_markup": f'<input type="url" placeholder="https://..." style="width: 100%; padding: 6px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 11px; font-family: monospace;">'
        }

    if fname_lower.endswith("_timestamp") or fname_lower.endswith("_at") or fname_lower.endswith("_date"):
        return {
            "field": clean_name,
            "label": clean_label,
            "view_type": "Timestamp Readout",
            "view_markup": f'<span style="font-size: 10px; color: #71717a; font-family: monospace;">{{{{{clean_name}}}}}</span>',
            "form_type": "Date/Time Input Box",
            "form_markup": f'<input type="datetime-local" style="width: 100%; padding: 6px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 11px; font-family: monospace;">'
        }

    # Default fallback
    return {
        "field": clean_name,
        "label": clean_label,
        "view_type": "Data Property Readout",
        "view_markup": f'<div style="font-size: 11px;"><span style="color: #71717a;">{clean_label}:</span> <span style="color: #FFFFFF;">{{{{{clean_name}}}}}</span></div>',
        "form_type": "Standard Text Input",
        "form_markup": f'<input type="text" placeholder="{clean_label}" style="width: 100%; padding: 6px; background: #08080c; border: 1px solid #282834; color: #FFFFFF; font-size: 11px;">'
    }


def generate_married_behtml_template(
    entity_name: str,
    fields_roster: List[Dict[str, str]],
    template_role: str = "management"
) -> str:
    """Generates a BEHTML template married 1:1 to the backend taxonomy with zero unmapped fields."""
    marriages = [classify_field_marriage(f["name"], f["type"]) for f in fields_roster]

    view_elements = []
    form_elements = []

    for m in marriages:
        view_elements.append(f"""        <!-- Married View: {m['field']} ({m['view_type']}) -->
        <div style="margin-bottom: 8px;">
          {m['view_markup']}
        </div>""")

        form_elements.append(f"""        <!-- Married Control: {m['field']} ({m['form_type']}) -->
        <div style="margin-bottom: 10px;">
          <label style="display: block; font-size: 10px; text-transform: uppercase; color: #a1a1aa; margin-bottom: 3px; font-weight: 500;">{m['label']}</label>
          {m['form_markup']}
        </div>""")

    # Table columns for directory view
    table_headers = "".join([f'<th style="padding: 6px 10px; border-bottom: 2px solid #DE2626; color: #a1a1aa; font-size: 11px; text-align: left;">{m["label"]}</th>' for m in marriages])
    table_sample_row = "".join([f'<td style="padding: 6px 10px; border-bottom: 1px solid #14141c; font-size: 11px; font-family: monospace;">{{{{{m["field"]}}}}}</td>' for m in marriages])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>{entity_name} — Married BEHTML Template</title>
  <style>
    :root {{
      --app-height: 100vh;
      --behtml-ry: 32px;
      --behtml-bg-canvas: #000000;
      --behtml-fg-text: #FFFFFF;
      --behtml-accent-red: #DE2626;
      --behtml-border-divider: #1f1f28;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    html, body {{
      width: 100vw;
      height: var(--app-height);
      overflow-x: hidden;
      background: var(--behtml-bg-canvas);
      color: var(--behtml-fg-text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
      font-size: 13px;
    }}
    /* Layer 4 Top-Docked Control Hub (z: 128) */
    .behtml-layer-4-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 64px;
      z-index: 128;
      background: #060608;
      border-bottom: 1px solid var(--behtml-border-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
    }}
    /* Layer 1 16-Sublane Base Canvas */
    .behtml-layer-1-canvas {{
      margin-top: 64px;
      padding: 24px 16px 48px;
      display: grid;
      grid-template-columns: repeat(16, 1fr);
      gap: 16px;
    }}
    /* Layer 2 Surface Cards (z: 32) */
    .behtml-layer-2-card {{
      background: #09090d;
      border: 1px solid var(--behtml-border-divider);
      padding: 16px;
      display: flex;
      flex-direction: column;
    }}
  </style>
</head>
<body>

  <!-- Layer 4 Persistent Header (z: 128) -->
  <header class="behtml-layer-4-header">
    <div style="display: flex; align-items: center; gap: 10px;">
      <div style="font-weight: 700; font-size: 13px; letter-spacing: 0.5px;">
        TAXONOMY MARRIAGE: <span style="color: var(--behtml-accent-red);">{entity_name.upper()}</span>
      </div>
      <span style="font-size: 10px; color: #71717a; font-family: monospace;">{len(fields_roster)} Married Fields</span>
    </div>
    <div style="font-size: 11px; color: #a1a1aa; font-family: monospace;">
      ZERO UNMAPPED FIELDS · RELEASE 300
    </div>
  </header>

  <!-- Layer 1 Canvas Surface -->
  <main class="behtml-layer-1-canvas">

    <!-- View Directory Card (Occupies 10 sublanes = 62.5% width) -->
    <section class="behtml-layer-2-card" style="grid-column: span 10;">
      <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--behtml-accent-red); border-bottom: 1px solid #1a1a24; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between;">
        <span>{entity_name} Presentation Surface</span>
        <span>Directory View</span>
      </div>
      
      <!-- High-Density Tabular View with Married Columns -->
      <div style="overflow-x: auto; margin-bottom: 16px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
          <thead>
            <tr>
              {table_headers}
            </tr>
          </thead>
          <tbody>
            <tr>
              {table_sample_row}
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Detail Card Excerpt Readout -->
      <div style="background: #050508; border: 1px solid #181822; padding: 12px;">
        <div style="font-size: 10px; color: #71717a; text-transform: uppercase; margin-bottom: 8px; font-weight: 600;">Single Record Detail Projections</div>
{"".join(view_elements)}
      </div>
    </section>

    <!-- Interactive Form Card (Occupies 6 sublanes = 37.5% width) -->
    <section class="behtml-layer-2-card" style="grid-column: span 6;">
      <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--behtml-accent-red); border-bottom: 1px solid #1a1a24; padding-bottom: 8px; margin-bottom: 12px;">
        {entity_name} Interactive Form Controls
      </div>
      <form onsubmit="event.preventDefault();">
{"".join(form_elements)}
        <button type="submit" style="width: 100%; padding: 10px; background: var(--behtml-accent-red); border: 1px solid var(--behtml-accent-red); color: #FFFFFF; font-weight: 700; font-size: 11px; text-transform: uppercase; cursor: pointer; margin-top: 8px;">
          Commit {entity_name} Record
        </button>
      </form>
    </section>

  </main>

  <!-- Viewport Height Synchronization -->
  <script>
    if (window.visualViewport) {{
      function syncAppHeight() {{
        document.documentElement.style.setProperty('--app-height', window.visualViewport.height + 'px');
      }}
      window.visualViewport.addEventListener('resize', syncAppHeight);
      syncAppHeight();
    }}
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="marry_taxonomy_to_template",
        description="Marries backend BEJSON taxonomies directly to BEHTML templates with Zero Unmapped Fields."
    )
    parser.add_argument("schema", type=str, help="Path to source BEJSON schema file")
    parser.add_argument("--output", type=str, required=True, help="Destination path for married BEHTML template file")
    parser.add_argument("--version", action="version", version=f"marry_taxonomy_to_template v{VERSION}")

    args = parser.parse_args()
    schema_path = Path(args.schema).resolve()
    output_path = Path(args.output).resolve()

    entity_name, fields = parse_bejson_fields(schema_path)
    app_logger.info("Marrying entity '%s' (%d fields) -> %s", entity_name, len(fields), output_path)

    rendered_html = generate_married_behtml_template(entity_name, fields)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_html, encoding="utf-8")

    app_logger.info("Successfully materialized married template: %s", output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
