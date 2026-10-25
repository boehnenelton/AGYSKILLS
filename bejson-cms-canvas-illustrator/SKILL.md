---
name: bejson-cms-canvas-illustrator
description: >-
  Generate optimized, context-based SVG diagrams, 1280x640 article hero banners,
  and Playwright raster captures for BEJSON CMS blog posts using the SVG canvas tool
  and libraries_105 Canvas family. Analyzes project source files, research briefs,
  or post plans to render custom isometric BEJSON cube nodes, laser rays, and
  peripheral subsystem cards adhering to Policy §8.1 Tri-Color standards (#000000,
  #FFFFFF, #DE2626) and 8-lane quantized geometry. Use when creating featured post
  imagery or architecture graphics for BEJSON CMS. Do NOT use for basic browser
  automation (use playwright-termux-automation) or multi-viewport visual testing
  (use playwright-visual-testing).
---

# bejson-cms-canvas-illustrator (Layer 4 Services & Media Automation)

## Summary

`bejson-cms-canvas-illustrator` is the dedicated Layer 4 skill for generating context-optimized SVG vector graphics and Playwright raster captures for BEJSON CMS blog posts and NewAgent CMS publications. It directly links with the **SVG Graphic Animation Studio** (`/storage/emulated/0/Admin/Dev/Templates/Canvas_SVG_Capture_Templates/`) and `libraries_105/Lib_PY/Canvas`, translating article research, titles, and extracted module structures into high-impact, brand-aligned visual assets adhering to Policy §8.1 Tri-Color standards.

---

## When to Use

- Generating 1280x640 featured hero banners for BEJSON CMS blog posts.
- Extracting architecture nodes from `00_context_research.md` or `01_plan.md` to illustrate the 4 peripheral subsystem cards.
- Rendering standalone optimized SVG or capturing high-DPI PNGs via Termux Playwright.
- Producing BEJSON cube taxonomy badges (104 Standard, 104a Floating, 104db Pillar, MFDB Federation).
- Outputting ready-to-embed BEHTML and Markdown snippets for direct inclusion in post drafts.

## When NOT to Use

- Do NOT use for generic web page scraping (use [`playwright-termux-automation`](file:///data/data/com.termux/files/home/.gemini/config/skills/playwright-termux-automation/SKILL.md)).
- Do NOT use for multi-viewport pixel regression auditing (use [`playwright-visual-testing`](file:///data/data/com.termux/files/home/.gemini/config/skills/playwright-visual-testing/SKILL.md)).
- Do NOT use for authoring the blog post text or running the 5-part drafting pipeline (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).

---

## 1. Architectural Guardrails & Tri-Color Policy

- **Assigned Skill Tier**: Layer 4 (`L4`) Services & Media Automation
- **Codebase Layer Mapping**: `L4_Services_And_Tooling_Ports`
- **Color Palette (Policy §8.1)**:
  - Background: `#000000` (Pure Black)
  - Text: `#FFFFFF` (Pure White)
  - Laser Accents & Glows: `#DE2626` (Canonical Red)
- **Geometry**: 8-lane quantized X-axis (160px intervals across 1280px canvas) and 32px Ry quantized horizontal rows.
- **Author Crediting**: Elton Boehnen per Policy §9.2.

---

## 2. CLI Tooling & Execution

The skill is driven by [`scripts/cms_canvas_illustrator.py`](./scripts/cms_canvas_illustrator.py).

### Command-Line Arguments

```text
usage: cms_canvas_illustrator.py [-h] [--context-file CONTEXT_FILE]
                                 [--title TITLE] [--subtitle SUBTITLE]
                                 [--components COMPONENTS] [--output OUTPUT]
                                 [--no-raster] [--version] [--register]
                                 [--config] [--reset]

options:
  --context-file CONTEXT_FILE   Path to 00_context_research.md or 01_plan.md
  --title TITLE                 Override graphic headline title
  --subtitle SUBTITLE           Override telemetry subtitle
  --components COMPONENTS       Comma-separated peripheral components (e.g. 'REST Engine,Vault,Interactions,Dripper')
  --output OUTPUT               Destination path for graphic (SVG or PNG)
  --no-raster                   Skip Playwright raster capture; generate pure SVG only
  --version                     Show version identifier and exit
  --register                    Register utility with central database
  --config                      Display operational configuration parameters
  --reset                       Verify execution environment state
```

### Standard Invocations

#### Context-Driven Generation from Research Brief
```bash
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --context-file "~/generate/blog_posts/my_topic/00_context_research.md" \
  --output "/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/hero.svg"
```

#### Explicit Architecture Illustration
```bash
python3 ~/.gemini/config/skills/bejson-cms-canvas-illustrator/scripts/cms_canvas_illustrator.py \
  --title "Zero-SQL CMS Engine" \
  --subtitle "MFDB POSITIONAL ARCHITECTURE" \
  --components "Positional Storage,MFDB Master,REST Engine,Static Generator" \
  --output "~/generate/blog_posts/my_topic/hero.svg" \
  --no-raster
```

---

## 3. Output & Embed Formats

The tool produces both Markdown and BEHTML embed codes:

```html
<!-- BEHTML Featured Header -->
<div class="behtml-featured-header" style="text-align: center; margin-bottom: 24px;">
  <img src="storage/mfdb/assets/hero.svg" alt="Zero-SQL CMS Engine" style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px;" />
</div>
```

---

## 4. Deterministic Exit Codes

| Exit Code | Semantic Meaning | Recovery Action |
|:---:|---|---|
| `0` | **Success** &mdash; SVG and/or raster capture generated successfully. | Embed image link into article plan or header. |
| `10` | **Path Failure** &mdash; Context file or output directory not found. | Verify target file and folder paths. |
| `20` | **Environment Failure** &mdash; Python < 3.10 or missing dependencies. | Ensure execution under Python 3.10+. |
| `30` | **Validation Failure** &mdash; Invalid dimensions or SVG generation error. | Check component names and title syntax. |
