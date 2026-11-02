#!/usr/bin/env python3
"""
audit_redundancy_tool.py
Layer 5 Redundancy & Consolidation Planning Engine
Scans codebases and skill suites for code duplicates, identical function blocks,
overlapping skill triggers (Jaccard similarity), and unnormalized storage bloat.

Policy Anchors:
  Policy §6.1: Long self-describing variable names
  Policy §1.3: Code Cleanup & Discretion
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

TOOL_VERSION = "1.0.0"
TOOL_PACKAGE_VERSION = "100"

EXIT_CLEAN_PASS = 0
EXIT_PATH_FAILURE = 10
EXIT_ENV_FAILURE = 20
EXIT_REDUNDANCIES_IDENTIFIED = 30


def get_current_utc_timestamp_iso() -> str:
    """Return formatted UTC timestamp string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_target_path(untrusted_path_string: str) -> Path:
    """Resolve and sanitize input filesystem path."""
    resolved_filesystem_path = Path(untrusted_path_string).expanduser().resolve()
    return resolved_filesystem_path


def compute_token_set(text_content: str) -> Set[str]:
    """Tokenize text into a set of lower-case words for Jaccard calculation."""
    normalized_words = re.findall(r"[a-z0-9_-]+", text_content.lower())
    # Exclude trivial stop words
    stop_words = {"the", "a", "an", "and", "or", "to", "in", "for", "of", "with", "is", "use", "when", "do", "not"}
    return {w for w in normalized_words if w not in stop_words and len(w) > 2}


def calculate_jaccard_similarity(token_set_alpha: Set[str], token_set_beta: Set[str]) -> float:
    """Calculate Jaccard similarity index between two token sets."""
    if not token_set_alpha or not token_set_beta:
        return 0.0
    intersection_count = len(token_set_alpha.intersection(token_set_beta))
    union_count = len(token_set_alpha.union(token_set_beta))
    if union_count == 0:
        return 0.0
    return float(intersection_count) / float(union_count)


def audit_skill_trigger_collisions(skills_parent_directory: Path) -> List[Dict[str, Any]]:
    """Audit installed skills for trigger collision and high Jaccard overlap."""
    discovered_trigger_collisions_list: List[Dict[str, Any]] = []
    skill_manifest_registry: Dict[str, Set[str]] = {}

    for single_skill_path in skills_parent_directory.iterdir():
        if not single_skill_path.is_dir():
            continue
        skill_manifest_file = single_skill_path / "SKILL.md"
        if not skill_manifest_file.is_file():
            continue
        try:
            content_text = skill_manifest_file.read_text(encoding="utf-8")
            # Extract description
            desc_match = re.search(r"description:\s*(?:>-\s*|\|\s*)?(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)", content_text, re.DOTALL)
            if desc_match:
                desc_text = desc_match.group(1).strip()
                tokens = compute_token_set(desc_text)
                skill_manifest_registry[single_skill_path.name] = tokens
        except Exception:
            pass

    skill_names_list = sorted(list(skill_manifest_registry.keys()))
    for index_i in range(len(skill_names_list)):
        for index_j in range(index_i + 1, len(skill_names_list)):
            name_alpha = skill_names_list[index_i]
            name_beta = skill_names_list[index_j]
            tokens_alpha = skill_manifest_registry[name_alpha]
            tokens_beta = skill_manifest_registry[name_beta]

            similarity_score = calculate_jaccard_similarity(tokens_alpha, tokens_beta)
            # Flag if similarity is high (>= 0.65)
            if similarity_score >= 0.65:
                discovered_trigger_collisions_list.append(
                    {
                        "redundancy_code": "RED-SKILL-001",
                        "category": "SKILL_TRIGGER_COLLISION",
                        "severity": "HIGH",
                        "item_alpha": name_alpha,
                        "item_beta": name_beta,
                        "similarity_score": round(similarity_score, 3),
                        "description": f"Skills '{name_alpha}' and '{name_beta}' have high trigger overlap (Jaccard: {similarity_score:.2f}).",
                        "remediation": f"Disambiguate '{name_alpha}' and '{name_beta}' using explicit asymmetric negative constraint triggers.",
                    }
                )

    return discovered_trigger_collisions_list


def audit_code_duplication_functions(target_directory_path: Path) -> List[Dict[str, Any]]:
    """Audit python files for identical function definitions and implementations."""
    discovered_code_duplicates_list: List[Dict[str, Any]] = []
    function_hashes_registry: Dict[str, List[Tuple[str, str]]] = {}

    function_pattern = re.compile(
        r"^(?:async\s+)?def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(?:->\s*[^:]+)?:\s*\n((?:\s{4,}.*\n)+)",
        re.MULTILINE,
    )

    for python_file_path in target_directory_path.rglob("*.py"):
        # Skip virtualenvs or cache
        if "__pycache__" in python_file_path.parts or ".git" in python_file_path.parts:
            continue
        try:
            file_text = python_file_path.read_text(encoding="utf-8")
            for match_item in function_pattern.finditer(file_text):
                func_name = match_item.group(1)
                func_body = match_item.group(2).strip()
                # Skip tiny one-liners
                if len(func_body.splitlines()) < 4:
                    continue
                # Normalize whitespace
                normalized_body = re.sub(r"\s+", " ", func_body)
                body_hash = hashlib.sha256(normalized_body.encode("utf-8")).hexdigest()

                if body_hash not in function_hashes_registry:
                    function_hashes_registry[body_hash] = []
                function_hashes_registry[body_hash].append((func_name, str(python_file_path.relative_to(target_directory_path))))
        except Exception:
            pass

    for hash_token, occurrences_list in function_hashes_registry.items():
        if len(occurrences_list) > 1:
            file_locations_str = ", ".join([f"{loc} ({fn})" for fn, loc in occurrences_list])
            primary_func_name = occurrences_list[0][0]
            discovered_code_duplicates_list.append(
                {
                    "redundancy_code": "RED-CODE-001",
                    "category": "CODE_DUPLICATION",
                    "severity": "MEDIUM",
                    "function_name": primary_func_name,
                    "occurrences_count": len(occurrences_list),
                    "description": f"Identical function logic found in {len(occurrences_list)} locations: {file_locations_str}.",
                    "remediation": f"Extract duplicated function '{primary_func_name}' to a shared utility library.",
                }
            )

    return discovered_code_duplicates_list


def perform_complete_redundancy_audit(target_directory_path: Path, check_skills: bool = False) -> Dict[str, Any]:
    """Execute complete redundancy and overlap audit."""
    all_discovered_redundancies: List[Dict[str, Any]] = []

    # 1. Code duplicates
    code_duplicates = audit_code_duplication_functions(target_directory_path)
    all_discovered_redundancies.extend(code_duplicates)

    # 2. Skill collisions if requested or if skills directory
    if check_skills or any((target_directory_path / subdir / "SKILL.md").exists() for subdir in target_directory_path.iterdir() if subdir.is_dir()):
        skill_collisions = audit_skill_trigger_collisions(target_directory_path)
        all_discovered_redundancies.extend(skill_collisions)

    total_redundancies_count = len(all_discovered_redundancies)
    has_redundancies_flag = total_redundancies_count > 0

    audit_summary_dictionary = {
        "target_directory": str(target_directory_path),
        "audit_timestamp": get_current_utc_timestamp_iso(),
        "total_redundancies_identified": total_redundancies_count,
        "has_redundancies": has_redundancies_flag,
        "redundancies": all_discovered_redundancies,
    }
    return audit_summary_dictionary


def generate_markdown_redundancy_report(audit_result_dictionary: Dict[str, Any]) -> str:
    """Generate standardized Markdown redundancy analysis report."""
    target_dir_str = audit_result_dictionary["target_directory"]
    audit_timestamp_str = audit_result_dictionary["audit_timestamp"]
    total_redundancies_count = audit_result_dictionary["total_redundancies_identified"]
    has_redundancies_flag = audit_result_dictionary["has_redundancies"]

    status_str = "REDUNDANCIES_DETECTED" if has_redundancies_flag else "CLEAN_PASS"

    report_lines: List[str] = [
        "# Redundancy Audit & Consolidation Blueprint",
        "",
        f"- **Target System**: `{target_dir_str}`",
        f"- **Audit Timestamp**: `{audit_timestamp_str}`",
        f"- **Audit Status**: `{status_str}` ({total_redundancies_count} redundancy issues found)",
        "",
        "## 1. Discovered Duplications & Collisions",
    ]

    redundancies_list = audit_result_dictionary["redundancies"]
    if not redundancies_list:
        report_lines.append("No code duplication or skill trigger collisions detected. Architecture is fully normalized.")
    else:
        for index_counter, red_item in enumerate(redundancies_list, start=1):
            red_code_str = red_item["redundancy_code"]
            category_str = red_item["category"]
            severity_str = red_item["severity"]
            desc_str = red_item["description"]
            report_lines.append(
                f"{index_counter}. **[{red_code_str} | {category_str} | {severity_str}]**: {desc_str}"
            )

    report_lines.extend(["", "## 2. Phased Consolidation Blueprint"])
    if not redundancies_list:
        report_lines.append("- [x] Ecosystem is DRY and normalized.")
    else:
        for index_counter, red_item in enumerate(redundancies_list, start=1):
            remediation_step_str = red_item["remediation"]
            report_lines.append(f"- [ ] Step {index_counter}: {remediation_step_str}")

    report_lines.extend(
        [
            "",
            "---",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
        ]
    )
    return "\n".join(report_lines)


def main() -> int:
    """CLI entrypoint for Redundancy Auditor tool."""
    argument_parser = argparse.ArgumentParser(
        description="audit-redundancy-planner: Redundancy, duplication, and consolidation planning engine."
    )
    argument_parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to directory or codebase to audit (default: current directory).",
    )
    argument_parser.add_argument(
        "--check-skills",
        action="store_true",
        help="Audit installed skill manifests for trigger collisions and Jaccard similarity.",
    )
    argument_parser.add_argument(
        "--report",
        action="store_true",
        help="Persist markdown report to reports/audits/redundancy_audit_<timestamp>.md.",
    )
    argument_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw redundancy findings in JSON format.",
    )
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"audit_redundancy_tool v{TOOL_VERSION} (PKG{TOOL_PACKAGE_VERSION})",
    )

    parsed_arguments = argument_parser.parse_args()
    target_path = sanitize_target_path(parsed_arguments.target)

    if not target_path.exists() or not target_path.is_dir():
        sys.stderr.write(f"Error: Target directory does not exist: {target_path}\n")
        return EXIT_PATH_FAILURE

    try:
        audit_results = perform_complete_redundancy_audit(
            target_directory_path=target_path,
            check_skills=parsed_arguments.check_skills,
        )

        if parsed_arguments.json:
            print(json.dumps(audit_results, indent=2))
        else:
            markdown_content = generate_markdown_redundancy_report(audit_results)
            print(markdown_content)

        if parsed_arguments.report:
            reports_directory = target_path / "reports" / "audits"
            reports_directory.mkdir(parents=True, exist_ok=True)
            timestamp_token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_file_path = reports_directory / f"redundancy_audit_{timestamp_token}.md"
            report_file_path.write_text(generate_markdown_redundancy_report(audit_results), encoding="utf-8")
            sys.stderr.write(f"Redundancy report saved to: {report_file_path}\n")

        if audit_results["has_redundancies"]:
            return EXIT_REDUNDANCIES_IDENTIFIED
        return EXIT_CLEAN_PASS

    except Exception as general_execution_exception:
        sys.stderr.write(f"Fatal error during redundancy audit: {general_execution_exception}\n")
        return EXIT_ENV_FAILURE


if __name__ == "__main__":
    sys.exit(main())
