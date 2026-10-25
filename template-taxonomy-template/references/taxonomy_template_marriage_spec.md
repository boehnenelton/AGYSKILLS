# The Taxonomy-Template Marriage Specification

> **Parent Skill:** `template-taxonomy-template` (Layer 4 - Presentation & Template Synthesis)  
> **Version:** 1.0.0 | **Release_Version:** 300 | **RELATIONAL_ID:** `d14b8a20-7f3e-4b9c-8e01-2a4c6d8e9f02`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026

---

## 1. Architectural Philosophy: The Marriage

In Elton Boehnen's BEJSON/BEHTML ecosystem, templates and backend taxonomies do not exist as decoupled, drifting layers. They exist as an unbreakable **marriage**:

- **The Taxonomy** provides the ground truth: canonical entity prefixes (`<prefix>_`), semantic suffixes, primary keys, and relational foreign keys (`_fk`).
- **The Template** provides the physical realization: 8-lane / 16-sublane horizontal tracks, $R_y = 32\text{px}$ row quantization, Policy §8.1 Tri-Color tokens (`#000000`, `#FFFFFF`, `#DE2626`), and mathematically deterministic $z\text{-index} = \text{layer} \times 32$ stacking planes.
- **The Marriage** ensures that **every backend field is physically projected into the frontend**, and **every frontend control is backed by an explicit taxonomy field**.

---

## 2. The Zero Unmapped Fields Law

No backend schema field may ever be dropped or unrepresented during template generation. Every field declared in a BEJSON schema's `Fields` array must be mapped to:
1. A **View presentation element** (table column, metric stat box, metadata badge, excerpt container), AND/OR
2. An **Interactive form control** (input box, dropdown selector, checkbox toggle, or textarea editor).

---

## 3. Semantic Suffix Projection Matrix

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

## 4. Four-Layer Stacking Integration

Every married template conforms to the 4-layer stacking plane standard:
- **Layer 1: Base Canvas (`z: 0`)**: 16-sublane coordinate grid, body height lock (`var(--app-height)`), and dynamic `window.visualViewport` synchronization.
- **Layer 2: Surface Content (`z: 32 - 64`)**: High-density data tables, single-record detail cards, and interactive forms.
- **Layer 3: Contextual Panels (`z: 96`)**: Ephemeral dialogue modals, confirmation sheets, and flyouts with 100% solid opaque occlusion.
- **Layer 4: Persistent Chrome (`z: 128`)**: Top-docked 64px header hub, collapsible drawer sidebar, and 32px telemetry strip.

---

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
