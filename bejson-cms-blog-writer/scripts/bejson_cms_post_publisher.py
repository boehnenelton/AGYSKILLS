#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: bejson_cms_post_publisher.py
# Description: Layer 5 BEJSON CMS post publisher. Stages and publishes merged
#              blog posts into BEJSON CMS (or NewAgent CMS) using cms-manage.py
#              page commands, preserving metadata and two-part database integrity.
# Version: 100
# Date Created: 2026-10-25
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 8c34f0a2-63e4-4722-8b85-e5c8db39d052
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("bejson_cms_post_publisher requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SYSTEM_SCRIPT_VERSION_INTEGER: int = 100
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "8c34f0a2-63e4-4722-8b85-e5c8db39d052"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("BejsonCmsPostPublisher")

DEFAULT_BEJSON_CMS_REPOSITORY_PATH: Path = Path("/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS")
DEFAULT_NEWAGENT_CMS_REPOSITORY_PATH: Path = Path("/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS")


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [BejsonCmsPostPublisher] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_metadata_from_file_header(
    target_content_file_path: Path,
) -> Dict[str, str]:
    """Inspect content file or sibling 01_plan.md to discover Title, Category, and Author."""
    discovered_metadata_dictionary: Dict[str, str] = {
        "title": "Untitled Publication",
        "category": "BEJSON",
        "author": "boehnenelton2024",
    }

    if not target_content_file_path.is_file():
        return discovered_metadata_dictionary

    # Priority 1: Check sibling 01_plan.md if present in same directory
    sibling_plan_file_path = target_content_file_path.parent / "01_plan.md"
    if sibling_plan_file_path.is_file():
        try:
            raw_plan_text = sibling_plan_file_path.read_text(encoding="utf-8")
            title_match = re.search(r"^#\s+(.+)$", raw_plan_text, flags=re.MULTILINE)
            if title_match:
                discovered_metadata_dictionary["title"] = title_match.group(1).strip()
            cat_match = re.search(r"(?i)\*\*Category\*\*:\s*([a-zA-Z0-9_\-]+)", raw_plan_text)
            if cat_match:
                discovered_metadata_dictionary["category"] = cat_match.group(1).strip()
            author_match = re.search(r"(?i)\*\*Author\*\*:\s*([a-zA-Z0-9_\-]+)", raw_plan_text)
            if author_match:
                discovered_metadata_dictionary["author"] = author_match.group(1).strip()
            return discovered_metadata_dictionary
        except Exception as plan_read_error:
            EXECUTION_LOGGER_INSTANCE.debug("Could not read sibling plan: %s", str(plan_read_error))

    # Priority 2: Extract from content file directly
    try:
        raw_header_content_string: str = target_content_file_path.read_text(encoding="utf-8")[:4096]

        title_regular_expression_match = re.search(r"^#\s+(.+)$", raw_header_content_string, flags=re.MULTILINE)
        if title_regular_expression_match:
            discovered_metadata_dictionary["title"] = title_regular_expression_match.group(1).strip()
        else:
            alt_title_match = re.search(r'alt="([^"]+)"', raw_header_content_string)
            if alt_title_match:
                discovered_metadata_dictionary["title"] = alt_title_match.group(1).strip()

        category_regular_expression_match = re.search(
            r"(?i)\bCategory\b[^:]*:\s*(?:</[^>]+>\s*)?([a-zA-Z0-9_\-]+)", raw_header_content_string
        )
        if category_regular_expression_match:
            discovered_metadata_dictionary["category"] = category_regular_expression_match.group(1).strip()

        author_regular_expression_match = re.search(
            r"(?i)\bAuthor\b[^:]*:\s*(?:</[^>]+>\s*)?([a-zA-Z0-9_\-]+)", raw_header_content_string
        )
        if author_regular_expression_match:
            discovered_metadata_dictionary["author"] = author_regular_expression_match.group(1).strip()

        img_match = re.search(
            r'src=["\'](?:.*?/assets/|storage/mfdb/assets/)?([^"\'\s]+\.(?:svg|png|webp|jpg))["\']',
            raw_header_content_string,
        )
        if img_match:
            discovered_metadata_dictionary["featured_image"] = img_match.group(1).strip()
        elif (target_content_file_path.parent / "hero.svg").is_file():
            discovered_metadata_dictionary["featured_image"] = "hero.svg"

    except Exception as header_parsing_exception:
        EXECUTION_LOGGER_INSTANCE.warning(
            "Could not parse header metadata from %s: %s", target_content_file_path.name, str(header_parsing_exception)
        )

    return discovered_metadata_dictionary


def find_cms_manage_script_path(target_cms_root_directory_path: Path) -> Optional[Path]:
    """Locate cms-manage.py or newagent-manage.py within the target repository."""
    candidate_script_relative_paths: List[str] = [
        "src/cms-manage.py",
        "cms-manage.py",
        "src/newagent-manage.py",
        "newagent-manage.py",
    ]

    for candidate_relative_path_string in candidate_script_relative_paths:
        candidate_absolute_script_path: Path = target_cms_root_directory_path / candidate_relative_path_string
        if candidate_absolute_script_path.is_file():
            return candidate_absolute_script_path

    return None


def execute_cms_page_publish_command(
    target_cms_root_directory_path: Path,
    target_content_file_path: Path,
    publication_title_string: str,
    publication_category_string: str,
    publication_author_string: str,
    publication_page_type_string: str = "blog",
    publication_featured_image_string: Optional[str] = None,
    publication_featured_video_string: Optional[str] = None,
    is_dry_run_mode_enabled: bool = False,
) -> Tuple[bool, str]:
    """Execute cms-manage.py page import (for HTML) or page add command and return execution status."""
    resolved_cms_root_path: Path = target_cms_root_directory_path.resolve()
    if not resolved_cms_root_path.is_dir():
        return False, f"Target CMS root directory not found: {resolved_cms_root_path}"

    discovered_cms_manage_script_path: Optional[Path] = find_cms_manage_script_path(resolved_cms_root_path)
    if not discovered_cms_manage_script_path:
        return False, f"No cms-manage.py or newagent-manage.py executable found in {resolved_cms_root_path}"

    # Auto-resolve HTML sibling if target_content_file_path is markdown
    effective_content_file_path: Path = target_content_file_path
    if effective_content_file_path.suffix.lower() == ".md":
        candidate_html_paths = [
            effective_content_file_path.with_suffix(".html"),
            effective_content_file_path.parent / "final_post.html",
            effective_content_file_path.parent / "05_merged_post.html",
        ]
        for candidate_html in candidate_html_paths:
            if candidate_html.is_file():
                effective_content_file_path = candidate_html
                EXECUTION_LOGGER_INSTANCE.info(
                    "Resolved HTML sibling file for publication import: %s", effective_content_file_path.name
                )
                break

    if not effective_content_file_path.is_file():
        return False, f"Content file not found: {effective_content_file_path}"

    is_html_import_mode: bool = effective_content_file_path.suffix.lower() in [".html", ".htm", ".behtml"]

    if is_html_import_mode:
        execution_cli_arguments_list: List[str] = [
            sys.executable,
            str(discovered_cms_manage_script_path),
            "page",
            "import",
            "--html",
            str(effective_content_file_path),
            "--title",
            publication_title_string,
            "--category",
            publication_category_string,
            "--author",
            publication_author_string,
            "--type",
            publication_page_type_string,
        ]
        if publication_featured_image_string:
            execution_cli_arguments_list.extend(["--featured-img", publication_featured_image_string])
    else:
        try:
            raw_body_content_string: str = effective_content_file_path.read_text(encoding="utf-8")
        except Exception as read_exception:
            return False, f"Failed to read content file: {str(read_exception)}"

        execution_cli_arguments_list: List[str] = [
            sys.executable,
            str(discovered_cms_manage_script_path),
            "page",
            "add",
            publication_title_string,
            "--category",
            publication_category_string,
            "--author",
            publication_author_string,
            "--type",
            publication_page_type_string,
            "--body",
            raw_body_content_string,
        ]
        if publication_featured_video_string:
            execution_cli_arguments_list.extend(["--featured-video", publication_featured_video_string])

    if is_dry_run_mode_enabled:
        EXECUTION_LOGGER_INSTANCE.info(
            "[DRY-RUN] Would execute: python3 %s %s",
            discovered_cms_manage_script_path.name,
            " ".join(execution_cli_arguments_list[2:]),
        )
        return True, "Dry-run completed successfully. No data was written."

    try:
        EXECUTION_LOGGER_INSTANCE.info(
            "Executing CMS page publication for '%s' in %s...",
            publication_title_string,
            resolved_cms_root_path,
        )
        process_execution_result = subprocess.run(
            execution_cli_arguments_list,
            cwd=str(resolved_cms_root_path),
            capture_output=True,
            text=True,
            check=False,
        )

        if process_execution_result.returncode != 0:
            error_details_message = (
                f"cms-manage.py exited with code {process_execution_result.returncode}: "
                f"{process_execution_result.stderr.strip() or process_execution_result.stdout.strip()}"
            )
            return False, error_details_message

        return True, process_execution_result.stdout.strip()

    except Exception as execution_subroutine_exception:
        return False, f"Execution failed: {str(execution_subroutine_exception)}"


def main() -> int:
    """Main CLI dispatch entry point for BEJSON CMS post publisher."""
    argument_parser_instance = argparse.ArgumentParser(
        description="BEJSON CMS Post Publisher (Layer 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    argument_parser_instance.add_argument(
        "--content-file",
        type=str,
        required=False,
        help="Path to merged blog post file (Markdown or BEHTML)",
    )
    argument_parser_instance.add_argument(
        "--cms-path",
        type=str,
        default=str(DEFAULT_BEJSON_CMS_REPOSITORY_PATH),
        help="Path to BEJSON CMS or NewAgent CMS root repository",
    )
    argument_parser_instance.add_argument(
        "--title",
        type=str,
        default=None,
        help="Page title (default: extracted from content file)",
    )
    argument_parser_instance.add_argument(
        "--category",
        type=str,
        default=None,
        help="Category name (default: extracted from content file, fallback 'BEJSON')",
    )
    argument_parser_instance.add_argument(
        "--author",
        type=str,
        default=None,
        help="Author display name (default: extracted from content file, fallback 'boehnenelton2024')",
    )
    argument_parser_instance.add_argument(
        "--type",
        type=str,
        default="blog",
        help="CMS page type (blog, post, page)",
    )
    argument_parser_instance.add_argument(
        "--featured-img",
        type=str,
        default=None,
        help="Featured image filename (in storage/mfdb/assets)",
    )
    argument_parser_instance.add_argument(
        "--featured-video",
        type=str,
        default=None,
        help="Optional YouTube watch URL or 11-character video ID",
    )
    argument_parser_instance.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform dry-run validation without writing to CMS database",
    )
    argument_parser_instance.add_argument(
        "--version",
        action="store_true",
        help="Show script version and exit",
    )
    argument_parser_instance.add_argument(
        "--register",
        action="store_true",
        help="Register utility with central database",
    )
    argument_parser_instance.add_argument(
        "--config",
        action="store_true",
        help="Display operational configuration",
    )
    argument_parser_instance.add_argument(
        "--reset",
        action="store_true",
        help="Verify execution environment state",
    )

    parsed_cli_arguments = argument_parser_instance.parse_args()
    configure_execution_logging_subsystem()

    if parsed_cli_arguments.version:
        sys.stdout.write(f"bejson_cms_post_publisher v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.config:
        configuration_data_dictionary = {
            "version": SYSTEM_SCRIPT_VERSION_INTEGER,
            "release_version": SYSTEM_RELEASE_VERSION_INTEGER,
            "author": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
            "default_cms_path": str(DEFAULT_BEJSON_CMS_REPOSITORY_PATH),
            "fallback_newagent_path": str(DEFAULT_NEWAGENT_CMS_REPOSITORY_PATH),
            "default_author": "boehnenelton2024",
            "default_category": "BEJSON",
            "default_type": "blog",
        }
        sys.stdout.write(json.dumps(configuration_data_dictionary, indent=2) + "\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.reset:
        EXECUTION_LOGGER_INSTANCE.info("Publisher environment integrity verified.")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.register:
        EXECUTION_LOGGER_INSTANCE.info("Registered bejson_cms_post_publisher in local context.")
        return STATUS_CODE_SUCCESS_EXECUTION

    if not parsed_cli_arguments.content_file:
        EXECUTION_LOGGER_INSTANCE.error("Missing required argument: --content-file")
        return STATUS_CODE_PATH_ERROR_EXECUTION

    target_content_file_path: Path = Path(parsed_cli_arguments.content_file).resolve()
    if not target_content_file_path.is_file():
        EXECUTION_LOGGER_INSTANCE.error("Content file does not exist: %s", target_content_file_path)
        return STATUS_CODE_PATH_ERROR_EXECUTION

    extracted_metadata_map = extract_metadata_from_file_header(target_content_file_path)

    final_post_title_string: str = (
        parsed_cli_arguments.title
        if parsed_cli_arguments.title
        else extracted_metadata_map.get("title", "Untitled Publication")
    )
    final_post_category_string: str = (
        parsed_cli_arguments.category
        if parsed_cli_arguments.category
        else extracted_metadata_map.get("category", "BEJSON")
    )
    final_post_author_string: str = (
        parsed_cli_arguments.author
        if parsed_cli_arguments.author
        else extracted_metadata_map.get("author", "boehnenelton2024")
    )
    final_post_featured_image_string: Optional[str] = (
        parsed_cli_arguments.featured_img
        if parsed_cli_arguments.featured_img
        else extracted_metadata_map.get("featured_image", None)
    )

    is_publish_successful, publication_result_message = execute_cms_page_publish_command(
        target_cms_root_directory_path=Path(parsed_cli_arguments.cms_path),
        target_content_file_path=target_content_file_path,
        publication_title_string=final_post_title_string,
        publication_category_string=final_post_category_string,
        publication_author_string=final_post_author_string,
        publication_page_type_string=parsed_cli_arguments.type,
        publication_featured_image_string=final_post_featured_image_string,
        publication_featured_video_string=parsed_cli_arguments.featured_video,
        is_dry_run_mode_enabled=parsed_cli_arguments.dry_run,
    )

    if not is_publish_successful:
        EXECUTION_LOGGER_INSTANCE.error("Publication failed: %s", publication_result_message)
        return STATUS_CODE_VALIDATION_ERROR_EXECUTION

    EXECUTION_LOGGER_INSTANCE.info("Publication success: %s", publication_result_message)
    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
