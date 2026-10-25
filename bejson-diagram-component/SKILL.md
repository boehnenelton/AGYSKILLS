---
name: bejson-diagram-component
description: Generate, scaffold, validate, and inject self-contained, embeddable interactive diagram components with a 3-tab switcher (Diagram, Description & Schema, and About crediting Elton Boehnen) into any host HTML page, documentation article, or CMS template. Use when asked to generate an embeddable diagram component, portable diagram widget, or embed an interactive diagram directly into an existing webpage. Do NOT use for system architecture flowchart compilation via CLI (use bejson-diagrammer-cli).
---

# BEJSON Diagram Component

Generate, scaffold, validate, and inject self-contained, embeddable interactive diagram viewer components featuring a 3-tab switcher directly into any host webpage, documentation article, or CMS template without requiring a full-page HTML shell.

## Summary

This skill specializes in producing atomic, portable diagram components adhering to Elton Boehnen's Portable Widget Contract (Release_Version 300) and the **MFDB Diagrammer React Conversion Ecosystem** (Single Source of Truth). The output is a single self-contained `<div class="w-diag-comp">` component with an integrated 3-tab switcher that isolates the clean diagram from descriptions, author attribution, and raw schema data.

The skill integrates the **Prompt Concept** (Relational ID: 64b9314e-f6bf-4807-84c7-a2852eae1771) and the **Diagram Arrival Validation Protocols & AI Optimization Ledger** (Relational ID: c9f8e7d6-c5b4-4321-8765-43210fe98765) from the React flagship codebase.

## 3-Tab Component Architecture

The generated component strictly features 3 switcher tabs:

1. **Tab 1: 📊 Diagram**
   - Clean, uncluttered interactive SVG canvas surface with 50px grid snap.
   - Internal pan by dragging and smooth wheel zoom with docked toolbar (`[Fit View] [－] [85%] [＋] [Reset] [🌓 Theme]`).
   - On-canvas floating element inspector card on node/zone click (`.w-diag-node-popup`).
   - Zero distracting descriptive paragraphs on the canvas surface.

2. **Tab 2: 📝 Description & Schema**
   - Wrapped in a dedicated vertical scroll container (`.w-diag-scroll-panel`) ensuring full scrollability.
   - Diagram Scope & Narrative overview (`#w-diag-scope-text`).
   - Live Inspected Element card showing technical metadata for any clicked node or territory zone.
   - Iframe URL Embed Code Box with a one-click `📋 Copy Iframe Code` button.
   - **Diagram Schema** Box displaying the formatted, verified Diagram Model with a one-click `📋 Copy Schema JSON` button.

3. **Tab 3: ℹ️ About (Author Attribution)**
   - Wrapped in a dedicated vertical scroll container (`.w-diag-scroll-panel`).
   - Author: **Elton Boehnen**
   - Location: **Roseburg, Oregon, United States**
   - Standard: **Release_Version 300** · MFDB Diagrammer React Standard
   - Portfolio & Links: `boehnenelton2024@gmail.com` · `boehnenelton2024.pages.dev` · `github.com/boehnenelton`

4. **Mobile 100px Lower Toolbar Clearance Standard**:
   - On mobile viewports (`max-width: 768px`), the on-canvas element inspector popup (`.w-diag-node-popup`) is positioned at `bottom: calc(100px + env(safe-area-inset-bottom, 0px) + 16px)`.
   - Dedicated vertical scroll panels (`.w-diag-scroll-body`) enforce `padding-bottom: calc(100px + env(safe-area-inset-bottom, 0px) + 30px)`.
   - `fitView()` reserves at least 160px bottom clearance to ensure nodes and controls are never occluded by the 100-pixel lower browser toolbar.

## Diagram Data Model & Arrival Validation Protocols

Diagrams adhere to the React ecosystem's canonical data model (`FullDiagramPayload`):

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

### 1. Generating a Diagram

```bash
node scripts/diagram-cli.js generate \
  --prompt "Microservices Authentication and Token Rotation Pipeline" \
  --out auth_diagram.json \
  --title "Auth Service Diagram"
```

### 2. Validating a Diagram

```bash
node scripts/diagram-cli.js validate --file auth_diagram.json
```

Or via Python:

```bash
python3 scripts/diagram_cli.py validate -f auth_diagram.json
```

### 3. Injecting into 3-Tab Component Template

```bash
node scripts/diagram-cli.js component \
  --diagram auth_diagram.json \
  --template assets/diagram_component_template.html \
  --out auth_component.html \
  --title "Auth Service Diagram"
```

### 4. Embedding into Host Webpages

The generated `auth_component.html` contains the complete self-contained `<div class="w-diag-comp">...</div>` snippet ready for inclusion in articles, docs, or iframes.
