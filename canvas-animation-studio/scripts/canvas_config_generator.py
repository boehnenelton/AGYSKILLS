#!/data/data/com.termux/files/usr/bin/env python3
"""
File:        canvas_config_generator.py
Description: Generates parameterized BEJSON 105a Canvas Studio config documents.
Version:     1.0.0
Author:      Elton Boehnen · boehnenelton2024@gmail.com
"""

import argparse
import json
import sys
from pathlib import Path

# Add libraries path
sys.path.insert(0, "/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY/Canvas")
try:
    from lib_bejson_Canvas_canvas_schemas import create_canvas_config_105a, validate_canvas_config
except ImportError:
    print("Error: lib_bejson_Canvas_canvas_schemas not found on system path.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate BEJSON 105a Canvas Studio configuration")
    parser.add_argument("--id", default="canvas_stage_01", help="Canvas identifier")
    parser.add_argument("--template", default="template_square_800x800.html", help="Template name")
    parser.add_argument("--width", type=int, default=800, help="Stage width in pixels")
    parser.add_argument("--height", type=int, default=800, help="Stage height in pixels")
    parser.add_argument("--duration", type=float, default=8.0, help="Duration in seconds")
    parser.add_argument("--fps", type=int, default=60, help="Frame rate")
    parser.add_argument("--output", default="captures/output.png", help="Target output file path")
    parser.add_argument("--save", "-s", required=True, help="Destination .105a.bejson file path")

    args = parser.parse_args()

    doc = create_canvas_config_105a(
        canvas_id=args.id,
        template_name=args.template,
        width_px=args.width,
        height_px=args.height,
        duration_sec=args.duration,
        fps=args.fps,
        output_path=args.output
    )

    is_valid, errs = validate_canvas_config(doc)
    if not is_valid:
        print(f"Validation failed: {errs}")
        sys.exit(1)

    dest = Path(args.save)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Created valid BEJSON 105a Canvas Studio config at: {dest}")

if __name__ == "__main__":
    main()
