# Web Taxonomy Planning Specification (Domain 1 Standards)

## 1. Principles of Unified Web Taxonomies
In traditional development, relational database schemas and URL directory hierarchies are managed in silos. The Web Taxonomy Domain unifies them under the principle of **Taxonomic Filesystem Isomorphism**:
1. **Fields define data attributes** within records (`<prefix>_uuid`, `<prefix>_title`, `<prefix>_slug`).
2. **Taxonomies define physical directory branches** on disk (`/links/`, `/blog/`, `/wiki/`).
3. **Categories define physical partition subfolders** (`/links/partners/`, `/wiki/a/animals/`).

## 2. Entity Prefix & Snake Case Rules
- Immutable lowercase prefix + underscore:
  - `link_`
  - `partner_`
  - `blog_post_`
  - `wiki_entry_`
  - `doc_spec_`
- Standardized Suffixes:
  - `_uuid`: String UUIDv4.
  - `_slug`: String, lowercase alphanumeric with hyphens.
  - `_title`: String, display title.
  - `_content_markdown`: Long text content.
  - `_timestamp`: ISO-8601 UTC timestamp.
  - `_flag`: Integer or Boolean (0 or 1).

## 3. Tabular Classification for Horizontal Scroll Tables
The Taxonomy Planner classifies which fields are tabular attributes:
- For example: `partner_tier`, `partner_location`, `partner_license_key`, `wiki_entry_taxonomic_class`.
- When marked with `"display_target": "table"`, the Templator and Framework Planner know to lay out these attributes in a horizontally scrollable container:
  ```html
  <div class="fw-table-scroll" role="region" aria-label="Reference Data Table" tabindex="0">
    <table>...</table>
  </div>
  ```

## 4. Manifest Structure
The output is always written to `104a.taxonomy_schema.bejson` using BEJSON 104a format with field map caching.
