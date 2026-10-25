# BEJSON CMS Canvas Imagery Specifications

## 1. Visual Design Geometry & Policy §8.1 Tri-Color Palette

All generated SVG canvas graphics and Playwright raster captures adhere strictly to:
- **Background**: `#000000` (Pure Black)
- **Text & Foreground**: `#FFFFFF` (Pure White)
- **Active & Laser Accents**: `#DE2626` (Canonical Red)
- **Grid Stacking**: 8-lane quantized X-axis (160px intervals across 1280px canvas) and 32px Ry quantized horizontal rows.

---

## 2. Canvas Archetypes

| Archetype | Dimensions | Aspect Ratio | Primary Use Case |
|---|---|---|---|
| **Article Hero Banner** | 1280x640 | 2:1 | Featured top banner for BEJSON CMS blog posts and NewAgent articles. |
| **Medium Banner** | 840x420 | 2:1 | Category headers and mobile responsive hero views. |
| **Social / Post Square** | 800x800 | 1:1 | Square card embed, OpenGraph social previews, tweet media. |
| **Subsystem KPI Card** | 320x320 | 1:1 | Modular architecture callout cards and metric counters. |
| **Cube Taxonomy Badge** | 128x128 / 256x256 | 1:1 | Format markers (104, 104a, 104db, Nested, MFDB federation). |

---

## 3. Peripheral Node Architecture

The 1280x640 Hero Canvas dynamically positions 4 peripheral module cards connected to the central isometric BEJSON cube via glowing `#DE2626` laser rays:

- **Node 1 (Top Left)**: Primary ingestion / storage interface.
- **Node 2 (Bottom Left)**: Security vault / state synchronization.
- **Node 3 (Top Right)**: Service dispatch / API runtime.
- **Node 4 (Bottom Right)**: Presentation / CMS publisher output.

---

## 4. Integration with BEJSON CMS

Generated graphics are saved directly to:
- `/storage/emulated/0/Admin/Dev/Repos/BEJSON_CMS/storage/mfdb/assets/`
- Or the active blog post draft directory.

Embed Snippet (BEHTML):
```html
<div class="behtml-featured-header" style="text-align: center; margin-bottom: 24px;">
  <img src="storage/mfdb/assets/article_hero.svg" alt="Article Title" style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px;" />
</div>
```
