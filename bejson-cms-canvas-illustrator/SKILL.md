---
name: bejson-cms-canvas-illustrator
description: >-
  The Graphics Domain: Static Vector Architecture & Banner Illustrator (Layer 5: UI & Visual Interface Automation).
  Generate optimized, context-based SVG architecture diagrams, 1280x640 article hero banners, 1280x720 3-pillar blueprint
  slides, and high-DPI Playwright raster captures (PNG/WebP) for BEJSON CMS and publications using libraries_105 Graphics
  and Canvas families. Renders custom isometric BEJSON cube nodes, laser rays, and peripheral subsystem cards adhering
  to Policy §8.1 Tri-Color standards (#000000, #FFFFFF, #DE2626) and 8-lane quantized geometry. Handles atomic CMS media
  registration in mediaasset.bejson and pagerecord.bejson. Use when creating static featured post imagery, architecture
  schematics, or CMS headers. Do NOT use for multi-frame animations or timeline recordings (use canvas-animation-studio),
  HTML DOM layout composition (use behtml-layout-builder), or drafting blog post markdown prose (use bejson-cms-blog-writer).
---

# `bejson-cms-canvas-illustrator` (Graphics Domain: Static Vector Architecture & Banner Illustrator)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 5 (L5) UI & Visual Interface Automation
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `71929e8c-4c3e-40d6-a371-98fbd4dbf45c`
- **Version**: `1.3.0`
- **Domain**: Graphics Domain (`libraries_105/Lib_PY/Graphics` & `libraries_105/Lib_PY/Canvas`)

## Summary

`bejson-cms-canvas-illustrator` is the authoritative Graphics Domain skill for generating static, context-optimized SVG vector graphics, 1280x640 hero banners, 1280x720 3-pillar architectural diagrams, and Termux Playwright raster captures (high-DPI PNG and WebP) for BEJSON CMS and publications. It connects directly with `libraries_105/Lib_PY/Graphics` (`lib_bejson_Graphics_graphics_core.py`, `render_still_frame`, `render_branding_architecture_slide_svg`) and `libraries_105/Lib_PY/Canvas`, translating article research, titles, and peripheral subsystem nodes into high-impact, brand-aligned visual assets adhering to Policy §8.1 Tri-Color standards. It also provides zero-friction atomic media registration into `mediaasset.bejson` and page linkage in `pagerecord.bejson`.

---

## When to Use

- Generating 1280x640 featured hero banners for BEJSON CMS blog posts (never shipping with `default_page_image.webp`).
- Generating 1280x720 16:9 3-pillar architectural blueprint diagrams for Section 2 of technical deep dives.
- Rendering high-DPI (2x device scale) raster captures via Playwright (`termux_playwright`) alongside vector SVGs.
- Compiling compressed `.webp` assets via PIL for maximum browser compatibility and low bandwidth.
- Registering assets into `storage/mfdb/site_master/data/mediaasset.bejson` with SHA-256 hashes, byte sizes, and MIME types.
- Associating `page_featured_img` in `pagerecord.bejson` by `--page-uuid`.

## When NOT to Use (Mutual Negative Constraints)

- **Code 430**: Do NOT use for multi-frame timeline animations, row-per-frame animations, animated GIFs, or video recordings (use [`canvas-animation-studio`](file:///data/data/com.termux/files/home/.gemini/config/skills/canvas-animation-studio/SKILL.md)).
- **Code 431**: Do NOT use for 8-lane quantized HTML page layouts, UI component grids, or 18-field BEHTMLElement layout datasets (use [`behtml-layout-builder`](file:///data/data/com.termux/files/home/.gemini/config/skills/behtml-layout-builder/SKILL.md)).
- **Code 432**: Do NOT use for authoring blog post markdown text or running the 5-part drafting pipeline (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).
- **Code 433**: Do NOT use for generic external web page scraping or form submissions (use [`playwright-termux-automation`](file:///data/data/com.termux/files/home/.gemini/config/skills/playwright-termux-automation/SKILL.md)).
- **Code 434**: Do NOT use for multi-viewport pixel regression auditing or CSS token checks (use [`playwright-visual-testing`](file:///data/data/com.termux/files/home/.gemini/config/skills/playwright-visual-testing/SKILL.md)).

---

## 1. Architectural Guardrails & Tri-Color Policy

- **Assigned Skill Tier**: Layer 5 (`L5`) UI & Visual Interface Automation
- **Codebase Layer Mapping**: `L5_UI_Visual_Interface_Automation`
- **Domain**: Graphics Domain (`libraries_105/Lib_PY/Graphics` & `libraries_105/Lib_PY/Canvas`)
- **Color Palette (Policy §8.1)**:
  - Background: `#000000` (Pure Black) with `#stageGlow` radial gradient (`#1c0707` -> `#08080c` -> `#000000`)
  - Text: `#FFFFFF` (Pure White) with `#888899` subtitles
  - Laser Accents & Glows: `#DE2626` (Canonical Red) with `#laserGlow` blur filter
- **Geometry**:
  - Hero Banners: `1280x640` (2:1 aspect ratio), 8-lane quantized X-axis (160px intervals across 1280px) and 32px Ry quantized horizontal rows.
  - Architecture Diagrams: `1280x720` (16:9 widescreen), 3 structured pillar cards (360px wide, 36px gaps).
- **Author Crediting**: Elton Boehnen per Policy §9.2.

---

## 2. CLI Tooling & Execution

The skill is driven by [`scripts/cms_canvas_illustrator.py`](./scripts/cms_canvas_illustrator.py).

### Command-Line Arguments

```text
usage: cms_canvas_illustrator.py [-h] [--context-file CONTEXT_FILE]
                                 [--title TITLE] [--subtitle SUBTITLE]
                                 [--components COMPONENTS] [--output OUTPUT]
                                 [--diagram] [--tag TAG] [--no-raster]
                                 [--no-webp] [--register-cms REGISTER_CMS]
                                 [--page-uuid PAGE_UUID] [--termux-tts]
                                 [--export-tts-video EXPORT_TTS_VIDEO]
                                 [--version] [--register] [--config] [--reset]

options:
  --context-file CONTEXT_FILE   Path to 00_context_research.md or 01_plan.md to extract title and components
  --title TITLE                 Override graphic headline title
  --subtitle SUBTITLE           Override telemetry subtitle
  --components COMPONENTS       Comma-separated peripheral components (e.g. 'REST Engine,Vault,Interactions,Dripper')
  --output OUTPUT               Destination path for generated graphic (e.g. storage/mfdb/assets/hero.svg)
  --diagram                     Generate a 1280x720 16:9 3-pillar architectural blueprint diagram instead of hero banner
  --tag TAG                     Format header tag in top right HUD (e.g. 'BEJSON 105a • MFDB v1.40')
  --no-raster                   Skip Playwright browser PNG raster capture, generating pure SVG only
  --no-webp                     Skip WebP compression
  --register-cms REGISTER_CMS   CMS project root path to register assets into mediaasset.bejson automatically
  --page-uuid PAGE_UUID         Target page UUID to associate page_featured_img in pagerecord.bejson
  --termux-tts                  Optional: Speak generated banner title via Termux TTS
  --export-tts-video VIDEO_OUT  Optional: Compile a narrated H.264 MP4 video from generated graphic and TTS voiceover
  --version                     Show version identifier and exit
  --register                    Register utility with central database
  --config                      Display operational configuration parameters
  --reset                       Verify execution environment state
```

### Standard Invocations

#### 1. Turnkey Article Hero Banner with Auto-Registration
```bash
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "ZERO-SQL ARCHIVING: PROJECT CHUNKER" \
  --subtitle "ATOMIC SNAPSHOTS & DETERMINISTIC ARCHIVE REGISTRY" \
  --tag "BEJSON 104a • CHUNKER" \
  --components "Atomic Scoop & Wipe,BEJSON 104a Chunker,Registry Tracker,Web Workstation" \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/project_chunker_ecosystem_hero.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS" \
  --page-uuid "e2dfa590-833d-410f-b3b8-70d85913ea29"
```

#### 2. Turnkey Architecture Blueprint Diagram
```bash
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "BEJSON 105 & MFDB v1.40 ARCHITECTURE" \
  --subtitle "Immutable UUID provenance, federated foreign keys, and loaded chamber logging" \
  --diagram \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/bejson_105_architecture_diagram.svg" \
  --register-cms "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS"
```

---

## 3. Output & Embed Formats

The tool produces both Markdown and BEHTML embed codes:

```html
<!-- BEHTML Featured Hero Header -->
<div class="behtml-featured-header" style="text-align: center; margin: 24px 0;">
  <img src="../../../assets/project_chunker_ecosystem_hero.svg" alt="Zero-SQL Archiving: Project Chunker" style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px; box-shadow: 0 4px 20px rgba(222,38,38,0.2);" />
</div>

<!-- BEHTML Section 2 Architecture Diagram -->
<div class="behtml-featured-header" style="text-align: center; margin: 32px 0;">
  <img src="../../../assets/project_chunker_architecture_diagram.svg" alt="Project Chunker Architecture Blueprint" style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px; box-shadow: 0 4px 20px rgba(222,38,38,0.2);" />
</div>
```

---

## 4. Deterministic Exit Codes

| Exit Code | Semantic Meaning | Recovery Action |
|:---:|---|---|
| `0` | **Success** &mdash; SVG, PNG, and WebP generated and registered successfully. | Embed image link into article plan or header. |
| `10` | **Path Failure** &mdash; Context file or output directory not found. | Verify target file and folder paths. |
| `20` | **Environment Failure** &mdash; Python < 3.10 or missing dependencies. | Ensure execution under Python 3.10+. |
| `30` | **Validation Failure** &mdash; Invalid dimensions or SVG generation error. | Check component names and title syntax. |
