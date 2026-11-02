#!/usr/bin/env python3
"""
Name: bks_tool.py
Description: Production CLI Tool for BEJSON Book Standard (BKS-1 kit v1.1.5).
             Manages BEJSON 104db Book Documents, in-process declarative gates,
             JobMaker plan projections, C1-C4 validations, and multi-format exports.
Author: Elton Boehnen · boehnenelton2024@gmail.com
Version: 115
Release_Version: 300
RELATIONAL_ID: 5d66553b-1079-48ea-9b91-d9ec198c5655
"""

from pathlib import Path
import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

SCRIPT_DIRECTORY: Path = Path(__file__).resolve().parent
LIBRARY_CORE_DIRECTORY: Path = SCRIPT_DIRECTORY / "lib" / "Core"
LIBRARY_WRITING_DIRECTORY: Path = SCRIPT_DIRECTORY / "lib" / "Writing"

sys.path[:0] = [str(LIBRARY_CORE_DIRECTORY), str(LIBRARY_WRITING_DIRECTORY)]

import lib_bejson_Writing_bks_store as BKSStore  # noqa: E402
import lib_bejson_Writing_bks_validator as BKSValidator  # noqa: E402
import lib_bejson_Writing_bks_booktypes as BKSBookTypes  # noqa: E402
import lib_bejson_Writing_bks_plan as BKSPlan  # noqa: E402
import lib_bejson_Writing_bks_render as BKSRender  # noqa: E402
import lib_bejson_Writing_bks_export as BKSExport  # noqa: E402

VERSION: int = 115
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_LOCK_ERROR: int = 10
EXIT_CONFIG_ENV_ERROR: int = 20
EXIT_SCHEMA_VALIDATION_ERROR: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOGGER: logging.Logger = logging.getLogger("bks_tool")


def execute_create_new_book(
    book_title_string: str,
    book_topic_string: str,
    target_booktype_slug: str,
    author_name_string: str,
    target_output_file_path: Path,
    book_goal_string: Optional[str] = None,
) -> Path:
    skill_root_directory = SCRIPT_DIRECTORY.parent
    booktypes_store_directory = skill_root_directory / "book_types"

    target_booktype_file_path = booktypes_store_directory / f"{target_booktype_slug}.bks-type.bejson"
    if not target_booktype_file_path.exists():
        raise FileNotFoundError(f"BookType '{target_booktype_slug}' not found at: {target_booktype_file_path}")

    booktype_row_record = BKSBookTypes.bks_booktypes_load(str(target_booktype_file_path))
    outline_node_descriptors = BKSBookTypes.bks_booktypes_outline_nodes(booktype_row_record)

    created_book_document = BKSStore.bks_store_create_book(
        title=book_title_string,
        topic=book_topic_string,
        booktype_slug=target_booktype_slug,
        author_name=author_name_string,
        nodes=outline_node_descriptors,
        goal=book_goal_string or f"Comprehensive guide to {book_topic_string}",
    )

    BKSStore.bks_store_commit(str(target_output_file_path), created_book_document, level=2)
    LOGGER.info("Successfully created BKS-1 Book Document at: %s", target_output_file_path)
    return target_output_file_path


def execute_validate_book(
    target_book_file_path: Path,
    conformance_level_threshold: int = 3,
) -> bool:
    loaded_book_document = BKSStore.bks_store_load(str(target_book_file_path))
    validation_result = BKSValidator.bks_validate_book(
        loaded_book_document,
        level=conformance_level_threshold,
    )

    LOGGER.info(
        "Validation Result for '%s': Level Reached = C%d (Target: C%d), Status = %s",
        target_book_file_path.name,
        validation_result.level_reached,
        conformance_level_threshold,
        "PASSED" if validation_result.ok else "FAILED",
    )

    if not validation_result.ok:
        for problem_record in validation_result.problems:
            LOGGER.error("Violation [%s]: %s", problem_record.get("code"), problem_record.get("message"))
        return False

    return True


def execute_project_plan(
    target_book_file_path: Path,
    target_plan_output_path: Path,
) -> Path:
    loaded_book_document = BKSStore.bks_store_load(str(target_book_file_path))
    projected_plan_document = BKSPlan.bks_plan_from_book(loaded_book_document)

    with open(target_plan_output_path, "w", encoding="utf-8") as plan_write_stream:
        json.dump(projected_plan_document, plan_write_stream, indent=2, ensure_ascii=False)

    LOGGER.info("Successfully projected JobMaker plan to: %s", target_plan_output_path)
    return target_plan_output_path


def execute_render_and_export(
    target_book_file_path: Path,
    export_format_token: str,
    export_theme_token: str,
    target_destination_folder: Path,
) -> Path:
    loaded_book_document = BKSStore.bks_store_load(str(target_book_file_path))
    rendered_payload = BKSRender.bks_render_book(
        loaded_book_document,
        fmt=export_format_token,
        theme=export_theme_token,
    )

    target_destination_folder.mkdir(parents=True, exist_ok=True)
    destination_file_path = target_destination_folder / str(rendered_payload["filename"])

    with open(destination_file_path, "wb") as export_binary_stream:
        export_binary_stream.write(bytes(rendered_payload["bytes"]))

    LOGGER.info("Exported %s publication to: %s", export_format_token.upper(), destination_file_path)
    return destination_file_path


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BKS-1 BEJSON Book Standard CLI Tool")
    parser.add_argument("--create", action="store_true", help="Create fresh book from BookType.")
    parser.add_argument("--type", type=str, default="technical_manual", help="BookType slug.")
    parser.add_argument("--title", type=str, help="Book title.")
    parser.add_argument("--topic", type=str, help="Book topic.")
    parser.add_argument("--author", type=str, default="Elton Boehnen", help="Author display name.")
    parser.add_argument("--book", type=str, help="Path to target .bks.bejson file.")
    parser.add_argument("--validate", action="store_true", help="Validate book conformance (C1-C4).")
    parser.add_argument("--level", type=int, default=3, help="Conformance level target (1-4).")
    parser.add_argument("--plan", action="store_true", help="Project JobMaker JobTask plan.")
    parser.add_argument("--export", type=str, choices=["html", "md", "txt", "json", "bejson"], help="Export book.")
    parser.add_argument("--theme", type=str, default="becss", choices=["becss", "clean", "contrast", "minimal"], help="HTML theme.")
    parser.add_argument("--out", type=str, help="Output file or directory path.")
    return parser.parse_args()


def main() -> None:
    cli_arguments = parse_cli_arguments()

    try:
        if cli_arguments.create:
            if not cli_arguments.title or not cli_arguments.topic or not cli_arguments.out:
                LOGGER.error("--create requires --title, --topic, and --out")
                sys.exit(EXIT_CONFIG_ENV_ERROR)
            execute_create_new_book(
                book_title_string=cli_arguments.title,
                book_topic_string=cli_arguments.topic,
                target_booktype_slug=cli_arguments.type,
                author_name_string=cli_arguments.author,
                target_output_file_path=Path(cli_arguments.out),
            )
            sys.exit(EXIT_OK)

        if cli_arguments.validate:
            if not cli_arguments.book:
                LOGGER.error("--validate requires --book")
                sys.exit(EXIT_CONFIG_ENV_ERROR)
            is_valid = execute_validate_book(
                target_book_file_path=Path(cli_arguments.book),
                conformance_level_threshold=cli_arguments.level,
            )
            sys.exit(EXIT_OK if is_valid else EXIT_SCHEMA_VALIDATION_ERROR)

        if cli_arguments.plan:
            if not cli_arguments.book or not cli_arguments.out:
                LOGGER.error("--plan requires --book and --out")
                sys.exit(EXIT_CONFIG_ENV_ERROR)
            execute_project_plan(
                target_book_file_path=Path(cli_arguments.book),
                target_plan_output_path=Path(cli_arguments.out),
            )
            sys.exit(EXIT_OK)

        if cli_arguments.export:
            if not cli_arguments.book:
                LOGGER.error("--export requires --book")
                sys.exit(EXIT_CONFIG_ENV_ERROR)
            output_folder = Path(cli_arguments.out) if cli_arguments.out else Path(cli_arguments.book).parent / "exports"
            execute_render_and_export(
                target_book_file_path=Path(cli_arguments.book),
                export_format_token=cli_arguments.export,
                export_theme_token=cli_arguments.theme,
                target_destination_folder=output_folder,
            )
            sys.exit(EXIT_OK)

    except Exception as runtime_error:
        LOGGER.exception("Fatal BKS tool execution failure: %s", runtime_error)
        sys.exit(EXIT_SCHEMA_VALIDATION_ERROR)


if __name__ == "__main__":
    main()
