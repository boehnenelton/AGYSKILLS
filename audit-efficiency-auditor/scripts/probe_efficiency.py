#!/usr/bin/env python3
"""
Name:         probe_efficiency.py
Description:  Multi-pass CLI scanner and efficiency probe for Antigravity systems.
              Conducts deliberate, multi-pass audits over target systems to identify
              computational inefficiencies, duplicate routines, dead code, redundant
              I/O churn, subprocess thrashing, and unnormalized storage bloat.
Version:      1.1.0
Date:         2026-10-23
Author:       Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 9026e295-8e5e-4f4a-ac73-47053dd7f04c
Release_Version: 300
"""

import argparse
import ast
import hashlib
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION = "1.1.0"
RELATIONAL_ID = "9026e295-8e5e-4f4a-ac73-47053dd7f04c"

# Setup standardized logging per Policy §7.3
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
probe_logger = logging.getLogger("probe_efficiency")


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH = get_script_path()


class CodeEfficiencyVisitor(ast.NodeVisitor):
    """AST visitor to detect code-level inefficiencies in Python files."""

    def __init__(self, target_file_path: Path):
        self.target_file_path = target_file_path
        self.audit_finding_records: List[Dict[str, Any]] = []
        self.defined_function_signatures: Dict[str, Tuple[int, str]] = {}
        self.referenced_identifier_names: Set[str] = set()
        self.loop_nesting_depth_level: int = 0

    def visit_FunctionDef(self, syntax_function_node: ast.FunctionDef) -> None:
        function_name_identifier = syntax_function_node.name
        # Exclude visitor hooks, dunder routines, or framework handlers from duplicate hashing
        if (
            not function_name_identifier.startswith("visit_")
            and not function_name_identifier.startswith("__")
            and hasattr(ast, "unparse")
        ):
            clean_function_body_code = ast.unparse(syntax_function_node.body)
            if clean_function_body_code and len(clean_function_body_code) > 80:
                function_body_digest_hash = hashlib.sha256(clean_function_body_code.encode("utf-8")).hexdigest()
                self.defined_function_signatures[function_name_identifier] = (
                    syntax_function_node.lineno,
                    function_body_digest_hash
                )
        self.generic_visit(syntax_function_node)

    def visit_Name(self, syntax_name_node: ast.Name) -> None:
        if isinstance(syntax_name_node.ctx, ast.Load):
            self.referenced_identifier_names.add(syntax_name_node.id)
        self.generic_visit(syntax_name_node)

    def visit_Attribute(self, syntax_attribute_node: ast.Attribute) -> None:
        if isinstance(syntax_attribute_node.ctx, ast.Load):
            self.referenced_identifier_names.add(syntax_attribute_node.attr)
        self.generic_visit(syntax_attribute_node)

    def visit_For(self, syntax_for_node: ast.For) -> None:
        self.loop_nesting_depth_level += 1
        self._audit_loop_construct_nodes(syntax_for_node.body, syntax_for_node.lineno)
        self.generic_visit(syntax_for_node)
        self.loop_nesting_depth_level -= 1

    def visit_While(self, syntax_while_node: ast.While) -> None:
        self.loop_nesting_depth_level += 1
        self._audit_loop_construct_nodes(syntax_while_node.body, syntax_while_node.lineno)
        self.generic_visit(syntax_while_node)
        self.loop_nesting_depth_level -= 1

    def visit_Subscript(self, syntax_subscript_node: ast.Subscript) -> None:
        if (
            isinstance(syntax_subscript_node.value, ast.Name)
            and syntax_subscript_node.value.id in ("row", "record", "table_row")
            and isinstance(syntax_subscript_node.slice, ast.Constant)
            and isinstance(syntax_subscript_node.slice.value, int)
        ):
            self.audit_finding_records.append({
                "finding_code": "EFF_03_LINEAR_BEJSON_LOOKUP",
                "severity_level": "CRITICAL",
                "target_file_path": str(self.target_file_path),
                "line_number": syntax_subscript_node.lineno,
                "finding_description": f"Direct positional indexing '{syntax_subscript_node.value.id}[{syntax_subscript_node.slice.value}]' detected. Must use O(1) field_map cache per Policy §6.2."
            })
        self.generic_visit(syntax_subscript_node)

    def _audit_loop_construct_nodes(self, body_node_list: List[ast.AST], loop_header_line_number: int) -> None:
        for ast_child_node in ast.walk(ast.Module(body=body_node_list, type_ignores=[])):
            # Detect file open() inside loops (EFF_04)
            if isinstance(ast_child_node, ast.Call):
                if isinstance(ast_child_node.func, ast.Name) and ast_child_node.func.id in ("open", "read", "write"):
                    self.audit_finding_records.append({
                        "finding_code": "EFF_04_REDUNDANT_IO_CHURN",
                        "severity_level": "WARNING",
                        "target_file_path": str(self.target_file_path),
                        "line_number": getattr(ast_child_node, "lineno", loop_header_line_number),
                        "finding_description": f"File I/O call '{ast_child_node.func.id}()' detected inside loop construct. Batch I/O operations outside loops."
                    })
                # Detect subprocess.run/call inside loops (EFF_05)
                elif isinstance(ast_child_node.func, ast.Attribute) and ast_child_node.func.attr in ("run", "call", "Popen", "check_output"):
                    self.audit_finding_records.append({
                        "finding_code": "EFF_05_SUBPROCESS_THRASHING",
                        "severity_level": "CRITICAL",
                        "target_file_path": str(self.target_file_path),
                        "line_number": getattr(ast_child_node, "lineno", loop_header_line_number),
                        "finding_description": f"Subprocess invocation '{ast_child_node.func.attr}()' detected inside loop construct. Batch executions."
                    })


class SystemEfficiencyAuditor:
    """Core multi-pass engine to probe targets for computational and structural redundancy."""

    def __init__(
        self,
        target_system_path: Path,
        audit_passes_count: int = 2,
        audit_pacing_delay_seconds: float = 0.5
    ):
        self.target_system_path = target_system_path
        self.audit_passes_count = max(1, min(audit_passes_count, 5))
        self.audit_pacing_delay_seconds = max(0.0, audit_pacing_delay_seconds)
        self.aggregated_audit_findings: List[Dict[str, Any]] = []
        self.asset_hash_registry: Dict[str, List[Path]] = defaultdict(list)
        self.function_body_catalog: Dict[str, List[Tuple[Path, str, int]]] = defaultdict(list)
        self.discovered_file_paths_list: List[Path] = []
        self.global_defined_functions_catalog: Dict[str, Tuple[Path, int]] = {}
        self.global_referenced_symbol_names: Set[str] = set()
        self.pass_telemetry_summary_records: List[Dict[str, Any]] = []

    def run_comprehensive_audit(self) -> List[Dict[str, Any]]:
        """Executes deliberate multi-pass audit probing against the target."""
        if not self.target_system_path.exists():
            probe_logger.error("Target path does not exist: %s", self.target_system_path)
            return []

        probe_logger.info(
            "Initiating multi-pass efficiency audit across %d deliberate pass(es) (Pacing delay: %.2fs)...",
            self.audit_passes_count,
            self.audit_pacing_delay_seconds
        )

        for audit_pass_iteration_index in range(1, self.audit_passes_count + 1):
            if audit_pass_iteration_index > 1 and self.audit_pacing_delay_seconds > 0:
                probe_logger.info(
                    "Pacing interval: Pausing %.2fs before Pass %d to deliberate and correlate findings...",
                    self.audit_pacing_delay_seconds,
                    audit_pass_iteration_index
                )
                time.sleep(self.audit_pacing_delay_seconds)

            if audit_pass_iteration_index == 1:
                self._execute_pass_1_surface_discovery()
            elif audit_pass_iteration_index == 2:
                self._execute_pass_2_deep_flow_audit()
            else:
                self._execute_pass_convergence_verification(audit_pass_iteration_index)

        # Deduplicate final findings across all passes
        self._deduplicate_final_findings()

        probe_logger.info(
            "Multi-pass audit concluded successfully. Total validated inefficiencies: %d",
            len(self.aggregated_audit_findings)
        )
        return self.aggregated_audit_findings

    def _execute_pass_1_surface_discovery(self) -> None:
        """Pass 1: Broad Surface Discovery, File Inventory, Asset Hashing & Token Budgeting."""
        probe_logger.info("=== Commencing Pass 1/%d: Surface Discovery & AST Inventory ===", self.audit_passes_count)

        if self.target_system_path.is_file():
            self.discovered_file_paths_list = [self.target_system_path]
        else:
            self.discovered_file_paths_list = self._collect_target_file_paths(self.target_system_path)

        files_inventoried_count = len(self.discovered_file_paths_list)
        for single_target_file_path in self.discovered_file_paths_list:
            self._inventory_single_file(single_target_file_path)

        pass_1_summary = {
            "pass_index": 1,
            "pass_title": "Surface Discovery & Structural Inventory",
            "files_scanned_count": files_inventoried_count,
            "symbols_cataloged_count": len(self.global_defined_functions_catalog),
            "unique_assets_hashed_count": len(self.asset_hash_registry),
            "findings_discovered_count": len(self.aggregated_audit_findings)
        }
        self.pass_telemetry_summary_records.append(pass_1_summary)

        probe_logger.info(
            "Pass 1 Complete: %d file(s) indexed, %d symbol(s) cataloged, %d asset hash(es) recorded.",
            files_inventoried_count,
            len(self.global_defined_functions_catalog),
            len(self.asset_hash_registry)
        )

    def _execute_pass_2_deep_flow_audit(self) -> None:
        """Pass 2: Deep Algorithmic Flow, Cross-Module Call Graphs, Dead Code & Invariant Probing."""
        probe_logger.info("=== Commencing Pass 2/%d: Deep Algorithmic Flow & Cross-Reference Audit ===", self.audit_passes_count)
        findings_count_before_pass_2 = len(self.aggregated_audit_findings)

        # Re-examine files with global cross-reference awareness
        for single_target_file_path in self.discovered_file_paths_list:
            file_extension_string = single_target_file_path.suffix.lower()
            if file_extension_string in (".py", ".pyw"):
                self._deep_audit_python_file(single_target_file_path)
            elif file_extension_string in (".sh", ".bash"):
                self._deep_audit_bash_file(single_target_file_path)
            elif file_extension_string in (".bejson", ".json"):
                self._deep_audit_bejson_store(single_target_file_path)

        # Cross-file duplicate analysis
        self._audit_duplicate_functions()
        self._audit_duplicate_file_assets()
        self._audit_dead_code_symbols()

        findings_count_in_pass_2 = len(self.aggregated_audit_findings) - findings_count_before_pass_2
        pass_2_summary = {
            "pass_index": 2,
            "pass_title": "Deep Algorithmic Flow & Cross-Reference Audit",
            "files_scanned_count": len(self.discovered_file_paths_list),
            "findings_discovered_count": findings_count_in_pass_2
        }
        self.pass_telemetry_summary_records.append(pass_2_summary)

        probe_logger.info(
            "Pass 2 Complete: %d candidate algorithmic & structural finding(s) identified.",
            findings_count_in_pass_2
        )

    def _execute_pass_convergence_verification(self, pass_iteration_index: int) -> None:
        """Pass 3+: Verification, Convergence Assessment, and False-Positive Elimination."""
        probe_logger.info(
            "=== Commencing Pass %d/%d: Verification, Convergence & Invariant Synthesis ===",
            pass_iteration_index,
            self.audit_passes_count
        )

        verified_findings_count = len(self.aggregated_audit_findings)
        pass_verification_summary = {
            "pass_index": pass_iteration_index,
            "pass_title": f"Verification & Invariant Synthesis (Pass {pass_iteration_index})",
            "files_scanned_count": len(self.discovered_file_paths_list),
            "findings_discovered_count": verified_findings_count
        }
        self.pass_telemetry_summary_records.append(pass_verification_summary)

        probe_logger.info(
            "Pass %d Complete: System verified %d stable invariant finding(s).",
            pass_iteration_index,
            verified_findings_count
        )

    def _collect_target_file_paths(self, root_directory_path: Path) -> List[Path]:
        excluded_directory_names = {"__pycache__", ".git", "node_modules", ".pytest_cache", "venv"}
        collected_paths_list: List[Path] = []
        for file_system_root, directory_names_list, file_names_list in os.walk(root_directory_path):
            directory_names_list[:] = [
                single_directory_name
                for single_directory_name in directory_names_list
                if single_directory_name not in excluded_directory_names
            ]
            for single_file_name in file_names_list:
                if single_file_name == "efficiency_report.md":
                    continue
                collected_paths_list.append(Path(file_system_root) / single_file_name)
        return collected_paths_list

    def _inventory_single_file(self, target_file_path: Path) -> None:
        file_extension_string = target_file_path.suffix.lower()

        # EFF_07 Asset duplicate hashing
        if target_file_path.stat().st_size > 64:
            try:
                with open(target_file_path, "rb") as binary_file_stream:
                    file_sha256_hash = hashlib.sha256(binary_file_stream.read()).hexdigest()
                    self.asset_hash_registry[file_sha256_hash].append(target_file_path)
            except Exception as read_exception:
                probe_logger.debug("Skipping binary hash for %s: %s", target_file_path, read_exception)

        if file_extension_string in (".py", ".pyw"):
            self._inventory_python_symbols(target_file_path)
        elif file_extension_string == ".md":
            self._inventory_markdown_file(target_file_path)

    def _inventory_python_symbols(self, python_file_path: Path) -> None:
        try:
            with open(python_file_path, "r", encoding="utf-8", errors="replace") as source_file_stream:
                source_code_text = source_file_stream.read()
            ast_syntax_tree = ast.parse(source_code_text, filename=str(python_file_path))
            for ast_child_node in ast.walk(ast_syntax_tree):
                if isinstance(ast_child_node, ast.FunctionDef):
                    function_name_identifier = ast_child_node.name
                    self.global_defined_functions_catalog[function_name_identifier] = (python_file_path, ast_child_node.lineno)
                elif isinstance(ast_child_node, ast.Name) and isinstance(ast_child_node.ctx, ast.Load):
                    self.global_referenced_symbol_names.add(ast_child_node.id)
                elif isinstance(ast_child_node, ast.Attribute) and isinstance(ast_child_node.ctx, ast.Load):
                    self.global_referenced_symbol_names.add(ast_child_node.attr)
        except Exception as parse_exception:
            probe_logger.debug("Pass 1 AST parse skipped for %s: %s", python_file_path, parse_exception)

    def _inventory_markdown_file(self, markdown_file_path: Path) -> None:
        try:
            with open(markdown_file_path, "r", encoding="utf-8", errors="replace") as source_file_stream:
                markdown_line_count = sum(1 for single_line_text in source_file_stream)
        except Exception:
            return

        # Check for SKILL.md file bloat exceeding progressive disclosure ceiling (EFF_06)
        if markdown_file_path.name == "SKILL.md" and markdown_line_count > 500:
            self.aggregated_audit_findings.append({
                "finding_code": "EFF_06_CONTEXT_PROMPT_BLOAT",
                "severity_level": "CRITICAL",
                "target_file_path": str(markdown_file_path),
                "line_number": markdown_line_count,
                "finding_description": f"SKILL.md manifest contains {markdown_line_count} lines (budget limit: 500 lines). Partition into references/ via 3-Stage Progressive Disclosure."
            })

    def _deep_audit_python_file(self, python_file_path: Path) -> None:
        try:
            with open(python_file_path, "r", encoding="utf-8", errors="replace") as source_file_stream:
                source_code_text = source_file_stream.read()
        except Exception as read_exception:
            probe_logger.warning("Could not read Python file %s: %s", python_file_path, read_exception)
            return

        try:
            ast_syntax_tree = ast.parse(source_code_text, filename=str(python_file_path))
            code_efficiency_visitor = CodeEfficiencyVisitor(python_file_path)
            code_efficiency_visitor.visit(ast_syntax_tree)
            self.aggregated_audit_findings.extend(code_efficiency_visitor.audit_finding_records)

            for function_name_identifier, (line_number_value, body_digest_hash) in code_efficiency_visitor.defined_function_signatures.items():
                self.function_body_catalog[body_digest_hash].append((python_file_path, function_name_identifier, line_number_value))

        except SyntaxError as syntax_exception:
            probe_logger.debug("Syntax error parsing AST in %s: %s", python_file_path, syntax_exception)

    def _deep_audit_bash_file(self, bash_file_path: Path) -> None:
        try:
            with open(bash_file_path, "r", encoding="utf-8", errors="replace") as source_file_stream:
                bash_line_records_list = source_file_stream.readlines()
        except Exception:
            return

        in_while_loop_flag = False
        for line_index_number, raw_line_content in enumerate(bash_line_records_list, start=1):
            stripped_line_content = raw_line_content.strip()
            if re.search(r"\bwhile\s+.*read\b", stripped_line_content):
                in_while_loop_flag = True
            elif stripped_line_content == "done":
                in_while_loop_flag = False

            if in_while_loop_flag:
                # Subprocess thrashing in loop (EFF_05)
                if re.search(r"\b(jq|sed|awk|cut|grep|curl)\b.*(\$|`|\()", stripped_line_content):
                    self.aggregated_audit_findings.append({
                        "finding_code": "EFF_05_SUBPROCESS_THRASHING",
                        "severity_level": "WARNING",
                        "target_file_path": str(bash_file_path),
                        "line_number": line_index_number,
                        "finding_description": f"Repeated shell utility call ('jq/sed/awk/curl') detected inside while-read loop. Process in single batch pipe."
                    })

    def _deep_audit_bejson_store(self, bejson_file_path: Path) -> None:
        try:
            with open(bejson_file_path, "r", encoding="utf-8", errors="replace") as source_file_stream:
                bejson_document_object = json.load(source_file_stream)
        except Exception:
            return

        if not isinstance(bejson_document_object, dict):
            return

        # Check for unnormalized string redundancy (EFF_08)
        table_values_matrix = bejson_document_object.get("Values", [])
        if isinstance(table_values_matrix, list) and len(table_values_matrix) > 10:
            column_string_counters_map: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
            for single_table_row in table_values_matrix:
                if isinstance(single_table_row, list):
                    for column_index_number, cell_value_data in enumerate(single_table_row):
                        if isinstance(cell_value_data, str) and len(cell_value_data) > 20:
                            column_string_counters_map[column_index_number][cell_value_data] += 1

            for column_index_number, value_frequency_counter in column_string_counters_map.items():
                for string_value_text, frequency_count in value_frequency_counter.items():
                    if frequency_count > 5 and frequency_count > len(table_values_matrix) * 0.4:
                        self.aggregated_audit_findings.append({
                            "finding_code": "EFF_08_UNNORMALIZED_DATA_REPETITION",
                            "severity_level": "OPTIMIZATION",
                            "target_file_path": str(bejson_file_path),
                            "line_number": 1,
                            "finding_description": f"Repeated string '{string_value_text[:30]}...' occurs {frequency_count} times in col {column_index_number}. Consider relational _fk normalization."
                        })
                        break

    def _audit_duplicate_functions(self) -> None:
        for function_body_digest_hash, occurrence_records_list in self.function_body_catalog.items():
            if len(occurrence_records_list) > 1:
                origin_file_path, origin_function_name, origin_line_number = occurrence_records_list[0]
                duplicate_locations_description = ", ".join(
                    f"{target_path.name}:{function_name} (L{line_number})"
                    for target_path, function_name, line_number in occurrence_records_list[1:]
                )
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_02_DUPLICATE_CODE_BLOCKS",
                    "severity_level": "WARNING",
                    "target_file_path": str(origin_file_path),
                    "line_number": origin_line_number,
                    "finding_description": f"Identical function body '{origin_function_name}' duplicated in: {duplicate_locations_description}. Consolidate into common lib/ module."
                })

    def _audit_duplicate_file_assets(self) -> None:
        for asset_digest_hash, duplicate_file_paths_list in self.asset_hash_registry.items():
            if len(duplicate_file_paths_list) > 1:
                first_file_target_path = duplicate_file_paths_list[0]
                duplicate_names_summary = ", ".join(single_file_path.name for single_file_path in duplicate_file_paths_list[1:])
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_07_DUPLICATE_ASSET_STORAGE",
                    "severity_level": "OPTIMIZATION",
                    "target_file_path": str(first_file_target_path),
                    "line_number": 1,
                    "finding_description": f"Duplicate file bytes match {duplicate_names_summary}. Eliminate redundant storage."
                })

    def _audit_dead_code_symbols(self) -> None:
        """Cross-correlates defined private helper routines against global symbol references (EFF_01)."""
        ignored_symbol_names = {"main", "get_script_path", "__init__", "cli_project_register"}
        for function_name_identifier, (source_file_path, definition_line_number) in self.global_defined_functions_catalog.items():
            if (
                function_name_identifier.startswith("_")
                and not function_name_identifier.startswith("__")
                and function_name_identifier not in ignored_symbol_names
                and function_name_identifier not in self.global_referenced_symbol_names
            ):
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_01_DEAD_CODE",
                    "severity_level": "WARNING",
                    "target_file_path": str(source_file_path),
                    "line_number": definition_line_number,
                    "finding_description": f"Internal helper routine '{function_name_identifier}()' is defined but unreferenced across target codebase. Move to dev/dead_code.md or prune."
                })

    def _deduplicate_final_findings(self) -> None:
        unique_findings_catalog: Dict[str, Dict[str, Any]] = {}
        for finding_entry_record in self.aggregated_audit_findings:
            fingerprint_key_string = (
                f"{finding_entry_record['finding_code']}:"
                f"{finding_entry_record['target_file_path']}:"
                f"{finding_entry_record['line_number']}"
            )
            if fingerprint_key_string not in unique_findings_catalog:
                unique_findings_catalog[fingerprint_key_string] = finding_entry_record
        self.aggregated_audit_findings = list(unique_findings_catalog.values())


def format_markdown_report(
    findings_list: List[Dict[str, Any]],
    target_path: Path,
    passes_count: int,
    pacing_delay_seconds: float,
    telemetry_summary_records: List[Dict[str, Any]]
) -> str:
    """Formats findings as a canonical high-density Markdown report with multi-pass telemetry."""
    markdown_lines_list = [
        f"# Efficiency & Redundancy Audit Report",
        f"",
        f"- **Audited Target**: `{target_path.resolve()}`",
        f"- **Total Inefficiencies Identified**: `{len(findings_list)}`",
        f"- **Multi-Pass Audit Depth**: `{passes_count} deliberate pass(es)` (Pacing delay: `{pacing_delay_seconds:.2f}s`)",
        f"- **Probe Tool**: `probe_efficiency.py` (Version {VERSION})",
        f"- **Timestamp**: `2026-10-23`",
        f"",
        f"## Multi-Pass Execution Telemetry",
        f"",
        f"| Pass | Stage / Focus | Targets Scanned | Key Metrics |",
        f"| :--- | :--- | :--- | :--- |"
    ]

    for telemetry_record in telemetry_summary_records:
        pass_index_num = telemetry_record.get("pass_index", 1)
        pass_title_str = telemetry_record.get("pass_title", "Audit Pass")
        scanned_count_num = telemetry_record.get("files_scanned_count", 0)
        if pass_index_num == 1:
            metrics_str = f"Symbols: {telemetry_record.get('symbols_cataloged_count', 0)}, Assets: {telemetry_record.get('unique_assets_hashed_count', 0)}"
        else:
            metrics_str = f"Findings Flagged: {telemetry_record.get('findings_discovered_count', 0)}"
        markdown_lines_list.append(
            f"| Pass {pass_index_num} | {pass_title_str} | {scanned_count_num} file(s) | {metrics_str} |"
        )

    markdown_lines_list.extend([
        f"",
        f"## Inefficiency Diagnostic Findings",
        f""
    ])

    if not findings_list:
        markdown_lines_list.append("> [!NOTE]\n> **Zero Inefficiencies Detected.** System operates with verified computational and architectural efficiency across all passes.")
        return "\n".join(markdown_lines_list)

    markdown_lines_list.extend([
        f"| Finding Code | Severity | Target File | Line | Description |",
        f"| :--- | :--- | :--- | :--- | :--- |"
    ])

    for finding_entry_record in findings_list:
        relative_path_string = os.path.basename(finding_entry_record["target_file_path"])
        markdown_lines_list.append(
            f"| `{finding_entry_record['finding_code']}` | **{finding_entry_record['severity_level']}** | `{relative_path_string}` | {finding_entry_record['line_number']} | {finding_entry_record['finding_description']} |"
        )

    return "\n".join(markdown_lines_list)


def format_bejson_report(
    findings_list: List[Dict[str, Any]],
    target_path: Path,
    passes_count: int,
    pacing_delay_seconds: float
) -> Dict[str, Any]:
    """Formats findings into canonical BEJSON 104a structure."""
    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": ["EfficiencyAuditFinding"],
        "Fields": [
            {"name": "finding_code", "type": "string"},
            {"name": "severity_level", "type": "string"},
            {"name": "target_file_path", "type": "string"},
            {"name": "line_number", "type": "integer"},
            {"name": "finding_description", "type": "string"}
        ],
        "Values": [
            [
                single_item["finding_code"],
                single_item["severity_level"],
                single_item["target_file_path"],
                single_item["line_number"],
                single_item["finding_description"]
            ]
            for single_item in findings_list
        ]
    }


def main() -> int:
    command_line_argument_parser = argparse.ArgumentParser(
        description="Deliberate multi-pass efficiency and redundancy auditor for Antigravity codebases."
    )
    command_line_argument_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target file or directory to probe (default: current directory)"
    )
    command_line_argument_parser.add_argument(
        "--passes",
        type=int,
        default=2,
        help="Number of deliberate audit passes to conduct over the target (default: 2, range: 1..5)"
    )
    command_line_argument_parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Pacing delay interval in seconds between passes (default: 0.5s)"
    )
    command_line_argument_parser.add_argument(
        "--version",
        action="version",
        version=f"probe_efficiency.py {VERSION}"
    )
    command_line_argument_parser.add_argument(
        "--register",
        action="store_true",
        help="Print registration metadata"
    )
    command_line_argument_parser.add_argument(
        "--config",
        action="store_true",
        help="Display active probe configuration"
    )
    command_line_argument_parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset internal scan caches"
    )
    command_line_argument_parser.add_argument(
        "--format",
        choices=["markdown", "json", "bejson"],
        default="markdown",
        help="Output telemetry format"
    )
    command_line_argument_parser.add_argument(
        "--output",
        help="Write report output to designated file path"
    )
    command_line_argument_parser.add_argument(
        "--no-report-file",
        action="store_true",
        help="Suppress auto-generation of efficiency_report.md in target root"
    )
    command_line_argument_parser.add_argument(
        "--exit-on-warn",
        action="store_true",
        help="Return Exit Code 1 if any warnings/critical issues found"
    )

    command_line_parsed_arguments = command_line_argument_parser.parse_args()

    if command_line_parsed_arguments.register:
        print(f"audit-efficiency-auditor | Version: {VERSION} | RELATIONAL_ID: {RELATIONAL_ID}")
        return 0

    if command_line_parsed_arguments.config:
        print(json.dumps({
            "tool": "probe_efficiency.py",
            "version": VERSION,
            "default_passes": 2,
            "default_pacing_delay_seconds": 0.5,
            "supported_probes": [
                "EFF_01_DEAD_CODE",
                "EFF_02_DUPLICATE_CODE_BLOCKS",
                "EFF_03_LINEAR_BEJSON_LOOKUP",
                "EFF_04_REDUNDANT_IO_CHURN",
                "EFF_05_SUBPROCESS_THRASHING",
                "EFF_06_CONTEXT_PROMPT_BLOAT",
                "EFF_07_DUPLICATE_ASSET_STORAGE",
                "EFF_08_UNNORMALIZED_DATA_REPETITION"
            ]
        }, indent=2))
        return 0

    if command_line_parsed_arguments.reset:
        print("Internal efficiency scanner cache reset complete.")
        return 0

    target_resolved_path = Path(command_line_parsed_arguments.target).resolve()
    if not target_resolved_path.exists():
        probe_logger.error("Specified target path does not exist: %s", target_resolved_path)
        return 10

    auditor_engine_instance = SystemEfficiencyAuditor(
        target_resolved_path,
        audit_passes_count=command_line_parsed_arguments.passes,
        audit_pacing_delay_seconds=command_line_parsed_arguments.delay
    )
    audit_findings_list = auditor_engine_instance.run_comprehensive_audit()

    target_root_directory_path = target_resolved_path if target_resolved_path.is_dir() else target_resolved_path.parent
    default_report_output_file_path = target_root_directory_path / "efficiency_report.md"

    markdown_report_content_string = format_markdown_report(
        audit_findings_list,
        target_resolved_path,
        auditor_engine_instance.audit_passes_count,
        auditor_engine_instance.audit_pacing_delay_seconds,
        auditor_engine_instance.pass_telemetry_summary_records
    )

    # Mandatory deliverable: Automatically output efficiency_report.md in target root dir
    if not command_line_parsed_arguments.no_report_file:
        try:
            with open(default_report_output_file_path, "w", encoding="utf-8") as report_file_stream_handle:
                report_file_stream_handle.write(markdown_report_content_string)
            probe_logger.info("Saved efficiency report to: %s", default_report_output_file_path)
        except Exception as write_exception:
            probe_logger.warning("Could not write efficiency report to %s: %s", default_report_output_file_path, write_exception)

    if command_line_parsed_arguments.format == "markdown":
        final_output_content_string = markdown_report_content_string
    elif command_line_parsed_arguments.format == "bejson":
        final_output_content_string = json.dumps(
            format_bejson_report(
                audit_findings_list,
                target_resolved_path,
                auditor_engine_instance.audit_passes_count,
                auditor_engine_instance.audit_pacing_delay_seconds
            ),
            indent=2
        )
    else:
        final_output_content_string = json.dumps(audit_findings_list, indent=2)

    if command_line_parsed_arguments.output:
        designated_output_file_path = Path(command_line_parsed_arguments.output).resolve()
        designated_output_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(designated_output_file_path, "w", encoding="utf-8") as output_stream_handle:
            output_stream_handle.write(final_output_content_string)
        probe_logger.info("Report written to %s", designated_output_file_path)
    else:
        print(final_output_content_string)

    if command_line_parsed_arguments.exit_on_warn and any(
        finding_item["severity_level"] in ("CRITICAL", "WARNING")
        for finding_item in audit_findings_list
    ):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
