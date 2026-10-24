#!/usr/bin/env python3
"""
File_Name:          verify_variable_naming.py
Description:        Audits Python source files for compliance with the Long Self-Describing Variable Standard (Policy §6.1).
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      5d1a8e2b-4c3f-47a9-9e0d-1b2c3a4f5e6d
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
from pathlib import Path
import sys
from typing import Any, Dict, List

VERSION = "100"
RELEASE_VERSION = "300"
RELATIONAL_ID = "5d1a8e2b-4c3f-47a9-9e0d-1b2c3a4f5e6d"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("verify_variable_naming")

PROHIBITED_STANDALONE_NAMES = {
    "a", "b", "c", "d", "e", "f", "p", "r", "s", "t", "v", "w", "x", "y", "z",
    "tmp", "temp", "val", "value", "res", "result", "arr", "array", "obj", "object",
    "data", "rec", "col", "item",
}

PERMITTED_SHORT_INDEX_NAMES = {"i", "j", "k", "idx", "row_idx", "col_idx", "_"}


class VariableNamingAuditor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations: List[Dict[str, Any]] = []

    def check_identifier(self, name: str, line_num: int, context_type: str) -> None:
        name_lower = name.lower()
        if name_lower in PROHIBITED_STANDALONE_NAMES:
            self.violations.append({
                "file": self.filename,
                "line": line_num,
                "variable": name,
                "context": context_type,
                "error": f"Prohibited cryptic variable '{name}'. Use long self-describing HGP name (Policy §6.1).",
            })

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.check_identifier(target.id, node.lineno, "assignment")
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.check_identifier(elt.id, node.lineno, "tuple_unpacking")
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            self.check_identifier(node.target.id, node.lineno, "annotated_assignment")
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        if isinstance(node.target, ast.Name):
            if node.target.id not in PERMITTED_SHORT_INDEX_NAMES:
                self.check_identifier(node.target.id, node.lineno, "for_loop_target")
        elif isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name) and elt.id not in PERMITTED_SHORT_INDEX_NAMES:
                    self.check_identifier(elt.id, node.lineno, "for_loop_tuple_target")
        self.generic_visit(node)


def audit_file(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        LOG.error("File not found: %s", file_path)
        sys.exit(20)

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code, filename=str(file_path))
    except Exception as exc:
        LOG.error("Failed to parse AST for %s: %s", file_path, exc)
        sys.exit(30)

    auditor = VariableNamingAuditor(str(file_path))
    auditor.visit(tree)
    return auditor.violations


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="verify_variable_naming",
        description="Audits Python files for Long Self-Describing Variable Standard compliance (Policy §6.1).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Register script with master index.")
    parser.add_argument("--config", action="store_true", help="Display script configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset state.")
    parser.add_argument("target", nargs="?", type=Path, help="Path to Python file to audit.")

    args = parser.parse_args()

    if args.register:
        LOG.info("Registered verify_variable_naming v%s (%s)", VERSION, RELATIONAL_ID)
        return 0

    if args.config:
        cfg = {
            "version": VERSION,
            "release_version": RELEASE_VERSION,
            "author": "Elton Boehnen",
            "prohibited_names": sorted(PROHIBITED_STANDALONE_NAMES),
        }
        sys.stdout.write(json.dumps(cfg, indent=2) + "\n")
        return 0

    if args.reset:
        LOG.info("Reset state complete.")
        return 0

    if not args.target:
        parser.print_help()
        return 10

    violations = audit_file(args.target)
    audit_execution_result_payload = {
        "valid": len(violations) == 0,
        "file": str(args.target),
        "violation_count": len(violations),
        "violations": violations,
    }
    sys.stdout.write(json.dumps(audit_execution_result_payload, indent=2) + "\n")

    if violations:
        LOG.warning("Variable naming audit flagged %d violations.", len(violations))
        return 10

    LOG.info("Variable naming audit PASSED (0 violations).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
