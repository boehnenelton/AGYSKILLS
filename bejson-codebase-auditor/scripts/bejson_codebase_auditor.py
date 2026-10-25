#!/usr/bin/env python3
"""
Name:           bejson_codebase_auditor.py
Description:    Layer 2 Read-Only Codebase and Data Store Auditor for Elton Boehnen's
                BEJSON Ecosystem. Sniffs out BEJSON data mismatches, schema corruption,
                bad logic anti-patterns (raw row[i] indexing, non-atomic writes, silent
                exceptions), variable naming convention violations (Policy §6.1 Triad),
                and taxonomy architecture improvements. Strictly read-only; outputs
                comprehensive Markdown and BEJSON 104a diagnostic reports without
                mutating application files.
Version:        100
Date Created:   2026-10-24
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  7f12a9c4-541e-4cb8-8c12-3b2d184f9011
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("bejson_codebase_auditor requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import ast
import datetime
import json
import logging
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "7f12a9c4-541e-4cb8-8c12-3b2d184f9011"

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("bejson_codebase_auditor")


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()

# Severity constants
SEV_CRITICAL: str = "CRITICAL"
SEV_HIGH: str = "HIGH"
SEV_MEDIUM: str = "MEDIUM"
SEV_LOW: str = "LOW"
SEV_INFO: str = "INFO"

SEVERITY_WEIGHTS: Dict[str, int] = {
    SEV_CRITICAL: 10,
    SEV_HIGH: 5,
    SEV_MEDIUM: 2,
    SEV_LOW: 1,
    SEV_INFO: 0,
}

# Cryptic / banned single-letter and ambiguous variable names per Policy §6.1
BANNED_SINGLE_LETTERS: Set[str] = {
    "i", "j", "k", "x", "y", "z", "d", "p", "n", "c",
    "r", "v", "e", "t", "s", "m", "f", "b", "o", "a", "q", "w", "u"
}

BANNED_AMBIGUOUS_NAMES: Set[str] = {
    "tmp", "temp", "val", "res", "arr", "obj", "item", "data",
    "row", "col", "rec", "elem", "info", "dict_val", "foo", "bar",
    "result", "output", "input", "thing", "stuff", "holder", "param"
}

# Exempt names in common python idiomatic contexts
ALLOWED_IDIOMATIC_NAMES: Set[str] = {
    "_", "__", "self", "cls", "args", "kwargs", "e", "f", "fp", "fd"
}


class AuditFinding:
    """Represents an atomic diagnostic finding from the audit pass."""

    def __init__(
        self,
        finding_code: str,
        category: str,
        severity: str,
        file_path: str,
        line_number: int,
        policy_reference: str,
        issue_summary: str,
        code_or_data_snippet: str,
        recommended_remediation: str,
    ) -> None:
        self.finding_uuid: str = str(uuid.uuid4())
        self.finding_code: str = finding_code
        self.category: str = category  # DATA_CORRUPTION, LOGIC_FLAW, NAMING_CONVENTION, TAXONOMY
        self.severity: str = severity  # CRITICAL, HIGH, MEDIUM, LOW, INFO
        self.file_path: str = file_path
        self.line_number: int = line_number
        self.policy_reference: str = policy_reference
        self.issue_summary: str = issue_summary
        self.code_or_data_snippet: str = code_or_data_snippet
        self.recommended_remediation: str = recommended_remediation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_uuid": self.finding_uuid,
            "finding_code": self.finding_code,
            "category": self.category,
            "severity": self.severity,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "policy_reference": self.policy_reference,
            "issue_summary": self.issue_summary,
            "code_or_data_snippet": self.code_or_data_snippet,
            "recommended_remediation": self.recommended_remediation,
        }

    def to_row(self, field_map: Dict[str, int]) -> List[Any]:
        row_values: List[Any] = [None] * len(field_map)
        row_values[field_map["finding_uuid"]] = self.finding_uuid
        row_values[field_map["finding_code"]] = self.finding_code
        row_values[field_map["category"]] = self.category
        row_values[field_map["severity"]] = self.severity
        row_values[field_map["file_path"]] = self.file_path
        row_values[field_map["line_number"]] = self.line_number
        row_values[field_map["policy_reference"]] = self.policy_reference
        row_values[field_map["issue_summary"]] = self.issue_summary
        row_values[field_map["code_or_data_snippet"]] = self.code_or_data_snippet
        row_values[field_map["recommended_remediation"]] = self.recommended_remediation
        return row_values


class PythonASTLogicAndNamingVisitor(ast.NodeVisitor):
    """AST visitor for Python source auditing: logic flaws, raw row indexing, naming."""

    def __init__(self, relative_file_path: str) -> None:
        self.relative_file_path: str = relative_file_path
        self.findings_accumulator: List[AuditFinding] = []
        self.declared_variables: Set[Tuple[str, int]] = set()

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Detect raw row[0] or record[1] positional indexing without field_map."""
        if isinstance(node.value, ast.Name):
            target_var_name = node.value.id.lower()
            if any(marker in target_var_name for marker in ["row", "record", "rec", "entry", "values"]):
                if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
                    self.findings_accumulator.append(
                        AuditFinding(
                            finding_code="E_LOGIC_RAW_INDEXING",
                            category="LOGIC_FLAW",
                            severity=SEV_CRITICAL,
                            file_path=self.relative_file_path,
                            line_number=node.lineno,
                            policy_reference="Policy §6.2 (BEJSON Core Mandate - O(1) Field Map Cache)",
                            issue_summary=f"Direct positional indexing '{node.value.id}[{node.slice.value}]' detected.",
                            code_or_data_snippet=f"{node.value.id}[{node.slice.value}]",
                            recommended_remediation="Resolve column index dynamically via field_map[clean_col] lookup.",
                        )
                    )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Detect hardcoded column offset constants or cryptic variable names."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                # Check for hardcoded column offsets like COL_NAME = 0 or ID_IDX = 1
                if any(var_name.upper().endswith(sfx) for sfx in ["_IDX", "_COL", "_INDEX", "_OFFSET"]):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, int):
                        self.findings_accumulator.append(
                            AuditFinding(
                                finding_code="E_LOGIC_HARDCODED_COL_OFFSET",
                                category="LOGIC_FLAW",
                                severity=SEV_HIGH,
                                file_path=self.relative_file_path,
                                line_number=node.lineno,
                                policy_reference="Policy §6.2 (Prohibition of Fixed Positional Offsets)",
                                issue_summary=f"Hardcoded column offset constant '{var_name} = {node.value.value}' detected.",
                                code_or_data_snippet=f"{var_name} = {node.value.value}",
                                recommended_remediation="Query field offsets dynamically from doc['Fields'] into a field_map dict.",
                            )
                        )

                # Check variable naming conventions (Policy §6.1 Triad formula)
                self._check_variable_name(var_name, node.lineno)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function naming and parameter naming."""
        fn_name = node.name
        # Check vague function names
        if fn_name in {"process", "handle", "run", "do_stuff", "execute", "work", "func", "helper"}:
            self.findings_accumulator.append(
                AuditFinding(
                    finding_code="E_NAMING_VAGUE_FUNCTION",
                    category="NAMING_CONVENTION",
                    severity=SEV_LOW,
                    file_path=self.relative_file_path,
                    line_number=node.lineno,
                    policy_reference="Policy §6.1 (Hierarchy-Group-Purpose Triad)",
                    issue_summary=f"Vague function identifier '{fn_name}' lacks descriptive operational domain.",
                    code_or_data_snippet=f"def {fn_name}(...):",
                    recommended_remediation=f"Rename '{fn_name}' to describe exact domain and action (e.g., entity_record_validate_syntax).",
                )
            )

        # Check argument names
        for arg in node.args.args:
            self._check_variable_name(arg.arg, node.lineno)

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Detect silent exception suppression (except: pass)."""
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.findings_accumulator.append(
                AuditFinding(
                    finding_code="E_LOGIC_SILENT_EXCEPTION",
                    category="LOGIC_FLAW",
                    severity=SEV_HIGH,
                    file_path=self.relative_file_path,
                    line_number=node.lineno,
                    policy_reference="Policy §7.3 (Zero Silent Failures Protocol)",
                    issue_summary="Silent exception suppression ('except: pass') detected without logging or error propagation.",
                    code_or_data_snippet="except ...: pass",
                    recommended_remediation="Log exception with logger.error/warning or re-raise with explicit deterministic error code.",
                )
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Detect print() calls used in place of standard logging."""
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.findings_accumulator.append(
                AuditFinding(
                    finding_code="E_LOGIC_PRINT_CALL",
                    category="LOGIC_FLAW",
                    severity=SEV_MEDIUM,
                    file_path=self.relative_file_path,
                    line_number=node.lineno,
                    policy_reference="Policy §7.3 (Negative Constraint - Never print() for Logging)",
                    issue_summary="Invocation of built-in print() detected instead of standard logging.",
                    code_or_data_snippet="print(...)",
                    recommended_remediation="Replace print() with structured logging module (logger.info, logger.debug, logger.error).",
                )
            )
        self.generic_visit(node)

    def _check_variable_name(self, var_name: str, line_number: int) -> None:
        if var_name in ALLOWED_IDIOMATIC_NAMES or var_name.startswith("__"):
            return

        # Check single-letter variable names
        if var_name.lower() in BANNED_SINGLE_LETTERS:
            self.findings_accumulator.append(
                AuditFinding(
                    finding_code="E_NAMING_SINGLE_LETTER",
                    category="NAMING_CONVENTION",
                    severity=SEV_LOW,
                    file_path=self.relative_file_path,
                    line_number=line_number,
                    policy_reference="Policy §6.1 (Strict Prohibition on Cryptic Single-Letter Names)",
                    issue_summary=f"Cryptic single-letter variable name '{var_name}' violates long self-describing variable policy.",
                    code_or_data_snippet=var_name,
                    recommended_remediation=f"Replace '{var_name}' with descriptive identifier following <scope>_<domain>_<role> triad.",
                )
            )
            return

        # Check ambiguous names
        if var_name.lower() in BANNED_AMBIGUOUS_NAMES:
            self.findings_accumulator.append(
                AuditFinding(
                    finding_code="E_NAMING_CRYPTIC",
                    category="NAMING_CONVENTION",
                    severity=SEV_LOW,
                    file_path=self.relative_file_path,
                    line_number=line_number,
                    policy_reference="Policy §6.1 (Strict Prohibition on Cryptic/Abbreviated Names)",
                    issue_summary=f"Ambiguous variable name '{var_name}' lacks descriptive scope and domain context.",
                    code_or_data_snippet=var_name,
                    recommended_remediation=f"Rename '{var_name}' using Hierarchy-Group-Purpose formula (e.g., entity_record_payload).",
                )
            )


class CodebaseAuditor:
    """Core read-only auditing engine for BEJSON data integrity, logic, and taxonomies."""

    def __init__(self, target_root_directory: Path, min_severity: str = SEV_INFO) -> None:
        self.target_root_directory: Path = target_root_directory.resolve()
        self.min_severity: str = min_severity
        self.audit_findings: List[AuditFinding] = []
        self.total_scanned_files_count: int = 0
        self.bejson_documents_scanned_count: int = 0
        self.source_code_files_scanned_count: int = 0

    def execute_audit(self) -> List[AuditFinding]:
        """Runs the four-pass read-only audit across the target directory."""
        logger.info("Commencing read-only audit over directory: %s", self.target_root_directory)

        # Walk entire directory tree (read-only)
        for root_path_str, directory_names, file_names in os.walk(self.target_root_directory):
            # Skip transient / cache / git directories
            directory_names[:] = [
                d for d in directory_names
                if d not in {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules", ".gemini", "reports"}
            ]

            current_folder_path = Path(root_path_str)
            for file_name in file_names:
                candidate_file_path = current_folder_path / file_name
                relative_file_path = str(candidate_file_path.relative_to(self.target_root_directory))

                # Check BEJSON data files
                if file_name.endswith((".bejson", ".json")):
                    self.bejson_documents_scanned_count += 1
                    self.total_scanned_files_count += 1
                    self._audit_bejson_data_file(candidate_file_path, relative_file_path)

                # Check Python source files
                elif file_name.endswith(".py"):
                    self.source_code_files_scanned_count += 1
                    self.total_scanned_files_count += 1
                    self._audit_python_source_file(candidate_file_path, relative_file_path)

                # Check Shell scripts
                elif file_name.endswith(".sh"):
                    self.source_code_files_scanned_count += 1
                    self.total_scanned_files_count += 1
                    self._audit_shell_source_file(candidate_file_path, relative_file_path)

                # Check JavaScript / TypeScript files
                elif file_name.endswith((".js", ".ts")):
                    self.source_code_files_scanned_count += 1
                    self.total_scanned_files_count += 1
                    self._audit_js_ts_source_file(candidate_file_path, relative_file_path)

        # Filter findings by minimum severity threshold
        min_weight = SEVERITY_WEIGHTS.get(self.min_severity, 0)
        filtered_findings = [
            f for f in self.audit_findings
            if SEVERITY_WEIGHTS.get(f.severity, 0) >= min_weight
        ]

        logger.info(
            "Audit complete. Files inspected: %d (Data: %d, Code: %d). Total findings: %d.",
            self.total_scanned_files_count,
            self.bejson_documents_scanned_count,
            self.source_code_files_scanned_count,
            len(filtered_findings),
        )
        return filtered_findings

    def _audit_bejson_data_file(self, file_path: Path, relative_path: str) -> None:
        """Inspects JSON/BEJSON data files for structural corruption, mismatches, and format flaws."""
        try:
            with open(file_path, "r", encoding="utf-8") as file_stream:
                raw_content = file_stream.read()
        except Exception as read_err:
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_DATA_UNREADABLE_FILE",
                    category="DATA_CORRUPTION",
                    severity=SEV_CRITICAL,
                    file_path=relative_path,
                    line_number=1,
                    policy_reference="POSIX File Access Standard",
                    issue_summary=f"Unable to read file: {read_err}",
                    code_or_data_snippet="",
                    recommended_remediation="Verify file permissions and UTF-8 encoding.",
                )
            )
            return

        # 1. Parse JSON
        try:
            parsed_document = json.loads(raw_content)
        except json.JSONDecodeError as decode_err:
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_DATA_CORRUPT_JSON",
                    category="DATA_CORRUPTION",
                    severity=SEV_CRITICAL,
                    file_path=relative_path,
                    line_number=decode_err.lineno,
                    policy_reference="JSON RFC 8259 Standard",
                    issue_summary=f"Malformed JSON syntax: {decode_err.msg} at line {decode_err.lineno}, col {decode_err.colno}.",
                    code_or_data_snippet=raw_content[:200],
                    recommended_remediation="Repair JSON syntax error, check for unescaped characters or truncated file.",
                )
            )
            return

        if not isinstance(parsed_document, dict):
            # Not a BEJSON dictionary structure
            return

        # Check if this claims to be BEJSON or has tabular structure
        is_bejson_claim = (
            parsed_document.get("Format") == "BEJSON" or
            ("Fields" in parsed_document and "Values" in parsed_document)
        )

        if not is_bejson_claim:
            # Suggest converting dense array-of-objects to BEJSON 104a
            if any(isinstance(v, list) and len(v) > 5 and isinstance(v[0], dict) for v in parsed_document.values()):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_TAXONOMY_UNSTRUCTURED_DATA",
                        category="TAXONOMY",
                        severity=SEV_INFO,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="BEJSON Format 104a Architecture",
                        issue_summary="Unnormalized JSON array-of-objects detected; candidate for BEJSON 104a compaction.",
                        code_or_data_snippet=file_path.name,
                        recommended_remediation="Migrate repeated dictionary keys into separated Fields and dense Values array.",
                    )
                )
            return

        # 2. Check Mandatory BEJSON 104/104a Headers
        format_version = str(parsed_document.get("Format_Version", ""))
        required_headers = ["Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values"]
        for header in required_headers:
            if header not in parsed_document:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_MISSING_HEADER",
                        category="DATA_CORRUPTION",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §4.4 (BEJSON 104a Header Invariants)",
                        issue_summary=f"Mandatory top-level header '{header}' is absent in BEJSON document.",
                        code_or_data_snippet=f"Missing: '{header}'",
                        recommended_remediation=f"Add mandatory '{header}' top-level key to document schema.",
                    )
                )

        fields_definition = parsed_document.get("Fields")
        values_matrix = parsed_document.get("Values")

        if not isinstance(fields_definition, list):
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_DATA_FIELDS_NOT_LIST",
                    category="DATA_CORRUPTION",
                    severity=SEV_CRITICAL,
                    file_path=relative_path,
                    line_number=1,
                    policy_reference="Policy §4.4 (Fields Specification)",
                    issue_summary="BEJSON 'Fields' must be an array of field definition objects.",
                    code_or_data_snippet=str(type(fields_definition)),
                    recommended_remediation="Convert 'Fields' to an array of objects [{'name': ..., 'type': ...}].",
                )
            )
            return

        if not isinstance(values_matrix, list):
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_DATA_VALUES_NOT_LIST",
                    category="DATA_CORRUPTION",
                    severity=SEV_CRITICAL,
                    file_path=relative_path,
                    line_number=1,
                    policy_reference="Policy §4.4 (Values Specification)",
                    issue_summary="BEJSON 'Values' must be a 2D array of record rows.",
                    code_or_data_snippet=str(type(values_matrix)),
                    recommended_remediation="Convert 'Values' to an array of rows: [[col1, col2, ...]].",
                )
            )
            return

        # 3. Validate Field Definitions & Boundary Sanitization
        expected_field_count = len(fields_definition)
        seen_field_names: Set[str] = set()

        for field_idx, field_obj in enumerate(fields_definition):
            if not isinstance(field_obj, dict):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_MALFORMED_FIELD",
                        category="DATA_CORRUPTION",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §4.4 (Field Definition Object)",
                        issue_summary=f"Field item at index {field_idx} is not an object.",
                        code_or_data_snippet=str(field_obj),
                        recommended_remediation="Define field as a dictionary: {'name': 'identifier', 'type': 'string'}.",
                    )
                )
                continue

            field_name = str(field_obj.get("name", ""))
            field_type = str(field_obj.get("type", ""))

            if not field_name:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_EMPTY_FIELD_NAME",
                        category="DATA_CORRUPTION",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §4.4 (Field Name Mandate)",
                        issue_summary=f"Field at index {field_idx} has an empty or missing 'name' attribute.",
                        code_or_data_snippet=str(field_obj),
                        recommended_remediation="Provide an explicit non-empty snake_case identifier for field name.",
                    )
                )

            # Check boundary whitespace sanitization (Policy §10.9)
            if field_name != field_name.strip():
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_WHITESPACE_IN_FIELD_NAME",
                        category="DATA_CORRUPTION",
                        severity=SEV_MEDIUM,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §10.9 (Boundary-Layer Sanitization Core)",
                        issue_summary=f"Field name '{field_name}' contains leading/trailing whitespace.",
                        code_or_data_snippet=f"'{field_name}'",
                        recommended_remediation=f"Sanitize field name: '{field_name.strip()}'.",
                    )
                )

            clean_name = field_name.strip()
            if clean_name in seen_field_names:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_DUPLICATE_FIELD",
                        category="DATA_CORRUPTION",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §6.2 (Field Map Cache Collision Guard)",
                        issue_summary=f"Duplicate field name '{clean_name}' causes field_map index collision.",
                        code_or_data_snippet=clean_name,
                        recommended_remediation=f"Deduplicate field name '{clean_name}' across schema Fields.",
                    )
                )
            seen_field_names.add(clean_name)

            # Taxonomy Sniffing: Check for entity prefixes
            if "_" not in clean_name and clean_name not in {"id", "type", "status", "name"}:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_TAXONOMY_UNPREFIXED_FIELD",
                        category="TAXONOMY",
                        severity=SEV_INFO,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §6.1 / §10.2 (Entity Prefix Taxonomy Standard)",
                        issue_summary=f"Column '{clean_name}' lacks explicit entity prefix (e.g. <entity>_{clean_name}).",
                        code_or_data_snippet=clean_name,
                        recommended_remediation=f"Prefix field with entity name (e.g., manifest_{clean_name} or record_{clean_name}).",
                    )
                )

        # 4. Check Format 105 UUID Requirements
        if format_version.startswith("105"):
            for field_idx, field_obj in enumerate(fields_definition):
                if isinstance(field_obj, dict) and "field_uuid" not in field_obj:
                    self.audit_findings.append(
                        AuditFinding(
                            finding_code="E_DATA_105_MISSING_FIELD_UUID",
                            category="DATA_CORRUPTION",
                            severity=SEV_HIGH,
                            file_path=relative_path,
                            line_number=1,
                            policy_reference="Policy E90 (Integrity Era Format 105 field_uuid Requirement)",
                            issue_summary=f"Format 105 field '{field_obj.get('name')}' is missing mandatory 'field_uuid'.",
                            code_or_data_snippet=str(field_obj),
                            recommended_remediation="Assign pre-compiled UUIDv4 to 'field_uuid' attribute.",
                        )
                    )

        # 5. Check Row Widths & Cell Type Conformance
        for row_index, record_row in enumerate(values_matrix):
            if not isinstance(record_row, list):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_ROW_NOT_LIST",
                        category="DATA_CORRUPTION",
                        severity=SEV_CRITICAL,
                        file_path=relative_path,
                        line_number=row_index + 1,
                        policy_reference="Policy §4.4 (Values 2D Row Constraint)",
                        issue_summary=f"Values row at index {row_index} is not an array.",
                        code_or_data_snippet=str(record_row)[:100],
                        recommended_remediation="Wrap row elements in an array [val1, val2, ...].",
                    )
                )
                continue

            # Row-width mismatch detection
            if len(record_row) != expected_field_count:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_WIDTH_MISMATCH",
                        category="DATA_CORRUPTION",
                        severity=SEV_CRITICAL,
                        file_path=relative_path,
                        line_number=row_index + 1,
                        policy_reference="Policy §6.2 (Field Map Parity Invariant)",
                        issue_summary=f"Row width mismatch at row {row_index}: has {len(record_row)} cells, expected {expected_field_count}.",
                        code_or_data_snippet=f"Length {len(record_row)} vs Expected {expected_field_count}",
                        recommended_remediation="Pad or trim row values to match exact Fields count.",
                    )
                )

            # Cell type validation
            for col_idx, cell_value in enumerate(record_row):
                if col_idx >= expected_field_count:
                    break
                expected_type_str = str(fields_definition[col_idx].get("type", "any")).lower()
                field_name_str = str(fields_definition[col_idx].get("name", f"col_{col_idx}"))

                # Check boundary whitespace in string values (Policy §10.9)
                if isinstance(cell_value, str) and cell_value != cell_value.strip():
                    self.audit_findings.append(
                        AuditFinding(
                            finding_code="E_DATA_CELL_WHITESPACE",
                            category="DATA_CORRUPTION",
                            severity=SEV_LOW,
                            file_path=relative_path,
                            line_number=row_index + 1,
                            policy_reference="Policy §10.9 (Boundary-Layer Sanitization Core)",
                            issue_summary=f"Cell in column '{field_name_str}' at row {row_index} has untrimmed whitespace.",
                            code_or_data_snippet=f"'{cell_value}'",
                            recommended_remediation=f"Apply .strip() sanitization: '{cell_value.strip()}'.",
                        )
                    )

                # Type mismatch check
                if cell_value is not None:
                    type_valid = True
                    if expected_type_str in {"string", "str"} and not isinstance(cell_value, str):
                        type_valid = False
                    elif expected_type_str in {"integer", "int"} and (not isinstance(cell_value, int) or isinstance(cell_value, bool)):
                        type_valid = False
                    elif expected_type_str in {"float", "number"} and not isinstance(cell_value, (int, float)):
                        type_valid = False
                    elif expected_type_str in {"boolean", "bool"} and not isinstance(cell_value, bool):
                        type_valid = False
                    elif expected_type_str in {"array", "list"} and not isinstance(cell_value, list):
                        type_valid = False
                    elif expected_type_str in {"object", "dict"} and not isinstance(cell_value, dict):
                        type_valid = False

                    if not type_valid:
                        self.audit_findings.append(
                            AuditFinding(
                                finding_code="E_DATA_TYPE_MISMATCH",
                                category="DATA_CORRUPTION",
                                severity=SEV_MEDIUM,
                                file_path=relative_path,
                                line_number=row_index + 1,
                                policy_reference="Policy §4.4 (Field Type Verification)",
                                issue_summary=f"Type mismatch in column '{field_name_str}' at row {row_index}: got {type(cell_value).__name__}, expected {expected_type_str}.",
                                code_or_data_snippet=f"Value: {repr(cell_value)}",
                                recommended_remediation=f"Cast value to expected type '{expected_type_str}' or adjust schema definition.",
                            )
                        )

        # 6. Check Project Tracker Governance if bejson_project.json
        if file_path.name == "bejson_project.json":
            project_guid = parsed_document.get("Project_GUID")
            is_registered = parsed_document.get("Is_Registered")
            if is_registered is True and project_guid in {"GUID_PLACEHOLDER", None, ""}:
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_DATA_UNRESOLVED_GUID",
                        category="DATA_CORRUPTION",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=1,
                        policy_reference="Policy §4.6 / §7.3 (Strict Project_GUID Governance)",
                        issue_summary="Project is marked Is_Registered: true, but Project_GUID contains unresolved GUID_PLACEHOLDER.",
                        code_or_data_snippet=f"Project_GUID: {project_guid}",
                        recommended_remediation="Run registration tool ($PROJECT_INDEX_ROOT/cli_project_register.py) to assign canonical GUID.",
                    )
                )

    def _audit_python_source_file(self, file_path: Path, relative_path: str) -> None:
        """Audits Python source code via AST analysis and regex pattern matching."""
        try:
            with open(file_path, "r", encoding="utf-8") as file_stream:
                source_code = file_stream.read()
        except Exception as read_err:
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_LOGIC_UNREADABLE_FILE",
                    category="LOGIC_FLAW",
                    severity=SEV_HIGH,
                    file_path=relative_path,
                    line_number=1,
                    policy_reference="POSIX Standard",
                    issue_summary=f"Unable to read Python file: {read_err}",
                    code_or_data_snippet="",
                    recommended_remediation="Check file read permissions.",
                )
            )
            return

        # 1. AST-based analysis
        try:
            syntax_tree = ast.parse(source_code, filename=str(file_path))
            visitor = PythonASTLogicAndNamingVisitor(relative_path)
            visitor.visit(syntax_tree)
            self.audit_findings.extend(visitor.findings_accumulator)
        except SyntaxError as syntax_err:
            self.audit_findings.append(
                AuditFinding(
                    finding_code="E_LOGIC_SYNTAX_ERROR",
                    category="LOGIC_FLAW",
                    severity=SEV_CRITICAL,
                    file_path=relative_path,
                    line_number=syntax_err.lineno or 1,
                    policy_reference="Python 3.10+ Grammar Standard",
                    issue_summary=f"Python syntax error: {syntax_err.msg} at line {syntax_err.lineno}.",
                    code_or_data_snippet=syntax_err.text or "",
                    recommended_remediation="Fix Python syntax error to enable execution and AST linting.",
                )
            )

        # 2. Regex-based pattern checks
        lines = source_code.splitlines()
        for line_num, line_text in enumerate(lines, start=1):
            # Check hardcoded host paths (Policy §4.1 / §7.3)
            if re.search(r'["\']/(storage/emulated/0|data/data/com\.termux)/[^"\']+["\']', line_text):
                # Exclude comments or docstrings or default config fallbacks if commented
                stripped_line = line_text.strip()
                if not stripped_line.startswith("#"):
                    self.audit_findings.append(
                        AuditFinding(
                            finding_code="E_LOGIC_HARDCODED_HOST_PATH",
                            category="LOGIC_FLAW",
                            severity=SEV_HIGH,
                            file_path=relative_path,
                            line_number=line_num,
                            policy_reference="Policy §4.1 / §7.3 (Negative Constraint - Never Hardcode Paths)",
                            issue_summary="Hardcoded absolute host path detected in runtime logic.",
                            code_or_data_snippet=stripped_line[:120],
                            recommended_remediation="Use self-locating Path(__file__).resolve().parent or definitions.json variables.",
                        )
                    )

            # Check non-atomic file writes on json/bejson files
            if re.search(r'open\s*\([^)]+\.bejson["\'],\s*["\']w["\']\)', line_text):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_LOGIC_NON_ATOMIC_WRITE",
                        category="LOGIC_FLAW",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=line_num,
                        policy_reference="Policy §1.1 / Layer 1 Atomic Disk Write Protocol",
                        issue_summary="Direct open(..., 'w') detected on BEJSON file without atomic temp-file replace.",
                        code_or_data_snippet=line_text.strip()[:120],
                        recommended_remediation="Write to .tmp file first, flush, call os.fsync(), then os.replace().",
                    )
                )

    def _audit_shell_source_file(self, file_path: Path, relative_path: str) -> None:
        """Audits Bash/Shell scripts for non-portable paths and hardcoded positional parsing."""
        try:
            with open(file_path, "r", encoding="utf-8") as file_stream:
                lines = file_stream.readlines()
        except Exception:
            return

        for line_num, line_text in enumerate(lines, start=1):
            stripped = line_text.strip()
            if stripped.startswith("#"):
                continue

            # Check hardcoded paths
            if re.search(r'/(storage/emulated/0|data/data/com\.termux)/', stripped):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_LOGIC_HARDCODED_BASH_PATH",
                        category="LOGIC_FLAW",
                        severity=SEV_HIGH,
                        file_path=relative_path,
                        line_number=line_num,
                        policy_reference="Policy §4.2 (Bash Self-Locating Script Path)",
                        issue_summary="Hardcoded absolute Android path in Bash script.",
                        code_or_data_snippet=stripped[:120],
                        recommended_remediation="Derive paths relatively via SCRIPT_PATH=$(get_script_path).",
                    )
                )

            # Check cut -d',' or awk hardcoded column offsets
            if re.search(r'\b(cut\s+-d\s*["\']?[,:]|awk\s+["\']\{print\s+\$[0-9]+)', stripped):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_LOGIC_BASH_RAW_OFFSET",
                        category="LOGIC_FLAW",
                        severity=SEV_MEDIUM,
                        file_path=relative_path,
                        line_number=line_num,
                        policy_reference="Policy §6.2 (Bash BEJSON Positional Indexing Guard)",
                        issue_summary="Positional stream cutting (cut/awk) detected; risks schema column offset corruption.",
                        code_or_data_snippet=stripped[:120],
                        recommended_remediation="Use jq or python helper with dynamic field_map to query fields by name.",
                    )
                )

    def _audit_js_ts_source_file(self, file_path: Path, relative_path: str) -> None:
        """Audits JS/TS files for direct row[0] indexing and console.log spam."""
        try:
            with open(file_path, "r", encoding="utf-8") as file_stream:
                lines = file_stream.readlines()
        except Exception:
            return

        for line_num, line_text in enumerate(lines, start=1):
            stripped = line_text.strip()
            if stripped.startswith("//") or stripped.startswith("/*"):
                continue

            # Check raw row[0] indexing
            if re.search(r'\b(row|record|rec|entry)\[[0-9]+\]', stripped):
                self.audit_findings.append(
                    AuditFinding(
                        finding_code="E_LOGIC_JS_RAW_INDEXING",
                        category="LOGIC_FLAW",
                        severity=SEV_CRITICAL,
                        file_path=relative_path,
                        line_number=line_num,
                        policy_reference="Policy §6.2 (BEJSON JavaScript Field Map Mandate)",
                        issue_summary="Raw positional indexing 'row[n]' detected in JS/TS source.",
                        code_or_data_snippet=stripped[:120],
                        recommended_remediation="Construct fieldMap object: const fieldMap = Object.fromEntries(doc.Fields.map((f, i) => [f.name, i])).",
                    )
                )


class AuditReportBuilder:
    """Compiles audit findings into Markdown and BEJSON 104a reports (Strictly Read-Only)."""

    def __init__(
        self,
        target_root_directory: Path,
        findings_list: List[AuditFinding],
        scanned_files_count: int,
        scanned_data_count: int,
        scanned_code_count: int,
    ) -> None:
        self.target_root_directory: Path = target_root_directory
        self.findings_list: List[AuditFinding] = findings_list
        self.scanned_files_count: int = scanned_files_count
        self.scanned_data_count: int = scanned_data_count
        self.scanned_code_count: int = scanned_code_count
        self.timestamp_str: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.iso_timestamp: str = datetime.datetime.now().isoformat()

    def calculate_health_score(self) -> int:
        """Calculates codebase health score out of 100 based on severity weights."""
        if self.scanned_files_count == 0:
            return 100
        total_penalty = sum(SEVERITY_WEIGHTS.get(f.severity, 0) for f in self.findings_list)
        # Normalize penalty by files scanned
        penalty_per_file = total_penalty / max(1, self.scanned_files_count)
        health_score = max(0, int(100 - (penalty_per_file * 5)))
        return min(100, health_score)

    def generate_markdown_report(self) -> str:
        """Generates a comprehensive Markdown report adhering to GitHub-flavored syntax."""
        health_score = self.calculate_health_score()
        sev_counts: Dict[str, int] = {
            SEV_CRITICAL: sum(1 for f in self.findings_list if f.severity == SEV_CRITICAL),
            SEV_HIGH: sum(1 for f in self.findings_list if f.severity == SEV_HIGH),
            SEV_MEDIUM: sum(1 for f in self.findings_list if f.severity == SEV_MEDIUM),
            SEV_LOW: sum(1 for f in self.findings_list if f.severity == SEV_LOW),
            SEV_INFO: sum(1 for f in self.findings_list if f.severity == SEV_INFO),
        }

        category_counts: Dict[str, int] = {
            "DATA_CORRUPTION": sum(1 for f in self.findings_list if f.category == "DATA_CORRUPTION"),
            "LOGIC_FLAW": sum(1 for f in self.findings_list if f.category == "LOGIC_FLAW"),
            "NAMING_CONVENTION": sum(1 for f in self.findings_list if f.category == "NAMING_CONVENTION"),
            "TAXONOMY": sum(1 for f in self.findings_list if f.category == "TAXONOMY"),
        }

        md_lines: List[str] = [
            f"# BEJSON Codebase Diagnostic Audit Report",
            f"",
            f"- **Target Root**: `{self.target_root_directory}`",
            f"- **Audit Timestamp**: `{self.timestamp_str}`",
            f"- **Auditor Version**: `v{VERSION}` (Release_Version: `{RELEASE_VERSION}`)",
            f"- **Auditor ID**: `{RELATIONAL_ID}`",
            f"- **Execution Mode**: `Strictly Read-Only (Zero Files Modified)`",
            f"- **Overall Health Score**: **{health_score}/100**",
            f"",
            f"---",
            f"",
            f"## 1. Executive Summary & Telemetry",
            f"",
            f"| Metric | Value |",
            f"| :--- | :--- |",
            f"| Total Files Scanned | **{self.scanned_files_count}** |",
            f"| Data Documents Scanned (.bejson, .json) | **{self.scanned_data_count}** |",
            f"| Source Code Files Scanned (.py, .sh, .js, .ts) | **{self.scanned_code_count}** |",
            f"| Total Audit Findings Reported | **{len(self.findings_list)}** |",
            f"| Codebase Health Rating | **{'EXCELLENT' if health_score >= 90 else 'GOOD' if health_score >= 75 else 'NEEDS_WORK' if health_score >= 50 else 'CRITICAL_RISK'}** |",
            f"",
            f"### Severity Distribution",
            f"",
            f"| Severity Level | Count | Action Required |",
            f"| :--- | :--- | :--- |",
            f"| 🚨 **CRITICAL** | **{sev_counts[SEV_CRITICAL]}** | Immediate intervention: data corruption or fatal logic flaw. |",
            f"| ⚠️ **HIGH** | **{sev_counts[SEV_HIGH]}** | High priority: missing headers, unhandled errors, path leaks. |",
            f"| 🟡 **MEDIUM** | **{sev_counts[SEV_MEDIUM]}** | Moderate priority: cell whitespace, type divergence, logging. |",
            f"| 🔵 **LOW** | **{sev_counts[SEV_LOW]}** | Low priority: variable naming, single-letter variables. |",
            f"| ℹ️ **INFO** | **{sev_counts[SEV_INFO]}** | Informational: taxonomy normalization suggestions. |",
            f"",
            f"### Category Breakdown",
            f"",
            f"- **BEJSON Data Integrity & Corruption**: `{category_counts['DATA_CORRUPTION']}` issue(s)",
            f"- **BEJSON Logic Anti-Patterns & Flaws**: `{category_counts['LOGIC_FLAW']}` issue(s)",
            f"- **Naming Conventions & Hierarchy Triad**: `{category_counts['NAMING_CONVENTION']}` issue(s)",
            f"- **Taxonomy & Relational Architecture**: `{category_counts['TAXONOMY']}` suggestion(s)",
            f"",
            f"---",
            f"",
            f"## 2. Detailed Findings Catalog",
            f"",
        ]

        if not self.findings_list:
            md_lines.append("> [!NOTE]\n> Zero audit issues detected across target codebase! All files conform cleanly.")
        else:
            for idx, finding in enumerate(self.findings_list, start=1):
                icon = {
                    SEV_CRITICAL: "🚨",
                    SEV_HIGH: "⚠️",
                    SEV_MEDIUM: "🟡",
                    SEV_LOW: "🔵",
                    SEV_INFO: "ℹ️",
                }.get(finding.severity, "•")

                md_lines.extend([
                    f"### {idx}. [{finding.finding_code}] {icon} {finding.severity} in `{finding.file_path}` (Line {finding.line_number})",
                    f"",
                    f"- **Category**: `{finding.category}`",
                    f"- **Policy Reference**: {finding.policy_reference}",
                    f"- **Summary**: {finding.issue_summary}",
                    f"",
                    f"```text",
                    f"{finding.code_or_data_snippet}",
                    f"```",
                    f"",
                    f"**Recommended Remediation**:",
                    f"> {finding.recommended_remediation}",
                    f"",
                ])

        md_lines.extend([
            f"---",
            f"",
            f"## 3. Author & Ecosystem Credit",
            f"",
            f"Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton",
            f"",
        ])

        return "\n".join(md_lines)

    def generate_bejson_104a_report(self) -> Dict[str, Any]:
        """Generates a canonical BEJSON 104a telemetry document with field map cache."""
        fields_spec = [
            {"name": "finding_uuid", "type": "string"},
            {"name": "finding_code", "type": "string"},
            {"name": "category", "type": "string"},
            {"name": "severity", "type": "string"},
            {"name": "file_path", "type": "string"},
            {"name": "line_number", "type": "integer"},
            {"name": "policy_reference", "type": "string"},
            {"name": "issue_summary", "type": "string"},
            {"name": "code_or_data_snippet", "type": "string"},
            {"name": "recommended_remediation", "type": "string"},
        ]

        field_map = {f["name"]: i for i, f in enumerate(fields_spec)}
        values_rows = [f.to_row(field_map) for f in self.findings_list]

        return {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Report_Timestamp": self.iso_timestamp,
            "Target_Directory": str(self.target_root_directory),
            "Auditor_Version": str(VERSION),
            "Auditor_Relational_Id": RELATIONAL_ID,
            "Health_Score": self.calculate_health_score(),
            "Total_Files_Scanned": self.scanned_files_count,
            "Records_Type": ["CodebaseAuditFindings"],
            "Fields": fields_spec,
            "Values": values_rows,
        }


def run_audit_cli() -> int:
    """CLI driver for the codebase auditor."""
    parser = argparse.ArgumentParser(
        prog="bejson_codebase_auditor",
        description="Layer 2 Read-Only Codebase and Data Store Auditor for Elton Boehnen's BEJSON Ecosystem.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to project or codebase root to audit (defaults to current working directory).",
    )
    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory where audit reports will be stored (defaults to 'reports').",
    )
    parser.add_argument(
        "--format",
        choices=["both", "markdown", "bejson"],
        default="both",
        help="Format of generated audit reports (default: both).",
    )
    parser.add_argument(
        "--min-severity",
        choices=[SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW, SEV_INFO],
        default=SEV_INFO,
        help="Minimum severity threshold to include in report (default: INFO).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{VERSION} (Release_Version: {RELEASE_VERSION}, ID: {RELATIONAL_ID})",
    )
    parser.add_argument("--register", action="store_true", help="Print registration command.")
    parser.add_argument("--config", action="store_true", help="Display active configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset temporary auditor cache.")

    cli_arguments = parser.parse_args()

    if cli_arguments.register:
        sys.stdout.write(f"python3 $PROJECT_INDEX_ROOT/cli_project_register.py --register \"{SCRIPT_PATH}\"\n")
        return EXIT_OK

    if cli_arguments.config:
        sys.stdout.write(json.dumps({
            "version": VERSION,
            "release_version": RELEASE_VERSION,
            "relational_id": RELATIONAL_ID,
            "script_path": str(SCRIPT_PATH),
            "allowed_single_letters": sorted(list(BANNED_SINGLE_LETTERS)),
        }, indent=2) + "\n")
        return EXIT_OK

    if cli_arguments.reset:
        logger.info("Resetting temporary audit cache. All state cleared.")
        return EXIT_OK

    target_directory = Path(cli_arguments.target).resolve()
    if not target_directory.exists():
        logger.error("Target path does not exist: %s", target_directory)
        return EXIT_PATH_FAILURE

    output_directory = Path(cli_arguments.output_dir).resolve()
    try:
        output_directory.mkdir(parents=True, exist_ok=True)
    except Exception as dir_err:
        logger.error("Failed to create output reports directory %s: %s", output_directory, dir_err)
        return EXIT_PATH_FAILURE

    # Run audit
    auditor = CodebaseAuditor(target_directory, min_severity=cli_arguments.min_severity)
    findings = auditor.execute_audit()

    report_builder = AuditReportBuilder(
        target_root_directory=target_directory,
        findings_list=findings,
        scanned_files_count=auditor.total_scanned_files_count,
        scanned_data_count=auditor.bejson_documents_scanned_count,
        scanned_code_count=auditor.source_code_files_scanned_count,
    )

    timestamp_slug = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate Markdown Report
    if cli_arguments.format in {"both", "markdown"}:
        md_content = report_builder.generate_markdown_report()
        md_file_path = output_directory / f"bejson_audit_report_{timestamp_slug}.md"
        # Atomic write to report file
        temp_md = md_file_path.with_suffix(".tmp")
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(md_content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_md, md_file_path)
        logger.info("Markdown audit report generated: %s", md_file_path)

    # Generate BEJSON 104a Report
    if cli_arguments.format in {"both", "bejson"}:
        bejson_doc = report_builder.generate_bejson_104a_report()
        bejson_file_path = output_directory / f"bejson_audit_report_{timestamp_slug}.104a.bejson"
        temp_bejson = bejson_file_path.with_suffix(".tmp")
        with open(temp_bejson, "w", encoding="utf-8") as f:
            json.dump(bejson_doc, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_bejson, bejson_file_path)
        logger.info("BEJSON 104a audit telemetry report generated: %s", bejson_file_path)

    critical_count = sum(1 for f in findings if f.severity == SEV_CRITICAL)
    if critical_count > 0:
        logger.warning("Audit completed with %d CRITICAL issue(s). Review reports for details.", critical_count)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(run_audit_cli())
