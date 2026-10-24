# BEHTML Design Preferences & Spatial Architecture Specification

> **Parent Skill:** `behtml-design-preferences` (Layer 4 - Knowledge, Principles & Preferences)  
> **Version:** 101 | **Release_Version:** 300 | **RELATIONAL_ID:** `6a1b9c43-2d8e-4f01-9c74-8b5a2e3f1d90`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026 (Consolidated Master Spec)

---

## 1. Core Philosophy & Fundamental Clarifications

*Ref: `BEHTML-Clarification.md` & `BEHTML2 Architecture Master Spec`*

### 1.1 The Purpose of BEHTML
The purpose of BEHTML is the same as normal HTML: to design purposeful, ergonomic, and beautiful websites, dashboards, and applications. It replaces free-drag layout slop and brittle nested flex drift with a mathematically deterministic spatial coordinate system.

### 1.2 The Grid is for Development; Transparent in Production
- **The grid is a development scaffold.** An IDE or developer debugging session may enable debug mode to render grid lines and coordinate boundaries.
- **Finished websites and production applications must render the grid completely transparent.** The final deployed user experience is clean, uncluttered, and seamless; the user should have no idea there is even a grid.
- Border outlines on components should be subtle, transparent, or purposeful—never an abrasive grid cage.

### 1.3 Depth & Layering: Production Occlusion vs. IDE Transparency
- In production applications, upper Z-planes (`z-layer-1`, `z-layer-2`) **block out background layers completely**, preventing click-through and visual noise.
- Transparency is utilized exclusively in IDEs and inspection tooling as depth indicators to inspect underlying planes during design.

### 1.4 File Format & Extensions
BEHTML files are standard, valid `.html` documents containing clean semantic HTML, CSS custom properties, and optional vanilla JavaScript.

### 1.5 Typography & Spatial Sizing Rule
- When rendering content inside narrow single-column (`12.5%`) or half-wide (`6.25%`) cells, **always consider slightly smaller typography** (e.g. `10px - 12px`, uppercase monospace or compact sans-serif) to maintain proportion and eliminate awkward text wrapping.

---

## 2. Policy §8.1 Tri-Color Visual Constitution

BEHTML interfaces enforce a strict, schematic-grade visual palette engineered for maximum contrast, legibility, and architectural authority.

| Visual Role | Hex Value | Application & Purpose |
| :--- | :--- | :--- |
| **Canvas / Background** | `#000000` or `#FFFFFF` | `#000000` (Dark Mode / Infinite Spatial Void for dashboards, feeds, consoles) or `#FFFFFF` (Light Mode / Document Canvas for web specs, reports). |
| **Primary Text / Frames** | `#FFFFFF` or `#000000` | High-contrast foreground text, primary readouts, hard borders, and structural framing. |
| **Active / Accent Highlight** | `#DE2626` | Vivid red active selection handles, brand badges, table header underlines, primary buttons, status dots, and live playheads. |
| **Muted Metadata** | `#71717a` / `#888888` | Secondary timestamps, author null tokens, tag outlines, breadcrumb trails, and subtle captions. |
| **Structural Dividers** | `#1a1a1a` / `#262626` / `#e5e5e5` | Subtle cell borders and horizontal rules separating content without drawing excessive attention. |

### Contrast Laws & Negative Constraints:
- ✅ **Permitted**: White text on black/dark surfaces; black text on white/light surfaces; white text on `#DE2626` red elements; `#DE2626` red accents on black or white.
- ❌ **Strictly Forbidden**: Black text on a red background (severe contrast degradation and eye strain).

---

## 3. Spatial Grid Foundations & Geometry

### 3.1 Horizontal Grid Geometry: 8-Lane Base & 16-Wide / 6.25% Clarification
The BEHTML horizontal matrix is partitioned as follows:
- **Standard 8-Lane Grid**: 8 uniform lanes of $12.5\%$ width each ($8 \times 12.5\% = 100\%$).
- **CLARIFICATION: 6.25% Half-Wide Cells & 16-Wide Grids**:
  - **Half-wide cells ($6.25\%$ width = 0.5 lane)** are officially supported and standard across all BEHTML layouts.
  - A layout may be declared directly as a **16-wide grid** (`grid-template-columns: repeat(16, 1fr)` or `repeat(16, 6.25%)`), or as an 8-lane grid with 0.5-cell sublane resolution.
  - Enables granular sidebars (e.g., 2.5 lanes), compact metric badges, side gutters (6.25%), and high-density card streams.

```css
/* Standard 8-Lane Container */
.behtml-grid-8 {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-auto-rows: 32px;
}

/* 16-Wide High-Precision Container */
.behtml-grid-16 {
    display: grid;
    grid-template-columns: repeat(16, 1fr);
    grid-auto-rows: 32px;
}
```

### 3.2 Vertical Row Quantization ($R_y = 32\text{px}$)
- The fundamental vertical unit of BEHTML is **$R_y = 32\text{px}$**.
- All block heights, headers, spacers, and card containers align to integer multiples of $32\text{px}$:
  - Header: $1 \times R_y = 32\text{px}$ (compact) or $2 \times R_y = 64\text{px}$ (standard app header).
  - Metric Card: $3 \times R_y = 96\text{px}$ or $4 \times R_y = 128\text{px}$.
  - Data Table / Main Canvas: $17 \times R_y = 544px$ or full remaining viewport $1fr$.
  - Spatial Buffer: $1 \times R_y = 32\text{px}$.
  - Widget Shelf: $5 \times R_y = 160\text{px}$.

### 3.3 Spatial Coordinates
Every placed element is defined by deterministic bounding coordinates:
- `x_start`: Horizontal starting lane index.
- `x_span`: Number of lanes/sublanes spanned.
- `y_start`: Vertical starting row index.
- `y_span`: Number of vertical $R_y$ modules spanned.
- `z_layer`: Vertical stacking plane.

---

## 4. Stacking Planes, Z-Depth Architecture & Library Component Stacking

Stacking planes follow the deterministic formula:
$$\text{z-index} = \text{layer} \times 32$$

| Layer Identifier | Z-Index | Operational Role | Representative Components | Production Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1 (`z-layer-1`)** | `0` | Base Canvas & Structural Void | Page body container, empty root stage, base section header, viewport lock (`100vw × --app-height`), 8-lane/16-sublane coordinate matrix, $R_y = 32\text{px}$ row tracks. | Foundation layout. Development grid lines render completely transparent in production. |
| **Layer 2 (`z-layer-2`)** | `32` - `64` | Surface Content & Interactive Controls | Page content blocks, BEJSON tabular data viewers, KPI metric cards, command buttons, operational fire/toggle switches, toolbars, form inputs. | Active work surface. Snapped to $(x_{\text{start}}, x_{\text{span}}, y_{\text{start}}, y_{\text{span}})$ coordinate bounds. |
| **Layer 3 (`z-layer-3`)** | `96` | Contextual Panels & Ephemeral Dialogues | Modal dialogues, floating dialogue cards, configuration drawers, confirmation sheets, inspector HUDs. | **Production Occlusion**: 100% opaque void background (`#000000` or `#FFFFFF`) completely blocks lower layers without bleed-through or click-through. |
| **Layer 4 (`z-layer-4`)** | `128` | Persistent Chrome & Navigation Metaphors | Collapsible hamburger sidebar drawer, sticky brand badge, top-docked control hub, live status indicators. | Highest persistent system chrome. Drawer occludes content when expanded. |

*Note: In IDE/development modes only, depth inspection overlays may apply partial opacity (e.g. `rgba(255,255,255,0.15)`) or layer sliders to inspect underlying layers simultaneously.*

### 4.1 Library Component Stacking Mechanics
Components templated and generated through specialized ecosystem libraries (`Lib_PY/BEHTML`, `Lib_PY/CMS`, `Lib_PY/Diagrams`, `Lib_SH/Terminal_Menus`) declare a standardized 5-tuple spatial coordinate vector:

$$\mathbf{C} = (x_{\text{start}},\, x_{\text{span}},\, y_{\text{start}},\, y_{\text{span}},\, z_{\text{layer}})$$

- **$x$ Coordinates**: Restrained to 8 lanes ($12.5\%$ per lane) or 16 sublanes ($6.25\%$ per half-cell).
- **$y$ Coordinates**: Quantized to integer multiples of $R_y = 32\text{px}$ (`32px`, `64px`, `96px`, `128px`, `160px`).
- **$z$ Coordinates**: Integer layer assignment ($1, 2, 3, 4$). Lower layers never bleed through higher layers because each upper-layer container has a solid opaque background token matching Policy §8.1 (`#000000` or `#FFFFFF`).
- **Library Decoupling**: Components are built and tested as modular library units and stacked deterministically on top of each other, preventing CSS specificity drift and z-index collisions.

---

## 5. Viewport Lock & Dynamic Height Synchronization

To eliminate mobile browser address bar jump, rubber-band bounce, and horizontal layout drift:
1. **Window Scroll Lock**:
   ```css
   body {
       width: 100vw;
       height: var(--app-height);
       overflow: hidden;
       -webkit-font-smoothing: antialiased;
   }
   ```
2. **Dynamic Height Synchronization**:
   ```javascript
   function syncCanvasHeight() {
       if (window.visualViewport) {
           document.documentElement.style.setProperty('--app-height', `${window.visualViewport.height}px`);
       }
   }
   if (window.visualViewport) {
       window.visualViewport.addEventListener('resize', syncCanvasHeight);
   }
   syncCanvasHeight();
   ```
3. **Contained Scrollbars**:
   ```css
   ::-webkit-scrollbar { width: 5px; height: 5px; }
   ::-webkit-scrollbar-track { background: transparent; }
   ::-webkit-scrollbar-thumb { background: #333333; border-radius: 2px; }
   ::-webkit-scrollbar-thumb:hover { background: #DE2626; }
   ```

---

## 6. Archetype Taxonomy & Exemplar Decoupling

BEHTML does **NOT** force all web tasks into a single document scaffold. Templates are provided as **flexible starting examples** across distinct UI archetypes:

```
                          ┌────────────────────────┐
                          │ behtml-design-pref-    │
                          │ erences (Knowledge/L4) │
                          └───────────┬────────────┘
                                      │ Enforces Grid & Constitution
             ┌────────────────────────┴────────────────────────┐
             ▼                                                 ▼
┌─────────────────────────┐                       ┌─────────────────────────┐
│     Web Documents       │                       │    Web Applications     │
├─────────────────────────┤                       ├─────────────────────────┤
│ • Document (With Shelf) │                       │ • Standard Page (Web)   │
│ • Document Widgetless   │                       │ • Card & News Feed      │
│ • Declaration Standard  │                       │ • Tactical Dashboard    │
└─────────────────────────┘                       └─────────────────────────┘
```

1. **Formal Web Document (With Shelf)**: 16-sublane stage (6.25% gutters, 87.5% canvas), Row 1 (32px) title bar, Rows 2..18 (544px) scroll canvas, Row 19 (32px) buffer, Rows 20..24 (160px) shelf with 150x150px widget slots.
2. **Web Document (Widgetless Variant)**: 16-sublane stage, Row 1 (32px) title bar, Rows 2..24 full-height scrollable canvas without bottom shelf or Row 19 buffer. Ideal for continuous technical reading.
3. **Standard Page**: 64px header ($2 \times 32\text{px}$), brand badge, hamburger toggle, collapsible BEM sidebar drawer (300px), expansive design surface with article typography, modular card grid, and Auditor HUD.
4. **Feed Stream**: Top control hub, category/tag filter pills, multi-column card stream aligned to 8-lane or 16-sublane geometry, author badges, timestamps, tags, and pagination triggers.
5. **Tactical Dashboard**: Top docked control hub with layer depth slider, 8-lane or 16-wide spatial canvas, multi-layer Z-stacking planes, metric KPI cards, BEJSON data tables, and telemetry monitors.
