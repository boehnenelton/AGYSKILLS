---
name: project-bejson-cms-manage
description: >-
  Operational CLI workflow execution, entity lifecycle management, health auditing, disaster recovery, dynamic skeleton template promotion, headless static publishing, and single-file Chunked-104a database staging across BEJSON CMS (src/cms-manage.py) and NewAgent CMS (tools/NA-CMS/src/newagent-manage.py). Use when executing cms-manage or newagent-manage commands, authoring two-part pages (manifest + 104db content), drafting and promoting skeleton templates, running headless static site builds, converting media assets to WebP, linking canvas SVG featured banners, or staging database snapshots. Do NOT use for general architectural navigation without CLI actions (use project-bejson-cms-grounding), raw standalone BEJSON table mutations (use bejson-104-core), or general skill scaffolding (use skill-architect).
---

# `project-bejson-cms-manage` (Layer 3 Project Domain Management & Operational CLI)

## Summary

`project-bejson-cms-manage` drives operational CLI execution, content lifecycles, template promotion, static site publication, and disaster recovery across both the foundational **BEJSON CMS** (`/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`) and the streamlined **NewAgent CMS** (`/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS`).

---

## When to Use

- Executing live administrative CLI commands via `newagent-manage.py` (NewAgent CMS) or `cms-manage.py` (BEJSON CMS).
- Managing the **Two-Part Page Lifecycle**: adding, updating, or deleting pages across the manifest `PageRecord` and the standalone 104db content file (`storage/mfdb/pages_db/<uuid>.json`).
- Driving the **Dynamic Skeleton Loader**: drafting, diffing, validating, and promoting HTML templates via `skeleton edit|diff|validate|promote|discard`.
- Executing headless static site publishing via `newagent-manage.py build` (or `publish`).
- Ingesting and optimizing media assets to compressed WebP format via `asset add` and `asset optimize`.
- Generating and linking 1280×640 (2:1 widescreen) or 1280×720 (16:9 HD) SVG canvas featured banners via `canvas-animation-studio` and `page update <uuid> <title> --image <file>`.
- Serving static build previews on port 8000 and launching device browsers via `termux-open`.
- Performing database backups, restores, or Chunked-104a snapshots (`cms_database_chunker.py`).

## When NOT to Use

- Pure architectural navigation or static sitemap inspection without operational CLI execution (use `project-bejson-cms-grounding`).
- Low-level standalone BEJSON CRUD operations outside the CMS domain (use `bejson-104-core`).
- Authoring or scaffolding new agent skill manifests or auditing skill topologies (use `skill-architect`).

---

## 1. Dual Environment & Entrypoint Topology

| System | Root Path | Primary CLI Script | Port Roster | Core Architecture |
|---|---|---|---|---|
| **NewAgent CMS** | `/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS` | `src/newagent-manage.py` | Admin: 5001<br>Publisher: 5001 (or auto +10)<br>Preview: 8000 | Stripped fork: Thin Admin (4 Blueprints) + Publisher; shared Core in `NewAgent/lib/`, CMS libs in `tools_lib/na-cms/` |
| **BEJSON CMS** | `/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS`<br>*(mirror: `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`)* | `src/cms-manage.py` | Admin: 5000<br>Publisher: 5001<br>Editor V2: 5002<br>Profiles: 5003 | Full legacy suite: 4 microservices, disconnected workspace manager (`mount`/`commit`), private `src/lib/` |

---

## 2. NewAgent CMS Operational Workflows (`newagent-manage.py`)

### 2.1 Two-Part Page Persistence Contract
Every page in NewAgent CMS requires a two-part atomic write:
1. **Manifest Row:** Added to `PageRecord` table inside `storage/mfdb/site_master/data/pagerecord.bejson` via `CMSCore`.
2. **Content Document:** Standalone BEJSON 104db file written to `storage/mfdb/pages_db/<page_uuid>.json` containing `PageMeta` and `Content` records.

```bash
# Import Page from HTML (Recommended: reads file directly; supports --type and --featured-img)
python3 src/newagent-manage.py page import --html article.html --title "Article Title" --category "Projects" --author "boehnenelton2024" --type blog --featured-img banner.webp

# Add Page via inline body (Note: --category requires Category NAME like "Projects", not slug; --author requires Author display name)
python3 src/newagent-manage.py page add "Article Title" --category "Projects" --author "boehnenelton2024" --type blog --body article.html

# Update Page Title, Category, Author, or Featured Image
python3 src/newagent-manage.py page update <page_uuid> "Updated Title" --category "Projects" --image banner.webp

# Delete Page (removes both manifest record and pages_db/<uuid>.json file)
python3 src/newagent-manage.py page delete <page_uuid>

# List Pages
python3 src/newagent-manage.py page list
```

### 2.2 Category & Author Management
```bash
# Categories (identified by name on add; identified by slug on update/delete)
python3 src/newagent-manage.py category add "Projects" projects --desc "NewAgent Projects" --type blog
python3 src/newagent-manage.py category update projects "NewAgent Projects"
python3 src/newagent-manage.py category delete projects
python3 src/newagent-manage.py category list

# Authors (identified by display name)
python3 src/newagent-manage.py author add "boehnenelton2024" --bio "Core Architect" --image avatar.webp
python3 src/newagent-manage.py author update "boehnenelton2024" --bio "Updated bio"
python3 src/newagent-manage.py author delete "boehnenelton2024"
python3 src/newagent-manage.py author list
```

### 2.3 Headless Static Site Publishing
Build the complete static publication site directly into `storage/builds/` without launching web servers:
```bash
# Compile and publish static site
python3 src/newagent-manage.py build
# or alias
python3 src/newagent-manage.py publish
```
The build pipeline automatically:
1. Runs pre-publish skeleton validation across active themes.
2. Cleans ephemeral build artifacts in `storage/builds/`.
3. Copies assets from `storage/mfdb/assets/` to `storage/builds/assets/`.
4. Applies `behtml.css` (Ry=32px Y-axis, X0-X7 octal lane grid, Tri-Color `#000000` / `#FFFFFF` / `#DE2626`).
5. Renders polymorphic page routes (`blog/<cat_slug>/<page_slug>/index.html`), category feeds, home index, sitemaps, and robots.txt.

---

## 3. Dynamic Skeleton Loader Architecture (v20.0+)

HTML skeletons reside exclusively on disk under `resources/templates/` and are tracked by `resources/skeleton_registry.json`. Python string literals are completely eliminated.

```text
resources/templates/
  default/              # Canonical live skeletons (Home, Article, Category, Author, App, Apps_Feed, Global)
  _factory/default/     # Read-only factory reset baseline
  <theme>/              # Optional theme overrides
```

### Draft / Diff / Validate / Promote Lifecycle
```bash
# 1. Edit a skeleton in a draft copy (seeded from live file)
python3 src/newagent-manage.py skeleton edit default Article_Skeleton

# 2. View unified diff between draft and live file
python3 src/newagent-manage.py skeleton diff default Article_Skeleton

# 3. Validate tag contracts (exits 1 if required {{tags}} are missing)
python3 src/newagent-manage.py skeleton validate

# 4. Promote draft: backs up current live file to _history/, validates tags, commits as live
python3 src/newagent-manage.py skeleton promote default Article_Skeleton

# 5. Discard draft if changes are abandoned
python3 src/newagent-manage.py skeleton discard default Article_Skeleton

# 6. Clone an entire theme for customization
python3 src/newagent-manage.py skeleton new-theme my-theme --from default
```

---

## 4. Media Ingestion, WebP Optimization & Canvas SVG Banners

### 4.1 Low-Peak-Memory Media Optimization
- Single serial background worker model prevents out-of-memory crashes on mobile/Termux.
- Automatic SHA-256 deduplication rejects duplicate asset uploads.
- WebP batch conversion:
  ```bash
  # Ingest new asset
  python3 src/newagent-manage.py asset add /path/to/image.png

  # Batch convert PNG assets to WebP (88%–94% compression) and patch page references
  python3 src/newagent-manage.py asset optimize
  ```

### 4.2 Canvas SVG Featured Banners (`canvas-animation-studio`)
Optimal featured image dimensions for BEHTML article containers are **1280×640 px (2:1 widescreen)** or **1280×720 px (16:9 HD)**:
1. Render canvas stage using `playwright_canvas_studio.py`:
   ```bash
   python3 ~/.gemini/config/skills/canvas-animation-studio/scripts/playwright_canvas_studio.py \
       --template template_newagent_article_hero_1280x640.html \
       --seek 0.5 \
       --output storage/assets/article_hero.png
   ```
2. Ingest and optimize:
   ```bash
   python3 src/newagent-manage.py asset add storage/assets/article_hero.png
   python3 src/newagent-manage.py asset optimize
   ```
3. Link to page record:
   ```bash
   python3 src/newagent-manage.py page update <page_uuid> "Title" --image article_hero.webp
   ```
4. BEHTML CSS rule in `behtml.css` ensures crisp, uncropped display:
   ```css
   .article-featured-image {
       width: 100%;
       max-width: 100%;
       height: auto;
       aspect-ratio: 2 / 1;
       object-fit: cover;
       margin-bottom: calc(var(--behtml-ry) * 1.5);
       border: 1px solid var(--behtml-ethereal-line);
       display: block;
   }
   ```

---

## 5. Local Preview & Browser Testing

Run an isolated daemon preview server for `storage/builds/` on port 8000 and test immediately on Android:
```bash
# Start background preview server
python3 -m http.server 8000 --directory storage/builds &

# Open live page directly in Android Chrome / system browser
termux-open "http://localhost:8000/blog/projects/<page_slug>/index.html"
```

---

## 6. Legacy BEJSON CMS Operations (`cms-manage.py`)

For the legacy suite at `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`:
- **Cascades:** `category rename <slug> <new_name>` and `category merge <source> <dest>` cascade to referencing page records.
- **Doctor:** `python3 src/cms-manage.py doctor` checks orphaned foreign keys and duplicate names.
- **Snapshot Chunker:**
  ```bash
  python3 scripts/cms_database_chunker.py --site-master
  python3 scripts/cms_database_chunker.py --stage --include-binary
  python3 scripts/cms_database_chunker.py --restore <chunk_file.bejson.txt>
  ```
