---
name: large-website-architect
description: >-
  Architect, design, and scaffold production-ready large multi-page websites,
  documentation portals, taxonomy feeds, media galleries, and e-books using clean
  BEHTML structural skeletons adhering strictly to 8-lane spatial grids, Ry=32px
  row quantization, BECSS Tri-Color standards, and zero-filler laws. Provides 13
  canonical production templates engineered with horizontal overflow scrolling and
  collapsible sidebar trees. Use when building or scaffolding multi-page websites,
  portals, video feeds, image galleries, documentation hubs, or e-books. Do NOT use
  for database field planning or category hierarchy design (use web-taxonomy-planner),
  website routing compilation (use web-framework-architect), multi-domain workflow
  orchestration (use web-domain-coordinator), or reverse-engineering existing
  websites (use ui-navigation-decomposer).
---

# Large Website Architect (Domain 2: The Template Domain / The Templator)

The **Large Website Architect** governs **Domain 2 (The Template Domain / The Templator)** of the Three-Domain Web Architecture. The Templator is a pure visual, spatial, and defensive UI engineer. Its sole responsibility is to build and maintain the **Reusable Template Design Files** - the structural `.html` and `.css` layout skeletons that websites use to display content.

---

## 1. The Three-Domain Architecture & Domain Boundaries

Website creation is strictly partitioned into three mutually exclusive domains:

```text
+-----------------------------------+       +-----------------------------------+
|     DOMAIN 1: TAXONOMY PLANNER    |       |       DOMAIN 2: THE TEMPLATOR     |
| - Database Field Definitions      |       | - HTML/CSS Visual Design Files    |
| - Entity Schemas (<prefix>_field) |       | - 8-Lane Grid & Ry=32px Layouts   |
| - Website Organizational Structure|       | - Collapsible Sidebar UI Shell    |
|   (links, blog, wiki, categories) |       | - Horizontal-Scroll Toolbars      |
|                                   |       | - Horizontal-Scroll Body Tables   |
+-----------------+-----------------+       +-----------------+-----------------+
                  |                                           |
                  +-------------------+   +-------------------+
                                      |   |
                                      v   v
            +-------------------------------------------------------+
            |            DOMAIN 3: THE FRAMEWORK PLANNER            |
            |   Takes Taxonomy Knowledge + Template Design Files    |
            |   & Articulates the Complete Website System Framework |
            +-------------------------------------------------------+
```

### Strict Negative Constraints & Boundaries
- **NEVER Model Database Fields or Column Types**: The Templator has zero database awareness; it only exposes clean structural placeholder slots (`"Page Title"`, `"Body Paragraph text"`, `"Data Table"`). Database modeling belongs exclusively to **Domain 1 (The Taxonomy Planner)** via [`web-taxonomy-planner`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-taxonomy-planner/SKILL.md).
- **NEVER Make Directory Tree or URL Routing Decisions**: The Templator treats every `.html` design file as an isolated, self-contained viewport canvas. It does not decide whether an entity resolves to `partner1/index.html` vs. `partner.html`, nor which template file binds to Depth 1 vs. Depth 4. System routing belongs exclusively to **Domain 3 (The Framework Planner)** via [`web-framework-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-framework-architect/SKILL.md).
- **NEVER Reverse-Engineer Live Sites**: Analyzing and tracing existing websites belongs to the **Decomposition Domain** via [`ui-navigation-decomposer`](file:///data/data/com.termux/files/home/.gemini/config/skills/ui-navigation-decomposer/SKILL.md).

---

## 2. Defensive Overflow & Spatial Invariants

All templates in Domain 2 are defensively engineered against container overflow and mobile viewport crushing:

1. **Docked Horizontal-Scroll Toolbars (`.fw-docked-toolbar`)**:
   - `display: flex; flex-direction: row; flex-wrap: nowrap; overflow-x: auto; white-space: nowrap;`
   - Height quantized to $R_y = 48\text{px}$ (1.5 units). Action pills and navigation buttons never wrap onto multiple lines.
2. **Body Table Horizontal-Scroll Containers (`.fw-table-scroll`)**:
   - Every `<table>` is wrapped inside `<div class="fw-table-scroll">`.
   - `overflow-x: auto; max-width: 100%; white-space: nowrap;`. Columns preserve readable min-widths without breaking outer page bounds.
3. **Collapsible Sidebar Taxonomy Tree (`.fw-sidebar-tree`)**:
   - Built with native `<details class="fw-tree-node">` elements styled to initialize **collapsed by default ("classified to fall")**.
4. **Horizontal-Scroll Breadcrumb Rail (`.fw-breadcrumb-rail`)**:
   - Quantized to $R_y = 32\text{px}$ height with `overflow-x: auto; white-space: nowrap;`. Deep hierarchical paths scroll smoothly on narrow viewports.
5. **BECSS Tri-Color Standard**: Pure Black (`#060606`, `#101010`), Pure White (`#FFFFFF`, `#CCCCCC`), and Strict Red Accent (`#DE2626`).
6. **Zero-Filler Skeleton Law**: Purely functional placeholders (`"Page Title"`, `"Section Heading"`, `"Body Paragraph text"`, `"Sidebar link1"`, `"Action Button"`). Zero lorem ipsum, zero artificial filler.

---

## 3. The 13 Canonical Production Templates

The skill bundles 13 production-ready scaffold skeletons in `assets/`:

1. `scaffold_master_index.html`: Portal home landing page featuring docked toolbar, hero header, responsive 8-lane card grid, and collapsible sidebar.
2. `scaffold_feed.html`: Taxonomy feed view with horizontal-scroll breadcrumb trail, filter pills, sorted feed items, and pagination controls.
3. `scaffold_category_feed.html`: Subcategory feed view with deep breadcrumbs, subcategory selector pills, stacked item rows, and scoped paging feet.
4. `scaffold_content_page.html`: Documentation and deep article page featuring topbar navigation, red-accent header card, content/code container with copy control, horizontal-scroll table container, and sequential paging feet.
5. `scaffold_consolidated_ebook.html`: Single-file publication e-book format with cover header, interactive table of contents with leader lines, sequential chapter articles, and print styling.
6. `scaffold_video_feed.html`: Video-centric taxonomy feed view with 16:9 media cards, duration badges, author/meta stamps, and pagination.
7. `scaffold_image_feed.html`: Multi-column image gallery feed with aspect ratio preservation, caption bars, and category filtering.
8. `scaffold_media_grid.html`: Mixed multimedia grid supporting both image and video cards with media type tags and timestamp metadata.
9. `scaffold_video_player.html`: Dedicated video playback view featuring a 16:9 primary video stage, action bar, playlist queue sidebar, and metadata table.
10. `scaffold_image_lightbox.html`: Interactive gallery grid with zero-filler modal lightbox overlay, previous/next navigation, and caption slots.
11. `scaffold_document.html`: Split-pane technical documentation layout with default-collapsed sidebar tree (`.fw-sidebar-tree`), horizontal-scroll toolbar (`.fw-docked-toolbar`), breadcrumb rail (`.fw-breadcrumb-rail`), callout boxes, and horizontal-scroll body table (`.fw-table-scroll`).
12. `scaffold_blog_post.html`: Editorial article layout featuring hero title, author byline, prose body container, tag list, and next/prev article navigation.
13. `scaffold_project_showcase.html`: Portfolio showcase layout featuring hero banner, primary media viewport, tech stack tags, structural feature grid, and action bar.
