---
name: behtml-layout-builder
description: Build, compose, and assemble deterministic, production-ready BEHTML page layouts, UI component grids, and 18-field BEHTMLElement entity records adhering strictly to 8-lane X-axis constraints, Ry=32px row quantization, z-layer stacking, transparent production grids, zero filler content, minimal functional section labels, and BECSS Tri-Color standards. Use when generating BEHTML layouts, designing spatial UI templates, constructing 18-field BEHTMLElement datasets, or rendering spatially locked web interfaces. Do NOT use for raw format math (use behtml-format-core), structural validation (use behtml-schema-validator), or web navigation tree mapping (use ui-navigation-decomposer).
---
# BEHTML Layout Builder

Deterministic engine for constructing, composing, and assembling production-ready BEHTML layout templates and BEJSON 104/104a datasets.

## Summary

Builds clean, purposeful, and visually structured web applications using the BEHTML spatially locked layout framework. Enforces the core truth that BEHTML serves the same purpose as standard HTML: building clean, functional, beautiful web applications using an 8-lane X-axis, Ry=32px Y-axis quantization, and native CSS z-index stacking. Guarantees that layout grids remain completely transparent in production outputs, restricts visual depth offsets exclusively to IDE development tools, eliminates all filler/fluff content in favor of strictly functional section placeholder labels, bundles 5 canonical zero-fluff production templates, and enforces the authoritative 18-field BEHTMLElement schema.

## When to Use

- Constructing production BEHTML page layouts, dashboards, and UI component templates.
- Generating authoritative 18-field `BEHTMLElement` entity records in BEJSON 104/104a format.
- Translating UI wireframes into deterministic 8-lane X-axis and 32px quantized Y-axis coordinates.
- Assembling nested container hierarchies, toolbars, modal overlays, and control surfaces.
- Configuring typography overrides (`font_size`, `font_weight`), sliders, and combobox option sets.
- Scaffolding zero-filler, minimal functional placeholder templates adhering to Elton Boehnen's standards.

## When NOT to Use

- Calculating low-level coordinate math or format primitives (use `behtml-format-core`).
- Validating document integrity, drift, or collisions (use `behtml-schema-validator`).
- Mapping site architecture, navigation trees, or route decomposition (use `ui-navigation-decomposer`).
- Scaffolding bare-bones structural wireframe templates without components (use `template-architect`).

## Core Principles and Clarifications

1. **Purpose of BEHTML**:
   - The purpose of BEHTML is identical to standard HTML: to design purposeful, clean, and nice-looking websites or applications.
   - It is a production application framework, not an abstract art display or wireframe showcase.

2. **Transparent Production Grid Law**:
   - The grid exists strictly for development and alignment during construction.
   - In finished websites and applications, the grid MUST be completely transparent.
   - Never render visible grid lines, grid background linear-gradients, or coordinate labels in production output unless debug mode is explicitly enabled.
   - The end user must experience a clean, properly aligned application without visible grid scaffolding.

3. **Production Z-Layer Stacking vs. IDE Depth View**:
   - Standard BEHTML stacks layers cleanly and natively utilizing CSS z-index (`z_layer * 32`).
   - Upper layers (modals, overlays, floating action buttons) block out the view and pointer events of layers beneath them completely, unless an overlay intentionally specifies a semi-transparent backdrop.
   - Visual depth offsets (`translate(32px, 32px)` and 33.3% opacity reductions per layer) are strictly an IDE development inspection view and MUST NEVER appear in standard production templates.

4. **Zero Filler Content and Minimal Functional Placeholders**:
   - Templates and component examples must be completely free of filler content, simulated Latin text (lorem ipsum), fake copywriting, decorative stock graphics, or simulated marketing claims.
   - All placeholders must be strictly minimal, literal, title-cased section labels:
     - Titles / Headers: `"Title"`, `"Section Heading"`, `"Card Title"`, `"Subtitle"`
     - Body Content: `"Body"` or `"Body Paragraph text"`
     - Lists: `"List"` with `"List Item 1"`, `"List Item 2"`
     - Controls / Buttons: `"Action Button"`, `"Submit"`, `"Cancel"`, `"Close"`
     - Status / Badges: `"Badge"`, `"Tag"`, `"Status"`
     - Form Inputs: `"Input Field"`, `"Search text"`

5. **Canonical Production References**:
   - Follow the bundled zero-fluff templates in `assets/` as the standard application architecture: Layer 0 base interface (header, sidebar, metric cards, data table), Layer 1 modal overlay (fixed header, scrollable body container with `overflow-y: auto` and `flex: 1`, fixed footer), and Layer 2 floating controls (toasts, FABs).

## Bundled Canonical Production Templates

The skill bundles 5 production-ready, zero-fluff BEHTML layout templates in `assets/`:

1. `assets/BEHTML_Dashboard_Demonstration.html`: Canonical 3-layer enterprise dashboard featuring a docked control hub, Layer 0 base grid (system header, tree navigation list with `List Item 1` and `List Item 2`, 3 metric cards, and 5-column data table), Layer 1 modal overlay (`Title`, `Tag`, scrollable `Body`, `Cancel`, `Submit`), and Layer 2 floating controls (`Toast`, FAB).
2. `assets/BEHTML_Grid_Visualization_Demonstration.html`: Quantum 2D BEM Grid demonstration showing 8-lane row quantization, red trigger cell, and Layer 2 slide-out drawer (`Title`, `Body`, `Close`).
3. `assets/BEHTML_IDE_Transparency_Layer_Depth.html`: Compact inverted 3-layer architecture (`Title`, `Sidebar`, `Body`, `Toast`, `Badge`, `Action Button`).
4. `assets/BEJSON_Page.html`: Spatially quantized blog/article layout (`Title`, `Badge`, sidebar list with `List Item 1` and `List Item 2`, `Subtitle`, `Title`, `Body`, card grid with `Title` and `Body`, and `Status` HUD).
5. `assets/ZBETML_VIDEO.html`: Tactical cinema media deck with 16:9 primary stage, stream queue list (`List Item 1`, `List Item 2`), scrubber timeline, transport controls, audio rack, telemetry rows, and operator manual modal.

## Core Spatial Laws

1. **X-Axis (8 Lanes: X0 to X7)**:
   - Width is divided into exactly 8 equal lanes (12.5% width per lane).
   - `x_start`: integer from `0` to `7`.
   - `x_span`: integer from `1` to `8`.
   - Invariant: `x_start + x_span <= 8`. Out-of-bounds spans are strictly invalid (`E_BEHTML_X_SPAN_OVERFLOW`, code 306).

2. **Y-Axis (Row Quantization: Ry = 32px)**:
   - `y_start`: integer >= `0` representing row index.
   - `y_span`: integer >= `1` representing row count (multi-row resize supported).
   - Total vertical footprint = `y_span * 32px`.
   - Generalized Padding Law: Padding is applied once per container footprint, not once per row (`visual_height = y_span * 32px - 4px`, with 4px outer padding).
   - Horizontal counterpart: container padding gap applies once per footprint, not per lane.

3. **Z-Axis (Stacking Layers)**:
   - `z_layer`: integer >= `0` (default `0`).
   - CSS z-index conversion = `z_layer * 32`.
   - Collision Rule: Elements collide only if they share identical X/Y bounding space AND the same `z_layer` within the same parent container scope. Different `z_layer` indices do not collide.
   - Keyboard Navigation: Arrow-key focus moves between elements on the current `z_layer` only.

4. **Container Scope and Hierarchy**:
   - `parent_id_fk`: `null` for root canvas elements, or parent `element_id` for nested children.
   - Children coordinates (`x_start`, `y_start`, `x_span`, `y_span`) are local to the parent container's 8-lane grid.
   - Direct self-parenting and cyclic descendant parenting are strictly forbidden (`E_BEHTML_CYCLIC_PARENT`, code 320).

## Standard Element Types and Defaults

| Element Type | Default x_span | Default y_span | Content Kind | Description |
| :--- | :--- | :--- | :--- | :--- |
| `button` | 2 | 1 | `text` | Interactive action button (red-filled `#DE2626`, white text) |
| `input` | 4 | 1 | `text` | Single-line text input (white background, black text/border) |
| `textarea` | 4 | 2 | `text` | Multi-line text field (white background, black text/border) |
| `combobox` | 3 | 1 | `text` | Select dropdown; renders `<option>` tags from referenced `option_set_id` |
| `checkbox` | 1 | 1 | `text` | Binary checkbox toggle (`<input type="checkbox">`) |
| `radio` | 1 | 1 | `text` | Single-select radio option (`<input type="radio">`) |
| `label` | 2 | 1 | `text` | Static typography label |
| `container` | 8 | 2+ | `text` | Structural wrapper holding nested children in its own 8-lane grid |
| `toolbar` | 8 | 1 | `text` | Single-row horizontal control bar holding nested children |
| `slider` | 4 | 1 | `text` | Range slider (`<input type="range">`) configured via min/max/step |

## Supported Content Kinds

- `text`: Plain text string escaped with `html.escape()`.
- `field_binding`: Dynamic template variable placeholder (e.g. `user.display_name`).
- `url`: Valid URI path starting with `https://`, `http://`, or `/`. Javascript schemes are strictly rejected (`E_BEHTML_INVALID_URL`, code 316).
- `asset_ref`: Static asset identifier or image key.

## Authoritative 18-Field BEHTMLElement Schema (Zero-Fluff Reference)

BEHTML entity records are persisted in BEJSON 104 / 104a tabular arrays adhering to the 18-field specification:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Parent_Hierarchy": "../104a.mfdb.bejson",
  "Records_Type": [
    "BEHTMLElement"
  ],
  "Fields": [
    { "name": "element_id", "type": "string" },
    { "name": "element_type", "type": "string" },
    { "name": "y_start", "type": "integer" },
    { "name": "y_span", "type": "integer" },
    { "name": "x_start", "type": "integer" },
    { "name": "x_span", "type": "integer" },
    { "name": "z_layer", "type": "integer" },
    { "name": "bem_modifiers", "type": "string" },
    { "name": "content_ref", "type": "string" },
    { "name": "content_kind", "type": "string" },
    { "name": "parent_id_fk", "type": "string" },
    { "name": "is_active", "type": "boolean" },
    { "name": "option_set_id", "type": "string" },
    { "name": "font_size", "type": "integer" },
    { "name": "font_weight", "type": "string" },
    { "name": "range_min", "type": "integer" },
    { "name": "range_max", "type": "integer" },
    { "name": "range_step", "type": "integer" }
  ],
  "Values": [
    [
      "el_toolbar_01", "toolbar", 0, 1, 0, 8, 0, "", "", "text", null, true, null, null, null, 0, 100, 1
    ],
    [
      "el_label_01", "label", 0, 1, 0, 3, 0, "", "Title", "text", "el_toolbar_01", true, null, 14, "bold", 0, 100, 1
    ],
    [
      "el_slider_01", "slider", 0, 1, 3, 3, 0, "", "", "text", "el_toolbar_01", true, null, null, null, 0, 50, 5
    ],
    [
      "el_btn_01", "button", 0, 1, 6, 2, 0, "", "Action Button", "text", "el_toolbar_01", true, null, null, null, 0, 100, 1
    ]
  ]
}
```

## Reusable Option Sets (Comboboxes)

Option sets live at the project level (`SCHEMA_OPTIONSET_v1`), allowing any number of comboboxes to share reusable dropdown options using functional placeholders:

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

## BECSS Visual Design Standards

- **Tri-Color Palette**:
  - Pure Black (`#000000` / `oklch(15% 0 0)` to `oklch(0% 0 0)`).
  - Pure White (`#FFFFFF`).
  - Strict Red Accent (`#DE2626` / `oklch(58.1% 0.217 27.4)`).
  - Hover Red (`oklch(50% 0.2 27.4)`).
- **Typography**:
  - `Inter` for primary UI text, headers, and navigation.
  - `Roboto Mono` or `Source Code Pro` for tabular data, IDs, and code blocks.
- **Namespacing**:
  - Use `behtml-` prefix for grid elements, cells, and spatial canvas utilities.
  - Use `becss-` prefix for application chrome (headers, breadcrumbs, sidebars, tables).
- **Mobile First Adaptation**:
  - Edge-to-edge canvas width on viewports <= 768px (`padding: 8px 0 0 0`, zero dead margins).
  - Bottom padding cleared for mobile viewports without floating bar overlaps.

## Error Codes and Validation Registry

The Anti-Drift Auditor enforces cross-language validation parity (Python, JS, TS, Bash) across codes 300 to 329:

- `301: E_BEHTML_MISSING_ID` - Missing element_id.
- `303: E_BEHTML_DUPLICATE_ID` - Duplicate element_id within document.
- `305: E_BEHTML_INVALID_X_ADDRESS` - `x_start` outside 0-7 or `x_span` < 1.
- `306: E_BEHTML_X_SPAN_OVERFLOW` - `x_start + x_span > 8`.
- `307: E_BEHTML_QUANTIZATION_FAIL` - Vertical height not multiple of Ry=32px.
- `314: E_BEHTML_ELEMENT_NOT_FOUND` - Target element does not exist.
- `315: E_BEHTML_INVALID_CONTENT_KIND` - Unrecognized content_kind.
- `316: E_BEHTML_INVALID_URL` - URL does not start with `https://`, `http://`, or `/`.
- `317: E_BEHTML_COLLISION` - Element overlaps another on same layer and container scope.
- `318: E_BEHTML_INVALID_OPTION_SET_REF` - Referenced option_set_id does not exist.
- `319: E_BEHTML_INVALID_ELEMENT_ID` - element_id violates `^[A-Za-z0-9_-]+$`.
- `320: E_BEHTML_CYCLIC_PARENT` - Container references itself or one of its descendants.

## Step-by-Step Template Assembly Workflow

1. **Establish Application Hierarchy**:
   - Determine active layers: Layer 0 for base interface, Layer 1 for modals/dialogs, Layer 2 for notifications/FABs.
   - Plan container scopes: root canvas containers (`parent_id_fk: null`), nested child elements.

2. **Calculate 8-Lane Layout and 32px Row Coordinates**:
   - Map elements to integer lanes (`x_start: 0-7`, `x_span: 1-8`, sum <= 8).
   - Quantize heights strictly to integer row counts (`y_span >= 1`).

3. **Configure Element Details with Minimal Section Placeholders**:
   - Assign valid `element_id` matching `^[A-Za-z0-9_-]+$`.
   - Set content using literal section placeholders: `"Title"`, `"Body"`, `"List Item 1"`, `"List Item 2"`, `"Action Button"`.
   - Strictly prohibit lorem ipsum, decorative narratives, and fake metrics.

4. **Verify Collision Freedom and Parent Validity**:
   - Verify no overlapping coordinates among elements sharing the same `parent_id_fk` and `z_layer`.
   - Confirm parent containers exist and form no circular dependencies.

5. **Ensure Transparent Output**:
   - Set grid background and borders transparent for production rendering.
   - Apply clean BECSS Tri-Color styling without visual development scaffolding.

## Common Gotchas to Avoid

- **Filler Content Creep**: Populating templates with fake marketing claims, dummy statistics, or multi-sentence instructions violates the Zero Filler rule. Use `"Title"`, `"Body"`, and `"List Item 1"`.
- **Visible Grid in Production**: Rendering visible grid lines or checkerboard backgrounds in production apps violates the Transparent Production Grid Law.
- **IDE Depth Offsets in Standard Apps**: Translating layers by 32px with opacity decay is an IDE tool feature; real apps stack cleanly with CSS z-index.
- **X-Span Overflow**: Setting `x_start: 5` and `x_span: 4` totals 9, exceeding the 8-lane ceiling.
- **Non-Quantized Heights**: Setting arbitrary pixel heights breaks the `Ry = 32px` quantization invariant.
- **Layer Collision Confusion**: Elements on different `z_layer` indices do not collide even if X/Y coordinates overlap.
- **Dangling Parent References**: Pointing `parent_id_fk` to an ID not in the document corrupts the tree.
- **Unsanitized Element IDs**: Using spaces or symbols in `element_id` breaks CSS selectors and routing.
