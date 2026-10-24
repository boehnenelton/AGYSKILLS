#!/data/data/com.termux/files/usr/bin/python3
# ==============================================================================
# Script Name: capture_page.py
# Description: Modular CLI tool to capture screenshots, evaluate JavaScript, and
#              dump rendered HTML from URLs using native Playwright on Termux.
# Version: 1.0.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 57ca60b7-ecbb-4dd1-9e77-8f09886cb138
# ==============================================================================

import argparse
import asyncio
import os
import sys
from pathlib import Path

from termux_playwright import async_playwright_termux, launch

VERSION = "1.0.0"
AUTHOR = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID = "57ca60b7-ecbb-4dd1-9e77-8f09886cb138"

async def capture_target_page(
    target_url: str,
    output_screenshot_path: str | None = None,
    output_html_path: str | None = None,
    viewport_dimensions_pair: tuple[int, int] = (1280, 800),
    is_full_page_screenshot: bool = False,
    timeout_duration_milliseconds: int = 30000,
    http_authentication_username: str | None = None,
    http_authentication_password: str | None = None,
) -> int:
    """Launch headless browser, navigate to URL, and capture screenshot and/or HTML."""
    print(f"[*] Navigating to: {target_url}")
    async with async_playwright_termux() as playwright_instance:
        browser_instance = await launch(playwright_instance, headless=True)
        
        context_options: dict = {
            "viewport": {
                "width": viewport_dimensions_pair[0],
                "height": viewport_dimensions_pair[1]
            },
            "device_scale_factor": 1.0,
        }
        if http_authentication_username and http_authentication_password:
            context_options["http_credentials"] = {
                "username": http_authentication_username,
                "password": http_authentication_password
            }

        browser_context = await browser_instance.new_context(**context_options)
        browser_page = await browser_context.new_page()

        try:
            await browser_page.goto(
                target_url,
                timeout=timeout_duration_milliseconds,
                wait_until="domcontentloaded"
            )
            # Give rendering a brief moment to settle
            await browser_page.wait_for_timeout(1000)

            page_title_string = await browser_page.title()
            print(f"[✓] Page loaded successfully: '{page_title_string}'")

            if output_screenshot_path:
                screenshot_destination = Path(output_screenshot_path)
                screenshot_destination.parent.mkdir(parents=True, exist_ok=True)
                await browser_page.screenshot(
                    path=str(screenshot_destination),
                    full_page=is_full_page_screenshot
                )
                print(f"[✓] Screenshot saved ({screenshot_destination.stat().st_size:,} bytes): {screenshot_destination}")

            if output_html_path:
                html_destination = Path(output_html_path)
                html_destination.parent.mkdir(parents=True, exist_ok=True)
                rendered_markup_content = await browser_page.content()
                html_destination.write_text(rendered_markup_content, encoding="utf-8")
                print(f"[✓] Rendered HTML dumped ({len(rendered_markup_content):,} chars): {html_destination}")

        except Exception as navigation_exception:
            print(f"[✗] Error during navigation: {navigation_exception}", file=sys.stderr)
            await browser_context.close()
            await browser_instance.close()
            return 1

        await browser_context.close()
        await browser_instance.close()
        return 0

def main():
    argument_parser = argparse.ArgumentParser(
        prog="capture_page.py",
        description="Capture screenshots and HTML using native Playwright on Termux."
    )
    argument_parser.add_argument("--url", required=True, help="Target URL to visit")
    argument_parser.add_argument("--output", "-o", help="Output path for PNG screenshot")
    argument_parser.add_argument("--dump-html", help="Output path for rendered HTML DOM dump")
    argument_parser.add_argument("--full-page", action="store_true", help="Capture full page screenshot")
    argument_parser.add_argument("--width", type=int, default=1280, help="Viewport width (default: 1280)")
    argument_parser.add_argument("--height", type=int, default=800, help="Viewport height (default: 800)")
    argument_parser.add_argument("--timeout", type=int, default=30000, help="Navigation timeout in ms")
    argument_parser.add_argument("--user", help="HTTP Basic Auth username")
    argument_parser.add_argument("--password", help="HTTP Basic Auth password")

    parsed_args = argument_parser.parse_args()

    exit_status = asyncio.run(capture_target_page(
        target_url=parsed_args.url,
        output_screenshot_path=parsed_args.output,
        output_html_path=parsed_args.dump_html,
        viewport_dimensions_pair=(parsed_args.width, parsed_args.height),
        is_full_page_screenshot=parsed_args.full_page,
        timeout_duration_milliseconds=parsed_args.timeout,
        http_authentication_username=parsed_args.user,
        http_authentication_password=parsed_args.password,
    ))
    sys.exit(exit_status)

if __name__ == "__main__":
    main()
