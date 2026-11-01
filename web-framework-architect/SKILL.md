---
name: web-framework-architect
description: >-
  Architect, compile, and validate deterministic website routing systems marrying taxonomies to templates per the 12 Invariant Laws of Web Frameworks. Governs Domain 3 (The Web Framework Domain) of the Three-Domain Web Architecture. Enforces Taxonomic Filesystem Isomorphism, Universal Directory Index Resolution (index.html mandate), Page-Style Default vs. Blog Feed Exception, Default-Collapsed Sidebar Navigation Trees ('Classified to Fall'), Universal Horizontal Overflow Scrolling (.fw-docked-toolbar, .fw-table-scroll, .fw-breadcrumb-rail), and Terminal Node Cardinality (folder_index vs. flat_html vs. category_direct). Emits canonical 104a.web_framework.bejson manifests and compiles static multi-tier websites with relative path mathematics. Use when compiling website routing, binding templates across folder depths, synthesizing sidebar trees, or enforcing web framework routing laws. Do NOT use for planning database fields or taxonomy categories (use web-taxonomy-planner), designing visual HTML/CSS templates (use large-website-architect or template-architect), multi-domain workflow orchestration (use web-domain-coordinator), or reverse-engineering existing websites (use ui-navigation-decomposer).
---

# Web Framework Architect (Domain 3: The Web Framework Domain)

The **Web Framework Architect** governs **Domain 3 (The Web Framework Domain)** of the Three-Domain Web Architecture. A **Web Framework** is neither a database schema nor an HTML stylesheet. It is the **active structural contract, routing topology engine, navigation tree synthesizer, and binding rulebook** that marries a **Taxonomy** (from Domain 1) to a set of **Templates** (from Domain 2) to compile a deterministic, self-consistent website architecture.

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
            | 1. Content Style Assignment:                          |
            |    - Page Style (with opening/docs) for all sections  |
            |    - Feed Style ONLY for Blog (/blog/)                |
            | 2. Hub Mode Selection:                                |
            |    - Section Docs + Table vs. Section Docs + Grid     |
            | 3. Terminal Node Option Selection:                    |
            |    - Folder (/partner1/index.html) for multi-page     |
            |    - Flat (/partner.html) for single-page             |
            |    - Direct Category (/blog/cat/index.html) for blog  |
            |    - N-Tier Folder (/wiki/a/animals/cat/index.html)   |
            | 4. Depth-to-Template Binding Matrix:                  |
            |    - Maps exact Template Files to Depths 0, 1, 2, 3, 4|
            | 5. Global Navigation Synthesis:                       |
            |    - Compiles full Taxonomy into Default-Collapsed    |
            |      Sidebar Tree + Horizontal-Scroll Breadcrumbs     |
            | 6. Field-to-Slot Hydration:                           |
            |    - Maps Taxonomy DB Fields into Template Tables/Text|
            +-------------------------------------------------------+
```

### Strict Negative Constraints & Guardrails
- **NEVER Invent Database Fields or Taxonomies**: The Framework Planner never invents database columns, entity prefixes, or logical categories out of thin air. It consumes the taxonomy contract emitted by [`web-taxonomy-planner`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-taxonomy-planner/SKILL.md).
- **NEVER Design Visual Templates or Raw CSS From Scratch**: The Framework Planner never drafts raw HTML wireframes, CSS styles, or 8-lane grid measurements. It selects and binds existing design files provided by [`large-website-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/large-website-architect/SKILL.md) and [`template-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-architect/SKILL.md).
- **NEVER Violate the 12 Invariant Laws**: Any compiled website that breaks `index.html` resolution, turns non-blog hubs into bare link feeds, or fails to initialize sidebar trees in the collapsed state will fail validation.

---

## 2. The 12 Invariant Laws of Web Frameworks

Every framework built or executed within this ecosystem must obey these twelve foundational laws:

### Law 1: The Law of Taxonomic Filesystem Isomorphism
The physical folder structure on disk must mirror the logical URL taxonomy 1:1. Never obscure taxonomic hierarchy behind opaque query strings (`?cat=12&id=99`) or flat unorganized root directories. If an entity belongs to the `links` taxonomy under the `partners` category, its physical path must reside under `/links/partners/`.

### Law 2: The Law of Universal Directory Index Resolution (`index.html` Mandate)
Every directory level within a taxonomy must resolve cleanly via a bare trailing-slash URL (`site.domain/taxonomy/` or `site.domain/taxonomy/category/`) by housing a canonical `index.html` file. No directory in the taxonomic path may exist as an un-indexed "dead folder" that exposes a raw server directory listing or returns a 403/404 error.

### Law 3: The Law of Page-Style Default vs. Blog Feed Exception
A Web Framework strictly distinguishes between **Page-Style Taxonomies (The Universal Default)** and **Feed-Style Taxonomies (Reserved Strictly for Blogs)**:
- **Page-Style Mandate (All Non-Blog Taxonomies & Categories)**: Unless a taxonomy is explicitly a chronological **Blog**, every taxonomy hub (`site.domain/taxonomy/index.html`) and category page (`site.domain/taxonomy/category/index.html`) **MUST be a Page-Style document**. It must contain substantive page content directly related to that section or taxonomy—such as an opening essay, a domain description, architectural documentation, usage guidelines, or a structured reference matrix. **It must NEVER be just a bare feed of links.**
- **Feed-Style Exception (Exclusive to Blog Taxonomies)**: Only a **Blog** taxonomy (`site.domain/blog/` and `site.domain/blog/category/index.html`) uses a pure **Feed Style** as its primary main-canvas layout, because blog consumption is inherently chronological and stream-driven.
- **Why Bare Link Feeds Are Forbidden on Non-Blog Hubs**: Because global and taxonomic navigation is handled comprehensively by the **Collapsible Sidebar Tree** and **Breadcrumb Rail**, turning a non-blog taxonomy or category `index.html` into a glorified list of links wastes the main viewport and deprives the section of its own authoritative documentation.

### Law 4: The Law of Sidebar Navigation Authority & Default-Collapsed Taxonomy Trees
Primary navigation across taxonomies, categories, and subcategories belongs in the **Sidebar**, not scattered as crutch navigation lists in the main canvas. The sidebar taxonomy tree must:
1. **Initialize in a Default-Collapsed State ("Classified to Fall")**: Every top-level taxonomy branch (`<details class="fw-tree-node">`) initializes closed/collapsed by default so the user sees a clean, high-density overview of the entire site without visual clutter.
2. **Context-Aware Active Expansion**: Only the specific taxonomy branch containing the currently viewed page expands automatically to reveal its active child category and leaf item, visually highlighted via `.is-active`.
3. **Consistent Multi-Depth Syntax**: Nested branches use recursive `<details class="fw-tree-node">` elements indented with `.fw-tree-branch` margin lines.

### Law 5: The Law of Universal Horizontal Scroll on Overflow
Any UI element that can exceed its container's width on narrow screens or dense datasets must be explicitly engineered to horizontally scroll rather than wrapping awkwardly, squishing columns, or causing the global page viewport to break:
- **Docked Toolbars (`.fw-docked-toolbar`)**: Must use `flex-wrap: nowrap; overflow-x: auto; white-space: nowrap;`. Toolbar action buttons and navigation pills never wrap onto a second line.
- **Body Tables (`.fw-table-scroll`)**: Must wrap inside `<div class="fw-table-scroll"><table>...</table></div>` with `overflow-x: auto; max-width: 100%; white-space: nowrap;`.
- **Breadcrumb Trails (`.fw-breadcrumb-rail`)**: Must use `overflow-x: auto; flex-wrap: nowrap; white-space: nowrap;` so deep taxonomic paths scroll cleanly horizontally on mobile viewports.
- **Code Blocks & Tab Strips**: Must use `overflow-x: auto`.

### Law 6: The Law of Breadcrumb Spatial Orientation
Every page rendered below the site root (Depth $\ge 1$) must display a horizontally scrollable Breadcrumb Rail directly above the main article canvas (`.fw-breadcrumb-rail`). Breadcrumbs trace the exact taxonomic lineage from Home (`/index.html`) through intermediate directories to the current page (`aria-current="page"`).

### Law 7: The Law of Explicit Terminal Node Cardinality
A Web Framework must explicitly define the storage model for terminal entity instances:
- **Multi-Page Folder Leaf (`folder_index`)**: Used when an entity requires child sub-pages, local assets, or dedicated documentation (`/links/partners/partner1/index.html`).
- **Single-File Flat Leaf (`flat_html`)**: Used when an entity is a standalone, single-page presentation (`/links/partners/partner.html`).
- **Category-Direct Single Page (`category_direct`)**: Used by Blogs where posts live directly within category directories without per-post sub-folders.
- **N-Tier Encyclopedia Folder (`n_tier_folder`)**: Used by deep hierarchies (`/wiki/a/animals/cat/index.html`).

### Law 8: The Law of Depth-Deterministic Template Binding
Templates from Domain 2 must bind deterministically to specific directory depths:
- Depth 0 (Site Root): `scaffold_master_index.html`
- Depth 1 (Taxonomy Hub): `scaffold_document.html` (or `scaffold_feed.html` for blog)
- Depth 2 (Category Hub): `scaffold_document.html` or `scaffold_media_grid.html` (or `scaffold_category_feed.html` for blog)
- Depth 3+ (Terminal Leaf): `scaffold_project_showcase.html`, `scaffold_blog_post.html`, or `scaffold_content_page.html`

### Law 9: The Law of Upward Metadata & Sidebar Tree Synchronization
When an entity is added, removed, or updated at Depth $N$, all parent directory `index.html` files and the global sidebar tree across every page must synchronize their navigational links and reference tables upward.

### Law 10: The Law of Category-Scoped Horizontal Pagination
In feed-style taxonomies (Blog), pagination controls must be scoped strictly within the active category partition (`/blog/releases/page/2/index.html`), never bleeding across unrelated categories.

### Law 11: The Law of Hybrid Taxonomy Coexistence
A single website can simultaneously host multiple taxonomies governed by different archetypes:
- `/links/` operates as a **Page-Style Directory Framework**.
- `/blog/` operates as a **Feed-Style Chronological Framework**.
- `/wiki/` operates as an **N-Depth Page-Style Encyclopedia Framework**.

### Law 12: The Law of Zero-Fluff Structural Compilation
All generated frameworks, starter templates, and compilation artifacts must use strictly functional, self-describing placeholders (`"Page Title"`, `"Section Heading"`, `"Body Paragraph text"`). Zero lorem ipsum, zero synthetic filler.

---

## 3. Canonical Deliverable: `104a.web_framework.bejson`

The authoritative deliverable produced by the Framework Planner is the BEJSON 104a Web Framework Manifest:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["WebFrameworkManifest"],
  "Site_Identifier": "canonical_web_ecosystem",
  "Fields": [
    {"name": "route_id", "type": "string"},
    {"name": "taxonomy_slug", "type": "string"},
    {"name": "category_slug", "type": "string"},
    {"name": "depth_level", "type": "integer"},
    {"name": "content_style_mode", "type": "string"},
    {"name": "terminal_node_storage_mode", "type": "string"},
    {"name": "bound_template_file", "type": "string"},
    {"name": "sidebar_tree_default_collapsed_flag", "type": "boolean"},
    {"name": "horizontal_scroll_toolbar_flag", "type": "boolean"},
    {"name": "horizontal_scroll_table_flag", "type": "boolean"},
    {"name": "breadcrumb_rail_flag", "type": "boolean"}
  ],
  "Values": [
    [
      "route_root", "", "", 0,
      "page_style", "folder_index", "scaffold_master_index.html",
      true, true, true, false
    ],
    [
      "route_links_hub", "links", "", 1,
      "page_style", "folder_index", "scaffold_document.html",
      true, true, true, true
    ],
    [
      "route_links_partners", "links", "partners", 2,
      "page_style", "hybrid", "scaffold_document.html",
      true, true, true, true
    ],
    [
      "route_blog_hub", "blog", "", 1,
      "feed_style", "category_direct", "scaffold_feed.html",
      true, true, false, true
    ],
    [
      "route_blog_releases", "blog", "releases", 2,
      "feed_style", "category_direct", "scaffold_category_feed.html",
      true, true, true, true
    ],
    [
      "route_wiki_hub", "wiki", "", 1,
      "page_style", "n_tier_folder", "scaffold_document.html",
      true, true, true, true
    ],
    [
      "route_wiki_animals", "wiki", "a/animals", 3,
      "page_style", "n_tier_folder", "scaffold_document.html",
      true, true, true, true
    ]
  ]
}
```

---

## 4. Operational CLI Tooling: `fw_compiler.py`

This skill provides an automated compiler and validator located at `scripts/fw_compiler.py`:

```bash
# Validate a Web Framework manifest and check adherence to the 12 Invariant Laws
python3 ~/.gemini/config/skills/web-framework-architect/scripts/fw_compiler.py --validate 104a.web_framework.bejson

# Compile physical directory tree and synthesize sidebar trees from taxonomy + framework manifests
python3 ~/.gemini/config/skills/web-framework-architect/scripts/fw_compiler.py \
  --taxonomy 104a.taxonomy_schema.bejson \
  --framework 104a.web_framework.bejson \
  --templates-dir ~/.gemini/config/skills/large-website-architect/assets \
  --output-dir ./dist_site
```

---

## 5. Relative Path Resolution Mathematics

When compiling static multi-tier websites without root-relative server hosting, relative paths must calculate deterministically based on depth $D$:

$$\text{Prefix}(D) = \begin{cases} \text{"./"} & \text{if } D = 0 \\ \underbrace{\text{"../"} \times D}_{D \text{ repetitions}} & \text{if } D \ge 1 \end{cases}$$

- Depth 0 (Root `/`): `href="./links/index.html"`
- Depth 1 (`/links/`): `href="../blog/index.html"`, `href="./partners/index.html"`
- Depth 2 (`/links/partners/`): `href="../../wiki/index.html"`, `href="./partner1/index.html"`
- Depth 3 (`/wiki/a/animals/`): `href="../../../index.html"`, `href="./cat/index.html"`
