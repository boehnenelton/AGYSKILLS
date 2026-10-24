#!/usr/bin/env python3
"""
==============================================================================
Name: agy_subject_list_automator.py
Description: Subject-Specific Function, Library, and Idea List Automator for agy.
             Runs automated prompt routines on configurable minute-based timers,
             generating modular library functions, feature menus, and schemas
             organized into subject-specific target subdirectories.
Version: 1.0.0
Author: Elton Boehnen
Date: 2026-09-06
Target: Python 3.10+
RELATIONAL_ID: d3a98071-71e4-4a52-b883-fa4c02967201
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
logger = logging.getLogger("agy_subject_automator")

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()

# ==============================================================================
# SUBJECT DOMAINS & GENERATION WORKFLOWS
# ==============================================================================

SUBJECT_DOMAINS: Dict[str, Dict[str, Any]] = {
    "bejson_data_architecture": {
        "display_name": "BEJSON Data Architecture & MFDB",
        "description": "High-throughput tabular data, field map caching, and multi-file databases",
        "library_family": "lib_bejson_Core",
        "function_topics": [
            "Atomic file writer with sync buffer flushing and rename replacement",
            "Field Map Cache compiler for O(1) column resolution from Fields definition",
            "Nested 104 cell serializer and dotted path query evaluator",
            "MFDB manifest 104a validator and entity file discoverer",
            "Boundary-layer whitespace sanitizer for ingestion pipelines"
        ],
        "list_topics": [
            "Exhaustive 30-point menu of BEJSON database utility commands and validation tools",
            "Inventory of 20 edge cases and corruption vectors in tabular JSON serialization",
            "Catalog of 15 schema migration patterns preserving positional integrity"
        ]
    },
    "android_termux_systems": {
        "display_name": "Android & Termux System Automation",
        "description": "Linux environment on Android, storage synchronization, and shell tools",
        "library_family": "lib_bejson_Termux",
        "function_topics": [
            "Android file picker invocation via Termux API with deterministic timeout exit codes",
            "Storage synchronization daemon syncing /storage/emulated/0 with local app directories",
            "Termux wake-lock manager ensuring uninterrupted background processing",
            "Termux toast and notification dispatcher for headless task completion alerts",
            "Subprocess launcher opening default browser via termux-open before server binding"
        ],
        "list_topics": [
            "Exhaustive 25-point menu of Termux CLI productivity tools and daemon services",
            "Checklist of 15 Android filesystem permissions and storage boundary edge cases",
            "Taxonomy of 20 background automation tasks suitable for continuous heartbeat execution"
        ]
    },
    "spatial_ui_and_becss": {
        "display_name": "Spatial UI & BECSS Design Architecture",
        "description": "8-lane grid systems, Ry=32px quantization, and Tri-Color Law styling",
        "library_family": "lib_bejson_BEHTML",
        "function_topics": [
            "8-lane coordinate collision validator verifying x_start + x_span <= 8",
            "Ry=32px vertical height budget calculator with single-footprint outer padding",
            "becss- BEM CSS class generator enforcing block__element--modifier naming",
            "Tri-Color theme token injector (#000000 Black, #FFFFFF White, #DE2626 Red)",
            "Responsive layout switcher converting desktop sidebars to mobile hamburger menus"
        ],
        "list_topics": [
            "Comprehensive 30-point inventory of reusable BEHTML component widgets",
            "Classification list of 20 floating state classes and their exact becss- BEM equivalents",
            "Exhaustive 25-point visual design ruleset enforcing zero-fluff aesthetic standards"
        ]
    },
    "local_first_security_crypto": {
        "display_name": "Local-First Security & Cryptography",
        "description": "Offline note encryption, secret isolation, and hostile code audits",
        "library_family": "lib_bejson_Security",
        "function_topics": [
            "Password-protected AES-256-GCM file encryptor and decryptor",
            "Zero-dependency secret environment file loader parsing secureenv_file.json",
            "Hostile static code auditor scanning for hardcoded secrets and token leakage",
            "Advisory file locker preventing concurrent process collisions via PID markers",
            "Deterministic SHA-256 package checksum verifier for deliverable validation"
        ],
        "list_topics": [
            "Exhaustive 30-point security audit checklist for local-first LLM applications",
            "Inventory of 20 common prompt injection vectors and defensive sanitization patterns",
            "Catalog of 15 supply chain verification rules for vendored library dependencies"
        ]
    }
}

# ==============================================================================
# DISPATCH & GENERATION ENGINE
# ==============================================================================

def generate_subject_task(
    subject_key: str,
    workflow_type: str,
    output_root: Path,
    dry_run: bool = False
) -> bool:
    """Dispatches a single subject-specific generation task via agy."""
    domain = SUBJECT_DOMAINS.get(subject_key)
    if not domain:
        logger.error("Unknown subject domain: %s", subject_key)
        return False

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    subject_dir = output_root / subject_key
    
    if workflow_type == "function":
        target_dir = subject_dir / "lib"
        target_dir.mkdir(parents=True, exist_ok=True)
        topic = random.choice(domain["function_topics"])
        family = domain["library_family"]
        
        prompt = (
            f"[ZERO-DEPS] [SURGICAL] Author a robust, reusable Python 3.10+ library function module "
            f"belonging to the '{family}' family. Focus strictly on: '{topic}'. "
            f"Requirements: (1) Single VERSION variable bumped to 100, (2) Fresh RELATIONAL_ID UUID, "
            f"(3) Author credit to Elton Boehnen, (4) Standard logging with zero print statements, "
            f"(5) Function name prefixed with family identity, (6) Self-contained unit tests. "
            f"Save the implementation directly to lib/{family}_{subject_key}_{timestamp}.py."
        )
    elif workflow_type == "list":
        target_dir = subject_dir / "ideas"
        target_dir.mkdir(parents=True, exist_ok=True)
        topic = random.choice(domain["list_topics"])
        
        prompt = (
            f"Act as a principal system architect. Focus on the domain: '{domain['display_name']}'. "
            f"Generate an exhaustive, massively detailed, sequentially numbered list for: '{topic}'. "
            f"Formatting: (1) Each item must feature a bold title followed by a 2-sentence operational description, "
            f"(2) Zero conversational filler or generic preambles, (3) Group items into 4-5 logical categories, "
            f"(4) Include exact implementation considerations. "
            f"Save the list directly to ideas/massive_list_{subject_key}_{timestamp}.md."
        )
    else:  # schema
        target_dir = subject_dir / "schemas"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        prompt = (
            f"[BEJSON-104A] Construct an authoritative BEJSON 104a data schema and initial registry "
            f"modeling entities, parameters, and states for: '{domain['display_name']}'. "
            f"Requirements: (1) Six mandatory keys (Format='BEJSON', Format_Version='104a', Format_Creator='Elton Boehnen'), "
            f"(2) Primitive types only (string, integer, boolean), (3) Positional integrity across Values, "
            f"(4) Cached field map access instructions. "
            f"Save directly to schemas/{subject_key}_registry_{timestamp}.104a.bejson."
        )

    logger.info("----------------------------------------------------------------------")
    logger.info("Subject: %s", domain["display_name"])
    logger.info("Workflow: %s", workflow_type.upper())
    logger.info("Target Directory: %s", target_dir)
    logger.info("Prompt: %s", prompt)
    logger.info("----------------------------------------------------------------------")

    if dry_run:
        logger.info("[DRY RUN] Skipping agy subprocess call.")
        return True

    cmd = [
        "agy",
        "--sandbox",
        f"--dir={str(subject_dir)}",
        "-p",
        prompt
    ]

    try:
        t0 = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        elapsed = time.time() - t0
        logger.info("Task completed successfully in %.2fs.", elapsed)
        return True
    except subprocess.CalledProcessError as err:
        logger.error("agy execution failed (Exit %d): %s", err.returncode, err.stderr.strip())
        return False
    except FileNotFoundError:
        logger.error("Executable 'agy' not found in system PATH.")
        return False

# ==============================================================================
# MINUTE-BASED SCHEDULER & CLI
# ==============================================================================

def run_minute_loop(
    output_root: Path,
    min_minutes: float,
    max_minutes: float,
    subject_filter: Optional[str] = None,
    workflow_filter: Optional[str] = None,
    once: bool = False,
    dry_run: bool = False
):
    """Executes automated generation tasks with delays defined in minutes."""
    output_root.mkdir(parents=True, exist_ok=True)
    
    logger.info("======================================================================")
    logger.info("Antigravity Subject-Specific Automator (Minute-Based Scheduler)")
    logger.info("Target Output Root: %s", output_root)
    logger.info("Timing Cadence: %.1f mins to %.1f mins (%.0fs to %.0fs)",
                min_minutes, max_minutes, min_minutes * 60, max_minutes * 60)
    logger.info("Mode: %s", "Single-Shot Pass" if once else "Continuous Minute Loop")
    logger.info("======================================================================")

    subjects = [subject_filter] if subject_filter and subject_filter in SUBJECT_DOMAINS else list(SUBJECT_DOMAINS.keys())
    workflows = [workflow_filter] if workflow_filter in ("function", "list", "schema") else ["function", "list", "schema"]

    while True:
        sel_subject = random.choice(subjects)
        sel_workflow = random.choice(workflows)

        generate_subject_task(sel_subject, sel_workflow, output_root=output_root, dry_run=dry_run)

        if once:
            logger.info("Single-shot execution completed.")
            break

        # Compute randomized sleep in minutes, converted to float seconds
        delay_minutes = random.uniform(min_minutes, max_minutes)
        delay_seconds = delay_minutes * 60.0
        logger.info("Pausing for %.2f minutes (~%.0f seconds) before next dispatch...", delay_minutes, delay_seconds)
        time.sleep(delay_seconds)

def main():
    parser = argparse.ArgumentParser(description="Automated Subject Function & Massive List Generator")
    parser.add_argument("--output-dir", type=str, default="./automation_targets", help="Directory where generated outputs will be written")
    parser.add_argument("--min-minutes", type=float, default=2.0, help="Minimum delay between tasks in minutes (default: 2.0)")
    parser.add_argument("--max-minutes", type=float, default=10.0, help="Maximum delay between tasks in minutes (default: 10.0)")
    parser.add_argument("--subject", type=str, choices=list(SUBJECT_DOMAINS.keys()), help="Constrain to a single subject domain")
    parser.add_argument("--workflow", type=str, choices=["function", "list", "schema"], help="Constrain to function, list, or schema generation")
    parser.add_argument("--once", action="store_true", help="Run a single pass and exit")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing agy")
    args = parser.parse_args()

    run_minute_loop(
        output_root=Path(args.output_dir).resolve(),
        min_minutes=args.min_minutes,
        max_minutes=args.max_minutes,
        subject_filter=args.subject,
        workflow_filter=args.workflow,
        once=args.once,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
