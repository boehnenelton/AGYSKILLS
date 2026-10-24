---
name: cli-processing-standardizer
description: Create or refactor CLI file-processing tools to adhere to self-bootstrapping directory initialization, built-in default configuration extraction on first run, portable relative path resolution with external overrides, single-instance locking, resumable BEJSON state tracking, and smart asset auto-detection. Use when creating or refactoring Python CLI tools specifically for file processing, batch media conversions, asset pipelines, or document transforms. Do NOT use for general scripts, web APIs, or non-file CLI utilities.
---
# cli-processing-standardizer

Standardize Python CLI tools specifically designed for automated file and asset processing. Enforces Python 3.10+ runtime guards, deterministic exit-code registries, pre-bootstrap CLI flag parsing (`--help`/`--version` never blocked by first run), built-in default configuration extraction with type/range validation, portable script-relative path resolution, single-instance locking (`InstanceLock`), smart asset discovery, source-fingerprinted resumable state tracking, and structured `logging` output.

## When to Use

Use this skill exclusively when creating or refactoring command-line tools that perform file or asset processing:

- Creating new automated file-processing CLI tools (video cutters, audio splitters, Base64 media encoders, image processors, slideshow generators, format converters).
- Refactoring existing file-processing Python scripts that suffer from hardcoded absolute paths, `print()` logging, missing configuration validation, or lack of resumable state tracking.
- Standardizing file-drop workflows where users place assets into an input folder (`assets/`) and the CLI automatically discovers, validates, processes, and separates or moves them one by one into `out/`.

## When NOT to Use

Do NOT use this skill for:

- General-purpose shell scripts or administrative automation without file processing pipelines.
- Web APIs, Flask or FastAPI services, database migrations, or daemon background services.
- CLI utilities that do not process files from an input directory (use `cli-standardizer`).

## Core Standardization Principles

### 1. Python 3.10+ Guard & Deterministic Exit-Code Registry
Every tool starts with an explicit Python 3.10+ version check and defines a deterministic exit-code registry:

```python
EXIT_OK              = 0
EXIT_PARTIAL_FAILURE = 1    # one or more assets failed; rerun resumes
EXIT_PATH_FAILURE    = 10   # directory / path problem
EXIT_ENV_FAILURE     = 20   # configuration / environment problem
EXIT_SCHEMA_FAILURE  = 30   # BEJSON validation / checksum failure
EXIT_DEP_MISSING     = 40   # external binary (e.g. ffmpeg) missing
EXIT_BUSY            = 50   # another instance holds the lock
EXIT_INTERRUPTED     = 130  # SIGINT / KeyboardInterrupt
```

### 2. Pre-Bootstrap Argument Parsing & First-Run Initialization
- `build_parser().parse_args()` always runs **before** `initialize_directories()` so `--help` and `--version` work cleanly without creating folders on an uninitialized tree.
- `initialize_directories()` atomically extracts `DEFAULT_CONFIG` into `config/config.json` and creates `config/`, `assets/`, and `out/`.
- If `assets/` is empty on first run, the tool logs instructions to drop files into `assets/` and exits cleanly with `EXIT_OK (0)`. If `assets/` already contains compatible files on first run, processing proceeds immediately without requiring a second invocation.

### 3. Script-Relative Portability with Validated Overrides
The script never assumes the current working directory (`cwd`) is where the script resides:

```python
SCRIPT_PATH = Path(__file__).resolve().parent
CONFIG_DIR  = SCRIPT_PATH / "config"
ASSETS_DIR  = SCRIPT_PATH / "assets"
OUT_DIR     = SCRIPT_PATH / "out"
LOGS_DIR    = SCRIPT_PATH / "logs"
CONFIG_FILE = CONFIG_DIR / "config.json"
LOCK_FILE   = CONFIG_DIR / "processor.lock"
```

- Paths stored in state files use `rel_to_script(path)` so project directories remain portable across machines.
- `load_config()` merges user configuration over `copy.deepcopy(DEFAULT_CONFIG)`. If `-c`/`--config` is passed explicitly and the file is missing or malformed, it raises `ConfigError` (`EXIT_ENV_FAILURE`).
- `sanitize_config()` type-checks and range-validates every setting (including rejecting path separators or `..` in subfolder names), falling back to defaults with a warning on invalid values.

### 4. Single-Instance Lock & Stale Temp Cleanup
- `InstanceLock` uses `os.open(..., os.O_CREAT | os.O_EXCL | os.O_WRONLY)` and checks PID liveness via `os.kill(pid, 0)`, automatically recovering from stale locks left by crashed processes while returning `EXIT_BUSY (50)` if another instance is actively running.
- While holding `InstanceLock`, `cleanup_stale_temps()` removes leftover `.tmp_*` and `.bejson_*.tmp` files before processing stages run.

### 5. Smart Asset Discovery & Stem-Collision Disambiguation
- `collect_assets()` scans `assets/`, filtering for lowercase `SUPPORTED_EXTS` while skipping dotfiles, symlinks (with a warning), and 0-byte files.
- `choose_folder_name()` routes per-asset outputs to `out/<stem>/`, automatically disambiguating same-stem collisions (e.g. `clip.mp4` and `clip.wav` -> `out/clip_mp4/` and `out/clip_wav/`) and honoring any `folder_name` persisted in the state file across partial runs.

### 6. Resumable State Tracking & Atomic Output Placement
- Multi-stage pipelines track per-asset progress in a `BEJSON 104a` state file (`JobRecord` with `source_size`, `source_mtime`, `folder_name`, and stage booleans).
- Schema upgrades append new fields to the end of `STATE_FIELDS` and run idempotent `migrate_state_schema()` with automatic `.premigration` backups; corrupt state files are backed up (`.corrupt`) before re-initialization.
- Each stage writes to a temporary file in the target folder, verifies output integrity, and promotes via `os.replace()`.
- `place_original()` moves or copies source files using same-filesystem `os.replace()` with a cross-device copy + size-verification + unlink fallback.

### 7. Structured Console & Rotating File Logging
Uses Python's `logging` module rather than `print()` statements:
- `_ConsoleFormatter` applies Elton Boehnen's palette (`#DE2626` red accent for warnings/errors, `#FFEEDD` cream for info) when `sys.stdout.isatty()` and `NO_COLOR` is unset.
- `attach_file_logging()` attaches a `RotatingFileHandler` (`logs/<tool>.log`, 1 MB × 3 backups).

## Workflows

### Workflow 1: Creating a New File Processing CLI Tool

1. Copy the starter template from `assets/file_processor_template.py`.
2. Update header metadata (`Name`, `File`, `Description`, `Date Created`, and a fresh UUIDv4 `RELATIONAL_ID`).
3. Define domain-specific parameters in `DEFAULT_CONFIG` and validation rules in `sanitize_config()`.
4. Set `SUPPORTED_EXTS` to the required lowercase file extensions.
5. Implement `process_file()` with atomic temp writes, output verification, and `checkpoint()` updates.
6. Test `--help` and `--version` on a clean directory, first-run bootstrap, normal processing, and interrupted resume.

## Checklist for Validation

- [ ] Does the script enforce a Python 3.10+ version check and deterministic exit codes (`0/1/10/20/30/40/50/130`)?
- [ ] Does `build_parser().parse_args()` execute before `initialize_directories()` so `--help`/`--version` do not create folders?
- [ ] Does `initialize_directories()` use atomic JSON writes and proceed immediately if `assets/` is already populated?
- [ ] Does `load_config()` + `sanitize_config()` validate types/ranges and fail fast on missing explicit `--config`?
- [ ] Does `InstanceLock` guard the processing loop with stale-PID recovery?
- [ ] Does `collect_assets()` skip dotfiles, symlinks, and empty files?
- [ ] Are outputs written to temp files, verified, and atomically promoted via `os.replace()`?
- [ ] Is all output emitted through `logging` (`LOG.info`, `LOG.warning`, `LOG.error`) with rotating file logs?
