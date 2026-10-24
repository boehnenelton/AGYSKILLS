#!/usr/bin/env python3
"""
File:          playwright_capture_runner.py
Description:   Automated Playwright SVG Animation & Canvas Capture Engine.
               Launches headless browser in Android Termux/Linux, loads canvas HTML template,
               waits for window.isReadyToCapture, optionally seeks animation state (window.seekProgress),
               and captures pixel-perfect PNG still frames or frame sequences.
Version:       1.0.0
Date Created:  2026-10-24
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 9c1f2e3d-4a5b-6c7d-8e9f-0a1b2c3d4e5f
"""

import asyncio
import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, List

VERSION = "1.0.0"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app_logger = logging.getLogger("playwright_capture_runner")

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

async def execute_canvas_capture(
    target_html_path: Path,
    output_png_path: Path,
    viewport_width: int = 1280,
    viewport_height: int = 800,
    target_selector: str = "#capture-stage",
    seek_progress_ratio: Optional[float] = None,
    frames_count: int = 1,
    device_scale_factor: int = 2
) -> List[Path]:
    """Automates headless browser capture of fixed-size canvas templates."""
    captured_files_roster: List[Path] = []

    # Import browser runner
    try:
        from termux_playwright import async_playwright_termux, launch
        use_termux_wrapper = True
    except ImportError:
        from playwright.async_api import async_playwright
        use_termux_wrapper = False

    async def run_session(playwright_driver):
        if use_termux_wrapper:
            browser_instance = await launch(playwright_driver, headless=True)
        else:
            browser_instance = await playwright_driver.chromium.launch(headless=True)

        browser_context = await browser_instance.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=device_scale_factor
        )
        browser_page = await browser_context.new_page()

        target_file_url = f"file://{target_html_path.resolve()}"
        app_logger.info(f"Navigating to {target_file_url}")
        await browser_page.goto(target_file_url, wait_until="domcontentloaded")

        # Wait for canvas ready signal
        try:
            await browser_page.wait_for_function("window.isReadyToCapture === true", timeout=5000)
        except Exception:
            app_logger.warning("Timeout waiting for window.isReadyToCapture. Proceeding after fallback delay.")
            await browser_page.wait_for_timeout(1000)

        # Locate target stage
        stage_element = await browser_page.query_selector(target_selector)
        if not stage_element:
            app_logger.warning(f"Selector {target_selector} not found; capturing full page.")
            capture_target = browser_page
        else:
            capture_target = stage_element

        output_png_path.parent.mkdir(parents=True, exist_ok=True)

        if frames_count <= 1:
            if seek_progress_ratio is not None:
                app_logger.info(f"Seeking animation progress to {seek_progress_ratio:.2f}")
                await browser_page.evaluate(f"window.seekProgress && window.seekProgress({seek_progress_ratio})")
                await browser_page.wait_for_timeout(100)

            await capture_target.screenshot(path=str(output_png_path))
            captured_files_roster.append(output_png_path)
            app_logger.info(f"Saved snapshot to {output_png_path} ({output_png_path.stat().st_size} bytes)")
        else:
            # Multi-frame sequence
            stem_name = output_png_path.stem
            parent_dir = output_png_path.parent
            for frame_index in range(frames_count):
                progress = frame_index / float(frames_count)
                await browser_page.evaluate(f"window.seekProgress && window.seekProgress({progress})")
                await browser_page.wait_for_timeout(100)
                frame_path = parent_dir / f"{stem_name}_frame_{frame_index:03d}.png"
                await capture_target.screenshot(path=str(frame_path))
                captured_files_roster.append(frame_path)
            app_logger.info(f"Saved {frames_count} animation frames to {parent_dir}")

        await browser_instance.close()

    if use_termux_wrapper:
        async with async_playwright_termux() as playwright_instance:
            await run_session(playwright_instance)
    else:
        async with async_playwright() as playwright_instance:
            await run_session(playwright_instance)

    return captured_files_roster

def build_argument_parser() -> argparse.ArgumentParser:
    cli_parser = argparse.ArgumentParser(
        description="Playwright Canvas Capture Runner — Automated SVG Animation & Template Screenshots"
    )
    cli_parser.add_argument("--html", type=str, required=True, help="Path to canvas HTML template file")
    cli_parser.add_argument("--output", type=str, required=True, help="Destination path for output PNG image")
    cli_parser.add_argument("--width", type=int, default=1280, help="Browser viewport width (default: 1280)")
    cli_parser.add_argument("--height", type=int, default=800, help="Browser viewport height (default: 800)")
    cli_parser.add_argument("--selector", type=str, default="#capture-stage", help="CSS selector of stage container (default: #capture-stage)")
    cli_parser.add_argument("--seek", type=float, default=None, help="Animation progress ratio to seek (0.0 to 1.0)")
    cli_parser.add_argument("--frames", type=int, default=1, help="Number of sequential animation frames to capture")
    cli_parser.add_argument("--version", action="version", version=f"playwright_capture_runner v{VERSION}")
    return cli_parser

def main() -> int:
    cli_parser = build_argument_parser()
    cli_arguments = cli_parser.parse_args()

    target_html_path = Path(cli_arguments.html).resolve()
    if not target_html_path.exists():
        app_logger.error(f"HTML template not found: {target_html_path}")
        return 10

    output_png_path = Path(cli_arguments.output).resolve()

    try:
        captured_files = asyncio.run(execute_canvas_capture(
            target_html_path=target_html_path,
            output_png_path=output_png_path,
            viewport_width=cli_arguments.width,
            viewport_height=cli_arguments.height,
            target_selector=cli_arguments.selector,
            seek_progress_ratio=cli_arguments.seek,
            frames_count=cli_arguments.frames
        ))
        app_logger.info(f"Capture run successful. {len(captured_files)} file(s) produced.")
        return 0
    except Exception as runtime_error:
        app_logger.error(f"Capture execution failed: {runtime_error}")
        return 10

if __name__ == "__main__":
    sys.exit(main())
