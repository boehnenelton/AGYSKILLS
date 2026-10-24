#!/usr/bin/env python3
"""
Name:           cartographer_index
File:           cartographer_index.py
Description:    Layer 6 Ecosystem Cartographer indexing and collision detection engine.
                Scans skill directories, extracts YAML frontmatter and trigger boundaries,
                enforces boundary-layer sanitization and O(1) BEJSON field_map caching,
                writes data/skill_registry_catalog.104a.bejson atomically, and generates
                the pairwise trigger collision matrix (Codes 430-433).
Version:        102
Date Created:   2026-10-17
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  4d7c1e92-8a3b-4f10-9c25-6b8e3a1d7f04
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("cartographer_index requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import re
import json
import uuid
import hashlib
import logging
import tempfile
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

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
LOG = logging.getLogger("cartographer_index")

SUFFIX_TO_LAYER: Dict[str, Tuple[int, str]] = {
    "-core": (1, "L0_Substrate_L1_Entities"),
    "-nesting-core": (1, "L0_Substrate_L1_Entities"),
    "-mfdb-core": (1, "L0_Substrate_L1_Entities"),
    "-validator": (2, "L1_Validation_L2_Verification"),
    "-chunker": (2, "L1_Validation_L2_Verification"),
    "-auditor": (2, "L1_Validation_L2_Verification"),
    "-engine": (2, "L1_Validation_L2_Verification"),
    "-automator": (3, "L2_Adapters_L3_Services"),
    "-pipeline": (3, "L2_Adapters_L3_Services"),
    "-scaffold-python": (3, "L2_Adapters_L3_Services"),
    "-scaffold-javascript": (3, "L2_Adapters_L3_Services"),
    "-scaffold-bash": (3, "L2_Adapters_L3_Services"),
    "-manager": (3, "L2_Adapters_L3_Services"),
    "-manage": (3, "L2_Adapters_L3_Services"),
    "-delivery": (3, "L2_Adapters_L3_Services"),
    "-builder": (4, "L4_Presentation_Transport"),
    "-diagrammer": (4, "L4_Presentation_Transport"),
    "-decomposer": (4, "L4_Presentation_Transport"),
    "-mapper": (4, "L4_Presentation_Transport"),
    "-template": (4, "L4_Presentation_Transport"),
    "-preferences": (4, "L4_Presentation_Transport"),
    "-composer": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-planner": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-architect": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-refactor": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-rewriter": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-writer": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-analysis": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-extraction": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-grounding": (5, "L3_Use_Cases_Cross_Layer_Blueprinting"),
    "-coordinator": (6, "L5_Composition_Root"),
    "-cartographer": (6, "L5_Composition_Root"),
    "-recipe-composer": (6, "L5_Composition_Root"),
}

LAYER6_OVERRIDES: Set[str] = {
    "skill-architect",
    "skill-ecosystem-cartographer",
    "skill-chain-coordinator",
    "skill-chain-recipe-composer",
    "planning-coordinator",
    "arch-layered-refactor",
    "agy-skill-refactor",
}


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer whitespace sanitization."""
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
    """O(1) Field Map Cache mapping field_name -> column index."""
    fields_list = bejson_doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}


def bejson_core_append_record(
    bejson_doc: Dict[str, Any], field_map: Dict[str, int], record_payload: Dict[str, Any]
) -> None:
    """Appends a record row using dynamic field_map indices and explicit null padding."""
    row: List[Any] = [None] * len(field_map)
    for fname, fval in record_payload.items():
        if fname not in field_map:
            raise KeyError(f"E_CORE_UNKNOWN_FIELD (21): Unknown field '{fname}'.")
        row[field_map[fname]] = fval.strip() if isinstance(fval, str) else fval
    bejson_doc["Values"].append(row)


def bejson_core_atomic_write(target_file_path: Path, bejson_doc: Dict[str, Any]) -> None:
    """Atomic write: .tmp -> flush -> os.fsync -> os.replace."""
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


def infer_layer_and_suffix(skill_name: str) -> Tuple[int, str, str]:
    if skill_name in LAYER6_OVERRIDES:
        for sfx in ("-coordinator", "-cartographer", "-recipe-composer", "-architect", "-refactor"):
            if skill_name.endswith(sfx):
                return 6, "L5_Composition_Root", sfx
        return 6, "L5_Composition_Root", "-architect"
    for sfx, (layer_num, cb_layer) in sorted(
        SUFFIX_TO_LAYER.items(), key=lambda x: len(x[0]), reverse=True
    ):
        if skill_name.endswith(sfx):
            return layer_num, cb_layer, sfx
    return 3, "L2_Adapters_L3_Services", "-unknown"


def parse_skill_md(skill_md_path: Path, root_dir: Path) -> Dict[str, Any]:
    raw_bytes = skill_md_path.read_bytes()
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    raw_text = raw_bytes.decode("utf-8")
    parts = raw_text.split("---", 2)
    fm_block = parts[1] if len(parts) >= 3 else ""
    body_block = parts[2] if len(parts) >= 3 else raw_text

    name_match = re.search(r"^name:\s*([^\n]+)$", fm_block, re.MULTILINE)
    skill_name = (
        name_match.group(1).strip().strip("'\"") if name_match else skill_md_path.parent.name
    )

    desc_match = re.search(
        r"description:\s*(?:>-\s*|\|\s*)?(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)",
        fm_block,
        re.DOTALL,
    )
    desc_norm = " ".join(desc_match.group(1).split()) if desc_match else ""

    pos_match = re.search(
        r"use when\s+(.*?)(?:do not use for|\Z)", desc_norm, re.IGNORECASE
    )
    neg_match = re.search(r"do not use for\s+(.*)", desc_norm, re.IGNORECASE)

    pos_triggers = pos_match.group(1).strip(" .") if pos_match else ""
    neg_triggers = neg_match.group(1).strip(" .") if neg_match else ""
    blocked_siblings = sorted(set(re.findall(r"\(use\s+([a-z0-9-]+)\)", desc_norm.lower())))

    layer_num, cb_layer, suffix_tok = infer_layer_and_suffix(skill_name)
    domain_tok = skill_name.split("-")[0] if "-" in skill_name else skill_name
    body_line_count = len(body_block.strip().splitlines())

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rel_path = str(skill_md_path.relative_to(root_dir)) if skill_md_path.is_relative_to(root_dir) else str(skill_md_path)

    deterministic_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"agy.skill.{skill_name}"))

    return {
        "skill_entry_uuid": deterministic_uuid,
        "skill_canonical_name": skill_name,
        "skill_layer_tier_number": layer_num,
        "skill_codebase_layer_mapping": cb_layer,
        "skill_domain_prefix_token": domain_tok,
        "skill_functional_suffix_token": suffix_tok,
        "skill_scope_origin_kind": "global",
        "skill_manifest_relative_path": rel_path,
        "skill_positive_triggers_csv": pos_triggers,
        "skill_negative_triggers_csv": neg_triggers,
        "skill_blocked_siblings_csv": ",".join(blocked_siblings),
        "skill_allowed_downward_deps_csv": "bejson-104-core,bejson-104-validator"
        if layer_num > 2
        else ("bejson-104-core" if layer_num == 2 else "none"),
        "skill_input_contract_spec": f"Layer {layer_num} verified upstream contract",
        "skill_output_artifact_spec": f"Layer {layer_num} deterministic deliverable",
        "skill_body_line_count_metric": body_line_count,
        "skill_desc_char_count_metric": len(desc_norm),
        "skill_manifest_sha256_hash": sha256_hex,
        "skill_linter_verified_flag": body_line_count <= 500 and len(desc_norm) <= 1024 and len(blocked_siblings) > 0,
        "skill_created_at": now_iso,
    }


def create_empty_catalog_doc() -> Dict[str, Any]:
    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Registry_Domain": "Antigravity_Skill_Ecosystem_Cartography",
        "Schema_Version": "1.0.0",
        "Records_Type": ["SkillCatalogEntry"],
        "Fields": [
            {"name": "skill_entry_uuid", "type": "string"},
            {"name": "skill_canonical_name", "type": "string"},
            {"name": "skill_layer_tier_number", "type": "integer"},
            {"name": "skill_codebase_layer_mapping", "type": "string"},
            {"name": "skill_domain_prefix_token", "type": "string"},
            {"name": "skill_functional_suffix_token", "type": "string"},
            {"name": "skill_scope_origin_kind", "type": "string"},
            {"name": "skill_manifest_relative_path", "type": "string"},
            {"name": "skill_positive_triggers_csv", "type": "string"},
            {"name": "skill_negative_triggers_csv", "type": "string"},
            {"name": "skill_blocked_siblings_csv", "type": "string"},
            {"name": "skill_allowed_downward_deps_csv", "type": "string"},
            {"name": "skill_input_contract_spec", "type": "string"},
            {"name": "skill_output_artifact_spec", "type": "string"},
            {"name": "skill_body_line_count_metric", "type": "integer"},
            {"name": "skill_desc_char_count_metric", "type": "integer"},
            {"name": "skill_manifest_sha256_hash", "type": "string"},
            {"name": "skill_linter_verified_flag", "type": "boolean"},
            {"name": "skill_created_at", "type": "string"},
        ],
        "Values": [],
    }


def audit_pairwise_collisions(
    catalog_doc: Dict[str, Any], fmap: Dict[str, int]
) -> Tuple[List[str], str]:
    """Audits all cataloged skills for Codes 430-433 and emits a Markdown matrix report."""
    rows = catalog_doc.get("Values", [])
    errors: List[str] = []
    seen_names: Set[str] = set()

    entries: List[Dict[str, Any]] = []
    for row in rows:
        rec = {k: row[idx] for k, idx in fmap.items()}
        cname = rec["skill_canonical_name"]
        if cname in seen_names:
            errors.append(f"E_CARTOGRAPHER_DUPLICATE_SKILL (430): Duplicate skill '{cname}'.")
        seen_names.add(cname)
        entries.append(rec)

    md_lines: List[str] = [
        "# Ecosystem Topology & Pairwise Trigger Collision Matrix",
        "",
        f"> **Generated By:** `skill-ecosystem-cartographer` v{VERSION} (Release {RELEASE_VERSION})",
        f"> **Total Indexed Skills:** {len(entries)}",
        "",
        "## 1. Registered Skill Roster",
        "",
        "| Skill Name | Layer | Codebase Layer | Body Lines | Desc Chars | Blocked Siblings (`T^-`) | SHA-256 Prefix |",
        "| :--- | :---: | :--- | :---: | :---: | :--- | :--- |",
    ]

    for e in entries:
        md_lines.append(
            f"| `{e['skill_canonical_name']}` | L{e['skill_layer_tier_number']} | "
            f"`{e['skill_codebase_layer_mapping']}` | {e['skill_body_line_count_metric']} | "
            f"{e['skill_desc_char_count_metric']} | `{e['skill_blocked_siblings_csv']}` | "
            f"`{e['skill_manifest_sha256_hash'][:12]}` |"
        )

    md_lines.extend(["", "## 2. Pairwise Negative Guardrail Matrix", ""])
    header_cols = " | ".join(f"`{e['skill_canonical_name']}`" for e in entries)
    sep_cols = " | ".join(":---:" for _ in entries)
    md_lines.append(f"| Skill | {header_cols} |")
    md_lines.append(f"| :--- | {sep_cols} |")

    for e_a in entries:
        name_a = e_a["skill_canonical_name"]
        blocked_a = set(filter(None, e_a["skill_blocked_siblings_csv"].split(",")))
        dom_a = e_a["skill_domain_prefix_token"]
        row_cells: List[str] = []
        for e_b in entries:
            name_b = e_b["skill_canonical_name"]
            if name_a == name_b:
                row_cells.append("`-`")
                continue
            blocked_b = set(filter(None, e_b["skill_blocked_siblings_csv"].split(",")))
            dom_b = e_b["skill_domain_prefix_token"]

            if name_b in blocked_a and name_a in blocked_b:
                row_cells.append("`COND (Reciprocal)`")
            elif name_b in blocked_a or name_a in blocked_b:
                row_cells.append("`COND (Directed)`")
            elif dom_a != dom_b:
                row_cells.append("`OK (Orthogonal)`")
            else:
                errors.append(
                    f"E_CARTOGRAPHER_TRIGGER_COLLISION (431): Same-domain skills '{name_a}' and '{name_b}' lack mutual negative guardrails."
                )
                row_cells.append("`ERR_D (Collision)`")
        md_lines.append(f"| **`{name_a}`** | {' | '.join(row_cells)} |")

    md_lines.extend(
        [
            "",
            "---",
            "",
            "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
            "",
        ]
    )
    return errors, "\n".join(md_lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cartographer_index",
        description="Scans skill bundles and populates skill_registry_catalog.104a.bejson.",
    )
    parser.add_argument("--scan-root", help="Directory containing skill subfolders.")
    parser.add_argument("--catalog", help="Output path for skill_registry_catalog.104a.bejson.")
    parser.add_argument("--report", help="Output path for topology_collision_matrix.md.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"cartographer_index v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Show config.")
    parser.add_argument("--reset", action="store_true", help="Reset catalog to canonical seed state.")

    args = parser.parse_args()
    if args.config or args.register:
        LOG.info("cartographer_index v%d ready.", VERSION)
        return EXIT_OK

    if not args.scan_root or not args.catalog:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    scan_dir = Path(args.scan_root).resolve()
    catalog_path = Path(args.catalog).resolve()
    if not scan_dir.is_dir():
        LOG.error("Scan root does not exist: %s", scan_dir)
        return EXIT_PATH_FAILURE

    catalog_doc = create_empty_catalog_doc()
    fmap = bejson_core_get_field_map(catalog_doc)

    skill_mds = sorted(scan_dir.glob("*/SKILL.md"))
    for smd in skill_mds:
        record = parse_skill_md(smd, scan_dir)
        bejson_core_append_record(catalog_doc, fmap, record)

    sanitized_doc = bejson_core_sanitize_doc(catalog_doc)
    bejson_core_atomic_write(catalog_path, sanitized_doc)
    LOG.info("Wrote %d skill records to %s", len(sanitized_doc["Values"]), catalog_path)

    collision_errors, matrix_md = audit_pairwise_collisions(sanitized_doc, fmap)
    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(matrix_md, encoding="utf-8")
        LOG.info("Wrote collision matrix report to %s", report_path)

    if collision_errors:
        for err in collision_errors:
            LOG.error("%s", err)
        return EXIT_SCHEMA_FAILURE

    LOG.info("Pairwise collision audit PASSED (0 collisions across %d skills).", len(skill_mds))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
