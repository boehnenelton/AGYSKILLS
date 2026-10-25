---
name: publication-html-builder
description: >-
  Build and format standalone editorial HTML documents, technical specifications, and publication views backed by the canonical 16-sublane (6.25% edge gutters, 87.5% main canvas), Ry=32px row-quantized BE HTML document templates (with widget shelf or widgetless), seamless transparent borders, and Policy 8.1 Tri-Color palette (#ffffff, #000000, #DE2626). Use when formatting standalone HTML publications, editorial technical reports, or compiling structured prose and telemetry into production HTML documents. Do NOT use for raw BE HTML CSS design preference token rules (use behtml-design-preferences), scaffolding multi-archetype templates or web apps (use behtml-templates), or rendering BEJSON 104 vertical domain tables and terminal menus (use behtml-104-builder).
---

# Skill: `publication-html-builder` (Layer 4 - HTML Document & Editorial Publication Builder)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `104 (Foundational Era - Editorial HTML Document Builder, Release 300)`
- **Canonical Document Template**: `assets/Template_HTML_Document.html`
- **Date Created**: `2026-10-18`
- **RELATIONAL_ID**: `7b4e1a90-3f8c-4d21-9e54-1c6a8b2d0f39`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`publication-html-builder` operates at **Layer 4** of the 6-Tier Layered Skill Architecture to format and compile standalone editorial HTML documents and technical publications using the locked dimensions, seamless transparent borders, and Policy 8.1 Tri-Color rules (`#ffffff`, `#000000`, `#DE2626`) of the canonical BE HTML document template (`assets/Template_HTML_Document.html`).

---

## 2. Structural & Dimensional Contract

1. **16-Sublane Stage & Viewport Lock**:
   - `body`: `width: 100vw; height: var(--app-height); overflow: hidden; font-size: 15px; line-height: 1.6;` with `visualViewport` resize synchronization (`--app-height: 100dvh` fallback).
   - `.behtml-stage`: `grid-template-columns: 6.25% repeat(14, 6.25%) 6.25%; grid-auto-rows: var(--ry-unit);` (`--ry-unit: 32px`).
2. **Row Allocation (`Ry = 32px`)**:
   - **Row 1 (`32px`)**: `header.behtml-title-bar` (`1 / -1`) with `border-bottom: 2px solid var(--color-accent)`.
   - **Rows 2..18 (`544px`)**: `.gutter-left` (`1 / 2`, `border-right: 1px solid transparent`), `main.behtml-doc-canvas` (`2 / 16`, `height: calc(17 * var(--ry-unit)); overflow-y: auto; padding: 16px 24px 20px; border-bottom: 1px solid transparent`), and `.gutter-right` (`16 / -1`, `border-left: 1px solid transparent`).
   - **Row 19 (`32px`)**: Implicit 1-row transparent buffer between canvas and widget shelf.
   - **Rows 20..24 (`160px`)**: `section.behtml-widget-shelf` (`2 / 16`, `gap: 20px; padding: 0 16px`) containing `150px x 150px` `.widget-block` cards (`border: 1px solid transparent`).
3. **Editorial & Telemetry Typography**:
   - `h2` (`1.25rem`, `border-left: 3px solid #DE2626; padding-left: 0.75rem`) paired with `.section-meta-bar` (`11px` mono, `border-left: 3px solid transparent; padding-left: 0.75rem`).
   - Justified body paragraphs (`p`), `.data-table-wrapper` (`1px solid #000000`), `pre` blocks (`border-left: 4px solid #DE2626`), `.control-row` buttons, and `.author-null-footer`.

---

## 3. Canonical HTML Document Template (Embedded Reference)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, maximum-scale=1.0, user-scalable=no"/>
    <title>Title</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --app-height: 100dvh;
            --ry-unit: 32px;
            --bg-canvas: #ffffff;
            --text-primary: #000000;
            --color-accent: #DE2626;
            --color-muted-gray: #71717a;
            --color-disabled-gray: #a1a1aa;
            --color-disabled-bg: #f4f4f5;
            --border-canvas: 1px solid transparent;
            --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', ui-monospace, monospace;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
        /* Viewport lock: window never scrolls, inner document canvas handles overflow */
        body {
            background-color: var(--bg-canvas); color: var(--text-primary);
            font-family: var(--font-ui); font-size: 15px; line-height: 1.6;
            width: 100vw; height: var(--app-height); overflow: hidden; -webkit-font-smoothing: antialiased;
        }
        /* 16-sublane grid: Sublane 1 (0.5 cell: 6.25%), Sublanes 2..15 (7 cells: 87.5%), Sublane 16 (0.5 cell: 6.25%) */
        .behtml-stage {
            display: grid; grid-template-columns: 6.25% repeat(14, 6.25%) 6.25%;
            grid-auto-rows: var(--ry-unit); width: 100vw; height: var(--app-height); background-color: var(--bg-canvas);
        }
        /* Row 1: Full-width Title Bar with bottom accent */
        .behtml-title-bar {
            grid-column: 1 / -1; grid-row: 1 / span 1; display: flex; align-items: center; justify-content: center;
            border: none; border-bottom: 2px solid var(--color-accent); background-color: var(--bg-canvas); z-index: 20;
        }
        .behtml-title-bar h1 {
            font-size: 14px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
            color: var(--text-primary); font-family: var(--font-mono);
        }
        .behtml-title-bar h1 span { color: var(--color-accent); }
        /* Canvas: 17 rows (Rows 2..18 = 544px) - Completely transparent bottom border */
        .behtml-doc-canvas {
            grid-column: 2 / 16; grid-row: 2 / span 17;
            height: calc(17 * var(--ry-unit)); max-height: calc(17 * var(--ry-unit));
            display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden;
            padding: 16px 24px 20px; background-color: var(--bg-canvas); border: none; border-bottom: 1px solid transparent;
        }
        /* 0.5-Cell Side Boundaries: Completely transparent and seamless */
        .behtml-edge-gutter { background-color: var(--bg-canvas); pointer-events: none; }
        .gutter-left { grid-column: 1 / 2; grid-row: 2 / span 17; border-right: 1px solid transparent; }
        .gutter-right { grid-column: 16 / -1; grid-row: 2 / span 17; border-left: 1px solid transparent; }
        .behtml-doc-canvas::-webkit-scrollbar { width: 4px; }
        .behtml-doc-canvas::-webkit-scrollbar-track { background: transparent; }
        .behtml-doc-canvas::-webkit-scrollbar-thumb { background: var(--color-disabled-gray); }
        .behtml-doc-canvas::-webkit-scrollbar-thumb:hover { background: var(--color-accent); }
        /* Section Heading & Sub-Heading Metadata Block */
        .behtml-doc-canvas h2 {
            font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; margin-top: 1.25rem; margin-bottom: 0.25rem;
            border-left: 3px solid var(--color-accent); padding-left: 0.75rem; line-height: 1.2;
        }
        .behtml-doc-canvas h2:first-of-type { margin-top: 0; }
        .section-meta-bar {
            font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase;
            color: var(--text-primary); margin-bottom: 1rem; padding-left: 0.75rem;
            border-left: 3px solid transparent; display: flex; gap: 12px;
        }
        .section-meta-bar span { color: var(--color-accent); font-weight: 700; }
        .section-meta-bar em { color: var(--color-muted-gray); font-style: italic; }
        .behtml-doc-canvas p { margin-bottom: 1.25rem; color: var(--text-primary); text-align: justify; }
        strong, b { font-weight: 700; color: var(--color-accent); }
        em, i { font-style: italic; color: var(--color-muted-gray); }
        /* Telemetry Data Table */
        .data-table-wrapper { margin: 1.25rem 0 1.75rem; overflow-x: auto; border: 1px solid var(--text-primary); }
        table { width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 0.82rem; }
        th {
            background-color: var(--bg-canvas); color: var(--text-primary); font-weight: 700; text-align: left;
            padding: 8px 12px; border-bottom: 2px solid var(--color-accent); text-transform: uppercase; letter-spacing: 0.05em;
        }
        td { padding: 8px 12px; border-bottom: 1px solid #e4e4e7; color: var(--text-primary); }
        tr:last-child td { border-bottom: none; }
        .status-badge { font-weight: 700; color: var(--color-accent); }
        .status-badge-disabled {
            font-size: 0.75rem; padding: 2px 6px; background-color: var(--color-disabled-bg);
            color: var(--color-disabled-gray); border: 1px solid var(--color-disabled-gray); text-transform: uppercase;
        }
        /* Monospace Pre Block */
        code { font-family: var(--font-mono); font-size: 0.85em; color: var(--color-accent); font-weight: 500; }
        pre {
            background-color: var(--bg-canvas); border: 1px solid var(--text-primary);
            border-left: 4px solid var(--color-accent); padding: 1rem; margin-bottom: 1.5rem; overflow-x: auto;
        }
        pre code { color: var(--text-primary); font-size: 0.85rem; }
        /* Action Buttons */
        .control-row { display: flex; gap: 12px; margin-top: 1rem; margin-bottom: 1.5rem; }
        button {
            font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; padding: 8px 16px;
            border: 1px solid var(--color-accent); background-color: var(--color-accent); color: #ffffff;
            cursor: pointer; text-transform: uppercase; letter-spacing: 0.05em;
        }
        button:hover { background-color: var(--text-primary); border-color: var(--text-primary); }
        button:disabled {
            background-color: var(--color-disabled-bg); border-color: var(--color-disabled-gray);
            color: var(--color-disabled-gray); cursor: not-allowed;
        }
        /* Monospace Author Null Footer Bar */
        .author-null-footer {
            margin-top: 2rem; padding-top: 14px; border-top: 1px solid var(--text-primary);
            display: flex; justify-content: space-between; align-items: center;
            font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase;
        }
        .author-null-footer .auth-field { font-weight: 700; color: var(--color-accent); }
        .author-null-footer .null-token { color: var(--color-muted-gray); font-style: italic; }
        /* Widgets Shelf: Shifted to Row 20 (Height 5 rows = 160px) */
        .behtml-widget-shelf {
            grid-column: 2 / 16; grid-row: 20 / span 5; width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center; gap: 20px; padding: 0 16px; background-color: var(--bg-canvas);
        }
        /* 150x150 Widget Blocks: Completely transparent seamless borders */
        .widget-block {
            width: 150px; min-width: 150px; max-width: 150px; height: 150px; min-height: 150px; max-height: 150px;
            border: 1px solid transparent; display: flex; flex-direction: column; justify-content: space-between;
            padding: 10px; background-color: var(--bg-canvas); flex-shrink: 0;
        }
        .widget-block-header {
            font-family: var(--font-mono); font-size: 10px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.05em; color: var(--text-primary); border-bottom: 2px solid var(--color-accent); padding-bottom: 4px;
        }
        .widget-block-body { font-family: var(--font-mono); font-size: 9px; color: var(--color-muted-gray); font-style: italic; text-align: center; }
        .widget-block-footer { font-family: var(--font-mono); font-size: 9px; font-weight: 700; color: var(--color-accent); text-transform: uppercase; text-align: right; }
    </style>
</head>
<body>
    <div class="behtml-stage">
        <!-- Row 1: Full-Width Seamless Title Bar with Red Bottom Line -->
        <header class="behtml-title-bar">
            <h1><span>//</span> DOCUMENT SPECIFICATION <span>01</span></h1>
        </header>
        <!-- 0.5-Cell Side Boundaries: Completely transparent -->
        <div class="behtml-edge-gutter gutter-left"></div>
        <div class="behtml-edge-gutter gutter-right"></div>
        <!-- Canvas: 17 Rows = 544px, Completely transparent borders -->
        <main class="behtml-doc-canvas">
            <h2>Section Heading</h2>
            <div class="section-meta-bar">
                <div>DATE: <span>2026-10-18</span></div>
                <div>AUTHOR: <span>NULL</span></div>
                <div>STATUS: <em>COMMITTED</em></div>
            </div>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore <strong>magna aliqua</strong>. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui <em>officia deserunt mollit</em> anim id est laborum.</p>
            <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae <strong>dicta sunt explicabo</strong>. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, <em>adipisci velit</em>, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.</p>
            <h2>Operational Telemetry Data</h2>
            <div class="data-table-wrapper">
                <table>
                    <thead>
                        <tr><th>Module Key</th><th>Sublane Vector</th><th>Runtime Status</th><th>Action Execution</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><code>kernel_dispatcher</code></td><td>X1 - X6 [Ry=32px]</td><td><span class="status-badge">COMMITTED</span></td><td><button type="button">Process</button></td></tr>
                        <tr><td><code>canvas_projector</code></td><td>Sublanes 02..15</td><td><span class="status-badge">ACTIVE</span></td><td><button type="button">Process</button></td></tr>
                        <tr><td><code>legacy_adapter</code></td><td>Isolated Gutter</td><td><span class="status-badge-disabled">Disabled</span></td><td><button type="button" disabled>Locked</button></td></tr>
                    </tbody>
                </table>
            </div>
            <h2>Execution Constraints</h2>
            <pre><code>{
  "canvas_format": "BEHTML",
  "y_start_row": 2,
  "y_span_rows": 17,
  "vertical_height_px": 544,
  "overflow_behavior": "scroll_y_contained",
  "author_signature": null
}</code></pre>
            <div class="control-row">
                <button type="button">Commit State</button>
                <button type="button" disabled>Rollback (Unavailable)</button>
            </div>
            <footer class="author-null-footer">
                <div>AUTHOR: <span class="auth-field">null</span></div>
                <div class="null-token">REVISION: NULL_POINTER // UNSET</div>
            </footer>
        </main>
        <!-- Widgets Shelf: Centered, Transparent Outer Box Borders -->
        <section class="behtml-widget-shelf">
            <div class="widget-block">
                <div class="widget-block-header">WIDGET 01</div>
                <div class="widget-block-body"><em>150x150 Slot</em></div>
                <div class="widget-block-footer">ACTIVE</div>
            </div>
            <div class="widget-block">
                <div class="widget-block-header">WIDGET 02</div>
                <div class="widget-block-body"><em>150x150 Slot</em></div>
                <div class="widget-block-footer">ACTIVE</div>
            </div>
        </section>
    </div>
    <script>
        if (window.visualViewport) {
            const syncCanvasHeight = () => {
                document.documentElement.style.setProperty('--app-height', `${window.visualViewport.height}px`);
            };
            window.visualViewport.addEventListener('resize', syncCanvasHeight);
            syncCanvasHeight();
        }
    </script>
</body>
</html>
```

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

All BEJSON data reads resolve via `field_map`, and headless executions enforce `--sandbox`:

```bash
agy --sandbox -p "Execute publication-html-builder verification gate and return deterministic JSON status."
```

---

## When NOT to Use

- **Inspecting or defining base BE HTML CSS design preferences and spatial measurement laws**: Redirect immediately to `behtml-design-preferences`.
- **Scaffolding parameterized BEHTML document templates**: Redirect immediately to `behtml-document-template`.
- **Rendering BEJSON 104 vertical domain tables, diagrams, or Lib_SH terminal menus**: Redirect immediately to `behtml-104-builder`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
