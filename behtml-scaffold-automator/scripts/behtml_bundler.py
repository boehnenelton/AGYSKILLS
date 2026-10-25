#!/usr/bin/env python3
"""
File:          behtml_bundler.py
Description:   Layer 3 BEHTML Static Site Bundler, Token Injector & Distribution Scaffolder.
               Automates the compilation, asset localization, BECSS Tri-Color token
               injection, and distribution staging for deterministic BEHTML interfaces.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6e
"""

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("behtml_bundler requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [behtml_bundler]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("behtml_bundler")

TRI_COLOR_CSS_BLOCK = """<style id="becss-injected-tokens">
  :root {
    --bg-primary: #000000;
    --text-primary: #FFFFFF;
    --accent-red: #DE2626;
    --grid-lane-width: 12.5%;
    --grid-sublane-width: 6.25%;
    --row-unit-height: 32px;
  }
  body {
    margin: 0;
    padding: 0;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
  }
  .behtml-lane-grid {
    display: grid;
    grid-template-columns: repeat(8, 12.5%);
    width: 100%;
    box-sizing: border-box;
  }
  .behtml-sublane-grid {
    display: grid;
    grid-template-columns: repeat(16, 6.25%);
    width: 100%;
    box-sizing: border-box;
  }
</style>"""


def compute_sha256(filepath: Path) -> str:
    """Calculates SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def audit_tri_color_compliance(html_content: str) -> Tuple[bool, List[str]]:
    """Checks for adherence to #000000, #FFFFFF, and #DE2626 color palette."""
    warnings = []
    # Search for arbitrary hex colors
    found_hexes = set(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", html_content))
    allowed_hexes = {"#000000", "#000", "#ffffff", "#fff", "#de2626", "#DE2626"}
    
    disallowed = [h for h in found_hexes if h.lower() not in {"#000000", "#000", "#ffffff", "#fff", "#de2626"}]
    if disallowed:
        warnings.append(f"Found non-tri-color hex values: {disallowed[:5]}")
    return len(warnings) == 0, warnings


def audit_zero_filler(html_content: str) -> Tuple[bool, List[str]]:
    """Checks for forbidden lorem ipsum or fabricated filler copy."""
    errors = []
    filler_terms = ["lorem ipsum", "dolor sit amet", "consectetur adipiscing", "sample body text"]
    lower_content = html_content.lower()
    for term in filler_terms:
        if term in lower_content:
            errors.append(f"Found forbidden filler copy: '{term}'")
    return len(errors) == 0, errors


def inject_becss_tokens(html_content: str) -> str:
    """Injects canonical BECSS Tri-Color tokens into <head> if not already present."""
    if "becss-injected-tokens" in html_content:
        return html_content

    if "</head>" in html_content:
        return html_content.replace("</head>", f"  {TRI_COLOR_CSS_BLOCK}\n</head>", 1)
    elif "<body>" in html_content:
        return html_content.replace("<body>", f"<head>\n  {TRI_COLOR_CSS_BLOCK}\n</head>\n<body>", 1)
    else:
        return f"{TRI_COLOR_CSS_BLOCK}\n{html_content}"


def bundle_behtml_page(
    source_file: Path,
    dist_dir: Path,
    project_name: str = "BEHTML_Project",
    manifest_path: Optional[Path] = None
) -> Optional[Path]:
    """Bundles, injects tokens, audits, and stages a BEHTML document."""
    if not source_file.exists():
        logger.error(f"Source file does not exist: {source_file}")
        return None

    raw_html = source_file.read_text(encoding="utf-8")
    tri_ok, tri_warn = audit_tri_color_compliance(raw_html)
    for w in tri_warn:
        logger.warning(f"Compliance note: {w}")

    filler_ok, filler_err = audit_zero_filler(raw_html)
    if not filler_ok:
        logger.error(f"Zero-filler audit failed: {filler_err}")
        return None

    processed_html = inject_becss_tokens(raw_html)

    dist_dir.mkdir(parents=True, exist_ok=True)
    dist_file = dist_dir / source_file.name
    dist_file.write_text(processed_html, encoding="utf-8")
    logger.info(f"Staged bundled HTML to: {dist_file}")

    file_sha = compute_sha256(dist_file)

    if manifest_path:
        update_bejson_manifest(
            manifest_path=manifest_path,
            record={
                "build_id": f"bld_{int(datetime.now(timezone.utc).timestamp())}",
                "project_name": project_name,
                "source_html_path": str(source_file),
                "dist_html_path": str(dist_file),
                "total_elements": len(re.findall(r"<[a-zA-Z0-9_-]+", processed_html)),
                "grid_system": "8-lane-Ry32",
                "tri_color_compliant": tri_ok,
                "validation_status": "PASSED",
                "sha256_hash": file_sha,
                "build_timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

    return dist_file


def update_bejson_manifest(manifest_path: Path, record: Dict[str, Any]) -> None:
    """Updates BEJSON 104a build manifest."""
    manifest_data: Dict[str, Any] = {"Values": []}
    if manifest_path.exists():
        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest_data = {"Values": []}

    fields = manifest_data.get("Fields", [
        {"name": "build_id", "type": "string"},
        {"name": "project_name", "type": "string"},
        {"name": "source_html_path", "type": "string"},
        {"name": "dist_html_path", "type": "string"},
        {"name": "total_elements", "type": "integer"},
        {"name": "grid_system", "type": "string"},
        {"name": "tri_color_compliant", "type": "boolean"},
        {"name": "validation_status", "type": "string"},
        {"name": "sha256_hash", "type": "string"},
        {"name": "build_timestamp", "type": "string"}
    ])
    manifest_data["Fields"] = fields

    field_map = {f["name"]: idx for idx, f in enumerate(fields)}
    row = [None] * len(fields)
    for k, v in record.items():
        if k in field_map:
            row[field_map[k]] = v

    manifest_data.setdefault("Values", []).append(row)
    manifest_data["Format"] = "BEJSON"
    manifest_data["Format_Version"] = "104a"
    manifest_data["Format_Creator"] = "Elton Boehnen"
    manifest_data["Records_Type"] = ["BEHTMLBuildRecord"]

    tmp_path = manifest_path.parent / f"{manifest_path.name}.tmp"
    tmp_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    os.replace(tmp_path, manifest_path)
    logger.info(f"Updated BEJSON 104a build manifest: {manifest_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BEHTML Static Site Bundler & Scaffolder"
    )
    parser.add_argument("source", type=Path, help="Path to source BEHTML file or directory")
    parser.add_argument("--dist-dir", type=Path, default=Path("dist"), help="Output distribution folder (default: dist/)")
    parser.add_argument("--project-name", type=str, default="BEHTML_App", help="Project name identifier")
    parser.add_argument("--manifest", type=Path, default=None, help="Optional BEJSON 104a build manifest path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.source.exists():
        logger.error(f"Target not found: {args.source}")
        sys.exit(1)

    if args.source.is_file():
        res = bundle_behtml_page(args.source, args.dist_dir, args.project_name, args.manifest)
        if res and res.exists():
            logger.info("Build completed successfully.")
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        html_files = list(args.source.glob("*.html"))
        if not html_files:
            logger.warning(f"No HTML files found in {args.source}")
            sys.exit(0)
        for hf in html_files:
            bundle_behtml_page(hf, args.dist_dir, args.project_name, args.manifest)
        logger.info(f"Bundled {len(html_files)} HTML pages into {args.dist_dir}")


if __name__ == "__main__":
    main()
