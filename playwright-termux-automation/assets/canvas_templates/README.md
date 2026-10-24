# Fixed-Size Canvas Templates for SVG Animation & Playwright Capture

Production-ready fixed-size HTML canvas templates engineered specifically for pixel-perfect, deterministic headless screenshot capture of SVG animations using Playwright and Termux Playwright.

---

## 1. Overview & Design Principles

All templates adhere to strict deterministic rendering rules:
- **BECSS Tri-Color Standard**: Foreground `#FFFFFF` and active accent `#DE2626` over `#000000` deep black background.
- **Fixed-Dimension Stage Isolation**: The `#capture-stage` element enforces exact pixel width and height with zero margin bleed and clipped boundaries.
- **Settling & Synchronization Flag**: Templates export `window.isReadyToCapture = true` once DOM and layout settle, ensuring no partial or blank frame captures.
- **Deterministic Animation Seeking**: Exposes `window.seekProgress(ratio)` (0.0 to 1.0) by calculating exact negative CSS animation offsets, enabling arbitrary keyframe seeking and frame sequence generation without running realtime timers.

---

## 2. Template Suite Specifications

| File Name | Resolution | Aspect Ratio | Focus / Semantic Motif |
|---|---|---|---|
| `template_square_800x800.html` | 800 × 800 px | 1:1 Square | Isometric 3D cube matrix, rotating reticle rings, telemetry HUD |
| `template_banner_840x420.html` | 840 × 420 px | 2:1 Banner | 8-lane production grid, scanning data waves, 420p downscale target |
| `template_widescreen_1280x720.html` | 1280 × 720 px | 16:9 HD | 6-Tier Layered Architecture visual matrix, bus lines, pulse nodes |
| `template_portrait_720x1280.html` | 720 × 1280 px | 9:16 Portrait | Vertical telemetry rail, waterfall stream, stacked layer status cards |
| `template_universal_stage.html` | Dynamic / Configurable | Flexible | Parameterized stage with URL query controls (`?size=`, `?bg=`, `?svg=`) |

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

## 4. Universal Stage Query Parameters

The `template_universal_stage.html` supports runtime parameterization via URL query parameters:

- `?size=WIDTHxHEIGHT`: Sets stage dimensions (e.g. `?size=1200x630`, `?size=600x400`, `?size=800x800`).
- `?bg=dark|light|transparent`: Toggles background theme (`#000000`, `#FFFFFF`, or transparent for clean alpha masking).
- `?svg=relative/path/to/icon.svg`: Dynamically embeds an external SVG file inside the stage center.

---

## 5. Playwright Capture CLI Runner

The included Python runner script (`playwright_capture_runner.py`) provides single-command capture execution with automated browser handling.

### Single Still Capture (Middle of Animation)
```bash
python3 playwright_capture_runner.py \
    --html template_banner_840x420.html \
    --output banner_frame.png \
    --width 840 \
    --height 420 \
    --seek 0.5
```

### High-Resolution Square Still (2x DPR)
```bash
python3 playwright_capture_runner.py \
    --html template_square_800x800.html \
    --output square_hero.png \
    --width 800 \
    --height 800 \
    --seek 0.25
```

### Multi-Frame Sequential Capture (For GIF/Video Assembling)
```bash
python3 playwright_capture_runner.py \
    --html template_widescreen_1280x720.html \
    --output frames/frame.png \
    --width 1280 \
    --height 720 \
    --frames 24
```

---

## 6. Author Credit

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
