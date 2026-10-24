#!/usr/bin/env python3
"""
==============================================================================
Name: agy_project_randomizer.py
Description: Autonomous Multi-Project Randomization Engine for Antigravity CLI (agy).
             Periodically selects a random project directory from a root tree,
             picks a randomized workflow (Reports, Audits, Ideation, Schemas, Instructions),
             creates target subdirectories, and executes headless prompts on randomized timers.
Version: 1.0.0
Author: Elton Boehnen
Date: 2026-09-06
Target: Python 3.10+
RELATIONAL_ID: e4c99e12-4217-482a-bc81-88f110c73a49
==============================================================================
"""

import os
import sys
import time
import random
import logging
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

# Enforce Python 3.10+
if sys.version_info < (3, 10):
    sys.stderr.write("Fatal: Requires Python 3.10 or higher.\n")
    sys.exit(1)

# Configure Standard Logging (Zero print() statements)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("agy_project_randomizer")

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()

# ==============================================================================
# WORKFLOW DEFINITIONS & PROMPT TEMPLATES
# ==============================================================================

WORKFLOW_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "reports": {
        "target_subfolder": "reports",
        "description": "Generates structured project reports into <project>/reports/",
        "prompts": [
            "[SURGICAL] Inspect the codebase in this project directory. Generate an Architectural Health & Dependency Report summarizing active modules, libraries in lib/, and entry points. Save the report to reports/architecture_overview_{TIMESTAMP}.md.",
            "[PLAN] Review recent commits and file change timestamps. Compile a Project Status & Workstream Progress Report highlighting recent feature deliveries. Save to reports/status_report_{TIMESTAMP}.md.",
            "[HOSTILE-AUDIT] Analyze data flow and external integrations in this project. Generate an Integration Surface & API Exposure Report detailing endpoints, env variable usage, and network calls. Save to reports/api_surface_report_{TIMESTAMP}.md.",
            "Inspect codebase structure and class hierarchies. Generate a complete Technical Overview Report documenting key functions in the format 'File_Name / Function_Name (var1, var2)'. Save to reports/technical_overview_{TIMESTAMP}.md."
        ]
    },
    "audits": {
        "target_subfolder": "reports/audits",
        "description": "Performs deep security, logic, and schema audits into <project>/reports/audits/ and <project>/dev/",
        "prompts": [
            "[HOSTILE-AUDIT] Perform an exhaustive Security & Vulnerability Audit on all source files. Check for hardcoded credentials, unsanitized inputs, insecure subprocess calls, and path traversal risks. Append findings to dev/security-notes.md and save full audit to reports/audits/security_audit_{TIMESTAMP}.md.",
            "[DEAD-CODE-PURGE] Audit the codebase for uncalled functions, obsolete imports, and dead variables. List confirmed dead code candidates in dev/dead_code.md with precise file and line numbers.",
            "[BEJSON-104] Verify all .bejson and .json data files in this project. Check that every BEJSON file adheres to the 6 mandatory top-level keys, positional integrity, and field map caching standards. Save report to reports/audits/bejson_schema_audit_{TIMESTAMP}.md.",
            "[BECSS-BEM] Audit all UI templates, HTML, and CSS files in this project. Verify strict adherence to the Tri-Color Law (#000000, #FFFFFF, #DE2626) and becss- BEM naming syntax. Save findings to reports/audits/ui_style_audit_{TIMESTAMP}.md."
        ]
    },
    "ideas": {
        "target_subfolder": "target/ideas",
        "description": "Generates feature brainstorms, expansion specs, and ideation-feature-composer menus into <project>/target/ideas/",
        "prompts": [
            "Act as a system architect. Analyze the core utility of this project and generate an exhaustive numbered menu of 25 novel feature enhancements, automation hooks, and UI workflow extensions. Save the feature menu to target/ideas/feature_expansion_menu_{TIMESTAMP}.md.",
            "Brainstorm 10 advanced CLI automation flags and background worker capabilities that could be added to this project. Provide concise architectural rationale for each. Save to target/ideas/cli_automation_ideas_{TIMESTAMP}.md.",
            "Analyze current bottlenecks or repetitive steps in this project. Formulate 5 zero-dependency helper utilities or subagent workflows to streamline execution. Save to target/ideas/workflow_optimizations_{TIMESTAMP}.md."
        ]
    },
    "schemas_instructions": {
        "target_subfolder": "target/schemas",
        "description": "Produces BEJSON schemas and LLM agent instruction prompt sets into <project>/target/schemas/",
        "prompts": [
            "[BEJSON-104A] Analyze the configuration and runtime settings required by this project. Construct a valid BEJSON 104a configuration schema and initial dataset adhering strictly to Elton Boehnen's specification. Save to target/schemas/config_registry_{TIMESTAMP}.104a.bejson.",
            "Formulate a specialized Agent Instruction Set & System Prompt for an autonomous subagent dedicated to maintaining and testing this specific codebase. Save the prompt file to target/schemas/agent_system_instructions_{TIMESTAMP}.md.",
            "[BEJSON-104] Define a complete BEJSON 104 entity schema and taxonomy definition for the primary data models manipulated by this project. Include field types and cached field map logic. Save to target/schemas/entity_model_{TIMESTAMP}.104.bejson."
        ]
    }
}

# ==============================================================================
# CORE RANDOMIZATION & EXECUTION ENGINE
# ==============================================================================

def discover_project_folders(root_dir: Path) -> List[Path]:
    """Finds eligible project subdirectories within the root directory."""
    if not root_dir.exists() or not root_dir.is_dir():
        logger.error("Root directory does not exist or is not a directory: %s", root_dir)
        return []

    candidates: List[Path] = []
    # Check immediate child directories
    try:
        children = [d for d in root_dir.iterdir() if d.is_dir() and not d.name.startswith((".", "__"))]
    except (PermissionError, OSError) as e:
        logger.warning("Could not list directory %s: %s", root_dir, e)
        return []

    for child in children:
        try:
            has_markers = any((
                (child / ".bejson_project.json").exists(),
                (child / "bejson_project.json").exists(),
                (child / ".git").exists(),
                (child / "src").exists(),
                (child / "lib").exists(),
                any(child.glob("*.py")),
                any(child.glob("*.sh"))
            ))
            if has_markers:
                candidates.append(child)
            else:
                # Also allow subfolders if child is a category folder
                try:
                    for sub in child.iterdir():
                        if sub.is_dir() and not sub.name.startswith((".", "__")):
                            candidates.append(sub)
                except (PermissionError, OSError):
                    pass
        except (PermissionError, OSError):
            continue

    if not candidates:
        candidates = children

    return candidates

def execute_random_task(project_dir: Path, category_filter: Optional[str] = None, dry_run: bool = False) -> bool:
    """Selects a random category, ensures subfolder exists, and executes agy."""
    categories = [category_filter] if category_filter and category_filter in WORKFLOW_CATEGORIES else list(WORKFLOW_CATEGORIES.keys())
    selected_cat_name = random.choice(categories)
    cat_data = WORKFLOW_CATEGORIES[selected_cat_name]

    # Resolve target subfolder inside project
    target_dir = project_dir / cat_data["target_subfolder"]
    target_dir.mkdir(parents=True, exist_ok=True)

    # Select random prompt and interpolate timestamp
    raw_prompt = random.choice(cat_data["prompts"])
    timestamp_str = time.strftime("%Y%m%d_%H%M%S")
    formatted_prompt = raw_prompt.replace("{TIMESTAMP}", timestamp_str)

    logger.info("----------------------------------------------------------------------")
    logger.info("Selected Project: %s", project_dir.name)
    logger.info("Category: %s", selected_cat_name)
    logger.info("Target Subfolder: %s", target_dir)
    logger.info("Prompt: %s", formatted_prompt)
    logger.info("----------------------------------------------------------------------")

    if dry_run:
        logger.info("[DRY RUN] Skipping actual agy execution.")
        return True

    # Invoke Antigravity CLI in headless mode targeting the project directory
    cmd = [
        "agy",
        "--sandbox",
        f"--dir={str(project_dir)}",
        "-p",
        formatted_prompt
    ]

    try:
        start_t = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        elapsed = time.time() - start_t
        logger.info("Task completed successfully in %.2fs.", elapsed)
        if res.stdout:
            preview = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""
            logger.info("Output Summary: %s", preview[:140])
        return True
    except subprocess.CalledProcessError as err:
        logger.error("agy execution failed (Exit code %d): %s", err.returncode, err.stderr.strip())
        return False
    except FileNotFoundError:
        logger.error("Antigravity CLI executable ('agy') not found in PATH.")
        return False

def run_automation_loop(
    root_dir: Path,
    min_delay: int,
    max_delay: int,
    category: Optional[str] = None,
    once: bool = False,
    dry_run: bool = False
):
    """Main dispatch loop with randomized timing and project rotation."""
    logger.info("======================================================================")
    logger.info("Antigravity Autonomous Project Dispatcher")
    logger.info("Root Directory: %s", root_dir)
    logger.info("Interval Delay: %ds - %ds", min_delay, max_delay)
    logger.info("Mode: %s", "Single-Shot" if once else "Continuous Heartbeat Loop")
    logger.info("======================================================================")

    while True:
        projects = discover_project_folders(root_dir)
        if not projects:
            logger.warning("No project folders discovered under: %s. Retrying in 30s...", root_dir)
            if once:
                break
            time.sleep(30)
            continue

        selected_project = random.choice(projects)
        execute_random_task(selected_project, category_filter=category, dry_run=dry_run)

        if once:
            logger.info("Single-shot execution complete. Exiting.")
            break

        # Compute randomized jitter sleep
        sleep_sec = random.randint(min_delay, max_delay)
        logger.info("Heartbeat sleeping for %d seconds (~%.1f mins)...", sleep_sec, sleep_sec / 60.0)
        time.sleep(sleep_sec)

# ==============================================================================
# CLI PARSER ENTRYPOINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Autonomous Project Randomizer for Antigravity CLI (agy)")
    parser.add_argument("--root-dir", type=str, default=os.environ.get("PROJECT_ROOT", "."), help="Path to parent folder containing projects")
    parser.add_argument("--min-delay", type=int, default=60, help="Minimum sleep interval between tasks in seconds (default: 60)")
    parser.add_argument("--max-delay", type=int, default=300, help="Maximum sleep interval between tasks in seconds (default: 300)")
    parser.add_argument("--category", type=str, choices=list(WORKFLOW_CATEGORIES.keys()), help="Constrain to a specific workflow category")
    parser.add_argument("--once", action="store_true", help="Execute exactly one randomized task and exit")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without executing agy")
    args = parser.parse_args()

    root_path = Path(args.root_dir).resolve()
    run_automation_loop(
        root_dir=root_path,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        category=args.category,
        once=args.once,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
