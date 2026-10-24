---
name: readme-visual-enhancer
description: >-
  Author, upgrade, audit, and visually enrich README documentation adhering strictly to professional developer standards: no hardcoded absolute paths (except user environment setup guidance), zero mention of internal policies or rules, and zero AI vocalization or attribution. Enforces deep pre-writing codebase study, hostile post-writing completeness auditing ("Is there anything more to add?"), 2-phase document architecture (first half: setup/usage/features; second half: technical details/architecture), and mandatory Table of Contents. Automates UI visual tours via native Playwright capture, aspect-ratio scaling down to 420px max dimension, and mathematically balanced line interval embedding. Use when writing, refactoring, or visually enhancing README.md files. Do NOT use for raw non-documentation backend code changes or unscaled multi-megabyte image dumping.
---

# Skill: `readme-visual-enhancer`

- **Purpose**: Authoring, hostile auditing, and visual enhancement of production README documentation with 420p aspect-ratio scaling and line-balanced figure embedding.
- **Primary Runtime**: Python 3.10+ (`Pillow`, `termux-playwright`, `argparse`)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `2df20dff-a417-420d-ab06-af92e5418250`
- **Version**: `1.2.0`

---

## 1. Absolute Negative Constraints (Strict Supremacy)

Every README authored, refactored, or enhanced must strictly enforce three negative constraints:

1. **❌ NEVER Hardcode Absolute Paths**:
   - Never embed machine-specific paths (e.g. `/storage/emulated/0/...`, `/data/data/com.termux/...`, `/home/...`).
   - **Single Exemption**: Explicitly guiding the user during environment setup on what local paths or environment variables they need to configure (e.g., `export DATA_DIR="/path/to/your/storage"`).
   - In all runtime documentation, examples, and image references, use relative paths (`./images/ui.png`, `src/main.py`) or portable environment variables (`$PROJECT_ROOT`).

2. **❌ NEVER Mention Policies, Rules, or Agent Instructions**:
   - Never mention internal policy numbers (e.g., "Policy §8.1"), governing rules, rule files, system prompts, or agent instructions inside the README.
   - Present clean, authoritative technical facts and specifications without referencing background constraints.

3. **❌ NEVER Vocalize or Indicate AI Authorship**:
   - Never state, imply, or vocalize that the documentation or codebase was created by AI, an LLM, an assistant, ChatGPT, Claude, or Gemini.
   - Maintain a grounded, peer-to-peer senior software engineer voice representing the project maintainer.

---

## 2. Mandatory README Authoring Protocol

### Step 1: Deep Target Codebase Study (Pre-Writing)
Heavily study and analyze the target repository before drafting documentation:
- Inspect directory trees, entry points (`main.py`, `app.py`, `run.sh`), and configuration schemas.
- Trace CLI argument parsers, public APIs, database connections, and operational dependencies.
- Map the complete user journey from clean installation to daily workflows.

### Step 2: Two-Phase Document Architecture & Table of Contents
Section the README cleanly and always provide an anchor-linked Table of Contents (TOC) at the top:

```markdown
# Project Name

[Short 1-2 sentence descriptive summary]

## Table of Contents
- [Prerequisites & Setup](#prerequisites--setup)
- [Installation & Quick Start](#installation--quick-start)
- [Core Features & Usage](#core-features--usage)
- [Visual Interface Tour](#visual-interface-tour)
- [System Architecture](#system-architecture)
- [Technical Specifications & Schemas](#technical-specifications--schemas)
- [CLI Reference](#cli-reference)
- [Testing & Verification](#testing--verification)
```

- **First Half (Setup, Usage & Features)**:
  - Clear prerequisites, dependencies, and environment setup (noting customizable paths).
  - Quick-start installation commands and step-by-step usage workflows.
  - Core features and visual interface tour with real UI captures.
- **Second Half (Technical Details & Architecture)**:
  - Deep system architecture and component interactions.
  - Data schemas, storage formats, and API contracts.
  - Complete CLI flag matrix, deterministic exit codes, and testing/verification instructions.

### Step 3: Hostile Post-Writing Audit ("Is there anything more to add?")
Hostilely challenge the drafted README:
- Are any CLI flags, configuration parameters, or edge-case failure modes omitted?
- Can a new developer clone and successfully execute the tool with zero guesswork?
- Run the automated auditor to ensure zero policy leaks and zero unscaled assets:
  ```bash
  python3 ~/.gemini/config/skills/readme-visual-enhancer/scripts/readme_auditor.py --readme path/to/README.md
  ```

---

## 3. Visual Enhancement & 420p Aspect-Ratio Scaling

### The 420p Scaling Standard
Downscale captured images so that the **maximum of the highest dimension is 420px** while strictly maintaining original aspect ratio:

$$\text{Scaling Factor} = \frac{420}{\max(\text{Width}_{\text{source}}, \text{Height}_{\text{source}})}$$
$$\text{Width}_{\text{target}} = \text{round}(\text{Width}_{\text{source}} \times \text{Scaling Factor})$$
$$\text{Height}_{\text{target}} = \text{round}(\text{Height}_{\text{source}} \times \text{Scaling Factor})$$

### Mathematical Line Interval Distribution
Embed $N$ visual figures into a document with $L$ total lines at balanced intervals:

$$\text{Line Interval} = \left\lfloor \frac{L}{N} \right\rfloor$$

#### Insertion Rules:
1. **Zero Text Collisions**: Never insert figures inside code blocks or mid-paragraph.
2. **Safe Boundary Snapping**: Snap target lines to adjacent empty lines or markdown section dividers (`---`).
3. **Relative Pathing**: Use relative links (`images/filename.png`).
4. **Italicized Captions**: Always include an italicized descriptive caption below the image:
   ```markdown
   ![Dashboard Overview](images/01_dashboard.png)
   *_Figure 1: Dashboard Overview_*
   ```

---

## 4. Playwright Capture Workflow for Termux

Capture high-fidelity screenshots using native Termux Playwright before downscaling:

```python
import asyncio
from termux_playwright import async_playwright_termux, launch

async def capture_views(view_urls: list[str], staging_directory: str):
    async with async_playwright_termux() as playwright_instance:
        browser = await launch(playwright_instance, headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        for index, url in enumerate(view_urls, start=1):
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{staging_directory}/view_{index:02d}.png")

        await browser.close()
```

---

## 5. Tooling Suite & CLI Commands

### 1. 420p Aspect-Ratio Resizer (`scripts/resize_420p.py`)
```bash
# Single file resize
python3 ~/.gemini/config/skills/readme-visual-enhancer/scripts/resize_420p.py \
    --input "raw_view.png" \
    --output "images/01_view.png" \
    --max-dim 420

# Batch directory resize
python3 ~/.gemini/config/skills/readme-visual-enhancer/scripts/resize_420p.py \
    --input "raw_screenshots_dir" \
    --output "project/images" \
    --max-dim 420
```

### 2. End-to-End Capture & Even Embedding Pipeline (`scripts/readme_embed_pipeline.py`)
```bash
python3 ~/.gemini/config/skills/readme-visual-enhancer/scripts/readme_embed_pipeline.py \
    --readme "project/README.md" \
    --images-dir "project/images" \
    --source-images "raw_screenshots_dir" \
    --max-dim 420
```

### 3. Hostile README Auditor (`scripts/readme_auditor.py`)
```bash
python3 ~/.gemini/config/skills/readme-visual-enhancer/scripts/readme_auditor.py \
    --readme "project/README.md"
```

---

## 6. When to Use & When NOT to Use

### Use This Skill When:
- Writing a new README.md from scratch for any project or repository.
- Upgrading an existing README to professional developer standards with high technical fidelity.
- Capturing live application views via Playwright and downscaling to 420p maintaining aspect ratio.
- Evenly distributing visual figures across Markdown documents using line interval division.
- Hostilely auditing README documentation prior to release.

### Do NOT Use This Skill When:
- Modifying backend core databases or BEJSON schema files.
- Dumping unscaled raw screenshots into git repositories without optimization.
- Writing internal scratch files or developer notes that are not public-facing READMEs.
