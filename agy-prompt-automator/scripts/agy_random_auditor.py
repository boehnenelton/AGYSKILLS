#!/usr/bin/env python3
"""
==============================================================================
Name: agy_random_auditor.py
Description: Autonomous Antigravity CLI Targeted Auditor with Subfolder & Audit
             Randomization. Targets a chosen project directory, selects a random
             subfolder (or specific module), chooses a random specialized audit type,
             invokes headless agy with --sandbox, and leaves a
             structured audit report in the project's reports/ directory.
Version: 1.0.0
Author: Elton Boehnen
Date: 2026-09-06
Target: Python 3.10+
RELATIONAL_ID: 871a942b-e104-4b52-b883-fa4c02967911
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

# Standard logging (zero print statements)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("agy_random_auditor")

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()

# ==============================================================================
# SPECIALIZED AUDIT TYPES & DIRECTIVES
# ==============================================================================

AUDIT_TYPES: Dict[str, Dict[str, Any]] = {
    "security_hostile": {
        "name": "Hostile Security & Credential Leak Audit",
        "directive": "[HOSTILE-AUDIT]",
        "focus": (
            "Scan for hardcoded API keys, exposed tokens, unsanitized inputs, "
            "insecure subprocess execution, command injection vulnerabilities, "
            "and unsafe file operations. Append any confirmed vulnerabilities to dev/security-notes.md."
        ),
        "report_prefix": "security_audit"
    },
    "dead_code_purge": {
        "name": "Dead Code & Unused Reference Audit",
        "directive": "[DEAD-CODE-PURGE]",
        "focus": (
            "Identify unreferenced functions, obsolete imports, dead variables, "
            "and unreachable code paths. Detail exact candidate locations with file and line numbers, "
            "and append entries to dev/dead_code.md."
        ),
        "report_prefix": "dead_code_audit"
    },
    "bejson_schema_integrity": {
        "name": "BEJSON 104/104a Positional & Schema Integrity Audit",
        "directive": "[BEJSON-104]",
        "focus": (
            "Verify all .bejson and data files. Enforce the 6 mandatory top-level keys, "
            "Format_Creator='Elton Boehnen', positional integrity across Values, "
            "explicit null padding, and O(1) Field Map Cache usage instead of index lookups."
        ),
        "report_prefix": "bejson_integrity_audit"
    },
    "becss_ui_conformance": {
        "name": "BECSS BEM & Tri-Color Law Conformance Audit",
        "directive": "[BECSS-BEM]",
        "focus": (
            "Audit all UI templates, HTML, Jinja2, and CSS files. Verify strict adherence "
            "to the Tri-Color Law (#000000 Black, #FFFFFF White, #DE2626 Red) and becss- BEM syntax "
            "(block__element--modifier). Flag all non-BEM floating state classes and illegal BEM nesting."
        ),
        "report_prefix": "becss_ui_audit"
    },
    "concurrency_race_conditions": {
        "name": "Concurrency, Race Condition & File Lock Audit",
        "directive": "[HOSTILE-AUDIT]",
        "focus": (
            "Examine state persistence, file writes, and asynchronous subprocesses. "
            "Audit for TOCTOU file races, non-atomic writes without temporary sync/replace, "
            "and missing advisory locks in daemon routines."
        ),
        "report_prefix": "concurrency_race_audit"
    },
    "path_portability_check": {
        "name": "Path Portability & SCRIPT_PATH Sourcing Audit",
        "directive": "[SURGICAL]",
        "focus": (
            "Check all scripts for hardcoded absolute paths. Verify that every executable "
            "dynamically resolves its own location via SCRIPT_PATH = Path(__file__).resolve().parent "
            "and sources environment files properly."
        ),
        "report_prefix": "path_portability_audit"
    },
    "error_handling_and_logging": {
        "name": "Error Handling, Exit Codes & Logging Audit",
        "directive": "[SURGICAL]",
        "focus": (
            "Check for silent failures or unhandled exceptions. Verify that print() is NEVER used "
            "for logging (standard logging module enforced) and that Termux/API degradation "
            "uses deterministic exit codes (0, 10, 20, 30)."
        ),
        "report_prefix": "error_logging_audit"
    },
    "lifecycle_and_versioning": {
        "name": "Lifecycle Parity & Versioning Audit",
        "directive": "[SURGICAL]",
        "focus": (
            "Verify single VERSION variable at the top of every file, fresh RELATIONAL_ID UUIDs, "
            "single write-ownership per entity, and single factory-reset parity across entry points."
        ),
        "report_prefix": "lifecycle_versioning_audit"
    }
}

# ==============================================================================
# SUBFOLDER DISCOVERY & AUDIT RUNNER
# ==============================================================================

EXCLUDED_DIR_NAMES = {
    ".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules",
    ".idea", ".vscode", "reports", "output", ".bejson_project.json"
}

def discover_subfolders(project_dir: Path) -> List[Path]:
    """Discovers eligible subfolders within the project directory."""
    if not project_dir.exists() or not project_dir.is_dir():
        logger.error("Project directory does not exist: %s", project_dir)
        return []

    eligible: List[Path] = []
    try:
        for p in project_dir.iterdir():
            if p.is_dir() and p.name not in EXCLUDED_DIR_NAMES and not p.name.startswith((".", "__")):
                eligible.append(p)
                # Also include depth 2 subfolders if present (e.g. src/lib)
                try:
                    for sub in p.iterdir():
                        if sub.is_dir() and sub.name not in EXCLUDED_DIR_NAMES and not sub.name.startswith((".", "__")):
                            eligible.append(sub)
                except (PermissionError, OSError):
                    pass
    except (PermissionError, OSError) as e:
        logger.warning("Error inspecting subdirectories in %s: %s", project_dir, e)

    # If no subfolders found, fallback to the project root itself
    if not eligible:
        eligible = [project_dir]

    return eligible

def run_single_audit(
    project_dir: Path,
    subfolder_target: Optional[str] = None,
    audit_type_choice: Optional[str] = None,
    custom_output_dir: Optional[str] = None,
    dry_run: bool = False
) -> bool:
    """Selects a random subfolder and audit type, builds prompt, and runs agy."""
    # 1. Resolve target subfolder
    if subfolder_target and subfolder_target.lower() != "random":
        target_sub = project_dir / subfolder_target
        if not target_sub.exists():
            logger.warning("Requested subfolder '%s' does not exist. Using project root.", subfolder_target)
            target_sub = project_dir
    else:
        candidates = discover_subfolders(project_dir)
        target_sub = random.choice(candidates)

    rel_sub_path = target_sub.relative_to(project_dir) if target_sub != project_dir else Path(".")
    sub_slug = str(rel_sub_path).replace(os.sep, "_").strip("._")
    if not sub_slug:
        sub_slug = "root"

    # 2. Select audit type
    if audit_type_choice and audit_type_choice in AUDIT_TYPES:
        selected_key = audit_type_choice
    else:
        selected_key = random.choice(list(AUDIT_TYPES.keys()))
    
    audit_cfg = AUDIT_TYPES[selected_key]
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # 3. Resolve report destination folder inside the project
    if custom_output_dir:
        report_dir = project_dir / custom_output_dir
    else:
        # Save into reports/audits/ or dedicated reports/<audit_type>/
        report_dir = project_dir / "reports" / "audits"
    
    report_dir.mkdir(parents=True, exist_ok=True)
    report_filename = f"{audit_cfg['report_prefix']}_{sub_slug}_{timestamp}.md"
    report_file_rel = report_dir.relative_to(project_dir) / report_filename

    # 4. Formulate prompt for agy
    target_clause = f"Target Scope: Files inside '{rel_sub_path}'." if rel_sub_path != Path(".") else "Target Scope: All project files."
    prompt = (
        f"{audit_cfg['directive']} You are an autonomous code auditor. {target_clause} "
        f"Perform an exhaustive '{audit_cfg['name']}'. Focus: {audit_cfg['focus']} "
        f"Instructions: (1) Scan all target files in scope, (2) Document each finding with file name, "
        f"line number, severity (CRITICAL, HIGH, MEDIUM, LOW), and technical impact, "
        f"(3) Provide minimal surgical code fixes for each finding, (4) Output the full structured audit report "
        f"directly to '{report_file_rel}'."
    )

    logger.info("======================================================================")
    logger.info("Project:       %s", project_dir.resolve())
    logger.info("Target Subdir: %s (%s)", target_sub.name, rel_sub_path)
    logger.info("Audit Type:    %s (%s)", audit_cfg['name'], selected_key)
    logger.info("Report File:   %s", report_file_rel)
    logger.info("Prompt Preview: %s", prompt[:160] + "...")
    logger.info("======================================================================")

    if dry_run:
        logger.info("[DRY RUN] Skipping agy subprocess call.")
        return True

    # 5. Execute agy headlessly targeting the project directory
    cmd = [
        "agy",
        "--sandbox",
        f"--dir={str(project_dir.resolve())}",
        "-p",
        prompt
    ]

    try:
        t0 = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        elapsed = time.time() - t0
        logger.info("Audit complete in %.2fs. Report written to: %s", elapsed, report_file_rel)
        return True
    except subprocess.CalledProcessError as err:
        logger.error("agy audit failed with code %d: %s", err.returncode, err.stderr.strip())
        return False
    except FileNotFoundError:
        logger.error("Antigravity CLI ('agy') binary not found in PATH.")
        return False

# ==============================================================================
# CLI PARSER & LOOP DISPATCHER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Autonomous Antigravity CLI Subfolder & Audit Randomizer")
    parser.add_argument("--project", type=str, default=".", help="Target project directory path (default: current directory)")
    parser.add_argument("--subfolder", type=str, default="random", help="Specific subfolder to audit, or 'random' to pick one automatically")
    parser.add_argument("--audit-type", type=str, choices=list(AUDIT_TYPES.keys()) + ["random"], default="random", help="Specific audit type or 'random'")
    parser.add_argument("--output-dir", type=str, default="reports/audits", help="Subdirectory inside project where report is saved")
    parser.add_argument("--loop-minutes", type=float, default=0, help="If > 0, run continuously with randomized jitter on an N-minute loop")
    parser.add_argument("--min-minutes", type=float, default=2.0, help="Minimum delay in minutes for continuous loop")
    parser.add_argument("--max-minutes", type=float, default=10.0, help="Maximum delay in minutes for continuous loop")
    parser.add_argument("--dry-run", action="store_true", help="Log chosen project, subfolder, and prompt without executing agy")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()
    if not project_path.exists() or not project_path.is_dir():
        logger.error("Invalid project directory: %s", project_path)
        sys.exit(1)

    audit_type = None if args.audit_type == "random" else args.audit_type

    if args.loop_minutes > 0 or (args.min_minutes > 0 and args.max_minutes > args.min_minutes and not args.dry_run and args.loop_minutes < 0):
        interval_min = args.loop_minutes if args.loop_minutes > 0 else args.min_minutes
        interval_max = args.loop_minutes if args.loop_minutes > 0 else args.max_minutes
        logger.info("Starting continuous audit daemon on '%s'. Interval: %.1f to %.1f mins.",
                    project_path.name, interval_min, interval_max)
        while True:
            run_single_audit(
                project_dir=project_path,
                subfolder_target=args.subfolder,
                audit_type_choice=audit_type,
                custom_output_dir=args.output_dir,
                dry_run=args.dry_run
            )
            delay_mins = random.uniform(interval_min, interval_max)
            logger.info("Pausing for %.2f minutes (~%.0f seconds)...", delay_mins, delay_mins * 60.0)
            time.sleep(delay_mins * 60.0)
    else:
        run_single_audit(
            project_dir=project_path,
            subfolder_target=args.subfolder,
            audit_type_choice=audit_type,
            custom_output_dir=args.output_dir,
            dry_run=args.dry_run
        )

if __name__ == "__main__":
    main()
