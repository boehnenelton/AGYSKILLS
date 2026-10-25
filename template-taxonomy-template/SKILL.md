---
name: template-taxonomy-template
description: >-
  Materialize, synthesize, and scaffold concrete, production-ready BEHTML template files and UI component surfaces directly married to backend BEJSON entity taxonomies and identifier schemas. Takes a backend schema or taxonomy manifest, couples every declared field (_title, _desc, _metric, _url, _flag, _fk) to its designated presentational slot or interactive control, and outputs deterministic, zero-filler BEHTML files structured into 8-lane / 16-sublane grids with Ry=32px quantization, Policy 8.1 Tri-Color tokens (#000000, #FFFFFF, #DE2626), and z-index = layer * 32 stacking depths. Enforces the Zero Unmapped Fields Law. Use when scaffolding concrete BEHTML template files directly married to backend data taxonomies, generating zero-filler views and forms with 100% field coverage, or materializing template suites planned by template-tax-composer. Do NOT use for planning site-wide multi-template architectures (use template-tax-composer), deriving backend taxonomies from UI trees (use taxonomy-template-taxonomy), or low-level coordinate math (use behtml-format-core).
---

# Skill: `template-taxonomy-template` (Layer 4 - Taxonomy-to-Template Physical Marriage)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `Universal (BEHTML Presentation & BEJSON Taxonomy Marriage)`
- **Reference Specification**: `references/taxonomy_template_marriage_spec.md`
- **Bundled Execution Tool**: `scripts/marry_taxonomy_to_template.py`
- **Example Asset**: `assets/starter_married_template.html`
- **Date Created**: `2026-10-24`
- **RELATIONAL_ID**: `a82d1c40-4e3b-4a9c-b10f-8d0a7e6b5c32`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Purpose: "The Marriage"

`template-taxonomy-template` operates at **Layer 4** as the physical realization engine that marries backend data taxonomies directly into concrete frontend BEHTML template files.

In this architecture, templates never float free from their data schemas:
1. **Unbreakable Coupling**: Every template component exists as the physical manifestation of an underlying backend taxonomy entity.
2. **The Zero Unmapped Fields Law**: No backend schema field is ever omitted. Every field declared in a BEJSON schema's `Fields` array is mapped to either a presentational readout slot (table column, stat box, metadata pill) or an interactive form control (input field, dropdown selector, toggle switch, textarea).
3. **Spatial Determinism**: All generated markup adheres strictly to 8-lane ($12.5\%$) or 16-sublane ($6.25\%$) grid tracks, $R_y = 32\text{px}$ row quantization, Policy §8.1 Tri-Color visual linguistics (`#000000`, `#FFFFFF`, `#DE2626`), and $\text{z-index} = \text{layer} \times 32$ stacking planes.

---

## 2. Bidirectional Architectural Pair

`template-taxonomy-template` forms a symmetrical, bidirectional pair with `taxonomy-template-taxonomy`:

```
┌─────────────────────────────────┐
│ Backend Data Taxonomy / Schemas │
└─────────────────────────────────┘
      ▲                     │
      │                     │  template-taxonomy-template
      │                     │  (Taxonomy ──> Template)
      │                     ▼
┌─────────────────────────────────┐
│ Frontend BEHTML Template Suites │
└─────────────────────────────────┘
      ▲                     │
      │  taxonomy-template-taxonomy
      │  (Template ──> Taxonomy)
      │                     │
      └─────────────────────┘
```

- **`template-taxonomy-template`** (Domain: `template`): Ingests backend taxonomies and synthesizes production BEHTML templates with zero unmapped fields.
- **`taxonomy-template-taxonomy`** (Domain: `taxonomy`): Ingests abstract UI layouts/templates and derives canonical backend data taxonomies, entity prefixes, and BEJSON schemas.

---

## 3. Semantic Projection Matrix

| Semantic Suffix | Data Type | Married Presentation Slot | Married Form Control |
|---|---|---|---|
| `*_id`, `*_uuid` | `string` | Monospace ID Badge (`color: #71717a`) | Read-Only Identifier Input Field |
| `*_fk` | `string` | Relational Target Link Badge (`#DE2626`) | Foreign Key Dropdown Selector / Modal Picker |
| `*_title`, `*_name` | `string` | Card Header Title (`<h3>`, `#FFFFFF`) | Standard Text Input Field |
| `*_desc`, `*_content` | `string` | Prose Body Excerpt Container | Multi-Line Textarea Editor |
| `*_metric`, `*_count` | `int`/`number` | KPI Metric Stat Block (Red left border) | Monospace Numeric Input Field |
| `*_flag`, `is_*` | `boolean` | High-Contrast Status Pill (`#DE2626`) | Checkbox Toggle Switch |
| `*_url`, `*_link` | `string` | External Hyperlink Action (`target="_blank"`) | URL Input Field |
| `*_timestamp`, `*_at` | `string` | Monospace UTC Timestamp Readout | Native Datetime Picker Input Field |

---

## 4. Bundled CLI Tooling

Use [`scripts/marry_taxonomy_to_template.py`](./scripts/marry_taxonomy_to_template.py) to compile any backend schema into a production-ready, married BEHTML template:

```bash
python3 scripts/marry_taxonomy_to_template.py path/to/entity.bejson --output templates/entity_template.html
```

---

## 5. When to Use & When NOT to Use

### Use When:
- Scaffolding concrete BEHTML template files directly married to backend BEJSON schemas or entity taxonomies.
- Generating zero-filler view presentations (data tables, KPI cards, bylines, feeds) and form controls (inputs, dropdowns, toggles, textareas) with 100% field coverage.
- Enforcing the **Zero Unmapped Fields Law** between backend data definitions and frontend templates.
- Materializing templates planned by `template-tax-composer` into real, valid `.html` files.

### Do NOT Use For:
- Planning site-wide multi-template architectures or blueprinting required template suites $\rightarrow$ Use [`template-tax-composer`](../template-tax-composer/SKILL.md).
- Deriving backend data models from existing frontend UI trees $\rightarrow$ Use [`taxonomy-template-taxonomy`](../taxonomy-template-taxonomy/SKILL.md).
- Generating backend BEJSON 104 data stores or owning writer scripts $\rightarrow$ Use [`template-104-template`](../template-104-template/SKILL.md).
- Generating backend BEJSON 105 UUID-tracked data stores $\rightarrow$ Use [`template-105-template`](../template-105-template/SKILL.md).
- Low-level 8-lane / Ry=32px coordinate math $\rightarrow$ Use [`behtml-format-core`](../behtml-format-core/SKILL.md).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
