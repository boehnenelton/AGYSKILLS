# Twitter / X Visual Media Technical Specifications

## 1. Optimal In-Feed Aspect Ratios & Dimensions

Twitter/X compresses and crops images based on viewport containers. To avoid arbitrary auto-cropping and maximize pixel sharpness:

| Placement / Category | Target Ratio | Canvas Resolution | Recommended Canvas Studio Template |
| :--- | :--- | :--- | :--- |
| **In-Feed Landscape (Primary)** | 16:9 | 1200 x 675 px | `template_widescreen_1280x720.html` |
| **Summary Large Card / Banner** | 2:1 | 1200 x 600 px (or 840 x 420 px) | `template_banner_840x420.html` |
| **Single Focal Metric / Cube** | 1:1 Square | 800 x 800 px (or 1200 x 1200 px) | `template_square_800x800.html` |
| **Mobile Vertical Waterfall** | 9:16 | 720 x 1280 px | `template_portrait_720x1280.html` |
| **PWA / App Icon Badge** | 1:1 Square | 512 x 512 px | `template_icon_bejson_104a_floating.html` |

## 2. Palette & Contrast Compliance

All generated visual assets must adhere strictly to the Policy Section 8.1 Tri-Color Standard:
- **Pitch Black (`#000000`)**: Canvas background, void space, dark frames.
- **Pure White (`#FFFFFF`)**: High-contrast typography, primary isometric cube faces, telemetry grids.
- **Accent Red (`#DE2626`)**: Pulse nodes, focal reticles, laser vectors, active status markers.

## 3. Playwright Rendering Pacing & Deterministic Seeking

Rather than waiting for real-time timers, the canvas studio uses deterministic CSS animation offsets:
- `target_time_sec = seek_progress * total_duration_sec`
- `window.seekProgress(ratio)` sets negative animation delays instantly.
- Captured via Termux Playwright at `device_scale_factor = 2` for crisp retina-grade rendering.

## 4. Destination Directory Conventions

Rendered assets are automatically placed in the designated tweet images directory:
- Default: `~/generate/prompts/tweet/images/`
- Custom: Target project image repositories (e.g., `/storage/emulated/0/Admin/Dev/Repos/NewAgent/images/`)
