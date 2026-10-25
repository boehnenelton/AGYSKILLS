---
name: publication-tweet-automator
description: >-
  Automate the generation of Twitter/X-optimized visual media assets (16:9 landscape 1200x675, 1:1 square 800x800, 2:1 header banner 1200x600/840x420) by invoking canvas-animation-studio SVG templates and Termux Playwright, and synchronizing the rendered captures directly into designated tweet prompt and deliverable folders. Use when generating Twitter-optimized images for promotional tweets, creating visual thread hero cards, seeking deterministic SVG canvas keyframes for social media, or registering social media captures into BEJSON manifests. Do NOT use for raw standalone browser automation (use playwright-termux-automation), multi-viewport responsive design audits (use playwright-visual-testing), or compiling long-form technical e-books (use publication-html-builder).
---

# publication-tweet-automator (Layer 3 Social Media Visual Asset & Tweet Image Generator)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & Linux
- **Architectural Tier**: Layer 3 (L3) Automation & Service Pipeline
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `8f1c2d3e-4a5b-6c7d-8e9f-0a1b2c3d4e5f`
- **Version**: `1.0.0`
- **Companion Skill**: `canvas-animation-studio` (Layer 5 SVG Animation Studio)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Generating Twitter/X-optimized visual media cards tailored for promotional tweets and technical launch threads.
- Bridging tweet prompts in `~/generate/prompts/tweet/` with deterministic SVG canvas renders.
- Capturing high-resolution Twitter presets: 16:9 Landscape (`1200x675` px), 1:1 Square (`800x800` px), 2:1 Banner (`1200x600` or `840x420` px), and 9:16 Vertical (`720x1280` px).
- Copying and organizing rendered image captures directly into target tweet folders (e.g., `~/generate/prompts/tweet/images/` or local project repositories).
- Tracking generated social media images in structured BEJSON 104a manifests with SHA-256 integrity verification.

### When NOT to Use:
- Do NOT use for general unblocked web page scraping or form submission (use `playwright-termux-automation`).
- Do NOT use for multi-viewport CSS token audits or perceptual visual regression diffing (use `playwright-visual-testing`).
- Do NOT use for compiling multi-page HTML documentation websites or e-books (use `publication-html-builder`).
- Do NOT use for writing 4-part long-form technical blog posts (use `publication-blog-post-writer`).

---

## 2. Twitter / X Aspect Ratio Presets

The skill embeds standardized presets mapped directly to Twitter/X's native image display containers:

| Preset Name | Dimensions | Ratio | Recommended Canvas Template | Primary Social Media Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `landscape` | 1200 x 675 px | 16:9 | `template_widescreen_1280x720.html` | High-impact in-feed landscape cards, launch heroes |
| `banner` | 1200 x 600 px | 2:1 | `template_banner_840x420.html` | Thread opener header banners, large summary cards |
| `square` | 800 x 800 px | 1:1 | `template_square_800x800.html` | Metric callouts, isometric 3D cube spotlights |
| `portrait` | 720 x 1280 px | 9:16 | `template_portrait_720x1280.html` | Mobile vertical feed, waterfall architecture rails |
| `icon` | 512 x 512 px | 1:1 | `template_icon_bejson_104a_floating.html` | Project avatar badges, PWA splash graphics |

All captures strictly honor the immutable Tri-Color palette: Pitch Black (`#000000`), Pure White (`#FFFFFF`), and Accent Red (`#DE2626`).

---

## 3. Operational Workflow & Tool Execution

The primary automation engine is driven by `scripts/tweet_canvas_generator.py`, which invokes the underlying `canvas-animation-studio` headless Playwright engine and synchronizes output files to the target tweet directory:

### Step 1: Discover & Select Presets
```bash
python3 scripts/tweet_canvas_generator.py --list-presets
```

### Step 2: Render & Copy Image to Tweet Directory
Capture a 16:9 landscape hero image at 50% seek progress and copy directly into the tweet images folder:
```bash
python3 scripts/tweet_canvas_generator.py \
    --preset landscape \
    --template template_widescreen_1280x720.html \
    --seek 0.5 \
    --output newagent_launch_hero_1200x675.png \
    --prompt-file newagent_launch_and_breakthrough_thread.md \
    --tweet-number 1 \
    --tweet-dir /data/data/com.termux/files/home/generate/prompts/tweet/images
```

### Step 3: Square Metric Spotlight Capture
Capture an isometric 3D cube metric graphic for Tweet 4 in a thread:
```bash
python3 scripts/tweet_canvas_generator.py \
    --preset square \
    --template template_square_800x800.html \
    --seek 0.35 \
    --output newagent_token_benchmark_800x800.png \
    --prompt-file newagent_bejson_zero_sql_persistence_thread.md \
    --tweet-number 4
```

### Step 4: BEJSON 104a Manifest Tracking
Pass `--manifest` to automatically register the generated image, dimensions, template, and SHA-256 hash into a BEJSON 104a registry:
```bash
python3 scripts/tweet_canvas_generator.py \
    --preset landscape \
    --seek 0.5 \
    --manifest assets/tweet_image_registry.104a.bejson
```

---

## 4. Headless agy Execution Protocol

When executing headless automation tasks via Antigravity CLI, always invoke `agy` with mandatory `--sandbox` isolation:

```bash
agy --sandbox -p "Generate Twitter-optimized landscape image for newagent_brain_surgery_hotpatch_thread.md using template_widescreen_1280x720.html at seek 0.5 and copy to ~/generate/prompts/tweet/images"
```

Negative Constraints: Zero conversational filler. Do not modify files outside designated tweet and staging folders.

---

## 5. BEJSON Manifest Schema (Format 104a)

Companion image registries in `assets/` follow strict BEJSON 104a specifications:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["TweetImageRecord"],
  "Fields": [
    {"name": "image_id", "type": "string"},
    {"name": "tweet_prompt_file", "type": "string"},
    {"name": "tweet_number", "type": "integer"},
    {"name": "canvas_template", "type": "string"},
    {"name": "aspect_ratio", "type": "string"},
    {"name": "width_px", "type": "integer"},
    {"name": "height_px", "type": "integer"},
    {"name": "seek_progress", "type": "number"},
    {"name": "output_filename", "type": "string"},
    {"name": "destination_dir", "type": "string"},
    {"name": "sha256_hash", "type": "string"},
    {"name": "created_timestamp", "type": "string"}
  ],
  "Values": []
}
```
In Python operations, field indices are resolved dynamically via `field_map` caching:
```python
field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}
image_id = row[field_map["image_id"]]
```
