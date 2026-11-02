---
name: template-html-document-skeleton
description: >-
  Scaffold and deploy blank, bare-bones HTML document canvases for offline authoring and Markdown-to-HTML
  conversion workflows. Enforces the Domain 2 Zero-Filler Skeleton Law with strictly literal placeholder
  labels ('Document Title', 'Section 1 Title', 'Column One'), zero fake lore, zero AI filler,
  and responsive DOM structures (table-container, pre code, section anchors). Provisions two standard
  canvas variants: Style-Agnostic (functional containment with zero theme colors for CMS integration)
  and BECSS Styled Document (complete responsive HTML shell with embedded BECSS Tri-Color styling #DE2626).
  Use when generating, scaffolding, or deploying blank ready-to-populate HTML document skeletons.
  Do NOT use for high-level UX design standards or typography contracts (use design-html-document-preferences),
  BEJSON CMS article skeletons (use template-bejson-cms-skeleton), or low-level BEJSON tables (use template-104-template).
---

# template-html-document-skeleton (Layer 4 Presentation & Design)

## Summary

`template-html-document-skeleton` provisions standardized, blank, production-ready HTML document templates engineered for Markdown-to-HTML conversions, documentation exports, and CMS ingestion. Operating within the **Template Domain** (`template-*` / Domain 2), it strictly enforces the **Zero-Filler Skeleton Law**: every generated template contains pure semantic scaffolding, responsive containment hooks, and literal placeholder labels (`Document Title`, `Section 1 Title`, `Value 1`) with **zero simulated content, zero lorem ipsum, and zero marketing fluff**.

---

## When to Use

- Deploying fresh, blank HTML document canvases for offline authoring or programmatic Markdown conversion.
- Generating structural skeletons carrying responsive table containment (`<div class="table-container"><table>...</table></div>`).
- Deploying the **Style-Agnostic** document canvas (recommended default) to allow host CMS stylesheets (`dark.css` or `light.css`) or publishing engines to apply themes dynamically without CSS collisions.
- Deploying the **BECSS Styled** document canvas for self-contained, standalone HTML files featuring the canonical BECSS Tri-Color palette (`#DE2626`).
- Scaffolding templates for conversion tools such as `MD_To_HTML`.

## When NOT to Use

- Establishing high-level conversion design rules, typography scales, or sanitization gates (use [`design-html-document-preferences`](file:///data/data/com.termux/files/home/.gemini/config/skills/design-html-document-preferences/SKILL.md)).
- Scaffolding BEJSON CMS-specific multi-layer articles or cards (use [`template-bejson-cms-skeleton`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-bejson-cms-skeleton/SKILL.md)).
- Generating 8-lane / 16-sublane spatial BEHTML document layouts (use [`behtml-templates`](file:///data/data/com.termux/files/home/.gemini/config/skills/behtml-templates/SKILL.md)).
- Scaffolding BEJSON 104 data tables (use [`template-104-template`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-104-template/SKILL.md)).

---

## 1. Zero-Filler Skeleton Law (Domain 2 Contract)

Per the ecosystem-wide Zero-Filler Skeleton Law:
1. **Zero Hallucinated Articles**: Never generate simulated essays, fake documentation, or synthetic text when providing a template.
2. **Literal Structural Labels**:
   - Document Title: `Document Title`
   - Section Headings: `Section 1 Title`, `Section 2 Title`
   - Section Content: `Section 1 Content Body`
   - Table Headers: `Header 1`, `Header 2`
   - Table Cells: `Value 1`, `Value 2`
   - Code Block: `Code Content 1`
   - Metadata Attribution: `Author: Author Name • Date: YYYY-MM-DD`
3. **Pristine Class Fidelity**: Skeletons must carry responsive containment hooks:
   - Root Container: `<article class="bejson-cms-article">`
   - Section Anchors: `<section class="article-section" id="section-N">`
   - Table Wrappers: `<div class="table-container"><table>...</table></div>`
   - Syntax Elements: `<pre><code class="language-text">...</code></pre>`

---

## 2. Bundled Canvas Archetypes

This skill provisions two canonical blank skeletons in `templates/`:

1. **Style-Agnostic Document Skeleton (Default Recommendation)**:
   [`templates/blank_style_agnostic_document.html`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-html-document-skeleton/templates/blank_style_agnostic_document.html)
   - Contains ONLY functional containment styles (`max-width: 100%`, `overflow-x: auto`, `border-collapse`, `.table-container`).
   - Zero hardcoded colors or fonts. Automatically inherits the styling of any host CMS or stylesheet (`dark.css` or `light.css`).

2. **BECSS Styled Document Skeleton**:
   [`templates/blank_becss_styled_document.html`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-html-document-skeleton/templates/blank_becss_styled_document.html)
   - Full standalone document styling with the BECSS Tri-Color system (`--primary-color: #DE2626`, `--background-color: #FFFFFF`, `--text-color: #111111`, `--border-color: #E0E0E0`).
   - Responsive layout, styled table borders, code block formatting, and article footer metadata bar.

---

## 3. Deployment & Instantiation Protocol

To instantiate a fresh HTML document canvas:
```bash
# 1. Optimal Style-Agnostic canvas:
cp ~/.gemini/config/skills/template-html-document-skeleton/templates/blank_style_agnostic_document.html my_document.html

# 2. Standalone BECSS Styled canvas:
cp ~/.gemini/config/skills/template-html-document-skeleton/templates/blank_becss_styled_document.html my_styled_document.html
```
Upon copying, replace literal placeholders (`Document Title`, `Section 1 Title`, etc.) with production content.
