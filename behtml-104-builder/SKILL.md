---
name: behtml-104-builder
description: >-
  Build and render Foundational Era vertical domain artifacts using libraries_104 specialized families including BEHTML and BEHTML_IDE tabular markup, Headless CMS/ExpCMS widgets, Diagrams flowcharts, Bookmaker publications, Gaming 2D grids, and Lib_SH AOT Terminal Menus while enforcing Policy 8.1 (#FFFFFF, #000000, #DE2626) visual branding, 8-lane / 16-wide Ry=32px grid geometry, and archetype binding via behtml-templates. Use when building UI/TUI components, CMS views, or diagrams backed by libraries_104 vertical families. Do NOT use for raw BEHTML design preference token specifications (use behtml-design-preferences), instantiating standalone HTML templates or app scaffolds (use behtml-templates), formatting standalone editorial publications (use publication-html-builder), low-level 104/104a/104db record CRUD (use bejson-104-core), 104 schema template binding (use template-104-template), or Format 105 Integrity Era operations (use bejson-105-core).
---

# Skill: `behtml-104-builder` (Layer 4 - Foundational Era Vertical Domain Builder)

- **Version**: `102`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104 Vertical Domains, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `BEHTML (104/104a), CMS/ExpCMS MFDB, Diagrams, Bookmaker, Terminal_Menus`
- **Design Framework Binding**: `behtml-design-preferences`
- **Design Specification**: `behtml-design-preferences/references/behtml_design_preferences_spec.md` (single master copy; per-skill copies removed)
- **Template Library Binding**: `behtml-templates`
- **Date Created**: `2026-10-17` (Updated `2026-10-19`)
- **RELATIONAL_ID**: `a84f2c19-5e3b-4d70-9c15-2b7e6a9d0f42`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`behtml-104-builder` operates at **Layer 4** to compile, transform, and render Foundational Era domain-specific structures into valid BEHTML interfaces, terminal menus, and CMS components using `libraries_104`.

### Bound Canonical Modules:
- `Lib_PY/BEHTML/lib_bejson_BEHTML_core.py & lib_bejson_BEHTML_render.py`
- `Lib_PY/CMS/lib_bejson_CMS_cms_core.py & Lib_PY/ExpCMS/lib_bejson_ExpCMS_widgets.py`
- `Lib_PY/Diagrams/lib_bejson_Diagrams_diagrams_core.py`
- `Lib_PY/Bookmaker/lib_bejson_Bookmaker_bookwriter_core.py`
- `Lib_SH/Terminal_Menus/lib_bejson_TerminalMenus_compiler.sh`

---

## 2. Core Structural & Policy Invariants

1. **Policy 8.1 Visual Palette**: Strictly `#FFFFFF` White, `#000000` Black, and `#DE2626` Vivid Red accent.
2. **Spatial Grid Foundations**: Conforms to `behtml-design-preferences`:
   - 8-lane grid base ($12.5\%$ per column) with **6.25% half-wide cells (0.5 cell units) allowed or 16-wide grids ($16 \times 6.25\% = 100\%$)**.
   - Vertical quantization module: $R_y = 32\text{px}$.
   - **Production Grid Transparency**: The grid is a development scaffold; finished rendered artifacts render cleanly without visible grid cage lines.
3. **Collision & Occupancy Verification**: Execute collision and bounds checking via `lib_bejson_BEHTML_collision.py` prior to compiling HTML markup.
4. **Mandatory Field Map Cache & Boundary Sanitization**: All record reads and writes must strip boundary whitespace (Policy 10.9) and resolve column indices through a dynamic `field_map` (Policy 6.2):

```python
def bejson_read_column(doc: dict, field_map: dict[str, int], row: list, col_name: str):
    clean_col = col_name.strip()
    col_idx = field_map[clean_col]
    val = row[col_idx]
    return val.strip() if isinstance(val, str) else val
```

---

## 3. Template Archetype Binding via `behtml-templates`

When compiling domain artifacts into standalone HTML views, select the appropriate archetype from `behtml-templates` instead of forcing non-document outputs into a document scaffold:

| Domain Output | Target Archetype | Characteristics |
| :--- | :--- | :--- |
| **Technical Telemetry / Governance** | `Template_Document_With_Shelf.html` | 16-sublane stage, Row 1 title bar, 544px canvas, Row 19 buffer, Rows 20..24 widget shelf with 150x150px slots. |
| **Long-form Specs / Bookmaker** | `Template_Document_Widgetless.html` | 16-sublane stage, Row 1 title bar, full vertical canvas without bottom widget shelf. Uninterrupted reading flow. |
| **Headless CMS Portal / Web App** | `Template_Standard_Page.html` | 64px header, brand badge, hamburger toggle, collapsible BEM sidebar drawer, main design surface, card grid, auditor HUD. |
| **ExpCMS Activity / Stream Feeds** | `Template_Feed.html` | Filter pills, modular card stream aligned to 8-lane or 16-sublane geometry, author badges, timestamps, tags, pagination triggers. |
| **Interactive Spatial Consoles** | `Template_Dashboard.html` | Top docked hub, layer depth slider, 8-lane/16-wide canvas, KPI cards, BEJSON data tables, telemetry stream, dev-grid toggle. |

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or CLI verification tools from `behtml-104-builder`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute behtml-104-builder verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `behtml-104-builder` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **BE HTML CSS design preference tokens and dimensional laws**: Redirect immediately to `behtml-design-preferences`.
- **Instantiating standalone HTML templates or scaffolds**: Redirect immediately to `behtml-templates`.
- **Formatting standalone editorial HTML publications**: Redirect immediately to `publication-html-builder`.
- **Low-level BEJSON 104, 104a, or 104db CRUD**: Redirect immediately to `bejson-104-core`.
- **Generating 104 data templates and owning writers**: Redirect immediately to `template-104-template`.
- **Format 105 Integrity Era operations**: Redirect immediately to `bejson-105-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
