#!/data/data/com.termux/files/usr/bin/python3
# ==============================================================================
# Script Name: readme_auditor.py
# Description: Hostile verification CLI tool that audits README.md documents against
#              mandatory authoring laws: no hardcoded absolute paths, no policy leaks,
#              no AI vocalization, mandatory TOC, 2-phase structure, and 420p visual assets.
# Version: 1.0.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: a76f7263-6a09-4cd0-ba8d-367ec1e91b31
# ==============================================================================

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from PIL import Image

VERSION = "1.0.0"
AUTHOR = "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
RELATIONAL_ID = "a76f7263-6a09-4cd0-ba8d-367ec1e91b31"

auditor_logger = logging.getLogger("readme_auditor")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

FORBIDDEN_POLICY_KEYWORDS = [
    r"policy\s*§",
    r"gemini\.md",
    r"user\s+rules?",
    r"user\s+instructions?",
    r"system\s+prompt",
    r"negative\s+constraint",
    r"golden\s+rule",
    r"user_global",
    r"policy\s+absolutism"
]

FORBIDDEN_AI_VOCALIZATION_PATTERNS = [
    r"as\s+an\s+ai",
    r"written\s+by\s+ai",
    r"generated\s+by\s+ai",
    r"ai\s+assistant",
    r"large\s+language\s+model",
    r"\bllm\b",
    r"chatgpt",
    r"claude",
    r"gemini\s+cli\s+policy",
    r"antigravity\s+agent"
]

HARDCODED_PATH_PATTERNS = [
    r"/storage/emulated/0",
    r"/data/data/com\.termux",
    r"/home/[a-zA-Z0-9_-]+/",
    r"C:\\Users\\[a-zA-Z0-9_-]+"
]

def audit_hardcoded_paths(readme_lines: list[str]) -> list[str]:
    """Flag absolute system paths outside explicit environment setup instructions."""
    detected_violations = []
    is_inside_environment_setup_block = False

    for line_index, current_line in enumerate(readme_lines, start=1):
        lower_line = current_line.lower()
        if "### environment" in lower_line or "## setup" in lower_line or "export " in lower_line or ".env" in lower_line:
            is_inside_environment_setup_block = True
        elif current_line.startswith("## ") and not ("setup" in lower_line or "environment" in lower_line or "config" in lower_line):
            is_inside_environment_setup_block = False

        for path_pattern in HARDCODED_PATH_PATTERNS:
            if re.search(path_pattern, current_line, re.IGNORECASE):
                # Allowed only if it is explicitly guiding the user on environment variables / config setting
                is_configuration_guidance = (
                    "export " in current_line or
                    "config" in lower_line or
                    "set " in lower_line or
                    "path" in lower_line or
                    "replace" in lower_line or
                    "custom" in lower_line or
                    is_inside_environment_setup_block
                )
                if not is_configuration_guidance:
                    detected_violations.append(
                        f"Line {line_index}: Hardcoded system path detected: '{current_line.strip()}'"
                    )
    return detected_violations

def audit_policy_and_instructions_leak(readme_lines: list[str]) -> list[str]:
    """Flag mentions of internal policies, rules, or system instructions."""
    detected_violations = []
    for line_index, current_line in enumerate(readme_lines, start=1):
        for policy_keyword_regex in FORBIDDEN_POLICY_KEYWORDS:
            if re.search(policy_keyword_regex, current_line, re.IGNORECASE):
                detected_violations.append(
                    f"Line {line_index}: Internal policy/rule reference leaked: '{current_line.strip()}'"
                )
    return detected_violations

def audit_ai_vocalization(readme_lines: list[str]) -> list[str]:
    """Flag indications that documentation was generated or written by AI."""
    detected_violations = []
    for line_index, current_line in enumerate(readme_lines, start=1):
        for ai_pattern_regex in FORBIDDEN_AI_VOCALIZATION_PATTERNS:
            if re.search(ai_pattern_regex, current_line, re.IGNORECASE):
                detected_violations.append(
                    f"Line {line_index}: AI vocalization/attribution detected: '{current_line.strip()}'"
                )
    return detected_violations

def audit_table_of_contents(readme_lines: list[str]) -> list[str]:
    """Verify presence of a structured Table of Contents with anchor links."""
    detected_violations = []
    has_toc_header = False
    toc_link_count = 0

    for current_line in readme_lines:
        lower_line = current_line.lower().strip()
        if "table of contents" in lower_line or lower_line in {"## contents", "## toc"}:
            has_toc_header = True
        if has_toc_header and re.search(r"\[.+\]\(#.+\)", current_line):
            toc_link_count += 1

    if not has_toc_header:
        detected_violations.append("Missing Table of Contents ('## Table of Contents').")
    elif toc_link_count < 3:
        detected_violations.append(f"Table of Contents has insufficient navigation links ({toc_link_count} found).")

    return detected_violations

def audit_two_phase_structure(readme_lines: list[str]) -> list[str]:
    """Verify first half covers Setup/Usage/Features, second half covers Technical Details."""
    detected_violations = []
    total_lines = len(readme_lines)
    if total_lines < 30:
        detected_violations.append(f"README is too brief for production release ({total_lines} lines).")
        return detected_violations

    midpoint_line = total_lines // 2
    first_half_text = "\n".join(readme_lines[:midpoint_line]).lower()
    second_half_text = "\n".join(readme_lines[midpoint_line:]).lower()

    # First half checks
    has_setup_or_usage = any(k in first_half_text for k in ["setup", "install", "getting started", "prerequisites", "quick start"])
    has_usage_or_features = any(k in first_half_text for k in ["usage", "feature", "workflow", "overview"])
    if not (has_setup_or_usage and has_usage_or_features):
        detected_violations.append("First half must focus on Setup, Installation, Usage, and Feature Details.")

    # Second half checks
    has_technical_depth = any(k in second_half_text for k in ["architecture", "technical", "schema", "api", "specification", "module", "internals", "data model"])
    if not has_technical_depth:
        detected_violations.append("Second half must provide deep Technical Architecture, Specifications, or Data Models.")

    return detected_violations

def audit_visual_assets_and_scaling(readme_file_path: Path, readme_lines: list[str]) -> list[str]:
    """Audit embedded figures for 420px max dimension, aspect ratio preservation, and even distribution."""
    detected_violations = []
    embedded_image_matches = []

    for line_index, current_line in enumerate(readme_lines, start=1):
        image_markdown_matches = re.findall(r"!\[(.*?)\]\((.*?)\)", current_line)
        for caption_text, relative_image_path in image_markdown_matches:
            # Strip anchors or query params
            clean_path_string = relative_image_path.split("?")[0].split("#")[0]
            embedded_image_matches.append((line_index, caption_text, clean_path_string))

    if not embedded_image_matches:
        auditor_logger.warning("No visual screenshot figures detected in README.md.")
        return detected_violations

    # Check each image on disk
    for line_index, caption_text, image_rel_path in embedded_image_matches:
        if image_rel_path.startswith("http://") or image_rel_path.startswith("https://"):
            continue
        resolved_image_path = (readme_file_path.parent / image_rel_path).resolve()
        if not resolved_image_path.exists():
            detected_violations.append(f"Line {line_index}: Embedded image file not found on disk: {image_rel_path}")
            continue

        try:
            with Image.open(resolved_image_path) as image_handle:
                image_width, image_height = image_handle.size
                highest_dimension = max(image_width, image_height)
                if highest_dimension > 420:
                    detected_violations.append(
                        f"Line {line_index}: Image {resolved_image_path.name} exceeds 420px max dimension ({image_width}x{image_height})."
                    )
        except Exception as file_read_error:
            detected_violations.append(f"Line {line_index}: Unable to open image {image_rel_path}: {file_read_error}")

    return detected_violations

def execute_hostile_readme_audit(readme_file_path: Path) -> int:
    """Run full hostile audit suite on README."""
    if not readme_file_path.exists():
        auditor_logger.error("README target path does not exist: %s", readme_file_path)
        return 1

    readme_content = readme_file_path.read_text(encoding="utf-8")
    readme_lines = readme_content.splitlines()

    all_audit_errors: list[str] = []

    auditor_logger.info("Executing hostile audit on: %s", readme_file_path)
    all_audit_errors.extend(audit_hardcoded_paths(readme_lines))
    all_audit_errors.extend(audit_policy_and_instructions_leak(readme_lines))
    all_audit_errors.extend(audit_ai_vocalization(readme_lines))
    all_audit_errors.extend(audit_table_of_contents(readme_lines))
    all_audit_errors.extend(audit_two_phase_structure(readme_lines))
    all_audit_errors.extend(audit_visual_assets_and_scaling(readme_file_path, readme_lines))

    if all_audit_errors:
        auditor_logger.error("Hostile README Audit FAILED with %d violations:", len(all_audit_errors))
        for violation_index, violation_message in enumerate(all_audit_errors, start=1):
            auditor_logger.error("  [%d] %s", violation_index, violation_message)
        return 1

    auditor_logger.info("Hostile README Audit PASSED with zero violations.")
    return 0

def main():
    command_parser = argparse.ArgumentParser(
        prog="readme_auditor.py",
        description="Hostile verification CLI tool for README quality, policy protection, and 420p visual compliance."
    )
    command_parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    command_parser.add_argument("--readme", "-r", required=True, help="Path to README.md file to audit")

    parsed_arguments = command_parser.parse_args()
    target_readme_path = Path(parsed_arguments.readme).resolve()

    exit_status = execute_hostile_readme_audit(target_readme_path)
    sys.exit(exit_status)

if __name__ == "__main__":
    main()
