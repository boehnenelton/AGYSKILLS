#!/usr/bin/env python3
"""
Name: Visual_Diff_Auditor
Description: Layer 5 multi-viewport screenshot capture and Policy 8.1 Tri-Color visual regression auditor.
Version: 1.0.0
Date Created: 2026-10-23
Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 102b6b50-0c49-413e-a8d8-fc1bcf7dd94d
"""

import argparse
import asyncio
import datetime
import json
import logging
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.0.0"

# Self-locating preamble adhering to Policy 4.1
def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()

# Optional core debugger import
CORE_DEBUGGER_PATH = Path.home() / "downloads" / "Playwright_Debugger"
if CORE_DEBUGGER_PATH.exists():
    sys.path.insert(0, str(CORE_DEBUGGER_PATH))
    from lib.server_manager import LocalHttpServerManager

from termux_playwright import async_playwright_termux, launch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Visual_Diff_Auditor")

VIEWPORT_PROFILES_ROSTER = [
    {"profile_name_key": "mobile_360x640", "viewport_width_px": 360, "viewport_height_px": 640, "is_mobile_device_flag": True},
    {"profile_name_key": "tablet_768x1024", "viewport_width_px": 768, "viewport_height_px": 1024, "is_mobile_device_flag": True},
    {"profile_name_key": "desktop_1280x720", "viewport_width_px": 1280, "viewport_height_px": 720, "is_mobile_device_flag": False},
]


class ViewportVisualAuditResult:
    """Stores telemetry for a single viewport visual audit."""

    def __init__(self, viewport_profile_identifier: str) -> None:
        self.viewport_profile_identifier = viewport_profile_identifier
        self.rendered_screenshot_path: str = ""
        self.tri_color_compliance_percentage: float = 0.0
        self.total_pixels_evaluated_count: int = 0
        self.conforming_pixels_count: int = 0
        self.non_conforming_pixels_count: int = 0
        self.dominant_color_hex_codes: List[str] = []
        self.layout_overflow_detected_flag: bool = False


async def probe_viewport_visual_compliance(
    browser_process_instance: Any,
    target_navigation_url: str,
    viewport_profile_record: Dict[str, Any],
    output_screenshots_directory: Path,
) -> ViewportVisualAuditResult:
    profile_identifier = viewport_profile_record["profile_name_key"]
    viewport_width_dimension = viewport_profile_record["viewport_width_px"]
    viewport_height_dimension = viewport_profile_record["viewport_height_px"]
    is_mobile_mode = viewport_profile_record["is_mobile_device_flag"]

    audit_result_container = ViewportVisualAuditResult(profile_identifier)

    browser_page_context = await browser_process_instance.new_page(
        viewport={"width": viewport_width_dimension, "height": viewport_height_dimension},
        is_mobile=is_mobile_mode,
        user_agent="Mozilla/5.0 (Linux; Android 14; Termux Visual Auditor) AppleWebKit/537.36 Chrome/130.0 Mobile Safari/537.36",
    )

    try:
        await browser_page_context.goto(target_navigation_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(0.5)

        # 1. Take Screenshot
        screenshot_target_filename = f"viewport_{profile_identifier}.png"
        screenshot_full_output_path = output_screenshots_directory / screenshot_target_filename
        await browser_page_context.screenshot(path=str(screenshot_full_output_path), full_page=False)
        audit_result_container.rendered_screenshot_path = str(screenshot_full_output_path)

        # 2. In-Browser Pixel & Layout Analysis for Policy 8.1 Tri-Color Conformance
        evaluation_payload = await browser_page_context.evaluate(
            """
            () => {
                const doc_width = document.documentElement.scrollWidth;
                const win_width = window.innerWidth;
                const has_horizontal_overflow = doc_width > win_width + 2;

                // Sample computed styles across representative elements
                const sampled_elements = Array.from(document.querySelectorAll('*')).slice(0, 500);
                let compliant_color_samples = 0;
                let non_compliant_color_samples = 0;
                const discovered_color_histogram = {};

                function is_tri_color_compliant(rgb_string) {
                    if (!rgb_string || rgb_string === 'transparent' || rgb_string === 'rgba(0, 0, 0, 0)') return true;
                    const match = rgb_string.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
                    if (!match) return false;
                    const r = parseInt(match[1]);
                    const g = parseInt(match[2]);
                    const b = parseInt(match[3]);

                    // Distance to White (255, 255, 255)
                    const d_white = Math.sqrt((r-255)**2 + (g-255)**2 + (b-255)**2);
                    // Distance to Black (0, 0, 0)
                    const d_black = Math.sqrt(r**2 + g**2 + b**2);
                    // Distance to Policy 8.1 Red (#DE2626 -> 222, 38, 38)
                    const d_red = Math.sqrt((r-222)**2 + (g-38)**2 + (b-38)**2);

                    return (d_white <= 15 || d_black <= 15 || d_red <= 20);
                }

                sampled_elements.forEach(node => {
                    const style = window.getComputedStyle(node);
                    const bg_color = style.backgroundColor;
                    const text_color = style.color;
                    const border_color = style.borderColor;

                    [bg_color, text_color, border_color].forEach(color_val => {
                        if (color_val && color_val !== 'rgba(0, 0, 0, 0)' && color_val !== 'transparent') {
                            discovered_color_histogram[color_val] = (discovered_color_histogram[color_val] || 0) + 1;
                            if (is_tri_color_compliant(color_val)) {
                                compliant_color_samples++;
                            } else {
                                non_compliant_color_samples++;
                            }
                        }
                    });
                });

                const total_samples = compliant_color_samples + non_compliant_color_samples;
                const compliance_ratio = total_samples > 0 ? (compliant_color_samples / total_samples) * 100.0 : 100.0;

                // Sort top colors
                const sorted_colors = Object.keys(discovered_color_histogram).sort((a,b) => discovered_color_histogram[b] - discovered_color_histogram[a]);

                return {
                    "horizontal_overflow": has_horizontal_overflow,
                    "total_samples": total_samples,
                    "compliant_samples": compliant_color_samples,
                    "non_compliant_samples": non_compliant_color_samples,
                    "compliance_percentage": compliance_ratio,
                    "top_colors": sorted_colors.slice(0, 5)
                };
            }
            """
        )

        audit_result_container.layout_overflow_detected_flag = evaluation_payload.get("horizontal_overflow", False)
        audit_result_container.total_pixels_evaluated_count = evaluation_payload.get("total_samples", 0)
        audit_result_container.conforming_pixels_count = evaluation_payload.get("compliant_samples", 0)
        audit_result_container.non_conforming_pixels_count = evaluation_payload.get("non_compliant_samples", 0)
        audit_result_container.tri_color_compliance_percentage = evaluation_payload.get("compliance_percentage", 100.0)
        audit_result_container.dominant_color_hex_codes = evaluation_payload.get("top_colors", [])

    finally:
        await browser_page_context.close()

    return audit_result_container


async def run_visual_testing_suite(
    target_path_input: str,
    output_directory_path: Path,
    override_port: int = 8092,
) -> int:
    target_path = Path(target_path_input).resolve()
    if not target_path.exists():
        logger.error("Target path does not exist: %s", target_path)
        return 30

    output_screenshots_dir = output_directory_path / "screenshots"
    output_reports_dir = output_directory_path / "reports"
    output_screenshots_dir.mkdir(parents=True, exist_ok=True)
    output_reports_dir.mkdir(parents=True, exist_ok=True)

    server_instance: Optional[Any] = None
    target_url: str = ""

    if target_path.is_file() and target_path.suffix == ".html":
        server_root = target_path.parent
        if "LocalHttpServerManager" in globals():
            server_instance = LocalHttpServerManager(target_serving_directory=str(server_root), preferred_server_port=override_port)
            bound_port = server_instance.start_local_server()
            target_url = f"http://127.0.0.1:{bound_port}/{target_path.name}"
        else:
            target_url = f"file://{target_path}"
    elif target_path.is_dir():
        server_root = target_path
        candidate_entry = target_path / "index.html"
        if not candidate_entry.exists():
            candidate_entry = target_path / "play.html"
        if "LocalHttpServerManager" in globals():
            server_instance = LocalHttpServerManager(target_serving_directory=str(server_root), preferred_server_port=override_port)
            bound_port = server_instance.start_local_server()
            relative_entry = candidate_entry.relative_to(server_root).as_posix() if candidate_entry.exists() else ""
            target_url = f"http://127.0.0.1:{bound_port}/{relative_entry}"
        else:
            target_url = f"file://{candidate_entry}"
    else:
        target_url = target_path_input

    logger.info("Executing visual testing on target: %s", target_url)

    viewport_results_collection: List[ViewportVisualAuditResult] = []

    try:
        async with async_playwright_termux() as playwright_environment_instance:
            browser_process = await launch(playwright_environment_instance, headless=True)

            for profile_item in VIEWPORT_PROFILES_ROSTER:
                logger.info("Evaluating viewport profile: %s", profile_item["profile_name_key"])
                audit_record = await probe_viewport_visual_compliance(
                    browser_process_instance=browser_process,
                    target_navigation_url=target_url,
                    viewport_profile_record=profile_item,
                    output_screenshots_directory=output_screenshots_dir,
                )
                viewport_results_collection.append(audit_record)

            await browser_process.close()

    finally:
        if server_instance is not None:
            server_instance.stop_local_server()

    # Output Terminal Summary
    print("\n" + "=" * 65)
    print("PLAYWRIGHT VISUAL TESTING — POLICY 8.1 TRI-COLOR AUDIT")
    print("=" * 65)
    print(f"Target URL: {target_url}")
    print("-" * 65)

    has_critical_failure = False
    for res in viewport_results_collection:
        compliance_label = "PASS" if res.tri_color_compliance_percentage >= 90.0 else ("WARN" if res.tri_color_compliance_percentage >= 75.0 else "FAIL")
        if compliance_label == "FAIL":
            has_critical_failure = True
        print(f"Viewport: {res.viewport_profile_identifier:<18} | Tri-Color: {res.tri_color_compliance_percentage:5.1f}% [{compliance_label}] | Overflow: {res.layout_overflow_detected_flag}")
        print(f"  Screenshot: {res.rendered_screenshot_path}")
        print(f"  Top Colors: {', '.join(res.dominant_color_hex_codes[:3])}")

    print("=" * 65 + "\n")

    return 20 if has_critical_failure else 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="visual_diff_auditor.py", description="Playwright L5 visual regression & Policy 8.1 tri-color auditor.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("target", type=str, help="Target URL, HTML file, or project folder")
    parser.add_argument("--output", type=str, default=str(SCRIPT_PATH.parent / "exports"), help="Output directory for visual artifacts")

    args = parser.parse_args()
    exit_code = asyncio.run(run_visual_testing_suite(target_path_input=args.target, output_directory_path=Path(args.output)))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
