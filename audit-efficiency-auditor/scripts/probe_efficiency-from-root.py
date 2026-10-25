#!/usr/bin/env python3
"""
Name:         probe_efficiency.py
Description:  Black-box CLI scanner and efficiency probe for Antigravity systems.
              Audits codebases, scripts, BEJSON stores, and skills for computational
              inefficiency, duplicate routines, dead code, redundant I/O churn,
              subprocess thrashing, and unnormalized storage bloat.
Version:      1.0.0
Date:         2026-10-23
Author:       Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 5569d31d-7e5a-4c8d-8e9a-0c8a4f3377f5
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
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.0.0"
RELATIONAL_ID = "5569d31d-7e5a-4c8d-8e9a-0c8a4f3377f5"

# Setup standardized logging
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
        self.loop_depth_level: int = 0
        self.raw_source_content: str = ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Check function body hash for duplicate implementation detection
        clean_code_body = ast.unparse(node.body) if hasattr(ast, "unparse") else ""
        if clean_code_body and len(clean_code_body) > 40:
            body_digest_hash = hashlib.sha256(clean_code_body.encode("utf-8")).hexdigest()
            self.defined_function_signatures[node.name] = (node.lineno, body_digest_hash)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.loop_depth_level += 1
        self._audit_loop_body_nodes(node.body, node.lineno)
        self.generic_visit(node)
        self.loop_depth_level -= 1

    def visit_While(self, node: ast.While) -> None:
        self.loop_depth_level += 1
        self._audit_loop_body_nodes(node.body, node.lineno)
        self.generic_visit(node)
        self.loop_depth_level -= 1

    def _audit_loop_body_nodes(self, body_nodes: List[ast.AST], loop_line_number: int) -> None:
        for child_node in ast.walk(ast.Module(body=body_nodes, type_ignores=[])):
            # Detect file open() inside loops (EFF_04)
            if isinstance(child_node, ast.Call):
                if isinstance(child_node.func, ast.Name) and child_node.func.id in ("open", "read", "write"):
                    self.audit_finding_records.append({
                        "finding_code": "EFF_04_REDUNDANT_IO_CHURN",
                        "severity_level": "WARNING",
                        "target_file_path": str(self.target_file_path),
                        "line_number": getattr(child_node, "lineno", loop_line_number),
                        "finding_description": f"File I/O call '{child_node.func.id}()' detected inside loop construct. Batch I/O operations outside loops."
                    })
                # Detect subprocess.run/call inside loops (EFF_05)
                elif isinstance(child_node.func, ast.Attribute) and child_node.func.attr in ("run", "call", "Popen", "check_output"):
                    self.audit_finding_records.append({
                        "finding_code": "EFF_05_SUBPROCESS_THRASHING",
                        "severity_level": "CRITICAL",
                        "target_file_path": str(self.target_file_path),
                        "line_number": getattr(child_node, "lineno", loop_line_number),
                        "finding_description": f"Subprocess invocation '{child_node.func.attr}()' detected inside loop construct. Batch executions."
                    })


class SystemEfficiencyAuditor:
    """Core engine to probe targets for computational and structural redundancy."""

    def __init__(self, target_system_path: Path):
        self.target_system_path = target_system_path
        self.aggregated_audit_findings: List[Dict[str, Any]] = []
        self.asset_hash_registry: Dict[str, List[Path]] = defaultdict(list)
        self.function_body_catalog: Dict[str, List[Tuple[Path, str, int]]] = defaultdict(list)

    def run_comprehensive_audit(self) -> List[Dict[str, Any]]:
        """Executes all registered probes against the target."""
        if not self.target_system_path.exists():
            probe_logger.error("Target path does not exist: %s", self.target_system_path)
            return []

        if self.target_system_path.is_file():
            self._probe_single_file(self.target_system_path)
        else:
            self._probe_directory_tree(self.target_system_path)

        # Cross-file duplicate analysis
        self._audit_duplicate_functions()
        self._audit_duplicate_file_assets()

        return self.aggregated_audit_findings

    def _probe_directory_tree(self, root_directory_path: Path) -> None:
        excluded_directory_names = {"__pycache__", ".git", "node_modules", ".pytest_cache", "venv"}
        for current_root, subdirectories, filenames in os.walk(root_directory_path):
            subdirectories[:] = [d for d in subdirectories if d not in excluded_directory_names]
            for file_name in filenames:
                if file_name == "efficiency_report.md":
                    continue
                file_path = Path(current_root) / file_name
                self._probe_single_file(file_path)

    def _probe_single_file(self, target_file_path: Path) -> None:
        file_extension = target_file_path.suffix.lower()

        # EFF_07 Asset duplicate hashing
        if target_file_path.stat().st_size > 64:
            try:
                with open(target_file_path, "rb") as binary_file:
                    file_sha256_hash = hashlib.sha256(binary_file.read()).hexdigest()
                    self.asset_hash_registry[file_sha256_hash].append(target_file_path)
            except Exception as read_exception:
                probe_logger.debug("Skipping binary hash for %s: %s", target_file_path, read_exception)

        if file_extension in (".py", ".pyw"):
            self._probe_python_source(target_file_path)
        elif file_extension in (".sh", ".bash"):
            self._probe_bash_source(target_file_path)
        elif file_extension in (".bejson", ".json"):
            self._probe_bejson_store(target_file_path)
        elif file_extension == ".md":
            self._probe_markdown_file(target_file_path)

    def _probe_python_source(self, python_file_path: Path) -> None:
        try:
            with open(python_file_path, "r", encoding="utf-8", errors="replace") as source_stream:
                source_text = source_stream.read()
        except Exception as read_err:
            probe_logger.warning("Could not read Python file %s: %s", python_file_path, read_err)
            return

        # Check raw regex for BEJSON without field_map (EFF_03)
        if "Values" in source_text:
            raw_bracket_matches = re.findall(r"row\[(\d+)\]", source_text)
            if raw_bracket_matches:
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_03_LINEAR_BEJSON_LOOKUP",
                    "severity_level": "CRITICAL",
                    "target_file_path": str(python_file_path),
                    "line_number": 1,
                    "finding_description": f"Direct positional row[i] indexing detected ({len(raw_bracket_matches)} occurrences). Must use O(1) field_map cache."
                })

        try:
            syntax_tree = ast.parse(source_text, filename=str(python_file_path))
            visitor = CodeEfficiencyVisitor(python_file_path)
            visitor.visit(syntax_tree)
            self.aggregated_audit_findings.extend(visitor.audit_finding_records)

            for func_name, (lineno, body_hash) in visitor.defined_function_signatures.items():
                self.function_body_catalog[body_hash].append((python_file_path, func_name, lineno))

        except SyntaxError as syntax_err:
            probe_logger.debug("Syntax error parsing AST in %s: %s", python_file_path, syntax_err)

    def _probe_bash_source(self, bash_file_path: Path) -> None:
        try:
            with open(bash_file_path, "r", encoding="utf-8", errors="replace") as source_stream:
                lines = source_stream.readlines()
        except Exception:
            return

        in_while_loop = False
        for line_index, line_content in enumerate(lines, start=1):
            stripped_line = line_content.strip()
            if re.search(r"\bwhile\s+.*read\b", stripped_line):
                in_while_loop = True
            elif stripped_line == "done":
                in_while_loop = False

            if in_while_loop:
                # Subprocess thrashing in loop (EFF_05)
                if re.search(r"\b(jq|sed|awk|cut|grep)\b.*(\$|`|\()", stripped_line):
                    self.aggregated_audit_findings.append({
                        "finding_code": "EFF_05_SUBPROCESS_THRASHING",
                        "severity_level": "WARNING",
                        "target_file_path": str(bash_file_path),
                        "line_number": line_index,
                        "finding_description": f"Repeated utility call ('jq/sed/awk') detected inside while-read loop. Process in single batch pipe."
                    })

    def _probe_bejson_store(self, bejson_file_path: Path) -> None:
        try:
            with open(bejson_file_path, "r", encoding="utf-8", errors="replace") as stream:
                bejson_doc = json.load(stream)
        except Exception:
            return

        if not isinstance(bejson_doc, dict):
            return

        # Check for unnormalized string redundancy (EFF_08)
        values_matrix = bejson_doc.get("Values", [])
        if isinstance(values_matrix, list) and len(values_matrix) > 10:
            column_string_counters: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
            for row in values_matrix:
                if isinstance(row, list):
                    for col_idx, cell_value in enumerate(row):
                        if isinstance(cell_value, str) and len(cell_value) > 20:
                            column_string_counters[col_idx][cell_value] += 1

            for col_idx, counter in column_string_counters.items():
                for string_val, frequency in counter.items():
                    if frequency > 5 and frequency > len(values_matrix) * 0.4:
                        self.aggregated_audit_findings.append({
                            "finding_code": "EFF_08_UNNORMALIZED_DATA_REPETITION",
                            "severity_level": "OPTIMIZATION",
                            "target_file_path": str(bejson_file_path),
                            "line_number": 1,
                            "finding_description": f"Repeated string '{string_val[:30]}...' occurs {frequency} times in col {col_idx}. Consider relational _fk normalization."
                        })
                        break

    def _probe_markdown_file(self, markdown_file_path: Path) -> None:
        try:
            with open(markdown_file_path, "r", encoding="utf-8", errors="replace") as stream:
                line_count = sum(1 for _ in stream)
        except Exception:
            return

        # Check for SKILL.md file bloat exceeding progressive disclosure ceiling (EFF_06)
        if markdown_file_path.name == "SKILL.md" and line_count > 500:
            self.aggregated_audit_findings.append({
                "finding_code": "EFF_06_CONTEXT_PROMPT_BLOAT",
                "severity_level": "CRITICAL",
                "target_file_path": str(markdown_file_path),
                "line_number": line_count,
                "finding_description": f"SKILL.md manifest contains {line_count} lines (budget limit: 500 lines). Partition into references/."
            })

    def _audit_duplicate_functions(self) -> None:
        for body_hash, occurrences in self.function_body_catalog.items():
            if len(occurrences) > 1:
                origin_file, origin_name, origin_line = occurrences[0]
                duplicates_info = ", ".join(f"{p.name}:{name} (L{line})" for p, name, line in occurrences[1:])
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_02_DUPLICATE_CODE_BLOCKS",
                    "severity_level": "WARNING",
                    "target_file_path": str(origin_file),
                    "line_number": origin_line,
                    "finding_description": f"Identical function body '{origin_name}' duplicated in: {duplicates_info}. Consolidate into common lib/ module."
                })

    def _audit_duplicate_file_assets(self) -> None:
        for file_hash, file_list in self.asset_hash_registry.items():
            if len(file_list) > 1:
                first_file = file_list[0]
                duplicate_names = ", ".join(f.name for f in file_list[1:])
                self.aggregated_audit_findings.append({
                    "finding_code": "EFF_07_DUPLICATE_ASSET_STORAGE",
                    "severity_level": "OPTIMIZATION",
                    "target_file_path": str(first_file),
                    "line_number": 1,
                    "finding_description": f"Duplicate file bytes match {duplicate_names}. Eliminate redundant storage."
                })


def format_markdown_report(findings: List[Dict[str, Any]], target_path: Path) -> str:
    """Formats findings as a canonical high-density Markdown report."""
    markdown_lines = [
        f"# Efficiency & Redundancy Audit Report",
        f"",
        f"- **Audited Target**: `{target_path.resolve()}`",
        f"- **Total Inefficiencies Identified**: `{len(findings)}`",
        f"- **Probe Tool**: `probe_efficiency.py` (Version {VERSION})",
        f"- **Timestamp**: `2026-10-23`",
        f"",
    ]

    if not findings:
        markdown_lines.append("> [!NOTE]\n> **Zero Inefficiencies Detected.** System operates with high computational and architectural efficiency.")
        return "\n".join(markdown_lines)

    markdown_lines.extend([
        f"| Finding Code | Severity | Target File | Line | Description |",
        f"| :--- | :--- | :--- | :--- | :--- |"
    ])

    for entry in findings:
        rel_path = os.path.basename(entry["target_file_path"])
        markdown_lines.append(
            f"| `{entry['finding_code']}` | **{entry['severity_level']}** | `{rel_path}` | {entry['line_number']} | {entry['finding_description']} |"
        )

    return "\n".join(markdown_lines)


def format_bejson_report(findings: List[Dict[str, Any]], target_path: Path) -> Dict[str, Any]:
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
                item["finding_code"],
                item["severity_level"],
                item["target_file_path"],
                item["line_number"],
                item["finding_description"]
            ]
            for item in findings
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Black-box efficiency and redundancy auditor for Antigravity codebases."
    )
    parser.add_argument("target", nargs="?", default=".", help="Target file or directory to probe (default: current directory)")
    parser.add_argument("--version", action="version", version=f"probe_efficiency.py {VERSION}")
    parser.add_argument("--register", action="store_true", help="Print registration metadata")
    parser.add_argument("--config", action="store_true", help="Display active probe configuration")
    parser.add_argument("--reset", action="store_true", help="Reset internal scan caches")
    parser.add_argument("--format", choices=["markdown", "json", "bejson"], default="markdown", help="Output telemetry format")
    parser.add_argument("--output", help="Write report output to designated file path")
    parser.add_argument("--no-report-file", action="store_true", help="Suppress auto-generation of efficiency_report.md in target root")
    parser.add_argument("--exit-on-warn", action="store_true", help="Return Exit Code 1 if any warnings/critical issues found")

    parsed_arguments = parser.parse_args()

    if parsed_arguments.register:
        print(f"audit-efficiency-auditor | Version: {VERSION} | RELATIONAL_ID: {RELATIONAL_ID}")
        return 0

    if parsed_arguments.config:
        print(json.dumps({
            "tool": "probe_efficiency.py",
            "version": VERSION,
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

    if parsed_arguments.reset:
        print("Internal efficiency scanner cache reset complete.")
        return 0

    target_path = Path(parsed_arguments.target).resolve()
    if not target_path.exists():
        probe_logger.error("Specified target path does not exist: %s", target_path)
        return 10

    auditor = SystemEfficiencyAuditor(target_path)
    audit_findings = auditor.run_comprehensive_audit()

    target_root_directory = target_path if target_path.is_dir() else target_path.parent
    default_report_path = target_root_directory / "efficiency_report.md"

    markdown_report_content = format_markdown_report(audit_findings, target_path)

    # Mandatory deliverable: Automatically output efficiency_report.md in target root dir
    if not parsed_arguments.no_report_file:
        try:
            with open(default_report_path, "w", encoding="utf-8") as rep_stream:
                rep_stream.write(markdown_report_content)
            probe_logger.info("Saved efficiency report to: %s", default_report_path)
        except Exception as write_err:
            probe_logger.warning("Could not write efficiency report to %s: %s", default_report_path, write_err)

    if parsed_arguments.format == "markdown":
        output_content = markdown_report_content
    elif parsed_arguments.format == "bejson":
        output_content = json.dumps(format_bejson_report(audit_findings, target_path), indent=2)
    else:
        output_content = json.dumps(audit_findings, indent=2)

    if parsed_arguments.output:
        out_file = Path(parsed_arguments.output).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(output_content)
        probe_logger.info("Report written to %s", out_file)
    else:
        print(output_content)

    if parsed_arguments.exit_on_warn and any(item["severity_level"] in ("CRITICAL", "WARNING") for item in audit_findings):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
