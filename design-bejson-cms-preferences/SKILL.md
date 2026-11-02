---
name: design-bejson-cms-preferences
description: >-
  Establish authoritative architectural design principles, typography, layout containment,
  Graphics 105 visual standards, and aesthetic rules for authoring HTML documents intended
  for ingestion into BEJSON CMS. Codifies DOM boundary encapsulation (<article class="bejson-cms-article">),
  title extraction priority (<title> over <h1>), section heading progression (<h2> with 5px #DE2626 left borders),
  mobile viewport containment (100% max-width, overflow-x: auto), 1280x640 Policy §8.1 Tri-Color hero banners,
  1280x720 3-pillar architectural blueprint diagrams, and component card grids (.grid, .card).
  Showcases three canonical exemplar documents: Dark Theme, Light Theme, and the optimal Style-Agnostic
  architecture. Use when designing, reviewing, or formatting articles and rich HTML publications for BEJSON CMS.
  Do NOT use for stamping bare blank skeleton canvases (use template-bejson-cms-skeleton), low-level BEJSON CRUD
  (use bejson-104-core), or authoring raw 8-lane BEHTML spatial layouts (use behtml-layout-builder).
---

# design-bejson-cms-preferences (Layer 4 Presentation & Design)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 4 (L4) Presentation & Design
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `2c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f`
- **Version**: `1.3.0`
- **Domain**: Publication Design & Visual Aesthetics (`BEJSON_CMS`)

## Summary

`design-bejson-cms-preferences` establishes the canonical publication design standards, DOM structural rules, and aesthetic patterns for rich HTML documents ingested into Elton Boehnen's **BEJSON CMS**. As part of the **Design Domain** (`design-*`), it is strictly decoupled from the **Template Domain** (`template-*`): design skills establish *governing UX laws, layout mathematics, aesthetic treatments, and showcase exemplars*, whereas template skills stamp out bare mechanical structural skeletons.

This skill ensures that external articles, technical compendiums, multi-part guides, and Graphics 105 visual assets import seamlessly into `BEJSON_CMS_Content.py` without parser errors, styling collisions, or broken mobile viewports.

---

## When to Use

- Designing, formatting, or reviewing HTML articles intended for ingestion into the BEJSON CMS.
- Enforcing the **Graphics 105 Hero Banner Standard** (1280x640, 2:1 widescreen, Policy §8.1 Tri-Color `#000000`, `#FFFFFF`, `#DE2626`, 8-lane quantized geometry, central isometric cube).
- Enforcing the **Graphics 105 Architectural Blueprint Standard** (1280x720, 16:9 widescreen, 3 structured pillar cards) in Section 2 of technical articles.
- Eliminating generic placeholders: strictly barring unreplaced `default_page_image.webp`.
- Enforcing mobile responsive containment (`max-width: 100% !important`, `overflow-x: auto`) for data tables, pre/code blocks, and interactive textareas.
- Applying Policy §8.1 `#DE2626` / Red Tri-Color accenting to article section headers (`border-left: 5px solid #DE2626`), bold text (`<strong>`), and meta highlights.
- Comparing and selecting between **Dark Theme**, **Light Theme**, and **Style-Agnostic** import architectures.

## When NOT to Use

- Stamping out blank, unpopulated skeleton templates ready for content drafting (use [`template-bejson-cms-skeleton`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-bejson-cms-skeleton/SKILL.md)).
- Enforcing raw 8-lane / 16-sublane coordinate quantization or Ry=32px grid math (use [`behtml-layout-builder`](file:///data/data/com.termux/files/home/.gemini/config/skills/behtml-layout-builder/SKILL.md)).
- Running automated headless static site builds or CMS server previews (use [`bejson-cms-publish-automator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-publish-automator/SKILL.md)).
- Operating CMS operational CLI commands (use [`project-bejson-cms-manage`](file:///data/data/com.termux/files/home/.gemini/config/skills/project-bejson-cms-manage/SKILL.md)).

---

## 1. Graphics 105 Visual Standards for Articles

Every published post must feature custom Graphics 105 visual assets adhering to Policy §8.1:

### 1.1 The 1280x640 Hero Banner Architecture
- **Dimensions**: Exactly `1280px` width by `640px` height (2:1 widescreen aspect ratio).
- **Backdrop**: `#000000` base with `#stageGlow` radial gradient (`#1c0707` center glow fading to `#08080c` and `#000000`).
- **Quantized Production Grid**: 8-lane vertical intervals at 160px (`x=160, 320, 480, 640, 800, 960, 1120`) and 32px Ry quantized horizontal rows.
- **Header HUD Telemetry Bar**: Positioned at `y=0` to `y=48` with `#08080a` background and a 1.5px `#DE2626` bottom border. Contains:
  - Subsystem token: `BEJSON CMS // <TOPIC>` (Red monospace, 13px bold)
  - Telemetry subtitle: Centered monospace, 11px
  - Format tag: Right-aligned `BEJSON 104a • MFDB` or `BEJSON 105a • MFDB v1.40`, 12px
- **Central Isometric BEJSON Cube**: Anchored at `(640, 310)` with `#cubeTop` (`#FFFFFF` to `#CCCCCC`), `#cubeLeft` (`#888888` to `#444444`), and `#cubeRight` (`#666666` to `#222222`), framed by a `#DE2626` orbital dashed ring.
- **Peripheral Subsystem Nodes**: 4 distinct cards at `(140, 140)`, `(140, 390)`, `(900, 140)`, and `(900, 390)` with 4px `#DE2626` left indicator strips and laser connectivity rays connecting to the central cube.
- **Headline & Footer**: Centered headline at `y=470` (24px monospace bold) with a 240px red divider bar and author footer `ELTON BOEHNEN • ZERO-SQL ARCHITECTURE` at `y=515`.

### 1.2 The 1280x720 Architectural Blueprint Standard
- **Dimensions**: `1280px` width by `720px` height (16:9 widescreen HD).
- **Layout**: 3 structured pillar cards (360px wide, 36px gap, 450px height) at `y=160`.
- **Placement**: Mandatory in **Section 2** (Architecture Deep Dive) of all technical articles.
- **Content**: Each pillar features 4 bullet features marked by 6x6px `#DE2626` squares and a bottom pill badge.

---

## 2. Canonical Classes & IDs Roster

| Element | Class / ID | Functional Role |
| :--- | :--- | :--- |
| Root Container | `article.bejson-cms-article` | Encapsulates full article body, enforces max-width: 900px |
| Header Wrapper | `header.article-header` | Contains title, meta details, and divider bar |
| Article Title | `h1.article-title` | Primary title display |
| Metadata Strip | `div.article-meta-bar` | Flexbox row displaying author, category, date, engine |
| Hero Banner Wrap| `div.featured-banner-wrapper`| Centered wrapper for primary featured image |
| Hero Image | `img.article-featured-image` | 16:9/2:1 aspect-ratio image binding to CMS lightbox |
| Section 2 Diagram| `div.behtml-featured-header` | Centered wrapper with red border for architectural blueprints |
| Abstract Box | `div.executive-abstract` | Highlight callout with red left border |
| Table of Contents| `nav.table-of-contents` | Numbered anchor navigation linked to `#section-N` |
| Section Wrapper | `section.article-section` | Major content block identified by `id="section-N"` |
| Section Title | `h2` | Section heading receiving 5px #DE2626 left border |
| Table Wrapper | `div.table-container` | Enforces horizontal scroll on mobile viewports |
| Table Data | `table` | Clean border-collapse table with `thead` / `tbody` |
| Code Container | `pre` | Syntax-highlighted block with horizontal scroll |
| Inline Code | `code` | Monospace code snippet font |
| Schema Box | `div.schema-box` | Container for editable/selectable raw BEJSON payload |
| Schema Textarea| `textarea` | Readonly monospace box with `onclick="this.select();"` |
| Card Grid | `div.grid` | Responsive multi-column container (`minmax(260px, 1fr)`) |
| Card Element | `div.card` | Elevated component surface with hover elevation |
| Card Badge | `span.card-type` | Uppercase bold accent tag identifying component type |
