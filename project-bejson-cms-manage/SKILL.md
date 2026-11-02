---
name: project-bejson-cms-manage
description: >-
  Operational CLI workflow execution, entity lifecycle management, health auditing, disaster
  recovery, dynamic skeleton template promotion, headless static publishing, BKS Blog Job Studio
  execution, and Graphics 105 asset orchestration across BEJSON CMS (src/cms-manage.py) and
  NewAgent CMS (tools/NA-CMS/src/newagent-manage.py). Use when executing cms-manage or newagent-manage
  commands, authoring two-part pages (manifest + 104db content), drafting and promoting skeleton templates,
  running headless static site builds, generating context-based hero graphics and architectural blueprints
  via cms_canvas_illustrator.py, or staging database snapshots. Do NOT use for general architectural navigation
  without CLI actions (use project-bejson-cms-grounding), raw standalone BEJSON table mutations (use bejson-104-core),
  or general skill scaffolding (use skill-architect).
---

# `project-bejson-cms-manage` (Layer 3 Project Domain Management & Operational CLI)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 3 (L3) Project Domain Management & Operational CLI
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `5f6a7b8c-9012-4def-ab34-56789abcdef0`
- **Version**: `1.3.0`
- **Domain**: Project Domain Management (`BEJSON_CMS` & `NewAgent CMS`)

## Summary

`project-bejson-cms-manage` drives operational CLI execution, content lifecycles, template promotion, static site publication, and disaster recovery across both the foundational **BEJSON CMS** (`/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS`, mirrored at `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`) and the streamlined **NewAgent CMS** (`/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS`). It codifies complete operational practices for BKS Blog Job Studio workflows, Graphics 105 hero banner generation, 3-pillar architectural diagrams, atomic media asset registration, and static site compilation.

---

## When to Use

- Executing live administrative CLI commands via `cms-manage.py` (BEJSON CMS) or `newagent-manage.py` (NewAgent CMS).
- Managing the **Two-Part Page Lifecycle**: updating manifest `PageRecord` and the standalone 104db content file (`storage/mfdb/pages_db/<uuid>.json`).
- Generating and registering 1280x640 Policy §8.1 Tri-Color hero banners and 1280x720 3-pillar architecture diagrams via `cms_canvas_illustrator.py`.
- Running the **BKS Blog Job Studio** (BKS-1 4-part plan generation, part execution, merging, and approving/overwriting posts).
- Executing headless static site publishing via `BEJSON_CMS_Publisher._execute()` or `cms-manage.py`.
- Running Playwright layout audits checking `scrollWidth <= clientWidth` across desktop (1280px) and mobile (375px).
- Synchronizing development mirrors and tracking project versions via Project Chunker (`project_chunker.py --track`).

## When NOT to Use

- Pure architectural navigation or static sitemap inspection without operational CLI execution (use `project-bejson-cms-grounding`).
- Low-level standalone BEJSON CRUD operations outside the CMS domain (use `bejson-104-core`).
- Authoring or scaffolding new agent skill manifests or auditing skill topologies (use `skill-architect`).

---

## 1. Dual Environment & Entrypoint Topology

| System | Root Path | Primary CLI Script | Port Roster | Core Architecture |
|---|---|---|---|---|
| **BEJSON CMS** | `/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS`<br>*(mirror: `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`)* | `src/cms-manage.py` | Admin: 5000<br>Publisher: 5001<br>PageEditor V2: 5002<br>Profiles: 5003 | Full production suite: 4 microservices, BKS Blog Jobs, CLI_AI 48, Graphics 105 |
| **NewAgent CMS** | `/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS` | `src/newagent-manage.py` | Admin: 5001<br>Publisher: 5001 (or auto +10)<br>Preview: 8000 | Stripped fork: Thin Admin (4 Blueprints) + Publisher; shared Core in `NewAgent/lib/` |

---

## 2. Standard Operational Workflows

### 2.1 Graphics 105 Hero Banner & Diagram Generation
Every CMS post must have a dedicated Policy §8.1 Tri-Color hero banner (never use `default_page_image.webp`) and an architectural blueprint diagram:

```bash
# 1. Generate 1280x640 Hero Banner + PNG + WebP & Register in CMS
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "ZERO-SQL ARCHIVING: PROJECT CHUNKER" \
  --subtitle "ATOMIC SNAPSHOTS & DETERMINISTIC ARCHIVE REGISTRY" \
  --tag "BEJSON 104a • CHUNKER" \
  --components "Atomic Scoop & Wipe,BEJSON 104a Chunker,Registry Tracker,Web Workstation" \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/project_chunker_ecosystem_hero.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS" \
  --page-uuid "e2dfa590-833d-410f-b3b8-70d85913ea29"

# 2. Generate 1280x720 16:9 3-Pillar Architectural Blueprint Diagram
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "PROJECT CHUNKER ARCHITECTURE" \
  --subtitle "Deterministic containerization, verified scoops, and multi-version tracking" \
  --diagram \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/project_chunker_architecture_diagram.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS"
```

### 2.2 Two-Part Page Persistence Contract
Every page in BEJSON CMS consists of:
1. **Manifest Row:** In `storage/mfdb/site_master/data/pagerecord.bejson`.
2. **Content Document:** In `storage/mfdb/pages_db/<uuid>.json` (contains `PageMeta` at row 0, `Content` at row 1).

```bash
# Markdown Import with Category and Author
python3 src/cms-manage.py page md-import \
  --file "/path/to/article.md" \
  --category "Projects"

# Update Featured Image
python3 src/cms-manage.py page update <page_uuid> "Updated Title" --image "project_chunker_ecosystem_hero.svg"
```

### 2.3 Headless Static Site Publishing & Asset Staging
```bash
python3 -c "
import shutil, sys
from pathlib import Path

repo = Path('/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS')
dev = Path('/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS')

# 1. Pre-flight asset staging
shutil.copytree(repo / 'storage/mfdb/assets', repo / 'storage/builds/assets', dirs_exist_ok=True)

# 2. Compile static distribution
sys.path.insert(0, str(repo / 'src/web'))
import BEJSON_CMS_Publisher
BEJSON_CMS_Publisher._execute()

# 3. Synchronize development mirror
for sub in ['storage/mfdb/assets', 'storage/builds/assets', 'storage/builds', 'storage/mfdb/pages_db', 'storage/mfdb/site_master/data']:
    shutil.copytree(repo / sub, dev / sub, dirs_exist_ok=True)
print('Static build and dual-repo sync complete.')
"
```

### 2.4 Version Governance & Project Chunker Registration
Always increment the package version and track the updated baseline:
```bash
# Track registered project in Project Chunker
python3 /storage/emulated/0/Admin/System/Project_Chunker/CLI/project_chunker.py --track "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS"
```

---

## 3. Responsive Playwright QA Audit

Verify that published pages never introduce mobile horizontal scroll blowouts:
```bash
python3 -c "
import asyncio
from termux_playwright import launch
from playwright.async_api import async_playwright

async def audit():
    async with async_playwright() as pw:
        browser = await launch(pw, headless=True)
        page = await browser.new_page(viewport={'width': 375, 'height': 667})
        await page.goto('file:///storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/builds/index.html')
        sw = await page.evaluate('document.documentElement.scrollWidth')
        cw = await page.evaluate('document.documentElement.clientWidth')
        assert sw <= cw, f'Overflow on mobile: scrollWidth={sw} > clientWidth={cw}'
        print('Mobile viewport clean (0 overflow)')
        await browser.close()

asyncio.run(audit())
"
```
