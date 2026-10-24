#!/data/data/com.termux/files/usr/bin/python3
# ==============================================================================
# Script Name: resize_420p.py
# Description: CLI utility to resize images so that the maximum of the highest dimension
#              is 420px while strictly maintaining original aspect ratio.
# Version: 1.2.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 0f20d4da-9d57-49d6-b567-0100e3fd891b
# ==============================================================================

import argparse
import logging
import os
import sys
from pathlib import Path
from PIL import Image

VERSION = "1.2.0"
AUTHOR = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID = "0f20d4da-9d57-49d6-b567-0100e3fd891b"

logger_instance = logging.getLogger("resize_420p")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

def calculate_scaled_proportional_dimensions(
    source_width_pixels: int,
    source_height_pixels: int,
    target_maximum_dimension_pixels: int = 420
) -> tuple[int, int]:
    """Calculate scaled dimensions so that max(width, height) equals target maximum while strictly preserving aspect ratio."""
    if source_height_pixels <= 0 or source_width_pixels <= 0:
        raise ValueError(f"Invalid image dimensions: {source_width_pixels}x{source_height_pixels}")

    highest_source_dimension_pixels = max(source_width_pixels, source_height_pixels)
    if highest_source_dimension_pixels == target_maximum_dimension_pixels:
        return (source_width_pixels, source_height_pixels)

    scaling_ratio_factor = float(target_maximum_dimension_pixels) / float(highest_source_dimension_pixels)
    scaled_width_pixels = int(round(source_width_pixels * scaling_ratio_factor))
    scaled_height_pixels = int(round(source_height_pixels * scaling_ratio_factor))
    return (scaled_width_pixels, scaled_height_pixels)

def process_single_image_file(
    source_image_file_path: Path,
    destination_image_file_path: Path,
    target_maximum_dimension_pixels: int = 420,
    optimize_output_flag: bool = True
) -> bool:
    """Resize an individual image so its highest dimension is 420px max, preserving aspect ratio."""
    try:
        with Image.open(source_image_file_path) as source_image_handle:
            original_image_width, original_image_height = source_image_handle.size
            highest_source_dimension = max(original_image_width, original_image_height)

            if highest_source_dimension == target_maximum_dimension_pixels:
                logger_instance.info("Image highest dimension already at %dpx: %s", target_maximum_dimension_pixels, source_image_file_path.name)
                scaled_width_pixels, scaled_height_pixels = original_image_width, original_image_height
                output_image_handle = source_image_handle
            else:
                scaled_width_pixels, scaled_height_pixels = calculate_scaled_proportional_dimensions(
                    original_image_width, original_image_height, target_maximum_dimension_pixels
                )
                logger_instance.info(
                    "Resizing %s: %dx%d -> %dx%d (Max Dimension: %dpx)",
                    source_image_file_path.name,
                    original_image_width, original_image_height,
                    scaled_width_pixels, scaled_height_pixels,
                    target_maximum_dimension_pixels
                )
                output_image_handle = source_image_handle.resize(
                    (scaled_width_pixels, scaled_height_pixels),
                    Image.Resampling.LANCZOS
                )

            destination_image_file_path.parent.mkdir(parents=True, exist_ok=True)
            output_image_format = output_image_handle.format or destination_image_file_path.suffix.lstrip(".").upper()
            if output_image_format == "JPG":
                output_image_format = "JPEG"

            save_options_dictionary: dict = {"optimize": optimize_output_flag}
            if output_image_format == "JPEG":
                save_options_dictionary["quality"] = 85
            elif output_image_format == "PNG":
                save_options_dictionary["compress_level"] = 9

            output_image_handle.save(destination_image_file_path, format=output_image_format, **save_options_dictionary)
            destination_file_size_bytes = destination_image_file_path.stat().st_size
            logger_instance.info(
                "Saved 420p image (%dx%d, %d bytes): %s",
                scaled_width_pixels, scaled_height_pixels, destination_file_size_bytes, destination_image_file_path
            )
            return True
    except Exception as processing_error_exception:
        logger_instance.error("Failed to process image %s: %s", source_image_file_path, processing_error_exception)
        return False

def execute_batch_image_resizing(
    source_target_path: Path,
    destination_directory_path: Path,
    target_maximum_dimension_pixels: int = 420
) -> int:
    """Process a single file or an entire directory of images."""
    if source_target_path.is_file():
        target_destination_file = (
            destination_directory_path / source_target_path.name
            if destination_directory_path.is_dir()
            else destination_directory_path
        )
        operation_success = process_single_image_file(
            source_target_path, target_destination_file, target_maximum_dimension_pixels
        )
        return 0 if operation_success else 1

    if source_target_path.is_dir():
        image_files_collection = [
            file_entry for file_entry in source_target_path.iterdir()
            if file_entry.is_file() and file_entry.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ]
        if not image_files_collection:
            logger_instance.warning("No supported image files found in %s", source_target_path)
            return 0

        successful_processing_count = 0
        for current_image_file in sorted(image_files_collection):
            target_destination_file = destination_directory_path / current_image_file.name
            if process_single_image_file(current_image_file, target_destination_file, target_maximum_dimension_pixels):
                successful_processing_count += 1

        logger_instance.info(
            "Batch processing complete: %d/%d images scaled to %dpx max dimension.",
            successful_processing_count, len(image_files_collection), target_maximum_dimension_pixels
        )
        return 0 if successful_processing_count == len(image_files_collection) else 1

    logger_instance.error("Source path does not exist: %s", source_target_path)
    return 1

def main():
    command_line_parser = argparse.ArgumentParser(
        prog="resize_420p.py",
        description="Downscale images so that the highest dimension is 420px max while strictly preserving aspect ratio."
    )
    command_line_parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    command_line_parser.add_argument("--input", "-i", required=True, help="Input image file or directory")
    command_line_parser.add_argument("--output", "-o", required=True, help="Output image file or directory")
    command_line_parser.add_argument(
        "--max-dim", "--dimension", "-m",
        dest="max_dim",
        type=int,
        default=420,
        help="Maximum highest dimension in pixels (default: 420)"
    )

    parsed_command_arguments = command_line_parser.parse_args()

    resolved_input_path = Path(parsed_command_arguments.input).resolve()
    resolved_output_path = Path(parsed_command_arguments.output).resolve()

    exit_status_code = execute_batch_image_resizing(
        resolved_input_path, resolved_output_path, parsed_command_arguments.max_dim
    )
    sys.exit(exit_status_code)

if __name__ == "__main__":
    main()
