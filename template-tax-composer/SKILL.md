---
name: template-tax-composer
description: >-
  Plan, encapsulate, and compose comprehensive, taxonomy-aware template architectures, site suites, and UI component tree maps directly from backend data taxonomies and entity schemas. Determines the complete roster of required templates for any site archetype (e.g. blog post, home master index, static content page, category feed, author profile, contact form, comments discussion feed) keeping entity prefixes, foreign keys, and 4-layer spatial bounds in mind. Projects backend schemas into 5-tier front-end component hierarchies (host application, functional modules, card containers, toolbars, and atomic controls) with zero unmapped fields. Use when planning required template suites for a project archetype, composing taxonomy-aware site architectures, or generating schema-to-UI component tree maps. Do NOT use for raw backend schema modeling (use component-taxonomy-architect), single-component bare-bones wireframing (use template-architect), sitemap DOM tracing (use ui-navigation-decomposer), or building single-page editorial articles (use publication-html-builder).
---

# Skill: `template-tax-composer` (Layer 5 - Taxonomy-Aware Template Architecture & Planning)

- **Version**: `101`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (L3_Use_Cases_Cross_Layer_Blueprinting)`
- **Era & Library Binding**: `Universal (Cross-Layer Schema-to-Template Planning)`
- **Reference Specifications**: 
  - `references/template_planning_matrix.md`
  - `references/schema_to_ui_projection_spec.md`
  - `references/mtv_domain_blueprints_spec.md`
- **Bundled Execution Tools**:
  - `scripts/compose_template_plan.py`: Encapsulates and plans complete template suites for site archetypes with taxonomy grounding and optional zero-filler HTML scaffolding.
  - `scripts/project_schema_to_ui.py`: Projects backend BEJSON schemas into 5-tier component tree maps with zero unmapped fields.
- **Example Asset**: `assets/sample_blog_template_plan.104a.bejson`
- **Date Created**: `2026-10-19` (Updated `2026-10-24`)
- **RELATIONAL_ID**: `5b2c7e91-4d3f-5a8b-1e0c-8f9a7d6c5b4e`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Purpose

`template-tax-composer` operates at **Layer 5** as the primary architectural engine for planning, encapsulating, and composing complete template suites and component hierarchies grounded directly in backend data taxonomies.

It bridges the gap between raw data schemas and frontend template production:
1. **Template Suite Planning**: Evaluates a site archetype (e.g. blog, documentation portal, video hub, portfolio, community) and deterministically encapsulates every template needed to make the site whole—such as master index, individual post, content page, category/tag feed, author profile, contact form, and comments feed.
2. **Taxonomy & Relational Grounding**: Keeps backend entity taxonomies in mind at every step. Each planned template declares its bound entity prefixes (`cat_`, `author_`, `post_`, `comment_`, `page_`), relational foreign keys (`_fk`), and field semantic types.
3. **Layer Allocation & Zero Unmapped Fields**: Assigns each component to its mathematical stacking depth (Layer 1 Viewport Void, Layer 2 Surface Data Tables/Cards, Layer 3 Contextual Dialogues/Modals, Layer 4 Persistent Chrome) and ensures every backend schema field is projected into either a view readout or an interactive form input.

---

## 2. Template Suite Planning Matrix

For any target domain archetype, `template-tax-composer` encapsulates the full roster of required templates:

| Domain Archetype | Required Template Suite | Primary Entity Prefixes | Layer Allocations |
|---|---|---|---|
| **Editorial Blog** | `index.html` (Master Home Index)<br>`post.html` (Single Article View)<br>`page.html` (Static Content/About/Legal)<br>`feed.html` (Category/Tag Filtered Feed)<br>`author.html` (Author Profile & Bio)<br>`contact.html` (Reader Inquiry Form)<br>`comments.html` (Threaded Discussion Component) | `blog_`, `post_`, `cat_`, `author_`, `comment_`, `tag_` | L1 (Base), L2 (Surfaces), L3 (Discussion Modals), L4 (Persistent Chrome) |
| **Technical Documentation** | `index.html` (Documentation Hub)<br>`article.html` (Spec & Guide Split-Pane)<br>`feed.html` (Module Category Feed)<br>`ebook.html` (Single-File Manual Compendium) | `doc_`, `cat_`, `spec_`, `version_` | L1 (Base), L2 (Surfaces), L4 (Persistent Chrome) |
| **Video Streaming Hub** | `index.html` (Portal Home & Carousels)<br>`player.html` (16:9 Viewport & Playlist Queue)<br>`channel.html` (Creator Profile & Uploads)<br>`feed.html` (Category Stream) | `video_`, `channel_`, `cat_`, `playlist_` | L1 (Base), L2 (Surfaces), L3 (Theater Dialogues), L4 (Persistent Chrome) |
| **Creative Portfolio** | `index.html` (Showcase Grid)<br>`project.html` (In-Depth Case Study)<br>`gallery.html` (Masonry Lightbox Overlay)<br>`about.html` (Resume & Skill Matrix) | `project_`, `asset_`, `client_`, `service_` | L1 (Base), L2 (Surfaces), L3 (Lightbox Modals), L4 (Persistent Chrome) |

---

## 3. Five-Tier Component Architecture Projection

Every template composed through the skill adheres to the canonical five-tier hierarchy:

1. **Tier 1: Entry Surface / Application File**: The primary route file (e.g., `index.html`, `post.html`, `author.html`).
2. **Tier 2: Functional Module / Surface Zone**: High-level domain zone (e.g., `[SECTION] Post Content`, `[SECTION] Author Metadata`).
3. **Tier 3: View Container / Section Card**: Visual boundaries (e.g., `[CARD] Directory Table`, `[SECTION] Input Form`, `[MODAL] Picker Overlay`).
4. **Tier 4: Component Group / Toolbar**: Logical groupings (e.g., `[TOOLBAR] Filter Action Bar`, `Input Group: Metadata Controls`).
5. **Tier 5: Atomic Control / Interactive Action**: Leaf elements (Inputs, Dropdown Selectors, Checkbox Toggles, Confirm Buttons).

---

## 4. Bundled CLI Tools

### 4.1 Template Plan Composer (`scripts/compose_template_plan.py`)
Generates BEJSON 104a and Markdown template plans, and optionally scaffolds bare-bones zero-filler HTML template files:
```bash
python3 scripts/compose_template_plan.py \
    --archetype blog \
    --name "Tech_Chronicle" \
    --output-json assets/sample_blog_template_plan.104a.bejson \
    --output-md references/template_planning_matrix.md \
    --scaffold-dir dist/templates/
```

### 4.2 Schema-to-UI Component Projector (`scripts/project_schema_to_ui.py`)
Synthesizes database-agnostic ASCII component trees from BEJSON schema files:
```bash
python3 scripts/project_schema_to_ui.py <path_to_schema.bejson> --entry-point App_Admin.py --output component_map.txt
```

---

## 5. When to Use & When NOT to Use

### Use When:
- Determining the complete suite of templates required for a project archetype (blog, docs, video hub, portfolio).
- Composing taxonomy-aware site architectures where templates map directly to entity prefixes and relational keys.
- Projecting backend BEJSON schemas into exhaustive 5-tier component trees with zero unmapped fields.
- Scaffolding production-ready zero-filler BEHTML template skeletons.

### Do NOT Use For:
- Authoring low-level database schemas or primary/foreign key definitions $\rightarrow$ Use [`component-taxonomy-architect`](../component-taxonomy-architect/SKILL.md).
- Scaffolding isolated bare-bones structural wireframe containers without domain semantics $\rightarrow$ Use [`template-architect`](../template-architect/SKILL.md).
- Tracing or reverse-engineering DOM trees from existing live web pages $\rightarrow$ Use [`ui-navigation-decomposer`](../ui-navigation-decomposer/SKILL.md).
- Authoring single-page editorial prose publications $\rightarrow$ Use [`publication-html-builder`](../publication-html-builder/SKILL.md).
- Low-level 8-lane / Ry=32px spatial coordinate math $\rightarrow$ Use [`behtml-design-preferences`](../behtml-design-preferences/SKILL.md).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
