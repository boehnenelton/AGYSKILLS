#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: admin_topic_scout.py
# Description: Layer 5 Recursive Admin Topic Scout & Plan Configuration Tuner.
#              Recursively scans /storage/emulated/0/Admin across repos, libraries,
#              skills, and specs to discover active development artifacts, suggests
#              numbered blog post topics, and tunes the 5-part plan prompt config.
# Version: 100
# Date Created: 2026-10-25
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 5b1a8c23-9e41-4710-8d52-2b6e1f0c9073
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("admin_topic_scout requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SYSTEM_SCRIPT_VERSION_INTEGER: int = 100
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "5b1a8c23-9e41-4710-8d52-2b6e1f0c9073"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("AdminTopicScout")
DEFAULT_ADMIN_ROOT_DIRECTORY_PATH: Path = Path("/storage/emulated/0/Admin")


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [AdminTopicScout] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@dataclass
class DiscoveredProjectArtifact:
    project_canonical_name: str
    absolute_filesystem_path: Path
    detected_project_type: str
    manifest_description: str = ""
    discovered_technologies: List[str] = field(default_factory=list)
    key_subdirectories: List[str] = field(default_factory=list)


@dataclass
class ProposedBlogTopic:
    topic_index: int
    title: str
    subtitle_hook: str
    target_path: str
    category: str
    difficulty_level: str
    core_subsystems: List[str]
    talking_points: List[str]


def extract_manifest_information(
    target_directory_path: Path,
) -> Tuple[str, str, str]:
    """Inspect directory for bejson_project.json or package.json."""
    for manifest_name in ("bejson_project.json", ".bejson_project.json"):
        manifest_file = target_directory_path / manifest_name
        if manifest_file.is_file():
            try:
                data = json.loads(manifest_file.read_text(encoding="utf-8"))
                name = data.get("Project_Name", target_directory_path.name)
                desc = data.get("Project_Description", "")
                proj_type = data.get("Type") or data.get("Project_Type", "bejson")
                return name, desc, proj_type
            except Exception:
                pass
    return target_directory_path.name, "", "unknown"


def scan_admin_directory_recursively(
    target_admin_root_path: Path,
    maximum_recursion_depth: int = 4,
) -> List[DiscoveredProjectArtifact]:
    """Recursively discover projects, library tiers, and systems under Admin."""
    discovered_artifacts_list: List[DiscoveredProjectArtifact] = []
    resolved_admin_path = target_admin_root_path.resolve()

    if not resolved_admin_path.is_dir():
        EXECUTION_LOGGER_INSTANCE.warning("Admin root directory not found: %s", resolved_admin_path)
        return discovered_artifacts_list

    EXECUTION_LOGGER_INSTANCE.info("Recursively scanning Admin root: %s (depth=%d)", resolved_admin_path, maximum_recursion_depth)

    # Traverse subdirectories with depth guard
    for root_dirpath_string, subdirectory_names_list, file_names_list in os.walk(str(resolved_admin_path)):
        current_path = Path(root_dirpath_string)
        current_relative_parts = current_path.relative_to(resolved_admin_path).parts

        # Skip hidden or heavy cache directories
        subdirectory_names_list[:] = [
            d for d in subdirectory_names_list
            if not d.startswith((".", "__pycache__", "venv", "node_modules", "captures", "build", "dist"))
        ]

        if len(current_relative_parts) > maximum_recursion_depth:
            continue

        # Check if this folder constitutes an autonomous project / system
        has_bejson_manifest = any(f in file_names_list for f in ("bejson_project.json", ".bejson_project.json"))
        has_python_app = any(f.endswith(".py") for f in file_names_list) and any(f in file_names_list for f in ("README.md", "run.sh", "requirements.txt"))
        is_library_tier = current_path.name in ("libraries_104", "libraries_105") or (current_path.parent.name in ("libraries_104", "libraries_105") and current_path.name.startswith("Lib_"))
        is_repo_root = current_path.parent.name == "Repos"
        is_templates_system = current_path.name in ("Canvas_SVG_Capture_Templates", "Templates")

        if has_bejson_manifest or is_repo_root or is_library_tier or is_templates_system or (has_python_app and len(current_relative_parts) <= 3):
            proj_name, proj_desc, proj_type = extract_manifest_information(current_path)
            
            # Detect technologies
            technologies = []
            if any(f.endswith(".py") for f in file_names_list): technologies.append("Python 3.10+")
            if any(f.endswith((".js", ".jsx", ".ts", ".tsx")) for f in file_names_list): technologies.append("JavaScript/TypeScript")
            if any(f.endswith((".bejson", ".bejson.json")) for f in file_names_list) or has_bejson_manifest: technologies.append("BEJSON 104a/105")
            if any(f.endswith(".html") for f in file_names_list): technologies.append("BEHTML / SVG")
            if any(f.endswith(".sh") for f in file_names_list): technologies.append("Bash / Termux")

            subdirs = [d for d in subdirectory_names_list if not d.startswith(".")]

            artifact = DiscoveredProjectArtifact(
                project_canonical_name=proj_name,
                absolute_filesystem_path=current_path,
                detected_project_type=proj_type,
                manifest_description=proj_desc,
                discovered_technologies=technologies,
                key_subdirectories=subdirs,
            )
            discovered_artifacts_list.append(artifact)

    return discovered_artifacts_list


def synthesize_blog_proposals_from_artifacts(
    discovered_artifacts_list: List[DiscoveredProjectArtifact],
) -> List[ProposedBlogTopic]:
    """Generate categorized, numbered blog post topic proposals from discovered artifacts."""
    proposed_topics_list: List[ProposedBlogTopic] = []
    current_topic_index = 1

    for artifact in discovered_artifacts_list:
        path_str = str(artifact.absolute_filesystem_path)
        name = artifact.project_canonical_name
        desc = artifact.manifest_description

        # Category 1: BEJSON CMS & Publishing Systems
        if "BEJSON_CMS" in path_str or "NA-CMS" in path_str or "CMS" in name.upper():
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title=f"Zero-SQL CMS on Android: Inside the {name} Two-Part Storage Engine",
                subtitle_hook="How decoupled manifests and dense 104db payloads deliver serverless publication speeds in Termux.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="Advanced",
                core_subsystems=["Positional Storage", "MFDB Manifest", "REST Engine", "Static Site Generator"],
                talking_points=[
                    "The limits of SQLite on mobile and the zero-SQL architecture imperative",
                    "Two-part persistence: fast index pagerecord.bejson vs dense pages_db/<uuid>.json",
                    "Automating content lifecycles via cms-manage.py and headless Playwright builds",
                    "Operational benchmarking, fault recovery, and static site export pipelines"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

        # Category 2: SVG Graphic Animation & Playwright Studio
        elif "Canvas_SVG_Capture_Templates" in path_str or "Canvas" in path_str:
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title="Automating Vector Motion: Headless SVG Canvas Capture with Termux Playwright",
                subtitle_hook="Building deterministic 60fps SVG animation seek pipelines and isometric brand asset generators.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="God Tier",
                core_subsystems=["SVG Canvas Stage", "BEJSON 105a Config", "Playwright Driver", "Frame Seek Timeline"],
                talking_points=[
                    "Why raster-based workflows fail on constrained devices and how vector canvas wins",
                    "Quantized 8-lane grids, Ry=32px rhythm, and Policy 8.1 Tri-Color compliance",
                    "Automating timeline seeking and high-DPI screenshots via playwright_canvas_studio.py",
                    "Embedding animated hero banners directly into BEHTML technical documentation"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

        # Category 3: Integrity Era Libraries (105 / 105a / 105db)
        elif "libraries_105" in path_str or "105" in name:
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title="The Integrity Era: Defeating Context Drift with BEJSON 105 UUID Fingerprints",
                subtitle_hook="How reserved record_uuid rows and field_uuid caches eliminate silent AI hallucinations.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="Advanced",
                core_subsystems=["UUID Fingerprints", "Field Map Cache", "Row Checksums", "E95 Guardrails"],
                talking_points=[
                    "The AI context corruption crisis in flat JSON arrays and unvalidated schemas",
                    "Architectural anatomy of Format 105: record_uuid offsets and field_uuid definitions",
                    "O(1) lookups via compiled by_name_row and by_uuid field map caching",
                    "Atomic POSIX migration from 104 to 105 without breaking backward compatibility"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

        # Category 4: Foundational Era Core Libraries (104 / 104a / 104db)
        elif "libraries_104" in path_str or "104" in name:
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title="Positional Telemetry: Zero-Overhead Memory Matrices in BEJSON 104",
                subtitle_hook="Stripping repetitive JSON keys for 80% token reduction across multi-agent pipelines.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="Intermediate",
                core_subsystems=["Positional Values", "Schema Fields", "Nested Core", "MFDB Manifests"],
                talking_points=[
                    "Token bloat in modern LLM function calling and nested JSON payloads",
                    "Separating Field declarations from positional row arrays in BEJSON 104",
                    "Hierarchical cell nesting using NestAddress(path, row, col, depth) up to depth 16",
                    "Benchmarking serialization throughput and memory efficiency against raw JSON"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

        # Category 5: Multi-File Database Federation (MFDB v1.31 / v1.40)
        elif "MFDB" in name.upper() or "site_master" in path_str:
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title="Relational Without SQL: Distributed Database Federation via MFDB",
                subtitle_hook="Linking cross-entity files with bidirectional Parent_Hierarchy manifests and foreign key cascades.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="God Tier",
                core_subsystems=["MFDB Manifest", "Foreign Keys", "Cascade Engine", "AES-GCM Encryption"],
                talking_points=[
                    "The challenge of relational integrity in distributed local-first applications",
                    "Master-Slave Network_Role federation in 104a.mfdb.bejson",
                    "Enforcing E39 referential integrity and fk_on_delete cascade behaviors",
                    "Tamper-proof Web Crypto ENC:AES-GCM encrypted cell persistence"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

        # General Autonomous Tools / Agent Systems
        elif any(k in name.lower() for k in ("agent", "launcher", "job", "newagent", "cli")):
            topic = ProposedBlogTopic(
                topic_index=current_topic_index,
                title=f"Autonomous Tooling on Linux: Dissecting {name}'s Runtime Engine",
                subtitle_hook="Decoupled daemons, single-instance locking, and resilient multi-step task execution.",
                target_path=path_str,
                category="BEJSON",
                difficulty_level="Intermediate",
                core_subsystems=["CLI Engine", "Daemon Lifecycle", "Resilient State", "Telemetry TUI"],
                talking_points=[
                    "Designing headless CLI utilities that survive mobile process termination",
                    "Self-locating preambles and zero-SDK REST API dispatch patterns",
                    "Building high-density 57-column terminal user interfaces (TUIs)",
                    "Hardening deployment scripts and automating system recovery"
                ]
            )
            proposed_topics_list.append(topic)
            current_topic_index += 1

    return proposed_topics_list


def format_proposals_catalog_markdown(
    proposed_topics_list: List[ProposedBlogTopic],
) -> str:
    """Render proposed topics into a clean, numbered Markdown catalog for user selection."""
    current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: List[str] = [
        "# Admin Recursive Topic Scout — Blog Subject Matter Catalog",
        f"\n> **Discovered Topics**: {len(proposed_topics_list)} | **Scanned Root**: `/storage/emulated/0/Admin` | **Generated**: {current_date}\n",
        "Select any topic by index number (e.g. `--select-topic 1`) to tune the plan prompt configuration.\n",
        "---",
    ]

    for topic in proposed_topics_list:
        lines.append(f"\n### [{topic.topic_index}] {topic.title}\n")
        lines.append(f"> **Hook**: *\"{topic.subtitle_hook}\"*\n")
        lines.append(f"- **Target Target**: `{topic.target_path}`")
        lines.append(f"- **Category / Difficulty**: `{topic.category}` | `{topic.difficulty_level}`")
        lines.append(f"- **Peripheral Canvas Nodes**: `{', '.join(topic.core_subsystems)}`")
        lines.append(f"- **Planned 4-Part Structure (>=120 lines each)**:")
        for idx, pt in enumerate(topic.talking_points, start=1):
            lines.append(f"  {idx}. Section {idx}: {pt}")
        lines.append("")

    lines.append("---\n")
    lines.append("## How to Select & Tune\n")
    lines.append("Run the scout with your chosen topic index to configure the 5-part plan prompt:\n")
    lines.append("```bash\npython3 ~/.gemini/config/skills/bejson-cms-admin-scout/scripts/admin_topic_scout.py \\\n  --select-topic 1 \\\n  --tune-config \"config/plan_config.104a.bejson\" \\\n  --generate-plan-prompt\n```\n")

    return "\n".join(lines)


def update_bejson_plan_configuration(
    target_config_file_path: Path,
    selected_topic: ProposedBlogTopic,
    minimum_lines_threshold: int = 120,
) -> Dict[str, Any]:
    """Generate or update BEJSON 104a plan prompt configuration."""
    peripheral_nodes_string = ",".join(selected_topic.core_subsystems)
    
    tuned_plan_prompt = (
        f"Execute Part 1 of the bejson-cms-blog-writer 5-part pipeline for: '{selected_topic.title}'.\n"
        f"Ground the plan in context researched from '{selected_topic.target_path}'.\n"
        f"Enforce mandatory target of at least {minimum_lines_threshold} lines per section (>=480 lines total).\n"
        f"Use category '{selected_topic.category}', author 'boehnenelton2024', and hero canvas '{peripheral_nodes_string}'."
    )

    bejson_104a_config_payload = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
        "Records_Type": ["PlanPromptConfig"],
        "Fields": [
            {"name": "setting_name", "type": "string"},
            {"name": "setting_value", "type": "any"},
            {"name": "description", "type": "string"}
        ],
        "Values": [
            ["selected_topic_index", selected_topic.topic_index, "Numerical index of chosen topic"],
            ["post_title", selected_topic.title, "Canonical publication title"],
            ["subtitle_hook", selected_topic.subtitle_hook, "Article hook and subtitle"],
            ["post_category", selected_topic.category, "Target CMS category name"],
            ["author_credit", "boehnenelton2024", "Author display name for CMS and footer credit"],
            ["min_lines_per_section", minimum_lines_threshold, "Mandatory minimum lines per section across all 4 sections"],
            ["target_context_path", selected_topic.target_path, "Filesystem path for Turn 0 context research"],
            ["hero_canvas_archetype", "hero_1280x640", "Visual layout archetype"],
            ["peripheral_components", peripheral_nodes_string, "Comma-separated 4 peripheral subsystem nodes"],
            ["plan_prompt_template", tuned_plan_prompt, "Tuned builder prompt for bejson-cms-blog-writer"]
        ]
    }

    target_config_file_path.parent.mkdir(parents=True, exist_ok=True)
    target_config_file_path.write_text(json.dumps(bejson_104a_config_payload, indent=2), encoding="utf-8")
    EXECUTION_LOGGER_INSTANCE.info("Tuned plan configuration saved to: %s", target_config_file_path)

    return bejson_104a_config_payload


def main() -> int:
    """Main CLI execution dispatch for Admin Topic Scout."""
    argument_parser_instance = argparse.ArgumentParser(
        description="Recursive Admin Topic Scout & Plan Configuration Tuner (Layer 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    argument_parser_instance.add_argument(
        "--scan-root",
        type=str,
        default=str(DEFAULT_ADMIN_ROOT_DIRECTORY_PATH),
        help="Root path to recursively scan for projects, repos, and libraries",
    )
    argument_parser_instance.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum directory recursion depth",
    )
    argument_parser_instance.add_argument(
        "--topics-output",
        type=str,
        default=None,
        help="File path to save the generated topic proposals Markdown catalog",
    )
    argument_parser_instance.add_argument(
        "--select-topic",
        type=int,
        default=None,
        help="Numerical index (1..N) of topic to select and tune",
    )
    argument_parser_instance.add_argument(
        "--tune-config",
        type=str,
        default="config/plan_config.104a.bejson",
        help="Destination path for the BEJSON 104a plan prompt configuration file",
    )
    argument_parser_instance.add_argument(
        "--min-lines",
        type=int,
        default=120,
        help="Target minimum lines per section for the tuned plan",
    )
    argument_parser_instance.add_argument(
        "--generate-plan-prompt",
        action="store_true",
        help="Output the finalized tuned builder prompt for bejson-cms-blog-writer",
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
        help="Display operational configuration parameters",
    )
    argument_parser_instance.add_argument(
        "--reset",
        action="store_true",
        help="Verify execution environment state",
    )

    parsed_cli_arguments = argument_parser_instance.parse_args()
    configure_execution_logging_subsystem()

    if parsed_cli_arguments.version:
        sys.stdout.write(f"admin_topic_scout v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.config:
        config_data = {
            "version": SYSTEM_SCRIPT_VERSION_INTEGER,
            "release_version": SYSTEM_RELEASE_VERSION_INTEGER,
            "author": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
            "default_scan_root": str(DEFAULT_ADMIN_ROOT_DIRECTORY_PATH),
            "default_max_depth": 4,
            "min_lines_per_section": 120,
        }
        sys.stdout.write(json.dumps(config_data, indent=2) + "\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.reset or parsed_cli_arguments.register:
        EXECUTION_LOGGER_INSTANCE.info("Scout environment verified.")
        return STATUS_CODE_SUCCESS_EXECUTION

    scan_root_path = Path(parsed_cli_arguments.scan_root).resolve()
    discovered_artifacts = scan_admin_directory_recursively(
        target_admin_root_path=scan_root_path,
        maximum_recursion_depth=parsed_cli_arguments.max_depth,
    )

    proposed_topics_list = synthesize_blog_proposals_from_artifacts(discovered_artifacts)
    EXECUTION_LOGGER_INSTANCE.info("Synthesized %d blog topic proposals from %d discovered artifacts.", len(proposed_topics_list), len(discovered_artifacts))

    # Output topics markdown catalog
    catalog_markdown = format_proposals_catalog_markdown(proposed_topics_list)
    output_catalog_path = Path(parsed_cli_arguments.topics_output) if parsed_cli_arguments.topics_output else Path("suggested_topics.md")
    try:
        output_catalog_path.parent.mkdir(parents=True, exist_ok=True)
        output_catalog_path.write_text(catalog_markdown, encoding="utf-8")
        EXECUTION_LOGGER_INSTANCE.info("Topics catalog successfully saved to: %s", output_catalog_path)
    except Exception as write_err:
        EXECUTION_LOGGER_INSTANCE.error("Failed to write catalog: %s", str(write_err))

    # If user selected a topic
    if parsed_cli_arguments.select_topic is not None:
        selected_index = parsed_cli_arguments.select_topic
        matched_topic: Optional[ProposedBlogTopic] = next((t for t in proposed_topics_list if t.topic_index == selected_index), None)
        if not matched_topic:
            EXECUTION_LOGGER_INSTANCE.error("Topic index [%d] not found in catalog (available: 1..%d)", selected_index, len(proposed_topics_list))
            return STATUS_CODE_VALIDATION_ERROR_EXECUTION

        target_config_path = Path(parsed_cli_arguments.tune_config)
        bejson_config = update_bejson_plan_configuration(
            target_config_file_path=target_config_path,
            selected_topic=matched_topic,
            minimum_lines_threshold=parsed_cli_arguments.min_lines,
        )

        if parsed_cli_arguments.generate_plan_prompt:
            prompt_str = bejson_config["Values"][9][1]
            sys.stdout.write(f"\n=======================================================\n")
            sys.stdout.write(f"TUNED BUILDER PROMPT FOR BEJSON CMS BLOG WRITER\n")
            sys.stdout.write(f"=======================================================\n\n")
            sys.stdout.write(f"{prompt_str}\n\n")
            sys.stdout.write(f"Turnkey Execution Commands:\n")
            sys.stdout.write(
                f"1. python3 ~/.gemini/config/skills/bejson-cms-blog-writer/scripts/cms_context_researcher.py \\\n"
                f"     --target-path \"{matched_topic.target_path}\" \\\n"
                f"     --output \"00_context_research.md\"\n\n"
                f"2. python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \\\n"
                f"     --context-file \"00_context_research.md\" \\\n"
                f"     --output \"hero.svg\"\n\n"
            )

    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
