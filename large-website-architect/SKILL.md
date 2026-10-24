---
name: large-website-architect
description: >-
  Architect, design, and scaffold production-ready large multi-page websites, documentation portals, taxonomy feeds, media galleries, and e-books using clean BEHTML structural skeletons adhering strictly to 8-lane spatial grids, Ry=32px row quantization, BECSS Tri-Color standards, and zero-filler laws. Use when building or scaffolding multi-page websites, portals, video feeds, image galleries, video players, documentation hubs, blog posts, project showcases, or e-book publications. Do NOT use for single-page editorial articles (use publication-html-builder) or raw BEHTML format coordinate math (use behtml-format-core).
---
# Large Website Architect

Framework for architecting, designing, and scaffolding comprehensive multi-page websites, taxonomy feeds, media galleries, documentation hubs, and single-file e-book publications.

## Summary

Provides standardized, zero-fluff BEHTML structural skeletons for building large websites and multimedia portals. Bridges the gap between single-page UI wireframes and full multi-tier site hierarchies, bundling 13 canonical production templates across portals, feeds, media players, galleries, documentation views, and publication layouts.

## When to Use

- Architecting multi-page web applications, knowledge bases, media feeds, or documentation hubs.
- Designing video feeds, image galleries, mixed media grids, video players, or lightbox overlays.
- Creating technical documentation layouts, editorial blog posts, or project portfolio showcases.
- Building single-file publication e-books with interactive tables of contents and chapter anchors.
- Scaffolding production BEHTML websites adhering to 8-lane grids and 32px row quantization.
- Enforcing zero-filler content and strictly functional placeholders across large site projects.

## When NOT to Use

- Scaffolding single-component bare-bones wireframes or isolated dialogs (use template-architect).
- Validating low-level BEJSON tabular records (use bejson-104-validator).
- Populating production content copy (handled by domain authoring workflows).

## Bundled Canonical Templates

The skill bundles 13 production-ready scaffold skeletons in `assets/`:

1. `scaffold_master_index.html`: Portal home landing page featuring a topbar, hero header, category filter bar, search input, responsive 8-lane card grid, and footer.
2. `scaffold_feed.html`: Taxonomy feed view with breadcrumb trail, filter pills, sorted feed items, and pagination controls.
3. `scaffold_category_feed.html`: Subcategory feed view with deep breadcrumbs, subcategory selector pills, stacked item rows, and scoped paging feet.
4. `scaffold_content_page.html`: Documentation and deep article page featuring topbar navigation, red-accent header card, content/code container with copy control, metadata table, and sequential paging feet.
5. `scaffold_consolidated_ebook.html`: Single-file publication e-book format with cover header, interactive table of contents with leader lines, sequential chapter articles, and print styling.
6. `scaffold_video_feed.html`: Video-centric taxonomy feed view with 16:9 media cards, duration badges, author/meta stamps, and pagination.
7. `scaffold_image_feed.html`: Multi-column image gallery feed with aspect ratio preservation, caption bars, and category filtering.
8. `scaffold_media_grid.html`: Mixed multimedia grid supporting both image and video cards with media type tags and timestamp metadata.
9. `scaffold_video_player.html`: Dedicated video playback view featuring a 16:9 primary video stage, action bar, playlist queue sidebar, and metadata table.
10. `scaffold_image_lightbox.html`: Interactive gallery grid with zero-filler modal lightbox overlay (Layer 1, z=32), previous/next navigation, and caption slots.
11. `scaffold_document.html`: Split-pane technical documentation layout with sticky sidebar navigation, callout boxes, and structured prose sections.
12. `scaffold_blog_post.html`: Editorial article layout featuring hero title, author byline, prose body container, tag list, and next/prev article navigation.
13. `scaffold_project_showcase.html`: Portfolio showcase layout featuring hero banner, primary media viewport, tech stack tags, structural feature grid, and action bar.

## Architecture and Spatial Invariants

All templates adhere strictly to the core spatial laws:

- **8-Lane Partitioning**: Page widths divide into 8 equal lanes (12.5% per lane) with zero horizontal overflow.
- **Row Quantization ($R_y = 32\text{px}$)**: Vertical control heights, topbars, and header spacing align to integer multiples of 32px.
- **BECSS Tri-Color Standard**: Pure Black (`#060606`, `#101010`), Pure White (`#FFFFFF`, `#CCCCCC`), and Strict Red Accent (`#DE2626`).
- **Dedicated Paging Feet**: Deep documentation and feed pages include category-scoped pagination bars preserving navigation flow.
- **Zero Filler Content**: All templates use strictly functional placeholders (`Page Title`, `Card Title`, `Body Paragraph text`, `Action Button`).

## Workflow Steps

1. **Determine Site Topology**:
   - Identify the required page types across the site (master portal, feeds, players, galleries, docs, or showcase).

2. **Select Scaffold Skeletons**:
   - Copy the appropriate templates from `assets/` to target project directories.
   - Maintain the standardized relative path structure (`root/category/subcategory/item.html`).

3. **Configure Navigation and Paging**:
   - Bind hierarchical breadcrumbs to parent and grandparent routes.
   - Configure category-scoped paging feet (`Prev`, `Module X of Y`, `Next`) to link sequential pages.

4. **Verify Fluff Compliance**:
   - Run the fluff linter to ensure no unrequested copy, lorem ipsum, or fake metrics were added:
     `python3 skills/template-architect/scripts/scaffold_fluff_linter.py <target-file-or-dir>`

5. **Deliver Deliverables**:
   - Package all generated site files into a ZIP archive and upload to Google Drive following file-delivery rules.

## Gotchas to Avoid

- **Noisy Boxy Borders**: Avoid applying 1px solid borders around every element. Use subtle surface elevation transitions (`#060606`, `#101010`, `#161616`) with red top-accent bars (`#DE2626`).
- **Unscoped Pagination**: Never link pagination footers across unrelated categories. Keep pagination strictly within the active section or language.
- **Filler Content Creep**: Never populate cards or feeds with marketing fluff or fake stats. Keep placeholders strictly functional.
