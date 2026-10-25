---
name: behtml-document-template
description: >-
  Use when creating formal web documents, specifications, or operational telemetry reports using the canonical BEHTML document templates: Document with Shelf (16-sublane stage, Row 1 32px title bar, Rows 2..18 544px canvas, Row 19 32px buffer, Rows 20..24 160px widget shelf with 150x150px slots), Document Widgetless Variant (full-canvas document for uninterrupted technical reading), and Declaration of Standardization (dual-pane pattern card catalog and code switcher). Use ONLY when creating formal web documents, specifications, or operational telemetry reports. Do NOT use as a global scaffold for general web apps, dashboards, or feeds (use behtml-templates), defining base BEHTML design preferences and grid geometry (use behtml-design-preferences), or rendering vertical domain tables and terminal menus (use behtml-104-builder).
---

# Skill: `behtml-document-template` (Layer 4 - Canonical BEHTML Web Document Templates)

- **Version**: `102`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `104 (Foundational Era - Canonical Web Document Templating, Release 300)`
- **Parent Knowledge Skill**: `behtml-design-preferences`
- **Comprehensive Template Catalog**: `behtml-templates`
- **Canonical Document Assets**:
  - `assets/Template_HTML_Document.html` (Web Document with 150x150px Widget Shelf)
  - `assets/Template_Document_Widgetless.html` (Web Document Widgetless Variant)
  - `assets/Template_Declaration_of_Standardization.html` (Declaration of Standardization)
- **Date Created**: `2026-10-18` (Updated `2026-10-19`)
- **RELATIONAL_ID**: `9c4e1a82-7b3d-4f60-8a15-2d5c9b0e4f73`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Scope Clarification

`behtml-document-template` operates at **Layer 4** specifically for **Web Documents**.

> [!WARNING]
> **Scaffold Scope Restriction**: This skill and its templates are **ONLY** meant for formal web documents, technical specifications, and operational telemetry reports. They are **NOT** a global scaffold for all web tasks. For general web applications, knowledge hubs, card feeds, or tactical dashboards, route directly to `behtml-templates`.

---

## 2. Document Template Variants

### 2.1 Variant A: Document With Widget Shelf (`assets/Template_HTML_Document.html`)
- **Geometry**: 16-sublane horizontal partitioning (Sublane 1: 6.25% left gutter, Sublanes 2..15: 87.5% inner canvas, Sublane 16: 6.25% right gutter).
- **Row 1 (`32px`)**: Title bar spanning `1 / -1` with `border-bottom: 2px solid #DE2626`.
- **Rows 2..18 (`544px`)**: Scrollable document canvas (`display: block`, `overflow-y: auto`). Provided as a clean, bare-bones empty canvas with at most a preset header and metadata bar—zero fake text, zero made-up sections, zero marketing fluff. Ready to deploy and build on immediately.
- **Smashed Text Box Prevention**: Canvas uses `display: block` (not flex) with `pre, textarea, .text-box { min-height: calc(3 * var(--ry-unit)); box-sizing: border-box; }` and `.behtml-doc-canvas > * { flex-shrink: 0; }` to ensure code blocks and text boxes are never squashed into a single row.
- **Row 19 (`32px`)**: Unallocated spatial breathing buffer.
- **Rows 20..24 (`160px`)**: Centered widget shelf with fixed `150px x 150px` widget blocks (`border: 1px solid transparent`, red header underline).
- **Use Case**: Telemetry specifications, hardware readouts, system declarations requiring dedicated telemetry cubes.

### 2.2 Variant B: Document Widgetless (`assets/Template_Document_Widgetless.html`)
- **Geometry**: 16-sublane horizontal partitioning (6.25% side gutters, 87.5% inner canvas).
- **Row 1 (`32px`)**: Title bar spanning `1 / -1`.
- **Rows 2..24 / 1fr**: Full-height scrollable document canvas (`height: calc(var(--app-height) - var(--ry-unit))`, `display: block`). Strict empty scaffold with preset header and author footer—zero filler content.
- **Smashed Text Box Prevention**: Multi-row minimum height (`min-height: calc(3 * var(--ry-unit))`) and block document flow prevent single-row text box collapse.
- **Eliminations**: Omit Row 19 buffer and Rows 20..24 widget shelf.
- **Use Case**: Long-form architectural specifications, research publications, and technical documentation where a bottom widget shelf would obstruct continuous vertical reading.

### 2.3 Variant C: Declaration of Standardization (`assets/Template_Declaration_of_Standardization.html`)
- **Geometry**: Dual-pane split canvas.
- **Components**: Concept idea and nuance pattern cards (`.pattern-card`), interactive multi-file code editor tab strip (`.std-tab-strip`), live line count indicators, and clipboard export tools.
- **Use Case**: Formal system declarations, architectural contracts, and policy enforcement audits.

---

## 3. When NOT to Use

- **Raw BEHTML design preference tokens, color laws, and grid geometry**: Redirect immediately to `behtml-design-preferences`.
- **General Web Applications, Portals, Card Feeds, or Dashboards**: Redirect immediately to `behtml-templates`.
- **Rendering vertical domain tables and terminal menus via libraries_104**: Redirect immediately to `behtml-104-builder`.
- **Multi-chapter book publications**: Redirect immediately to `publication-html-builder`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
