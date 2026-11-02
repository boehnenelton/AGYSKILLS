---
name: bejson-cms-blog-writer
description: >-
  Plan, draft, format, assemble, and publish 5-part technical blog posts into BEJSON CMS
  or NewAgent CMS. Conducts automated context research on target project files or URLs to
  anchor plans in verified code signatures. Enforces a 5-turn pipeline: Part 1 generates a
  4-part plan (>=120 lines/section); Part 2 drafts Sections 1-2; Part 3 drafts Sections 3-4;
  Part 4 verifies line counts, zero-filler compliance, and integrates Graphics 105 SVG hero
  banners and Section 2 architecture diagrams via bejson-cms-canvas-illustrator; Part 5 merges
  sections, registers media in mediaasset.bejson, and imports via cms-manage.py or BKS Job
  Studio. Use when authoring multi-part technical blog posts or publishing into BEJSON CMS.
  Do NOT use for initial topic discovery (use bejson-cms-admin-scout), static site publishing
  automation (use bejson-cms-publish-automator), or generating SVG banners (use bejson-cms-canvas-illustrator).
---

# bejson-cms-blog-writer (Layer 5 Use Cases & Publication Drafting)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 5 (L5) Use Cases & Publication Drafting
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `8d123e45-6789-4abc-def0-123456789abc`
- **Version**: `1.3.0`
- **Domain**: Publication Drafting (`BEJSON_CMS` & `NewAgent CMS`)

## Summary

`bejson-cms-blog-writer` is the canonical Layer 5 skill for executing long-form, rigorous technical blog post authoring directly integrated with Elton Boehnen's zero-SQL BEJSON CMS and NewAgent CMS platforms. It combines automated **codebase/website context research** with a strict **5-part sequential pipeline** and mandatory **Graphics 105 visual asset integration**:

0. **Context Research (Target Files / URL)**: Analyzes local project trees (AST signatures, manifests, READMEs) or fetches live website URLs to generate `00_context_research.md`.
1. **Part 1 (Sectional Blueprint & Plan)**: Generates a planned 4-part blog post outline grounded in the researched context where each section has a strict target of **at least 120 lines** (`01_plan.md`).
2. **Part 2 (Drafting Sections 1 & 2)**: Writes Section 1 ($\ge 120$ lines) and Section 2 ($\ge 120$ lines) consecutively, completing and auditing both before moving forward.
3. **Part 3 (Drafting Sections 3 & 4)**: Writes Section 3 ($\ge 120$ lines) and Section 4 ($\ge 120$ lines) consecutively, completing and auditing both before moving forward.
4. **Part 4 (Audit Gate & Canvas Imagery)**: Verifies line counts ($\ge 480$ lines total), eliminates filler, and generates dedicated Policy §8.1 Tri-Color hero banners and Section 2 architecture diagrams via [`bejson-cms-canvas-illustrator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-canvas-illustrator/SKILL.md). **Strict prohibition**: Posts must NEVER ship with `default_page_image.webp`.
5. **Part 5 (Merging, Media Registration & Direct Import)**: Merges all 4 sections into a unified post, registers assets in `mediaasset.bejson`, updates `pagerecord.bejson`, and imports directly to BEJSON CMS using `src/cms-manage.py` or the BKS Job Studio (`lib_bejson_CMS_bks_blog_jobs.py`).

---

## When to Use

- Authoring comprehensive, long-form technical blog posts targeted for BEJSON CMS or NewAgent CMS.
- Grounding articles in deep technical research from local project codebases or live documentation URLs.
- Executing multi-turn drafting workflows requiring minimum 120-line depth per section.
- Drafting 2 sections at a time with verification gates before advancing.
- Generating and embedding context-based SVG canvas imagery and Playwright raster captures.
- Publishing verified markdown and BEHTML content directly into `pagerecord.bejson` and `storage/mfdb/pages_db/<uuid>.json`.

## When NOT to Use

- Do NOT use for multi-chapter standalone technical books or e-books (use [`publication-book-builder`](file:///data/data/com.termux/files/home/.gemini/config/skills/publication-book-builder/SKILL.md)).
- Do NOT use for initial topic discovery across general directories (use [`bejson-cms-admin-scout`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-admin-scout/SKILL.md)).
- Do NOT use for standalone SVG canvas generation without post authoring (use [`bejson-cms-canvas-illustrator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-canvas-illustrator/SKILL.md)).

---

## 1. Architectural Guardrails & 5-Part Protocol

- **Assigned Skill Tier**: Layer 5 (`L5`) Use Cases & Publication Drafting
- **Codebase Layer Mapping**: `L3_Use_Cases_Cross_Layer_Blueprinting`
- **Allowed Downward Dependencies**: Layers 1 through 4 (utilizes `bejson-cms-canvas-illustrator` at L4/L5)
- **The Grounded 5-Part Pipeline**:
  - **Turn 0 (Context Research)**: Automated forensic AST and schema scan on target project codebase or website URL (`00_context_research.md`).
  - **Part 1 (Sectional Blueprint)**: Grounded outline (`01_plan.md`) with explicit $\ge 120$ lines per section target.
  - **Part 2 (Drafting Batch 1)**: Consecutively draft Section 1 ($\ge 120$ lines) and Section 2 ($\ge 120$ lines).
  - **Part 3 (Drafting Batch 2)**: Consecutively draft Section 3 ($\ge 120$ lines) and Section 4 ($\ge 120$ lines).
  - **Part 4 (Audit & Media Integration)**: Line audit gate ($\ge 480$ total lines), BEHTML styling, and mandatory graphic generation via `cms_canvas_illustrator.py`:
    1. 1280x640 Tri-Color SVG Hero Banner + 2x high-DPI Playwright PNG + WebP.
    2. 1280x720 16:9 3-Pillar Architecture Blueprint Diagram embedded into Section 2.
  - **Part 5 (Assembly, Registration & Publishing)**:
    1. Automated section merge and semantic HTML compilation.
    2. Register all generated media into `storage/mfdb/site_master/data/mediaasset.bejson`.
    3. Update `pagerecord.bejson` setting `page_featured_img` to the hero SVG filename.
    4. Save to `storage/mfdb/pages_db/<uuid>.json`.
    5. Copy assets to `storage/builds/assets/` and run `BEJSON_CMS_Publisher._execute()`.
    6. Verify responsive viewports (1280px Desktop & 375px Mobile) with Playwright ensuring `scrollWidth <= clientWidth`.
- **Author Crediting**: Elton Boehnen per Policy §9.2 (`boehnenelton2024`).
- **Color Standards**: Adheres to Policy §8.1 Tri-Color palette (`#FFFFFF`, `#000000`, `#DE2626`).

---

## 2. CLI Tooling & Standard Execution

### A. Step 1: Context Research
```bash
python3 ~/.gemini/config/skills/bejson-cms-blog-writer/scripts/cms_context_researcher.py \
  --target-path "/storage/emulated/0/Admin/Dev/Repos/MyProject" \
  --output "00_context_research.md"
```

### B. Step 2: Graphics Generation & CMS Registration
```bash
# Generate Hero Banner + PNG + WebP & Register in CMS
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "ZERO-SQL ARCHIVING: PROJECT CHUNKER" \
  --subtitle "ATOMIC SNAPSHOTS & DETERMINISTIC ARCHIVE REGISTRY" \
  --tag "BEJSON 104a • CHUNKER" \
  --components "Atomic Scoop & Wipe,BEJSON 104a Chunker,Registry Tracker,Web Workstation" \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/project_chunker_ecosystem_hero.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS" \
  --page-uuid "<target_page_uuid>"

# Generate Section 2 Architectural Blueprint Diagram
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "PROJECT CHUNKER ARCHITECTURE" \
  --subtitle "Deterministic containerization, verified scoops, and multi-version tracking" \
  --diagram \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/project_chunker_architecture_diagram.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS"
```

### C. Step 3: Section Merge & Audit Gate
```bash
python3 ~/.gemini/config/skills/bejson-cms-blog-writer/scripts/bejson_cms_post_merger.py \
  --sections-dir "./sections" \
  --title "Zero-SQL Archiving & Deterministic Snapshots: Dissecting Project Chunker's Ecosystem" \
  --category "Projects" \
  --author "Elton Boehnen" \
  --featured-image "project_chunker_ecosystem_hero.svg" \
  --output-html "./post_merged.html"
```

### D. Step 4: Direct CMS Import & Static Site Build
```bash
# Import post via cms-manage
python3 /storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/src/cms-manage.py page md-import \
  --file "./post_merged.md" \
  --category "Projects"

# Or execute static site build
python3 -c "
import sys; sys.path.insert(0, '/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/src/web')
import BEJSON_CMS_Publisher
BEJSON_CMS_Publisher._execute()
"
```

---

## 3. Post-Publish Verification Protocol

1. **Verify No Default Image Placeholders**:
   Run grep over built HTML to confirm zero occurrences of `default_page_image.webp`.
2. **Synchronize Development Mirror**:
   Always sync modified data and assets between `/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS` and `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`.
3. **Bump Package Version**:
   Increment package integer in `bejson_project.json` and sync `dev/change-log.md`.
4. **Playwright Layout Audit**:
   Verify mobile viewport (375px) to guarantee zero horizontal scroll blowout.
