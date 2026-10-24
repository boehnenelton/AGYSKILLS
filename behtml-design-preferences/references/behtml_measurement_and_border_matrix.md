# BEHTML Measurement, Transparency & Seamless Border Reference Matrix

Exhaustive selector-by-selector forensic specification of the canonical BEHTML Document Specification Template.

## 1. Root Design Tokens (`:root`)

| Token Name | Exact Value | Purpose & Role |
| :--- | :--- | :--- |
| `--app-height` | `100dvh` (synced to `visualViewport.height`) | Dynamic viewport height lock for `.behtml-stage` and `body` |
| `--ry-unit` | `32px` | Canonical vertical row quantization unit ($R_y = 32\text{px}$) |
| `--bg-canvas` | `#ffffff` | Pure white background across body, stage, title bar, gutters, canvas, tables, pre blocks, and widget shelf |
| `--text-primary` | `#000000` | Pure black text, active button hover fill, table/pre outer frame, and footer top divider |
| `--color-accent` | `#DE2626` | Strict BEHTML Red for title bar bottom border, heading left bars, `th` bottom border, `pre` left border, buttons, `strong`/`b`, `code`, and active badges |
| `--color-muted-gray` | `#71717a` | Zinc-500 gray for italic emphasis (`em`, `i`), `.section-meta-bar em`, `.null-token`, and `.widget-block-body` |
| `--color-disabled-gray` | `#a1a1aa` | Zinc-400 gray for disabled text, disabled borders, and default scrollbar thumb |
| `--color-disabled-bg` | `#f4f4f5` | Zinc-100 background fill for disabled buttons and `.status-badge-disabled` |
| `--border-canvas` | `1px solid transparent` | Canonical invisible boundary token |
| `--font-ui` | `'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | Primary prose and body typography |
| `--font-mono` | `'JetBrains Mono', ui-monospace, monospace` | Monospace chrome, headers, tables, metadata bars, code, buttons, footer, and widgets |

## 2. Spatial Grid & Sublane Coordinate Matrix

| Region / Selector | Grid Column | Width Allocation | Grid Row | Height Allocation | Border & Transparency Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.behtml-stage` | `6.25% repeat(14, 6.25%) 6.25%` | `100vw` (16 sublanes = 8 cells) | `grid-auto-rows: 32px` | `var(--app-height)` | `background-color: #ffffff`, zero visible grid lines |
| `.behtml-title-bar` | `1 / -1` (Sublanes 1..16) | `100vw` (8.0 cells) | `1 / span 1` (Row 1) | `32px` ($1 \times R_y$) | `border: none; border-bottom: 2px solid #DE2626; z-index: 20` |
| `.gutter-left` | `1 / 2` (Sublane 1) | `6.25%` (0.5 cell) | `2 / span 17` (Rows 2..18) | `544px` ($17 \times R_y$) | `border-right: 1px solid transparent; pointer-events: none` |
| `.behtml-doc-canvas` | `2 / 16` (Sublanes 2..15) | `87.5%` (7.0 cells) | `2 / span 17` (Rows 2..18) | `544px` (`calc(17 * 32px)`) | `border: none; border-bottom: 1px solid transparent; overflow-y: auto; overflow-x: hidden` |
| `.gutter-right` | `16 / -1` (Sublane 16) | `6.25%` (0.5 cell) | `2 / span 17` (Rows 2..18) | `544px` ($17 \times R_y$) | `border-left: 1px solid transparent; pointer-events: none` |
| *(Row 19 Buffer)* | Implicit | `100vw` | Row 19 (`span 1`) | `32px` ($1 \times R_y$) | Empty vertical separation row between canvas and widget shelf |
| `.behtml-widget-shelf` | `2 / 16` (Sublanes 2..15) | `87.5%` (7.0 cells) | `20 / span 5` (Rows 20..24) | `160px` ($5 \times R_y$) | Seamless `#ffffff` flex row (`gap: 20px; padding: 0 16px`) |
| `.widget-block` | Flex child inside shelf | `150px` (`min`/`max: 150px`) | Centered in `160px` shelf | `150px` (`min`/`max: 150px`) | `border: 1px solid transparent; padding: 10px; flex-shrink: 0` |

## 3. Complete Component & Typography Specification Table

| Selector | Font Family & Size | Weight / Style / Case | Spacing (Margin / Padding) | Borders, Colors & Visual Rules |
| :--- | :--- | :--- | :--- | :--- |
| `body` | `var(--font-ui)`, `15px` | Regular, `line-height: 1.6` | `margin: 0; padding: 0` | `bg: #ffffff`, `color: #000000`, `width: 100vw`, `height: var(--app-height)`, `overflow: hidden` |
| `.behtml-title-bar h1` | `var(--font-mono)`, `14px` | `700`, `uppercase`, `letter-spacing: 0.12em` | Centered via flex | `color: #000000`; child `span` is `color: #DE2626` |
| `.behtml-doc-canvas` | Inherits `body` (`15px`) | `flex-direction: column` | `padding: 16px 24px 20px` | `height: calc(17 * 32px)` (`544px`), `max-height: 544px`, `border-bottom: 1px solid transparent` |
| `.behtml-doc-canvas::-webkit-scrollbar` | N/A | N/A | `width: 4px` | Track: `transparent`; Thumb: `#a1a1aa`; Thumb hover: `#DE2626` |
| `.behtml-doc-canvas h2` | `var(--font-ui)`, `1.25rem` | `700`, `letter-spacing: -0.02em`, `line-height: 1.2` | `margin: 1.25rem 0 0.25rem` (`first-of-type` top `0`), `padding-left: 0.75rem` | `border-left: 3px solid #DE2626` |
| `.section-meta-bar` | `var(--font-mono)`, `11px` | `uppercase`, `letter-spacing: 0.05em` | `margin-bottom: 1rem`, `padding-left: 0.75rem`, `gap: 12px` | `border-left: 3px solid transparent` (optical alignment with `h2`); `span`: `#DE2626` bold; `em`: `#71717a` italic |
| `.behtml-doc-canvas p` | `var(--font-ui)`, `15px` | Regular, `text-align: justify` | `margin-bottom: 1.25rem` | `color: #000000` |
| `strong, b` | Inherits | `font-weight: 700` | Inline | `color: #DE2626` |
| `em, i` | Inherits | `font-style: italic` | Inline | `color: #71717a` |
| `.data-table-wrapper` | N/A | N/A | `margin: 1.25rem 0 1.75rem` | `border: 1px solid #000000; overflow-x: auto` |
| `table` | `var(--font-mono)`, `0.82rem` | `border-collapse: collapse` | `width: 100%` | Inside `.data-table-wrapper` |
| `th` | `var(--font-mono)`, `0.82rem` | `700`, `uppercase`, `letter-spacing: 0.05em` | `padding: 8px 12px`, `text-align: left` | `bg: #ffffff`, `color: #000000`, `border-bottom: 2px solid #DE2626` |
| `td` | `var(--font-mono)`, `0.82rem` | Regular | `padding: 8px 12px` | `border-bottom: 1px solid #e4e4e7` (last row `none`), `color: #000000` |
| `.status-badge` | `var(--font-mono)` | `font-weight: 700` | Inline | `color: #DE2626` |
| `.status-badge-disabled` | `var(--font-mono)`, `0.75rem` | `uppercase` | `padding: 2px 6px` | `bg: #f4f4f5`, `color: #a1a1aa`, `border: 1px solid #a1a1aa` |
| `code` (inline) | `var(--font-mono)`, `0.85em` | `font-weight: 500` | Inline | `color: #DE2626` |
| `pre` | `var(--font-mono)` | Block | `padding: 1rem`, `margin-bottom: 1.5rem` | `bg: #ffffff`, `border: 1px solid #000000`, `border-left: 4px solid #DE2626`, `overflow-x: auto` |
| `pre code` | `var(--font-mono)`, `0.85rem` | `font-weight: 500` | Reset inline color | `color: #000000` |
| `.control-row` | N/A | Flex row | `gap: 12px`, `margin: 1rem 0 1.5rem` | Houses interactive buttons |
| `button` | `var(--font-mono)`, `0.8rem` | `700`, `uppercase`, `letter-spacing: 0.05em` | `padding: 8px 16px` | `bg: #DE2626`, `border: 1px solid #DE2626`, `color: #ffffff`; `:hover` -> `#000000`; `:disabled` -> `bg: #f4f4f5`, `border/color: #a1a1aa` |
| `.author-null-footer` | `var(--font-mono)`, `11px` | `uppercase`, `letter-spacing: 0.05em` | `margin-top: 2rem`, `padding-top: 14px` | `border-top: 1px solid #000000`, `display: flex`, `justify-content: space-between`; `.auth-field`: `#DE2626` bold; `.null-token`: `#71717a` italic |
| `.widget-block-header` | `var(--font-mono)`, `10px` | `700`, `uppercase`, `letter-spacing: 0.05em` | `padding-bottom: 4px` | `color: #000000`, `border-bottom: 2px solid #DE2626` |
| `.widget-block-body` | `var(--font-mono)`, `9px` | `italic`, `text-align: center` | Flex middle | `color: #71717a` |
| `.widget-block-footer` | `var(--font-mono)`, `9px` | `700`, `uppercase`, `text-align: right` | Flex bottom | `color: #DE2626` |
