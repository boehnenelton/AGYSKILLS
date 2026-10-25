---
name: bejson-cms-publish-automator
description: >-
  Automate static site compilation, local HTTP preview server binding, Android browser
  dispatch via termux-open, and optional multi-viewport 6-screenshot captures for
  BEJSON CMS using Playwright. Use when building static assets, launching preview
  servers, or taking responsive QA screenshots of published BEJSON CMS sites. Do NOT
  use for authoring blog post markdown (use bejson-cms-blog-writer) or generating
  canvas diagrams (use bejson-cms-canvas-illustrator).
---

# bejson-cms-publish-automator (Layer 4 Services & Deployment Automation)

## Summary

`bejson-cms-publish-automator` orchestrates the final deployment, preview, and visual verification lifecycle for Elton Boehnen's zero-SQL BEJSON CMS. It automates static site builds via `BEJSON_CMS_Publisher`, spins up a lightweight preview server on port 8000, launches the Android Chrome browser via `termux-open`, and captures 6 canonical multi-viewport responsive screenshots via Termux Playwright.

---

## When to Use

- Compiling static production HTML builds from BEJSON CMS relational stores.
- Binding and launching the local HTTP preview server (`http://localhost:8000`).
- Dispatching `termux-open` to launch published pages in the Android Chrome app.
- Taking 6 responsive QA screenshots across desktop (1280x720) and mobile (375x812) viewports.
- Executing automated visual regression pixel diffing against baseline screenshots via Pillow (`--visual-diff`).

## When NOT to Use

- Do NOT use for authoring or drafting blog post markdown content (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).
- Do NOT use for raw standalone SVG canvas rendering (use [`bejson-cms-canvas-illustrator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-canvas-illustrator/SKILL.md)).
- Do NOT use for recursive project topic discovery (use [`bejson-cms-admin-scout`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-admin-scout/SKILL.md)).

---

## 1. Architectural Guardrails & 5-Stage Protocol

- **Assigned Skill Tier**: Layer 4 (`L4`) Services & Deployment Automation
- **Codebase Layer Mapping**: `L4_Services_And_Tooling_Ports`
- **The 5-Stage Deployment Pipeline**:
  1. **Static Build**: Executes `BEJSON_CMS_Publisher._execute()` to compile `storage/builds/`.
  2. **Preview Server**: Binds a socketserver/http.server instance on port 8000.
  3. **Browser Dispatch**: Invokes `termux-open http://localhost:8000/index.html`.
  4. **Visual Capture**: Headless Playwright captures 6 canonical surfaces to `images/`.
  5. **Visual Diffing**: Automated pixel-level diffing against `baseline/` screenshots generating delta maps.

---

## 2. CLI Tooling & Execution

The skill is driven by [`scripts/cms_publisher_preview_pipeline.py`](./scripts/cms_publisher_preview_pipeline.py).

### Command-Line Arguments

```text
usage: cms_publisher_preview_pipeline.py [-h] [--cms-root CMS_ROOT]
                                        [--port PORT] [--open-browser]
                                        [--no-browser] [--screenshots]
                                        [--images-dir IMAGES_DIR]
                                        [--visual-diff]
                                        [--baseline-dir BASELINE_DIR]
                                        [--diff-dir DIFF_DIR]
                                        [--manifest MANIFEST]
```

### Standard Invocations

```bash
# Build and preview in Android browser
python3 ~/.gemini/config/skills/bejson-cms-publish-automator/scripts/cms_publisher_preview_pipeline.py

# Build only
python3 ~/.gemini/config/skills/bejson-cms-publish-automator/scripts/cms_publisher_preview_pipeline.py --build-only

# Build, preview, and capture 6 responsive screenshots
python3 ~/.gemini/config/skills/bejson-cms-publish-automator/scripts/cms_publisher_preview_pipeline.py --screenshots
```
