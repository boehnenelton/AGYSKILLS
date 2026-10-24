---
name: ui-navigation-decomposer
description: >-
  Traces, extracts, decomposes, and maps the complete hierarchical navigation structure, site architecture, and spatial BEHTML/BECSS UI layout of any web page, web application, SPA, native UI, wireframe, or DOM dump. Use when asking for site maps, navigation trees, UI decomposition, routing architecture, app menus, sidebar hierarchy, or breadcrumbs before generating spatial templates. Do NOT use for generating HTML component grids (use behtml-layout-builder).
compatibility: Works with HTML, DOM dumps, accessibility trees, JSON routing tables, sitemaps, UI screenshots, wireframes, and design outlines.
---
# Web UI & Navigation Deideation-feature-composer

A deterministic framework for systematically discovering, decomposing, and structuring every layer of navigation, route flow, functional interaction, and spatial component layout within web applications and native interfaces into detailed hierarchical trees and BEHTML/BECSS spatial models.

---

## 1. Core Operating Principles

When performing UI and navigation decomposition, adhere strictly to these principles:

1. **Complete Functional Categorization**: Never produce shallow link lists. Every node in the navigation tree must be assigned an explicit purpose, interaction trigger, target state, dynamic parameter model, and visibility tier.
2. **Context-Aware Multi-Surface Detection**: Parse all navigation and UI surfaces simultaneously:
   - Primary Header Navigation (Global)
   - Left/Right Utility Sidebars (Workspace / App-level)
   - Contextual Tab Sets (View-level)
   - Secondary Sub-Navigation / Breadcrumbs (Route-level)
   - Footer / Legal / Deep-link matrices (Utility-level)
   - Hidden / Modal / Command Palette Triggers (Overlay-level)
3. **Spatial Determinism (BEHTML / BECSS)**: When mapping visual UI components, quantize layouts strictly to the 8-lane horizontal grid (`x_start: 0-7`, `x_span: 1-8`), 32px vertical row units (`y_start`, `y_span`, `Ry = 32px`), and integer `z_layer` stacking.
4. **Resilient Inferencing**: When processing partial DOM trees, screenshots, or incomplete route manifests, infer missing ancestor containers and label inferred branches clearly with `[Inferred]`.

---

## 2. Navigation Decomposition Workflow

Follow this step-by-step pipeline for routing and interaction mapping:

1. **Surface Scanning**: Segment the interface into distinct navigation zones:
   - `global_topbar`: Brand root, top-level routes, profile menu, global search, switcher.
   - `primary_sidebar`: Main feature sets, workspace switchers, nested category folds.
   - `secondary_sidebar`: Context-dependent item listings (e.g. mail folders, channels, doc trees).
   - `content_header_tabs`: Tabbed views switching active sub-contexts without full-page reloads.
   - `footer_matrix`: Directory links, status endpoints, compliance, documentation.
   - `overlay_menus`: Command palettes (`Cmd+K`), hamburger drawouts, action popovers.

2. **Node Extraction & Classification**:
   - `Display Label`: Sanitized human-readable text.
   - `Node Identifier`: Normalized kebab-case unique ID (e.g. `sidebar.content.posts`).
   - `Trigger Type`: Direct Link (`<a>`), Route Switcher (`<button onclick>`), Modal Opener, Accordion Toggle, Virtual Route Dispatcher.
   - `Route / Target`: Destination URL, URI fragment, hash route, or virtual state.
   - `Purpose`: Concise 1-2 sentence description explaining what the user achieves or views.
   - `Auth Tier`: `Public`, `Authenticated`, `Admin/Privileged`, `Anonymous Only`.
   - `State Profile`: `Static`, `Dynamic Parametric` (e.g. `/posts/:id`), `Collapsible Parent`, `External Redirect`.

---

## 3. Spatial UI & BEHTML / BECSS Decomposition Engine

When translating visual UI surfaces into deterministic component coordinates, apply the core spatial laws:

### Spatial Coordinate Rules

- **X-Axis (8 Lanes: X0 to X7)**:
  - Width is divided into 8 equal lanes (12.5% per lane).
  - `x_start`: integer from `0` to `7`.
  - `x_span`: integer from `1` to `8`.
  - Invariant: `x_start + x_span <= 8`.
- **Y-Axis (Row Quantization: Ry = 32px)**:
  - `y_start`: integer >= `0` representing row index.
  - `y_span`: integer >= `1` representing row count.
  - Total vertical height = `y_span * 32px`.
- **Z-Axis (Stacking Layers)**:
  - `z_layer`: integer >= `0` (default `0`).
  - CSS z-index conversion = `z_layer * 32`.
- **Container Hierarchy**:
  - `parent_id_fk`: `null` for root canvas elements, or parent `element_id` for nested children.
  - Child coordinates are local to the parent container's 8-lane grid.

### Standard Element Types & Defaults

| Element Type | Default x_span | Default y_span | Content Kind | Description |
| :--- | :--- | :--- | :--- | :--- |
| `button` | 2 | 1 | `text` | Interactive action button |
| `input` | 4 | 1 | `text` | Single-line text input |
| `textarea` | 4 | 2 | `text` | Multi-line text field |
| `combobox` | 3 | 1 | `text` | Select dropdown |
| `checkbox` | 1 | 1 | `text` | Binary checkbox toggle |
| `radio` | 1 | 1 | `text` | Single-select radio option |
| `label` | 2 | 1 | `text` | Static typography label |
| `container` | 8 | 2+ | `text` | Dashed wrapper holding nested children |
| `toolbar` | 8 | 1 | `text` | Single-row horizontal control bar |

### BECSS Design Tokens

- **Tri-Color Palette**: Black (`#000000`), White (`#FFFFFF`), Red (`#DE2626`).
- **Typography**: `Inter` for UI sans-serif, `Roboto Mono` or `Source Code Pro` for code/tabular data.

---

## 4. Output Schemas & Deliverables

Every decomposition task produces structured outputs matching the user's scope:

### Deliverable A: ASCII Navigation Hierarchy Map

```text
Root / [App Entry Surface]
├── [Zone] Primary Navigation Surface (Header / Sidebar)
│   ├── Group / Section: [Group Name]
│   │   ├── Item: [Label] ──> [Route/Action]
│   │   │   ├── Purpose: <Clear functional description>
│   │   │   ├── Trigger: <Link | Button | Drawer | Modal>
│   │   │   └── Sub-item: [Nested Entity] ──> [Route]
│   │   │       └── Purpose: <Clear functional description>
│   └── Group / Section: [Group Name]
│       └── ...
└── [Zone] Secondary / Utility Surfaces
    └── ...
```

### Deliverable B: Structured Navigation JSON Object

```json
{
  "app_root": "App Title / Interface",
  "navigation_surfaces": [
    {
      "surface_name": "Primary Sidebar",
      "surface_type": "primary_sidebar",
      "nodes": [
        {
          "id": "nav.content",
          "label": "Content Management",
          "type": "container",
          "children": [
            {
              "id": "nav.content.posts",
              "label": "Blog Posts",
              "type": "folder",
              "route": "/admin/posts",
              "purpose": "Central repository of all draft and published articles.",
              "trigger": "accordion_toggle",
              "auth_tier": "authenticated"
            }
          ]
        }
      ]
    }
  ]
}
```

### Deliverable C: BEHTMLElement BEJSON 104 Dataset

```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["BEHTMLElement"],
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
    { "name": "is_active", "type": "boolean" }
  ],
  "Values": [
    ["el_toolbar_01", "toolbar", 0, 1, 0, 8, 0, "", "", "text", null, true],
    ["el_label_01", "label", 0, 1, 0, 3, 0, "", "System Dashboard", "text", "el_toolbar_01", true],
    ["el_btn_01", "button", 0, 1, 6, 2, 0, "", "Execute", "text", "el_toolbar_01", true]
  ]
}
```

---

## 5. Edge Cases & Special Patterns

- **Single Page Applications (Virtual Routes)**: If state shifts alter the viewport without changing URL paths, classify trigger as `virtual_route_dispatcher` and specify the active container.
- **Role-Gated Routes**: Mark restricted links with `auth_tier: "role_restricted"` and add `[Restricted: <Role>]` in the ASCII map.
- **Infinite Nesting (File Trees / Docs)**: Trace down to 3 levels of concrete nodes, then append `[...Dynamic Recursive Collection]`.
- **Context / Workspace Switchers**: Represent dropdown selectors as top-level Root Modifiers branching into cloneable sub-trees.
- **Spatial Grid Alignment**: Never emit non-integer row heights or horizontal spans exceeding lane 7 (`x_start + x_span <= 8`).
