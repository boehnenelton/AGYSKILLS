---
name: bejson-cms-publish-automator
description: >-
  Automate static site compilation, pre-flight asset synchronization, placeholder health
  checks, local HTTP preview server binding, Android browser dispatch via termux-open,
  responsive layout overflow audits (scrollWidth <= clientWidth), and multi-viewport
  screenshot captures for BEJSON CMS using Playwright. Use when building static assets,
  launching preview servers, auditing published HTML for missing hero graphics, or taking
  responsive QA screenshots of published BEJSON CMS sites. Do NOT use for authoring blog post
  markdown (use bejson-cms-blog-writer) or generating canvas diagrams (use bejson-cms-canvas-illustrator).
---

# bejson-cms-publish-automator (Layer 4 Services & Deployment Automation)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 4 (L4) Services & Deployment Automation
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `b3e4f5a6-7890-4bcd-ef12-3456789abcde`
- **Version**: `1.3.0`
- **Domain**: Services & Tooling Ports (`BEJSON_CMS`)

## Summary

`bejson-cms-publish-automator` orchestrates the complete production build, pre-flight asset synchronization, placeholder auditing, deployment preview, and responsive QA verification lifecycle for Elton Boehnen's zero-SQL BEJSON CMS. It automates static builds via `BEJSON_CMS_Publisher`, ensures all Graphics 105 assets are staged to `storage/builds/assets/`, audits published HTML against unreplaced `default_page_image.webp` placeholders, verifies responsive viewports (zero horizontal overflow across 1280px, 768px, and 375px), spins up preview servers, and synchronizes repositories in lockstep.

---

## When to Use

- Compiling static production HTML builds from BEJSON CMS relational stores (`storage/builds/`).
- Staging and copying newly generated hero vectors, PNGs, and WebPs from `storage/mfdb/assets/` to `storage/builds/assets/`.
- Auditing generated site pages to confirm zero orphan `default_page_image.webp` placeholders exist.
- Running automated Playwright layout audits checking `document.documentElement.scrollWidth <= document.documentElement.clientWidth` across desktop and mobile.
- Binding and launching the local HTTP preview server (`http://localhost:8000`).
- Dispatching `termux-open` to launch published pages in the Android Chrome app.
- Synchronizing changes between `/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS` and `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`.

## When NOT to Use

- Do NOT use for authoring or drafting blog post markdown content (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).
- Do NOT use for raw standalone SVG canvas rendering (use [`bejson-cms-canvas-illustrator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-canvas-illustrator/SKILL.md)).
- Do NOT use for recursive project topic discovery (use [`bejson-cms-admin-scout`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-admin-scout/SKILL.md)).

---

## 1. Architectural Guardrails & 6-Stage Release Protocol

- **Assigned Skill Tier**: Layer 4 (`L4`) Services & Deployment Automation
- **Codebase Layer Mapping**: `L4_Services_And_Tooling_Ports`
- **The 6-Stage Publishing Pipeline**:
  1. **Pre-Flight Asset Sync**: Copy all SVGs, PNGs, and WebPs from `storage/mfdb/assets/` to `storage/builds/assets/`.
  2. **Static Compilation**: Execute `BEJSON_CMS_Publisher._execute()` to compile all pages, category feeds, tags, and sitemaps.
  3. **Placeholder Health Audit**: Scan all compiled `.html` files for `default_page_image.webp`. Any occurrence triggers an immediate build warning identifying articles needing hero banners via `cms_canvas_illustrator.py`.
  4. **Playwright Responsive QA Gate**: Evaluate `scrollWidth <= clientWidth` across:
     - Desktop (1280px)
     - Tablet (768px)
     - Mobile (375px)
     Any horizontal scroll blowout (`scrollWidth > clientWidth`) halts the release.
  5. **Dual-Repo Synchronization**: Synchronize `storage/mfdb/`, `storage/builds/`, and project manifests to `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`.
  6. **Version Bump & Chunker Tracking**: Bump package integer in `bejson_project.json`, record entry in `dev/change-log.md`, and track with Project Chunker (`project_chunker.py --track`).

---

## 2. CLI Tooling & Execution

The skill is driven by [`scripts/cms_publisher_preview_pipeline.py`](./scripts/cms_publisher_preview_pipeline.py).

### Standard Invocations

#### Full Build, Asset Sync, and Responsive Playwright Audit
```bash
python3 ~/.gemini/config/skills/bejson-cms-publish-automator/scripts/cms_publisher_preview_pipeline.py \
  --cms-root "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS" \
  --build-only \
  --screenshots
```

#### Launch Preview Server and Open in Android Browser
```bash
python3 ~/.gemini/config/skills/bejson-cms-publish-automator/scripts/cms_publisher_preview_pipeline.py \
  --cms-root "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS" \
  --port 8000 \
  --open-browser
```

#### Standalone Python One-Liner Compilation & Sync
```bash
python3 -c "
import shutil, sys
from pathlib import Path

repo = Path('/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS')
dev = Path('/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS')

# 1. Sync assets
shutil.copytree(repo / 'storage/mfdb/assets', repo / 'storage/builds/assets', dirs_exist_ok=True)

# 2. Build
sys.path.insert(0, str(repo / 'src/web'))
import BEJSON_CMS_Publisher
BEJSON_CMS_Publisher._execute()

# 3. Sync to development mirror
for sub in ['storage/mfdb/assets', 'storage/builds/assets', 'storage/builds', 'storage/mfdb/pages_db', 'storage/mfdb/site_master/data']:
    shutil.copytree(repo / sub, dev / sub, dirs_exist_ok=True)
print('Static build and dual-repo sync complete.')
"
```

---

## 3. Playwright Verification Snippet

```python
from termux_playwright import launch
from playwright.async_api import async_playwright

async def audit_build_overflow():
    async with async_playwright() as pw:
        browser = await launch(pw, headless=True)
        for vp in [{'width': 1280, 'height': 800}, {'width': 375, 'height': 667}]:
            page = await browser.new_page(viewport=vp)
            await page.goto("file:///storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/builds/index.html")
            sw = await page.evaluate("document.documentElement.scrollWidth")
            cw = await page.evaluate("document.documentElement.clientWidth")
            assert sw <= cw, f"Horizontal overflow detected at {vp['width']}px: scrollWidth={sw} > clientWidth={cw}"
            await page.close()
        await browser.close()
```
