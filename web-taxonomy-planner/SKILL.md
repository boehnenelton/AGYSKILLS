---
name: web-taxonomy-planner
description: >-
  Architect, plan, and formalize backend database field definitions (<prefix>_field) AND website organizational directory hierarchies (links, blog, wiki, docs, categories, partitions) into canonical 104a.taxonomy_schema.bejson manifests. Governs Domain 1 (The Taxonomy Domain) of the Three-Domain Web Architecture. Defines entity prefixes, snake_case column identifiers, primitive data types, primary/foreign keys, tabular display classification for horizontal scroll tables, and physical filesystem taxonomy trees. Use when designing data models, planning website directory structures, structuring multi-tier categories, or creating domain entity schemas. Do NOT use for HTML/CSS visual template design (use web-large-architect or template-architect), website routing compilation or terminal node resolution (use web-framework-architect), multi-domain workflow orchestration (use web-domain-coordinator), or reverse-engineering existing websites (use ui-navigation-decomposer).
---

# Web Taxonomy Planner (Domain 1: The Taxonomy Domain)

The **Web Taxonomy Planner** governs **Domain 1 (The Taxonomy Domain)** of the Three-Domain Web Architecture. It establishes the foundational principle that **taxonomies do not merely define columns in a database table - they govern how information is partitioned, categorized, and structured across physical directories and URL namespaces**.

In this architecture, database schema design and website hierarchy planning are unified into a single coherent domain: **The Taxonomy Domain**.

---

## 1. The Three-Domain Architecture & Domain Boundaries

Website creation is strictly partitioned into three mutually exclusive domains:

```text
+-----------------------------------+
|   DOMAIN 1: TAXONOMY PLANNER      |
| - Database Field Definitions      |  --> Defines WHAT data exists &
| - Entity Schemas (<prefix>_field) |      WHERE it logically lives.
| - Website Organizational Tree     |
+-----------------+-----------------+
                  |
                  | [Handoff: 104a.taxonomy_schema.bejson]
                  v
+-----------------------------------+       +-----------------------------------+
|  DOMAIN 3: THE FRAMEWORK PLANNER  | <---  |      DOMAIN 2: THE TEMPLATOR      |
| - Ingests Taxonomy + Templates    |       | - Reusable HTML/CSS Design Files  |
| - Evaluates Routing & Node Laws   |       | - 8-Lane Grid & Ry=32px Layout    |
| - Synthesizes Sidebar Tree        |       | - Horizontal-Scroll Overflow Laws |
| - Compiles Isomorphic Filesystem  |       | - Zero-Filler Skeletons           |
+-----------------------------------+       +-----------------------------------+
```

### Negative Constraints & Strict Guardrails
- **NEVER Write CSS, HTML, or Spatial Math**: The Taxonomy Planner does not author HTML markup, CSS styling, 8-lane grids, or $R_y = 32\text{px}$ vertical rhythm rules. That is exclusively the responsibility of **Domain 2 (The Templator)** via [`web-large-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-large-architect/SKILL.md) and [`template-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-architect/SKILL.md).
- **NEVER Make URL Routing or Terminal Storage Decisions**: The Taxonomy Planner defines logical relationships and categories, but **never** decides whether an entity resolves to a multi-page directory (`partner1/index.html`) or a flat file (`partner.html`), nor does it bind specific `.html` template files to directory depths. That is exclusively the responsibility of **Domain 3 (The Framework Planner)** via [`web-framework-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-framework-architect/SKILL.md).
- **NEVER Perform Runtime Static Site Compilation**: The Taxonomy Planner emits structured schema and organizational blueprints (`104a.taxonomy_schema.bejson`), but never compiles physical `.html` files on disk.

---

## 2. Core Responsibilities

The Taxonomy Planner executes two coordinated responsibilities:

### 2.1 Responsibility A: Database Field Definitions & Entity Schemas
Defines canonical BEJSON 104/104a record schemas for every entity in the ecosystem:
1. **Canonical Entity Prefix Assignment**:
   - Every domain entity is assigned an immutable, lowercase prefix followed by an underscore:
     - `link_` for directory links.
     - `partner_` for partner directory entities.
     - `blog_post_` for chronological blog articles.
     - `wiki_entry_` for encyclopedia/wiki records.
     - `doc_item_` for technical documentation specifications.
2. **Snake Case Identifiers & Primitive Typing**:
   - Every column uses strict `snake_case` identifiers.
   - Types are strictly primitive: `"string"`, `"integer"`, `"float"`, `"boolean"`.
   - Mandatory standard semantic suffixes:
     - `_uuid`: Immutable UUIDv4 identifier.
     - `_slug`: URL-safe filesystem and route slug.
     - `_title`: Human-readable display title.
     - `_summary_text`: Short descriptive abstract.
     - `_url`: External or target URI.
     - `_timestamp`: ISO-8601 UTC timestamp.
     - `_flag`: Boolean state toggle (`0`/`1` or `false`/`true`).
3. **Tabular Display Classification (Horizontal Scroll Identification)**:
   - Identifies which database fields belong in the top-level main prose section versus which fields should be rendered inside horizontally scrollable body tables (`.fw-table-scroll`).
   - Fields marked with `"display_target": "table"` inform the downstream Framework Planner and Templator to render them in a `<div class="fw-table-scroll"><table>...</table></div>` container.

### 2.2 Responsibility B: Website Organizational Hierarchy & Directory Blueprint
Defines the logical categorization, namespace tree, and parent-child partitions of the website:
1. **Top-Level Taxonomies**:
   - Declares root functional namespaces: e.g., `links`, `blog`, `wiki`, `docs`, `showcase`.
2. **Category & Partition Hierarchies**:
   - Single-tier categories:
     - `links` $\rightarrow$ `partners`, `tools`, `community`
     - `blog` $\rightarrow$ `releases`, `engineering`, `notes`
   - Multi-tier encyclopedic partitions:
     - `wiki` $\rightarrow$ `[a..z]` $\rightarrow$ `[animals, astronomy, ...]` $\rightarrow$ `[cat, dog, ...]`
3. **Entity-to-Category Association**:
   - Maps each entity type to its parent taxonomy and category.

---

## 3. Canonical Deliverable: `104a.taxonomy_schema.bejson`

The authoritative deliverable produced by the Taxonomy Planner is the BEJSON 104a Taxonomy Manifest:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["WebTaxonomyManifest"],
  "Site_Identifier": "canonical_web_ecosystem",
  "Fields": [
    {"name": "taxonomy_id", "type": "string"},
    {"name": "taxonomy_slug", "type": "string"},
    {"name": "taxonomy_display_name", "type": "string"},
    {"name": "parent_taxonomy_id", "type": "string"},
    {"name": "depth_level", "type": "integer"},
    {"name": "entity_prefix", "type": "string"},
    {"name": "content_style_intent", "type": "string"},
    {"name": "schema_fields_json", "type": "string"}
  ],
  "Values": [
    [
      "tax_links_root", "links", "Directory Links", "", 1,
      "link_", "page_style",
      "[{\"name\":\"link_uuid\",\"type\":\"string\"},{\"name\":\"link_title\",\"type\":\"string\"},{\"name\":\"link_url\",\"type\":\"string\"}]"
    ],
    [
      "tax_links_partners", "partners", "Partner Directory", "tax_links_root", 2,
      "partner_", "page_style",
      "[{\"name\":\"partner_uuid\",\"type\":\"string\"},{\"name\":\"partner_title\",\"type\":\"string\"},{\"name\":\"partner_tier\",\"type\":\"string\",\"display_target\":\"table\"},{\"name\":\"partner_url\",\"type\":\"string\"}]"
    ],
    [
      "tax_blog_root", "blog", "Engineering Blog", "", 1,
      "blog_post_", "feed_style",
      "[{\"name\":\"blog_post_uuid\",\"type\":\"string\"},{\"name\":\"blog_post_title\",\"type\":\"string\"},{\"name\":\"blog_post_date\",\"type\":\"string\"}]"
    ],
    [
      "tax_wiki_root", "wiki", "Encyclopedia Wiki", "", 1,
      "wiki_entry_", "page_style",
      "[{\"name\":\"wiki_entry_uuid\",\"type\":\"string\"},{\"name\":\"wiki_entry_title\",\"type\":\"string\"},{\"name\":\"wiki_entry_rank\",\"type\":\"string\",\"display_target\":\"table\"}]"
    ]
  ]
}
```

---

## 4. Operational CLI Tooling: `plan_web_taxonomy.py`

This skill includes an automated CLI tool located at `scripts/plan_web_taxonomy.py` for validating and generating taxonomy manifests:

```bash
# Validate an existing taxonomy blueprint
python3 ~/.gemini/config/skills/web-taxonomy-planner/scripts/plan_web_taxonomy.py --validate blueprint.104a.bejson

# Generate a starter taxonomy manifest for a target domain
python3 ~/.gemini/config/skills/web-taxonomy-planner/scripts/plan_web_taxonomy.py --init --output 104a.taxonomy_schema.bejson
```

---

## 5. Handoff to Domain 3 (The Framework Planner)

Once the Taxonomy Planner finalizes `104a.taxonomy_schema.bejson`, it delegates directly to:
- [`web-framework-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-framework-architect/SKILL.md): Ingests the taxonomy manifest, pairs it with the template catalog from [`web-large-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-large-architect/SKILL.md), assigns terminal node laws and depth bindings, and compiles the physical directory tree.
