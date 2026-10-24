---
name: code-manual-builder
description: Architect, structure, and generate multi-page technical documentation websites, e-book manuals, and code compendiums with clean SEO hierarchies (root/category/feed.html, root/category/module/index.html, raw file delivery), accessible mobile-responsive hamburger navigation, live feed filtering, hardened self-contained dark-theme CSS, and W3C XML/HTML sitemaps. Use when asked to document a codebase or library ecosystem as an e-book or manual, generate a documentation portal with mobile navigation drawers, structure root/language/feed.html and root/language/module/index.html layouts, or create production documentation websites with raw source delivery. Do NOT use for single-page editorial HTML documents (use publication-html-builder).
---
# Code Manual Builder

Architect, structure, and scaffold high-density, low-padding, dark-themed technical documentation websites, manuals, and e-book compendiums from polyglot codebases or BEJSON Format 105 Multi-File Databases (MFDB). Enforces a clean search-engine-optimized directory structure, self-contained inline dark-theme styling (immune to `file:///` cross-origin stylesheet drops), zero header bulk buttons, trimmed non-redundant telemetry, hardened CSP/accessibility, and complete W3C XML + HTML sitemaps.

## Canonical Directory & SEO URL Structure

```text
root/
├── index.html                                 # Master Portal Overview & Taxonomy Matrix
├── sitemap.html                               # Interactive HTML Site Map (All Routes & Raw Files)
├── sitemap.xml                                # W3C Standard XML Sitemap
├── robots.txt                                 # Crawler Directives & Sitemap Declaration
├── <category_1>/
│   ├── feed.html                              # Category Feed, Instant Filter & Raw Links
│   ├── index.html                             # Direct Directory Alias to feed.html
│   ├── <module_stem_1>/
│   │   ├── index.html                         # Dedicated Module Documentation & Code Viewer
│   │   └── <actual_library_file_1.ext>        # Collocated Raw Source File
│   └── <module_stem_2>/
│       ├── index.html
│       └── <actual_library_file_2.ext>
└── <category_2>/
    ├── feed.html
    ├── index.html
    └── ...
```

## Refined UI, Tight Spacing & Hardening Rules

1. **Self-Contained Inline Dark Theme (Zero CSS Load Failures)**:
   - Canvas `#05070B`, Surface `#0B0F17`, Elevated `#111827`, Code `#04060A`, Border `1px solid #1E293B`, Accent `#DE2626` (BEJSON Crimson).
   - Embed minified CSS directly inside `<style>` in every HTML document `<head>` so local `file:///` browsing and deep subpaths never fail to load external stylesheets.

2. **Slim Padding & High-Density Layout**:
   - Header height `44px` (`padding: 0 0.85rem`), container `max-width: 1100px` (`padding: 0.75rem 0.85rem 1.5rem`), compact `.page-bar` (`padding: 0.65rem 0.85rem`) with a 3px crimson left accent bar, and tight card grids (`gap: 0.6rem`, card padding `0.65rem 0.75rem`).

3. **Zero Header Bulk Buttons & Zero Redundancy**:
   - Never place bulky CTA buttons in `.site-header` or standalone `.action-bar` strips below module headers.
   - Keep `.site-header` strictly to the left hamburger toggle (`#menuToggle`) + brand title and subtle right-side text links (`Site Map · GitHub ↗`).
   - Integrate `Copy Code` and `Raw ⤓` controls directly into `.code-bar` above the `<pre><code>` viewer.
   - Consolidate metadata into a single `.telemetry` row (`Category`, `Subcategory`, `Record UUID`, `Relational ID`, `SHA-256`) without duplicate meta-pill rows or redundant bottom hero banners.

4. **Hardened Security & Accessibility**:
   - Enforce `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; form-action 'none';">` and `X-Content-Type-Options: nosniff`.
   - Bind all UI interactions (`#menuToggle`, `#drawerClose`, `#drawerBackdrop`, `Escape` key, `#searchInput`, `#copyCodeBtn`) inside a strict-mode IIFE with zero inline `onclick`/`onkeyup` attributes.

5. **Comprehensive SEO & Sitemap Suite**:
   - Emit `sitemap.xml`, `sitemap.html`, `robots.txt`, and `<category>/index.html` aliases.
   - Populate every page `<head>` with unique `<title>`, `<meta name="description">`, `<link rel="canonical">`, Open Graph (`og:*`), Twitter Card, and Schema.org `application/ld+json` (`WebSite`, `CollectionPage`, `TechArticle`, `SoftwareSourceCode`).

6. **Clean Main Hub & Collapsed-By-Default Sidebar**:
   - The root `index.html` Main Hub displays ONLY the category cards (`<section class="hub-grid">`) without telemetry boxes, intro banners, or bottom tables.
   - All categories in the sidebar drawer (`.nav-cat`) render folded up (collapsed, `.nav-cat-panel { display: none }`, `aria-expanded="false"`) by default and expand only when clicked.
