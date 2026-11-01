#!/usr/bin/env python3
"""
Name: debug_skill_templates.py
Description: Automated Playwright headless browser auditor and Zero-Filler validator for HTML/BEHTML templates.
Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Version: 1.0.0
Date: 2026-10-30
"""

import os
import sys
import re
import argparse
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_NODEJS_PATH"] = "/data/data/com.termux/files/usr/bin/node"
CHROMIUM_PATH = "/data/data/com.termux/files/usr/lib/chromium/chrome"

BANNED_FILLER_PATTERNS = [
    r"\blorem\s+ipsum\b",
    r"\bdolor\s+sit\s+amet\b",
    r"\bconsectetur\s+adipiscing\b",
    r"\bsample\s+text\b",
    r"\bdummy\s+text\b",
    r"\bwelcome\s+to\s+our\s+website\b",
    r"\btestimonials?\b",
    r"\bthe\s+quick\s+brown\s+fox\b",
]

async def run_audit(target_dir: Path, verbose: bool = False):
    if not target_dir.exists():
        print(f"Error: Target directory does not exist: {target_dir}")
        return 1

    html_files = sorted(target_dir.rglob("*.html"))
    total_count = len(html_files)
    print(f"Starting Playwright audit on {total_count} templates under {target_dir}...")

    passed = 0
    failed = 0
    warnings = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--js-flags=--jitless"
            ]
        )
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        for i, file_path in enumerate(html_files, 1):
            rel_name = file_path.relative_to(target_dir)
            filler_detected = []
            
            # 1. Zero-filler validation
            try:
                raw_text = file_path.read_text(encoding="utf-8", errors="ignore")
                for pat in BANNED_FILLER_PATTERNS:
                    found = re.findall(pat, raw_text, re.IGNORECASE)
                    if found:
                        filler_detected.append(found[0])
            except Exception as e:
                filler_detected.append(f"Read error: {e}")

            # 2. Playwright Headless Render Audit
            console_errors = []
            page_errors = []

            def on_console(msg):
                if msg.type == "error":
                    console_errors.append(msg.text)

            def on_pageerror(err):
                page_errors.append(str(err))

            page.on("console", on_console)
            page.on("pageerror", on_pageerror)

            try:
                await page.goto(f"file://{file_path.resolve()}", wait_until="load", timeout=12000)
                await asyncio.sleep(0.05)
            except Exception as e:
                page_errors.append(f"Nav failed: {e}")
            finally:
                page.remove_listener("console", on_console)
                page.remove_listener("pageerror", on_pageerror)

            # Status determination
            if filler_detected or page_errors:
                failed += 1
                status = "FAIL"
            elif console_errors:
                warnings += 1
                status = "WARN"
            else:
                passed += 1
                status = "PASS"

            if verbose or status != "PASS":
                print(f"[{i}/{total_count}] {rel_name} -> {status}")
                if filler_detected:
                    print(f"    - Filler: {filler_detected}")
                if page_errors:
                    print(f"    - Page Errors: {page_errors}")
                if console_errors:
                    print(f"    - Console: {console_errors}")
            elif i % 20 == 0 or i == total_count:
                print(f"[{i}/{total_count}] Progress: {passed} passed, {warnings} warnings, {failed} failed.")

        await browser.close()

    print("\n" + "=" * 60)
    print(f"AUDIT COMPLETE: Total={total_count} | Passed={passed} | Warnings={warnings} | Failed={failed}")
    print("=" * 60)
    return 0 if failed == 0 else 1

def main():
    parser = argparse.ArgumentParser(description="Audit and debug HTML/BEHTML templates with Playwright.")
    parser.add_argument("--dir", default=str(Path.home() / ".gemini" / "config" / "skills"), help="Root directory to audit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output for all files")
    args = parser.parse_args()

    exit_code = asyncio.run(run_audit(Path(args.dir), args.verbose))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
