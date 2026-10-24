#!/usr/bin/env python3
"""
File_Name:          definitions_lookup.py
Description:        CLI and query engine for ecosystem terminology, inline definitions, and semantic aliases.
Version:            100
Release_Version:    300
Date_Created:       2026-10-19
Author_Credit:      Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:      e5b1287c-3f94-4d82-b7e1-80a9c6d3f154
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

VERSION = "100"
RELEASE_VERSION = "300"
RELATIONAL_ID = "e5b1287c-3f94-4d82-b7e1-80a9c6d3f154"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("definitions_lookup")


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


def get_default_registry_path() -> Path:
    return get_script_path().parent / "data" / "definitions_registry.104a.bejson"


def sanitize_val(val: Any) -> Any:
    """Boundary-layer whitespace sanitization per Policy §10.9."""
    if isinstance(val, str):
        return val.strip()
    return val


def load_registry(registry_path: Path) -> tuple[Dict[str, Any], Dict[str, int]]:
    """Loads BEJSON 104a definitions registry and compiles an O(1) Field Map Cache."""
    if not registry_path.exists():
        LOG.error("Registry file not found: %s", registry_path)
        sys.exit(20)

    try:
        raw_data = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as exc:
        LOG.error("Failed to parse registry JSON: %s", exc)
        sys.exit(30)

    fields = raw_data.get("Fields", [])
    if not isinstance(fields, list) or not fields:
        LOG.error("Missing or invalid 'Fields' array in registry.")
        sys.exit(30)

    fmap: Dict[str, int] = {}
    for idx, fld in enumerate(fields):
        fname = sanitize_val(fld.get("name"))
        if not fname:
            LOG.error("Field at index %d has no name.", idx)
            sys.exit(30)
        fmap[fname] = idx

    return raw_data, fmap


def query_definitions(
    doc: Dict[str, Any],
    fmap: Dict[str, int],
    query_str: Optional[str] = None,
    term_str: Optional[str] = None,
    category_str: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Queries definitions matching exact term, substring/alias query, or category."""
    rows = doc.get("Values", [])
    results: List[Dict[str, Any]] = []

    q_lower = query_str.lower().strip() if query_str else None
    t_lower = term_str.lower().strip() if term_str else None
    c_lower = category_str.lower().strip() if category_str else None

    for row in rows:
        rec = {k: sanitize_val(row[idx]) for k, idx in fmap.items()}
        canonical = str(rec.get("canonical_term", "")).lower()
        category = str(rec.get("domain_category", "")).lower()
        aliases = [a.strip() for a in str(rec.get("synonyms_aliases_csv", "")).lower().split(",") if a.strip()]
        defn = str(rec.get("inline_definition", "")).lower()

        # Category filter
        if c_lower and category != c_lower and c_lower not in category:
            continue

        # Exact term match
        if t_lower:
            if canonical == t_lower:
                results.append(rec)
            continue

        # Query filter (matches canonical name, aliases, or definition text)
        if q_lower:
            matched = False
            if q_lower == canonical or q_lower in canonical:
                matched = True
            elif any(q_lower == a or q_lower in a for a in aliases):
                matched = True
            elif q_lower in defn:
                matched = True

            if matched:
                results.append(rec)
            continue

        # If no specific query/term, include row (filtered by category if provided)
        results.append(rec)

    return results


def format_markdown(results: List[Dict[str, Any]]) -> str:
    """Formats definitions as a Markdown report."""
    lines: List[str] = [
        "# Ecosystem Definitions & Concept Cartography",
        "",
        f"> **Total Definitions Found:** {len(results)}",
        "",
        "| Canonical Term | Category | Inline Definition (Policy §5.1) | Policy Binding | Canonical Pointer |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in results:
        lines.append(
            f"| **`{r.get('canonical_term')}`** | `{r.get('domain_category')}` | "
            f"{r.get('inline_definition')} | `{r.get('policy_binding')}` | `{r.get('canonical_reference_pointer')}` |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="definitions_lookup",
        description="Definitions Cartographer: authoritative ecosystem terminology and semantic alias engine.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Register script with master index.")
    parser.add_argument("--config", action="store_true", help="Display script configuration.")
    parser.add_argument("--reset", action="store_true", help="Reset definitions state.")
    parser.add_argument("--registry", type=Path, default=get_default_registry_path(), help="Path to definitions_registry.104a.bejson.")
    parser.add_argument("--query", "-q", type=str, help="Fuzzy/alias search query across terms and definitions.")
    parser.add_argument("--term", "-t", type=str, help="Exact canonical term lookup.")
    parser.add_argument("--category", "-c", type=str, help="Filter by domain category (BEHTML, BEJSON, Policy, etc.).")
    parser.add_argument("--format", choices=["markdown", "json", "inline"], default="markdown", help="Output format.")

    args = parser.parse_args()

    if args.register:
        LOG.info("Registered definitions_lookup v%s (%s)", VERSION, RELATIONAL_ID)
        return 0

    if args.config:
        cfg = {
            "version": VERSION,
            "release_version": RELEASE_VERSION,
            "registry_path": str(args.registry),
            "author": "Elton Boehnen",
        }
        sys.stdout.write(json.dumps(cfg, indent=2) + "\n")
        return 0

    if args.reset:
        LOG.info("Definitions state reset complete.")
        return 0

    doc, fmap = load_registry(args.registry)
    results = query_definitions(
        doc,
        fmap,
        query_str=args.query,
        term_str=args.term,
        category_str=args.category,
    )

    if not results:
        LOG.warning("No definitions found matching criteria.")
        return 10

    if args.format == "json":
        sys.stdout.write(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    elif args.format == "inline":
        for r in results:
            sys.stdout.write(f"{r.get('canonical_term')}: {r.get('inline_definition')}\n")
    else:
        sys.stdout.write(format_markdown(results) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
