# Large Website Scaffold Architecture

Reference guidelines for building large multi-page websites, portal feeds, category hubs, and documentation e-books adhering to BEHTML and BECSS standards.

## 1. Page Hierarchy & Topology

| Template | Role | Key Components |
| :--- | :--- | :--- |
| `scaffold_master_index.html` | Portal / Home Landing | Hero banner, category navigation bar, search input, 8-lane card grid, footer |
| `scaffold_feed.html` | Taxonomy Feed | Breadcrumbs, filter pills, sorted article/card list, paging feet |
| `scaffold_category_feed.html` | Subcategory View | Deep breadcrumbs, subcategory selector pills, stacked item rows, paging feet |
| `scaffold_content_page.html` | Content / Library View | Topbar, red-accent header card, content/code block with copy, metadata table, paging feet |
| `scaffold_consolidated_ebook.html` | Single-File Publication | Formal cover, interactive table of contents with leader lines, sequential chapter articles, print styles |

## 2. Invariant Spatial Laws

1. **8-Lane Grid Architecture**: Horizontal layouts align strictly across 8 equal lanes (12.5% each).
2. **Row Quantization ($R_y = 32\text{px}$)**: Vertical measurements snap to integer multiples of 32px.
3. **BECSS Tri-Color Standard**: Pure Black (`#060606`), Pure White (`#FFFFFF`), Strict Red Accent (`#DE2626`).
4. **Dedicated Paging Feet**: Deep pages feature category-scoped or language-scoped pagination footers.
5. **Zero Filler Content**: All templates enforce zero fluff, zero fake metrics, and strictly functional placeholders.
