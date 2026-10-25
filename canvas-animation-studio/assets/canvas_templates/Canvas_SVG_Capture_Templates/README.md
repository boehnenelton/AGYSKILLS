# Fixed-Size Canvas & Seamless Texture Tile Templates for Playwright

Production-ready fixed-size HTML canvas and seamless texture tile templates engineered specifically for pixel-perfect, deterministic headless screenshot capture of SVG animations and repeating pattern tiles using Playwright and Termux Playwright.

---

## 1. Overview & Design Principles

All templates adhere to strict deterministic rendering rules:
- **BECSS Tri-Color Standard**: Foreground `#FFFFFF` and active accent `#DE2626` over `#000000` deep black background.
- **Fixed-Dimension Stage Isolation**: The `#capture-stage` element enforces exact pixel width and height with zero margin bleed and clipped boundaries.
- **Dual-Mode Capture Support**: Allows capturing either the full seamless repeating canvas (e.g. 800x800, 1280x720) or isolating the individual tile unit (`#tile-unit svg`).
- **Settling & Synchronization Flag**: Templates export `window.isReadyToCapture = true` once DOM and layout settle, ensuring no partial or blank frame captures.
- **Deterministic Animation Seeking**: Exposes `window.seekProgress(ratio)` (0.0 to 1.0) by calculating exact negative CSS animation offsets, enabling arbitrary keyframe seeking and frame sequence generation without running realtime timers.

---

## 2. Template Suite Specifications

### Fixed-Size Visual Canvas Stages

| File Name | Resolution | Aspect Ratio | Focus / Semantic Motif |
|---|---|---|---|
| `template_square_800x800.html` | 800 × 800 px | 1:1 Square | Isometric 3D cube matrix, rotating reticle rings, telemetry HUD |
| `template_banner_840x420.html` | 840 × 420 px | 2:1 Banner | 8-lane production grid, scanning data waves, 420p downscale target |
| `template_widescreen_1280x720.html` | 1280 × 720 px | 16:9 HD | 6-Tier Layered Architecture visual matrix, bus lines, pulse nodes |
| `template_portrait_720x1280.html` | 720 × 1280 px | 9:16 Portrait | Vertical telemetry rail, waterfall stream, stacked layer status cards |
| `template_universal_stage.html` | Dynamic / Configurable | Flexible | Parameterized stage with URL query controls (`?size=`, `?bg=`, `?svg=`) |

### Seamless Repeating Texture Tile Stages

| File Name | Tile Unit Size | Default Stage | Pattern Type & Features |
|---|---|---|---|
| `template_texture_isometric_cube.html` | 128 × 128 px | 800 × 800 px | 104a Isometric cube complex with floating top and pulsing vertices |
| `template_texture_checkerboard.html` | 64 × 64 px | 840 × 420 px | Dual-tone checkerboard with micro-crosshairs and pulsing red reticles |
| `template_texture_circuit_grid.html` | 64 × 64 px | 1280 × 720 px | Continuous electronic PCB bus traces with pulsing transmission tracks |
| `template_texture_tile_studio.html` | 32/64/128/256 px | Multi-Size | Master interactive studio: Cube, Checkerboard, Circuit, Hex Mesh, Dots |

---

## 3. JavaScript Automation Hooks

Every template exposes global JavaScript hooks designed for Playwright execution:

```javascript
// Check if template is fully mounted and ready
if (window.isReadyToCapture) { ... }

// Pause CSS keyframe animations
window.pauseAnimation();

// Resume CSS keyframe animations
window.playAnimation();

// Seek animation to exact progress ratio (0.0 to 1.0)
window.seekProgress(0.5); // Seeks exactly 50% into animation cycle
```

---

## 4. Query Parameter Controls

### Universal Stage (`template_universal_stage.html`)
- `?size=WIDTHxHEIGHT`: Sets stage dimensions (e.g. `?size=1200x630`, `?size=600x400`, `?size=800x800`).
- `?bg=dark|light|transparent`: Toggles background theme (`#000000`, `#FFFFFF`, or transparent).
- `?svg=relative/path/to/icon.svg`: Dynamically embeds an external SVG file inside the stage center.

### Texture Tile Studio (`template_texture_tile_studio.html`)
- `?pattern=cube|checkerboard|circuit|hex|dots`: Selects the active repeating pattern algorithm.
- `?tilesize=32|64|128|256`: Sets the dimensions of the repeating pattern unit cell.
- `?canvas=WIDTHxHEIGHT`: Adjusts stage viewport bounds (e.g. `?canvas=840x420`, `?canvas=1280x720`).
- `?mode=canvas|tile`: Toggles between full tiled canvas stage (`canvas`) or centered single tile unit (`tile`).
- `?ui=hide`: Hides top interactive buttons during automated headless captures.

---

## 5. Playwright Capture CLI Runner Examples

The included Python runner script (`playwright_capture_runner.py`) handles automated headless browser initialization and capture.

### 1. Capture Full Repeating Canvas (Seamless Tile Texture)
```bash
python3 playwright_capture_runner.py \
    --html template_texture_isometric_cube.html \
    --output captures/cube_texture_canvas.png \
    --width 800 \
    --height 800 \
    --seek 0.5
```

### 2. Capture Isolated Single Tile Unit (Seamless Asset Export)
```bash
python3 playwright_capture_runner.py \
    --html template_texture_isometric_cube.html \
    --output captures/cube_single_tile_128px.png \
    --selector "#tile-unit svg" \
    --width 800 \
    --height 800
```

### 3. Capture Texture Studio with Query Parameters
```bash
python3 playwright_capture_runner.py \
    --html "template_texture_tile_studio.html?pattern=circuit&tilesize=64&ui=hide" \
    --output captures/circuit_studio_tile.png \
    --width 800 \
    --height 800 \
    --seek 0.25
```

### 4. High-Resolution Banner Still (2x DPR)
```bash
python3 playwright_capture_runner.py \
    --html template_banner_840x420.html \
    --output captures/hero_banner.png \
    --width 840 \
    --height 420 \
    --seek 0.5
```

---

## 6. Author Credit

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
