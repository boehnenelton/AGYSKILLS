# Specification: Pre-Packaged MTV Domain Blueprints

**Status**: Canonical Standard Reference  
**Parent Skill**: `taxonomy-ui-component-architect` (Layer 5)  
**Release Version**: 300  
**Format Creator**: Elton Boehnen  
**Location**: Roseburg, Oregon, United States  
**Effective Date**: October 2026  
**RELATIONAL_ID**: `4d2c8e1a-5b9f-4318-ae76-9c0d3a2f8b1e`

---

## 1. Architectural Overview

The **MTV (Model-Template-View) Domain Blueprints** provide pre-packaged, standardized scaffolding units for common web domain archetypes. Rather than manually designing data schemas and guessing front-end UI needs, each blueprint pairs:
1. **The Model ($M$)**: Validated BEJSON 104 entity stores (`schemas/data/*.bejson`) with canonical snake_case prefixes, synthetic UUID primary keys at column index 0, and explicit foreign keys (`<prefix>_<target>_uuid_fk`).
2. **The Template ($T$)**: Zero-filler 8-lane BEHTML scaffold templates (`templates/*.html`) adhering to $R_y = 32\text{px}$ row quantization and Policy §8.1 Tri-Color visual branding (`#060606`, `#FFFFFF`, `#DE2626`).
3. **The View ($V$) / Interface**: Deterministically projected 5-Tier ASCII UI Component Maps synthesizing host admin panels, data tables, form inputs, toolbars, and action footers.

The blueprints reside under `blueprints/<blueprint_id>/`.

---

## 2. Canonical Blueprint Roster

### 2.1 Technical Documentation & E-Book Compendium (`documentation`)
* **Archetype Identifier**: `archetype_documentation`
* **Purpose**: Multi-module programming guides, API specifications, and formal e-books.
* **Entities & Prefixes**:
  * `Category` (`cat_`): `cat_uuid`, `cat_name`, `cat_slug`, `cat_order`, `cat_active`
  * `DocumentRecord` (`doc_`): `doc_uuid`, `doc_slug`, `doc_title`, `doc_format`, `doc_toc_level`, `doc_cat_uuid_fk`, `doc_body_html`, `doc_created_at`
  * `SpecificationMetadata` (`spec_`): `spec_uuid`, `spec_doc_uuid_fk`, `spec_version`, `spec_relational_id`, `spec_author`
* **Bound Scaffolds**:
  * `scaffold_document.html`: Formal technical specification layout with widget shelf.
  * `scaffold_consolidated_ebook.html`: Multi-chapter single-page compiled publication.
  * `scaffold_category_feed.html`: Categorized manual index with filter tags.
  * `scaffold_content_page.html`: Uninterrupted widgetless documentation canvas.

### 2.2 Editorial Multi-Author Publication (`editorial`)
* **Archetype Identifier**: `archetype_editorial`
* **Purpose**: Multi-category journalism, editorial blogs, and periodic articles.
* **Entities & Prefixes**:
  * `Category` (`cat_`): `cat_uuid`, `cat_name`, `cat_slug`, `cat_order`, `cat_active`
  * `AuthorProfile` (`author_`): `author_uuid`, `author_display_name`, `author_bio`, `author_avatar_url`
  * `PageRecord` (`page_`): `page_uuid`, `page_slug`, `page_title`, `page_cat_name`, `page_cat_uuid_fk`, `page_author_name`, `page_author_uuid_fk`, `page_type`, `page_created_at`, `page_body_html`
* **Bound Scaffolds**:
  * `scaffold_master_index.html`: Portal homepage with hero featured story, category links, and telemetry grid.
  * `scaffold_feed.html`: Paginated article card stream with author bylines and timestamps.
  * `scaffold_blog_post.html`: Long-form editorial layout with author bio card, social bar, and related posts.

### 2.3 Creative Portfolio & Digital Showcase (`portfolio`)
* **Archetype Identifier**: `archetype_portfolio`
* **Purpose**: Design portfolios, technical showcases, case studies, and image galleries.
* **Entities & Prefixes**:
  * `Category` (`cat_`): `cat_uuid`, `cat_name`, `cat_slug`, `cat_order`, `cat_active`
  * `ProjectShowcase` (`project_`): `project_uuid`, `project_slug`, `project_title`, `project_sub`, `project_tech_stack`, `project_cat_uuid_fk`, `project_overview_html`, `project_spec_meta`
  * `MediaAsset` (`asset_`): `asset_uuid`, `asset_filename`, `asset_original_name`, `asset_mime_type`, `asset_aspect_ratio`, `asset_caption`, `asset_uploaded_at`
* **Bound Scaffolds**:
  * `scaffold_project_showcase.html`: Case study page with spec grid, architecture diagrams, and tech badges.
  * `scaffold_image_feed.html`: Responsive Masonry grid of image cards with aspect ratio preservation.
  * `scaffold_image_lightbox.html`: Modal view overlay for high-resolution visual inspection.

### 2.4 Video Hub & Streaming Archive (`video_hub`)
* **Archetype Identifier**: `archetype_video_hub`
* **Purpose**: Streaming channels, video tutorials, and curated playlists.
* **Entities & Prefixes**:
  * `Category` (`cat_`): `cat_uuid`, `cat_name`, `cat_slug`, `cat_order`, `cat_active`
  * `ExternalMedia` (`extmedia_`): `extmedia_uuid`, `extmedia_slug`, `extmedia_title`, `extmedia_url`, `extmedia_duration_sec`, `extmedia_duration_formatted`, `extmedia_cat_uuid_fk`, `extmedia_created_at`
  * `MediaPlaylist` (`playlist_`): `playlist_uuid`, `playlist_slug`, `playlist_title`, `playlist_desc`, `playlist_extmedia_uuids`, `playlist_created_at`
* **Bound Scaffolds**:
  * `scaffold_video_feed.html`: Video card feed with static poster thumbnails and CSS play badges (anti-lag law).
  * `scaffold_video_player.html`: Dedicated watch page with 16:9 responsive embed iframe and transcript drawer.
  * `scaffold_media_grid.html`: Dense multimedia collection grid with duration badges and playlist switchers.

---

## 3. Projection Workflow: Schema to Interface

To generate the complete 5-Tier UI Component Map for any entity within these blueprints:

```bash
# Project an entity schema to an ASCII Component Tree Map
python3 scripts/project_schema_to_ui.py blueprints/editorial/schemas/data/pagerecord.bejson -e EditorialApp.py

# Verify that the generated map has zero backend database leaks
python3 ../web-ui-component-mapper/scripts/verify_component_map.py path/to/generated_map.txt
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
