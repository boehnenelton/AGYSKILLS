---
name: bejson-diagrammer-cli
description: Generate, extend, validate, and inject systems architecture and workflow diagrams using the BEJSON Diagrammer CLI and prompt ledger instructions, in two output modes: (1) standalone read-only interactive SVG canvas HTML pages, and (2) self-contained embeddable 3-tab diagram components (Diagram, Description & Schema, About crediting Elton Boehnen) for injection into any host webpage, documentation article, or CMS template. Use when asked to generate diagrams, architecture flowcharts, BEJSON MFDB diagram schemas, extend active board diagrams, compile interactive diagram canvas HTML files, or produce a portable embeddable diagram widget. Do NOT use for general-purpose charts or data visualization unrelated to BEJSON diagram schemas.
---

# BEJSON Diagrammer CLI (Canvas + Embeddable Component)

Generate, scaffold, validate, extend, and compile interactive systems architecture diagrams and workflow boards into standalone read-only SVG canvas HTML deliverables or embeddable 3-tab components using the BEJSON Diagrammer CLI tool and Elton Boehnen's AI Prompt and Instruction Historical Ledger.

## Summary

This skill equips the agent to act as a Senior Diagram Systems Architect and Layout Engine adhering to Elton Boehnen's **MFDB Diagrammer React Conversion Ecosystem** (Single Source of Truth). It orchestrates diagram plan synthesis, attached context file ingestion, active board non-overlapping expansion, spatial layout math (50px snap, 40px padding), arrival schema validation, and template injection into read-only standalone HTML files.

The skill integrates the **Prompt Concept** (Relational ID: 64b9314e-f6bf-4807-84c7-a2852eae1771) and the **Diagram Arrival Validation Protocols & AI Optimization Ledger** (Relational ID: c9f8e7d6-c5b4-4321-8765-43210fe98765) from the React flagship codebase.

## Output Modes

| Mode | Command | Template | Deliverable |
| :--- | :--- | :--- | :--- |
| **Canvas** | `inject` / `append --inject` | `assets/diagram_canvas_template.html` | Standalone read-only SVG canvas HTML page |
| **Component** | `component` | `assets/diagram_component_template.html` | Single `<div class="w-diag-comp">` snippet with 3-tab switcher, embeddable in host pages or iframes |

Both modes share one data model, one validation pipeline, and one CLI (`scripts/diagram-cli.js`, Python mirror `scripts/diagram_cli.py`).

## Mode 1: Read-Only Canvas Deliverable Specifications

The output HTML file produced by the skill adheres strictly to these UX specifications:

1. **Read-Only Viewer**: Focused viewing surface without distracting editing tools or node mutation controls.
2. **Bottom-Right Floating Action Button**: A fixed floating button in the bottom right corner (`#btn-fab-sidebar`) that smoothly opens and closes the inspector drawer.
3. **Sidebar Schema Viewer with One-Click Copy**: Inside the drawer, a dedicated schema section features an input box (`<textarea class="schema-input-box">`) displaying the formatted Diagram Schema and a one-click `📋 Copy Schema` button with instant clipboard feedback.
4. **Horizontal Floating Zoom Controls**:
   - Floating horizontally at the top of the canvas viewport (`[Fit View] [－] [85%] [＋] [Reset] [🌓 Theme]`).
   - Sticky horizontal zoom controls at the very top of the sidebar drawer (`[－] [85%] [＋] [100%] [Fit]`).
5. **Interactive Element Inspection**: Clicking any shape, relationship connector, or zone on the canvas displays its metadata in the sidebar.
6. **Tri-Color Palette Standard**: Clean high-contrast styling adhering to `#000000` (dark mode) / `#FFFFFF` (light mode) with `#DE2626` active accents.
7. **Mobile 100px Lower Toolbar Clearance**: On mobile screens (`max-width: 768px`), all bottom-anchored controls (including the `#btn-fab-sidebar` button, drawer scroll bodies, and canvas viewport bounds) must strictly account for the 100-pixel lower browser toolbar (`bottom: calc(100px + env(safe-area-inset-bottom, 0px) + 16px)` and `padding-bottom: calc(100px + 30px)`) so action targets and bottom-most nodes are never obscured by mobile browser navigation bars.


## Mode 2: 3-Tab Embeddable Component Specifications

The `component` command produces a single self-contained `<div class="w-diag-comp">` (Portable Widget Contract, Release_Version 300) whose switcher isolates the clean diagram from descriptions, attribution, and raw schema data:

1. **Tab 1: Diagram** - uncluttered interactive SVG surface with 50px grid snap, drag-pan, wheel-zoom, docked toolbar (`[Fit View] [－] [85%] [＋] [Reset] [🌓 Theme]`), and an on-canvas inspector card (`.w-diag-node-popup`) on node/zone click. No descriptive paragraphs on the canvas surface.
2. **Tab 2: Description & Schema** - vertical scroll container (`.w-diag-scroll-panel`) holding the scope narrative (`#w-diag-scope-text`), the live Inspected Element card, an iframe embed-code box with `📋 Copy Iframe Code`, and the formatted verified Diagram Schema with `📋 Copy Schema JSON`.
3. **Tab 3: About** - scroll container with Author **Elton Boehnen**, Location **Roseburg, Oregon, United States**, Standard **Release_Version 300 · MFDB Diagrammer React Standard**, and portfolio links `boehnenelton2024@gmail.com` · `boehnenelton2024.pages.dev` · `github.com/boehnenelton`.
4. **Mobile 100px clearance** (`max-width: 768px`): `.w-diag-node-popup` at `bottom: calc(100px + env(safe-area-inset-bottom, 0px) + 16px)`; `.w-diag-scroll-body` with `padding-bottom: calc(100px + env(safe-area-inset-bottom, 0px) + 30px)`; `fitView()` reserves at least 160px bottom clearance.

The generated component file is ready for inclusion in articles, docs, or iframes without a full-page HTML shell.

## Diagram Data Model & Arrival Validation Protocols (Both Modes)

Diagrams adhere to the React ecosystem's canonical data model:

```json
{
  "diagramId": "string",
  "name": "string",
  "description": "string",
  "shapes": [
    {
      "id": "string",
      "label": "string",
      "text": "string",
      "kind": "rect | circle",
      "sizeClass": "small | medium | large | huge",
      "color": "hex",
      "fontColor": "auto | hex",
      "cx": 300,
      "cy": 200,
      "parentId": "string | null"
    }
  ],
  "connectors": [
    { "id": "string", "from": "shape_1", "to": "shape_2", "flow": "forward | backward | bidirectional | none" }
  ],
  "territories": [
    { "id": "string", "kind": "rect | circle", "cx": 300, "cy": 300, "size": 280, "label": "string", "color": "hex" }
  ]
}
```

### Arrival Validation & Sanitization Pipeline (Relational ID: c9f8e7d6-c5b4-4321-8765-43210fe98765):
1. **Pre-Validation (`validatePlanSemantics`)**: Validates tempId uniqueness, sizeClass enums, kind enums, flow enums, numeric coordinates, and valid hex colors.
2. **Post-Assembly Verification (`validateDiagram`)**: Validates non-overlapping bounding boxes (min distance 40px clearance), foreign key resolution (all connector `from`/`to` exist), parentId existence, and cyclic hierarchy prevention.
3. **Auto-Remediation on Arrival (`remediateDiagram`)**: Automatically purges dangling connectors, clears broken parent links, deduplicates IDs, and quantizes coordinates to 50px increments.

## Core Workflows

### 1. Generating a Diagram Plan

```bash
node scripts/diagram-cli.js generate \
  --prompt "Distributed Payment Gateway with Ledger, Fraud Detection, and Bank Integration" \
  --out payment_plan.json \
  --title "Payment Architecture"
```

### 2. Validating a Diagram

```bash
node scripts/diagram-cli.js validate --file payment_plan.json
```

Or via Python:

```bash
python3 scripts/diagram_cli.py validate -f payment_plan.json
```

### 3. Injecting into Canvas HTML Template

```bash
node scripts/diagram-cli.js inject \
  --diagram payment_plan.json \
  --template assets/diagram_canvas_template.html \
  --out payment_canvas.html \
  --title "Payment Architecture"
```

### 4. Append Mode (Extending an Active Diagram)

```bash
node scripts/diagram-cli.js append \
  --existing payment_plan.json \
  --prompt "Add Prometheus metrics monitoring and automated alerting webhooks" \
  --out payment_extended.json \
  --inject assets/diagram_canvas_template.html
```

### 5. Injecting into the 3-Tab Component Template (Mode 2)

```bash
node scripts/diagram-cli.js component \
  --diagram payment_plan.json \
  --template assets/diagram_component_template.html \
  --out payment_component.html \
  --title "Payment Architecture"
```

```bash
python3 scripts/diagram_cli.py validate -f payment_plan.json
```

`assets/example_payment_plan.json` is a ready sample diagram for smoke-testing every command above (copy it to `payment_plan.json`).
