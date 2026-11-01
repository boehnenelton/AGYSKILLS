# The 12 Invariant Laws of Web Frameworks

## 1. Executive Summary
A Web Framework is the structural bridge marrying a Taxonomy (Domain 1) to Templates (Domain 2). To ensure deterministic stability, every framework compiled in this ecosystem enforces these 12 Invariant Laws:

1. **Taxonomic Filesystem Isomorphism**: Physical folder paths mirror logical URL routes 1:1 (`/links/partners/`).
2. **Universal Directory Index Resolution**: Every directory houses an `index.html`. Zero dead directories.
3. **Page-Style Default vs. Blog Feed Exception**:
   - Universal Default: Every taxonomy/category hub is a Page-Style document with substantive section documentation or reference tables. Never a bare link feed.
   - Blog Exception: Only `/blog/` hubs feature feed-style streams as primary canvas layouts.
4. **Sidebar Navigation Authority & Default-Collapsed Trees**:
   - Primary navigation lives in the Sidebar.
   - Initial state is default collapsed ("classified to fall") using `<details class="fw-tree-node">`.
   - Only the active branch automatically expands.
5. **Universal Horizontal Scroll on Overflow**:
   - Docked toolbars: `.fw-docked-toolbar` (`overflow-x: auto; flex-wrap: nowrap;`).
   - Body tables: `.fw-table-scroll` (`overflow-x: auto; max-width: 100%;`).
   - Breadcrumbs: `.fw-breadcrumb-rail` (`overflow-x: auto; white-space: nowrap;`).
6. **Breadcrumb Spatial Orientation**:
   - Placed above the main article canvas on all sub-pages ($D \ge 1$).
7. **Explicit Terminal Node Cardinality**:
   - `folder_index`: `/links/partners/partner1/index.html` (multi-page/assets).
   - `flat_html`: `/links/partners/partner.html` (single-page).
   - `category_direct`: `/blog/releases/index.html` (blog streams).
   - `n_tier_folder`: `/wiki/a/animals/cat/index.html` (encyclopedic trees).
8. **Depth-Deterministic Template Binding**:
   - Maps specific templates to depths 0, 1, 2, 3+.
9. **Upward Metadata & Sidebar Tree Synchronization**:
   - Leaf changes propagate upward to parent indices and global sidebar trees.
10. **Category-Scoped Horizontal Pagination**:
    - Feeds paginate strictly within active category partitions.
11. **Hybrid Taxonomy Coexistence**:
    - Different taxonomies on the same site can operate under different framework archetypes simultaneously.
12. **Zero-Fluff Structural Compilation**:
    - Pure functional placeholders (`"Page Title"`, `"Body Paragraph text"`), zero lorem ipsum, zero artificial filler.
