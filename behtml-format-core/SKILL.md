---
name: behtml-format-core
description: Foundational data format specification, coordinate math, 8-lane/16-sublane spatial schemas (18-field BEHTMLElement, SCHEMA_OPTIONSET_v1), zero filler placeholder rules, and positional integrity rules for BEHTML across Python, JavaScript, TypeScript, and Bash. Use when authoring, modifying, inspecting, or serializing BEHTML documents, defining OptionSets, calculating 8-lane/16-sublane (6.25% half-cell) and 32px dimensions, or implementing low-level BEHTML primitives. Do NOT use for validation (use behtml-schema-validator), visual design preferences (use behtml-design-preferences), or UI layout composition (use behtml-layout-builder).
---
# BEHTML Format Core

Foundational specifications, coordinate invariants, data schemas, mathematical primitives, and canonical template examples for BEHTML documents adhering to Elton Boehnen's 2026 standards.

## Summary

Defines the low-level data structures, positional integrity rules, and coordinate mathematics governing BEHTML documents and Multi-File Database (MFDB) project storage. Enforces the authoritative 18-field `BEHTMLElement` schema, project-scoped `OptionSet` schema, 8-lane horizontal partition with full 16-sublane (`6.25%` half-cell) spatial precision, Ry=32px vertical row quantization, native z-layer stacking, zero filler content standards, and the generalized container padding law.

## When to Use

- Authoring, reading, or serializing raw `BEHTMLElement` records in BEJSON 104 tabular format.
- Calculating deterministic grid coordinates (`x_start`, `x_span`, `y_start`, `y_span`, `z_layer`) across both full macro cells (12.5%) and half-cell sublanes (6.25%).
- Implementing low-level BEHTML core library functions across Python, JS, TS, or Bash.
- Defining project-scoped reusable OptionSet records (`SCHEMA_OPTIONSET_v1`) for comboboxes using functional placeholders.
- Calculating visual padding and container gap geometry (`Ry=32px` and 28px Paradox).
- Enforcing zero filler content and minimal section labels across BEHTML datasets.

## When NOT to Use

- Performing structural validation, collision audits, or drift checks (use `behtml-schema-validator`).
- Consulting visual design tokens, seamless border transparencies, or typography rules (use `behtml-design-preferences`).
- Composing full production page layouts, dashboards, or UI components (use `behtml-layout-builder`).
- Decomposing navigation hierarchies or sitemaps (use `ui-navigation-decomposer`).
- Scaffolding bare-bones structural wireframe templates (use `template-architect`).

## Coordinate Math and Spatial Invariants

BEHTML layout is governed by three deterministic axes:

1. **X-Axis (8 Macro Lanes: 12.5% Each / 16 Sublanes: 6.25% Half-Cells)**:
   - Page width is partitioned into 8 equal macro lanes (`12.5%` per lane) and 16 half-cell sublanes (`6.25%` per sublane).
   - In 8-column BEHTML, a 16-cell (`6.25%`) or half-cell (`0.5` cell) placement is fully valid:
     - `x_start`: integer or half-step float from `0.0` to `7.5` in `0.5` increments (or sublane index `0..15`).
     - `x_span`: integer or half-step float from `0.5` to `8.0` in `0.5` increments (or sublane span `1..16`).
     - Invariant: `x_start + x_span <= 8.0` (or `sublane_start + sublane_span <= 16`). Values exceeding 8.0 are strictly invalid.
   - Percentage conversion: `width = x_span * 12.5% = sublane_span * 6.25%`.
   - Complete 16-Step Horizontal Quantization Matrix:
     - `0.5` cell (`1` sublane) = `6.25%`
     - `1.0` cell (`2` sublanes) = `12.50%`
     - `1.5` cells (`3` sublanes) = `18.75%`
     - `2.0` cells (`4` sublanes) = `25.00%`
     - `2.5` cells (`5` sublanes) = `31.25%`
     - `3.0` cells (`6` sublanes) = `37.50%`
     - `3.5` cells (`7` sublanes) = `43.75%`
     - `4.0` cells (`8` sublanes) = `50.00%`
     - `4.5` cells (`9` sublanes) = `56.25%`
     - `5.0` cells (`10` sublanes) = `62.50%`
     - `5.5` cells (`11` sublanes) = `68.75%`
     - `6.0` cells (`12` sublanes) = `75.00%`
     - `6.5` cells (`13` sublanes) = `81.25%`
     - `7.0` cells (`14` sublanes) = `87.50%`
     - `7.5` cells (`15` sublanes) = `93.75%`
     - `8.0` cells (`16` sublanes) = `100.00%`
   - Canonical Stage Sublane Partition: Sublane 1 (`6.25%`, 0.5 cell left gutter) + Sublanes 2..15 (`87.5%`, 7.0 cells active canvas) + Sublane 16 (`6.25%`, 0.5 cell right gutter) = `100.0%` (8.0 cells).

2. **Y-Axis (Row Quantization: Ry = 32px)**:
   - All vertical dimensions snap to integer multiples of `Ry = 32px`.
   - `y_start`: integer >= `0` representing row index.
   - `y_span`: integer >= `1` representing row span count.
   - Total vertical footprint = `y_span * 32px`. Arbitrary pixel heights are forbidden.
   - Canonical Document Row Allocation: Row 1 (`span 1 = 32px` title bar), Rows 2..18 (`span 17 = 544px` contained scrollable document canvas and side gutters), Row 19 (`span 1 = 32px` air-gap buffer), Rows 20..24 (`span 5 = 160px` widget shelf housing `150x150px` widgets).

3. **Generalized Padding Law (The 28px Paradox)**:
   - Outer padding is applied once per container footprint, not once per row (`visual_height = (y_span * 32px) - 4px`, with `4px` total vertical padding: `2px` top, `2px` bottom):
   - Data points:
     - `k = 1`: 28px visual height + 4px padding = 32px total.
     - `k = 2`: 60px visual height + 4px padding = 64px total.
     - `k = 3`: 92px visual height + 4px padding = 96px total.
   - Horizontal counterpart (`behtml_core_control_padding_x`): padding gap applies once per container footprint, not per lane.

4. **Z-Axis (Stacking Layers)**:
   - `z_layer`: non-negative integer (`0, 1, 2...`). Default is `0`.
   - Conversion to CSS z-index: `css_z_index = z_layer * 32`.
   - Native Stacking: In production applications, layers stack natively via CSS `z-index`. Higher layers completely occlude and block pointer events of lower layers unless explicitly configured with semi-transparent backdrops.
   - IDE Isolation: Translating layers (`32px` offset per layer) and fading opacity (`33.3%` per layer) is strictly an authoring tool inspection mode and must never be applied in production runtime.

5. **Container Scoping**:
   - `parent_id_fk`: `null` for root canvas elements, or string matching parent container `element_id`.
   - Child coordinates (`x_start`, `y_start`, `x_span`, `y_span`) are strictly local to the parent container's 8-lane / 16-sublane grid.

6. **Zero Filler Content Standard**:
   - All BEHTML data records, templates, and option sets must adhere to Elton Boehnen's Zero-Filler Law.
   - Layout containers and placeholder records must only use minimal, literal, title-cased section labels (`Title`, `Body`, `List`, `List Item 1`, `List Item 2`, `Action Button`, `Badge`, `Status`, `Input Field`).

## Authoritative 18-Field BEHTMLElement Schema

All BEHTML element entities are persisted in BEJSON 104 tabular format adhering strictly to these 18 fields:

| Field Index | Field Name | Data Type | Permitted Values / Constraints | Default Value |
| :--- | :--- | :--- | :--- | :--- |
| 0 | `element_id` | `string` | Regex `^[A-Za-z0-9_-]+$` | Required |
| 1 | `element_type` | `string` | `button`, `input`, `textarea`, `combobox`, `checkbox`, `radio`, `label`, `container`, `toolbar`, `slider` | Required |
| 2 | `y_start` | `integer` | Integer >= 0 | 0 |
| 3 | `y_span` | `integer` | Integer >= 1 | 1 |
| 4 | `x_start` | `number` | Float/Int 0.0 to 7.5 in 0.5 steps (or sublanes 0..15) | 0 |
| 5 | `x_span` | `number` | Float/Int 0.5 to 8.0 in 0.5 steps (`x_start + x_span <= 8.0`) | Type default |
| 6 | `z_layer` | `integer` | Integer >= 0 | 0 |
| 7 | `bem_modifiers` | `string` | Space or comma-delimited CSS modifier classes | `""` |
| 8 | `content_ref` | `string` | Text string, binding key, URL, or asset identifier | `""` |
| 9 | `content_kind` | `string` | `text`, `field_binding`, `url`, `asset_ref` | `"text"` |
| 10 | `parent_id_fk` | `string` | Valid `element_id` of parent container, or `null` | `null` |
| 11 | `is_active` | `boolean` | `true` or `false` | `true` |
| 12 | `option_set_id` | `string` | Valid referenced `OptionSet` ID, or `null` | `null` |
| 13 | `font_size` | `integer` | Positive integer (px override), or `null` | `null` |
| 14 | `font_weight` | `string` | `"normal"`, `"bold"`, or `null` | `null` |
| 15 | `range_min` | `integer` | Minimum range value (for `slider`) | 0 |
| 16 | `range_max` | `integer` | Maximum range value (`range_min < range_max`) | 100 |
| 17 | `range_step` | `integer` | Step interval (`1 <= range_step <= (range_max - range_min)`) | 1 |

### Standard Element Default Spans

- `button`: `x_span: 2`, `y_span: 1`
- `input`: `x_span: 4`, `y_span: 1`
- `textarea`: `x_span: 4`, `y_span: 2`
- `combobox`: `x_span: 3`, `y_span: 1`
- `checkbox`: `x_span: 1` (or `0.5` in 16-sublane layouts), `y_span: 1`
- `radio`: `x_span: 1` (or `0.5` in 16-sublane layouts), `y_span: 1`
- `label`: `x_span: 2`, `y_span: 1`
- `container`: `x_span: 8`, `y_span: 2`
- `toolbar`: `x_span: 8`, `y_span: 1`
- `slider`: `x_span: 4`, `y_span: 1`

## Project OptionSet Schema (`SCHEMA_OPTIONSET_v1`)

Reusable dropdown choices live at the project level in MFDB entity files using zero-fluff functional placeholders:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Parent_Hierarchy": "../104a.mfdb.bejson",
  "Records_Type": [
    "OptionSet"
  ],
  "Fields": [
    { "name": "option_set_id", "type": "string" },
    { "name": "name", "type": "string" },
    { "name": "options", "type": "string" }
  ],
  "Values": [
    ["opt_list", "List Options", "["List Item 1", "List Item 2"]"]
  ]
}
```

## Low-Level Mathematical Primitives (Reference Implementation)

```python
RY_PX = 32
X_LANES = 8
X_SUBLANES = 16
Z_LAYER_PX = 32

def behtml_core_validate_x_address(x_start: float, x_span: float) -> None:
    if not isinstance(x_start, (int, float)) or (x_start * 2) % 1 != 0 or x_start < 0 or x_start > 7.5:
        raise ValueError(f"Invalid x_start: {x_start}. Must be 0.0 to 7.5 in 0.5 increments.")
    if not isinstance(x_span, (int, float)) or (x_span * 2) % 1 != 0 or x_span < 0.5 or x_span > 8.0:
        raise ValueError(f"Invalid x_span: {x_span}. Must be 0.5 to 8.0 in 0.5 increments.")
    if x_start + x_span > X_LANES:
        raise ValueError(f"X span overflow: {x_start} + {x_span} > {X_LANES}")

def behtml_core_x_span_to_pct(x_span: float) -> float:
    return x_span * 12.5

def behtml_core_sublane_span_to_pct(sublane_span: int) -> float:
    return sublane_span * 6.25

def behtml_core_y_span_to_px(y_span: int) -> int:
    if not isinstance(y_span, int) or y_span < 1:
        raise ValueError(f"Invalid y_span: {y_span}")
    return y_span * RY_PX

def behtml_core_layer_to_css_zindex(z_layer: int) -> int:
    if not isinstance(z_layer, int) or z_layer < 0:
        raise ValueError(f"Invalid z_layer: {z_layer}")
    return z_layer * Z_LAYER_PX

def behtml_core_control_padding_y(y_span: int) -> dict:
    total_px = behtml_core_y_span_to_px(y_span)
    visual_px = total_px - 4
    return {"total_px": total_px, "visual_px": visual_px, "pad_top_px": 2, "pad_bottom_px": 2}
```

## Error Constants Registry (Core Range: 300-329)

- `301: E_BEHTML_MISSING_ID`
- `303: E_BEHTML_DUPLICATE_ID`
- `305: E_BEHTML_INVALID_X_ADDRESS`
- `306: E_BEHTML_X_SPAN_OVERFLOW`
- `307: E_BEHTML_QUANTIZATION_FAIL`
- `314: E_BEHTML_ELEMENT_NOT_FOUND`
- `315: E_BEHTML_INVALID_CONTENT_KIND`
- `316: E_BEHTML_INVALID_URL`
- `317: E_BEHTML_COLLISION`
- `318: E_BEHTML_INVALID_OPTION_SET_REF`
- `319: E_BEHTML_INVALID_ELEMENT_ID`
- `320: E_BEHTML_CYCLIC_PARENT`
