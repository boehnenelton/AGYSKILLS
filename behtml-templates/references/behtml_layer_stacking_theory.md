# BEHTML Multi-Layer Stacking Theory & Component Assembly

* Parent Skill: `behtml-templates`
* Reference Framework: `behtml-design-preferences`
* Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
* Effective Date: October 2026

---

## 1. Architectural Stacking Paradigm

BEHTML replaces uncontrolled CSS cascading floats and arbitrary `z-index` layering with mathematically deterministic stacking planes:

$$\text{z-index} = \text{layer} \times 32$$

```
================================================================================
 LAYER 4: PERSISTENT CHROME & NAVIGATION (z-index: 128)
 Collapsible Hamburger Drawer Sidebar · Brand Badge · Top Docked Hub · Auditor HUD
================================================================================
          │ (Occludes Layer 3, 2, 1 when expanded)
          ▼
================================================================================
 LAYER 3: CONTEXTUAL PANELS & EPHEMERAL DIALOGUES (z-index: 96)
 Floating Modals · Dialogue Cards · Settings Flyouts · Confirmation Sheets
================================================================================
          │ (Production Occlusion: 100% opaque void blocks lower layers)
          ▼
================================================================================
 LAYER 2: SURFACE CONTENT & INTERACTIVE CONTROLS (z-index: 32 - 64)
 BEJSON Data Tables · KPI Metric Cards · Buttons · Fire Switches · Form Inputs
================================================================================
          │ (Positioned in 8-lane or 16-sublane coordinate cells)
          ▼
================================================================================
 LAYER 1: BASE CANVAS & STRUCTURAL VOID (z-index: 0)
 Viewport Lock (100vw × --app-height) · 8-Lane Matrix · Row Quantization (Ry=32px)
================================================================================
```

---

## 2. Layer Definitions & Roles

### Layer 1: Base Canvas & Viewport Void (`z-index: 0`)
- **Nature**: The empty structural stage.
- **Anatomy**: `<body>` lock, stage grid wrapper (`100vw`, `--app-height`), 8-lane ($12.5\%$) or 16-sublane ($6.25\%$) base coordinate matrix, $R_y = 32\text{px}$ row quantization lines, and header bar placeholder.
- **Production Grid Transparency**: Development grid lines and lane guides render completely transparent in production.

### Layer 2: Surface Content & Interactive Controls (`z-index: 32` - `64`)
- **Nature**: The primary work surface and user interaction plane.
- **Anatomy**: Page content blocks, BEJSON data tables, operational switches / toggle fires, command buttons, card streams, toolbars, and primary input controls.
- **Spatial Bounds**: Snapped to $(x_{\text{start}}, x_{\text{span}}, y_{\text{start}}, y_{\text{span}})$ coordinate bounds on the Layer 1 matrix.

### Layer 3: Contextual Panels & Ephemeral Dialogues (`z-index: 96`)
- **Nature**: Temporary focus planes that interrupt the user's primary workflow.
- **Anatomy**: Modal dialogues, floating dialogue panels, configuration drawers, confirmation prompts, inspector HUDs, and layer sliders.
- **Production Occlusion**: 100% opaque (`#000000` or `#FFFFFF`) to completely block out background clutter and halt click-through. Transparency is strictly reserved for IDE inspection modes.

### Layer 4: Persistent Chrome & Global Navigation (`z-index: 128`)
- **Nature**: Global system chrome and structural navigation frame.
- **Anatomy**: Collapsible hamburger sidebar drawer, sticky brand badge, top-docked control hub, live status indicators, and global telemetry monitors.
- **Persistence**: Stays locked and persistent across page/content transitions.

---

## 3. Library Component Stacking Mechanics

Components templated and generated through specialized ecosystem libraries (`Lib_PY/BEHTML`, `Lib_PY/CMS`, `Lib_PY/Diagrams`, `Lib_SH/Terminal_Menus`) declare a standardized 5-tuple spatial coordinate vector:

$$\mathbf{C} = (x_{\text{start}},\, x_{\text{span}},\, y_{\text{start}},\, y_{\text{span}},\, z_{\text{layer}})$$

- **$x$ Coordinates**: Restrained to 8 lanes ($12.5\%$ per lane) or 16 sublanes ($6.25\%$ per half-cell).
- **$y$ Coordinates**: Quantized to integer multiples of $R_y = 32\text{px}$ (`32px`, `64px`, `96px`, `128px`, `160px`).
- **$z$ Coordinates**: Integer layer assignment ($1, 2, 3, 4$). Lower layers never bleed through higher layers because each upper-layer container has a solid opaque background token matching Policy §8.1 (`#000000` or `#FFFFFF`).
- **Library Decoupling**: Components are built and tested as modular library units and stacked deterministically on top of each other, preventing CSS specificity drift and z-index collisions.
