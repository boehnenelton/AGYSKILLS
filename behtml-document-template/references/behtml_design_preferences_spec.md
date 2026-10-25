# BE HTML Design Preferences: Exhaustive Architectural & Dimensional Reference

> **Parent Skill:** `behtml-design-preferences` (Layer 4)  
> **Version:** 100 | **Release_Version:** 300 | **RELATIONAL_ID:** `6a1b9c43-2d8e-4f01-9c74-8b5a2e3f1d90`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Dimensional & Spatial Invariants

The BE HTML template (`assets/Template_HTML_Document.html`) establishes a rigid, viewport-locked 16-sublane by 24-row grid stage where every component occupies an exact multiple of the `Ry = 32px` vertical quantization unit and `6.25%` (`0.5 cell`) horizontal sublane unit.

### 1.1 Complete Selector-by-Selector Measurement Matrix

| CSS Selector | Grid / Flex Coordinates | Exact Dimensions | Padding & Margin | Border & Transparency Rules | Typography & Color Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `:root` | Document Root | `--app-height: 100dvh`, `--ry-unit: 32px` | N/A | `--border-canvas: 1px solid transparent` | Defines Tri-Color (`#ffffff`, `#000000`, `#DE2626`) + zinc grays (`#71717a`, `#a1a1aa`, `#f4f4f5`) |
| `*` | Universal | `box-sizing: border-box` | `margin: 0; padding: 0` | `-webkit-tap-highlight-color: transparent` | Inherits |
| `body` | Viewport Container | `width: 100vw; height: var(--app-height)` | `0` | `overflow: hidden` (window never scrolls) | `font-family: var(--font-ui); font-size: 15px; line-height: 1.6; color: #000000; background: #ffffff; -webkit-font-smoothing: antialiased` |
| `.behtml-stage` | Root CSS Grid | `width: 100vw; height: var(--app-height)` | `0` | Seamless `#ffffff` canvas | `grid-template-columns: 6.25% repeat(14, 6.25%) 6.25%; grid-auto-rows: 32px` |
| `.behtml-title-bar` | `col: 1 / -1`, `row: 1 / span 1` | `100vw` x `32px` (`1 * 32px`), `z-index: 20` | `0` (Flex centered) | `border: none; border-bottom: 2px solid #DE2626` | Background `#ffffff` |
| `.behtml-title-bar h1` | Flex child | Auto | `0` | None | `JetBrains Mono`, `14px`, `700`, `uppercase`, `letter-spacing: 0.12em`, `#000000` (`span` = `#DE2626`) |
| `.gutter-left` | `col: 1 / 2`, `row: 2 / span 17` | `6.25%` (`0.5 cell`) x `544px` (`17 * 32px`) | `0` | `border-right: 1px solid transparent; pointer-events: none` | Background `#ffffff` |
| `.gutter-right` | `col: 16 / -1`, `row: 2 / span 17` | `6.25%` (`0.5 cell`) x `544px` (`17 * 32px`) | `0` | `border-left: 1px solid transparent; pointer-events: none` | Background `#ffffff` |
| `.behtml-doc-canvas` | `col: 2 / 16`, `row: 2 / span 17` | `87.5%` (`7 cells`) x `544px` (`calc(17 * var(--ry-unit))`) | `padding: 16px 24px 20px` | `border: none; border-bottom: 1px solid transparent; overflow-y: auto; overflow-x: hidden` | Flex column container on `#ffffff` |
| `.behtml-doc-canvas::-webkit-scrollbar` | Canvas Scrollbar | `width: 4px` | `0` | Track: `background: transparent` | Thumb: `#a1a1aa`, Hover: `#DE2626` |
| `.behtml-doc-canvas h2` | Canvas Child | Full canvas inner width | `margin: 1.25rem 0 0.25rem 0` (`first-of-type` top `0`), `padding-left: 0.75rem` | `border-left: 3px solid #DE2626` | `1.25rem` (`20px`), `700`, `line-height: 1.2`, `letter-spacing: -0.02em` |
| `.section-meta-bar` | Flex row (`gap: 12px`) | Full canvas inner width | `margin-bottom: 1rem; padding-left: 0.75rem` | `border-left: 3px solid transparent` (matches `h2` 3px border for exact text alignment) | `JetBrains Mono`, `11px`, `uppercase`, `letter-spacing: 0.05em` (`span` bold `#DE2626`, `em` italic `#71717a`) |
| `.behtml-doc-canvas p` | Prose block | Full canvas inner width | `margin-bottom: 1.25rem` | None | `text-align: justify; color: #000000` (`strong`/`b` bold `#DE2626`; `em`/`i` italic `#71717a`) |
| `.data-table-wrapper` | Block wrapper | Full canvas inner width | `margin: 1.25rem 0 1.75rem` | `border: 1px solid #000000; overflow-x: auto` | Wraps `table` |
| `table` | Tabular grid | `width: 100%` | `0` | `border-collapse: collapse` | `JetBrains Mono`, `0.82rem` |
| `th` | Table header cell | Auto | `padding: 8px 12px` | `border-bottom: 2px solid #DE2626` | `700`, `uppercase`, `letter-spacing: 0.05em`, `text-align: left`, `#000000` on `#ffffff` |
| `td` | Table data cell | Auto | `padding: 8px 12px` | `border-bottom: 1px solid #e4e4e7` (`tr:last-child td` = `none`) | `#000000` |
| `.status-badge` | Inline status | Auto | `0` | None | `700`, `#DE2626` |
| `.status-badge-disabled` | Inline disabled badge | Auto | `padding: 2px 6px` | `border: 1px solid #a1a1aa` | `0.75rem`, `uppercase`, color `#a1a1aa`, bg `#f4f4f5` |
| `code` (inline) | Inline monospace | Auto | `0` | None | `JetBrains Mono`, `0.85em`, `500`, `#DE2626` |
| `pre` / `pre code` | Code block | Full canvas inner width | `padding: 1rem; margin-bottom: 1.5rem` | `border: 1px solid #000000; border-left: 4px solid #DE2626; overflow-x: auto` | `pre code` overrides color to `#000000`, `0.85rem` |
| `.control-row` | Button bar | Flex row (`gap: 12px`) | `margin: 1rem 0 1.5rem` | None | Flex container |
| `button` | Action control | Auto | `padding: 8px 16px` | `border: 1px solid #DE2626` (hover `#000000`, disabled `#a1a1aa`) | `JetBrains Mono`, `0.8rem`, `700`, `uppercase`, `letter-spacing: 0.05em`, `#ffffff` on `#DE2626` (hover bg `#000000`, disabled bg `#f4f4f5` / color `#a1a1aa`) |
| `.author-null-footer` | Canvas footer | Flex (`space-between`, `center`) | `margin-top: 2rem; padding-top: 14px` | `border-top: 1px solid #000000` | `JetBrains Mono`, `11px`, `uppercase`, `letter-spacing: 0.05em` (`.auth-field` bold `#DE2626`, `.null-token` italic `#71717a`) |
| `.behtml-widget-shelf` | `col: 2 / 16`, `row: 20 / span 5` | `87.5%` x `160px` (`5 * 32px`), `gap: 20px` | `padding: 0 16px` | Centered flex (`justify-content: center; align-items: center`) | Background `#ffffff` (Row 19 is an intentional 32px gap above Row 20) |
| `.widget-block` | Flex child (`flex-shrink: 0`) | `150px` x `150px` (`min/max-width: 150px`, `min/max-height: 150px`) | `padding: 10px` | `border: 1px solid transparent` (seamless outer boundary) | Flex column (`justify-content: space-between`), bg `#ffffff` |
| `.widget-block-header` | Widget top | Full inner width | `padding-bottom: 4px` | `border-bottom: 2px solid #DE2626` | `JetBrains Mono`, `10px`, `700`, `uppercase`, `letter-spacing: 0.05em`, `#000000` |
| `.widget-block-body` | Widget middle | Full inner width | `0` | None | `JetBrains Mono`, `9px`, `italic`, `text-align: center`, `#71717a` |
| `.widget-block-footer` | Widget bottom | Full inner width | `0` | None | `JetBrains Mono`, `9px`, `700`, `uppercase`, `text-align: right`, `#DE2626` |

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
