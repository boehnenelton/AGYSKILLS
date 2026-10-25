---
name: canvas-animation-studio
description: >-
  Automate, parameterize, seek, and capture fixed-size SVG canvas animations and seamless repeating texture tiles using BEJSON 105a configuration schemas and Termux Playwright. Control frame rates, speeds, viewport sizes, and aspect ratios across 9 production-ready canvas stages. Use when generating animated SVG assets, capturing deterministic keyframes or frame sequences, rendering 8-lane UI stages, or exporting repeating pattern textures. Do NOT use for basic website screenshots (use playwright-termux-automation) or multi-viewport visual regression audits (use playwright-visual-testing).
---

# `canvas-animation-studio` (Layer 5 SVG Animation & Canvas Studio)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & Linux
- **Architectural Tier**: Layer 5 (L5) UI & Visual Interface Automation
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `b3e8c1a9-4f7d-4a2b-9e5c-0d1e2f3a4b5c`
- **Version**: `1.0.0`
- **BEJSON Libraries**: `lib_bejson_Canvas_canvas_schemas`, `lib_bejson_Canvas_canvas_templates` (Format 105/105a)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Generating deterministic still frames or multi-frame animation sequences from SVG canvas templates.
- Controlling animation duration, speed, frame rate (FPS), resolution, and timeline seek ratio via BEJSON 105a schemas.
- Capturing seamless repeating pattern tiles (Isometric Cube 128px, Checkerboard 64px, Circuit Grid 64px, Tile Studio).
- Rendering fixed-aspect visual assets (1:1 Square 800x800, 2:1 Banner 840x420, 16:9 HD 1280x720, 9:16 Portrait 720x1280).
- Seeking specific animation progress points (`window.seekProgress(ratio)`) without running real-time timers.

### Do NOT Use This Skill When:
- Capturing general external web page screenshots or navigating login portals (use `playwright-termux-automation`).
- Running multi-viewport responsive design audits and Tri-Color CSS token compliance checks (use `playwright-visual-testing`).
- Diagnosing internal browser runtime crashes or DOM context faults (use `playwright-debugger-auditor`).

---

## 2. Canvas Template Catalog

The studio includes 9 canonical canvas and texture tile templates located at `/storage/emulated/0/Admin/Dev/Templates/Canvas_SVG_Capture_Templates/`:

| Template Filename | Resolution / Tile | Category | Semantic Motif & Features |
|---|---|---|---|
| `template_square_800x800.html` | 800 × 800 px | Fixed Stage (1:1) | Isometric 3D cube matrix, rotating reticle rings, telemetry HUD |
| `template_banner_840x420.html` | 840 × 420 px | Fixed Stage (2:1) | 8-lane production grid, scanning data waves, 420p downscale target |
| `template_widescreen_1280x720.html` | 1280 × 720 px | Fixed Stage (16:9) | 6-Tier Layered Architecture visual matrix, bus lines, pulse nodes |
| `template_portrait_720x1280.html` | 720 × 1280 px | Fixed Stage (9:16) | Vertical telemetry rail, waterfall stream, stacked layer status cards |
| `template_universal_stage.html` | Dynamic / Configurable | Dynamic Stage | Parameterized stage with query controls (`?size=`, `?bg=`, `?svg=`) |
| `template_texture_isometric_cube.html` | 128 × 128 px unit | Seamless Tile | 104a Isometric cube complex with floating top and pulsing vertices |
| `template_texture_checkerboard.html` | 64 × 64 px unit | Seamless Tile | Dual-tone checkerboard with micro-crosshairs and pulsing red reticles |
| `template_texture_circuit_grid.html` | 64 × 64 px unit | Seamless Tile | Continuous electronic PCB bus traces with pulsing transmission tracks |
| `template_texture_tile_studio.html` | 32/64/128/256 px | Master Studio | Master interactive studio: Cube, Checkerboard, Circuit, Hex, Dots |

---

## 3. BEJSON 105a Schema Integration

All animation parameters, dimensions, and frame pacing are controlled strictly via BEJSON 105a documents backed by `libraries_105`:

### `CanvasStudioConfig` (Format 105a)
```json
{
  "Format": "BEJSON",
  "Format_Version": "105a",
  "Format_Creator": "Elton Boehnen",
  "Record_Type": ["CanvasStudioConfig"],
  "Fields": [
    {"name": "canvas_id",         "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000001"},
    {"name": "template_name",     "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000002"},
    {"name": "stage_selector",    "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000003"},
    {"name": "width_px",          "type": "integer", "field_uuid": "7a1b2c3d-1111-4000-8000-000000000004"},
    {"name": "height_px",         "type": "integer", "field_uuid": "7a1b2c3d-1111-4000-8000-000000000005"},
    {"name": "aspect_ratio",      "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000006"},
    {"name": "bg_theme",          "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000007"},
    {"name": "accent_color",      "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000008"},
    {"name": "animation_name",    "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000009"},
    {"name": "duration_sec",      "type": "number",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000010"},
    {"name": "fps",               "type": "integer", "field_uuid": "7a1b2c3d-1111-4000-8000-000000000011"},
    {"name": "total_frames",      "type": "integer", "field_uuid": "7a1b2c3d-1111-4000-8000-000000000012"},
    {"name": "device_scale",      "type": "integer", "field_uuid": "7a1b2c3d-1111-4000-8000-000000000013"},
    {"name": "export_format",     "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000014"},
    {"name": "output_path",       "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000015"},
    {"name": "svg_source_mode",   "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000016"},
    {"name": "svg_inline_markup", "type": "string",  "field_uuid": "7a1b2c3d-1111-4000-8000-000000000017"}
  ],
  "Values": [
    [
      "9c8b7a6d-5e4f-4a3b-2c1d-0e1f2a3b4c5d",
      "cube_matrix_stage_01",
      "template_square_800x800.html",
      "#capture-stage",
      800,
      800,
      "1:1",
      "#000000",
      "#DE2626",
      "pulseCore",
      8.0,
      60,
      480,
      2,
      "png",
      "captures/cube_matrix_800px.png",
      "template_default",
      ""
    ]
  ]
}
```

---

## 4. Deterministic Keyframe & Speed Math

The studio decouples timeline seeking from real-time clocks using CSS negative animation delays:

- **Target Offset Formula**:
  $$\text{targetTimeSec} = \text{seekProgress} \times \text{totalDurationSec}$$
- **Negative Animation Delay**:
  $$\text{element.style.animationDelay} = -\text{targetTimeSec} \text{ seconds}$$
  $$\text{element.style.animationPlayState} = \text{'paused'}$$
- **Multi-Frame Sequence Stepping**:
  For $N$ total frames over duration $D$:
  $$\text{stepRatio}_i = \frac{i}{N - 1} \quad (0 \le i < N)$$
  $$\text{timestamp}_i = i \times \frac{D}{N - 1}$$

---

## 5. Playwright Studio CLI Runner

Use the studio runner script to execute captures directly:

```bash
# 1. List all available canvas templates
python3 scripts/playwright_canvas_studio.py --list-templates

# 2. Capture a high-resolution still frame at 50% seek progress
python3 scripts/playwright_canvas_studio.py \
    --template template_square_800x800.html \
    --width 800 --height 800 \
    --seek 0.5 \
    --output captures/cube_seek_50.png

# 3. Render a multi-frame animation sequence controlled by BEJSON
python3 scripts/playwright_canvas_studio.py \
    --template template_banner_840x420.html \
    --duration 6.0 \
    --fps 30 \
    --frames 60 \
    --sequence \
    --output captures/banner_wave.png

# 4. Generate a BEJSON 105a configuration file
python3 scripts/playwright_canvas_studio.py \
    --template template_widescreen_1280x720.html \
    --width 1280 --height 720 \
    --duration 10.0 \
    --fps 60 \
    --gen-config configs/widescreen_config.105a.bejson
```

---

## 6. Python & Node.js Library Usage

```python
import sys
sys.path.insert(0, "/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY/Canvas")

from lib_bejson_Canvas_canvas_schemas import create_canvas_config_105a, validate_canvas_config
from lib_bejson_Canvas_canvas_templates import instantiate_stage_html

# Create valid BEJSON 105a config
config = create_canvas_config_105a(
    template_name="template_texture_isometric_cube.html",
    width_px=800,
    height_px=800,
    duration_sec=4.0,
    fps=60
)
valid, errors = validate_canvas_config(config)
assert valid, f"Config errors: {errors}"
```
