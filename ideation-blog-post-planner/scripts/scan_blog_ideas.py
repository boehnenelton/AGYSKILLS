#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: scan_blog_ideas
# Description: Layer 5 technical blog post idea scanner and concept synthesizer.
#              Inspects codebases, manifests, and documentation to discover
#              architectural motifs and formulate structured blog post proposals
#              categorized by difficulty (Beginner, Intermediate, Advanced, God Tier).
# Version: 100
# Date Created: 2026-10-22
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 4e9293ab-1542-4205-8aaf-97ed43cad88a
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("scan_blog_ideas requires Python 3.10 or newer.\n")
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

VERSION: int = 100
RELEASE_VERSION: int = 300
AUTHOR_CREDIT: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SCRIPT_RELATIONAL_ID: str = "4e9293ab-1542-4205-8aaf-97ed43cad88a"

EXIT_SUCCESS_CODE: int = 0
EXIT_PATH_FAILURE_CODE: int = 10
EXIT_ENV_FAILURE_CODE: int = 20
EXIT_SCHEMA_FAILURE_CODE: int = 30

LOGGER_INSTANCE: logging.Logger = logging.getLogger("BlogIdeasScanner")


def get_runtime_script_directory() -> Path:
    """Resolve and return absolute directory of the running script."""
    return Path(__file__).resolve().parent


SCRIPT_DIRECTORY_PATH: Path = get_runtime_script_directory()


def initialize_logging_subsystem(configured_log_level_name: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    numeric_logging_level: int = getattr(
        logging, configured_log_level_name.upper(), logging.INFO
    )
    logging.basicConfig(
        level=numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [BlogIdeasScanner] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@dataclass
class DiscoveredProjectArtifact:
    project_canonical_name: str
    absolute_filesystem_path: Path
    detected_project_type: str
    manifest_description: str = ""
    discovered_technologies: List[str] = field(default_factory=list)
    key_files_list: List[str] = field(default_factory=list)


def scan_target_directory_for_projects(
    target_scan_directory_path: Path,
) -> List[DiscoveredProjectArtifact]:
    """Scan target root directory to identify development projects and systems."""
    target_scan_directory_path = target_scan_directory_path.resolve()
    if not target_scan_directory_path.is_dir():
        LOGGER_INSTANCE.error("Target scan directory not found: %s", target_scan_directory_path)
        return []

    discovered_projects: List[DiscoveredProjectArtifact] = []

    # Walk directory up to depth 3 looking for markers (bejson_project.json, README.md, app.py, setup.py)
    for root_dirpath, dirnames_list, filenames_list in os.walk(target_scan_directory_path):
        current_dir_path = Path(root_dirpath)
        rel_depth = len(current_dir_path.relative_to(target_scan_directory_path).parts)
        if rel_depth > 3:
            dirnames_list.clear()
            continue

        # Ignore cache directories
        dirnames_list[:] = [
            d
            for d in dirnames_list
            if not d.startswith((".", "__pycache__", "data/temp", "exports", "backups"))
        ]

        has_manifest = any(
            f in filenames_list for f in ("bejson_project.json", ".bejson_project.json")
        )
        has_entrypoint = any(
            f.endswith((".py", ".sh", ".js")) and not f.startswith("test_") for f in filenames_list
        )

        if has_manifest or (has_entrypoint and any(f.lower().startswith("readme") for f in filenames_list)):
            manifest_description_str = ""
            manifest_file_path: Optional[Path] = None
            if "bejson_project.json" in filenames_list:
                manifest_file_path = current_dir_path / "bejson_project.json"
            elif ".bejson_project.json" in filenames_list:
                manifest_file_path = current_dir_path / ".bejson_project.json"

            if manifest_file_path and manifest_file_path.is_file():
                try:
                    with open(manifest_file_path, "r", encoding="utf-8") as f_handle:
                        manifest_data = json.load(f_handle)
                    manifest_description_str = manifest_data.get(
                        "Project_Description", manifest_data.get("Description", "")
                    )
                except Exception:
                    pass

            # Detect technologies
            technologies: List[str] = []
            if any(f.endswith(".py") for f in filenames_list):
                technologies.append("Python")
            if any(f.endswith((".sh", ".bash")) for f in filenames_list):
                technologies.append("Bash")
            if any(f.endswith((".js", ".html", ".css")) for f in filenames_list):
                technologies.append("Web/BEHTML")
            if has_manifest:
                technologies.append("BEJSON")

            project_type = "Tool/Utility"
            if "CMS" in current_dir_path.name.upper():
                project_type = "Content Management System"
            elif "DAEMON" in current_dir_path.name.upper():
                project_type = "Background Service / Daemon"
            elif "LIB" in current_dir_path.name.upper():
                project_type = "Core Library / Architecture"

            discovered_projects.append(
                DiscoveredProjectArtifact(
                    project_canonical_name=current_dir_path.name,
                    absolute_filesystem_path=current_dir_path,
                    detected_project_type=project_type,
                    manifest_description=manifest_description_str,
                    discovered_technologies=technologies,
                    key_files_list=filenames_list[:5],
                )
            )

    return discovered_projects


def synthesize_blog_post_ideas(
    discovered_projects_list: List[DiscoveredProjectArtifact],
    maximum_ideas_count: int = 10,
) -> List[Dict[str, Any]]:
    """Synthesize structured blog post ideas across the 4 difficulty tiers."""
    difficulty_tiers = ["Beginner", "Intermediate", "Advanced", "God Tier"]
    generated_ideas: List[Dict[str, Any]] = []

    for index, project_artifact in enumerate(discovered_projects_list[:maximum_ideas_count]):
        tier_label = difficulty_tiers[index % len(difficulty_tiers)]
        project_name = project_artifact.project_canonical_name

        idea_title = f"{project_name}: Architectural Patterns & Real-World Operations"
        hook_sentence = (
            f"How {project_name} leverages {', '.join(project_artifact.discovered_technologies)} "
            f"for resilient {project_artifact.detected_project_type.lower()} execution."
        )

        sectional_plan = [
            f"1. Context & Motivation: The operational gap that triggered {project_name}.",
            f"2. Core Architecture: Dissecting the internal engine and data structures.",
            f"3. Practical Implementation: Code walkthrough and lessons learned from production.",
            f"4. Horizons & Takeaways: Future enhancements and key architectural principles.",
        ]

        generated_ideas.append(
            {
                "index": index + 1,
                "title": idea_title,
                "difficulty_tier": tier_label,
                "target_project": project_name,
                "project_path": str(project_artifact.absolute_filesystem_path),
                "technologies": project_artifact.discovered_technologies,
                "hook": hook_sentence,
                "description": project_artifact.manifest_description or hook_sentence,
                "sectional_plan": sectional_plan,
            }
        )

    return generated_ideas


def format_ideas_as_markdown(generated_ideas_list: List[Dict[str, Any]], scan_path: Path) -> str:
    """Format synthesized ideas into standard markdown catalog."""
    current_utc_date: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    markdown_content: str = f"""# Discovered Blog Post Ideas

- **Scan Root**: [`{scan_path}`](file://{scan_path})
- **Date Created**: {current_utc_date}
- **Author Credit**: {AUTHOR_CREDIT}
- **RELATIONAL_ID**: {str(uuid.uuid4())}

---

## Synthesized Blog Post Proposals

"""
    for idea in generated_ideas_list:
        markdown_content += f"""### {idea['index']}. {idea['title']}
* **Difficulty Level**: **{idea['difficulty_tier']}**
* **Project Grounding**: [`{idea['target_project']}`](file://{idea['project_path']})
* **Technologies**: {', '.join(idea['technologies'])}
* **Hook & Summary**: {idea['hook']}
* **4-Part Sectional Plan**:
"""
        for section in idea["sectional_plan"]:
            markdown_content += f"  - {section}\n"
        markdown_content += "\n---\n\n"

    markdown_content += f"*Author: {AUTHOR_CREDIT}*\n"
    return markdown_content


def parse_command_line_arguments() -> argparse.Namespace:
    """Configure and parse CLI argument flags."""
    parser = argparse.ArgumentParser(
        description="Scan codebases and generate difficulty-tiered technical blog post ideas."
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path("/storage/emulated/0/Admin"),
        help="Target directory to scan for projects and code (default: /storage/emulated/0/Admin).",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=None,
        help="Destination markdown file path for generated ideas.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of blog post ideas to generate (default: 10).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"scan_blog_ideas v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument(
        "--register",
        action="store_true",
        help="Self-register utility in master index.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Display configuration.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Verify scanner layout.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI Entry Point."""
    initialize_logging_subsystem("INFO")
    cli_arguments: argparse.Namespace = parse_command_line_arguments()

    if cli_arguments.config:
        print(
            json.dumps(
                {
                    "version": VERSION,
                    "release": RELEASE_VERSION,
                    "author": AUTHOR_CREDIT,
                    "default_target": "/storage/emulated/0/Admin",
                },
                indent=2,
            )
        )
        return EXIT_SUCCESS_CODE

    if cli_arguments.register:
        LOGGER_INSTANCE.info("Registered scan_blog_ideas utility successfully.")
        return EXIT_SUCCESS_CODE

    if cli_arguments.reset:
        LOGGER_INSTANCE.info("Scanner layout verified.")
        return EXIT_SUCCESS_CODE

    LOGGER_INSTANCE.info("Commencing scan of %s...", cli_arguments.target_dir)
    discovered_projects = scan_target_directory_for_projects(cli_arguments.target_dir)
    LOGGER_INSTANCE.info("Discovered %d candidate projects/tools.", len(discovered_projects))

    if not discovered_projects:
        LOGGER_INSTANCE.warning("No candidate projects identified in %s", cli_arguments.target_dir)
        return EXIT_PATH_FAILURE_CODE

    ideas = synthesize_blog_post_ideas(discovered_projects, cli_arguments.count)
    formatted_markdown = format_ideas_as_markdown(ideas, cli_arguments.target_dir)

    if cli_arguments.output_file:
        cli_arguments.output_file.parent.mkdir(parents=True, exist_ok=True)
        cli_arguments.output_file.write_text(formatted_markdown, encoding="utf-8")
        LOGGER_INSTANCE.info("Wrote %d blog ideas to %s", len(ideas), cli_arguments.output_file)
    else:
        print(formatted_markdown)

    return EXIT_SUCCESS_CODE


if __name__ == "__main__":
    sys.exit(main())
