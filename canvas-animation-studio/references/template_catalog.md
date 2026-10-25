# Canvas Stage & Seamless Texture Tile Catalog

## 1. Fixed-Size Canvas Stages

### `template_square_800x800.html`
- **Resolution**: 800 × 800 px (1:1 Aspect Ratio)
- **Primary Selector**: `#capture-stage`
- **Motif**: Isometric 3D cube matrix, rotating reticle rings, telemetry HUD.
- **Default Animation**: `pulseCore` (8.0s), `orbitRing` (16.0s).
- **Use Cases**: Social media squares, square avatar assets, profile icons, isometric badges.

### `template_banner_840x420.html`
- **Resolution**: 840 × 420 px (2:1 Aspect Ratio)
- **Primary Selector**: `#capture-stage`
- **Motif**: 8-lane production grid, scanning data waves, 420p downscale target.
- **Default Animation**: `waveScan` (6.0s), `gridPulse` (3.0s).
- **Use Cases**: Documentation banners, repository headers, README hero visual.

### `template_widescreen_1280x720.html`
- **Resolution**: 1280 × 720 px (16:9 HD Aspect Ratio)
- **Primary Selector**: `#capture-stage`
- **Motif**: 6-Tier Layered Architecture visual matrix, bus lines, pulse nodes.
- **Default Animation**: `busTransmit` (10.0s), `layerShimmer` (5.0s).
- **Use Cases**: Video title cards, widescreen presentation slides, YouTube thumbnails.

### `template_portrait_720x1280.html`
- **Resolution**: 720 × 1280 px (9:16 Portrait Aspect Ratio)
- **Primary Selector**: `#capture-stage`
- **Motif**: Vertical telemetry rail, waterfall stream, stacked layer status cards.
- **Default Animation**: `waterfallStream` (8.0s).
- **Use Cases**: Mobile portrait displays, vertical telemetry monitors, mobile reels.

### `template_universal_stage.html`
- **Resolution**: Dynamic / Configurable via Query Params (`?size=WIDTHxHEIGHT`)
- **Primary Selector**: `#capture-stage`
- **Motif**: Parameterized dynamic stage with query controls (`?size=`, `?bg=`, `?svg=`).
- **Use Cases**: Arbitrary size tests, external SVG component testing, dynamic mockups.

---

## 2. Seamless Repeating Texture Tiles

### `template_texture_isometric_cube.html`
- **Tile Unit Size**: 128 × 128 px
- **Stage Size**: 800 × 800 px (repeating matrix)
- **Unit Selector**: `#tile-unit svg`
- **Motif**: 104a Isometric cube complex with floating top and pulsing vertices.
- **Default Animation**: `cubePulse` (4.0s).

### `template_texture_checkerboard.html`
- **Tile Unit Size**: 64 × 64 px
- **Stage Size**: 840 × 420 px (repeating matrix)
- **Unit Selector**: `#tile-unit svg`
- **Motif**: Dual-tone checkerboard with micro-crosshairs and pulsing red reticles.
- **Default Animation**: `reticleBlink` (4.0s).

### `template_texture_circuit_grid.html`
- **Tile Unit Size**: 64 × 64 px
- **Stage Size**: 1280 × 720 px (repeating matrix)
- **Unit Selector**: `#tile-unit svg`
- **Motif**: Continuous electronic PCB bus traces with pulsing transmission tracks.
- **Default Animation**: `tracePulse` (6.0s).

### `template_texture_tile_studio.html`
- **Tile Unit Size**: 32 / 64 / 128 / 256 px
- **Stage Size**: Multi-Size configurable
- **Unit Selector**: `#tile-unit svg`
- **Motif**: Master interactive studio supporting Cube, Checkerboard, Circuit, Hex Mesh, and Dots.

---

## 3. Dedicated Icon Canvases

### `template_icon_512x512.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Shape**: Squircle (`rx="108"`)
- **Motif**: Master App Store / PWA icon, 104a floating cube, orbiting reticle ring.
- **Default Duration**: 4.0s.

### `template_icon_256x256.html`
- **Resolution**: 256 × 256 px (1:1 Aspect Ratio)
- **Shape**: Squircle (`rx="54"`)
- **Motif**: Application launcher icon, hexagonal aperture, glowing cube nucleus.
- **Default Duration**: 3.5s.

### `template_icon_128x128.html`
- **Resolution**: 128 × 128 px (1:1 Aspect Ratio)
- **Shape**: Rounded Tile (`rx="28"`)
- **Motif**: System tray / widget icon, high-contrast isometric cube glyph.
- **Default Duration**: 3.0s.

### `template_icon_64x64.html`
- **Resolution**: 64 × 64 px (1:1 Aspect Ratio)
- **Shape**: Micro Squircle (`rx="14"`)
- **Motif**: Toolbar / navigation micro-icon, pixel-snapped cube silhouette.
- **Default Duration**: 2.0s.

### `template_icon_32x32.html`
- **Resolution**: 32 × 32 px (1:1 Aspect Ratio)
- **Shape**: Favicon Box (`rx="7"`)
- **Motif**: 32px Favicon / terminal prompt glyph, micro isometric cube and red pip.
- **Default Duration**: 1.8s.

### `template_icon_studio.html`
- **Resolution**: Dynamic (`?size=512|256|128|64|32|WIDTHxHEIGHT`)
- **Motif**: Parameterized studio for any custom icon size with URL query controls.
- **Default Duration**: 3.0s.

---

## 4. Small Component Graphic Canvases

### `template_graphic_badge_400x200.html`
- **Resolution**: 400 × 200 px (2:1 Aspect Ratio)
- **Shape**: Chamfered Cyber Card
- **Motif**: Component release badge, left rotating cube reticle, right telemetry readout, scanline sweep.
- **Default Duration**: 3.0s.

### `template_graphic_kpi_card_320x320.html`
- **Resolution**: 320 × 320 px (1:1 Aspect Ratio)
- **Shape**: Rounded Widget Card (`rx="20"`)
- **Motif**: Compact KPI metric card, radial progress gauge arc with pulsing red indicator.
- **Default Duration**: 3.0s.

### `template_graphic_button_240x80.html`
- **Resolution**: 240 × 80 px (3:1 Aspect Ratio)
- **Shape**: Chamfered Action Control Pill
- **Motif**: Cyber CTA button, left micro-cube, action label, right animated chevron.
- **Default Duration**: 2.5s.

### `template_graphic_chip_160x48.html`
- **Resolution**: 160 × 48 px (10:3 Aspect Ratio)
- **Shape**: Micro Pill Tag (`rx="20"`)
- **Motif**: System architecture tier tag (e.g. "L5 · UI_AUDIT"), pulsing status dot.
- **Default Duration**: 2.0s.

---

## 5. Canonical BEJSON Cube Taxonomy Icons (Policy §8.3)

### `template_icon_bejson_104_standard.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Taxonomy**: 104 Single Standard Cube
- **Motif**: Solid isometric monolithic cube, dual counter-rotating telemetry rings, pulsing red vertex nodes, center spine.
- **Default Duration**: 4.0s.

### `template_icon_bejson_104a_floating.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Taxonomy**: 104a Single Cube with Floating Top
- **Motif**: Signature 104a levitating diamond top cap bobbing vertically, emitting red plasma energy beams to the base cube.
- **Default Duration**: 3.5s.

### `template_icon_bejson_104db_pillar.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Taxonomy**: 104db Vertical Pillar of Stacked Cubes
- **Motif**: 3-tier monolithic stacked cube pillar with sequential cascading red data pulse waves traveling up and down the pillar.
- **Default Duration**: 3.0s.

### `template_icon_bejson_104_nested.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Taxonomy**: 104 Nested Large Cube Containing Smaller Cubes
- **Motif**: Large outer wireframe container cube with pulsating border lines enclosing a glowing inner rotating solid child cube.
- **Default Duration**: 4.0s.

### `template_icon_bejson_mfdb_federation.html`
- **Resolution**: 512 × 512 px (1:1 Aspect Ratio)
- **Taxonomy**: MFDB Central Cube Linked to External Cube Nodes
- **Motif**: Large central master cube linked via animated streaming red bus transmission traces to 4 orbiting satellite slave cubes.
- **Default Duration**: 3.5s.

