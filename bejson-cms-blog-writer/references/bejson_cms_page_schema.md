# BEJSON CMS Two-Part Page Data Contract

## 1. Architectural Overview

BEJSON CMS implements a decoupled **two-part persistence architecture** for web pages and blog posts, dividing metadata from dense content payloads:

1. **Top-Level Manifest** (`pagerecord.bejson`):
   - Fast index table tracking lightweight page headers (`page_id`, `page_title`, `page_slug`, `page_type`, `category_id`, `author_id`, `created_at`, `updated_at`, `status`).
   - Queried during index listing, search filtering, and feed generation without loading full article content.

2. **Dense Content Payloads** (`storage/mfdb/pages_db/<page_id>.json`):
   - BEJSON 104db multi-record document storing full HTML body content, relational revisions, and embedded telemetry.

```text
BEJSON_CMS/
├── data/
│   └── pagerecord.bejson          <-- Lightweight Page Manifest
└── storage/
    └── mfdb/
        └── pages_db/
            └── <uuid>.json        <-- Dense 104db Article Content Payload
```

---

## 2. Page Types & Valid Categories

- **Allowed Page Types**: `blog`, `post`, `page`, `article`
- **Supported Categories**:
  - `BEJSON` (cat_slug: `bejson`)
  - `Uncategorized` (cat_slug: `uncategorized`)
- **Default Author**:
  - `boehnenelton2024` (Display name in `AuthorProfile`)

---

## 3. Direct CLI Management Commands

All operations are executed via `src/cms-manage.py` in the CMS root:

```bash
# Import an HTML blog post (Recommended standard)
python3 src/cms-manage.py page import \
  --html "final_post.html" \
  --title "<title>" \
  --category "BEJSON" \
  --author "boehnenelton2024" \
  --type "blog" \
  --featured-img "hero.svg"

# Add a page directly via inline body
python3 src/cms-manage.py page add "<title>" \
  --category "BEJSON" \
  --author "boehnenelton2024" \
  --type "blog" \
  --body "<html>...</html>"

# List published pages
python3 src/cms-manage.py page list

# Update an existing page
python3 src/cms-manage.py page update <uuid> --title "<new_title>"

# Delete a page
python3 src/cms-manage.py page delete <uuid>
```
