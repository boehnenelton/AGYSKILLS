#!/usr/bin/env python3
"""
Name:           scaffold_layered_skill
File:           scaffold_layered_skill.py
Description:    Deterministic Layer 6 scaffolder for generating compliant Antigravity CLI
                (agy) skill bundles across Layers 1 through 6. Creates SKILL.md,
                references/, scripts/, and assets/ with atomic BEJSON 104a configuration
                writes and automatic post-scaffold verification via skill_architect_linter.py.
Version:        100
Date Created:   2026-10-17
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  8e2c5b10-4a9d-4f63-8c11-7d3e9a2b5f08
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("scaffold_layered_skill requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import json
import uuid
import logging
import tempfile
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("scaffold_layered_skill")

LAYER_METADATA: Dict[int, Dict[str, str]] = {
    1: {
        "title": "Core Substrate and Data Format",
        "codebase_layer": "L0_Substrate_L1_Entities",
        "allowed_deps": "None (Zero external dependencies; Open Substrate)",
    },
    2: {
        "title": "Domain Engines, Validation and Processing",
        "codebase_layer": "L1_Validation_L2_Verification",
        "allowed_deps": "Layer 1 only (bejson-format-core, behtml-format-core)",
    },
    3: {
        "title": "Automation Pipelines, CLI Execution and Scaffolding",
        "codebase_layer": "L2_Adapters_L3_Services",
        "allowed_deps": "Layers 1 - 2 (Embeds L1 schemas and L2 validators)",
    },
    4: {
        "title": "UI, Spatial Layout and Visual Presentation",
        "codebase_layer": "L4_Presentation_Transport",
        "allowed_deps": "Layers 1 - 3 (Closed presentation layer)",
    },
    5: {
        "title": "Ideation, System Architecture and Codebase Transformation",
        "codebase_layer": "L3_Use_Cases_Cross_Layer_Blueprinting",
        "allowed_deps": "Layers 1 - 4 (Pre-plans and transforms across L1-L4 contracts)",
    },
    6: {
        "title": "Root Orchestration and Meta-Governance",
        "codebase_layer": "L5_Composition_Root",
        "allowed_deps": "Layers 1 - 5 (Coordinates entire ecosystem lifecycles)",
    },
}


def bejson_core_atomic_write(target_file_path: Path, bejson_doc: Dict[str, Any]) -> None:
    """Writes a BEJSON document atomically via .tmp -> flush -> os.fsync -> os.replace."""
    target_file_path = target_file_path.resolve()
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".bejson_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_file_path.parent),
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
            json.dump(bejson_doc, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(str(tmp_path), str(target_file_path))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def parse_negative_siblings(raw_siblings: str) -> List[Dict[str, str]]:
    """Parses 'skill-a:task a,skill-b:task b' into structured dicts."""
    pairs: List[Dict[str, str]] = []
    for item in raw_siblings.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            sib_name, task_desc = item.split(":", 1)
            pairs.append({"sibling": sib_name.strip(), "task": task_desc.strip()})
        else:
            pairs.append({"sibling": item, "task": f"operations handled by {item}"})
    return pairs


def scaffold_bundle(
    skill_name: str,
    layer: int,
    output_root: Path,
    capability_summary: str,
    positive_triggers: str,
    negative_siblings_raw: str,
) -> Path:
    meta = LAYER_METADATA[layer]
    bundle_dir = output_root / skill_name
    for subdir in ("references", "scripts", "assets"):
        (bundle_dir / subdir).mkdir(parents=True, exist_ok=True)

    sib_list = parse_negative_siblings(negative_siblings_raw)
    neg_clauses = [f"{entry['task']} (use {entry['sibling']})" for entry in sib_list]
    neg_summary = ", ".join(neg_clauses)

    pos_bullets = "\n".join(
        f"- {trig.strip()}" for trig in positive_triggers.split(",") if trig.strip()
    )
    neg_bullets = "\n".join(
        f"- Do NOT use for {entry['task']} (use `{entry['sibling']}`)." for entry in sib_list
    )

    skill_md_content = f"""---
name: {skill_name}
description: >-
  {capability_summary}. Use when {positive_triggers}. Do NOT use for {neg_summary}.
---

# {skill_name} (Layer {layer} - {meta['title']})

## Summary

{capability_summary}. Operates strictly at Layer {layer} (`L{layer}`) aligned with codebase layer `{meta['codebase_layer']}`.

## When to Use

{pos_bullets}

## When NOT to Use

{neg_bullets}

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer {layer} (`L{layer}`)
- **Codebase Layer Mapping**: `{meta['codebase_layer']}`
- **Allowed Downward Dependencies**: {meta['allowed_deps']}
- **Sandbox Policy**: All `agy` CLI invocations MUST include `--sandbox`.
- **BEJSON Access Policy**: All `.bejson` reads and mutations MUST resolve column indices dynamically via `field_map`.

## 2. Step-by-Step Workflow

1. **Stage 1 Pre-Flight Verification**: Validate input artifacts and verify schema parity via `field_map`.
2. **Stage 2 Core Execution**: Execute the Layer {layer} domain procedure within the designated output subdirectory.
3. **Stage 3 Quality Gate**: Validate all generated artifacts and confirm deterministic exit code `0`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
"""

    skill_md_path = bundle_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")

    # Write starter BEJSON 104a config asset atomically
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    config_doc: Dict[str, Any] = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Registry_Domain": f"Skill_Bundle_{skill_name}",
        "Schema_Version": "1.0.0",
        "Records_Type": ["SkillConfigRecord"],
        "Fields": [
            {"name": "config_setting_key", "type": "string"},
            {"name": "config_setting_value", "type": "string"},
            {"name": "config_setting_description", "type": "string"},
        ],
        "Values": [
            ["skill_canonical_name", skill_name, "Canonical kebab-case skill identifier."],
            ["skill_layer_tier", str(layer), "Assigned 6-tier architectural layer (1-6)."],
            ["relational_id", str(uuid.uuid4()), "Release-scoped recency fingerprint."],
            ["created_at_utc", now_iso, "UTC ISO-8601 creation timestamp."],
        ],
    }
    bejson_core_atomic_write(bundle_dir / "assets" / "bundle_config.104a.bejson", config_doc)
    return bundle_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="scaffold_layered_skill",
        description="Scaffolds a compliant 6-tier Antigravity CLI skill bundle.",
    )
    parser.add_argument("--name", help="Canonical kebab-case skill name ([Domain]-[Subdomain]-[Suffix]).")
    parser.add_argument("--layer", type=int, choices=[1, 2, 3, 4, 5, 6], help="Layer number (1-6).")
    parser.add_argument("--output-dir", help="Target parent directory for the skill folder.")
    parser.add_argument(
        "--summary",
        default="Execute deterministic layer-governed operations with strict contract validation",
        help="Imperative capability summary.",
    )
    parser.add_argument("--positive-triggers", help="Comma-separated positive trigger phrases.")
    parser.add_argument(
        "--negative-siblings",
        help="Comma-separated 'sibling-skill:excluded task' pairs.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"scaffold_layered_skill v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Display configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("scaffold_layered_skill v%d ready.", VERSION)
        return EXIT_OK

    if not (args.name and args.layer and args.output_dir and args.positive_triggers and args.negative_siblings):
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    out_root = Path(args.output_dir).resolve()
    bundle_path = scaffold_bundle(
        skill_name=args.name.strip(),
        layer=args.layer,
        output_root=out_root,
        capability_summary=args.summary.strip(),
        positive_triggers=args.positive_triggers.strip(),
        negative_siblings_raw=args.negative_siblings.strip(),
    )
    LOG.info("Scaffolded skill bundle at: %s", bundle_path)

    # Import and run skill_architect_linter automatically
    sys.path.insert(0, str(SCRIPT_PATH))
    import skill_architect_linter  # type: ignore

    report = skill_architect_linter.validate_skill_manifest(bundle_path)
    if not report["valid"]:
        LOG.error("Post-scaffold lint failed: %s", report["errors"])
        return EXIT_SCHEMA_FAILURE

    LOG.info("Post-scaffold lint PASSED for '%s'.", args.name)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
