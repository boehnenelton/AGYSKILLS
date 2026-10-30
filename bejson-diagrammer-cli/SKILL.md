---
name: bejson-diagrammer-cli
description: Generate, extend, validate, and inject systems architecture and workflow diagrams into interactive HTML canvas templates using the BEJSON Diagrammer CLI tool and prompt ledger instructions. Use when asked to generate diagrams, architecture flowcharts, BEJSON MFDB diagram schemas, extend active board diagrams, or compile interactive diagram canvas HTML files. Do NOT use for embeddable 3-tab diagram widgets (use bejson-diagram-component).
---

# BEJSON Diagrammer CLI

Generate, scaffold, validate, extend, and compile interactive systems architecture diagrams and workflow boards into standalone read-only SVG canvas HTML deliverables using the BEJSON Diagrammer CLI tool and Elton Boehnen's AI Prompt and Instruction Historical Ledger.

## Summary

This skill equips the agent to act as a Senior Diagram Systems Architect and Layout Engine adhering to Elton Boehnen's **MFDB Diagrammer React Conversion Ecosystem** (Single Source of Truth). It orchestrates diagram plan synthesis, attached context file ingestion, active board non-overlapping expansion, spatial layout math (50px snap, 40px padding), arrival schema validation, and template injection into read-only standalone HTML files.

The skill integrates the **Prompt Concept** (Relational ID: 64b9314e-f6bf-4807-84c7-a2852eae1771) and the **Diagram Arrival Validation Protocols & AI Optimization Ledger** (Relational ID: c9f8e7d6-c5b4-4321-8765-43210fe98765) from the React flagship codebase.

## Read-Only Canvas Deliverable Specifications

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

## Diagram Data Model & Arrival Validation Protocols

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
