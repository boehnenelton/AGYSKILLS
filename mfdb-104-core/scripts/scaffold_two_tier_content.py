#!/usr/bin/env python3
"""
File_Name:          scaffold_two_tier_content.py
Description:        Scaffolds detached Two-Tier BEJSON 104db content records for long-form prose and reviews.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      3a8c1e2f-5d4b-4f7a-9e1c-7b0f8a5c2d3e
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
import uuid
from typing import Any, Dict, List, Optional

VERSION = 100
RELEASE_VERSION = 300
RELATIONAL_ID = "3a8c1e2f-5d4b-4f7a-9e1c-7b0f8a5c2d3e"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("scaffold_two_tier_content")

CANONICAL_FIELD_DEFINITIONS: List[Dict[str, str]] = [
    {"name": "Record_Type_Parent", "type": "string"},
    {"name": "meta_title", "type": "string"},
    {"name": "html_body", "type": "string"},
    {"name": "markdown_body", "type": "string"},
    {"name": "source_code", "type": "string"},
]


def sanitize_boundary_whitespace(input_value: Any) -> Any:
    """Sanitizes boundary-layer whitespace per Policy §10.9."""
    if isinstance(input_value, str):
        return input_value.strip()
    return input_value


def compile_field_map_cache(bejson_document_data: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) field map lookup cache from the Fields definition array."""
    field_map_lookup_cache: Dict[str, int] = {}
    field_definitions_list = bejson_document_data.get("Fields", [])
    for field_column_index, field_definition_entry in enumerate(field_definitions_list):
        if isinstance(field_definition_entry, dict):
            field_name_identifier = field_definition_entry.get("name", "")
        else:
            field_name_identifier = str(field_definition_entry)
        field_map_lookup_cache[field_name_identifier] = field_column_index
    return field_map_lookup_cache


def create_two_tier_document(
    document_headline_title: str,
    compiled_html_body_markup: str,
    raw_markdown_source_text: str = "",
    embedded_source_code_text: str = "",
) -> Dict[str, Any]:
    """Assembles a valid BEJSON 104db two-tier content document with PageMeta and Content records."""
    bejson_document_structure: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "104db",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": ["PageMeta", "Content"],
        "Fields": CANONICAL_FIELD_DEFINITIONS,
        "Values": [
            [
                "PageMeta",
                sanitize_boundary_whitespace(document_headline_title),
                None,
                None,
                None,
            ],
            [
                "Content",
                None,
                compiled_html_body_markup,
                raw_markdown_source_text,
                embedded_source_code_text,
            ],
        ],
    }
    return bejson_document_structure


def persist_two_tier_document_atomic(
    target_destination_file_path: Path,
    bejson_document_payload: Dict[str, Any],
) -> None:
    """Persists document atomically using a temporary file and POSIX replace."""
    target_destination_file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_scratch_file_path = target_destination_file_path.with_suffix(".104dbtmp")

    with open(temporary_scratch_file_path, "w", encoding="utf-8") as temporary_output_stream:
        json.dump(bejson_document_payload, temporary_output_stream, indent=2, ensure_ascii=False)
        temporary_output_stream.write("\n")

    temporary_scratch_file_path.replace(target_destination_file_path)
    LOG.info("Persisted atomic Two-Tier content record to %s", target_destination_file_path)


def main() -> int:
    argument_parser_instance = argparse.ArgumentParser(
        prog="scaffold_two_tier_content",
        description="Scaffolds detached Two-Tier BEJSON 104db content records for long-form prose and reviews.",
    )
    argument_parser_instance.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})",
    )
    argument_parser_instance.add_argument(
        "--register",
        action="store_true",
        help="Display registration status with master index.",
    )
    argument_parser_instance.add_argument(
        "--config",
        action="store_true",
        help="Display runtime configuration.",
    )
    argument_parser_instance.add_argument(
        "--reset",
        action="store_true",
        help="Reset state.",
    )
    argument_parser_instance.add_argument(
        "--page-uuid",
        type=str,
        default=None,
        help="RFC 4122 v4 UUID identifier for the page. Generated if omitted.",
    )
    argument_parser_instance.add_argument(
        "--title",
        "-t",
        type=str,
        default="Title",
        help="Headline title string for PageMeta.",
    )
    argument_parser_instance.add_argument(
        "--html",
        type=str,
        default="<p>Content Body</p>",
        help="Compiled HTML body string or path to an HTML fragment file.",
    )
    argument_parser_instance.add_argument(
        "--markdown",
        "-m",
        type=str,
        default="",
        help="Optional markdown source string or path to markdown file.",
    )
    argument_parser_instance.add_argument(
        "--source-code",
        "-s",
        type=str,
        default="",
        help="Optional embedded source code string or path to code file.",
    )
    argument_parser_instance.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("storage/mfdb/pages_db"),
        help="Destination directory for the detached 104db content record.",
    )

    parsed_command_arguments = argument_parser_instance.parse_args()

    if parsed_command_arguments.config or parsed_command_arguments.register:
        LOG.info("scaffold_two_tier_content v%d (Release %d) ready.", VERSION, RELEASE_VERSION)
        return 0

    if parsed_command_arguments.reset:
        LOG.info("State reset acknowledged.")
        return 0

    resolved_page_uuid_identifier = (
        parsed_command_arguments.page_uuid
        if parsed_command_arguments.page_uuid
        else str(uuid.uuid4())
    )

    # Ingest HTML body (inline or from file)
    resolved_html_body_content = parsed_command_arguments.html
    potential_html_file_path = Path(parsed_command_arguments.html)
    if potential_html_file_path.is_file():
        try:
            resolved_html_body_content = potential_html_file_path.read_text(encoding="utf-8")
        except Exception as file_read_exception:
            LOG.error("Failed to read HTML body from %s: %s", potential_html_file_path, file_read_exception)
            return 10

    # Ingest Markdown source (inline or from file)
    resolved_markdown_source_content = parsed_command_arguments.markdown
    if parsed_command_arguments.markdown:
        potential_markdown_file_path = Path(parsed_command_arguments.markdown)
        if potential_markdown_file_path.is_file():
            try:
                resolved_markdown_source_content = potential_markdown_file_path.read_text(encoding="utf-8")
            except Exception as file_read_exception:
                LOG.error("Failed to read Markdown from %s: %s", potential_markdown_file_path, file_read_exception)
                return 10

    # Ingest Source code (inline or from file)
    resolved_source_code_content = parsed_command_arguments.source_code
    if parsed_command_arguments.source_code:
        potential_code_file_path = Path(parsed_command_arguments.source_code)
        if potential_code_file_path.is_file():
            try:
                resolved_source_code_content = potential_code_file_path.read_text(encoding="utf-8")
            except Exception as file_read_exception:
                LOG.error("Failed to read source code from %s: %s", potential_code_file_path, file_read_exception)
                return 10

    constructed_two_tier_document = create_two_tier_document(
        document_headline_title=parsed_command_arguments.title,
        compiled_html_body_markup=resolved_html_body_content,
        raw_markdown_source_text=resolved_markdown_source_content,
        embedded_source_code_text=resolved_source_code_content,
    )

    destination_file_path = (
        parsed_command_arguments.output_dir / f"{resolved_page_uuid_identifier}.json"
    )

    try:
        persist_two_tier_document_atomic(
            target_destination_file_path=destination_file_path,
            bejson_document_payload=constructed_two_tier_document,
        )
    except Exception as persistence_exception:
        LOG.error("Failed atomic persistence: %s", persistence_exception)
        return 20

    LOG.info("Successfully scaffolded Two-Tier content record: %s", destination_file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
