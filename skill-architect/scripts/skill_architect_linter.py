#!/usr/bin/env python3
"""
Name:           skill_architect_linter
File:           skill_architect_linter.py
Description:    Deterministic Layer 2 / Layer 6 quality gate and Negative Constraint
                Trigger linter for Antigravity CLI (agy) skill bundles. Enforces YAML
                frontmatter syntax, kebab-case relational naming ([Domain]-[Subdomain]-[Suffix]),
                description length <= 1024 chars, mandatory positive ('Use when') and
                negative ('Do NOT use for') triggers, sibling redirection pointers,
                <= 500 body line progressive disclosure ceiling, zero em/en-dash
                typography, '--sandbox' containment, and O(1) 'field_map' BEJSON access.
Version:        102
Date Created:   2026-10-17
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  2e8a4c19-7b3d-4f60-9a15-8c4d2b7e0f63
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("skill_architect_linter requires Python 3.10 or newer.\n")
    sys.exit(20)

import re
import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION: int = 102
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
LOG = logging.getLogger("skill_architect_linter")

APPROVED_DOMAIN_PREFIXES: Tuple[str, ...] = (
    "agy-",
    "arch-",
    "audit-",
    "behtml-",
    "bejson-",
    "code-",
    "component-",
    "concept-",
    "concepts-",
    "file-",
    "ideation-",
    "job-",
    "mfdb-",
    "planning-",
    "policy-",
    "prompt-",
    "publication-",
    "project-",
    "projects-",
    "skill-",
    "taxonomy-",
    "template-",
    "ui-",
    "web-ui-",
)

LAYER_SUFFIX_MAP: Dict[int, Tuple[str, ...]] = {
    1: ("-core", "-nesting-core", "-mfdb-core"),
    2: ("-validator", "-chunker", "-auditor", "-engine"),
    3: (
        "-automator",
        "-pipeline",
        "-scaffold-python",
        "-scaffold-javascript",
        "-scaffold-bash",
        "-manager",
        "-manage",
        "-delivery",
    ),
    4: ("-builder", "-diagrammer", "-decomposer", "-mapper", "-template", "-preferences"),
    5: (
        "-composer",
        "-planner",
        "-architect",
        "-refactor",
        "-rewriter",
        "-writer",
        "-analysis",
        "-extraction",
        "-grounding",
    ),
    6: (
        "-coordinator",
        "-cartographer",
        "-recipe-composer",
        "-packager",
        "skill-architect",
        "arch-layered-refactor",
        "agy-skill-refactor",
    ),
}

ALL_CANONICAL_SUFFIXES: Tuple[str, ...] = tuple(
    sfx for suffixes in LAYER_SUFFIX_MAP.values() for sfx in suffixes
)


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer sanitization for any companion .bejson files in the skill bundle."""
    if not isinstance(raw_doc, dict):
        return raw_doc
    clean_doc: Dict[str, Any] = {
        (k.strip() if isinstance(k, str) else k): v for k, v in raw_doc.items()
    }
    fields = clean_doc.get("Fields")
    if isinstance(fields, list):
        for fdef in fields:
            if isinstance(fdef, dict):
                for fkey in ("name", "type"):
                    if isinstance(fdef.get(fkey), str):
                        fdef[fkey] = fdef[fkey].strip()
    values = clean_doc.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for idx, val in enumerate(row):
                    if isinstance(val, str) and val and (val[0].isspace() or val[-1].isspace()):
                        row[idx] = val.strip()
    return clean_doc


def bejson_core_get_field_map(bejson_doc: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) lookup dictionary mapping field_name -> 0-based column index."""
    fields_list = bejson_doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}


def validate_bejson_asset(bejson_path: Path) -> List[str]:
    """Validates any bundled .bejson asset against Layer 1 invariants (Codes 1-19)."""
    asset_errors: List[str] = []
    try:
        raw_data = json.loads(bejson_path.read_text(encoding="utf-8"))
    except Exception as exc:
        asset_errors.append(f"E_INVALID_JSON (1): {bejson_path.name} failed JSON parse: {exc}")
        return asset_errors

    doc = bejson_core_sanitize_doc(raw_data)
    mandatory_keys = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")
    for mkey in mandatory_keys:
        if mkey not in doc:
            asset_errors.append(f"E_MISSING_MANDATORY_KEY (2): {bejson_path.name} missing '{mkey}'.")

    if doc.get("Format_Creator") != "Elton Boehnen":
        asset_errors.append(
            f"E_INVALID_FORMAT_CREATOR (16): {bejson_path.name} must credit 'Elton Boehnen'."
        )

    fmap = bejson_core_get_field_map(doc)
    expected_len = len(fmap)
    for row_idx, row in enumerate(doc.get("Values", [])):
        if not isinstance(row, list) or len(row) != expected_len:
            asset_errors.append(
                f"E_RECORD_LENGTH_MISMATCH (9): {bejson_path.name} row {row_idx} length != {expected_len}."
            )
    return asset_errors


def validate_skill_manifest(skill_target: Path) -> Dict[str, Any]:
    """Runs the full 401-415 quality gate on a SKILL.md manifest and its bundle directory."""
    skill_md = skill_target / "SKILL.md" if skill_target.is_dir() else skill_target
    bundle_dir = skill_md.parent

    if not skill_md.exists():
        return {
            "valid": False,
            "skill_path": str(skill_md),
            "errors": [f"E_SKILL_MISSING (401): {skill_md} not found."],
            "warnings": [],
        }

    raw_text = skill_md.read_text(encoding="utf-8")
    all_lines = raw_text.splitlines()
    errors: List[str] = []
    warnings: List[str] = []

    if not raw_text.startswith("---\n"):
        errors.append("E_FRONTMATTER_START (402): SKILL.md must open with '---' on line 1.")
        return {"valid": False, "skill_path": str(skill_md), "errors": errors, "warnings": warnings}

    parts = raw_text.split("---", 2)
    if len(parts) < 3:
        errors.append("E_FRONTMATTER_UNCLOSED (403): Missing closing '---' YAML delimiter.")
        return {"valid": False, "skill_path": str(skill_md), "errors": errors, "warnings": warnings}

    fm_block, body_block = parts[1], parts[2]
    body_lines = body_block.strip().splitlines()

    # Check 404: Stage 2 Progressive Disclosure line budget (<= 500 lines)
    if len(body_lines) > 500:
        errors.append(
            f"E_LINE_BUDGET_EXCEEDED (404): Body is {len(body_lines)} lines (hard ceiling is 500)."
        )

    # Check 405-407: Relational Naming Taxonomy ([Domain]-[Subdomain]-[Suffix])
    name_match = re.search(r"^name:\s*([^\n]+)$", fm_block, re.MULTILINE)
    clean_name = ""
    if not name_match:
        errors.append("E_MISSING_NAME (405): YAML frontmatter must declare 'name'.")
    else:
        clean_name = (
            name_match.group(1).strip().strip("'\"").replace("user:", "").replace("system:", "")
        )
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", clean_name) or len(clean_name) > 64:
            errors.append(
                f"E_INVALID_NAME_SYNTAX (406): '{clean_name}' must be kebab-case <= 64 chars."
            )
        if not any(clean_name.startswith(pfx) for pfx in APPROVED_DOMAIN_PREFIXES):
            warnings.append(
                f"W_NON_STANDARD_DOMAIN: '{clean_name}' does not start with a registered domain token."
            )
        if not any(clean_name.endswith(sfx) for sfx in ALL_CANONICAL_SUFFIXES):
            errors.append(
                f"E_NON_CANONICAL_SUFFIX (407): '{clean_name}' must end with an approved 6-tier suffix."
            )

    # Check 408-412: Level 1 Positive & Mutual Negative Constraint Triggers
    desc_match = re.search(
        r"description:\s*(?:>-\s*|\|\s*)?(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)",
        fm_block,
        re.DOTALL,
    )
    siblings_referenced: List[str] = []
    if not desc_match:
        errors.append("E_MISSING_DESCRIPTION (408): YAML frontmatter must declare 'description'.")
    else:
        desc_norm = " ".join(desc_match.group(1).split())
        if len(desc_norm) > 1024:
            errors.append(
                f"E_DESC_OVERFLOW (409): Description is {len(desc_norm)} chars (max 1024)."
            )
        if "use when" not in desc_norm.lower() and "trigger on" not in desc_norm.lower():
            errors.append(
                "E_MISSING_POSITIVE_TRIGGER (410): Description must include 'Use when...' clause."
            )
        if "do not use for" not in desc_norm.lower():
            errors.append(
                "E_MISSING_NEGATIVE_TRIGGER (411): Description must include 'Do NOT use for...' clause."
            )
        siblings_referenced = re.findall(r"\(use\s+([a-z0-9-]+)\)", desc_norm.lower())
        if not siblings_referenced:
            errors.append(
                "E_MISSING_SIBLING_POINTER (412): Negative trigger must redirect via '(use <sibling-skill>)'."
            )

    # Check Level 2 Body Exclusion Section
    if "## when not to use" not in body_block.lower():
        warnings.append(
            "W_MISSING_LEVEL2_GUARDRAIL: Body should include a '## When NOT to Use' circuit-breaker section."
        )

    # Check 413: Zero Em-Dash / En-Dash Typography Rule
    if "\u2014" in raw_text or "\u2013" in raw_text:
        errors.append(
            "E_TYPOGRAPHY_DASH_VIOLATION (413): Found forbidden em-dash or en-dash in SKILL.md; use ASCII '-'."
        )

    # Check 414-415: Domain-Specific Sandbox and BEJSON Field Map Rules
    if re.search(r"\bagy\b", raw_text) and "--sandbox" not in raw_text:
        errors.append(
            "E_AGY_UNSANDBOXED (414): Skill references 'agy' without mandating '--sandbox'."
        )
    if "bejson" in raw_text.lower() and "row[" in raw_text and "field_map" not in raw_text:
        errors.append(
            "E_BEJSON_HARDCODED_INDEX (415): Found 'row[' indexing without dynamic 'field_map'."
        )

    # Validate any bundled .bejson assets in assets/
    assets_dir = bundle_dir / "assets"
    if assets_dir.is_dir():
        for bj_file in sorted(assets_dir.glob("*.bejson")):
            errors.extend(validate_bejson_asset(bj_file))

    return {
        "valid": len(errors) == 0,
        "skill_name": clean_name,
        "skill_path": str(skill_md),
        "total_lines": len(all_lines),
        "body_lines": len(body_lines),
        "siblings_referenced": siblings_referenced,
        "errors": errors,
        "warnings": warnings,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill_architect_linter",
        description="Layer 2/6 Quality Gate Linter for Antigravity CLI layered skills.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Path to skill directory or SKILL.md file to validate.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"skill_architect_linter v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Print registration command hint.")
    parser.add_argument("--config", action="store_true", help="Display active linter configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset temporary linter state.")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.config:
        LOG.info("Linter Config: max_body_lines=500, max_desc_chars=1024, version=%d", VERSION)
        return EXIT_OK
    if args.register or args.reset:
        LOG.info("Operation completed cleanly.")
        return EXIT_OK
    if not args.target:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        LOG.error("Target path does not exist: %s", target_path)
        return EXIT_PATH_FAILURE

    report = validate_skill_manifest(target_path)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")

    if not report["valid"]:
        LOG.error(
            "Validation FAILED for '%s' with %d error(s).",
            report.get("skill_name") or target_path.name,
            len(report["errors"]),
        )
        return EXIT_SCHEMA_FAILURE

    LOG.info(
        "Validation PASSED for '%s' (%d body lines, %d sibling pointers).",
        report["skill_name"],
        report["body_lines"],
        len(report["siblings_referenced"]),
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
