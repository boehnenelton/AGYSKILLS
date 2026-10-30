---
name: canvas-animation-studio
description: >-
  Automate, parameterize, seek, and capture fixed-size SVG canvas animations, dynamic blank-slate stages, row-per-frame animations, and seamless repeating texture tiles using BEJSON 105a configuration schemas, Playwright, and multi-format exporters (GIF, WebM, APNG, MP4). Control frame rates (FPS), duration, dynamic SVG injection, X-Y coordinate text overlays pre-recording, and slideshow compilation. Use when generating animated SVG assets, capturing deterministic keyframes or frame sequences, rendering dynamic blank slates, or exporting video/GIF recordings. Do NOT use for basic website screenshots (use playwright-termux-automation) or multi-viewport visual regression audits (use playwright-visual-testing).
---

# `canvas-animation-studio` (Layer 5 SVG Animation, Canvas Studio & Graphics Core)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 5 (L5) UI & Visual Interface Automation
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `b3e8c1a9-4f7d-4a2b-9e5c-0d1e2f3a4b5c`
- **Version**: `1.8.0`
- **BEJSON Libraries**: `lib_bejson_Graphics_graphics_core`, `lib_bejson_Graphics_graphics_canvas_templates`, `lib_bejson_Graphics_graphics_schemas`, `lib_bejson_Graphics_graphics_diagram_loader` (`libraries_105/Lib_PY/Graphics` & `libraries_105/Lib_JS/Graphics`)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Generating deterministic still frames or multi-frame animation sequences from dynamic SVG canvas templates.
- Controlling animation duration, speed, frame rate (FPS), resolution, and timeline seek ratio via BEJSON 105a schemas.
- Using **blank-slate canvas stages** to host arbitrary dynamic SVGs, images, and frame states across any dimension.
- Executing **BEJSON 105a Row-Per-Frame Animations** where each row declares a single frame with dynamic SVG markup, timestamp, seek progress, FPS, and post-render SHA-256 verification.
- Applying **X, Y coordinate-based text overlays** onto the canvas pre-recording defined by active canvas schema configs.
- Compiling animations into **GIF** (ffmpeg 2-pass palettegen or Pillow), **WebM** (VP9 / Playwright native recording), **APNG**, or **MP4**.
- Generating automated **slideshows** sequencing arbitrary images or SVG slides with configurable hold and transition times.
- Capturing seamless repeating pattern tiles (Isometric Cube 128px, Checkerboard 64px, Circuit Grid 64px).

### Do NOT Use This Skill When:
- Capturing general external web page screenshots or navigating login portals (use `playwright-termux-automation`).
- Running multi-viewport responsive design audits and Tri-Color CSS token compliance checks (use `playwright-visual-testing`).
- Diagnosing internal browser runtime crashes or DOM context faults (use `playwright-debugger-auditor`).

---

## 2. Canvas Blank-Slate & Stage Architecture

The studio treats canvas stages as **blank slates** capable of hosting arbitrary dynamic images, SVGs, and frame data:

| Stage Identifier | Resolution / Ratio | Category | Purpose & Characteristics |
|---|---|---|---|
| `blank_slate_stage.html` | Dynamic / Parameterized | Universal Blank Slate | Runtime dimension and SVG injection hooks (`window.setSvgContent`, `window.setTextOverlays`) |
| `blank_slate_square_800x800.html` | 800 × 800 px (1:1) | Fixed Blank Slate | Square graphics, avatars, centered isometric models |
| `blank_slate_banner_840x420.html` | 840 × 420 px (2:1) | Fixed Blank Slate | Social media cards, landscape banners, 420p targets |
| `blank_slate_widescreen_1280x720.html` | 1280 × 720 px (16:9) | Fixed Blank Slate | HD widescreen landscapes, presentation stages, video thumbnails |
| `blank_slate_article_hero_1280x640.html` | 1280 × 640 px (2:1) | Fixed Blank Slate | CMS article featured hero banners |
| `blank_slate_portrait_720x1280.html` | 720 × 1280 px (9:16) | Fixed Blank Slate | Mobile portrait cards, vertical video story frames |
| `blank_slate_kpi_card_320x320.html` | 320 × 320 px (1:1) | Fixed Blank Slate | Metric cards and telemetry widgets |
| `blank_slate_badge_400x200.html` | 400 × 200 px (2:1) | Fixed Blank Slate | System status badges and header chips |
| `blank_slate_button_240x80.html` | 240 × 80 px (3:1) | Fixed Blank Slate | Graphic buttons and call-to-action elements |
| `blank_slate_icon_512x512.html` | 512 × 512 px (1:1) | Icon Blank Slate | High-resolution application iconography |
| `blank_slate_texture_tile_128x128.html`| 128 × 128 px unit (1:1) | Tile Blank Slate | Repeating texture tile generation |

---

## 3. BEJSON 105a Row-Per-Frame Animation Schema

In the Graphics 105 library, multi-frame animations are declared as **BEJSON 105a tables where each row corresponds to a single frame**:

```json
{
  "Format": "BEJSON",
  "Format_Version": "105a",
  "Format_Creator": "Elton Boehnen",
  "Animation_Name": "pulse_cube_anim",
  "Duration_Sec": 4.0,
  "FPS": 30,
  "Total_Frames": 120,
  "Width_Px": 800,
  "Height_Px": 800,
  "Aspect_Ratio": "1:1",
  "Canvas_Id": "canvas_anim_01",
  "Template_Name": "blank_slate_stage.html",
  "Record_Type": ["GraphicFrameRecord"],
  "Fields": [
    {"name": "frame_index",      "type": "integer", "field_uuid": "9b2c3d4e-2222-4000-8000-000000000001"},
    {"name": "timestamp_sec",    "type": "number",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000002"},
    {"name": "seek_progress",    "type": "number",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000003"},
    {"name": "fps",              "type": "integer", "field_uuid": "9b2c3d4e-2222-4000-8000-000000000004"},
    {"name": "frame_filename",   "type": "string",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000005"},
    {"name": "svg_markup",       "type": "string",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000006"},
    {"name": "frame_data_json",  "type": "string",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000007"},
    {"name": "is_rendered",      "type": "boolean", "field_uuid": "9b2c3d4e-2222-4000-8000-000000000008"},
    {"name": "checksum_sha256",  "type": "string",  "field_uuid": "9b2c3d4e-2222-4000-8000-000000000009"}
  ],
  "Values": [
    [
      "9f1b2c3d-1111-4000-8000-000000000001",
      0,
      0.0,
      0.0,
      30,
      "frame_0000.png",
      "<svg>...</svg>",
      "{\"pulse\": 1.0}",
      true,
      "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    ]
  ]
}
```

---

## 4. X-Y Coordinate Text Overlays (Pre-Recording)

Text overlays can be defined in the active canvas configuration (`GraphicCanvasConfig`) and rendered onto the blank slate canvas **pre-recording**:

```python
from lib_bejson_Graphics_graphics_schemas import create_coordinate_text_overlay, create_graphic_stage_config_105a

# Define coordinate-based text overlay with dynamic interpolation tokens:
# {frame}, {time}, {fps}, {caption}
overlay_hud = create_coordinate_text_overlay(
    x=24,
    y=24,
    text="FPS: {fps} | FRAME: {frame} | T: {time}s",
    font_size=18,
    font_family="monospace",
    color="#FFFFFF",
    bg_color="rgba(0, 0, 0, 0.75)",
    padding="6px 12px",
    border_radius="4px"
)

# Embed into active stage configuration
stage_cfg = create_graphic_stage_config_105a(
    canvas_id="hud_stage_01",
    width_px=800,
    height_px=800,
    text_overlays=[overlay_hud]
)
```

---

## 5. Multi-Format Recording & Export Engines

The library exports rendered animations directly to multiple formats:

```python
from lib_bejson_Graphics_graphics_core import (
    compile_frames_to_gif,
    compile_frames_to_webm,
    compile_frames_to_apng,
    compile_frames_to_mp4,
    compile_row_per_frame_to_animated_svg
)

frames_dir = "captures/pulse_cube_anim"

# 1. Compile to high-quality GIF (ffmpeg 2-pass palettegen with Pillow fallback)
gif_file = compile_frames_to_gif(frames_dir, "captures/pulse_cube.gif", fps=30)

# 2. Compile to WebM video (VP9)
webm_file = compile_frames_to_webm(frames_dir, "captures/pulse_cube.webm", fps=30, crf=28)

# 3. Compile to Animated PNG (APNG)
apng_file = compile_frames_to_apng(frames_dir, "captures/pulse_cube.png", fps=30)

# 4. Compile to MP4 video (H.264)
mp4_file = compile_frames_to_mp4(frames_dir, "captures/pulse_cube.mp4", fps=30)
```

---

## 6. Slideshow Compilation Engine

Sequence arbitrary images or SVG slides across a timeline with automated hold and transition frames:

```python
from lib_bejson_Graphics_graphics_schemas import create_slideshow_animation_105a
from lib_bejson_Graphics_graphics_core import render_row_per_frame_animation, compile_frames_to_gif

slides = [
    {"svg_markup": "<svg>...</svg>", "duration_sec": 3.0, "caption": "Slide 1: Overview"},
    {"svg_markup": "<svg>...</svg>", "duration_sec": 3.0, "caption": "Slide 2: Architecture"},
    {"svg_markup": "<svg>...</svg>", "duration_sec": 3.0, "caption": "Slide 3: Telemetry"}
]

slideshow_doc = create_slideshow_animation_105a(
    slideshow_name="project_slideshow",
    slides=slides,
    fps=24,
    width_px=800,
    height_px=800
)

# Render all frames through Playwright into the blank slate stage
asyncio.run(render_row_per_frame_animation(slideshow_doc, output_dir="captures/slideshow"))

# Export directly to animated GIF or WebM
compile_frames_to_gif("captures/slideshow", "captures/slideshow.gif", fps=24)
```

---

## 7. CLI Quickstart Reference

```bash
CORE="/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY/Graphics/lib_bejson_Graphics_graphics_core.py"

# 1. List registered canvas templates
python3 "$CORE" --list-templates

# 2. Render a still frame with an isometric cube SVG
python3 "$CORE" --still --width 800 --height 800 --output captures/still.png

# 3. Render a row-per-frame animation and compile to GIF and WebM
python3 "$CORE" --row-animation --name cube_pulse --fps 30 --duration 3.0 --export-gif --export-webm

# 4. Render a multi-slide presentation to animated GIF
python3 "$CORE" --slideshow --name arch_presentation --fps 24 --export-gif
```
