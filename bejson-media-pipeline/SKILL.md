---
name: bejson-media-pipeline
description: >-
  Build, architect, and maintain automated FFmpeg media automation toolkits, dropzone-based processing pipelines, and standalone audio/video tools backed by BEJSON (104/104a) and MFDB v1.31 persistence layers. Use when designing media processing tools, batch audio/video scripts, auto-slideshow generators, visualizers, watermarkers, transcoders, or clip chunkers where files in an assets folder are processed automatically with atomic I/O. Do NOT use for document chunking (use bejson-document-chunker).
---
# BEJSON Media Tools

A skill for building, structuring, and maintaining FFmpeg-based media toolkits and automation utilities built on BEJSON 104/104a formats and MFDB v1.31 database architecture.

## When to Use

- Creating new FFmpeg-based automation tools or expanding media toolkits.
- Architecting drop-and-run processing pipelines centered around an `assets/` dropzone.
- Implementing media processing tools backed by BEJSON 104/104a and MFDB v1.31 manifests.
- Adding batch media features: slideshows, audio visualizers, watermarkers, transcoders, clip chunkers, timelapse controllers, audio extractors, or contact sheet grids.
- Implementing robust media metadata probing, verification, and atomic file I/O with zero third-party dependencies.

## Architecture and Layout

A standard BEJSON Media Toolkit consists of an MFDB v1.31 root manifest, BEJSON 104a system configuration, BEJSON 104 data entities, core utility libraries, standalone modular tools, and designated asset/output directories:

```
media_toolkit/
├── 104a.mfdb.bejson         # Root MFDB v1.31 manifest (BEJSON 104a)
├── media_toolkit.py        # Master CLI orchestrator & interactive menu
├── README.md               # Architecture documentation & command reference
├── config/
│   └── 104a_config.bejson  # System configuration & encoding presets (BEJSON 104a)
├── data/
│   ├── tool_registry.bejson # Registered FFmpeg tools & contracts (BEJSON 104)
│   ├── asset_catalog.bejson # Detected dropzone media & stream metrics (BEJSON 104)
│   ├── job_history.bejson   # Execution audit logs & runtime metrics (BEJSON 104)
│   └── tool_presets.bejson  # Default encoding and filter definitions (BEJSON 104)
├── lib/
│   ├── bejson_core.py      # Field map caching, schema validation, and atomic file I/O
│   ├── mfdb_core.py        # Manifest syncing, entity registration, and job logging
│   └── media_utils.py      # FFprobe probing, sanitization, and ANSI terminal styling
├── tools/
│   ├── tool_01_slideshow.py             # Auto Slideshow Maker
│   ├── tool_02_audio_visualizer.py      # Waveform & Spectrum Visualizer
│   ├── tool_03_video_watermarker.py     # Video Watermarker & Branding Inserter
│   ├── tool_04_transcoder_compressor.py # Universal Transcoder & CRF Compressor
│   ├── tool_05_clip_chunker.py          # Video Clip Chunker & Shorts Splitter
│   ├── tool_06_speed_timelapse.py       # Speed & Timelapse Controller
│   ├── tool_07_audio_extractor.py       # Audio Track Extractor & Normalizer
│   └── tool_08_thumbnail_grid.py        # Video Storyboard Grid Generator
├── assets/                 # Dropzone folder (dump files here)
│   └── README.txt          # Dropzone format guidelines & instructions
└── output/                 # Output directory for processed media artifacts
```

## Mandatory Standards and Conventions

### 1. BEJSON 104 / 104a and MFDB v1.31 Compliance

- `Format` must strictly be `"BEJSON"`.
- `Format_Creator` must strictly be `"Elton Boehnen"`.
- Root manifest `104a.mfdb.bejson`: strictly `104a`, `Records_Type: ["mfdb"]`, `MFDB_Version: "1.31"`, with standard fields (`entity_name`, `file_path`, `description`, `record_count`, `primary_key`).
- Entity files in `data/*.bejson`: strictly `104`, `Records_Type: ["<EntityName>"]`, and required `Parent_Hierarchy: "../104a.mfdb.bejson"`.
- Manifest record counts must be kept synchronized using `mfdb_sync_manifest_counts()`.

### 2. O(1) Field Map Caching and Atomic File I/O

- Never read or write records by hardcoding numeric column indexes. Always resolve column positions dynamically through a cached field map (`bejson_get_field_map(doc)`).
- Every file write must be atomic: stage changes in a temporary file (`.bejson_<pid>_<name>.tmp`), flush buffers, handle `os.fsync` with a fallback for virtual mounts, and replace the target atomically using `os.replace`.

### 3. Terminal Styling and Visual Standards

- Terminal color palette must strictly use Black (`#000000`), Light Cream/White (`#FFFFFF` or `\033[38;2;255;238;221m`), and Elton's Signature Red (`#DE2626` or `\033[38;2;222;38;38m`).
- Use the standard Python `logging` library with custom colored formatters rather than raw print statements for processing output.
- Interactive terminal About menus must feature the mandated 3-tab structure ordered strictly as:
  1. **About** (overview, author attribution, format standards)
  2. **Change Log** (version history, updates)
  3. **Assets** (dropzone inventory, detected media types)

### 4. Zero External Pip Dependencies

- Build entirely with standard Python 3.10+ libraries (`subprocess`, `pathlib`, `json`, `logging`, `shutil`, `re`, `time`, `uuid`, `argparse`).
- Tools must execute seamlessly across Android Termux, Linux, macOS, and Windows environments where `ffmpeg` and `ffprobe` are present on `PATH`.

## The 8 Core FFmpeg Tool Patterns

### Tool 1: Auto Slideshow Maker (`tool_01_slideshow.py`)

- Scans `assets/` for image sequences and audio files.
- Applies natural numeric-alpha sorting (`01_intro` < `02_main` < `10_outro`) via regex chunking.
- Probes audio duration and divides time evenly across images (`max(0.5, audio_duration / len(images))`).
- Generates an FFmpeg concat list with file paths properly escaped for cross-platform compatibility.
- Repeats the last image as a durationless sentinel to avoid dropped final frames.
- Applies aspect-ratio preservation with centered letterboxing:
  `scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2:black,setsar=1`

### Tool 2: Audio Reactive Visualizer (`tool_02_audio_visualizer.py`)

- Renders dynamic audio waveforms or frequency spectrums synced to audio files in `assets/`.
- If a background image is present, scales the image and composites the waveform overlay with transparency:
  `[0:a]showwaves=s=1280x240:mode=line:colors=0xDE2626@0.9:scale=cbrt[wv];[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,setsar=1[bg];[bg][wv]overlay=(W-w)/2:H-h-40[outv]`
- If no image is present, generates a canvas in black with a red waveform overlay.

### Tool 3: Video Watermarker (`tool_03_video_watermarker.py`)

- Detects video files and watermark/logo images in `assets/`.
- Pre-probes video width in Python and calculates watermark width (e.g. 15% of main video width):
  `target_wm_w = max(64, int(video_width * 0.15))`
- Scales watermark to `scale={target_wm_w}:-1` and applies overlay coordinates:
  - `bottom-right`: `main_w-overlay_w-24:main_h-overlay_h-24`
  - `top-right`: `main_w-overlay_w-24:24`
  - `bottom-left`: `24:main_h-overlay_h-24`
  - `top-left`: `24:24`
  - `center`: `(main_w-overlay_w)/2:(main_h-overlay_h)/2`

### Tool 4: Universal Transcoder & Compressor (`tool_04_transcoder_compressor.py`)

- Batch transcodes media to MP4, WebM, MKV, MP3, AAC, FLAC, or Opus.
- Provides CRF compression presets: 18 (near-lossless), 23 (balanced default), 28 (compact file size).
- Handles video downscaling with letterboxing (1080p, 720p, 480p).
- Preserves audio fidelity with configurable bitrates (128k, 192k, 320k).

### Tool 5: Video Clip Chunker (`tool_05_clip_chunker.py`)

- Splits long-form videos into short segments (e.g. 15s, 30s, 60s) for short-form platforms or archives.
- Supports instant lossless stream copying (`-c copy`) and frame-accurate re-encoding (`-c:v libx264 -crf 23`).
- Uses FFmpeg segment muxer:
  `-f segment -segment_time {seconds} -reset_timestamps 1 output/%03d.mp4`
- Verifies output chunks by checking candidate paths directly rather than relying on directory readdir.

### Tool 6: Speed & Timelapse Controller (`tool_06_speed_timelapse.py`)

- Adjusts playback speed (0.25x to 8x).
- Calculates presentation timestamp multiplier: `pts_factor = round(1.0 / speed, 6)`.
- Chains multiple `atempo` audio filters since FFmpeg's `atempo` filter is strictly bounded to the interval [0.5, 2.0]:
  For speed = 4.0x: `atempo=2.0,atempo=2.0`.

### Tool 7: Audio Extractor & Normalizer (`tool_07_audio_extractor.py`)

- Strips audio tracks from video containers into MP3 (320kbps), WAV (PCM 16-bit), FLAC, AAC, or Opus.
- Provides optional broadcast volume normalization via the EBU R128 `loudnorm` filter:
  `-af loudnorm=I=-16:TP=-1.5:LRA=11`

### Tool 8: Storyboard Grid Generator (`tool_08_thumbnail_grid.py`)

- Samples keyframes evenly across video duration: `interval = duration / (cols * rows + 1)`.
- Assembles tiled contact sheets (e.g. 3x3 or 4x3) for video inspection:
  `-vf fps=1/{interval},scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:black,tile={cols}x{rows} -frames:v 1 -q:v 2`

## Implementation Workflow

When building or extending a BEJSON Media Toolkit:

1. **Verify Environment**: Run `check_dependencies()` to confirm `ffmpeg` and `ffprobe` availability.
2. **Initialize MFDB & Config**: Write `104a.mfdb.bejson`, `config/104a_config.bejson`, and entity files with strict BEJSON schemas.
3. **Scan Dropzone**: Inspect `assets/` and bucket files into `images`, `audio`, `video`, and `watermarks`.
4. **Probe & Catalog**: Probe duration, dimensions, codecs, and bitrates with `ffprobe -of json`, then record entries in `AssetCatalog`.
5. **Execute & Verify**: Run FFmpeg commands via `subprocess.run()`, verify generated file sizes and durations with `verify_media_output()`.
6. **Audit & Log**: Record job status, duration, and execution commands in `JobHistory`.
7. **Sync Manifest**: Call `mfdb_sync_manifest_counts()` to update entity record counts in the root manifest.

## Gotchas and Pitfalls

- **FFmpeg Filter Parameters**: Never pass `main_w` or `main_h` into the `scale` filter; those variables exist only in `overlay`. Calculate scaled dimensions in Python before building filter strings.
- **Atempo Range Bounds**: FFmpeg's `atempo` filter fails if passed values outside `[0.5, 2.0]`. Always factorize and chain filters for higher or lower multipliers.
- **Directory Caching on 9p / Virtual Mounts**: When verifying multi-part outputs (such as segment chunks), do not rely on `Path.glob()` or `os.scandir()`. Check explicit file existence using `(out_dir / filename).exists()`.
- **fsync on OverlayFS**: Always wrap `os.fsync()` calls in a `try...except OSError` block to avoid crashes on filesystems that do not support disk sync.
- **Concat Demuxer Escaping**: Escape single quotes and backslashes in file paths before writing concat files. Always include a sentinel final frame without duration to avoid dropping the last frame.
