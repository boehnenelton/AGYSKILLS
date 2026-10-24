---
name: cli-standardizer
description: Scaffold, standardize, or refactor standalone Python CLI tools with embedded configuration defaults, first-run config bootstrapping, embedded BEJSON Core and Validator engines, deterministic exit codes, structured logging, and standard CLI flags (--help, --version, --about, --config, --validate). Use when creating or modernizing non-file-processing CLI tools, utility scripts, or operational commands. Do NOT use for file-processing asset pipelines or media conversion tools (use cli-processing-standardizer).
---
# cli-standardizer

Standardize general-purpose Python CLI tools with Python 3.10+ runtime guards, deterministic exit-code registries, pre-bootstrap argument parsing (`--help`/`--version`/`--about` never blocked by first run), embedded default configuration dictionaries with type/range sanitization, script-relative path anchoring, embedded BEJSON Core and Validator engines (with O(1) edge-whitespace sanitization and duplicate field-name checks), and structured `logging` output.

## When to Use

Use this skill when creating or refactoring general-purpose command-line tools that do not rely on an `assets/` file-processing dropzone:

- Scaffolding new standalone Python CLI tools or utilities requiring embedded configuration defaults, validation routines, and consistent flag handling.
- Refactoring existing scripts to embed core operations and validation inline without external library dependencies.
- Standardizing command-line argument parsing with uniform `-h`/`--help`, `-v`/`--version`, `--about`, and custom config overrides.
- Building tools that inspect, query, mutate, or validate structured data or BEJSON documents directly via terminal commands.

## When NOT to Use

Do NOT use this skill for:

- File-processing pipelines, batch media converters, image resizers, audio splitters, or slideshow tools that rely on auto-detecting files in an `assets/` folder and writing to `out/` (use `cli-processing-standardizer`).
- Web applications, Flask/FastAPI REST APIs, or background daemon services.
- Multi-file database architectural planning without CLI tool implementation (use `planning-schema-planner`).

## Core Standardization Principles

### 1. Python 3.10+ Guard & Deterministic Exit-Code Registry
Every tool enforces Python 3.10+ at startup and defines a deterministic exit-code registry:

```python
EXIT_OK             = 0
EXIT_ACTION_FAILURE = 1
EXIT_PATH_FAILURE   = 10
EXIT_ENV_FAILURE    = 20
EXIT_SCHEMA_FAILURE = 30
EXIT_BUSY           = 50
EXIT_INTERRUPTED    = 130
```

### 2. Script-Relative Portability
The tool anchors default paths relative to its own file location:

```python
SCRIPT_PATH = Path(__file__).resolve().parent
CONFIG_DIR  = SCRIPT_PATH / "config"
LOGS_DIR    = SCRIPT_PATH / "logs"
CONFIG_FILE = CONFIG_DIR / "config.json"
```

### 3. Pre-Bootstrap Argument Parsing & Validated Configuration
- `build_parser().parse_args()` runs before `initialize_config()` so `--help`, `--version`, and `--about` execute cleanly without creating directories on an uninitialized tree.
- `initialize_config()` atomically writes `DEFAULT_CONFIG` to `config/config.json` on first run via `write_json_atomic()`.
- `load_config()` merges user settings over `copy.deepcopy(DEFAULT_CONFIG)`. If `-c`/`--config` is passed explicitly and the file is missing or unreadable, it raises `ConfigError` (`EXIT_ENV_FAILURE`).
- `sanitize_config()` validates types and allowed values for every setting, falling back to defaults with a warning on invalid values.

### 4. Embedded BEJSON Core & Validator with O(1) Edge Sanitization
- **Boundary-Layer Sanitization (`bejson_core_sanitize_doc`)**: Strips whitespace from keys and field definitions, and uses an O(1) first/last character check (`v[0].isspace() or v[-1].isspace()`) on string cell values so large strings are never linearly scanned or copied when already clean.
- **Duplicate Field Rejection**: `bejson_validator_check_fields_structure()` rejects duplicate field names in `Fields`.
- **O(1) Field Map Caching & Atomic I/O**: All record reads/mutations use `bejson_core_get_field_map()`, and all writes use `bejson_core_atomic_write()`.

### 5. Structured Console & Rotating File Logging
Uses Python's `logging` module rather than `print()` statements:
- `_ConsoleFormatter` applies Elton Boehnen's palette (`#DE2626` red accent for warnings/errors, `#FFEEDD` cream for info) when `sys.stdout.isatty()` and `NO_COLOR` is unset.
- `attach_file_logging()` attaches a `RotatingFileHandler` (`logs/cli_tool.log`, 1 MB × 3 backups).

## Workflows

### Workflow 1: Scaffolding a New Standardized CLI Tool

1. Copy the starter template from `assets/cli_standard_template.py`.
2. Update metadata headers: tool name, description, date, and assign a fresh `RELATIONAL_ID` UUID.
3. Define tool-specific configuration parameters inside `DEFAULT_CONFIG` and `sanitize_config()`.
4. Extend `build_parser()` with domain-specific command flags, positional arguments, or subcommands while preserving `--help`, `--version`, `--about`, `--config`, `--validate`, and `--stats`.
5. Implement execution logic in `main()` returning deterministic exit codes.

## Checklist for Validation

- [ ] Does the script enforce a Python 3.10+ version check and deterministic exit codes?
- [ ] Does `build_parser().parse_args()` run before `initialize_config()`?
- [ ] Does `initialize_config()` write `config/config.json` atomically?
- [ ] Does `load_config()` + `sanitize_config()` validate settings and fail fast on missing explicit `--config`?
- [ ] Does `bejson_core_sanitize_doc()` use O(1) edge-whitespace checks on string values?
- [ ] Are all status/error messages routed through `logging` (`LOG.info`, `LOG.warning`, `LOG.error`)?
