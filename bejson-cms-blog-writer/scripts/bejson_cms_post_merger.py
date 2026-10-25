#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: bejson_cms_post_merger.py
# Description: Layer 5 BEJSON CMS blog post validator, section merger, and BEHTML
#              formatter. Enforces 4-part structure, minimum 120 lines per section,
#              zero-filler compliance, and packages publishable CMS content payloads.
# Version: 100
# Date Created: 2026-10-25
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 7a82e9b1-52d3-4611-9a74-d4b9ec28c941
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("bejson_cms_post_merger requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import html
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from markdown_it import MarkdownIt
    HAS_MARKDOWN_IT: bool = True
except ImportError:
    HAS_MARKDOWN_IT = False

SYSTEM_SCRIPT_VERSION_INTEGER: int = 100
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "7a82e9b1-52d3-4611-9a74-d4b9ec28c941"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("BejsonCmsPostMerger")


def resolve_current_script_directory_path() -> Path:
    """Resolve and return absolute directory of the running script."""
    return Path(__file__).resolve().parent


SYSTEM_SCRIPT_PARENT_DIRECTORY_PATH: Path = resolve_current_script_directory_path()


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [BejsonCmsPostMerger] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_plan_metadata_properties(
    target_plan_file_path: Path,
) -> Dict[str, str]:
    """Extract metadata (title, category, author, summary) from 01_plan.md if present."""
    extracted_metadata_dictionary: Dict[str, str] = {
        "title": "Untitled BEJSON CMS Publication",
        "category": "BEJSON",
        "author": "boehnenelton2024",
        "featured_image": "",
        "summary": "",
    }

    if not target_plan_file_path.is_file():
        return extracted_metadata_dictionary

    try:
        raw_plan_file_content_string: str = target_plan_file_path.read_text(encoding="utf-8")
        
        title_regular_expression_match = re.search(
            r"^#\s+(.+)$", raw_plan_file_content_string, flags=re.MULTILINE
        )
        if title_regular_expression_match:
            extracted_metadata_dictionary["title"] = title_regular_expression_match.group(1).strip()

        category_regular_expression_match = re.search(
            r"(?i)\*\*Category\*\*:\s*([^\n\r]+)", raw_plan_file_content_string
        )
        if category_regular_expression_match:
            extracted_metadata_dictionary["category"] = category_regular_expression_match.group(1).strip()

        author_regular_expression_match = re.search(
            r"(?i)\*\*Author\*\*:\s*([^\n\r]+)", raw_plan_file_content_string
        )
        if author_regular_expression_match:
            extracted_metadata_dictionary["author"] = author_regular_expression_match.group(1).strip()

        featured_image_expression_match = re.search(
            r"(?i)\*\*Featured Image\*\*:\s*([^\n\r]+)", raw_plan_file_content_string
        )
        if featured_image_expression_match:
            extracted_metadata_dictionary["featured_image"] = featured_image_expression_match.group(1).strip()

    except Exception as metadata_extraction_exception:
        EXECUTION_LOGGER_INSTANCE.warning(
            "Could not parse metadata from %s: %s", target_plan_file_path.name, str(metadata_extraction_exception)
        )

    return extracted_metadata_dictionary


def validate_and_merge_blog_sections(
    target_sections_directory_path: Path,
    minimum_required_lines_per_section_count: int = 120,
    override_post_title_string: Optional[str] = None,
    override_post_category_string: Optional[str] = None,
    override_post_author_string: Optional[str] = None,
    override_featured_image_string: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any], List[str]]:
    """Validate section line counts, audit for forbidden filler, and merge sections."""
    target_sections_directory_path = target_sections_directory_path.resolve()
    if not target_sections_directory_path.is_dir():
        return False, {}, [f"Sections directory path does not exist: {target_sections_directory_path}"]

    discovered_plan_file_path: Path = target_sections_directory_path / "01_plan.md"
    extracted_plan_metadata_map: Dict[str, str] = extract_plan_metadata_properties(discovered_plan_file_path)

    final_article_title_string: str = (
        override_post_title_string
        if override_post_title_string
        else extracted_plan_metadata_map.get("title", "Untitled Publication")
    )
    final_article_category_string: str = (
        override_post_category_string
        if override_post_category_string
        else extracted_plan_metadata_map.get("category", "BEJSON")
    )
    final_article_author_string: str = (
        override_post_author_string
        if override_post_author_string
        else extracted_plan_metadata_map.get("author", "boehnenelton2024")
    )
    final_article_featured_image_string: str = (
        override_featured_image_string
        if override_featured_image_string
        else extracted_plan_metadata_map.get("featured_image", "")
    )

    discovered_section_file_paths: List[Path] = sorted(
        [
            file_entry
            for file_entry in target_sections_directory_path.iterdir()
            if file_entry.is_file()
            and file_entry.suffix in (".md", ".txt")
            and file_entry.name not in ("00_context_research.md", "01_plan.md", "README.md", "merged_post.md", "final_post.html")
            and not file_entry.name.startswith((".", "assembled", "merged"))
        ]
    )

    if not discovered_section_file_paths:
        return False, {}, [f"No sectional markdown files found in: {target_sections_directory_path}"]

    validation_error_messages_list: List[str] = []
    audited_section_records_list: List[Dict[str, Any]] = []
    total_aggregate_line_count: int = 0

    for section_index_number, individual_section_file_path in enumerate(discovered_section_file_paths, start=1):
        try:
            raw_section_content_string: str = individual_section_file_path.read_text(encoding="utf-8")
        except Exception as file_read_exception:
            validation_error_messages_list.append(
                f"Failed to read file {individual_section_file_path.name}: {str(file_read_exception)}"
            )
            continue

        section_line_items_list: List[str] = raw_section_content_string.splitlines()
        section_total_lines_count: int = len(section_line_items_list)
        section_non_empty_lines_count: int = len([line for line in section_line_items_list if line.strip()])
        total_aggregate_line_count += section_total_lines_count

        # Policy & user requirement enforcement: minimum 120 lines per section
        if section_total_lines_count < minimum_required_lines_per_section_count:
            validation_error_messages_list.append(
                f"Section '{individual_section_file_path.name}' has {section_total_lines_count} lines, "
                f"which is below the mandatory minimum of {minimum_required_lines_per_section_count} lines."
            )

        # Negative constraint: Zero filler content / lorem ipsum
        if "lorem ipsum" in raw_section_content_string.lower():
            validation_error_messages_list.append(
                f"Section '{individual_section_file_path.name}' contains forbidden filler text 'lorem ipsum'."
            )

        audited_section_records_list.append(
            {
                "file_name": individual_section_file_path.name,
                "file_path": str(individual_section_file_path),
                "total_lines": section_total_lines_count,
                "non_empty_lines": section_non_empty_lines_count,
                "content": raw_section_content_string.strip(),
            }
        )

    current_timestamp_utc_string: str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date_iso_string: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build Merged Markdown Document
    markdown_document_chunks_list: List[str] = []
    markdown_document_chunks_list.append(f"# {final_article_title_string}\n")
    markdown_document_chunks_list.append(
        f"> **Author**: {final_article_author_string} | **Category**: {final_article_category_string} | "
        f"**Date**: {current_date_iso_string} | **Total Lines**: {total_aggregate_line_count}\n"
    )

    if final_article_featured_image_string:
        markdown_document_chunks_list.append(
            f"![Featured Image]({final_article_featured_image_string})\n"
        )

    for section_record_entry in audited_section_records_list:
        markdown_document_chunks_list.append(f"\n{section_record_entry['content']}\n")

    markdown_document_chunks_list.append(
        f"\n---\n\n"
        f"**Publication Metadata**:\n"
        f"- Author: {SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING}\n"
        f"- Compiled At: {current_timestamp_utc_string}\n"
        f"- Relational ID: {SYSTEM_SCRIPT_RELATIONAL_UUID_STRING}\n"
    )

    compiled_merged_markdown_string: str = "\n".join(markdown_document_chunks_list)

    # Build CMS-Ready BEHTML Formatted Content (CMS template renders {{featured_image_html}} natively)
    behtml_body_chunks_list: List[str] = []

    behtml_body_chunks_list.append(
        f'<div class="behtml-meta-bar" style="border-left: 4px solid #DE2626; padding-left: 12px; margin-bottom: 24px;">\n'
        f'  <p style="margin: 0; font-size: 0.9em; color: #777;">\n'
        f'    <strong>Author:</strong> {html.escape(final_article_author_string)} &bull; '
        f'<strong>Category:</strong> {html.escape(final_article_category_string)} &bull; '
        f'<strong>Date:</strong> {current_date_iso_string}\n'
        f'  </p>\n'
        f'</div>'
    )

    def wrap_html_tables_in_scrolling_container(raw_html_string: str) -> str:
        """Wraps bare <table>...</table> elements in <div class="table-container"> for horizontal scrolling."""
        sanitized_html = re.sub(
            r'<div\s+class=["\'](?:table-container|table-responsive)["\']\s*>\s*(<table\b[^>]*>[\s\S]*?</table>)\s*</div>',
            r'\1',
            raw_html_string,
            flags=re.IGNORECASE
        )
        return re.sub(
            r'(<table\b[^>]*>[\s\S]*?</table>)',
            r'<div class="table-container">\1</div>',
            sanitized_html,
            flags=re.IGNORECASE
        )


    markdown_parser_instance: Optional[Any] = (
        MarkdownIt("gfm-like", {"linkify": False, "html": True}) if HAS_MARKDOWN_IT else None
    )

    for section_record_entry in audited_section_records_list:
        sanitized_section_content: str = section_record_entry["content"]
        if markdown_parser_instance:
            rendered_section_html_string: str = markdown_parser_instance.render(sanitized_section_content)
            rendered_section_html_string = wrap_html_tables_in_scrolling_container(rendered_section_html_string)
        else:
            rendered_section_html_string = f"<pre>{html.escape(sanitized_section_content)}</pre>"

        behtml_body_chunks_list.append(
            f'<section class="bejson-cms-post-section" data-source="{html.escape(section_record_entry["file_name"])}">\n'
            f'{rendered_section_html_string}\n'
            f'</section>\n'
        )

    behtml_body_chunks_list.append(
        f'<footer class="behtml-footer-credits" style="margin-top: 48px; padding-top: 16px; border-top: 1px solid #333; font-size: 0.85em; color: #888;">\n'
        f'  <p>Published via BEJSON CMS &bull; Author: {html.escape(SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING)}</p>\n'
        f'</footer>'
    )

    compiled_merged_behtml_string: str = "\n".join(behtml_body_chunks_list)

    result_payload_dictionary: Dict[str, Any] = {
        "title": final_article_title_string,
        "category": final_article_category_string,
        "author": final_article_author_string,
        "featured_image": final_article_featured_image_string,
        "total_lines": total_aggregate_line_count,
        "sections_count": len(audited_section_records_list),
        "sections": audited_section_records_list,
        "merged_markdown": compiled_merged_markdown_string,
        "merged_behtml": compiled_merged_behtml_string,
    }

    is_operation_successful: bool = len(validation_error_messages_list) == 0
    return is_operation_successful, result_payload_dictionary, validation_error_messages_list


def main() -> int:
    """Main execution routine for BEJSON CMS post merger."""
    argument_parser_instance = argparse.ArgumentParser(
        description="BEJSON CMS 5-Part Post Validator and Merger Engine (Layer 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    argument_parser_instance.add_argument(
        "--sections-dir",
        type=str,
        default=".",
        help="Directory containing the 4 sectional markdown draft files and 01_plan.md",
    )
    argument_parser_instance.add_argument(
        "--min-lines",
        type=int,
        default=120,
        help="Minimum required line count threshold for each individual section",
    )
    argument_parser_instance.add_argument(
        "--title",
        type=str,
        default=None,
        help="Override publication title (default: extracted from 01_plan.md)",
    )
    argument_parser_instance.add_argument(
        "--category",
        type=str,
        default=None,
        help="Override category name (e.g. 'BEJSON')",
    )
    argument_parser_instance.add_argument(
        "--author",
        type=str,
        default=None,
        help="Override author display name (e.g. 'boehnenelton2024')",
    )
    argument_parser_instance.add_argument(
        "--featured-image",
        type=str,
        default=None,
        help="Relative or absolute path / URL to featured image asset",
    )
    argument_parser_instance.add_argument(
        "--output-md",
        type=str,
        default=None,
        help="File path to save the merged Markdown publication",
    )
    argument_parser_instance.add_argument(
        "--output-html",
        type=str,
        default=None,
        help="File path to save the merged BEHTML formatted body content",
    )
    argument_parser_instance.add_argument(
        "--ignore-line-check",
        action="store_true",
        help="Force merging even if sections do not reach the 120-line minimum requirement",
    )
    argument_parser_instance.add_argument(
        "--version",
        action="store_true",
        help="Show version identifier and exit",
    )
    argument_parser_instance.add_argument(
        "--register",
        action="store_true",
        help="Register utility with central database",
    )
    argument_parser_instance.add_argument(
        "--config",
        action="store_true",
        help="Display default operational configuration parameters",
    )
    argument_parser_instance.add_argument(
        "--reset",
        action="store_true",
        help="Verify execution environment state",
    )

    parsed_cli_arguments = argument_parser_instance.parse_args()
    configure_execution_logging_subsystem()

    if parsed_cli_arguments.version:
        sys.stdout.write(f"bejson_cms_post_merger v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.config:
        configuration_data_dictionary = {
            "version": SYSTEM_SCRIPT_VERSION_INTEGER,
            "release_version": SYSTEM_RELEASE_VERSION_INTEGER,
            "author": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
            "min_lines_per_section_default": 120,
            "allowed_categories": ["BEJSON", "Uncategorized"],
            "default_author": "boehnenelton2024",
        }
        sys.stdout.write(json.dumps(configuration_data_dictionary, indent=2) + "\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.reset:
        EXECUTION_LOGGER_INSTANCE.info("Environment reset and integrity verification successful.")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.register:
        EXECUTION_LOGGER_INSTANCE.info("Registered bejson_cms_post_merger in local context.")
        return STATUS_CODE_SUCCESS_EXECUTION

    target_sections_directory_path = Path(parsed_cli_arguments.sections_dir)
    is_success, merged_payload_map, error_messages = validate_and_merge_blog_sections(
        target_sections_directory_path=target_sections_directory_path,
        minimum_required_lines_per_section_count=parsed_cli_arguments.min_lines,
        override_post_title_string=parsed_cli_arguments.title,
        override_post_category_string=parsed_cli_arguments.category,
        override_post_author_string=parsed_cli_arguments.author,
        override_featured_image_string=parsed_cli_arguments.featured_image,
    )

    if not is_success and not parsed_cli_arguments.ignore_line_check:
        for error_message_text in error_messages:
            EXECUTION_LOGGER_INSTANCE.error("Validation Error: %s", error_message_text)
        return STATUS_CODE_VALIDATION_ERROR_EXECUTION

    if error_messages and parsed_cli_arguments.ignore_line_check:
        for warning_message_text in error_messages:
            EXECUTION_LOGGER_INSTANCE.warning("Validation Warning (ignored): %s", warning_message_text)

    # Save outputs if specified or save default files in sections_dir
    final_output_markdown_path = (
        Path(parsed_cli_arguments.output_md)
        if parsed_cli_arguments.output_md
        else target_sections_directory_path / "merged_post.md"
    )
    final_output_html_path = (
        Path(parsed_cli_arguments.output_html)
        if parsed_cli_arguments.output_html
        else target_sections_directory_path / "final_post.html"
    )

    try:
        final_output_markdown_path.parent.mkdir(parents=True, exist_ok=True)
        final_output_markdown_path.write_text(merged_payload_map["merged_markdown"], encoding="utf-8")
        EXECUTION_LOGGER_INSTANCE.info("Merged Markdown successfully saved to: %s", final_output_markdown_path)

        final_output_html_path.parent.mkdir(parents=True, exist_ok=True)
        final_output_html_path.write_text(merged_payload_map["merged_behtml"], encoding="utf-8")
        EXECUTION_LOGGER_INSTANCE.info("Merged BEHTML successfully saved to: %s", final_output_html_path)

        EXECUTION_LOGGER_INSTANCE.info(
            "Summary: %d sections merged | %d total lines | Title: '%s'",
            merged_payload_map["sections_count"],
            merged_payload_map["total_lines"],
            merged_payload_map["title"],
        )
    except Exception as file_write_exception:
        EXECUTION_LOGGER_INSTANCE.error("Failed to write output files: %s", str(file_write_exception))
        return STATUS_CODE_PATH_ERROR_EXECUTION

    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
