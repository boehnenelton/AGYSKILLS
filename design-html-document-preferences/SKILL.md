---
name: design-html-document-preferences
description: >-
  Establish authoritative architectural design standards, typography, viewport containment,
  and formatting rules for converting Markdown into standardized HTML documents. Governs the
  style-agnostic default output contract (<article class="bejson-cms-article">), BECSS Tri-Color
  palette (#FFFFFF, #000000, #DE2626), table containment in <div class="table-container">,
  fenced code syntax blocks in <pre><code class="language-...">, heading hierarchy, callout blocks,
  and zero Word/AI artifact scrubbing. Use when designing, evaluating, or refactoring Markdown-to-HTML
  converters, offline document generators, or publishing workflows. Do NOT use for stamping bare
  blank skeleton canvases (use template-html-document-skeleton), terminal menus (use design-terminal-menu),
  or low-level BEJSON CRUD (use bejson-104-core).
---

# design-html-document-preferences (Layer 4 Presentation & Design)

## Summary

`design-html-document-preferences` codifies the canonical formatting, semantic HTML5 structure, and visual ergonomics for converting Markdown documentation into standardized HTML. As part of the **Design Domain** (`design-*`), it establishes the *governing conversion contracts, responsive containment rules, and aesthetic themes*, while delegating raw structural skeletons to the **Template Domain** (`template-*`).

This standard guarantees that Markdown files converted offline or via automated CLI tools render with 100% typographic fidelity, zero viewport-widening overflow on mobile devices, and full compatibility with Elton Boehnen's **BEJSON CMS** and **BECSS** ecosystem.

---

## When to Use

- Designing or refactoring Markdown-to-HTML conversion engines (such as `MD_To_HTML`).
- Establishing the default **Style-Agnostic** conversion contract: producing semantic HTML wrapped in `<article class="bejson-cms-article">` with functional containment and zero theme bias.
- Applying the **BECSS Tri-Color** styling palette (`--primary-color: #DE2626`, neutral dark/light surfaces) to styled document exports.
- Enforcing responsive horizontal scroll wrapping on data tables (`<div class="table-container"><table>...</table></div>`).
- Formatting code blocks to preserve language indicators (`<pre><code class="language-json">`) without converting JSON or source code into unescaped paragraph tags.
- Sanitizing converted output by stripping Word/Office markup (`<o:p>`, `MsoNormal`) and forbidden AI generation watermarks.

## When NOT to Use

- Stamping out blank, unpopulated HTML document skeletons (use [`template-html-document-skeleton`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-html-document-skeleton/SKILL.md)).
- BEJSON CMS-specific content ingestion rules and microservice blueprint mapping (use [`design-bejson-cms-preferences`](file:///data/data/com.termux/files/home/.gemini/config/skills/design-bejson-cms-preferences/SKILL.md)).
- Terminal console interfaces or CLI menus (use [`design-terminal-menu`](file:///data/data/com.termux/files/home/.gemini/config/skills/design-terminal-menu/SKILL.md)).
- Scaffolding low-level BEJSON 104 data tables (use [`template-104-template`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-104-template/SKILL.md)).

---

## 1. The Two-Mode Output Architecture

All Markdown-to-HTML converters must support two distinct operational modes:

### Mode 1: Style-Agnostic Raw Semantic Document (Default)
The default mode converts Markdown into a clean, unstyled HTML5 document with functional containment:
- **Root Element**: `<article class="bejson-cms-article">`.
- **Styling**: Contains ONLY structural containment rules:
  ```css
  img { max-width: 100% !important; height: auto !important; display: block; }
  pre, code, table, div { max-width: 100% !important; overflow-x: auto; }
  .table-container { width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 1.5rem 0; }
  table { width: 100%; border-collapse: collapse; min-width: 600px; }
  ```
- **Benefit**: Emits zero hardcoded colors or fonts. Automatically inherits the styling of any host CMS or stylesheet (`dark.css` or `light.css`).

### Mode 2: Styled Standalone Document (`--style`)
When explicitly requested with `--style`, the converter wraps the article in a full HTML5 shell with embedded BECSS Tri-Color styling:
- **Palette**:
  - Primary Accent: `#DE2626` (headers, borders, links, strong emphasis).
  - Dark Theme: Background `#050505`, Surface `#0F0F0F`, Text `#FFFFFF`, Border `#222222`.
  - Light Theme: Background `#FFFFFF`, Surface `#F8F8F8`, Text `#111111`, Border `#E0E0E0`.
- **Typography**: Inter for body text, Source Code Pro or Roboto Mono for monospace code.
- **Header**: Document title, author attribution, and date metadata strip.
- **Footer**: Author credits, site URL, and repository links.

---

## 2. Markdown Conversion Invariants

A compliant converter must rigorously parse and translate Markdown constructs:

1. **Fenced Code Blocks**:
   Markdown ` ```lang ` blocks must convert to `<pre><code class="language-lang">...</code></pre>`.
   *Requirement*: Content inside code fences must be HTML-escaped (`&`, `<`, `>`) and NEVER wrapped in `<p>` tags.
2. **Data Tables**:
   Markdown pipe tables (`| Col1 | Col2 |`) must convert to:
   ```html
   <div class="table-container">
     <table>
       <thead><tr><th>Col1</th><th>Col2</th></tr></thead>
       <tbody><tr><td>Val1</td><td>Val2</td></tr></tbody>
     </table>
   </div>
   ```
   *Requirement*: Tables must always be wrapped in `.table-container` to prevent viewport break on mobile.
3. **Headings & Anchor IDs**:
   ATX headings (`#` through `######`) convert to `<h1>` through `<h6>`.
   Headings receive kebab-case IDs (`id="section-slug"`) for deep linking and Table of Contents navigation.
4. **Blockquotes & Callouts**:
   Lines starting with `>` convert to `<blockquote>`. Markdown alerts (`> [!NOTE]`, `> [!IMPORTANT]`) convert to `<blockquote class="callout callout-important">`.
5. **Lists**:
   Bullet lists convert to `<ul><li>`, numbered lists convert to `<ol><li>`, and task checkboxes (`- [ ]`, `- [x]`) convert to `<ul class="task-list"><li class="task-item">`.

---

## 3. Sanitization & Hygiene Gates

Before finalizing HTML output:
1. Strip all Microsoft Word XML/Mso tags (`<o:p>`, `mso-*`, `MsoNormal`).
2. Reject or strip generic AI generation watermarks ("As an AI language model...", "Generated by...").
3. Ensure all image tags carry `loading="lazy"` and `alt` descriptions.
4. Validate UTF-8 character encoding with self-closing or explicit tags.
