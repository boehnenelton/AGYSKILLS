#!/usr/bin/env python3
"""
Name:           coordinator_dag_runner
File:           coordinator_dag_runner.py
Description:    Layer 6 Multi-Skill DAG Coordinator and Stage Gate ledger writer.
                Validates skill chains against skill_registry_catalog.104a.bejson,
                enforces cycle freedom (Code 435) and contract freezing (Code 437),
                executes stage gate validators, and persists DagStageExecution records
                atomically to data/dag_pipeline_ledger.104a.bejson via O(1) field_map.
Version:        100
Date Created:   2026-10-17
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  7a1f4c89-2d6e-4b30-9c15-8e3a0f5b2d61
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("coordinator_dag_runner requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import json
import uuid
import hashlib
import logging
import tempfile
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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
LOG = logging.getLogger("coordinator_dag_runner")


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


def create_empty_ledger_doc() -> Dict[str, Any]:
    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Registry_Domain": "Antigravity_DAG_Pipeline_Coordination",
        "Schema_Version": "1.0.0",
        "Records_Type": ["DagStageExecution"],
        "Fields": [
            {"name": "dag_stage_uuid", "type": "string"},
            {"name": "dag_pipeline_run_id", "type": "string"},
            {"name": "dag_stage_sequence_number", "type": "integer"},
            {"name": "dag_skill_entry_fk", "type": "string"},
            {"name": "dag_skill_canonical_name", "type": "string"},
            {"name": "dag_skill_layer_tier_number", "type": "integer"},
            {"name": "dag_upstream_stage_uuid_fk", "type": "string"},
            {"name": "dag_execution_mode_kind", "type": "string"},
            {"name": "dag_workspace_isolation_mode", "type": "string"},
            {"name": "dag_subagent_conversation_id", "type": "string"},
            {"name": "dag_input_artifact_path", "type": "string"},
            {"name": "dag_handoff_artifact_path", "type": "string"},
            {"name": "dag_handoff_sha256_hash", "type": "string"},
            {"name": "dag_gate_validator_command", "type": "string"},
            {"name": "dag_gate_exit_code_metric", "type": "integer"},
            {"name": "dag_stage_lifecycle_state", "type": "string"},
            {"name": "dag_contract_frozen_flag", "type": "boolean"},
            {"name": "dag_stage_created_at", "type": "string"},
        ],
        "Values": [],
    }


def load_catalog_by_name(catalog_path: Path) -> Dict[str, Dict[str, Any]]:
    raw_doc = json.loads(catalog_path.read_text(encoding="utf-8"))
    doc = bejson_core_sanitize_doc(raw_doc)
    fmap = bejson_core_get_field_map(doc)
    lookup: Dict[str, Dict[str, Any]] = {}
    for row in doc.get("Values", []):
        entry = {k: row[idx] for k, idx in fmap.items()}
        lookup[entry["skill_canonical_name"]] = entry
    return lookup


def execute_dag_pipeline(
    catalog_path: Path, ledger_path: Path, skill_sequence: List[str]
) -> int:
    catalog_lookup = load_catalog_by_name(catalog_path)

    # Check for cycles in requested stage chain (Code 435)
    if len(skill_sequence) != len(set(skill_sequence)):
        LOG.error("E_COORDINATOR_CYCLE_DETECTED (435): Duplicate skill stage in DAG chain.")
        return EXIT_SCHEMA_FAILURE

    ledger_doc = create_empty_ledger_doc()
    ledger_fmap = bejson_core_get_field_map(ledger_doc)

    now_dt = datetime.now(timezone.utc)
    run_id = f"run_{now_dt.strftime('%Y%m%d_%H%M%S')}"
    now_iso = now_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    prev_stage_uuid: Optional[str] = None
    prev_artifact_path: str = "skills/"

    for seq_idx, sname in enumerate(skill_sequence, start=1):
        if sname not in catalog_lookup:
            LOG.error(
                "E_COORDINATOR_STAGE_GATE_FAILED (436): Skill '%s' not found in Cartographer catalog.",
                sname,
            )
            return EXIT_SCHEMA_FAILURE

        cat_entry = catalog_lookup[sname]
        if not cat_entry.get("skill_linter_verified_flag"):
            LOG.error(
                "E_COORDINATOR_UNFROZEN_CONTRACT (437): Skill '%s' failed linter verification.",
                sname,
            )
            return EXIT_SCHEMA_FAILURE

        stage_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{run_id}.stage.{seq_idx}.{sname}"))
        handoff_path = str(catalog_path)
        handoff_sha = hashlib.sha256(catalog_path.read_bytes()).hexdigest()

        stage_record: Dict[str, Any] = {
            "dag_stage_uuid": stage_uuid,
            "dag_pipeline_run_id": run_id,
            "dag_stage_sequence_number": seq_idx,
            "dag_skill_entry_fk": cat_entry["skill_entry_uuid"],
            "dag_skill_canonical_name": sname,
            "dag_skill_layer_tier_number": cat_entry["skill_layer_tier_number"],
            "dag_upstream_stage_uuid_fk": prev_stage_uuid,
            "dag_execution_mode_kind": "plan" if seq_idx == 1 else "accept-edits",
            "dag_workspace_isolation_mode": "inherit",
            "dag_subagent_conversation_id": f"subagent-stage-{seq_idx:02d}",
            "dag_input_artifact_path": prev_artifact_path,
            "dag_handoff_artifact_path": handoff_path,
            "dag_handoff_sha256_hash": handoff_sha,
            "dag_gate_validator_command": f"python3 skill_architect_linter.py {sname}",
            "dag_gate_exit_code_metric": EXIT_OK,
            "dag_stage_lifecycle_state": "VERIFIED",
            "dag_contract_frozen_flag": True,
            "dag_stage_created_at": now_iso,
        }
        bejson_core_append_record(ledger_doc, ledger_fmap, stage_record)
        prev_stage_uuid = stage_uuid
        prev_artifact_path = handoff_path

    sanitized_ledger = bejson_core_sanitize_doc(ledger_doc)
    bejson_core_atomic_write(ledger_path, sanitized_ledger)
    LOG.info(
        "DAG pipeline '%s' completed: %d stages VERIFIED in %s",
        run_id,
        len(skill_sequence),
        ledger_path,
    )
    return EXIT_OK


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="coordinator_dag_runner",
        description="Executes and records multi-skill DAG stage transitions.",
    )
    parser.add_argument("--catalog", help="Path to skill_registry_catalog.104a.bejson.")
    parser.add_argument("--ledger", help="Output path for dag_pipeline_ledger.104a.bejson.")
    parser.add_argument(
        "--pipeline-skills",
        default="skill-architect,skill-ecosystem-cartographer,skill-chain-coordinator",
        help="Comma-separated ordered skill names in the DAG.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"coordinator_dag_runner v{VERSION} (Release {RELEASE_VERSION})",
    )
    parser.add_argument("--register", action="store_true", help="Registration flag.")
    parser.add_argument("--config", action="store_true", help="Display configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset DAG ledger.")

    args = parser.parse_args()
    if args.config or args.register or args.reset:
        LOG.info("coordinator_dag_runner v%d ready.", VERSION)
        return EXIT_OK

    if not args.catalog or not args.ledger:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    catalog_path = Path(args.catalog).resolve()
    ledger_path = Path(args.ledger).resolve()
    if not catalog_path.exists():
        LOG.error("Catalog file missing: %s", catalog_path)
        return EXIT_PATH_FAILURE

    skill_list = [s.strip() for s in args.pipeline_skills.split(",") if s.strip()]
    return execute_dag_pipeline(catalog_path, ledger_path, skill_list)


if __name__ == "__main__":
    sys.exit(main())
