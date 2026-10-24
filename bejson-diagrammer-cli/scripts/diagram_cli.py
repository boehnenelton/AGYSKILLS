#!/usr/bin/env python3
"""
File:           diagram_cli.py
Description:    Python CLI tool for BEJSON Diagrammer generation, active board extension,
                spatial scaffolding, and injection into Canvas/Component Templates.
                Single Source of Truth: MFDB Diagrammer React Conversion Ecosystem.
Relational IDs: 64b9314e-f6bf-4807-84c7-a2852eae1771 (Ledger Blueprint)
                c9f8e7d6-c5b4-4321-8765-43210fe98765 (Arrival Validation)
Version:        2.0.0
Author:         Elton Boehnen · boehnenelton2024@gmail.com
"""

import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.error

RELATIONAL_ID = "64b9314e-f6bf-4807-84c7-a2852eae1771"
ARRIVAL_VALIDATION_RELATIONAL_ID = "c9f8e7d6-c5b4-4321-8765-43210fe98765"

TARGET_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.1-pro-preview"
]
DEFAULT_MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION_BLUEPRINT = """You are an expert systems diagrammer and spatial software architect.
Your task is to take natural language requirements from the user and construct a structured diagram build plan adhering to the BEJSON Diagrammer MFDB Schema.

The diagram structure consists of:
1. Shapes: Nodes on the board.
   - tempId: unique temporary identifier (e.g. 's1', 's2')
   - label: concise descriptive label
   - text: optional multi-line explanatory body text
   - kind: 'rect' or 'circle'
   - sizeClass: 'small' (100x100), 'medium' (200x100), 'large' (300x150), 'huge' (600x300)
   - color: hex color code (default '#d9d9d9' or '#b3b3b3' for child nodes)
   - fontColor: 'auto', '#ffffff', or '#000000'
   - cx: horizontal center coordinate in pixels
   - cy: vertical center coordinate in pixels
   - parentTempId: optional parent shape tempId establishing tree hierarchy

2. Connectors: Relationships between shapes.
   - fromTempId: source shape tempId
   - toTempId: destination shape tempId
   - flow: 'forward' (arrow at destination), 'backward' (arrow at source), 'bidirectional' (arrows on both ends), 'none' (solid line)

3. Territories: Bounding background regions or zones.
   - kind: 'rect' or 'circle'
   - cx: horizontal center coordinate
   - cy: vertical center coordinate
   - size: width/height or diameter in pixels (min 80, typical 240-400)
   - label: territory name
   - color: brand territory hex color (e.g. '#000000', '#DE2626', '#737373')

Layout Rules:
- Prevent overlapping shapes by providing at least 40px padding between bounding boxes.
- Group related nodes inside dedicated territories if requested.
- Place root nodes near the top (cy: 200) and cascade child tiers downward (cy + 160) or horizontally (cx + 240).
- If XML tags such as <scaffold mode="tree|flowchart|grid"/> or <zone name="..."/> are used, align spatial coordinates to the requested pattern.
- Mobile Viewport Standard: Always account for the 100 pixel lower browser toolbar on mobile devices (reserve at least 100px bottom clearance/padding on viewports, position bottom floating actions and inspectors at bottom: calc(100px + 16px), and fitView with 160px bottom clearance).

Response Format:
Return strictly a valid JSON object without surrounding markdown fences or commentary:
{
  "shapes": [ ... ],
  "connectors": [ ... ],
  "territories": [ ... ]
}"""

SIZE_CLASSES = {
    "small":  {"w": 100, "h": 100},
    "medium": {"w": 200, "h": 100},
    "large":  {"w": 300, "h": 150},
    "huge":   {"w": 600, "h": 300},
}
KNOWN_SIZE_CLASSES = ["small", "medium", "large", "huge"]
KNOWN_SHAPE_KINDS = ["rect", "circle"]
KNOWN_FLOW_VALUES = ["forward", "backward", "bidirectional", "none"]
HEX_COLOR_REGEX = re.compile(r"^#[0-9a-fA-F]{3,8}$")


def validate_plan_semantics(plan):
    errors = []
    warnings = []
    if not isinstance(plan, dict):
        return {"valid": False, "errors": ["Plan is not a JSON object."], "warnings": []}

    seen_ids = set()
    for s in plan.get("shapes", []):
        tid = s.get("tempId") or s.get("id") or "?"
        if tid in seen_ids:
            errors.append(f"Duplicate shape identifier '{tid}'.")
        seen_ids.add(tid)

        sc = s.get("sizeClass", "medium")
        if sc not in KNOWN_SIZE_CLASSES:
            errors.append(f"Shape '{tid}': invalid sizeClass '{sc}'.")
        kind = s.get("kind", "rect")
        if kind not in KNOWN_SHAPE_KINDS:
            errors.append(f"Shape '{tid}': invalid kind '{kind}'.")
        for coord in ("cx", "cy"):
            if not isinstance(s.get(coord), (int, float)):
                errors.append(f"Shape '{tid}': {coord} must be numeric.")
        col = s.get("color")
        if col and not HEX_COLOR_REGEX.match(str(col)):
            warnings.append(f"Shape '{tid}': color '{col}' is not standard hex.")
        lbl = s.get("label")
        if not lbl or not str(lbl).strip():
            warnings.append(f"Shape '{tid}': missing descriptive label.")

    for i, c in enumerate(plan.get("connectors", [])):
        flow = c.get("flow", "forward")
        if flow not in KNOWN_FLOW_VALUES:
            errors.append(f"Connector #{i}: invalid flow '{flow}'.")

    for i, t in enumerate(plan.get("territories", [])):
        for coord in ("cx", "cy", "size"):
            if not isinstance(t.get(coord), (int, float)):
                errors.append(f"Territory #{i}: {coord} must be numeric.")
        if t.get("size", 0) <= 0:
            errors.append(f"Territory #{i}: size must be positive.")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def get_box_of(s):
    d = SIZE_CLASSES.get(s.get("sizeClass", "medium"), SIZE_CLASSES["medium"])
    cx = s.get("cx", 300)
    cy = s.get("cy", 200)
    return {"x": cx - d["w"] / 2, "y": cy - d["h"] / 2, "w": d["w"], "h": d["h"]}


def get_territory_box(t):
    sz = t.get("size", 240)
    cx = t.get("cx", 300)
    cy = t.get("cy", 300)
    return {"x": cx - sz / 2, "y": cy - sz / 2, "w": sz, "h": sz}


def boxes_overlap(a, b):
    return a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]


def validate_diagram(diagram):
    errors = []
    warnings = []

    shapes = diagram.get("shapes", [])
    connectors = diagram.get("connectors", [])
    territories = diagram.get("territories", [])

    shape_ids = set()
    shape_map = {}

    for s in shapes:
        sid = s.get("id")
        if sid in shape_ids:
            errors.append(f"Duplicate shape ID '{sid}'.")
        shape_ids.add(sid)
        shape_map[sid] = s

        sc = s.get("sizeClass")
        if sc and sc not in KNOWN_SIZE_CLASSES:
            errors.append(f"Shape '{sid}' has unknown sizeClass '{sc}'.")
        kind = s.get("kind")
        if kind and kind not in KNOWN_SHAPE_KINDS:
            errors.append(f"Shape '{sid}' has unknown kind '{kind}'.")
        pid = s.get("parentId")
        if pid and pid not in shape_ids and not any(x.get("id") == pid for x in shapes):
            errors.append(f"Shape '{sid}' references non-existent parentId '{pid}'.")

    # Cycle check
    for s in shapes:
        visited = set()
        cur = s
        while cur and cur.get("parentId"):
            cid = cur.get("id")
            if cid in visited:
                errors.append(f"Shape '{s.get('id')}' is part of a hierarchy cycle.")
                break
            visited.add(cid)
            cur = shape_map.get(cur.get("parentId"))

    # Connectors
    for c in connectors:
        cid = c.get("id")
        fr = c.get("from")
        to = c.get("to")
        if fr not in shape_ids:
            errors.append(f"Connector '{cid}' references missing source '{fr}'.")
        if to not in shape_ids:
            errors.append(f"Connector '{cid}' references missing target '{to}'.")
        if fr == to:
            errors.append(f"Connector '{cid}' connects shape '{fr}' to itself.")

    # Shape overlap
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            if boxes_overlap(get_box_of(shapes[i]), get_box_of(shapes[j])):
                errors.append(f"Shapes '{shapes[i].get('id')}' and '{shapes[j].get('id')}' overlap.")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def remediate_diagram(diagram):
    shapes = list(diagram.get("shapes", []))
    connectors = list(diagram.get("connectors", []))
    territories = list(diagram.get("territories", []))

    seen_ids = set()
    for idx, s in enumerate(shapes):
        sid = s.get("id")
        if not sid or sid in seen_ids:
            s["id"] = f"shape_{idx + 1}"
        seen_ids.add(s["id"])
        s["cx"] = int(round((s.get("cx") or 300) / 50.0) * 50)
        s["cy"] = int(round((s.get("cy") or 200) / 50.0) * 50)
        s["sizeClass"] = s.get("sizeClass", "medium")
        s["kind"] = s.get("kind", "rect")
        s["color"] = s.get("color", "#d9d9d9")
        s["fontColor"] = s.get("fontColor", "auto")

    shape_map = {s["id"]: s for s in shapes}
    for s in shapes:
        pid = s.get("parentId")
        if pid and pid not in shape_map:
            s["parentId"] = None

    connectors = [c for c in connectors if c.get("from") in shape_map and c.get("to") in shape_map and c.get("from") != c.get("to")]

    for idx, t in enumerate(territories):
        if not t.get("id"):
            t["id"] = f"terr_{idx + 1}"
        t["cx"] = int(round((t.get("cx") or 300) / 50.0) * 50)
        t["cy"] = int(round((t.get("cy") or 300) / 50.0) * 50)
        t["size"] = max(80, int(t.get("size", 240)))
        t["kind"] = t.get("kind", "rect")
        t["color"] = t.get("color", "#000000")

    return {
        "diagramId": diagram.get("diagramId", f"diag_{os.getpid()}"),
        "name": diagram.get("name", "Architecture Diagram"),
        "description": diagram.get("description", ""),
        "shapes": shapes,
        "connectors": connectors,
        "territories": territories
    }


def inject_into_template(template_path, diagram_data, output_path, custom_title=None):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    title = custom_title or diagram_data.get("name", "Architecture Diagram")
    desc = diagram_data.get("description", "Technical Architecture Specification")
    json_str = json.dumps(diagram_data, indent=2)

    placeholder_pattern = r"/\*\s*__DIAGRAM_DATA__\s*\*/"
    if re.search(placeholder_pattern, html):
        html = re.sub(placeholder_pattern, json_str, html)
    else:
        html = re.sub(
            r'<script class="w-diag-data" type="application/json">[\s\S]*?</script>',
            f'<script class="w-diag-data" type="application/json">\n{json_str}\n    </script>',
            html
        )
        html = re.sub(
            r'<script id="injected-diagram-data" type="application/json">[\s\S]*?</script>',
            f'<script id="injected-diagram-data" type="application/json">\n{json_str}\n  </script>',
            html
        )

    import random, string
    inst_id = "inst_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    html = html.replace("__INSTANCE_ID__", inst_id)
    html = html.replace("__DIAGRAM_TITLE__", title)
    html = html.replace("__DIAGRAM_DESCRIPTION__", desc)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def main():
    parser = argparse.ArgumentParser(description=f"BEJSON Diagrammer CLI (Relational ID: {RELATIONAL_ID})")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # validate
    val_p = subparsers.add_parser("validate", help="Validate diagram against React app validators")
    val_p.add_argument("-f", "--file", required=True, help="Diagram JSON file")

    args = parser.parse_args()

    if args.command == "validate":
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        sem = validate_plan_semantics(data)
        diag = validate_diagram(data)
        print("\n======================================================")
        print(f"DIAGRAM VALIDATION REPORT (Relational ID: {ARRIVAL_VALIDATION_RELATIONAL_ID})")
        print(f"Target: {args.file}")
        print("======================================================")
        print(f"1. Plan Semantics: {'PASSED' if sem['valid'] else 'FAILED'}")
        for e in sem["errors"]: print(f"   ✖ {e}")
        for w in sem["warnings"]: print(f"   ⚠ {w}")

        print(f"\n2. Relational & Spatial Verification: {'PASSED' if diag['valid'] else 'FAILED'}")
        print(f"   - Total Shapes: {len(data.get('shapes', []))}")
        print(f"   - Total Connectors: {len(data.get('connectors', []))}")
        print(f"   - Total Territories: {len(data.get('territories', []))}")
        for e in diag["errors"]: print(f"   ✖ {e}")
        for w in diag["warnings"]: print(f"   ⚠ {w}")
        print(f"\nOVERALL: {'100% VALID' if sem['valid'] and diag['valid'] else 'ISSUES REPORTED'}")


if __name__ == "__main__":
    main()
