---
name: behtml-design-preferences
description: >-
  Enforce the authoritative BEHTML design knowledge, principles, spatial grid mathematics, and visual preferences: Policy 8.1 Tri-Color tokens (#FFFFFF, #000000, #DE2626), 8-lane (12.5%) and 16-wide (6.25%) grid geometry with 0.5-cell half-wide sublanes, Ry=32px vertical row quantization, Z-plane occlusion (layer * 32), transparent production grid rendering (the grid is for development only), viewport lock with dynamic visualViewport height sync, and contained scrollbars. Use when establishing design rules, auditing layout geometry, configuring spatial coordinates, or styling BEHTML components. Do NOT use for instantiating concrete HTML templates or application scaffolds (use behtml-templates), rendering BEJSON 104 vertical domain tables and terminal menus (use behtml-104-builder), or formatting multi-chapter book publications (use publication-html-builder).
---

# Skill: `behtml-design-preferences` (Layer 4 - BEHTML Design Knowledge, Principles & Preferences)

- **Version**: `101`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `104 (Foundational Era - BEHTML Spatial & Visual Design Knowledge, Release 300)`
- **Reference Specification**: `references/behtml_design_preferences_spec.md`
- **Verification Script**: `scripts/verify_behtml_preferences.py`
- **Date Created**: `2026-10-18` (Updated `2026-10-19`)
- **RELATIONAL_ID**: `3c9a71e2-8d4b-4f19-a605-9e2b4d8c1f73`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Core Architectural Clarifications

`behtml-design-preferences` is the authoritative **Layer 4** design knowledge repository for BEHTML. It defines the mathematical foundations, spatial coordinates, color constitution, layering rules, and viewport ergonomics across all BEHTML interfaces.

> [!IMPORTANT]
> ### Crucial Architectural Directives (Ref: `BEHTML-Clarification.md`):
> 1. **Purpose of BEHTML**: The purpose of BEHTML is the same as normal HTML: to design purposeful, ergonomic, and beautiful websites, dashboards, and applications.
> 2. **The Grid is for Development**: A finished website or application must render the grid completely transparent unless debug mode is enabled. The grid is a development scaffold, not an ornamental cage. The final product should be clean and uncluttered.
> 3. **The Document Template is NOT a Global Scaffold**: The 24-row stage with a top title bar, 544px canvas, and 160px bottom widget shelf is **only meant for formal web documents and technical specifications**. Web applications, portals, feeds, and dashboards use their own dedicated archetypes (available in `behtml-templates`).
> 4. **Production Occlusion**: Upper Z-planes block out background layers completely in production. Transparency is reserved for IDE inspection and development debugging.
> 5. **Typography Rule**: When inside narrow single-column (`12.5%`) or half-column (`6.25%`) cells, consider slightly smaller typography (e.g. `10px - 12px`, uppercase mono or compact sans-serif).
> 6. **File Extension**: BEHTML files are standard, valid `.html` files.

---

## 2. Policy §8.1 Tri-Color Visual Constitution

The visual constitution enforces high-contrast, schematic-grade clarity:

| Visual Role | Color Value | Implementation Rule |
| :--- | :--- | :--- |
| **Canvas / Void** | `#000000` or `#FFFFFF` | `#000000` for application voids, dark dashboards, consoles; `#FFFFFF` for light document surfaces and clean web pages. |
| **Foreground / Text** | `#FFFFFF` or `#000000` | Pure white text on dark surfaces; pure black text on light surfaces. |
| **Active Accent** | `#DE2626` | Active resize handles, active nav items, brand badges, table header underlines, primary buttons, status dots. |
| **Muted Metadata** | `#71717a` / `#888888` | Secondary timestamps, tag outlines, null tokens, italic notes. |
| **Borders & Dividers** | `transparent` / `#1a1a1a` / `#333333` | Subtle structural dividers and seamless transparent seams. |

- ❌ **Strict Negative Constraint**: NEVER render black text on a `#DE2626` red background.

---

## 3. Spatial Grid Geometry & Clarifications

### 3.1 8-Lane Base & 16-Wide / 6.25% Sublane Clarification
- **8-Lane Base**: 8 equal lanes of $12.5\%$ width each ($8 \times 12.5\% = 100\%$).
- **6.25% Half-Wide Cells & 16-Wide Grids**:
  - **Half-wide cells ($6.25\%$ width = 0.5 lane)** are officially supported across all BEHTML layouts.
  - A layout may be declared directly as a **16-wide grid** (`grid-template-columns: repeat(16, 1fr)` or `repeat(16, 6.25%)`), or as an 8-lane grid with 0.5-cell sublane resolution.
  - Ideal for side gutters (6.25%), compact metric badges, sidebars (2.5 lanes), and high-density card streams.

### 3.2 Vertical Row Quantization ($R_y = 32\text{px}$)
All vertical dimensions align to integer multiples of $R_y = 32\text{px}$:
- **Header**: $1 \times 32\text{px} = 32\text{px}$ (compact) or $2 \times 32\text{px} = 64\text{px}$ (standard app header).
- **Metric Block**: $3 \times 32\text{px} = 96\text{px}$ or $4 \times 32\text{px} = 128\text{px}$.
- **Data Table / Document Canvas**: $17 \times 32\text{px} = 544\text{px}$ or flexible remaining viewport $1fr$.
- **Widget Shelf**: $5 \times 32\text{px} = 160\text{px}$.

### 3.3 Coordinate System
Elements are structurally defined by 5 coordinates:
`x_start` (0..15), `x_span` (1..16), `y_start` (0..N), `y_span` (1..N), `z_layer` (0..N).

---

## 4. Stacking Planes, Z-Depth & Library Component Stacking

Stacking planes follow the deterministic occlusion formula:
$$\text{z-index} = \text{layer} \times 32$$

- **Layer 1: Base Canvas & Viewport Void (`z-index: 0`)**: The page body, empty root stage, base section header, viewport lock (`100vw × --app-height`), 8-lane (12.5%) or 16-sublane (6.25%) coordinate tracks, and $R_y = 32\text{px}$ row quantization. The development grid renders transparent in production.
- **Layer 2: Surface Content & Interactive Controls (`z-index: 32` - `64`)**: Active work surface and data display: BEJSON tabular viewers, KPI cards, command buttons, fire/toggle switches, filter pills, and form inputs.
- **Layer 3: Contextual Panels & Dialogues (`z-index: 96`)**: Ephemeral interaction planes: modal dialogues, floating dialogue panels, settings flyouts, confirmation sheets, and inspector HUDs. **Production Occlusion**: 100% opaque void background (`#000000` or `#FFFFFF`) completely blocks lower layers without bleed-through or click-through.
- **Layer 4: Persistent Chrome & Global Navigation (`z-index: 128`)**: System-level routing chrome and structural metaphors: collapsible hamburger sidebar drawer, sticky brand badge, top-docked control hub, and auditor HUD.

### 4.1 Library Component Stacking Mechanics
Components templated and generated through specialized ecosystem libraries (`Lib_PY/BEHTML`, `Lib_PY/CMS`, `Lib_PY/Diagrams`) declare a 5-tuple spatial coordinate vector:
$$\mathbf{C} = (x_{\text{start}},\, x_{\text{span}},\, y_{\text{start}},\, y_{\text{span}},\, z_{\text{layer}})$$
Components stack deterministically on top of each other based on their assigned layer through library pipelines, eliminating CSS specificity drift and z-index collisions.

---

## 5. Viewport Lock & Dynamic Height Synchronization

To eliminate mobile address bar jump and horizontal drift:
1. `body { width: 100vw; height: var(--app-height); overflow: hidden; }`
2. Sync `--app-height` via `window.visualViewport`:
   ```javascript
   function syncHeight() {
       if (window.visualViewport) {
           document.documentElement.style.setProperty('--app-height', `${window.visualViewport.height}px`);
       }
   }
   if (window.visualViewport) {
       window.visualViewport.addEventListener('resize', syncHeight);
   }
   syncHeight();
   ```
3. Custom contained scrollbars with transparent tracks and red hover thumbs.

---

## 6. Archetype Ecosystem Reference

To instantiate concrete interfaces, use the dedicated template skill: **`behtml-templates`**:

- **Web Documents**:
  - `Template_Document_With_Shelf.html` (16-sublane stage with 150x150px bottom widget shelf).
  - `Template_Document_Widgetless.html` (Full-canvas document without widget shelf).
  - `Template_Declaration_of_Standardization.html` (Dual-pane pattern catalog & code switcher).
- **Web Applications**:
  - `Template_Standard_Page.html` (64px header, hamburger button, collapsible BEM sidebar drawer, article & card surface, auditor HUD).
  - `Template_Feed.html` (Modular card & news stream with tag filters and author badges).
  - `Template_Dashboard.html` (Tactical dashboard with layer depth slider, 8-lane/16-wide spatial canvas, KPI cards, and data tables).
