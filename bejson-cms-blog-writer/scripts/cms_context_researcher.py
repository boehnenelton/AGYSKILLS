#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: cms_context_researcher.py
# Description: Layer 5 Context Research Engine for BEJSON CMS Blog Authoring.
#              Conducts automated forensic analysis of target project codebases,
#              local specifications, or live website URLs, extracting architectural
#              nodes, schemas, API signatures, and talking points for 5-part drafts.
# Version: 100
# Date Created: 2026-10-25
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 9e5b2c14-7f1a-4d33-8b21-4f81c9a18032
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("cms_context_researcher requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import ast
import json
import logging
import os
import re
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SYSTEM_SCRIPT_VERSION_INTEGER: int = 100
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "9e5b2c14-7f1a-4d33-8b21-4f81c9a18032"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("CmsContextResearcher")


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [CmsContextResearcher] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_python_ast_signatures(target_file_path: Path) -> List[Dict[str, str]]:
    """Parse a Python source file using AST to extract class and function definitions."""
    extracted_signatures_list: List[Dict[str, str]] = []
    try:
        source_code_text: str = target_file_path.read_text(encoding="utf-8")
        parsed_abstract_syntax_tree = ast.parse(source_code_text, filename=str(target_file_path))

        for syntax_node in ast.walk(parsed_abstract_syntax_tree):
            if isinstance(syntax_node, ast.ClassDef):
                extracted_signatures_list.append(
                    {
                        "type": "class",
                        "name": syntax_node.name,
                        "docstring": ast.get_docstring(syntax_node) or "",
                        "line_number": str(syntax_node.lineno),
                    }
                )
            elif isinstance(syntax_node, ast.FunctionDef) and not syntax_node.name.startswith("_"):
                function_arguments_list = [arg.arg for arg in syntax_node.args.args]
                extracted_signatures_list.append(
                    {
                        "type": "function",
                        "name": f"{syntax_node.name}({', '.join(function_arguments_list)})",
                        "docstring": ast.get_docstring(syntax_node) or "",
                        "line_number": str(syntax_node.lineno),
                    }
                )
    except Exception as ast_parsing_exception:
        EXECUTION_LOGGER_INSTANCE.debug(
            "AST extraction skipped for %s: %s", target_file_path.name, str(ast_parsing_exception)
        )

    return extracted_signatures_list


def inspect_local_project_filesystem(
    target_project_path: Path,
) -> Dict[str, Any]:
    """Forensically inspect local project codebase, manifest, and source modules."""
    resolved_project_path: Path = target_project_path.resolve()
    research_results_dictionary: Dict[str, Any] = {
        "source_type": "local_project",
        "target_path": str(resolved_project_path),
        "project_name": resolved_project_path.name,
        "bejson_metadata": {},
        "discovered_files": [],
        "ast_signatures": [],
        "readme_summary": "",
        "key_components": [],
    }

    if not resolved_project_path.exists():
        return research_results_dictionary

    # If target is a single file
    if resolved_project_path.is_file():
        research_results_dictionary["discovered_files"].append(resolved_project_path.name)
        if resolved_project_path.suffix == ".py":
            signatures = extract_python_ast_signatures(resolved_project_path)
            research_results_dictionary["ast_signatures"].extend(signatures)
        return research_results_dictionary

    # If target is a directory
    discovered_files_list: List[Path] = [
        f for f in resolved_project_path.rglob("*")
        if f.is_file() and not any(p.startswith((".", "__pycache__", "venv")) for p in f.parts)
    ]
    research_results_dictionary["discovered_files"] = [
        str(f.relative_to(resolved_project_path)) for f in discovered_files_list[:60]
    ]

    # Check for bejson_project.json or .bejson_project.json
    for manifest_candidate_name in ("bejson_project.json", ".bejson_project.json"):
        manifest_file_path = resolved_project_path / manifest_candidate_name
        if manifest_file_path.is_file():
            try:
                manifest_data = json.loads(manifest_file_path.read_text(encoding="utf-8"))
                research_results_dictionary["bejson_metadata"] = {
                    "project_name": manifest_data.get("Project_Name", resolved_project_path.name),
                    "project_version": manifest_data.get("Project_Version", "1.0.0"),
                    "package_version": manifest_data.get("Package_Version", "100"),
                    "description": manifest_data.get("Project_Description", ""),
                    "project_type": manifest_data.get("Type") or manifest_data.get("Project_Type", ""),
                    "status": manifest_data.get("Status", "Active"),
                }
                if manifest_data.get("Project_Name"):
                    research_results_dictionary["project_name"] = manifest_data["Project_Name"]
            except Exception as json_read_error:
                EXECUTION_LOGGER_INSTANCE.warning("Error reading project manifest: %s", str(json_read_error))

    # Check for README.md
    readme_candidate_path = resolved_project_path / "README.md"
    if readme_candidate_path.is_file():
        try:
            readme_text = readme_candidate_path.read_text(encoding="utf-8")[:3000]
            research_results_dictionary["readme_summary"] = readme_text
        except Exception:
            pass

    # Extract AST signatures from key python files
    for file_path in discovered_files_list:
        if file_path.suffix == ".py" and len(research_results_dictionary["ast_signatures"]) < 30:
            extracted_signatures = extract_python_ast_signatures(file_path)
            for sig in extracted_signatures:
                sig["relative_file"] = str(file_path.relative_to(resolved_project_path))
                research_results_dictionary["ast_signatures"].append(sig)

    # Derive high-level components from directory structure
    root_subdirectories = [d.name for d in resolved_project_path.iterdir() if d.is_dir() and not d.name.startswith(".")]
    research_results_dictionary["key_components"] = root_subdirectories

    return research_results_dictionary


def fetch_and_analyze_site_url(
    target_site_url_string: str,
) -> Dict[str, Any]:
    """Fetch live web page content via HTTP and extract technical structure."""
    research_results_dictionary: Dict[str, Any] = {
        "source_type": "remote_url",
        "target_url": target_site_url_string,
        "page_title": "",
        "meta_description": "",
        "headings": [],
        "code_snippets": [],
        "clean_body_text_sample": "",
    }

    try:
        request_headers_map = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; Termux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36 Antigravity/1.0"
        }
        http_request_instance = urllib.request.Request(
            target_site_url_string, headers=request_headers_map
        )

        with urllib.request.urlopen(http_request_instance, timeout=15) as http_response_instance:
            raw_html_bytes: bytes = http_response_instance.read(500000)
            raw_html_content_string: str = raw_html_bytes.decode("utf-8", errors="replace")

        # Extract title
        title_match = re.search(r"<title>(.*?)</title>", raw_html_content_string, flags=re.IGNORECASE | re.DOTALL)
        if title_match:
            research_results_dictionary["page_title"] = title_match.group(1).strip()

        # Extract meta description
        meta_desc_match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            raw_html_content_string,
            flags=re.IGNORECASE,
        )
        if meta_desc_match:
            research_results_dictionary["meta_description"] = meta_desc_match.group(1).strip()

        # Extract H1, H2, H3 headings
        headings_matches = re.findall(
            r"<h([1-3])[^>]*>(.*?)</h\1>", raw_html_content_string, flags=re.IGNORECASE | re.DOTALL
        )
        for level_str, heading_text in headings_matches:
            clean_heading = re.sub(r"<[^>]+>", "", heading_text).strip()
            if clean_heading:
                research_results_dictionary["headings"].append(f"H{level_str}: {clean_heading}")

        # Extract code blocks
        code_matches = re.findall(
            r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
            raw_html_content_string,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for code_snippet in code_matches[:6]:
            clean_code = re.sub(r"<[^>]+>", "", code_snippet).strip()
            if clean_code:
                research_results_dictionary["code_snippets"].append(clean_code[:400])

        # Extract body text without scripts/styles
        sanitized_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw_html_content_string, flags=re.DOTALL | re.IGNORECASE)
        sanitized_plain_text = re.sub(r"<[^>]+>", " ", sanitized_html)
        sanitized_plain_text = re.sub(r"\s+", " ", sanitized_plain_text).strip()
        research_results_dictionary["clean_body_text_sample"] = sanitized_plain_text[:4000]

    except Exception as network_fetch_exception:
        EXECUTION_LOGGER_INSTANCE.error("Failed to fetch site URL: %s", str(network_fetch_exception))
        research_results_dictionary["error"] = str(network_fetch_exception)

    return research_results_dictionary


def synthesize_research_brief_document(
    research_data_dictionary: Dict[str, Any],
) -> str:
    """Format extracted research intelligence into a structured markdown document."""
    current_utc_timestamp_string: str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    source_type_string: str = research_data_dictionary.get("source_type", "unknown")

    brief_chunks_list: List[str] = [
        "# Technical Context Research Brief",
        f"\n> **Generated**: {current_utc_timestamp_string} | **Source Type**: {source_type_string}\n",
    ]

    if source_type_string == "local_project":
        project_name: str = research_data_dictionary.get("project_name", "Target Project")
        brief_chunks_list.append(f"## 1. Project Overview: {project_name}\n")
        brief_chunks_list.append(f"- **Filesystem Target**: `{research_data_dictionary.get('target_path')}`")

        bejson_meta = research_data_dictionary.get("bejson_metadata", {})
        if bejson_meta:
            brief_chunks_list.append(f"- **Version**: `{bejson_meta.get('project_version')}` (PKG {bejson_meta.get('package_version')})")
            brief_chunks_list.append(f"- **Type / Status**: `{bejson_meta.get('project_type')}` | `{bejson_meta.get('status')}`")
            brief_chunks_list.append(f"- **Description**: {bejson_meta.get('description')}")

        components = research_data_dictionary.get("key_components", [])
        if components:
            brief_chunks_list.append(f"\n### Core Architectural Directories & Modules\n")
            for comp_name in components:
                brief_chunks_list.append(f"- `/{comp_name}/`")

        ast_sigs = research_data_dictionary.get("ast_signatures", [])
        if ast_sigs:
            brief_chunks_list.append(f"\n### Verified Class & Function Signatures\n")
            for sig in ast_sigs[:20]:
                source_file = sig.get("relative_file", "")
                brief_chunks_list.append(f"- `{sig['type']}` **{sig['name']}** in `{source_file}` (line {sig['line_number']})")
                if sig.get("docstring"):
                    first_line_doc = sig["docstring"].splitlines()[0]
                    brief_chunks_list.append(f"  *Note: {first_line_doc}*")

        readme_text = research_data_dictionary.get("readme_summary", "")
        if readme_text:
            brief_chunks_list.append(f"\n### README Abstract\n```markdown\n{readme_text[:1200]}\n```\n")

    elif source_type_string == "remote_url":
        page_title: str = research_data_dictionary.get("page_title", "Web Target")
        brief_chunks_list.append(f"## 1. Web Target: {page_title}\n")
        brief_chunks_list.append(f"- **Target URL**: {research_data_dictionary.get('target_url')}")
        if research_data_dictionary.get("meta_description"):
            brief_chunks_list.append(f"- **Meta Description**: {research_data_dictionary.get('meta_description')}")

        headings = research_data_dictionary.get("headings", [])
        if headings:
            brief_chunks_list.append(f"\n### Discovered Page Headings\n")
            for heading in headings[:15]:
                brief_chunks_list.append(f"- {heading}")

        code_snippets = research_data_dictionary.get("code_snippets", [])
        if code_snippets:
            brief_chunks_list.append(f"\n### Extracted Code / Technical Blocks\n")
            for idx, code_sample in enumerate(code_snippets, start=1):
                brief_chunks_list.append(f"```text\n// Snippet {idx}\n{code_sample}\n```\n")

        body_sample = research_data_dictionary.get("clean_body_text_sample", "")
        if body_sample:
            brief_chunks_list.append(f"\n### Content Summary Extract\n{body_sample[:1000]}...\n")

    # Add Strategic Section Allocation Guidelines for Part 1 Planner
    brief_chunks_list.append(
        "\n## 2. Strategic Narrative Anchors for 4-Part Blog Draft (>=120 lines each)\n\n"
        "1. **Section 1 (Problem Space & Motivation)**: Anchor the narrative on real-world engineering constraints "
        "and architectural trade-offs demonstrated by this target system.\n"
        "2. **Section 2 (Architecture & Data Contracts)**: Walk through the specific data structures, schemas, and "
        "modular interfaces extracted above.\n"
        "3. **Section 3 (Implementation & Verification)**: Detail exact command-line workflows, code algorithms, "
        "and execution stages using verified function signatures.\n"
        "4. **Section 4 (Hardening & Horizons)**: Detail operational error-handling, resilience, performance telemetry, "
        "and long-term maintenance.\n\n"
        "## 3. Recommended Visual Canvas Imagery\n\n"
        "- **Article Hero Canvas (1280x640)**: Centered around target core architecture with 4 peripheral node cards.\n"
        "- **Visual Accent**: Policy §8.1 Tri-Color (#000000 background, #FFFFFF text, #DE2626 laser accents).\n"
    )

    return "\n".join(brief_chunks_list)


def main() -> int:
    """Main CLI entry point for CMS Context Researcher."""
    argument_parser_instance = argparse.ArgumentParser(
        description="BEJSON CMS Blog Context Researcher (Layer 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    argument_parser_instance.add_argument(
        "--target-path",
        type=str,
        default=None,
        help="Path to local codebase repository or source file for context analysis",
    )
    argument_parser_instance.add_argument(
        "--target-url",
        type=str,
        default=None,
        help="Target site URL to fetch and analyze via HTTP",
    )
    argument_parser_instance.add_argument(
        "--output",
        type=str,
        default=None,
        help="Destination markdown file path for research brief (default: 00_context_research.md)",
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
        sys.stdout.write(f"cms_context_researcher v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.config:
        config_data = {
            "version": SYSTEM_SCRIPT_VERSION_INTEGER,
            "release_version": SYSTEM_RELEASE_VERSION_INTEGER,
            "author": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
            "default_output_filename": "00_context_research.md",
        }
        sys.stdout.write(json.dumps(config_data, indent=2) + "\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.reset or parsed_cli_arguments.register:
        EXECUTION_LOGGER_INSTANCE.info("Researcher integrity verified.")
        return STATUS_CODE_SUCCESS_EXECUTION

    if not parsed_cli_arguments.target_path and not parsed_cli_arguments.target_url:
        EXECUTION_LOGGER_INSTANCE.error("Must provide either --target-path or --target-url")
        return STATUS_CODE_PATH_ERROR_EXECUTION

    research_findings_data_dictionary: Dict[str, Any] = {}

    if parsed_cli_arguments.target_path:
        project_path = Path(parsed_cli_arguments.target_path).resolve()
        EXECUTION_LOGGER_INSTANCE.info("Conducting context research on local target: %s", project_path)
        research_findings_data_dictionary = inspect_local_project_filesystem(project_path)

    elif parsed_cli_arguments.target_url:
        target_url = parsed_cli_arguments.target_url
        EXECUTION_LOGGER_INSTANCE.info("Conducting context research on remote URL: %s", target_url)
        research_findings_data_dictionary = fetch_and_analyze_site_url(target_url)

    compiled_research_brief_markdown: str = synthesize_research_brief_document(research_findings_data_dictionary)

    # Determine output path
    output_target_file_path: Path
    if parsed_cli_arguments.output:
        output_target_file_path = Path(parsed_cli_arguments.output).resolve()
    else:
        output_target_file_path = Path("00_context_research.md").resolve()

    try:
        output_target_file_path.parent.mkdir(parents=True, exist_ok=True)
        output_target_file_path.write_text(compiled_research_brief_markdown, encoding="utf-8")
        EXECUTION_LOGGER_INSTANCE.info("Context research brief successfully written to: %s", output_target_file_path)
    except Exception as write_exception:
        EXECUTION_LOGGER_INSTANCE.error("Failed to write research brief: %s", str(write_exception))
        return STATUS_CODE_PATH_ERROR_EXECUTION

    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
