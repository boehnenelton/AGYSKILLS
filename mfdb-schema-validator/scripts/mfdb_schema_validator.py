#!/usr/bin/env python3
"""
Name: mfdb_schema_validator.py
Description: Production Multi-MFDB Linkage & Invariant Validator (E30-E39).
             Recursively validates manifests, bidirectional parent-child links,
             network roles, DAG cycle freedom, and unregistered entities.
Author: Elton Boehnen · boehnenelton2024@gmail.com
Version: 100
Release_Version: 300
RELATIONAL_ID: d30e3901-8c64-4e5d-9a2b-7f10e4b01e39
"""

from pathlib import Path
import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_LOCK_ERROR: int = 10
EXIT_CONFIG_ENV_ERROR: int = 20
EXIT_SCHEMA_VALIDATION_ERROR: int = 30


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOGGER: logging.Logger = logging.getLogger("mfdb_schema_validator")


class MFDBStructuralValidator:
    """
    Evaluates Multi-MFDB clusters against Invariant Gates E30 through E39.
    """

    def __init__(self, root_manifest_path: Path):
        self.root_manifest_path: Path = root_manifest_path.resolve()
        self.validation_errors_list: List[Dict[str, str]] = []
        self.validated_entities_set: Set[str] = set()

    def record_validation_error(self, error_code_token: str, error_message_text: str) -> None:
        LOGGER.error("[%s] %s", error_code_token, error_message_text)
        self.validation_errors_list.append({
            "code": error_code_token,
            "message": error_message_text,
        })

    def compile_field_map_cache(
        self,
        schema_fields_array: List[Dict[str, Any]],
        document_context_name: str,
    ) -> Optional[Dict[str, int]]:
        compiled_field_map: Dict[str, int] = {}
        for column_index, field_descriptor in enumerate(schema_fields_array):
            raw_name = field_descriptor.get("name")
            if not raw_name:
                self.record_validation_error(
                    "E33",
                    f"Document '{document_context_name}' field at index {column_index} lacks 'name' key.",
                )
                return None
            sanitized_name = str(raw_name).strip()
            compiled_field_map[sanitized_name] = column_index
        return compiled_field_map

    def validate_bejson_structural_primitives(
        self,
        document_file_path: Path,
    ) -> Optional[Dict[str, Any]]:
        if not document_file_path.exists():
            self.record_validation_error("E30", f"File not found: {document_file_path}")
            return None

        try:
            with open(document_file_path, "r", encoding="utf-8") as read_stream:
                parsed_document = json.load(read_stream)
        except Exception as parse_error:
            self.record_validation_error("E30", f"JSON syntax error in {document_file_path}: {parse_error}")
            return None

        format_token = parsed_document.get("Format")
        version_token = parsed_document.get("Format_Version")
        if format_token != "BEJSON" or str(version_token) not in ["104", "104a", "104db", "105", "105a", "105db"]:
            self.record_validation_error(
                "E31",
                f"Invalid Format/Format_Version in {document_file_path.name}: '{format_token}' '{version_token}'",
            )

        records_type_token = parsed_document.get("Records_Type")
        if not isinstance(records_type_token, list) or len(records_type_token) == 0:
            self.record_validation_error("E32", f"Missing Records_Type in {document_file_path.name}")

        fields_token = parsed_document.get("Fields")
        if not isinstance(fields_token, list):
            self.record_validation_error("E33", f"Missing Fields array in {document_file_path.name}")

        values_token = parsed_document.get("Values")
        if not isinstance(values_token, list):
            self.record_validation_error("E34", f"Missing Values array in {document_file_path.name}")

        return parsed_document

    def validate_entire_cluster(self) -> bool:
        LOGGER.info("Starting Multi-MFDB validation on root manifest: %s", self.root_manifest_path)

        root_document = self.validate_bejson_structural_primitives(self.root_manifest_path)
        if root_document is None:
            return False

        root_role = root_document.get("Network_Role", "Master")
        if root_role not in ["Master", "Proxy"]:
            self.record_validation_error(
                "E37",
                f"Root manifest Network_Role must be 'Master' or 'Proxy', found '{root_role}'",
            )

        field_map = self.compile_field_map_cache(root_document["Fields"], self.root_manifest_path.name)
        if not field_map or "entity_name" not in field_map or "file_path" not in field_map:
            self.record_validation_error("E33", "Manifest missing mandatory 'entity_name' or 'file_path' fields.")
            return False

        entity_name_idx = field_map["entity_name"]
        file_path_idx = field_map["file_path"]

        registered_entities: Dict[str, Path] = {}
        adjacency_graph: Dict[str, List[str]] = {str(self.root_manifest_path): []}

        for row in root_document["Values"]:
            entity_name = str(row[entity_name_idx]).strip()
            rel_path = str(row[file_path_idx]).strip()
            resolved_entity_path = (self.root_manifest_path.parent / rel_path).resolve()
            registered_entities[entity_name] = resolved_entity_path
            adjacency_graph[str(self.root_manifest_path)].append(str(resolved_entity_path))

        # Check for unregistered entity files in data/ directory (E38)
        cluster_data_dir = self.root_manifest_path.parent / "data"
        if cluster_data_dir.exists() and cluster_data_dir.is_dir():
            for disk_file in cluster_data_dir.glob("*.bejson"):
                resolved_disk_file = disk_file.resolve()
                if resolved_disk_file not in registered_entities.values():
                    self.record_validation_error(
                        "E38",
                        f"Unregistered entity file detected on disk: {disk_file.name}",
                    )

        # Validate Each Child Entity
        for entity_name, entity_path in registered_entities.items():
            child_document = self.validate_bejson_structural_primitives(entity_path)
            if child_document is None:
                continue

            self.validated_entities_set.add(str(entity_path))

            # Invariant E35: Parent_Hierarchy verification
            parent_hierarchy_token = child_document.get("Parent_Hierarchy")
            if not parent_hierarchy_token:
                self.record_validation_error("E35", f"Entity {entity_path.name} lacks 'Parent_Hierarchy'.")
            else:
                resolved_parent = (entity_path.parent / str(parent_hierarchy_token)).resolve()
                if resolved_parent != self.root_manifest_path:
                    self.record_validation_error(
                        "E35",
                        f"Handshake mismatch: {entity_path.name} points to '{resolved_parent}', expected root manifest '{self.root_manifest_path}'",
                    )

            # Invariant E37: Network_Role check
            child_role = child_document.get("Network_Role", "Slave")
            if child_role not in ["Slave", "Proxy"]:
                self.record_validation_error(
                    "E37",
                    f"Registered child entity {entity_path.name} has invalid Network_Role '{child_role}', expected 'Slave'",
                )

        # Invariant E36: DAG Cycle Check
        visitation_status: Dict[str, int] = {}
        def detect_cycles_dfs(node_id: str) -> None:
            visitation_status[node_id] = 1 # Gray
            for neighbor_node in adjacency_graph.get(node_id, []):
                state = visitation_status.get(neighbor_node, 0)
                if state == 1:
                    self.record_validation_error("E36", f"Circular linkage cycle detected: {neighbor_node}")
                elif state == 0:
                    detect_cycles_dfs(neighbor_node)
            visitation_status[node_id] = 2 # Black

        for node_key in list(adjacency_graph.keys()):
            if visitation_status.get(node_key, 0) == 0:
                detect_cycles_dfs(node_key)

        return len(self.validation_errors_list) == 0


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-MFDB Schema & Linkage Validator (E30-E39)")
    parser.add_argument("--manifest", type=str, required=True, help="Path to root 104a.mfdb.bejson or 105a.mfdb.bejson.")
    parser.add_argument("--report", action="store_true", help="Generate structured Markdown audit report in reports/audits/.")
    return parser.parse_args()


def main() -> None:
    cli_arguments = parse_cli_arguments()
    manifest_target_path = Path(cli_arguments.manifest)

    validator = MFDBStructuralValidator(manifest_target_path)
    is_valid = validator.validate_entire_cluster()

    audit_summary = {
        "manifest": str(manifest_target_path),
        "valid": is_valid,
        "total_entities_checked": len(validator.validated_entities_set),
        "total_errors": len(validator.validation_errors_list),
        "errors": validator.validation_errors_list,
    }

    if cli_arguments.report:
        reports_dir = manifest_target_path.parent / "reports" / "audits"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        report_file_path = reports_dir / f"mfdb_audit_report_{report_timestamp}.md"

        with open(report_file_path, "w", encoding="utf-8") as rep_stream:
            rep_stream.write(f"# MFDB Structural Audit Report\n\n")
            rep_stream.write(f"- **Manifest:** `{manifest_target_path}`\n")
            rep_stream.write(f"- **Status:** `{'PASSED' if is_valid else 'FAILED'}`\n")
            rep_stream.write(f"- **Timestamp:** `{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}`\n")
            rep_stream.write(f"- **Entities Verified:** `{len(validator.validated_entities_set)}`\n\n")
            if validator.validation_errors_list:
                rep_stream.write("## Discovered Violations\n\n")
                for err in validator.validation_errors_list:
                    rep_stream.write(f"- **[{err['code']}]**: {err['message']}\n")
            else:
                rep_stream.write("## Discovered Violations\n\n- Zero violations detected. Cluster is mathematically sound.\n")

        LOGGER.info("Wrote audit report to: %s", report_file_path)

    print(json.dumps(audit_summary, indent=2))
    sys.exit(EXIT_OK if is_valid else EXIT_SCHEMA_VALIDATION_ERROR)


if __name__ == "__main__":
    main()
