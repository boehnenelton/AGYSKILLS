# Canvas Studio BEJSON 105a Schema Reference

This reference outlines the data structures for `CanvasStudioConfig` and `CanvasFrameSequence` adhering to BEJSON 105a.

## 1. CanvasStudioConfig (Format 105a)

- **Record_Type**: `["CanvasStudioConfig"]`
- **Primary Key**: `record_uuid` (at `row[0]`)

### Fields Roster
1. `canvas_id` (`string`): Unique string identifier for the canvas stage session.
2. `template_name` (`string`): HTML template filename (e.g. `template_square_800x800.html`).
3. `stage_selector` (`string`): DOM selector for the target stage element (default `#capture-stage`).
4. `width_px` (`integer`): Target stage pixel width.
5. `height_px` (`integer`): Target stage pixel height.
6. `aspect_ratio` (`string`): Aspect ratio string (e.g. `1:1`, `2:1`, `16:9`, `9:16`).
7. `bg_theme` (`string`): Background color hex (`#000000`, `#FFFFFF`, transparent).
8. `accent_color` (`string`): Brand accent color hex (`#DE2626`).
9. `animation_name` (`string`): Primary CSS keyframe animation name.
10. `duration_sec` (`number`): Full animation loop cycle duration in seconds.
11. `fps` (`integer`): Target capture framerate.
12. `total_frames` (`integer`): Total frames in full cycle ($N = \text{duration} \times \text{fps}$).
13. `device_scale` (`integer`): Device scale factor (DPR, default `2` for HiDPI/Retina).
14. `export_format` (`string`): Format string (`png`, `webp`, `apng`).
15. `output_path` (`string`): Destination path for rendered snapshot or sequence stem.
16. `svg_source_mode` (`string`): `template_default`, `injected_markup`, or `external_file`.
17. `svg_inline_markup` (`string`): Custom raw SVG markup to inject into stage.

---

## 2. CanvasFrameSequence (Format 105a)

- **Record_Type**: `["CanvasFrameSequence"]`
- **Primary Key**: `record_uuid` (at `row[0]`)

### Fields Roster
1. `frame_index` (`integer`): 0-indexed frame number.
2. `seek_progress` (`number`): Floating-point timeline seek ratio ($0.0 \le \text{ratio} \le 1.0$).
3. `timestamp_sec` (`number`): Exact timeline position in seconds.
4. `frame_filename` (`string`): File path for the frame PNG.
5. `is_rendered_flag` (`boolean`): Rendering verification status.
6. `checksum_sha256` (`string`): SHA-256 integrity hash of the captured PNG file.
