#!/usr/bin/env python3
"""
scripts/plan_web_taxonomy.py
Domain 1: The Taxonomy Planner
Validates and generates canonical 104a.taxonomy_schema.bejson manifests.
"""

import sys
import json
import argparse
from pathlib import Path

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

def build_field_map(fields_list: list) -> dict:
    return {field_dict["name"]: idx for idx, field_dict in enumerate(fields_list)}

def validate_taxonomy_manifest(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"[ERROR] Manifest not found: {file_path}", file=sys.stderr)
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("Format") != "BEJSON" or data.get("Format_Version") != "104a":
        print(f"[ERROR] Invalid format: Expected BEJSON 104a, got {data.get('Format')} {data.get('Format_Version')}", file=sys.stderr)
        return False

    fields = data.get("Fields", [])
    values = data.get("Values", [])
    f_map = build_field_map(fields)

    required_fields = ["taxonomy_id", "taxonomy_slug", "taxonomy_display_name", "parent_taxonomy_id", "depth_level", "entity_prefix"]
    for req in required_fields:
        if req not in f_map:
            print(f"[ERROR] Missing required field: {req}", file=sys.stderr)
            return False

    print(f"[SUCCESS] Validated BEJSON 104a Taxonomy Manifest: {file_path} ({len(values)} taxonomy nodes)")
    return True

def init_starter_manifest(output_path: Path):
    sample_file = get_script_path().parent / "assets" / "sample_taxonomy_blueprint.104a.bejson"
    if sample_file.exists():
        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"[SUCCESS] Initialized starter taxonomy manifest at: {output_path}")
    else:
        print("[ERROR] Sample asset not found.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Web Taxonomy Planner CLI (Domain 1)")
    parser.add_argument("--validate", type=str, help="Path to 104a.taxonomy_schema.bejson to validate")
    parser.add_argument("--init", action="store_true", help="Initialize a starter taxonomy manifest")
    parser.add_argument("--output", type=str, default="104a.taxonomy_schema.bejson", help="Output path for initialized manifest")

    args = parser.parse_args()

    if args.validate:
        ok = validate_taxonomy_manifest(Path(args.validate))
        sys.exit(0 if ok else 1)
    elif args.init:
        init_starter_manifest(Path(args.output))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
