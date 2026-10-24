---
name: taxonomy-ui-component-architect
description: >-
  Synthesize, generate, and map comprehensive, optimized UI component architectures and interface tree maps directly from backend data taxonomies, entity schemas, and identifier specifications. Ingests canonical entity prefix registries, field names with semantic suffixes (_title, _url, _metric, _flag, _fk), and relational models, then projects them into complete front-end component hierarchies comprising host applications, management panels, data tables, form inputs, toolbars, embed modals, and confirm actions with zero unmapped schema fields. Use when taking a database schema, data taxonomy, or BEJSON specification and designing the user interface, admin dashboard, or component map to manage it. Do NOT use for analyzing existing UI code into taxonomies (use component-taxonomy-architect), raw UI mapping without schemas (use web-ui-component-mapper), or spatial coordinate quantization (use behtml-design-preferences).
---

# Skill: `taxonomy-ui-component-architect` (Layer 5 - Schema-to-UI Component Architecture Projection)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (L3_Use_Cases_Cross_Layer_Blueprinting)`
- **Era & Library Binding**: `Universal (Cross-Layer Schema-to-UI Architecture)`
- **Reference Specification**: `references/schema_to_ui_projection_spec.md`
- **Projection Tool**: `scripts/project_schema_to_ui.py`
- **Example Asset**: `assets/projected_component_map.txt`
- **Date Created**: `2026-10-19`
- **RELATIONAL_ID**: `5b2c7e91-4d3f-5a8b-1e0c-8f9a7d6c5b4e`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Architectural Scope

`taxonomy-ui-component-architect` provides the deterministic projection pipeline to synthesize, generate, and map comprehensive, optimized UI component architectures and ASCII component tree maps directly from backend data taxonomies, BEJSON schemas, and entity registries.

It ingests canonical entity prefix registries, field names with semantic suffixes (`_title`, `_url`, `_metric`, `_flag`, `_fk`), and relational models, then projects them into complete front-end component hierarchies comprising host applications, management panels, data tables, form inputs, toolbars, embed modals, and confirm actions with **zero unmapped schema fields**.

---

## 2. Core Five-Tier Architectural Projection

Every mapped interface follows a strict five-tier top-down cascade conforming to the component standard:

1. **Tier 1: Entry Surface / Application File**: The primary host file or route module derived from the owning writer module (e.g., `App_Admin.py`, `Editor_Workspace.html`).
2. **Tier 2: Functional Module / Surface Zone**: High-level domain corresponding to each entity (e.g., `[SECTION] Page Management`, `[SECTION] Media Asset Library`).
3. **Tier 3: View Container / Section Card**: Distinct visual containers:
   - `[CARD] <Entity> Directory Panel` (Collection table, stat readouts, search bar)
   - `[SECTION] <Entity> Editor Form` (Input canvas and control clusters)
   - `Modal: <Target> Picker Overlay` (Foreign key selector dialogs)
4. **Tier 4: Component Group / Toolbar**: Groupings of related controls:
   - `[TOOLBAR] Table Action Bar` (Search filter, Create action button)
   - `Input Group: Metadata Controls` (Headers, selectors, toggles)
   - `Input Group: Content Canvas` (Formatting action bars, textareas)
5. **Tier 5: Atomic Control / Interactive Action**: Leaf interaction elements:
   - Input Boxes, Dropdown Selectors, Checkbox Toggles, Confirm Action Buttons.

---

## 3. Semantic Projection Matrix

| Schema Pattern | Field Type | View Placement | Form / Interactive Placement |
| :--- | :--- | :--- | :--- |
| `*_id`, `*_uuid` | `string` | `Column: <Name> Display` | `<Name> Identifier Badge (Read-only)` |
| `*_title`, `*_name` | `string` | `Column: <Name> Display` | `<Name> Input Box` |
| `*_desc`, `*_content` | `string` | `Content Snippet: <Name> Excerpt` | `<Name> Textarea Editor` + Formatting Bar |
| `*_fk` | `string` | `Column: <Target> Link Badge` | `<Target> Dropdown Selector` / Modal Picker |
| `*_flag`, `is_*` | `boolean` | `Column: <Name> Status Badge` | `<Name> Checkbox Toggle` |
| `*_status`, `*_type` | `string` | `Column: <Name> Status Badge` | `<Name> Dropdown Selector` |
| `*_count`, `*_metric` | `int`/`number`| `Metric Readout: <Name> Display` | `<Name> Number Input Box` |
| `*_url`, `*_link` | `string` | `Column: <Name> Shortcut Link` | `<Name> URL Input Box` |
| `*_created_at` | `string` | `Column: <Name> Timestamp Readout`| `<Name> Date Picker Input Box` |

---

## 4. The Zero Unmapped Fields Law

No backend field may be dropped or forgotten during projection. Every field declared in a BEJSON schema's `Fields` array must be mapped to either:
1. A **View presentation element** (table column, metric stat, or metadata badge), AND/OR
2. An **Interactive form control** (input box, dropdown, toggle, or textarea).

---

## 5. Automated Projection Tool

Run [`scripts/project_schema_to_ui.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/taxonomy-ui-component-architect/scripts/project_schema_to_ui.py) to synthesize component maps from schemas:

```bash
python3 scripts/project_schema_to_ui.py <path_to_schema.bejson> --entry-point App_Admin.py --output component_map.txt
```

### 5.1 Pre-Packaged MTV Domain Blueprints

Four pre-packaged domain blueprints are bundled under [`blueprints/`](file:///data/data/com.termux/files/home/.gemini/config/skills/taxonomy-ui-component-architect/blueprints/) (see [`references/mtv_domain_blueprints_spec.md`](file:///data/data/com.termux/files/home/.gemini/config/skills/taxonomy-ui-component-architect/references/mtv_domain_blueprints_spec.md)):
1. `documentation`: Technical Documentation & E-Book Compendium (`cat_`, `doc_`, `spec_`).
2. `editorial`: Editorial Multi-Author Publication (`cat_`, `author_`, `page_`).
3. `portfolio`: Creative Portfolio & Digital Showcase (`cat_`, `project_`, `asset_`).
4. `video_hub`: Video Hub & Streaming Archive (`cat_`, `extmedia_`, `playlist_`).


---

## 6. Boundary Rules & Negative Guardrails

- **Do NOT** analyze existing UI code into backend data schemas $\rightarrow$ Use [`component-taxonomy-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/component-taxonomy-architect/SKILL.md).
- **Do NOT** map user interfaces without a backend schema $\rightarrow$ Use [`web-ui-component-mapper`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-ui-component-mapper/SKILL.md).
- **Do NOT** quantize elements into 8-lane Ry=32px spatial coordinate grids $\rightarrow$ Use [`behtml-design-preferences`](file:///data/data/com.termux/files/home/.gemini/config/skills/behtml-design-preferences/SKILL.md).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
