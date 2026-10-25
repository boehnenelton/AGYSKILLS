# BEHTML Pipeline Architecture & Asset Bundling Reference

## 1. The BEHTML 3-Stage Build Pipeline

The Layer 3 `behtml-scaffold-automator` closes the architectural gap between Layer 4 UI layout composition and Layer 2 schema validation:

```
[Layer 4 Layout Builder]
           |  (Raw BEHTML markup + inline 18-field elements)
           v
[Layer 3 BEHTML Bundler (This Skill)]
     1. Asset Localization (strip CDNs, localize fonts/scripts)
     2. Token Injection (inject BECSS Tri-Color CSS variables)
     3. Path Resolution (canonicalize relative links)
     4. Layer 2 Gatekeeper (executes behtml-schema-validator)
           |
           v
[Layer 2 Schema Validator] -> [Layer 1 Output Substrate (dist/)]
```

## 2. Inviolable Grid & Spatial Quantization Rules

All bundled templates must strictly conform to:
- **X-Axis Geometry**: 8 lanes (each 12.5% width, `X0..X7`) or 16 sublanes (each 6.25% width, `S0..S15`).
- **Y-Axis Geometry**: Row height unit $R_y = 32\text{px}$. All row spans and vertical paddings must be exact multiples of 32px (`Ry1=32px`, `Ry2=64px`, `Ry3=96px`).
- **BECSS Tri-Color Palette**:
  - Background: Pitch Black (`#000000`) or Pure White (`#FFFFFF`)
  - Typography: Pure White (`#FFFFFF`) or Pitch Black (`#000000`)
  - Accent / Focus: Vivid Accent Red (`#DE2626`)
- **Zero Filler Law**: No lorem ipsum or conversational filler. Minimal functional labels only (`'Title'`, `'Header'`, `'Nav'`).

## 3. Distribution Packaging Conventions

Bundled output is staged to `dist/`:
- `dist/index.html`: Fully self-contained or cleanly linked entrypoint.
- `dist/styles/becss_master.css`: Extracted Tri-Color tokens and 8-lane container classes.
- `dist/sitemap.xml`: Canonical W3C XML sitemap for SEO discovery.
- `dist/manifest.104a.bejson`: BEJSON build manifest recording file hashes and element counts.
