#!/usr/bin/env python3
"""
Name: goal_drift_auditor.py
Description: Production CLI Tool for Goal Drift Auditing and Override Gateway.
             Monitors modified files, intercepts counteracting actions, halts execution,
             and provides Policy Section 1.2 User Confirmation Override logging.
Author: Elton Boehnen · boehnenelton2024@gmail.com
Version: 100
Release_Version: 300
RELATIONAL_ID: 7a8e4b01-9c64-4e5d-8a2b-6f10e4b017a8
"""

from pathlib import Path
import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional, Set

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_LOCK_ERROR: int = 10
EXIT_CONFIG_ENV_ERROR: int = 20
EXIT_DRIFT_HALT: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOGGER: logging.Logger = logging.getLogger("goal_drift_auditor")


class GoalDriftAuditorEngine:
    """
    Evaluates file operations and agent trajectories against active Goal Contracts.
    """

    def __init__(self, contract_file_path: Path):
        self.contract_file_path: Path = contract_file_path.resolve()
        if not self.contract_file_path.exists():
            raise FileNotFoundError(f"Goal contract not found at: {self.contract_file_path}")

    def load_contract(self) -> Dict[str, Any]:
        with open(self.contract_file_path, "r", encoding="utf-8") as contract_read_stream:
            contract_data = json.load(contract_read_stream)

        # Supports BEJSON 104a or flat JSON
        if contract_data.get("Format") == "BEJSON":
            field_map = {f["name"]: i for i, f in enumerate(contract_data["Fields"])}
            values = contract_data["Values"][0] if contract_data["Values"] else []
            return {
                "objective": values[field_map["objective"]] if "objective" in field_map else "",
                "allowed_targets": json.loads(values[field_map["allowed_targets"]]) if "allowed_targets" in field_map else [],
                "negative_constraints": json.loads(values[field_map["negative_constraints"]]) if "negative_constraints" in field_map else [],
            }
        return contract_data

    def audit_touched_files(self, touched_files_list: List[Path]) -> List[Dict[str, str]]:
        contract = self.load_contract()
        allowed_targets: List[str] = contract.get("allowed_targets", [])
        negative_constraints: List[str] = contract.get("negative_constraints", [])

        drift_violations: List[Dict[str, str]] = []

        for touched_file in touched_files_list:
            resolved_touched = touched_file.resolve()
            str_path = str(resolved_touched)

            # Check explicit negative constraints
            for constraint in negative_constraints:
                if constraint in str_path:
                    drift_violations.append({
                        "file": str_path,
                        "code": "DRIFT_CONSTRAINT_BREACH",
                        "detail": f"File violates negative constraint: '{constraint}'",
                    })

            # Check scope boundaries if allowed_targets declared
            if allowed_targets:
                is_allowed = any(target in str_path for target in allowed_targets)
                if not is_allowed:
                    drift_violations.append({
                        "file": str_path,
                        "code": "DRIFT_SCOPE_EXPANSION",
                        "detail": "File is outside declared goal targets.",
                    })

        return drift_violations

    def record_user_override(self, override_reason_text: str, project_root_directory: Path) -> Path:
        overrides_log_path = project_root_directory / "dev" / "goal_overrides.md"
        overrides_log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        with open(overrides_log_path, "a", encoding="utf-8") as override_append_stream:
            override_append_stream.write(f"\n## User Override Confirmed: {timestamp_utc}\n")
            override_append_stream.write(f"- **Contract:** `{self.contract_file_path.name}`\n")
            override_append_stream.write(f"- **Exemption Rationale:** {override_reason_text.strip()}\n")
            override_append_stream.write(f"- **Authorized Protocol:** Policy Section 1.2 User Confirmation\n")

        LOGGER.info("Logged user override exemption to: %s", overrides_log_path)
        return overrides_log_path


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Goal Drift Auditor & Blocker Gateway")
    parser.add_argument("--contract", type=str, required=True, help="Path to goal_contract.bejson.")
    parser.add_argument("--files", type=str, help="Comma-separated list of modified files.")
    parser.add_argument("--override", type=str, help="Confirm user override with rationale (Policy 1.2).")
    parser.add_argument("--project-root", type=str, default=".", help="Project root directory.")
    return parser.parse_args()


def main() -> None:
    cli_arguments = parse_cli_arguments()
    contract_file_path = Path(cli_arguments.contract)
    project_root = Path(cli_arguments.project_root).resolve()

    try:
        auditor = GoalDriftAuditorEngine(contract_file_path)

        if cli_arguments.override:
            auditor.record_user_override(cli_arguments.override, project_root)
            LOGGER.info("User override accepted. Execution unblocked.")
            print(json.dumps({"status": "OVERRIDE_GRANTED", "reason": cli_arguments.override}))
            sys.exit(EXIT_OK)

        touched_paths: List[Path] = []
        if cli_arguments.files:
            touched_paths = [Path(p.strip()) for p in cli_arguments.files.split(",") if p.strip()]

        violations = auditor.audit_touched_files(touched_paths)

        if violations:
            LOGGER.warning("GOAL DRIFT DETECTED: %d violation(s). Execution HALTED.", len(violations))
            discrepancy_payload = {
                "status": "HALTED",
                "violations_count": len(violations),
                "violations": violations,
                "remediation_gateway": [
                    {"option": 1, "action": "HALT_AND_REVERT", "description": "Revert the pending file modification."},
                    {"option": 2, "action": "CONFIRM_OVERRIDE", "flag": "--override <reason>", "description": "Grant ad-hoc user exemption per Policy 1.2."},
                    {"option": 3, "action": "AMEND_CONTRACT", "description": "Update goal contract with new target files."},
                ],
            }
            print(json.dumps(discrepancy_payload, indent=2))
            sys.exit(EXIT_DRIFT_HALT)

        LOGGER.info("Goal audit PASSED cleanly. Zero drift detected.")
        print(json.dumps({"status": "PASSED"}))
        sys.exit(EXIT_OK)

    except Exception as runtime_error:
        LOGGER.exception("Fatal runtime error during goal drift auditing: %s", runtime_error)
        sys.exit(EXIT_CONFIG_ENV_ERROR)


if __name__ == "__main__":
    main()
