#!/data/data/com.termux/files/usr/bin/python3
# ==============================================================================
# Script Name: readme_embed_pipeline.py
# Description: Automated pipeline that captures web views via native Playwright,
#              resizes images to 420p maintaining aspect ratio, stages them in the
#              project's images/ subfolder, and evenly embeds them into README.md.
# Version: 1.2.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 9848c778-11e0-4189-94c8-803e6018fc4b
# ==============================================================================

import argparse
import asyncio
import logging
import os
import shutil
import sys
from pathlib import Path

from PIL import Image
from termux_playwright import async_playwright_termux, launch

VERSION = "1.2.0"
AUTHOR = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID = "9848c778-11e0-4189-94c8-803e6018fc4b"

pipeline_logger = logging.getLogger("readme_embed_pipeline")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def downscale_image_aspect_ratio_420p(
    source_file_path: Path,
    destination_file_path: Path,
    target_maximum_dimension_pixels: int = 420
) -> Path:
    """Downscale image so that max(width, height) is 420px while strictly maintaining aspect ratio."""
    with Image.open(source_file_path) as source_image_handle:
        original_width_pixels, original_height_pixels = source_image_handle.size
        highest_source_dimension_pixels = max(original_width_pixels, original_height_pixels)

        if highest_source_dimension_pixels == target_maximum_dimension_pixels:
            scaled_width_pixels, scaled_height_pixels = original_width_pixels, original_height_pixels
            output_image_handle = source_image_handle
        else:
            scaling_ratio_factor = float(target_maximum_dimension_pixels) / float(highest_source_dimension_pixels)
            scaled_width_pixels = int(round(original_width_pixels * scaling_ratio_factor))
            scaled_height_pixels = int(round(original_height_pixels * scaling_ratio_factor))
            output_image_handle = source_image_handle.resize(
                (scaled_width_pixels, scaled_height_pixels),
                Image.Resampling.LANCZOS
            )

        destination_file_path.parent.mkdir(parents=True, exist_ok=True)
        destination_image_format = source_image_handle.format or destination_file_path.suffix.lstrip(".").upper()
        if destination_image_format == "JPG":
            destination_image_format = "JPEG"

        output_image_handle.save(destination_file_path, format=destination_image_format, optimize=True)
        pipeline_logger.info(
            "420p Aspect Scaled: %s -> %dx%d (%d bytes)",
            source_file_path.name,
            scaled_width_pixels,
            scaled_height_pixels,
            destination_file_path.stat().st_size
        )
        return destination_file_path

async def capture_target_views_playwright(
    target_view_definitions: list[dict],
    staging_directory_path: Path,
    http_authentication_credentials: tuple[str, str] | None = None
) -> list[tuple[Path, str]]:
    """Capture screenshots for a list of URLs using native Playwright on Termux."""
    staging_directory_path.mkdir(parents=True, exist_ok=True)
    captured_image_entries = []

    pipeline_logger.info("Launching native Playwright browser in Termux...")
    async with async_playwright_termux() as playwright_instance:
        browser_instance = await launch(playwright_instance, headless=True)
        
        browser_context_arguments: dict = {
            "viewport": {"width": 1280, "height": 800},
            "device_scale_factor": 1.0
        }
        if http_authentication_credentials:
            browser_context_arguments["http_credentials"] = {
                "username": http_authentication_credentials[0],
                "password": http_authentication_credentials[1]
            }

        browser_context = await browser_instance.new_context(**browser_context_arguments)
        browser_page = await browser_context.new_page()

        for view_index, view_definition_item in enumerate(target_view_definitions, start=1):
            target_view_url = view_definition_item["url"]
            output_filename = view_definition_item.get("filename", f"screenshot_{view_index:02d}.png")
            caption_description = view_definition_item.get("caption", f"Figure {view_index}: View of {target_view_url}")
            destination_screenshot_path = staging_directory_path / output_filename

            pipeline_logger.info(
                "[%d/%d] Navigating to %s...",
                view_index, len(target_view_definitions), target_view_url
            )
            await browser_page.goto(target_view_url, timeout=35000, wait_until="domcontentloaded")
            await browser_page.wait_for_timeout(1000)
            await browser_page.screenshot(path=str(destination_screenshot_path))
            captured_image_entries.append((destination_screenshot_path, caption_description))

        await browser_context.close()
        await browser_instance.close()

    return captured_image_entries

def embed_images_evenly_in_markdown(
    readme_markdown_file_path: Path,
    image_entries_collection: list[tuple[str, str]],
    output_markdown_file_path: Path | None = None
) -> int:
    """Calculate total line count of README, divide by image count, and evenly embed images."""
    if not readme_markdown_file_path.exists():
        pipeline_logger.error("Target README file does not exist: %s", readme_markdown_file_path)
        return 1

    readme_source_text = readme_markdown_file_path.read_text(encoding="utf-8")
    original_document_lines = readme_source_text.splitlines()
    total_document_line_count = len(original_document_lines)
    total_image_count = len(image_entries_collection)

    if total_image_count == 0:
        pipeline_logger.warning("No images provided for embedding.")
        return 0

    computed_line_interval = max(1, total_document_line_count // total_image_count)
    pipeline_logger.info(
        "Line interval calculated: %d lines per image across %d total lines for %d images.",
        computed_line_interval, total_document_line_count, total_image_count
    )

    # Clean existing embedded image figures to prevent duplicate stacking
    cleaned_document_lines = []
    for current_existing_line in original_document_lines:
        if any(image_tuple[0] in current_existing_line for image_tuple in image_entries_collection):
            continue
        cleaned_document_lines.append(current_existing_line)

    total_cleaned_line_count = len(cleaned_document_lines)
    adjusted_line_interval = max(1, total_cleaned_line_count // total_image_count)

    result_document_lines = []
    current_image_index = 0
    lines_since_last_embed = 0

    for line_index_position, current_content_line in enumerate(cleaned_document_lines):
        result_document_lines.append(current_content_line)
        lines_since_last_embed += 1

        if current_image_index < total_image_count:
            is_line_interval_reached = lines_since_last_embed >= adjusted_line_interval
            is_safe_markdown_boundary = (
                current_content_line == "" or
                current_content_line.startswith("---") or
                line_index_position == total_cleaned_line_count - 1
            )
            if is_line_interval_reached and is_safe_markdown_boundary:
                relative_image_path, figure_caption_title = image_entries_collection[current_image_index]
                image_markup_block = [
                    "",
                    f"![{figure_caption_title}]({relative_image_path})",
                    f"*_{figure_caption_title}_*",
                    ""
                ]
                result_document_lines.extend(image_markup_block)
                pipeline_logger.info(
                    "Embedded image %d at line %d: %s",
                    current_image_index + 1, len(result_document_lines), relative_image_path
                )
                current_image_index += 1
                lines_since_last_embed = 0

    while current_image_index < total_image_count:
        relative_image_path, figure_caption_title = image_entries_collection[current_image_index]
        image_markup_block = [
            "",
            f"![{figure_caption_title}]({relative_image_path})",
            f"*_{figure_caption_title}_*",
            ""
        ]
        result_document_lines.extend(image_markup_block)
        pipeline_logger.info(
            "Appended image %d at line %d: %s",
            current_image_index + 1, len(result_document_lines), relative_image_path
        )
        current_image_index += 1

    destination_output_file_path = output_markdown_file_path or readme_markdown_file_path
    destination_output_file_path.write_text("\n".join(result_document_lines) + "\n", encoding="utf-8")
    pipeline_logger.info("README updated (%d total lines): %s", len(result_document_lines), destination_output_file_path)
    return 0

def main():
    command_line_parser = argparse.ArgumentParser(
        prog="readme_embed_pipeline.py",
        description="Capture views via Playwright, scale to 420p maintaining aspect ratio, and evenly embed into README.md."
    )
    command_line_parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    command_line_parser.add_argument("--readme", required=True, help="Path to project README.md")
    command_line_parser.add_argument("--images-dir", required=True, help="Target images/ folder relative to project root")
    command_line_parser.add_argument("--source-images", help="Directory of existing source screenshots to scale and embed")
    command_line_parser.add_argument(
        "--max-dim", "--target-dimension",
        dest="max_dim",
        type=int,
        default=420,
        help="Maximum highest dimension in pixels (default: 420)"
    )

    parsed_arguments = command_line_parser.parse_args()

    resolved_readme_path = Path(parsed_arguments.readme).resolve()
    resolved_target_images_directory = Path(parsed_arguments.images_dir).resolve()
    resolved_target_images_directory.mkdir(parents=True, exist_ok=True)

    if parsed_arguments.source_images:
        resolved_source_directory = Path(parsed_arguments.source_images).resolve()
        source_image_files = sorted([
            file_entry for file_entry in resolved_source_directory.iterdir()
            if file_entry.is_file() and file_entry.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ])
        
        staged_figure_entries = []
        for current_source_file in source_image_files:
            target_scaled_destination = resolved_target_images_directory / current_source_file.name
            downscale_image_aspect_ratio_420p(current_source_file, target_scaled_destination, parsed_arguments.max_dim)
            relative_image_path = os.path.relpath(target_scaled_destination, resolved_readme_path.parent)
            cleaned_figure_caption = f"Figure: {current_source_file.stem.replace('_', ' ').title()}"
            staged_figure_entries.append((relative_image_path, cleaned_figure_caption))

        embed_images_evenly_in_markdown(resolved_readme_path, staged_figure_entries)
    else:
        pipeline_logger.warning("No source images specified. Use --source-images <dir> to process.")

if __name__ == "__main__":
    main()
