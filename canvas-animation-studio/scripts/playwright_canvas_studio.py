#!/data/data/com.termux/files/usr/bin/env python3
"""
File:          playwright_canvas_studio.py
Description:   SVG Graphic Animation Playwright Studio Engine.
               Automates headless browser capture of SVG animations, repeating
               texture tiles, and fixed-size canvas stages using BEJSON 105a schemas
               to control frame rate, duration, size, speed, and timeline seeking.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 3a9c7b1e-5f8d-4e2a-9c60-1b2c3d4e5f6a
"""

import argparse
import asyncio
import hashlib
import json
import logging
import math
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Resolve sibling/parent library paths
_HERE = Path(__file__).resolve().parent
_LIB_105_PY = Path("/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY")
if _LIB_105_PY.exists():
    for fam in ("Canvas", "Core"):
        p = str(_LIB_105_PY / fam)
        if p not in sys.path:
            sys.path.insert(0, p)

try:
    from lib_bejson_Canvas_canvas_schemas import (
        create_canvas_config_105a,
        create_frame_sequence_105a,
        compute_frame_seek_points,
        validate_canvas_config,
        get_config_dict,
        CANVAS_STUDIO_CONFIG_FIELDS
    )
    from lib_bejson_Canvas_canvas_templates import (
        list_canvas_templates,
        get_template_path,
        load_template,
        render_canvas_html,
        instantiate_stage_html,
        CANVAS_TEMPLATE_CATALOG
    )
except ImportError:
    # Embedded fallback definitions if running standalone outside library tree
    CANVAS_TEMPLATE_CATALOG = {}
    def create_canvas_config_105a(**kwargs): return {"Format": "BEJSON", "Format_Version": "105a", "Values": [[]]}
    def create_frame_sequence_105a(**kwargs): return {"Format": "BEJSON", "Format_Version": "105a", "Values": []}
    def compute_frame_seek_points(dur, fps, cnt=None):
        cnt = cnt or int(math.ceil(dur * fps))
        return [(i, i / max(1, cnt - 1), i * (dur / max(1, cnt - 1))) for i in range(cnt)]
    def validate_canvas_config(doc): return True, []
    def get_config_dict(doc, idx=0): return {}
    def list_canvas_templates(): return []
    def get_template_path(name): return _HERE / name
    def render_canvas_html(name, **kwargs): return (get_template_path(name)).read_text("utf-8")
    def instantiate_stage_html(name, out, **kwargs):
        html = render_canvas_html(name, **kwargs)
        out.write_text(html, "utf-8")
        return out

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [studio]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("playwright_canvas_studio")
VERSION = "1.0.0"

async def execute_studio_capture(
    config_dict: Dict[str, Any],
    seek_progress: Optional[float] = None,
    render_sequence: bool = False
) -> Dict[str, Any]:
    """Automates Playwright capture of SVG animation canvas stages."""
    template_name = config_dict.get("template_name", "template_square_800x800.html")
    width_px = int(config_dict.get("width_px", 800))
    height_px = int(config_dict.get("height_px", 800))
    stage_selector = config_dict.get("stage_selector", "#capture-stage")
    duration_sec = float(config_dict.get("duration_sec", 8.0))
    fps = int(config_dict.get("fps", 60))
    total_frames = int(config_dict.get("total_frames", 1))
    device_scale = int(config_dict.get("device_scale", 2))
    output_path = Path(config_dict.get("output_path", "captures/stage_capture.png"))
    custom_svg = config_dict.get("svg_inline_markup") or None

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Prepare stage HTML file
    stage_file = output_path.parent / f"_active_{Path(template_name).stem}.html"
    instantiate_stage_html(
        template_name=template_name,
        target_output_file=stage_file,
        custom_svg_markup=custom_svg,
        width_px=width_px,
        height_px=height_px,
        duration_sec=duration_sec
    )

    # 2. Import Playwright driver
    try:
        from termux_playwright import async_playwright_termux, launch
        use_termux_wrapper = True
    except ImportError:
        from playwright.async_api import async_playwright
        use_termux_wrapper = False

    captured_frames_list: List[Dict[str, Any]] = []

    async def run_session(pw_driver):
        if use_termux_wrapper:
            browser = await launch(pw_driver, headless=True)
        else:
            browser = await pw_driver.chromium.launch(headless=True)

        context = await browser.new_context(
            viewport={"width": width_px + 80, "height": height_px + 80},
            device_scale_factor=device_scale
        )
        page = await context.new_page()

        target_url = f"file://{stage_file.resolve()}"
        logger.info(f"Navigating to stage: {target_url}")
        await page.goto(target_url, wait_until="domcontentloaded")

        # Wait for settling signal
        try:
            await page.wait_for_function("window.isReadyToCapture === true", timeout=6000)
        except Exception:
            logger.warning("Timeout on window.isReadyToCapture. Continuing after settling timeout.")
            await page.wait_for_timeout(1000)

        # Locate stage element
        stage_elem = await page.query_selector(stage_selector)
        capture_target = stage_elem if stage_elem else page

        if not render_sequence:
            # Single still frame capture
            target_seek = seek_progress if seek_progress is not None else 0.0
            logger.info(f"Seeking timeline to progress: {target_seek:.3f} ({target_seek * duration_sec:.2f}s)")
            await page.evaluate(f"window.seekProgress && window.seekProgress({target_seek})")
            await page.wait_for_timeout(150)

            await capture_target.screenshot(path=str(output_path))
            file_bytes = output_path.read_bytes()
            sha256 = hashlib.sha256(file_bytes).hexdigest()
            logger.info(f"Saved still capture to {output_path} ({len(file_bytes)} bytes)")

            captured_frames_list.append({
                "frame_index": 0,
                "seek_progress": target_seek,
                "path": str(output_path),
                "bytes": len(file_bytes),
                "sha256": sha256
            })
        else:
            # Multi-frame sequence
            frames_dir = output_path.parent / f"{output_path.stem}_frames"
            frames_dir.mkdir(parents=True, exist_ok=True)
            seek_points = compute_frame_seek_points(duration_sec, fps, total_frames)
            logger.info(f"Rendering sequence: {len(seek_points)} frames into {frames_dir}")

            for idx, ratio, timestamp in seek_points:
                frame_file = frames_dir / f"frame_{idx:04d}.png"
                await page.evaluate(f"window.seekProgress && window.seekProgress({ratio})")
                await page.wait_for_timeout(80)

                await capture_target.screenshot(path=str(frame_file))
                f_bytes = frame_file.read_bytes()
                f_sha = hashlib.sha256(f_bytes).hexdigest()

                captured_frames_list.append({
                    "frame_index": idx,
                    "seek_progress": ratio,
                    "timestamp_sec": timestamp,
                    "path": str(frame_file),
                    "bytes": len(f_bytes),
                    "sha256": f_sha
                })

            logger.info(f"Rendered all {len(seek_points)} frames.")

        await browser.close()

    if use_termux_wrapper:
        async with async_playwright_termux() as pw_instance:
            await run_session(pw_instance)
    else:
        async with async_playwright() as pw_instance:
            await run_session(pw_instance)

    return {
        "status": "success",
        "stage_file": str(stage_file),
        "total_captured": len(captured_frames_list),
        "frames": captured_frames_list
    }

def main():
    parser = argparse.ArgumentParser(description="SVG Graphic Animation Playwright Studio Engine")
    parser.add_argument("--config", "-c", type=str, help="Path to BEJSON 105a canvas studio config file")
    parser.add_argument("--template", "-t", type=str, default="template_square_800x800.html", help="Canvas template file name")
    parser.add_argument("--width", "-w", type=int, default=800, help="Canvas width in pixels")
    parser.add_argument("--height", "-H", type=int, default=800, help="Canvas height in pixels")
    parser.add_argument("--duration", "-d", type=float, default=8.0, help="Animation duration in seconds")
    parser.add_argument("--fps", type=int, default=60, help="Target frames per second")
    parser.add_argument("--frames", type=int, default=1, help="Total frames count (1 for still, >1 for sequence)")
    parser.add_argument("--seek", "-s", type=float, default=0.5, help="Timeline seek ratio (0.0 to 1.0) for still frame")
    parser.add_argument("--output", "-o", type=str, default="captures/canvas_studio_output.png", help="Output PNG path")
    parser.add_argument("--sequence", action="store_true", help="Render full multi-frame animation sequence")
    parser.add_argument("--list-templates", action="store_true", help="List all available canvas templates in the catalog")
    parser.add_argument("--gen-config", type=str, help="Generate a new BEJSON 105a config file at specified path")
    parser.add_argument("--version", action="version", version=f"playwright_canvas_studio v{VERSION}")

    args = parser.parse_args()

    if args.list_templates:
        catalog = list_canvas_templates()
        print(f"\nAvailable Canvas Templates ({len(catalog)} total):\n" + "=" * 65)
        for t in catalog:
            disk_marker = "✓ [Found]" if t.get("exists_on_disk") else "✗ [Missing]"
            print(f"- {t['name']:<36} | {t['width_px']}x{t['height_px']} | {t['category']:<16} | {disk_marker}")
            print(f"  Motif: {t['motif']}")
        return

    if args.gen_config:
        cfg = create_canvas_config_105a(
            template_name=args.template,
            width_px=args.width,
            height_px=args.height,
            duration_sec=args.duration,
            fps=args.fps,
            total_frames=args.frames,
            output_path=args.output
        )
        out_p = Path(args.gen_config)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        print(f"Generated BEJSON 105a config at: {out_p}")
        return

    # Load or compose config
    if args.config:
        cfg_path = Path(args.config)
        doc = json.loads(cfg_path.read_text(encoding="utf-8"))
        is_valid, errs = validate_canvas_config(doc)
        if not is_valid:
            logger.error(f"Invalid BEJSON 105a config: {errs}")
            sys.exit(1)
        config_dict = get_config_dict(doc, 0)
    else:
        doc = create_canvas_config_105a(
            template_name=args.template,
            width_px=args.width,
            height_px=args.height,
            duration_sec=args.duration,
            fps=args.fps,
            total_frames=args.frames,
            output_path=args.output
        )
        config_dict = get_config_dict(doc, 0)

    is_seq = args.sequence or args.frames > 1
    result = asyncio.run(execute_studio_capture(
        config_dict=config_dict,
        seek_progress=args.seek,
        render_sequence=is_seq
    ))
    print(f"\nCapture complete. Captured {result['total_captured']} frame(s).")

if __name__ == "__main__":
    main()
