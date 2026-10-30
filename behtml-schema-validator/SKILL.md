---
name: behtml-schema-validator
description: Validate structural integrity, coordinate quantization (8-lane/32px), collision freedom, zero-filler compliance, and schema adherence for BEHTML documents across Python, JavaScript, TypeScript, and Bash. Use when auditing BEHTML documents, detecting schema drift, inspecting error codes (300-329), verifying collision boundaries, validating URL schemes, or checking cyclic parent hierarchies. Do NOT use for BEJSON validation (use bejson-104-validator), low-level format primitives (use behtml-format-core), or layout composition (use behtml-layout-builder).
---
# BEHTML Schema Validator

The authoritative Anti-Drift Auditor and structural validator for BEHTML documents, enforcing four-language parity across Python, JavaScript, TypeScript, and Bash.

## Summary

Audits and validates BEHTML documents, element trees, and project entities against Elton Boehnen's deterministic spatial laws. Enforces exact error codes (300-329), identical error messaging across runtimes, 8-lane horizontal boundaries, Ry=32px vertical quantization, collision freedom across scoped z-layers, acyclic container hierarchies, zero-filler placeholder compliance, and sanitized identifier patterns.

## When to Use

- Validating BEHTML documents before persisting or rendering.
- Checking 8-lane bounds (`x_start + x_span <= 8`) and row quantization (`y_span * 32px`).
- Detecting spatial collisions within the same container scope and `z_layer`.
- Verifying container hierarchy validity and preventing cyclic parenting (`A -> B -> A`).
- Auditing content kinds (`text`, `field_binding`, `url`, `asset_ref`) and URL safety schemes.
- Auditing zero-filler compliance and minimal functional section labels (`Title`, `Body`, `List Item 1`, `List Item 2`, `Action Button`).
- Verifying typography bounds (`font_size`, `font_weight`) and slider parameters (`min`, `max`, `step`).
- Mapping validation failures to the authoritative 300-329 error code registry.

## When NOT to Use

- Validating general BEJSON 104/104a tabular records outside BEHTML (use `bejson-schema-validator`).
- Calculating coordinate math, dimensions, or padding laws (use `behtml-format-core`).
- Assembling or composing UI layouts, dashboards, and templates (use `behtml-layout-builder`).
- Tracing navigation sitemaps or decomposing web routes (use `ui-navigation-decomposer`).

## The Four-Language Parity Contract

The BEHTML Anti-Drift Auditor exists with strict parity across four target environments:

1. **Python** (`lib_bejson_BEHTML_validator.py`): Core reference validator using standard library only.
2. **JavaScript** (`lib/Lib_JS/BEHTML/lib_bejson_BEHTML_validator.js`): Browser and Node.js vanilla runtime.
3. **TypeScript** (`lib/Lib_TS/BEHTML/lib_bejson_BEHTML_validator.ts`): Compiled under strict mode.
4. **Bash** (`lib/Lib_SH/BEHTML/lib_bejson_BEHTML_validator.sh`): Termux and Linux shell validator using `jq`. Uses the `BEHTML_LAST_ERROR_CODE` global variable to prevent exit code 255 truncation.

Parity Invariant: Given the identical malformed BEHTML input, all four implementations MUST return the exact same numeric error code and identical message text.

## Comprehensive Error Code Registry (Codes 300-329)

| Code | Symbolic Constant | Failure Condition | Remediation |
| :--- | :--- | :--- | :--- |
| 301 | `E_BEHTML_MISSING_ID` | `element_id` is missing, empty, or null | Assign a unique string identifier |
| 302 | `E_BEHTML_MISSING_TYPE` | `element_type` field is missing or empty | Specify valid element type |
| 303 | `E_BEHTML_DUPLICATE_ID` | Two elements share the same `element_id` | Ensure all IDs are unique in document |
| 304 | `E_BEHTML_UNKNOWN_TYPE` | `element_type` outside standard set (Soft warning) | Verify element type against catalog |
| 305 | `E_BEHTML_INVALID_X_ADDRESS` | `x_start < 0`, `x_start > 7`, or `x_span < 1` | Correct start to 0-7, span to >= 1 |
| 306 | `E_BEHTML_X_SPAN_OVERFLOW` | `x_start + x_span > 8` | Reduce span or adjust start lane |
| 307 | `E_BEHTML_QUANTIZATION_FAIL` | Height footprint is not integer multiple of 32px | Ensure height snaps to `y_span * 32px` |
| 308 | `E_BEHTML_INVALID_Y_ADDRESS` | `y_start < 0` or `y_span < 1` | Correct row index or span |
| 309 | `E_BEHTML_INVALID_Z_LAYER` | `z_layer < 0` or non-integer | Ensure z_layer is integer >= 0 |
| 313 | `E_BEHTML_PARENT_NOT_CONTAINER`| `parent_id_fk` references non-container element | Reparent under container or toolbar |
| 314 | `E_BEHTML_ELEMENT_NOT_FOUND` | Referenced element does not exist | Check element ID in current project |
| 315 | `E_BEHTML_INVALID_CONTENT_KIND`| `content_kind` not in allowed set | Set to text, field_binding, url, asset_ref |
| 316 | `E_BEHTML_INVALID_URL` | URL does not start with `https://`, `http://`, `/` | Reject javascript: or invalid schemes |
| 317 | `E_BEHTML_COLLISION` | Two elements overlap on same layer and container | Move element or adjust z_layer |
| 318 | `E_BEHTML_INVALID_OPTION_SET_REF`| `option_set_id` not found in project | Link to valid OptionSet or set null |
| 319 | `E_BEHTML_INVALID_ELEMENT_ID` | ID contains characters outside `^[A-Za-z0-9_-]+$` | Sanitize element_id string |
| 320 | `E_BEHTML_CYCLIC_PARENT` | Container references itself or its descendant | Break circular parenting chain |
| 321 | `E_BEHTML_INVALID_FONT_WEIGHT` | `font_weight` is set but not "normal" or "bold" | Set to "normal", "bold", or null |
| 322 | `E_BEHTML_INVALID_FONT_SIZE` | `font_size <= 0` or non-integer | Set to positive integer px or null |
| 323 | `E_BEHTML_INVALID_SLIDER_RANGE` | Slider `range_min >= range_max` or step invalid | Set valid min, max, and step |

## Core Validation Algorithms

### 1. Spatial Bounds Validation

```python
def validate_spatial_bounds(element: dict) -> None:
    x_start = element.get("x_start", 0)
    x_span = element.get("x_span", 1)
    y_start = element.get("y_start", 0)
    y_span = element.get("y_span", 1)
    z_layer = element.get("z_layer", 0)

    if not isinstance(x_start, int) or x_start < 0 or x_start > 7:
        raise BEHTMLError(305, f"Invalid x_start: {x_start}")
    if not isinstance(x_span, int) or x_span < 1:
        raise BEHTMLError(305, f"Invalid x_span: {x_span}")
    if x_start + x_span > 8:
        raise BEHTMLError(306, f"X span overflow: {x_start} + {x_span} > 8")
    if not isinstance(y_start, int) or y_start < 0:
        raise BEHTMLError(308, f"Invalid y_start: {y_start}")
    if not isinstance(y_span, int) or y_span < 1:
        raise BEHTMLError(307, f"Invalid y_span: {y_span}")
    if not isinstance(z_layer, int) or z_layer < 0:
        raise BEHTMLError(309, f"Invalid z_layer: {z_layer}")
```

### 2. Collision Assertion (Layer-Scoped)

Two elements collide if and only if:
1. They share the same container scope (`parent_id_fk`).
2. They reside on the exact same `z_layer`.
3. Their 2D axis-aligned bounding boxes overlap:
   `candidate_x < existing_x + existing_span` AND `candidate_x + candidate_span > existing_x` AND
   `candidate_y < existing_y + existing_span` AND `candidate_y + candidate_span > existing_y`.

Rule: Elements on different `z_layer` indices do NOT collide even if their X/Y coordinates are identical.

### 3. Cyclic Parent Detection

```python
def get_descendant_ids(doc: dict, element_id: str) -> set[str]:
    descendants = set()
    rows = doc.get("Values", [])
    def walk(parent_id: str):
        for row in rows:
            el = row_to_dict(doc, row)
            if el.get("parent_id_fk") == parent_id:
                cid = el.get("element_id")
                if cid and cid not in descendants:
                    descendants.add(cid)
                    walk(cid)
    walk(element_id)
    return descendants

def validate_parent(doc: dict, element_id: str, parent_id_fk: str | None) -> None:
    if parent_id_fk is None:
        return
    if parent_id_fk == element_id:
        raise BEHTMLError(320, f"Element '{element_id}' cannot parent itself.")
    descendants = get_descendant_ids(doc, element_id)
    if parent_id_fk in descendants:
        raise BEHTMLError(320, f"Cyclic parent detected: '{parent_id_fk}' is a descendant of '{element_id}'.")
```

### 4. URL Safety Validation

URL strings must strictly conform to safe schemes:

```python
import re
SAFE_URL_PATTERN = re.compile(r"^(https?://|/)\S+$")

def validate_url(url_string: str) -> None:
    if not SAFE_URL_PATTERN.match(url_string):
        raise BEHTMLError(316, f"Invalid URL scheme: '{url_string}'. Only http://, https://, or / paths permitted.")
```

### 5. Content Fluff and Zero-Filler Audit

When auditing BEHTML templates, layouts, or element records, verify that content strings adhere to Elton Boehnen's Zero-Filler Law:
- Confirm no forbidden filler patterns exist: lorem ipsum, simulated marketing claims, fake metrics, or verbose instructional text.
- Verify placeholder text strictly uses minimal, title-cased section labels: `"Title"`, `"Body"`, `"List Item 1"`, `"List Item 2"`, `"Action Button"`, `"Badge"`, `"Status"`.

## Step-by-Step Validation Workflow

1. **Verify Document Structure**:
   - Check format headers (`Format: "BEJSON"`, `Format_Creator: "Elton Boehnen"`).
   - Verify all 18 fields are declared in positional parity with row values.

2. **Inspect Individual Records**:
   - Validate `element_id` syntax (`^[A-Za-z0-9_-]+$`).
   - Validate spatial coordinates and row quantization.
   - Validate typography overrides and slider bounds.
   - Validate content kinds and sanitize URL targets.
   - Audit content strings against zero-filler standards.

3. **Inspect Relational Integrity**:
   - Confirm all `parent_id_fk` references point to existing containers.
   - Assert zero circular or self-referential parenting.
   - Verify all `option_set_id` references exist in project OptionSet storage.

4. **Assert Collision Freedom**:
   - Group records by `(parent_id_fk, z_layer)`.
   - Run pairwise 2D rectangle intersection tests on each bucket.
   - Return clean confirmation or raise exact `E_BEHTML_*` error code.
