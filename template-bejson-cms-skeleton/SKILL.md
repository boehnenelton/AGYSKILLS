---
name: template-bejson-cms-skeleton
description: >-
  Scaffold and deploy bare-bones blank templated HTML canvas skeletons for BEJSON CMS
  document ingestion. Enforces the Domain 2 Zero-Filler Skeleton Law with literal placeholder
  labels ('Document Title', 'Section 1 Header', 'Column One'), zero fake lore, zero AI filler,
  and canonical CMS class/ID anchors (bejson-cms-article, article-header, table-container,
  schema-box, grid, card, id="section-N"). Pre-wires slots for 1280x640 Policy §8.1 Tri-Color hero
  banners and Section 2 1280x720 architecture diagrams via cms_canvas_illustrator.py. Deploys three
  standard variants: Style-Agnostic, Dark Theme, and Light Theme. Use when generating or outputting
  blank ready-to-populate HTML document templates for BEJSON CMS articles. Do NOT use for UX design
  principles or aesthetic styling guidance (use design-bejson-cms-preferences), plain BEHTML 8-lane
  web page templates (use behtml-templates), or low-level BEJSON tables (use template-104-template).
---

# template-bejson-cms-skeleton (Layer 4 Presentation & Design)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 4 (L4) Presentation & Design
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a`
- **Version**: `1.3.0`
- **Domain**: Publication Templates & Structural Skeletons (`BEJSON_CMS`)

## Summary

`template-bejson-cms-skeleton` governs the mechanical instantiation and scaffolding of blank, production-ready HTML document templates engineered for frictionless ingestion into Elton Boehnen's **BEJSON CMS**. Operating within the **Template Domain** (`template-*` / Domain 2), it strictly adheres to the **Zero-Filler Skeleton Law**: every generated canvas contains pure structural scaffolding, canonical CSS classes, semantic IDs, literal placeholder labels (`Document Title`, `Section 1 Header`, `Value 1A`), and dedicated slots for Graphics 105 hero banners and Section 2 architecture diagrams with **zero simulated content, zero lorem ipsum, and zero marketing fluff**.

---

## When to Use

- Deploying a fresh, blank, ready-to-write HTML article canvas for BEJSON CMS ingestion.
- Generating structural skeletons carrying canonical CMS DOM hooks (`<article class="bejson-cms-article">`, `.table-container`, `.schema-box`, `.grid`, `.card`).
- Providing users or automated builders with pre-wired section anchors (`#section-1`, `#section-2`, etc.) linked to an automated Table of Contents.
- Pre-wiring the **Featured Hero Image slot** (`.article-featured-image`) and **Section 2 Architecture Blueprint slot** (`.behtml-featured-header`) for handoff to `cms_canvas_illustrator.py`.
- Deploying the **Style-Agnostic** canvas (recommended) to let host CMS stylesheets (`dark.css` / `light.css`) apply styling dynamically.
- Deploying standalone **Dark Theme** or **Light Theme** skeleton variants for offline or preview authoring.

## When NOT to Use

- Exploring UX layout principles, typography rules, or aesthetic showcase exemplars (use [`design-bejson-cms-preferences`](file:///data/data/com.termux/files/home/.gemini/config/skills/design-bejson-cms-preferences/SKILL.md)).
- Generating 8-lane / 16-sublane spatial BEHTML document layouts (use [`behtml-templates`](file:///data/data/com.termux/files/home/.gemini/config/skills/behtml-templates/SKILL.md)).
- Scaffolding BEJSON 104 data tables (use [`template-104-template`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-104-template/SKILL.md)).
- Running CMS publishing or static compilation workflows (use [`bejson-cms-publish-automator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-publish-automator/SKILL.md)).

---

## 1. Zero-Filler Skeleton Law (Domain 2 Contract)

Per the ecosystem-wide Zero-Filler Skeleton Law:
1. **Zero Hallucinated Articles**: Never generate simulated tutorials, mock essays, or synthetic technical manuals when asked for a template.
2. **Literal Structural Labels**:
   - Title: `Document Title`
   - Author: `Author Name`
   - Dates: `YYYY-MM-DD`
   - Sections: `1. Section One Header`, `2. Architecture & System Blueprint`
   - Hero Banner: `<img src="../../../assets/article_hero_placeholder.svg" class="article-featured-image" alt="Article Hero Banner" />`
   - Section 2 Diagram: `<div class="behtml-featured-header" style="text-align: center; margin: 32px 0;"><img src="../../../assets/architecture_diagram_placeholder.svg" alt="Architecture Blueprint" style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px;" /></div>`
   - Table Headers: `Column One`, `Column Two`, `Column Three`
   - Table Cells: `Value 1A`, `Value 1B`, `Value 1C`
3. **Pristine Class Fidelity**: The skeleton must carry every essential CMS class and ID without omission:
   - Root: `article.bejson-cms-article`
   - Header: `header.article-header`, `h1.article-title`, `div.article-meta-bar`
   - Media: `div.featured-banner-wrapper`, `img.article-featured-image`
   - Navigation: `nav.table-of-contents`
   - Sections: `section.article-section[id="section-N"]`
   - Tables: `div.table-container > table`
   - Code: `pre > code`
   - Schemas: `div.schema-box > textarea`
   - Cards: `div.grid > div.card`

---

## 2. Bundled Canvas Archetypes

This skill provisions three canonical blank skeletons in `templates/`:

1. **Style-Agnostic Skeleton (Canonical Recommendation)**:
   [`templates/blank_style_agnostic_import_skeleton.html`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_style_agnostic_import_skeleton.html)
   - Contains ONLY functional containment styles (`max-width: 100%`, `overflow-x: auto`, `border-collapse`, `display: grid`).
   - Zero hardcoded colors or fonts. Automatically inherits active CMS theme (`dark.css` or `light.css`).

2. **Dark Theme Skeleton**:
   [`templates/blank_dark_import_skeleton.html`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_dark_import_skeleton.html)
   - Full dark theme styling with `#050505` background, `#FFFFFF` text, `#0F0F0F` cards, and `#DE2626` red accenting.

3. **Light Theme Skeleton**:
   [`templates/blank_light_import_skeleton.html`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_light_import_skeleton.html)
   - Full light theme styling with `#FFFFFF` background, `#111111` text, `#F8F8F8` cards, and `#DE2626` red accenting.

---

## 3. Deployment & Instantiation Protocol

To scaffold a fresh article canvas for immediate authoring:
```bash
# 1. Optimal Style-Agnostic canvas:
cp ~/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_style_agnostic_import_skeleton.html my_new_article.html

# 2. Standalone Dark Theme canvas:
cp ~/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_dark_import_skeleton.html my_dark_article.html

# 3. Standalone Light Theme canvas:
cp ~/.gemini/config/skills/template-bejson-cms-skeleton/templates/blank_light_import_skeleton.html my_light_article.html
```
Upon copying, populate the literal placeholders (`Document Title`, `Author Name`, etc.) with production content, and replace placeholder image references by running `cms_canvas_illustrator.py`.
