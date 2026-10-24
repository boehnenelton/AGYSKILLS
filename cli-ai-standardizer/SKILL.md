---
name: cli-ai-standardizer
description: Create, scaffold, or refactor standalone Python CLI AI file-processing and prompting tools powered by stdlib REST API dispatch (Gemini REST, OpenAI-compatible REST for Groq, OpenRouter, TokenRouter, Grok, HuggingFace, OpenAI, Ollama Cloud, and Ollama Local), round-robin API key rotation with retry backoff, self-bootstrapping directories, embedded BEJSON 104/104a validation, single-instance locking, XML command output parsing, and resumable state tracking. Use when building AI-powered CLI file processors, autoprompters, batch AI asset transformers, or refactoring CLI AI scripts to use zero-SDK REST endpoints. Do NOT use for non-AI media or local file converters (use cli-processing-standardizer) or non-AI general CLI utilities without REST LLM calls (use cli-standardizer).
---
# cli-ai-standardizer

Standardize Python CLI tools that combine automated `assets/` file-processing pipelines or one-shot terminal prompts with zero-SDK stdlib REST AI dispatch, round-robin key rotation, XML command output extraction, and resumable BEJSON 104a state tracking.

## Summary

Unifies the file-processing guarantees of `cli-processing-standardizer` and the embedded BEJSON 104/104a Core/Validator of `cli-standardizer` with the zero-SDK REST AI architecture from `CLI_AI`. Every generated tool uses Python's standard library (`urllib.request`) to call Gemini REST (`v1beta/models/<model>:generateContent`), OpenAI-compatible REST endpoints (`/v1/chat/completions` for Groq, OpenRouter, TokenRouter, Grok, HuggingFace, OpenAI, and Ollama Cloud), or local Ollama (`/api/chat`) without requiring third-party AI SDKs.

## When to Use

- Creating new AI-powered CLI file processors, autoprompters, code transformers, document analyzers, or batch LLM asset pipelines that process files from `assets/` into `out/`.
- Scaffolding standalone CLI AI tools that must run portably in Termux, Linux, or macOS using stdlib `urllib.request` REST calls rather than external SDK packages (`google-genai` or `openai`).
- Implementing round-robin API key rotation across `secureenv_file.json`, numbered environment variables (`GEMINI_KEY_1..30`, `GROQ_KEY_1..30`, `OPENROUTER_KEY_1..30`), and BEJSON 104a fallback key stores with automatic backoff retry on HTTP 429 and 5xx errors.
- Extracting structured multi-file outputs from LLM responses using XML command tags (such as `<file path="...">...</file>`) and promoting them atomically into `out/<stem>/`.

## When NOT to Use

- Creating local file-processing or FFmpeg media CLI tools that do not make AI/LLM API calls (use `cli-processing-standardizer`).
- Scaffolding general-purpose non-AI CLI utilities without an `assets/` dropzone or REST AI dispatcher (use `cli-standardizer`).
- Building multi-page web applications or Flask/FastAPI servers.

## Core Standardization Principles

### 1. Python 3.10+ Guard and Deterministic Exit-Code Registry

Every CLI AI tool enforces Python 3.10+ at startup and defines a deterministic exit-code registry:

```python
EXIT_OK              = 0
EXIT_PARTIAL_FAILURE = 1    # one or more assets/calls failed; rerun resumes
EXIT_PATH_FAILURE    = 10   # directory / path problem
EXIT_ENV_FAILURE     = 20   # configuration / environment / API key problem
EXIT_SCHEMA_FAILURE  = 30   # BEJSON validation / checksum failure
EXIT_DEP_MISSING     = 40   # external binary missing
EXIT_BUSY            = 50   # another instance holds the lock
EXIT_INTERRUPTED     = 130  # SIGINT / KeyboardInterrupt
```

### 2. Pre-Bootstrap Argument Parsing and First-Run Initialization

- Run `build_parser().parse_args()` before `initialize_directories()` so `--help`, `--version`, and `--about` execute cleanly without creating directories on an uninitialized tree.
- Support standard flags across all tools: `-v`/`--version`, `--about`, `-c`/`--config`, `-p`/`--provider`, `-m`/`--model`, `-s`/`--system`, `--prompt`, `--validate`, `--stats`, `--dry-run`, and `--verbose`.
- Atomically extract `DEFAULT_CONFIG` into `config/config.json` on first run and create `config/`, `assets/`, `out/`, and `logs/`.
- If `assets/` is empty on first run (and `--prompt` is not passed), log instructions to drop files into `assets/` and exit cleanly with `EXIT_OK (0)`. If `assets/` already contains compatible files on first run, proceed immediately with processing.

### 3. Script-Relative Portability with Validated Overrides

Anchor all paths relative to `SCRIPT_PATH` rather than `Path.cwd()`:

```python
SCRIPT_PATH   = Path(__file__).resolve().parent
CONFIG_DIR    = SCRIPT_PATH / "config"
ASSETS_DIR    = SCRIPT_PATH / "assets"
OUT_DIR       = SCRIPT_PATH / "out"
LOGS_DIR      = SCRIPT_PATH / "logs"
CONFIG_FILE   = CONFIG_DIR / "config.json"
STATE_FILE    = CONFIG_DIR / "job_state.104a.bejson"
KEYS_FILE     = CONFIG_DIR / "ai_keys.104a.bejson"
CALL_LOG_FILE = LOGS_DIR / "ai_call_log.104a.bejson"
LOCK_FILE     = CONFIG_DIR / "processor.lock"
```

- Persist relative paths in state files via `rel_to_script(path)` so project directories remain portable across machines.
- Merge user configuration over `copy.deepcopy(DEFAULT_CONFIG)` in `load_config()`. Raise `ConfigError` (`EXIT_ENV_FAILURE`) immediately if an explicit `-c`/`--config` file is missing or malformed.
- Validate types, numeric bounds, provider names, and subfolder names (rejecting `/`, `\`, `..`, or leading dots) in `sanitize_config()`.

### 4. Embedded BEJSON 104/104a Core and Validator Engine

- Use `bejson_core_sanitize_doc()` with O(1) first/last character whitespace checks (`v[0].isspace() or v[-1].isspace()`) so large prompt/response strings are never linearly scanned when already clean.
- Enforce strict BEJSON field types (`string`, `integer`, `number`, `boolean`, `array`, `object` - never `"any"`) and reject duplicate field names in `bejson_validator_check_fields_structure()`.
- Access all record columns through `bejson_core_get_field_map()` (O(1) cached dictionary) and persist all JSON/BEJSON files via `write_json_atomic()`.

### 5. Zero-SDK Stdlib REST AI Dispatch with Round-Robin Key Rotation

- **Non-Overwriting Environment Fill (`source_env_fill`)**: Load credentials from `/storage/emulated/0/.env/secure/secureenv_file.json` (or `.py` key-value lines) into `os.environ` without calling `exec()` and without overwriting existing environment variables.
- **Independent Slot Scanning (`RoundRobinKeyRegistry`)**: Scan single env vars (`GEMINI_API_KEY`), comma-separated lists (`GEMINI_API_KEYS`), and numbered slots (`GEMINI_KEY_1..30`, `GROQ_KEY_1..30`, `OPENROUTER_KEY_1..30`, `TOKENROUTER_KEY_1..30`, `GROK_KEY_1..30`, `HUGGINGFACE_MM_KEY_1..30`, `OPENAI_KEY_1..30`, `OLLAMA_KEY_1..30`) independently, followed by the `config/ai_keys.104a.bejson` fallback file while filtering out placeholder strings (`YOUR_`, `KEY_HERE`).
- **Singleton Rotation Cursor**: Cache the `RoundRobinKeyRegistry` instance per provider so `get_next_key()` advances across every call and retry attempt rather than resetting to slot 1.
- **Multi-Wire Stdlib REST Dispatch (`rest_ai_dispatch`)**:
  - `gemini_rest`: POSTs to `https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent` with `x-goog-api-key` header, `contents`, optional base64 `inline_data`, `system_instruction`, and `generationConfig`.
  - `openai_compat`: POSTs to `<base_url>/chat/completions` with `Authorization: Bearer <key>` for Groq, OpenRouter, TokenRouter, Grok, HuggingFace, OpenAI, and Ollama Cloud.
  - `ollama_local`: POSTs to `http://127.0.0.1:11434/api/chat` (`stream: false`) with no API key required.
- **Retry with Key Rotation**: On HTTP `(429, 500, 502, 503, 504)` or transient network/socket timeouts (and `401`/`403` when multiple keys are loaded), wait according to `retry_backoff_seconds` (`[5, 15, 30]`) and pull the next key from the round-robin registry on the next attempt. Return a normalized `AIResponse` TypedDict (`success`, `content`, `thought`, `error`, `provider`, `model_id`, `key_slot`, `attempts`, `raw`).

### 6. XML Command Output Instruction and Extraction

- When `enforce_xml_output` is enabled, append `build_xml_output_instruction(tag_name)` to instruct the model to emit output files inside `<file path="relative/path.ext">...</file>` XML command blocks.
- Parse responses with `parse_xml_file_commands()`, stripping accidental outer markdown code fences inside tag bodies, sanitizing relative file paths against directory traversal (`..`), and writing each extracted file atomically (`temp -> fsync -> size check -> os.replace()`) inside `out/<folder_name>/`.

### 7. Single-Instance Lock, Smart Asset Discovery, and Resumable State

- Guard processing with `InstanceLock` (`os.O_CREAT | os.O_EXCL | os.O_WRONLY` and `os.kill(pid, 0)` stale-lock recovery) and clean up leftover `.tmp_*` and `.bejson_*.tmp` files via `cleanup_stale_temps()`.
- Discover input files in `assets/` via `collect_assets()`, skipping dotfiles, symlinks, and 0-byte files, and disambiguate same-stem collisions via `choose_folder_name()`.
- Track per-asset progress in `config/job_state.104a.bejson` (`rel_path`, `source_size`, `source_mtime`, `folder_name`, `stage_prompted`, `stage_written`, `stage_completed`, `provider_used`, `model_used`, `files_emitted`, `updated_at`) with idempotent `migrate_state_schema()` and `.corrupt` backup recovery.

### 8. Structured Console and Rotating File Logging

- Route all output through Python's `logging` module (`LOG.info`, `LOG.warning`, `LOG.error`) rather than `print()`.
- Format TTY output with `_ConsoleFormatter` (`#DE2626` red accent for warnings/errors, `#FFEEDD` cream for info) while respecting `NO_COLOR`, and attach a `RotatingFileHandler` (`logs/<tool>.log`, 1 MB x 3 backups).

## Workflows

### Workflow 1: Creating a New Standardized CLI AI File Processor or Autoprompter

1. Copy the starter template from `assets/cli_ai_processor_template.py`.
2. Update top-of-file metadata (`Name`, `File`, `TOOL_NAME`, `PRODUCT_TITLE`, `DATE_CREATED`, and a fresh UUIDv4 `RELATIONAL_ID`).
3. Customize `DEFAULT_CONFIG` (`provider`, `model_id`, `system_instruction`, `prompt_template`, `xml_output_tag`, `enforce_xml_output`) and `SUPPORTED_EXTS` for the target domain.
4. If custom XML commands or multi-stage transformations are required, extend `build_xml_output_instruction()`, `parse_xml_file_commands()`, and `process_file()` while preserving atomic temp writes and `checkpoint_job()` calls.
5. Verify `--help`, `--version`, `--about`, first-run directory initialization, `--validate`, `--stats`, and `--dry-run` on a sample file in `assets/`.

## Checklist for Validation

- [ ] Enforces Python 3.10+ check and deterministic exit codes (`0/1/10/20/30/40/50/130`).
- [ ] Executes `build_parser().parse_args()` before `initialize_directories()` so `--help`, `--version`, and `--about` create zero folders.
- [ ] Uses stdlib `urllib.request` REST dispatch (`rest_ai_dispatch`) with singleton `RoundRobinKeyRegistry` rotation and backoff retries.
- [ ] Scans single env vars, comma-separated lists, and numbered key slots (`_1.._30`) independently after `source_env_fill()`.
- [ ] Validates BEJSON 104a state, key, and call-log files without using `"type": "any"`.
- [ ] Guards execution with `InstanceLock` and writes all outputs atomically via `os.replace()`.
- [ ] Emits all console and file output through `logging` with zero `print()` calls.

## Gotchas

- **Never instantiate a fresh KeyRegistry per call**: Always use the cached singleton `get_key_registry(provider, ...)` so the round-robin `_idx` cursor advances across calls and retry attempts.
- **Never use `"type": "any"` in BEJSON schemas**: Only `string`, `integer`, `number`, `boolean`, `array`, and `object` are valid BEJSON field types.
- **Sanitize XML file paths**: Always verify that resolved output paths from `<file path="...">` stay strictly inside `out/<folder_name>/` before writing to disk.
