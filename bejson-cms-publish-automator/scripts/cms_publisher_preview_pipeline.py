#!/data/data/com.termux/files/usr/bin/env python3
"""
File:          cms_publisher_preview_pipeline.py
Description:   Layer 3 BEJSON CMS Publisher, Preview Server & Playwright Capture Pipeline.
               Automates static site publication, preview server binding, Android browser
               dispatch via termux-open, and optional multi-viewport 6-screenshot capture
               directly into the CMS images/ directory.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 6d5e4f3a-2b1c-0d9e-8f7a-6b5c4d3e2f1a
"""

import argparse
import asyncio
import http.server
import json
import logging
import os
import shutil
import socket
import socketserver
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("cms_publisher_preview_pipeline requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [cms_pipeline]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("cms_publisher_preview_pipeline")


def execute_publisher_build(cms_root: Path) -> bool:
    """Executes BEJSON_CMS_Publisher static site build."""
    web_dir = cms_root / "src" / "web"
    if not web_dir.exists():
        logger.error(f"CMS web directory not found at: {web_dir}")
        return False

    sys.path.insert(0, str(web_dir))
    try:
        import BEJSON_CMS_Publisher as pub
        logger.info("Executing static site build via BEJSON_CMS_Publisher...")
        pub._execute()
        build_dir = cms_root / "storage" / "builds"
        if (build_dir / "index.html").exists():
            logger.info(f"Static build complete in: {build_dir}")
            return True
        else:
            logger.error("Build failed: index.html was not generated.")
            return False
    except Exception as exc:
        logger.error(f"Publisher build encountered an exception: {exc}")
        return False


def start_preview_server(build_dir: Path, port: int) -> Tuple[Optional[socketserver.TCPServer], Optional[threading.Thread]]:
    """Starts local HTTP preview server bound to build directory, or reuses existing active server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe_sock:
        probe_sock.settimeout(0.5)
        if probe_sock.connect_ex(("127.0.0.1", port)) == 0:
            logger.info(f"Existing preview server detected and responding at http://localhost:{port}")
            return None, None

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir), **kwargs)
        def log_message(self, fmt, *args):
            pass

    httpd = socketserver.TCPServer(("", port), Handler)
    httpd.allow_reuse_address = True
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    logger.info(f"Preview server running at http://localhost:{port}")
    return httpd, server_thread


def open_termux_browser(url: str) -> bool:
    """Invokes termux-open to launch browser on Android."""
    termux_open_path = shutil.which("termux-open")
    if not termux_open_path:
        logger.warning("termux-open binary not found on PATH. Skipping browser launch.")
        return False

    try:
        logger.info(f"Dispatching browser launch via termux-open: {url}")
        subprocess.run([termux_open_path, url], check=False)
        return True
    except Exception as exc:
        logger.warning(f"termux-open launch failed: {exc}")
        return False


async def capture_6_screenshots(cms_root: Path, port: int, images_dir: Optional[Path] = None) -> int:
    """Captures 6 canonical preview screenshots using Playwright."""
    target_images_dir = images_dir or (cms_root / "images")
    target_images_dir.mkdir(parents=True, exist_ok=True)

    build_dir = cms_root / "storage" / "builds"
    
    # Discover actual article subpath if present
    blog_dir = build_dir / "blog"
    blog_htmls = list(blog_dir.glob("**/*.html")) if blog_dir.exists() else []
    art1_url = f"http://localhost:{port}/index.html"
    art2_url = f"http://localhost:{port}/index.html"
    if len(blog_htmls) >= 1:
        rel1 = blog_htmls[0].relative_to(build_dir)
        art1_url = f"http://localhost:{port}/{rel1}"
    if len(blog_htmls) >= 2:
        rel2 = blog_htmls[1].relative_to(build_dir)
        art2_url = f"http://localhost:{port}/{rel2}"

    cat_dir = build_dir / "category"
    cat_htmls = list(cat_dir.glob("**/*.html")) if cat_dir.exists() else []
    cat_url = f"http://localhost:{port}/index.html"
    if cat_htmls:
        cat_rel = cat_htmls[0].relative_to(build_dir)
        cat_url = f"http://localhost:{port}/{cat_rel}"

    art1_name = "03_published_article_newagent.png" if "newagent" in str(art1_url) else "03_published_article_1.png"
    art2_name = "04_published_article_telemetry.png" if "telemetry" in str(art2_url) else "04_published_article_2.png"
    cat_name = "06_published_category_bejson.png" if "bejson" in str(cat_url) else "06_published_category_feed.png"

    targets = [
        ("01_published_home_desktop.png", f"http://localhost:{port}/index.html", 1280, 720),
        ("02_published_home_mobile.png", f"http://localhost:{port}/index.html", 375, 812),
        (art1_name, art1_url, 1280, 720),
        (art2_name, art2_url, 1280, 720),
        ("05_published_apps_feed.png", f"http://localhost:{port}/apps/index.html", 1280, 720),
        (cat_name, cat_url, 1280, 720)
    ]

    try:
        from termux_playwright import async_playwright_termux, launch
        use_termux_wrapper = True
    except ImportError:
        from playwright.async_api import async_playwright
        use_termux_wrapper = False

    captured_count = 0

    async def run_captures(pw_driver):
        nonlocal captured_count
        if use_termux_wrapper:
            browser = await launch(pw_driver, headless=True)
        else:
            browser = await pw_driver.chromium.launch(headless=True)

        for filename, url, width, height in targets:
            try:
                context = await browser.new_context(viewport={"width": width, "height": height})
                page = await context.new_page()
                logger.info(f"Navigating to {url} ({width}x{height})...")
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(350)
                out_path = target_images_dir / filename
                await page.screenshot(path=str(out_path))
                logger.info(f"Captured {filename} ({out_path.stat().st_size} bytes)")
                captured_count += 1
                await context.close()
            except Exception as e:
                logger.error(f"Failed to capture {filename}: {e}")

        await browser.close()

    if use_termux_wrapper:
        async with async_playwright_termux() as pw:
            await run_captures(pw)
    else:
        async with async_playwright() as pw:
            await run_captures(pw)

    return captured_count


def update_publish_manifest(manifest_path: Path, record: Dict[str, Any]) -> None:
    """Updates BEJSON 104a publish manifest."""
    manifest_data: Dict[str, Any] = {"Values": []}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception:
            manifest_data = {"Values": []}

    fields = manifest_data.get("Fields", [
        {"name": "session_id", "type": "string"},
        {"name": "cms_root", "type": "string"},
        {"name": "build_dir", "type": "string"},
        {"name": "preview_port", "type": "integer"},
        {"name": "browser_opened", "type": "boolean"},
        {"name": "screenshots_captured", "type": "integer"},
        {"name": "screenshots_dir", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "timestamp", "type": "string"}
    ])
    manifest_data["Fields"] = fields

    field_map = {f["name"]: idx for idx, f in enumerate(fields)}
    row = [None] * len(fields)
    for k, v in record.items():
        if k in field_map:
            row[field_map[k]] = v

    manifest_data.setdefault("Values", []).append(row)
    manifest_data["Format"] = "BEJSON"
    manifest_data["Format_Version"] = "104a"
    manifest_data["Format_Creator"] = "Elton Boehnen"
    manifest_data["Records_Type"] = ["PublishPreviewRecord"]

    tmp_path = manifest_path.parent / f"{manifest_path.name}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.replace(tmp_path, manifest_path)
    logger.info(f"Updated publish registry: {manifest_path}")


def perform_visual_regression_diff(
    current_images_dir: Path,
    baseline_images_dir: Path,
    diff_output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Compares current screenshots against baseline captures and detects pixel diffs."""
    results: Dict[str, Any] = {
        "compared": 0,
        "matched": 0,
        "diverged": 0,
        "missing_baseline": 0,
        "details": [],
    }

    if not baseline_images_dir.exists():
        logger.warning(f"Baseline directory not found: {baseline_images_dir}")
        return results

    if diff_output_dir:
        diff_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from PIL import Image, ImageChops
    except ImportError:
        logger.warning("Pillow is not installed. Skipping visual diffing.")
        return results

    for current_file in sorted(current_images_dir.glob("*.png")):
        baseline_file = baseline_images_dir / current_file.name
        if not baseline_file.is_file():
            results["missing_baseline"] += 1
            results["details"].append({"file": current_file.name, "status": "MISSING_BASELINE"})
            continue

        results["compared"] += 1
        with Image.open(current_file) as cur_img, Image.open(baseline_file) as base_img:
            if cur_img.size != base_img.size:
                results["diverged"] += 1
                results["details"].append({
                    "file": current_file.name,
                    "status": "DIMENSION_MISMATCH",
                    "current": cur_img.size,
                    "baseline": base_img.size
                })
                continue

            diff = ImageChops.difference(cur_img.convert("RGB"), base_img.convert("RGB"))
            bbox = diff.getbbox()
            if bbox is None:
                results["matched"] += 1
                results["details"].append({"file": current_file.name, "status": "MATCH"})
            else:
                results["diverged"] += 1
                if diff_output_dir:
                    diff_file = diff_output_dir / f"diff_{current_file.name}"
                    diff.save(diff_file)
                results["details"].append({
                    "file": current_file.name,
                    "status": "DIVERGED",
                    "bbox": bbox
                })

    logger.info(
        f"Visual Diff Complete: {results['compared']} compared, "
        f"{results['matched']} matched, {results['diverged']} diverged, "
        f"{results['missing_baseline']} missing baseline."
    )
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BEJSON CMS Publisher, Preview Server & Playwright Screenshot Pipeline"
    )
    parser.add_argument(
        "--cms-root",
        type=Path,
        default=Path("/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS"),
        help="Root path to BEJSON CMS repository"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Preview server port (default: 8000)"
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        default=True,
        help="Launch Android browser via termux-open (default: True)"
    )
    parser.add_argument(
        "--no-browser",
        action="store_false",
        dest="open_browser",
        help="Do not invoke termux-open"
    )
    parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Capture 6 multi-viewport Playwright screenshots into images/"
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=None,
        help="Custom destination directory for screenshots"
    )
    parser.add_argument(
        "--visual-diff",
        action="store_true",
        help="Execute automated visual regression pixel diff against baseline captures"
    )
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        default=None,
        help="Directory containing baseline screenshots for visual regression comparison"
    )
    parser.add_argument(
        "--diff-dir",
        type=Path,
        default=None,
        help="Directory to save visual difference highlight images"
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional BEJSON 104a manifest path to log session"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    cms_root = args.cms_root.resolve()
    if not cms_root.exists():
        logger.error(f"CMS root directory does not exist: {cms_root}")
        sys.exit(1)

    # 1. Execute static site build
    build_ok = execute_publisher_build(cms_root)
    if not build_ok:
        logger.error("Build failed. Terminating pipeline.")
        sys.exit(1)

    build_dir = cms_root / "storage" / "builds"

    # 2. Start preview server
    httpd, srv_thread = start_preview_server(build_dir, args.port)

    # 3. Open browser via termux-open
    browser_opened = False
    if args.open_browser:
        target_url = f"http://localhost:{args.port}/index.html"
        browser_opened = open_termux_browser(target_url)

    # 4. Optional Playwright screenshots
    captured_count = 0
    target_screenshots_dir = args.images_dir or (cms_root / "images")
    if args.screenshots or args.visual_diff:
        logger.info("Executing 6 Playwright screenshot captures...")
        captured_count = asyncio.run(capture_6_screenshots(cms_root, args.port, target_screenshots_dir))
        logger.info(f"Captured {captured_count} screenshots.")

    # 5. Optional Visual Regression Diffing
    diff_summary = None
    if args.visual_diff:
        baseline_path = args.baseline_dir or (cms_root / "images" / "baseline")
        diff_out_path = args.diff_dir or (cms_root / "images" / "diffs")
        diff_summary = perform_visual_regression_diff(
            current_images_dir=target_screenshots_dir,
            baseline_images_dir=baseline_path,
            diff_output_dir=diff_out_path
        )

    # 6. Log manifest
    if args.manifest:
        update_publish_manifest(
            manifest_path=args.manifest,
            record={
                "session_id": f"pub_{int(datetime.now(timezone.utc).timestamp())}",
                "cms_root": str(cms_root),
                "build_dir": str(build_dir),
                "preview_port": args.port,
                "browser_opened": browser_opened,
                "screenshots_captured": captured_count,
                "screenshots_dir": str(target_screenshots_dir),
                "visual_diff": diff_summary,
                "status": "SUCCESS",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

    logger.info(f"Pipeline complete. Server remains active on port {args.port}.")


if __name__ == "__main__":
    main()
