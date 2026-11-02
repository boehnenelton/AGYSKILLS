#!/usr/bin/env python3
"""
Name:           council_grounding_scout
File:           council_grounding_scout.py
Description:    Deterministic Layer 5 scout for surveying Elton Boehnen's ecosystem
                grounding context. Ingests canonical definitions.json, daily global
                log partitions ($GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson), project trackers,
                library tiers (104 stable vs 105 dev), and installed skills to synthesize
                a comprehensive operational state dossier for council deliberation.
Version:        100
Date Created:   2026-11-02
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  4a9e2d10-8b3c-4f71-9c22-1d5e6a7b8c99
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("council_grounding_scout requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import json
import uuid
import logging
import argparse
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
LOG = logging.getLogger("council_grounding_scout")


def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer sanitization per Policy Section 10.9."""
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


def bejson_core_atomic_write(target_path: Path, doc: Dict[str, Any]) -> None:
    """Atomic write via .tmp -> flush -> fsync -> replace."""
    target_path = target_path.resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".grounding_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_path.parent),
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
            json.dump(doc, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(str(tmp_path), str(target_path))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def load_canonical_definitions(definitions_path: Path) -> Dict[str, str]:
    """Loads variable definitions from canonical definitions.json with O(1) field map."""
    if not definitions_path.exists():
        LOG.warning("Definitions file not found at %s", definitions_path)
        return {}
    try:
        raw_doc = json.loads(definitions_path.read_text(encoding="utf-8"))
        doc = bejson_core_sanitize_doc(raw_doc)
        fmap = bejson_core_get_field_map(doc)
        var_name_idx = fmap.get("var_name")
        var_value_idx = fmap.get("var_value")
        if var_name_idx is None or var_value_idx is None:
            LOG.error("Definitions schema missing 'var_name' or 'var_value' fields.")
            return {}
        defs: Dict[str, str] = {}
        for row in doc.get("Values", []):
            if isinstance(row, list) and len(row) > max(var_name_idx, var_value_idx):
                name = str(row[var_name_idx])
                val = str(row[var_value_idx])
                defs[name] = val
        return defs
    except Exception as exc:
        LOG.error("Failed to parse definitions file: %s", exc)
        return {}


def scan_global_logs(global_logs_dir: Path, days_back: int = 3) -> Dict[str, Any]:
    """Scans and parses the last N days of global logs under $GLOBAL_LOGS."""
    if not global_logs_dir.exists():
        LOG.warning("Global logs directory not found at %s", global_logs_dir)
        return {"entries_scanned": 0, "recent_tasks": [], "recent_files": [], "recent_subsystems": []}

    today = datetime.now(timezone.utc)
    dates_to_check = [(today - timedelta(days=d)).strftime("%Y-%m-%d") for d in range(days_back + 1)]
    
    entries_scanned = 0
    recent_tasks: List[str] = []
    recent_files: List[str] = []
    recent_subsystems: List[str] = []
    recent_errors: List[str] = []

    for dstr in dates_to_check:
        log_file = global_logs_dir / f"Log-{dstr}.bejson"
        if not log_file.exists():
            continue
        try:
            raw_doc = json.loads(log_file.read_text(encoding="utf-8"))
            doc = bejson_core_sanitize_doc(raw_doc)
            fmap = bejson_core_get_field_map(doc)
            
            key_idx = fmap.get("log_event_key")
            msg_idx = fmap.get("log_event_message_text")
            ctx_idx = fmap.get("log_event_context_payload")
            subsys_idx = fmap.get("log_sender_subsystem_name")
            level_idx = fmap.get("log_event_level_kind")

            for row in doc.get("Values", []):
                if not isinstance(row, list):
                    continue
                entries_scanned += 1
                
                if subsys_idx is not None and row[subsys_idx]:
                    subsys = str(row[subsys_idx])
                    if subsys not in recent_subsystems:
                        recent_subsystems.append(subsys)

                if level_idx is not None and str(row[level_idx]).upper() in ("ERROR", "FATAL"):
                    msg = str(row[msg_idx]) if msg_idx is not None else "Unknown error"
                    recent_errors.append(f"[{dstr}] {msg}")

                if ctx_idx is not None and row[ctx_idx]:
                    try:
                        ctx_val = json.loads(row[ctx_idx])
                        if isinstance(ctx_val, dict):
                            ctx_inner = ctx_val.get("context", ctx_val)
                            task_title = ctx_inner.get("task")
                            if task_title and task_title not in recent_tasks:
                                recent_tasks.append(str(task_title))
                            mod_files = ctx_inner.get("files_modified", [])
                            if isinstance(mod_files, list):
                                for mf in mod_files:
                                    if str(mf) not in recent_files:
                                        recent_files.append(str(mf))
                    except Exception:
                        pass
                elif msg_idx is not None and row[msg_idx]:
                    msg = str(row[msg_idx])
                    if msg not in recent_tasks and len(msg) < 120:
                        recent_tasks.append(msg)

        except Exception as exc:
            LOG.error("Failed to read log file %s: %s", log_file, exc)

    return {
        "entries_scanned": entries_scanned,
        "recent_tasks": recent_tasks[:10],
        "recent_files": recent_files[:15],
        "recent_subsystems": recent_subsystems[:8],
        "recent_errors": recent_errors[:5],
    }


def scan_installed_skills(skills_dir: Path) -> List[str]:
    """Scans ~/.gemini/config/skills/ for installed skills."""
    if not skills_dir.exists():
        return []
    installed: List[str] = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            installed.append(item.name)
    return sorted(installed)


def build_grounding_dossier(
    definitions_path: Optional[Path] = None,
    skills_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Compiles the full grounding dossier."""
    def_path = definitions_path or Path("/storage/emulated/0/.env/user/definitions.json")
    defs = load_canonical_definitions(def_path)

    global_logs_dir = Path(defs.get("GLOBAL_LOGS", "/storage/emulated/0/Admin/System/Global_Logs"))
    logs_summary = scan_global_logs(global_logs_dir)

    sk_dir = skills_dir or Path("/data/data/com.termux/files/home/.gemini/config/skills")
    skills_list = scan_installed_skills(sk_dir)

    storage_roots = {
        "INTERNAL_STORAGE": defs.get("INTERNAL_STORAGE", "/storage/emulated/0"),
        "PROJECTS_ARCHIVE_ROOT": defs.get("PROJECTS_ARCHIVE_ROOT", "/storage/emulated/0/Admin/Core/Projects_Archive"),
        "GLOBAL_LOGS": str(global_logs_dir),
        "ADMIN_LIBRARIES_104": defs.get("ADMIN_LIBRARIES_104", "/storage/emulated/0/Admin/Libraries/libraries_104"),
        "ADMIN_LIBRARIES_105": defs.get("ADMIN_LIBRARIES_105", "/storage/emulated/0/Admin/Libraries/libraries_105"),
        "JOB_MANAGEMENT": defs.get("JOB_MANAGEMENT", "/storage/emulated/0/Admin/System/Job_Management"),
        "PROJECT_TYPE_LEDGER": defs.get("PROJECT_TYPE_LEDGER", "/storage/emulated/0/Admin/Dev/Policy/project_type_ledger.104a.bejson"),
        "PROJECT_CHUNKER": defs.get("PROJECT_CHUNKER", "/storage/emulated/0/Admin/System/Project_Chunker"),
    }

    negative_constraints = [
        "Do not edit official library directories without explicit instruction (Policy §1.1).",
        "Field Map Cache mandatory across all BEJSON operations; raw row[i] indexing prohibited (Policy §6.2).",
        "Zero raw field name string literals outside taxonomy registry modules (Policy §10.1).",
        "Always query and reuse pre-existing types from Project Type Ledger before assigning types (Policy Oct 25, 2026).",
        "Never auto-generate or assign global Project_GUID if missing; reserved for registration tooling (Policy §4.6).",
        "Daily global logs route strictly to $GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson (Policy Oct 31, 2026).",
    ]

    capture_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state_uuid = str(uuid.uuid4())

    dossier = {
        "state_uuid": state_uuid,
        "capture_timestamp": capture_ts,
        "definitions_path": str(def_path),
        "storage_roots": storage_roots,
        "recent_logs": logs_summary,
        "library_tiers": {
            "libraries_104": "Stable / Frozen (Primary Production Runtime)",
            "libraries_105": "Development / Active (Load only when instructed)",
        },
        "installed_skills_count": len(skills_list),
        "installed_skills_sample": skills_list[:12],
        "negative_constraints": negative_constraints,
        "summary": (
            f"Grounded operational state: {len(skills_list)} installed skills, "
            f"{logs_summary['entries_scanned']} log entries scanned, "
            f"{len(logs_summary['recent_tasks'])} active tasks tracked."
        ),
    }
    return dossier


def compile_bejson_container(dossier: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms the grounding dossier into a canonical BEJSON 104a document."""
    fields = [
        {"name": "state_uuid", "type": "string"},
        {"name": "capture_timestamp", "type": "string"},
        {"name": "environment_definitions_path", "type": "string"},
        {"name": "active_storage_roots", "type": "string"},
        {"name": "recent_global_log_keys", "type": "string"},
        {"name": "recent_completed_tasks", "type": "string"},
        {"name": "recent_files_modified", "type": "string"},
        {"name": "active_repositories", "type": "string"},
        {"name": "library_tiers_status", "type": "string"},
        {"name": "installed_skills_count", "type": "integer"},
        {"name": "active_negative_constraints", "type": "string"},
        {"name": "summary_digest", "type": "string"},
    ]

    values = [
        [
            dossier["state_uuid"],
            dossier["capture_timestamp"],
            dossier["definitions_path"],
            json.dumps(dossier["storage_roots"]),
            json.dumps(dossier["recent_logs"].get("recent_subsystems", [])),
            json.dumps(dossier["recent_logs"].get("recent_tasks", [])),
            json.dumps(dossier["recent_logs"].get("recent_files", [])),
            json.dumps(["BEJSON_CMS", "NewAgent", "NA-CMS", "BookWriter", "BKS_Standard"]),
            json.dumps(dossier["library_tiers"]),
            dossier["installed_skills_count"],
            json.dumps(dossier["negative_constraints"]),
            dossier["summary"],
        ]
    ]

    doc = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": ["CouncilGroundingState"],
        "Fields": fields,
        "Values": values,
    }
    return bejson_core_sanitize_doc(doc)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Council Grounding Scout: surveys environment definitions, global logs, and domain boundaries."
    )
    parser.add_argument("--definitions", type=Path, default=None, help="Path to definitions.json")
    parser.add_argument("--skills-dir", type=Path, default=None, help="Path to skills directory")
    parser.add_argument("--json", action="store_true", help="Print raw JSON dossier to stdout")
    parser.add_argument("--bejson-output", type=Path, default=None, help="Path to save BEJSON 104a container")
    parser.add_argument("--summary", action="store_true", help="Print formatted human-readable telemetry summary")
    args = parser.parse_args()

    try:
        dossier = build_grounding_dossier(args.definitions, args.skills_dir)
        
        if args.bejson_output:
            bejson_doc = compile_bejson_container(dossier)
            bejson_core_atomic_write(args.bejson_output, bejson_doc)
            LOG.info("BEJSON 104a grounding state written to %s", args.bejson_output)

        if args.json:
            print(json.dumps(dossier, indent=2, ensure_ascii=False))
        elif args.summary or not args.bejson_output:
            print("=" * 64)
            print("COUNCIL GROUNDING OPERATIONAL DOSSIER")
            print("=" * 64)
            print(f"State UUID:            {dossier['state_uuid']}")
            print(f"Capture Timestamp:     {dossier['capture_timestamp']}")
            print(f"Definitions Source:    {dossier['definitions_path']}")
            print(f"Installed Skills:      {dossier['installed_skills_count']} skills active")
            print(f"Global Logs Scanned:   {dossier['recent_logs']['entries_scanned']} entries")
            print("\nRecent Subsystems / Log Keys:")
            for s in dossier["recent_logs"]["recent_subsystems"]:
                print(f"  - {s}")
            print("\nRecent Active Tasks Tracked:")
            for t in dossier["recent_logs"]["recent_tasks"]:
                print(f"  - {t}")
            print("\nRecent Modified Files:")
            for f in dossier["recent_logs"]["recent_files"]:
                print(f"  - {f}")
            print("\nStorage Roots:")
            for k, v in dossier["storage_roots"].items():
                print(f"  {k:22}: {v}")
            print("\nActive Negative Constraints:")
            for nc in dossier["negative_constraints"]:
                print(f"  - {nc}")
            print("=" * 64)

        return EXIT_OK
    except Exception as exc:
        LOG.error("Failed to execute council grounding scout: %s", exc)
        return EXIT_SCHEMA_FAILURE


if __name__ == "__main__":
    sys.exit(main())
