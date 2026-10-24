---
name: web-ui-component-mapper
description: >-
  Extract, structure, and map complete component-level interface hierarchies of web applications, CMS platforms, admin portals, and dashboards into clean, database-agnostic ASCII tree maps from entry surfaces down to atomic controls. Use when analyzing existing web apps, mapping UI component trees, auditing interface surfaces for feature parity, generating hierarchical ASCII component blueprints, or preparing frontend structural specs. Do NOT use for tracing URL routing paths or sitemaps (use ui-navigation-decomposer), quantizing elements into 8-lane Ry=32px grids (use behtml-design-preferences), scaffolding zero-filler template code (use template-literal-skeleton), or modeling database schemas and table columns (use component-taxonomy-architect).
---

# Skill: `web-ui-component-mapper` (Layer 4 - Web UI Component Architecture Mapping)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `Universal (Component Architecture Analysis)`
- **Reference Specification**: `references/component_mapping_spec.md`
- **Verification Tool**: `scripts/verify_component_map.py`
- **Example Asset**: `assets/example_component_map.txt`
- **Date Created**: `2026-10-19`
- **RELATIONAL_ID**: `b7e2091a-3c4d-5e6f-8a1b-9c8d7e6f5a4b`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Architectural Scope

`web-ui-component-mapper` establishes a deterministic analytical framework for extracting, structuring, and mapping the complete component-level architecture and interface hierarchy of web applications, content management systems (CMS), admin portals, and interactive dashboards.

It acts as the component architecture counterpart to navigation analysis: while routing decomposers focus on URL paths, sitemaps, and spatial coordinate grids, the component mapper abstracts user interfaces into pure structural and functional hierarchies. It details every screen section, toolbar, input element, selector, modal, data table, and confirmation control without entangling the output in database fields, API schemas, or storage implementation details. This produces portable architectural blueprints that can be transferred across different backends, data models, or naming taxonomies.

---

## 2. Core Five-Tier Architectural Hierarchy

Every mapped interface follows a strict five-tier top-down cascade:

1. **Tier 1: Entry Surface / Application File**: The primary host file, view blueprint, or route module that initializes the interface (e.g., `App_Admin.py`, `Editor_Workspace.html`).
2. **Tier 2: Functional Module / Surface Zone**: The high-level functional domain or workspace (e.g., `Content Management`, `Media Library`, `Site Configuration`, `Publisher Engine`).
3. **Tier 3: View Container / Section Card**: Specific screens, view tabs, modals, or distinct visual cards (e.g., `Pages Manager`, `Article Editor Form`, `Bulk Action Drawer`).
4. **Tier 4: Component Group / Toolbar**: Functional groupings of related controls (e.g., `Metadata Bar`, `Text Formatting Toolbar`, `Search Bar`, `Table Row Header`).
5. **Tier 5: Atomic Control / Interactive Action**: Individual leaf elements with defined interaction roles (e.g., `Title Input Box`, `Category Dropdown Selector`, `Upload File Button`, `Save Changes Confirm Button`).

---

## 3. Standard Component Nomenclature

Use consistent, descriptive, non-technical terminology across all tree nodes:

| Component Category | Normalized Label | Example Elements |
| :--- | :--- | :--- |
| **Containers** | `[SECTION]`, `[PANEL]`, `[CARD]`, `[DRAWER]` | System Overview Card, Edit Panel, Details Drawer |
| **Toolbars** | `[TOOLBAR]`, `[ACTION BAR]` | Editor Formatting Toolbar, Bulk Operations Bar |
| **Inputs** | `Input Box`, `Textarea Editor`, `Search Input` | Title Input Box, Body Textarea, Filter Input Box |
| **Selectors** | `Dropdown Selector`, `Radio Group`, `Checkbox Toggle` | Category Dropdown Selector, Status Toggle |
| **Modals** | `Modal Overlay`, `Dialog Window` | Asset Picker Modal, Embed YouTube Dialog |
| **Tables / Lists** | `Data Table`, `Card Grid`, `Collapsible List` | Pages Data Table, Media Grid, Asset Row |
| **Actions** | `Button`, `Confirm Action`, `Shortcut Link` | Save Changes Button, Delete Action Button, Export Link |

---

## 4. Mapping Workflow (5-Step Process)

1. **Step 1: Entry Surface Discovery**: Identify the top-level application file, view route, or entry script that serves the user interface. Establish this as the root of the tree map.
2. **Step 2: Functional Domain Partitioning**: Segment the interface into its major functional modules and workspaces (e.g., Dashboard metrics, Content authoring, Media assets, System maintenance).
3. **Step 3: Container and Section Identification**: Catalog distinct visual containers (cards, stat displays, tab panels, form containers, drawers).
4. **Step 4: Component and Control Enumeration**: Drill down into each container to list all interactive controls grouped by functional clusters (inputs, dropdowns, buttons, tables, dialogs).
5. **Step 5: Abstract Tree Synthesis**: Assemble findings into a clear, nested ASCII tree diagram.

---

## 5. Deliverable Format: Clean ASCII Tree Map

All component mappings must follow this structural template:

```text
APPLICATION ENTRY POINT (File_Name.ext)
|
+-- [SECTION] Module / Domain Name
|   +-- [CARD] Container / Panel Name
|   |   +-- Metric Readout / Display Title
|   |   +-- [TOOLBAR] Control Bar Name
|   |   |   +-- Primary Action Button
|   |   |   +-- Search / Filter Input Box
|   |   +-- Data Table / Collection Grid
|   |       +-- Column: Identifier / Name Display
|   |       +-- Column: Status / Category Badge
|   |       +-- Column: Inline Actions Group (Edit Button, Delete Action Button)
|   |
|   +-- [SECTION] Sub-Feature or Editor Form
|   |   +-- Input Group: Metadata Controls
|   |   |   +-- Title Input Box
|   |   |   +-- Classification Dropdown Selector
|   |   |   +-- Attribution Dropdown Selector
|   |   +-- Input Group: Content Canvas
|   |   |   +-- Formatting Toolbar (Heading Buttons, Bold Button, Link Button)
|   |   |   +-- Modal Trigger Button (Open Asset Picker)
|   |   |   +-- Main Body Textarea Editor
|   |   +-- Modal: Asset Picker Overlay
|   |   |   +-- Source Switcher Tabs
|   |   |   +-- Asset Thumbnail Grid
|   |   |   +-- Selection Confirm Button
|   |   +-- Action Footer (Save Changes Confirm Button, Cancel Button)
|   |
|   +-- [SECTION] Operations & Overlays
|       +-- Confirmation Dialog (Warning Banner, Text Confirmation Input Box, Execute Action Button)
```

---

## 6. Gotchas & Anti-Patterns

- **Never Leak Backend Specifics**: Avoid database field names, column definitions, SQL queries, or internal storage formats. Describe what the user sees and interacts with (e.g., `Category Dropdown Selector`, not `page_cat_name foreign key`).
- **Never Produce Shallow Link Lists**: Do not stop at high-level navigation links. Map down to the form inputs, toolbars, buttons, and modal dialogs inside each view.
- **Maintain Top-Down Continuity**: Always start from the primary interface file or component and branch downward hierarchically.
- **Preserve Conceptual Portability**: Ensure that another developer could read the map and implement the exact same UI on an entirely different database, framework, or architecture.

---

## 7. Automated Audit Tool

Validate generated ASCII component maps using [`scripts/verify_component_map.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-ui-component-mapper/scripts/verify_component_map.py):

```bash
python3 scripts/verify_component_map.py <path_to_component_map.txt>
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
