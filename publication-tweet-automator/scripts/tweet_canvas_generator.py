#!/usr/bin/env python3
"""
File:          tweet_canvas_generator.py
Description:   Automated Twitter/X-Optimized SVG Canvas Media Generator.
               Bridges tweet prompts and threads with the canvas-animation-studio,
               generating high-resolution Twitter-optimized visuals (16:9 landscape,
               1:1 square, 2:1 banner, 9:16 portrait) and copying the resulting
               captures directly into target tweet folders.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 7a8c9b0e-1f2d-4e3a-8b5c-6d7e8f9a0b1c
"""

import argparse
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("tweet_canvas_generator requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [tweet_canvas]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("tweet_canvas_generator")

CANVAS_STUDIO_SCRIPT = Path(
    "/data/data/com.termux/files/home/.gemini/config/skills/canvas-animation-studio/scripts/playwright_canvas_studio.py"
)
DEFAULT_TWEET_IMAGE_DIR = Path(
    "/data/data/com.termux/files/home/generate/prompts/tweet/images"
)

PRESETS: Dict[str, Dict[str, Any]] = {
    "landscape": {
        "width": 1200,
        "height": 675,
        "ratio": "16:9",
        "default_template": "template_widescreen_1280x720.html",
        "description": "Standard In-Feed Landscape Card (1200x675 px, 16:9)"
    },
    "banner": {
        "width": 1200,
        "height": 600,
        "ratio": "2:1",
        "default_template": "template_banner_840x420.html",
        "description": "Thread Header / Summary Large Card Banner (1200x600 px, 2:1)"
    },
    "square": {
        "width": 800,
        "height": 800,
        "ratio": "1:1",
        "default_template": "template_square_800x800.html",
        "description": "Metric / Isometric 3D Cube Spotlight (800x800 px, 1:1)"
    },
    "portrait": {
        "width": 720,
        "height": 1280,
        "ratio": "9:16",
        "default_template": "template_portrait_720x1280.html",
        "description": "Mobile Feed Vertical Telemetry Rail (720x1280 px, 9:16)"
    },
    "icon": {
        "width": 512,
        "height": 512,
        "ratio": "1:1",
        "default_template": "template_icon_bejson_104a_floating.html",
        "description": "App Badge / PWA Master Icon (512x512 px, 1:1)"
    }
}


def compute_sha256(filepath: Path) -> str:
    """Calculates SHA-256 digest of a binary file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def update_bejson_manifest(
    manifest_path: Path,
    record: Dict[str, Any]
) -> None:
    """Safely updates or appends to a BEJSON 104a image manifest."""
    if not manifest_path.exists():
        manifest_data = {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": ["TweetImageRecord"],
            "Fields": [
                {"name": "image_id", "type": "string"},
                {"name": "tweet_prompt_file", "type": "string"},
                {"name": "tweet_number", "type": "integer"},
                {"name": "canvas_template", "type": "string"},
                {"name": "aspect_ratio", "type": "string"},
                {"name": "width_px", "type": "integer"},
                {"name": "height_px", "type": "integer"},
                {"name": "seek_progress", "type": "number"},
                {"name": "output_filename", "type": "string"},
                {"name": "destination_dir", "type": "string"},
                {"name": "sha256_hash", "type": "string"},
                {"name": "created_timestamp", "type": "string"}
            ],
            "Values": []
        }
    else:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception as exc:
            logger.warning(f"Could not parse manifest {manifest_path}: {exc}. Initializing clean store.")
            manifest_data = {"Values": []}

    fields = manifest_data.get("Fields", [])
    field_map = {f["name"]: idx for idx, f in enumerate(fields)}

    row = [None] * len(fields)
    for k, v in record.items():
        if k in field_map:
            row[field_map[k]] = v

    manifest_data.setdefault("Values", []).append(row)

    tmp_file = manifest_path.parent / f"{manifest_path.name}.tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.replace(tmp_file, manifest_path)
    logger.info(f"Updated BEJSON 104a manifest: {manifest_path}")


def run_canvas_capture(
    template_name: str,
    width_px: int,
    height_px: int,
    seek_progress: float,
    temp_output_path: Path
) -> bool:
    """Executes canvas-animation-studio CLI runner via subprocess."""
    if not CANVAS_STUDIO_SCRIPT.exists():
        logger.error(f"Canvas studio runner script not found at {CANVAS_STUDIO_SCRIPT}")
        return False

    cmd = [
        sys.executable,
        str(CANVAS_STUDIO_SCRIPT),
        "--template", template_name,
        "--width", str(width_px),
        "--height", str(height_px),
        "--seek", str(seek_progress),
        "--output", str(temp_output_path)
    ]
    logger.info(f"Invoking canvas studio: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Canvas studio capture failed (exit {result.returncode}):\n{result.stderr}")
        return False

    return temp_output_path.exists() and temp_output_path.stat().st_size > 0


def generate_tweet_image(
    preset_name: str,
    template_name: Optional[str] = None,
    seek_progress: float = 0.5,
    output_filename: Optional[str] = None,
    tweet_dir: Optional[Path] = None,
    prompt_file: str = "custom_tweet.md",
    tweet_number: int = 1,
    manifest_path: Optional[Path] = None
) -> Optional[Path]:
    """Generates Twitter-optimized canvas capture and synchronizes to tweet directory."""
    if preset_name not in PRESETS:
        logger.error(f"Unknown preset: {preset_name}. Valid presets: {list(PRESETS.keys())}")
        return None

    preset = PRESETS[preset_name]
    width_px = preset["width"]
    height_px = preset["height"]
    chosen_template = template_name or preset["default_template"]

    target_tweet_dir = tweet_dir or DEFAULT_TWEET_IMAGE_DIR
    target_tweet_dir.mkdir(parents=True, exist_ok=True)

    if not output_filename:
        stem = Path(prompt_file).stem
        output_filename = f"{stem}_t{tweet_number}_{preset_name}_{width_px}x{height_px}.png"

    staging_dir = Path("/data/data/com.termux/files/home/.gemini/tmp_tweet_canvas")
    staging_dir.mkdir(parents=True, exist_ok=True)
    staging_output = staging_dir / output_filename

    success = run_canvas_capture(
        template_name=chosen_template,
        width_px=width_px,
        height_px=height_px,
        seek_progress=seek_progress,
        temp_output_path=staging_output
    )

    if not success:
        logger.error("Failed to generate canvas image.")
        return None

    final_destination = target_tweet_dir / output_filename
    shutil.copy2(staging_output, final_destination)
    file_bytes = final_destination.stat().st_size
    sha256_hash = compute_sha256(final_destination)
    logger.info(f"Successfully copied Twitter-optimized image to {final_destination} ({file_bytes} bytes)")

    if manifest_path:
        now_ts = datetime.now(timezone.utc).isoformat()
        record = {
            "image_id": f"img_{int(datetime.now(timezone.utc).timestamp())}",
            "tweet_prompt_file": prompt_file,
            "tweet_number": tweet_number,
            "canvas_template": chosen_template,
            "aspect_ratio": preset["ratio"],
            "width_px": width_px,
            "height_px": height_px,
            "seek_progress": seek_progress,
            "output_filename": output_filename,
            "destination_dir": str(target_tweet_dir),
            "sha256_hash": sha256_hash,
            "created_timestamp": now_ts
        }
        update_bejson_manifest(manifest_path, record)

    return final_destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Twitter/X-Optimized SVG Canvas Media Generator (tweet-canvas-automator)"
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        default="landscape",
        help="Twitter/X aspect ratio preset (default: landscape 1200x675)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Canvas template filename (defaults to preset's recommended template)"
    )
    parser.add_argument(
        "--seek",
        type=float,
        default=0.5,
        help="Animation seek progress ratio between 0.0 and 1.0 (default: 0.5)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output image filename (e.g. newagent_hero.png)"
    )
    parser.add_argument(
        "--tweet-dir",
        type=Path,
        default=DEFAULT_TWEET_IMAGE_DIR,
        help=f"Target tweet directory to copy image to (default: {DEFAULT_TWEET_IMAGE_DIR})"
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        default="tweet_prompt.md",
        help="Associated tweet prompt filename"
    )
    parser.add_argument(
        "--tweet-number",
        type=int,
        default=1,
        help="Target tweet number in thread (default: 1)"
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional BEJSON 104a manifest file to register generated image"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available Twitter/X aspect ratio presets"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_presets:
        logger.info("Twitter/X Media Presets:")
        for name, data in PRESETS.items():
            logger.info(f"  - {name:10} | {data['width']}x{data['height']} ({data['ratio']}) | {data['description']}")
        sys.exit(0)

    dest = generate_tweet_image(
        preset_name=args.preset,
        template_name=args.template,
        seek_progress=args.seek,
        output_filename=args.output,
        tweet_dir=args.tweet_dir,
        prompt_file=args.prompt_file,
        tweet_number=args.tweet_number,
        manifest_path=args.manifest
    )

    if dest and dest.exists():
        logger.info(f"Execution complete. Image delivered: {dest}")
        sys.exit(0)
    else:
        logger.error("Failed to generate and copy tweet image.")
        sys.exit(1)


if __name__ == "__main__":
    main()
