#!/usr/bin/env python3
"""
Name:           behtml_validate.py
Description:    Layer 2 Anti-Drift Auditor and Spatial Validator for BEHTML Documents.
                Enforces 8-lane horizontal partition, full 16-sublane (0.5 increment) quantization,
                Ry=32px row quantization, collision freedom across scoped z-layers, acyclic container
                hierarchies, zero-filler compliance, and the authoritative 300-329 error registry.
Version:        100
Release_Version: 300
Date Created:   2026-10-24
Author Credit:  Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  a4e10000-0001-4000-8000-000000000001
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 10):
    sys.stderr.write("behtml_validate requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

VERSION: int = 100
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "a4e10000-0001-4000-8000-000000000001"

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

# Error Code Registry (Codes 301-324)
E_BEHTML_MISSING_ID: int = 301
E_BEHTML_MISSING_TYPE: int = 302
E_BEHTML_DUPLICATE_ID: int = 303
E_BEHTML_UNKNOWN_TYPE: int = 304
E_BEHTML_INVALID_X_ADDRESS: int = 305
E_BEHTML_X_SPAN_OVERFLOW: int = 306
E_BEHTML_QUANTIZATION_FAIL: int = 307
E_BEHTML_INVALID_Y_ADDRESS: int = 308
E_BEHTML_INVALID_Z_LAYER: int = 309
E_BEHTML_PARENT_NOT_CONTAINER: int = 313
E_BEHTML_ELEMENT_NOT_FOUND: int = 314
E_BEHTML_INVALID_CONTENT_KIND: int = 315
E_BEHTML_INVALID_URL: int = 316
E_BEHTML_COLLISION: int = 317
E_BEHTML_INVALID_OPTION_SET_REF: int = 318
E_BEHTML_INVALID_ELEMENT_ID: int = 319
E_BEHTML_CYCLIC_PARENT: int = 320
E_BEHTML_INVALID_FONT_WEIGHT: int = 321
E_BEHTML_INVALID_FONT_SIZE: int = 322
E_BEHTML_INVALID_SLIDER_RANGE: int = 323
E_BEHTML_ZERO_FILLER_VIOLATION: int = 324

VALID_ELEMENT_TYPES: Set[str] = {
    "button",
    "input",
    "textarea",
    "combobox",
    "checkbox",
    "radio",
    "label",
    "container",
    "toolbar",
    "slider",
}
CONTAINER_TYPES: Set[str] = {"container", "toolbar"}
VALID_CONTENT_KINDS: Set[str] = {"text", "field_binding", "url", "asset_ref"}
SAFE_URL_PATTERN = re.compile(r"^(https?://|/)\S+$")
ELEMENT_ID_REGEX = re.compile(r"^[A-Za-z0-9_-]+$")

FORBIDDEN_FILLER_PATTERNS = [
    re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE),
    re.compile(r"\bdolor\s+sit\s+amet\b", re.IGNORECASE),
    re.compile(r"\bfoo\s+bar\b", re.IGNORECASE),
    re.compile(r"\bquick\s+brown\s+fox\b", re.IGNORECASE),
    re.compile(r"\bplaceholder\s+text\b", re.IGNORECASE),
    re.compile(r"\bsample\s+content\b", re.IGNORECASE),
    re.compile(r"\btest\s+item\b", re.IGNORECASE),
]


def get_script_path() -> Path:
    """Self-locating script path per Policy §4.1."""
    return Path(__file__).resolve().parent


SCRIPT_PATH: Path = get_script_path()
BUNDLE_ROOT: Path = SCRIPT_PATH.parent
CONFIG_PATH: Path = BUNDLE_ROOT / "config" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("behtml_validate")


def bejson_boundary_sanitize(raw: Any) -> Any:
    """Strip boundary whitespace on keys and string values per Policy §10.9."""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        return [bejson_boundary_sanitize(item) for item in raw]
    if isinstance(raw, dict):
        return {str(k).strip(): bejson_boundary_sanitize(v) for k, v in raw.items()}
    return raw


def bejson_get_field_map(doc: dict[str, Any]) -> dict[str, int]:
    """Compile O(1) field name to column index map per Policy §6.2."""
    fields = doc.get("Fields", [])
    field_map: dict[str, int] = {}
    for idx, field_def in enumerate(fields):
        if isinstance(field_def, dict) and "name" in field_def:
            clean_name = str(field_def["name"]).strip()
            field_map[clean_name] = idx
    return field_map


def ensure_config_104a() -> dict[str, Any]:
    """Generate or load BEJSON 104a ScriptConfig per Policy §4.4."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_cfg = {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Records_Type": ["ScriptConfig"],
            "Fields": [
                {"name": "setting_name", "type": "string"},
                {"name": "setting_value", "type": "string"},
                {"name": "description", "type": "string"},
            ],
            "Values": [
                ["local_lib_directory", "lib/", "Relative path to local dep folder."],
                ["master_lib_source", "$ADMIN_LIBRARIES", "Fallback master library directory."],
                ["log_level", "INFO", "Default operational log level."],
                ["enforce_zero_filler", "true", "Enforce Elton Boehnen Zero-Filler Law on content strings."],
                ["allow_sublanes", "true", "Allow 16-sublane half-cell (0.5 increment) spatial coordinates."],
            ],
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, indent=2) + "\n", encoding="utf-8")
    return bejson_boundary_sanitize(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))


class BEHTMLValidationError:
    def __init__(self, code: int, message: str, element_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.element_id = element_id

    def __str__(self) -> str:
        target = f" [element: '{self.element_id}']" if self.element_id else ""
        return f"Code {self.code}: {self.message}{target}"


def parse_bejson_elements(doc: dict[str, Any]) -> Tuple[list[dict[str, Any]], list[BEHTMLValidationError]]:
    """Convert BEJSON 104 BEHTMLElement rows into dictionaries via field_map."""
    errors: list[BEHTMLValidationError] = []
    fmap = bejson_get_field_map(doc)
    required_cols = ["element_id", "element_type", "x_start", "x_span", "y_start", "y_span"]
    for col in required_cols:
        if col not in fmap:
            errors.append(BEHTMLValidationError(302, f"BEHTMLElement Fields missing required column '{col}'."))
    if errors:
        return [], errors

    rev_map = {idx: name for name, idx in fmap.items()}
    elements: list[dict[str, Any]] = []
    for r_idx, row in enumerate(doc.get("Values", [])):
        if not isinstance(row, list):
            errors.append(BEHTMLValidationError(301, f"Values row {r_idx} is not an array."))
            continue
        el = {rev_map[i]: row[i] for i in range(len(row)) if i in rev_map}
        elements.append(el)
    return elements, errors


def validate_spatial_bounds(el: dict[str, Any], allow_sublanes: bool = True) -> list[BEHTMLValidationError]:
    """Validate 8-lane horizontal bounds and Ry=32px quantization."""
    errors: list[BEHTMLValidationError] = []
    eid = el.get("element_id")

    x_start = el.get("x_start", 0)
    x_span = el.get("x_span", 1)
    y_start = el.get("y_start", 0)
    y_span = el.get("y_span", 1)
    z_layer = el.get("z_layer", 0)

    # Validate x_start
    if not isinstance(x_start, (int, float)):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_start must be numeric, got {type(x_start).__name__}", eid))
    elif x_start < 0 or x_start > 7.5:
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_start out of range (0.0 to 7.5): {x_start}", eid))
    elif not allow_sublanes and not isinstance(x_start, int):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"Half-cell x_start '{x_start}' not allowed when sublanes disabled.", eid))
    elif (x_start * 2) != int(x_start * 2):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_start must snap to 0.5 half-cell increments: {x_start}", eid))

    # Validate x_span
    if not isinstance(x_span, (int, float)):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_span must be numeric, got {type(x_span).__name__}", eid))
    elif x_span < 0.5:
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_span must be >= 0.5: {x_span}", eid))
    elif not allow_sublanes and not isinstance(x_span, int):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"Half-cell x_span '{x_span}' not allowed when sublanes disabled.", eid))
    elif (x_span * 2) != int(x_span * 2):
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_X_ADDRESS, f"x_span must snap to 0.5 half-cell increments: {x_span}", eid))

    # Validate X overflow
    if isinstance(x_start, (int, float)) and isinstance(x_span, (int, float)):
        if x_start + x_span > 8.0:
            errors.append(BEHTMLValidationError(E_BEHTML_X_SPAN_OVERFLOW, f"X span overflow: {x_start} + {x_span} = {x_start + x_span} > 8.0", eid))

    # Validate y_start
    if not isinstance(y_start, int) or y_start < 0:
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_Y_ADDRESS, f"y_start must be an integer >= 0, got {y_start}", eid))

    # Validate y_span (quantization: must be integer >= 1 rows of 32px)
    if not isinstance(y_span, int) or y_span < 1:
        errors.append(BEHTMLValidationError(E_BEHTML_QUANTIZATION_FAIL, f"y_span must be integer >= 1 row (32px), got {y_span}", eid))

    # Validate z_layer
    if not isinstance(z_layer, int) or z_layer < 0:
        errors.append(BEHTMLValidationError(E_BEHTML_INVALID_Z_LAYER, f"z_layer must be an integer >= 0, got {z_layer}", eid))

    return errors


def validate_zero_filler(content: str, eid: Optional[str] = None) -> list[BEHTMLValidationError]:
    """Enforce Elton Boehnen Zero-Filler Law on content text."""
    errors: list[BEHTMLValidationError] = []
    if not content or not isinstance(content, str):
        return errors

    for pat in FORBIDDEN_FILLER_PATTERNS:
        if pat.search(content):
            errors.append(
                BEHTMLValidationError(
                    E_BEHTML_ZERO_FILLER_VIOLATION,
                    f"Forbidden filler content matched pattern '{pat.pattern}': \"{content[:40]}...\"",
                    eid,
                )
            )
            break
    return errors


def check_collisions(elements: list[dict[str, Any]]) -> list[BEHTMLValidationError]:
    """
    Assert collision-freedom across elements sharing the same (parent_id_fk, z_layer).
    Two bounding boxes collide if:
      x1 < x2 + span2 AND x1 + span1 > x2 AND
      y1 < y2 + span2 AND y1 + span1 > y2
    """
    errors: list[BEHTMLValidationError] = []
    buckets: dict[Tuple[Any, int], list[dict[str, Any]]] = {}

    for el in elements:
        parent = el.get("parent_id_fk")
        z = el.get("z_layer", 0)
        key = (parent, z)
        buckets.setdefault(key, []).append(el)

    for (parent, z), bucket in buckets.items():
        n = len(bucket)
        for i in range(n):
            el_a = bucket[i]
            id_a = el_a.get("element_id")
            xa = el_a.get("x_start", 0)
            xsa = el_a.get("x_span", 1)
            ya = el_a.get("y_start", 0)
            ysa = el_a.get("y_span", 1)

            for j in range(i + 1, n):
                el_b = bucket[j]
                id_b = el_b.get("element_id")
                xb = el_b.get("x_start", 0)
                xsb = el_b.get("x_span", 1)
                yb = el_b.get("y_start", 0)
                ysb = el_b.get("y_span", 1)

                # Axis-aligned bounding box collision test
                x_overlap = (xa < xb + xsb) and (xa + xsa > xb)
                y_overlap = (ya < yb + ysb) and (ya + ysa > yb)

                if x_overlap and y_overlap:
                    msg = (
                        f"Collision on z_layer {z} (scope: '{parent}'): "
                        f"Element '{id_a}' [x:{xa}..{xa+xsa}, y:{ya}..{ya+ysa}] overlaps "
                        f"Element '{id_b}' [x:{xb}..{xb+xsb}, y:{yb}..{yb+ysb}]"
                    )
                    errors.append(BEHTMLValidationError(E_BEHTML_COLLISION, msg, f"{id_a}<->{id_b}"))

    return errors


def check_cyclic_parenting(elements: list[dict[str, Any]]) -> list[BEHTMLValidationError]:
    """Detect circular parent dependencies (A -> B -> A)."""
    errors: list[BEHTMLValidationError] = []
    parent_map: dict[str, Optional[str]] = {}
    for el in elements:
        eid = el.get("element_id")
        if eid:
            parent_map[eid] = el.get("parent_id_fk")

    for eid, pid in parent_map.items():
        if not pid:
            continue
        if pid == eid:
            errors.append(BEHTMLValidationError(E_BEHTML_CYCLIC_PARENT, f"Element '{eid}' cannot parent itself.", eid))
            continue

        visited = {eid}
        curr = pid
        while curr:
            if curr in visited:
                errors.append(
                    BEHTMLValidationError(
                        E_BEHTML_CYCLIC_PARENT,
                        f"Cyclic parent dependency detected involving '{eid}' and '{curr}'.",
                        eid,
                    )
                )
                break
            visited.add(curr)
            curr = parent_map.get(curr)

    return errors


def validate_element_list(
    elements: list[dict[str, Any]], enforce_filler: bool = True, allow_sublanes: bool = True
) -> Tuple[bool, list[BEHTMLValidationError]]:
    """Run full suite of BEHTML rules against list of element dicts."""
    errors: list[BEHTMLValidationError] = []
    seen_ids: set[str] = set()
    element_map: dict[str, dict[str, Any]] = {}

    # Pass 1: Individual element checks
    for el in elements:
        eid = el.get("element_id")
        etype = el.get("element_type")

        # 301 Missing ID
        if not eid or not isinstance(eid, str) or not eid.strip():
            errors.append(BEHTMLValidationError(E_BEHTML_MISSING_ID, "element_id is missing or empty."))
            continue

        clean_id = eid.strip()
        # 319 Invalid ID syntax
        if not ELEMENT_ID_REGEX.match(clean_id):
            errors.append(BEHTMLValidationError(E_BEHTML_INVALID_ELEMENT_ID, f"Invalid element_id '{clean_id}'. Must match ^[A-Za-z0-9_-]+$", clean_id))

        # 303 Duplicate ID
        if clean_id in seen_ids:
            errors.append(BEHTMLValidationError(E_BEHTML_DUPLICATE_ID, f"Duplicate element_id detected: '{clean_id}'", clean_id))
        seen_ids.add(clean_id)
        element_map[clean_id] = el

        # 302 Missing Type
        if not etype or not isinstance(etype, str) or not etype.strip():
            errors.append(BEHTMLValidationError(E_BEHTML_MISSING_TYPE, "element_type is missing or empty.", clean_id))
        else:
            clean_type = etype.strip()
            # 304 Unknown Type warning
            if clean_type not in VALID_ELEMENT_TYPES:
                errors.append(BEHTMLValidationError(E_BEHTML_UNKNOWN_TYPE, f"Unknown element_type '{clean_type}'.", clean_id))

        # Spatial Bounds & Quantization
        errors.extend(validate_spatial_bounds(el, allow_sublanes=allow_sublanes))

        # Content Kind & URL Safety
        ckind = el.get("content_kind", "text")
        if ckind and ckind not in VALID_CONTENT_KINDS:
            errors.append(BEHTMLValidationError(E_BEHTML_INVALID_CONTENT_KIND, f"Invalid content_kind '{ckind}'. Allowed: {VALID_CONTENT_KINDS}", clean_id))

        cref = el.get("content_ref")
        if ckind == "url" and cref and isinstance(cref, str):
            if not SAFE_URL_PATTERN.match(cref.strip()):
                errors.append(BEHTMLValidationError(E_BEHTML_INVALID_URL, f"Unsafe URL scheme in content_ref '{cref}'. Only http://, https://, or / permitted.", clean_id))

        # Zero Filler Check
        if enforce_filler and cref and isinstance(cref, str) and ckind == "text":
            errors.extend(validate_zero_filler(cref, clean_id))

        # Typography bounds
        fweight = el.get("font_weight")
        if fweight is not None and fweight not in ("normal", "bold", ""):
            errors.append(BEHTMLValidationError(E_BEHTML_INVALID_FONT_WEIGHT, f"Invalid font_weight '{fweight}'. Allowed: normal, bold, null.", clean_id))

        fsize = el.get("font_size")
        if fsize is not None:
            if not isinstance(fsize, int) or fsize <= 0:
                errors.append(BEHTMLValidationError(E_BEHTML_INVALID_FONT_SIZE, f"font_size must be positive integer px, got {fsize}", clean_id))

        # Slider bounds
        if etype == "slider":
            rmin = el.get("range_min", 0)
            rmax = el.get("range_max", 100)
            rstep = el.get("range_step", 1)
            if not isinstance(rmin, int) or not isinstance(rmax, int) or rmin >= rmax:
                errors.append(BEHTMLValidationError(E_BEHTML_INVALID_SLIDER_RANGE, f"Invalid slider range: min ({rmin}) must be < max ({rmax})", clean_id))
            if not isinstance(rstep, int) or rstep < 1:
                errors.append(BEHTMLValidationError(E_BEHTML_INVALID_SLIDER_RANGE, f"Invalid slider range_step ({rstep}): must be integer >= 1", clean_id))

    # Pass 2: Relational Integrity (Parent checks)
    for el in elements:
        eid = el.get("element_id")
        pid = el.get("parent_id_fk")
        if pid:
            if pid not in element_map:
                errors.append(BEHTMLValidationError(E_BEHTML_ELEMENT_NOT_FOUND, f"parent_id_fk '{pid}' references non-existent element.", eid))
            else:
                parent_el = element_map[pid]
                parent_type = parent_el.get("element_type")
                if parent_type not in CONTAINER_TYPES:
                    errors.append(BEHTMLValidationError(E_BEHTML_PARENT_NOT_CONTAINER, f"parent_id_fk '{pid}' is type '{parent_type}' (must be container or toolbar).", eid))

    # Pass 3: Cyclic Parenting
    errors.extend(check_cyclic_parenting(elements))

    # Pass 4: Collision Assertion
    errors.extend(check_collisions(elements))

    return len(errors) == 0, errors


def validate_html_file(file_path: Path) -> Tuple[bool, list[BEHTMLValidationError]]:
    """Audit rendered HTML document against BEHTML CSS tokens and spatial grid classes."""
    errors: list[BEHTMLValidationError] = []
    text = file_path.read_text(encoding="utf-8")

    # Required foundational preferences check
    if "box-sizing: border-box" not in text and "box-sizing:border-box" not in text:
        errors.append(BEHTMLValidationError(307, "HTML missing universal box-sizing: border-box reset."))
    if "--ry-unit" not in text and "32px" not in text:
        errors.append(BEHTMLValidationError(307, "HTML missing Ry vertical quantization unit (--ry-unit: 32px)."))
    if "#DE2626" not in text and "#de2626" not in text:
        errors.append(BEHTMLValidationError(307, "HTML missing Policy 8.1 Tri-Color Red accent (#DE2626)."))

    # Zero filler check on full HTML body
    for pat in FORBIDDEN_FILLER_PATTERNS:
        match = pat.search(text)
        if match:
            errors.append(
                BEHTMLValidationError(
                    E_BEHTML_ZERO_FILLER_VIOLATION,
                    f"Forbidden filler content in HTML: \"{match.group(0)}\"",
                )
            )
            break

    return len(errors) == 0, errors


def validate_file(file_path: Path, enforce_filler: bool = True, allow_sublanes: bool = True) -> bool:
    """Validate a BEHTML data file (.bejson) or HTML layout file."""
    if not file_path.is_file():
        LOG.error("Target file does not exist: %s", file_path)
        return False

    suffix = file_path.suffix.lower()

    # 1. BEJSON element dataset
    if suffix in (".bejson", ".json"):
        try:
            raw = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as exc:
            LOG.error("Failed to parse JSON in %s: %s", file_path, exc)
            return False

        if isinstance(raw, dict) and "Fields" in raw and "Values" in raw:
            elements, parse_errs = parse_bejson_elements(raw)
            if parse_errs:
                LOG.error("Failed to parse BEHTMLElement rows in %s:", file_path)
                for err in parse_errs:
                    LOG.error("  - %s", err)
                return False
        elif isinstance(raw, list):
            elements = raw
        else:
            LOG.error("Unsupported JSON root shape in %s (must be BEJSON or element list).", file_path)
            return False

        valid, errors = validate_element_list(elements, enforce_filler=enforce_filler, allow_sublanes=allow_sublanes)
        if not valid:
            LOG.error("BEHTML validation failed for %s (%d errors):", file_path.name, len(errors))
            for err in errors:
                LOG.error("  - %s", err)
            return False
        LOG.info("Valid BEHTML Dataset: %s [%d elements, collision-free, quantized]", file_path.name, len(elements))
        return True

    # 2. Rendered HTML page
    elif suffix in (".html", ".htm"):
        valid, errors = validate_html_file(file_path)
        if not valid:
            LOG.error("HTML design preference validation failed for %s (%d errors):", file_path.name, len(errors))
            for err in errors:
                LOG.error("  - %s", err)
            return False
        LOG.info("Valid BEHTML Document Layout: %s [Tri-Color, Ry=32px snapped, zero-filler verified]", file_path.name)
        return True

    else:
        LOG.warning("Skipping non-BEHTML file: %s", file_path)
        return True


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="behtml_validate",
        description="Layer 2 Anti-Drift Auditor and Spatial Validator for BEHTML Documents.",
    )
    parser.add_argument("target", nargs="?", help="Path to .bejson element dataset or .html layout file.")
    parser.add_argument("--version", action="version", version=f"behtml_validate v{VERSION} (Release {RELEASE_VERSION})")
    parser.add_argument("--register", action="store_true", help="Display project registration command.")
    parser.add_argument("--config", action="store_true", help="Initialize and display 104a ScriptConfig.")
    parser.add_argument("--reset", action="store_true", help="Reset config/config.json to canonical defaults.")
    parser.add_argument("--no-filler-check", action="store_true", help="Bypass zero-filler content text checks.")
    parser.add_argument("--disallow-sublanes", action="store_true", help="Reject 0.5 half-cell (16-sublane) coordinates.")

    args = parser.parse_args()
    if args.reset and CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
    cfg = ensure_config_104a()
    fmap = bejson_get_field_map(cfg)

    if args.config:
        settings = {row[fmap["setting_name"]]: row[fmap["setting_value"]] for row in cfg.get("Values", [])}
        LOG.info("Active 104a ScriptConfig: %s", json.dumps(settings))
        return EXIT_OK
    if args.register:
        LOG.info("Registration: python3 $PROJECT_INDEX_ROOT/cli_project_register.py --register \"%s\"", BUNDLE_ROOT)
        return EXIT_OK
    if not args.target:
        parser.print_help(sys.stderr)
        return EXIT_PATH_FAILURE

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        LOG.error("Target path not found: %s", target_path)
        return EXIT_PATH_FAILURE

    enforce_filler = not args.no_filler_check
    allow_sublanes = not getattr(args, "disallow_sublanes", False)

    if target_path.is_file():
        files_to_check = [target_path]
    else:
        files_to_check = sorted(
            [p for p in target_path.rglob("*") if p.suffix.lower() in (".bejson", ".json", ".html", ".htm")]
        )
        if not files_to_check:
            LOG.warning("No BEHTML or HTML files found in directory: %s", target_path)
            return EXIT_OK

    all_passed = True
    for f in files_to_check:
        if not validate_file(f, enforce_filler=enforce_filler, allow_sublanes=allow_sublanes):
            all_passed = False

    return EXIT_OK if all_passed else EXIT_SCHEMA_FAILURE


if __name__ == "__main__":
    sys.exit(main())
