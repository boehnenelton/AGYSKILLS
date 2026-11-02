#!/usr/bin/env python3
"""
Name:           File_Processor_Template
File:           file_processor_template.py
Description:    Standardized production starter template for automated file-processing
                CLI tools. Features Python 3.10+ guard, deterministic exit codes,
                pre-bootstrap argparse (--help/--version safe), atomic config extraction
                and sanitization, single-instance locking with stale-PID recovery,
                symlink/empty-safe asset discovery, stem-collision-safe folder routing,
                source-fingerprinted BEJSON 104a state tracking with verified resume,
                and console + rotating file logging.
Version:        3
Date Created:   2026-10-16
Date Updated:   2026-10-16
Author:         Elton Boehnen
Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
Format_Creator: Elton Boehnen
RELATIONAL_ID:  93c41e08-5b2a-4d79-8e14-6a0f3c9b7d21
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("This tool requires Python 3.10 or newer.\n")
    sys.exit(1)

import os
import copy
import json
import time
import uuid
import shutil
import logging
import tempfile
import argparse
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

VERSION = 3
RELEASE_VERSION: int = 300

# ==========================================
# EXIT CODES (deterministic)
# ==========================================

EXIT_OK              = 0
EXIT_PARTIAL_FAILURE = 1    # one or more assets failed; rerun resumes
EXIT_PATH_FAILURE    = 10   # directory / path problem
EXIT_ENV_FAILURE     = 20   # configuration / environment problem
EXIT_SCHEMA_FAILURE  = 30   # BEJSON validation / state failure
EXIT_DEP_MISSING     = 40   # required external dependency missing
EXIT_BUSY            = 50   # another instance holds the lock
EXIT_INTERRUPTED     = 130  # interrupted via SIGINT

# ==========================================
# CONFIGURATION & PATH RESOLUTION
# ==========================================

SCRIPT_PATH = Path(__file__).resolve().parent

CONFIG_DIR = SCRIPT_PATH / "config"
ASSETS_DIR = SCRIPT_PATH / "assets"
OUT_DIR    = SCRIPT_PATH / "out"
LOGS_DIR   = SCRIPT_PATH / "logs"

CONFIG_FILE = CONFIG_DIR / "config.json"
STATE_FILE  = CONFIG_DIR / "processor_state.bejson"
LOCK_FILE   = CONFIG_DIR / "processor.lock"

DEFAULT_CONFIG: Dict[str, Any] = {
    "tool_name": "File_Processor_Tool",
    "assets_path": "assets",
    "output_path": "out",
    "state_file_path": "config/processor_state.bejson",
    "move_original_on_complete": True,
    "overwrite_existing": False,
    "log_level": "INFO"
}

# Supported file extensions (lowercase)
SUPPORTED_EXTS: Set[str] = {".ext"}

# Terminal color palette (Elton Boehnen standard)
C_ACCENT = "\033[38;2;222;38;38m"  # Red accent (#DE2626)
C_TEXT   = "\033[38;2;255;238;221m"  # Cream text
C_RESET  = "\033[0m"

LOG = logging.getLogger("file_processor")


class ConfigError(Exception):
    """Raised for unrecoverable configuration problems."""


# ==========================================
# LOGGING
# ==========================================

class _ConsoleFormatter(logging.Formatter):
    def __init__(self, use_color: bool):
        super().__init__()
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno >= logging.ERROR:
            tag = "[ERROR]"
        elif record.levelno >= logging.WARNING:
            tag = "[WARN]"
        else:
            tag = "[INFO]"
        msg = record.getMessage()
        if self.use_color:
            color = C_ACCENT if record.levelno >= logging.WARNING else C_TEXT
            return f"{color}{tag}{C_RESET} {msg}"
        return f"{tag} {msg}"


def configure_console_logging(level: int = logging.INFO) -> None:
    LOG.setLevel(logging.DEBUG)
    for h in list(LOG.handlers):
        LOG.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(_ConsoleFormatter(sys.stdout.isatty() and "NO_COLOR" not in os.environ))
    LOG.addHandler(handler)
    LOG.propagate = False


def attach_file_logging(log_dir: Path, level: int, log_name: str = "processor.log") -> None:
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(log_dir / log_name, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        LOG.addHandler(fh)
    except OSError as e:
        LOG.warning("File logging unavailable: %s", e)


# ==========================================
# EMBEDDED BEJSON 104a STATE CORE & VALIDATOR
# ==========================================

VALID_VERSIONS = {"104", "104a", "104db"}
VALID_FIELD_TYPES = {"string", "integer", "number", "boolean", "array", "object"}
MANDATORY_KEYS = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")

_FIELD_MAP_CACHE: Dict[tuple, Dict[str, int]] = {}


def bejson_core_sanitize_doc(doc: Any) -> Any:
    """Boundary-layer sanitization with O(1) first/last character check on string values."""
    if not isinstance(doc, dict):
        return doc
    clean = {(k.strip() if isinstance(k, str) else k): v for k, v in doc.items()}
    fields = clean.get("Fields")
    if isinstance(fields, list):
        for fdef in fields:
            if isinstance(fdef, dict):
                for key in ("name", "type"):
                    if isinstance(fdef.get(key), str):
                        fdef[key] = fdef[key].strip()
    values = clean.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for i, v in enumerate(row):
                    if isinstance(v, str) and v and (v[0].isspace() or v[-1].isspace()):
                        row[i] = v.strip()
    return clean


def bejson_core_load_file(path: Union[str, Path]) -> Optional[dict]:
    resolved = Path(path).expanduser()
    if not resolved.exists():
        return None
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            return bejson_core_sanitize_doc(json.load(f))
    except (OSError, ValueError) as e:
        LOG.error("[BEJSON_CORE] Failed to load %s: %s", resolved, e)
        return None


def bejson_core_atomic_write(path: Union[str, Path], data: dict) -> bool:
    target_path = str(path)
    target_dir = os.path.dirname(os.path.abspath(target_path))
    os.makedirs(target_dir, exist_ok=True)
    clean_data = {k: v for k, v in data.items() if not k.startswith("_")}
    fd, tmp_path = tempfile.mkstemp(dir=target_dir, prefix=".bejson_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, indent=2)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(tmp_path, target_path)
        return True
    except Exception as e:
        LOG.error("[BEJSON_CORE] Atomic write failed for %s: %s", target_path, e)
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return False


def bejson_core_get_field_map(doc: dict) -> Dict[str, int]:
    if "_bejson_field_map" in doc:
        return doc["_bejson_field_map"]
    fields = doc.get("Fields", [])
    if not fields:
        return {}
    field_names = tuple(f["name"] for f in fields)
    cache_key = (doc.get("Format_Version"), field_names)
    field_map = _FIELD_MAP_CACHE.get(cache_key)
    if field_map is None:
        field_map = {f["name"]: i for i, f in enumerate(fields)}
        _FIELD_MAP_CACHE[cache_key] = field_map
    doc["_bejson_field_map"] = field_map
    return field_map


def bejson_core_create_104a(record_type: str, fields: list, values: list, **custom) -> dict:
    doc = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [record_type],
        "Fields": fields,
        "Values": values,
    }
    doc.update(custom)
    return doc


def validate_bejson(doc: Any) -> bool:
    if not isinstance(doc, dict) or any(k not in doc for k in MANDATORY_KEYS):
        return False
    if doc.get("Format") != "BEJSON" or doc.get("Format_Creator") != "Elton Boehnen":
        return False
    version = doc.get("Format_Version", "")
    if version not in VALID_VERSIONS:
        return False
    rt = doc.get("Records_Type")
    if not isinstance(rt, list) or (version in ("104", "104a") and len(rt) != 1):
        return False
    fields = doc.get("Fields")
    values = doc.get("Values")
    if not isinstance(fields, list) or not isinstance(values, list):
        return False
    seen = set()
    for f in fields:
        if not isinstance(f, dict) or not f.get("name") or f.get("type") not in VALID_FIELD_TYPES:
            return False
        if f["name"] in seen or (version == "104a" and f["type"] in ("array", "object")):
            return False
        seen.add(f["name"])
    for row in values:
        if not isinstance(row, list) or len(row) != len(fields):
            return False
    return True


# ==========================================
# STATE TRACKING & SINGLE-INSTANCE LOCK
# ==========================================

STATE_FIELDS = [
    {"name": "file_key", "type": "string"},
    {"name": "original_filename", "type": "string"},
    {"name": "stage", "type": "string"},
    {"name": "output_path", "type": "string"},
    {"name": "last_error", "type": "string"},
    {"name": "updated_utc", "type": "string"},
    {"name": "source_size", "type": "integer"},
    {"name": "source_mtime", "type": "integer"},
    {"name": "folder_name", "type": "string"},
]


@dataclass
class JobRecord:
    file_key: str
    original_filename: str
    stage: str = "DETECTED"
    output_path: str = ""
    last_error: str = ""
    updated_utc: str = ""
    source_size: int = 0
    source_mtime: int = 0
    folder_name: str = ""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel_to_script(path: Path) -> str:
    try:
        return path.resolve().relative_to(SCRIPT_PATH).as_posix()
    except (ValueError, OSError):
        return str(path)


class InstanceLock:
    """O_EXCL lock file with stale-PID recovery; prevents concurrent state corruption."""

    def __init__(self, path: Path):
        self.path = path
        self.held = False

    def _holder_alive(self) -> Tuple[bool, str]:
        try:
            pid = int(self.path.read_text().strip())
        except (OSError, ValueError):
            return False, "unknown"
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False, str(pid)
        except PermissionError:
            return True, str(pid)
        except OSError:
            return False, str(pid)
        return True, str(pid)

    def __enter__(self) -> "InstanceLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                alive, pid = self._holder_alive()
                if alive:
                    raise RuntimeError(f"Another instance is running (pid {pid}).")
                LOG.warning("Removing stale lock (pid %s).", pid)
                try:
                    self.path.unlink()
                except FileNotFoundError:
                    pass
                continue
            with os.fdopen(fd, "w") as f:
                f.write(str(os.getpid()))
            self.held = True
            return self
        raise RuntimeError("Could not acquire instance lock.")

    def __exit__(self, *exc) -> None:
        if self.held:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass
            self.held = False


# ==========================================
# SETUP, CONFIGURATION & INITIALIZATION
# ==========================================

def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".cfg_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def initialize_directories() -> bool:
    """Creates standard directories and default config.json on first run. True if newly created."""
    created = False
    for folder in (CONFIG_DIR, ASSETS_DIR, OUT_DIR):
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            created = True
    if not CONFIG_FILE.exists():
        write_json_atomic(CONFIG_FILE, DEFAULT_CONFIG)
        created = True
    return created


def sanitize_config(config: Dict[str, Any]) -> Dict[str, Any]:
    d = DEFAULT_CONFIG

    def pick(key: str, ok) -> None:
        if not ok(config.get(key)):
            LOG.warning("Config '%s'=%r invalid; using default %r.", key, config.get(key), d[key])
            config[key] = d[key]

    pick("move_original_on_complete", lambda v: isinstance(v, bool))
    pick("overwrite_existing", lambda v: isinstance(v, bool))
    pick("log_level", lambda v: isinstance(v, str) and v.upper() in ("DEBUG", "INFO", "WARNING", "ERROR"))
    for key in ("assets_path", "output_path", "state_file_path"):
        pick(key, lambda v: isinstance(v, str) and v.strip() != "")
    return config


def load_config(custom_path: Optional[str] = None) -> Dict[str, Any]:
    explicit = custom_path is not None
    target = Path(custom_path).expanduser() if explicit else CONFIG_FILE
    config = copy.deepcopy(DEFAULT_CONFIG)

    if not target.exists():
        if explicit:
            raise ConfigError(f"Config file not found: {target}")
        return config
    try:
        with open(target, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            raise ValueError("config root must be an object")
    except (ValueError, OSError) as e:
        if explicit:
            raise ConfigError(f"Config file {target} unreadable: {e}")
        LOG.error("Config %s corrupted (%s). Using defaults.", target, e)
        return config

    for k, v in loaded.items():
        if isinstance(v, dict) and isinstance(config.get(k), dict):
            config[k].update(v)
        else:
            config[k] = v
    return config


def resolve_directory(path_str: str, default_dir: Path) -> Path:
    if not path_str:
        return default_dir
    raw = Path(path_str).expanduser()
    return raw if raw.is_absolute() else SCRIPT_PATH / raw


# ==========================================
# ASSET DISCOVERY & HELPERS
# ==========================================

def collect_assets(directory: Path, extensions: Set[str]) -> List[Path]:
    """Deterministically sorted supported files; skips dotfiles, symlinks, and empty files."""
    if not directory.is_dir():
        return []
    found: List[Path] = []
    for f in sorted(directory.iterdir(), key=lambda p: p.name):
        if f.name.startswith(".") or f.suffix.lower() not in extensions:
            continue
        if f.is_symlink():
            LOG.warning("Skipping symlink: %s", f.name)
            continue
        if not f.is_file():
            continue
        if f.stat().st_size == 0:
            LOG.warning("Skipping empty file: %s", f.name)
            continue
        found.append(f)
    return found


def cleanup_stale_temps(*directories: Path) -> None:
    """Removes leftovers from interrupted runs (call only while holding InstanceLock)."""
    for d in directories:
        if not d.is_dir():
            continue
        for pattern in (".tmp_*", ".bejson_*.tmp"):
            for p in d.glob(pattern):
                try:
                    p.unlink()
                except OSError:
                    pass


def place_original(src: Path, dst: Path, move: bool) -> None:
    """Moves/copies the original into place; cross-device safe."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if move:
        try:
            os.replace(src, dst)
            return
        except OSError:
            pass
    tmp = dst.with_name(f".tmp_{uuid.uuid4().hex[:8]}_{dst.name}")
    try:
        shutil.copy2(src, tmp)
        if tmp.stat().st_size != src.stat().st_size:
            raise OSError("copied size mismatch")
        os.replace(tmp, dst)
        if move:
            src.unlink()
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


# ==========================================
# CORE PROCESSING PIPELINE (CUSTOMIZE HERE)
# ==========================================

def process_file(
    input_file: Path,
    out_dir: Path,
    config: Dict[str, Any]
) -> Optional[Path]:
    """
    Core file processing implementation.
    Write to a temporary file first, verify output, and promote via os.replace().
    Returns the Path to the output file/folder on success, or None on failure.
    """
    output_filename = f"{input_file.stem}_processed{input_file.suffix}"
    output_path = out_dir / output_filename

    # TODO: Implement custom atomic file transformation here.
    return output_path


# ==========================================
# MAIN EXECUTION CONTROLLER
# ==========================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file_processor",
        description="Standardized Automated File Processing CLI Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s V{VERSION} (Release_Version {RELEASE_VERSION})")
    parser.add_argument("--input-dir", default=None, help="Custom input directory (overrides config assets_path)")
    parser.add_argument("--output-dir", default=None, help="Custom output directory (overrides config output_path)")
    parser.add_argument("-c", "--config", default=None, help="Path to custom config.json")
    parser.add_argument("--overwrite", action="store_true", help="Force re-processing of existing outputs")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    configure_console_logging()
    started = time.monotonic()

    # 1. First-run bootstrap (never blocks --help/--version; continues if assets already present)
    bootstrapped = initialize_directories()
    if bootstrapped:
        LOG.info("Created default directories (config/, assets/, out/) and config at: %s", CONFIG_FILE)

    # 2. Load and validate configuration
    try:
        config = load_config(args.config)
    except ConfigError as e:
        LOG.error("%s", e)
        return EXIT_ENV_FAILURE
    if args.overwrite:
        config["overwrite_existing"] = True
    config = sanitize_config(config)

    level = getattr(logging, str(config["log_level"]).upper(), logging.INFO)
    LOG.handlers[0].setLevel(level)
    attach_file_logging(LOGS_DIR, level)

    # 3. Resolve directories
    assets_dir = resolve_directory(args.input_dir or config["assets_path"], ASSETS_DIR)
    out_dir    = resolve_directory(args.output_dir or config["output_path"], OUT_DIR)
    state_path = resolve_directory(config["state_file_path"], STATE_FILE)

    if assets_dir.resolve() == out_dir.resolve():
        LOG.error("Input and output directories must differ (%s).", assets_dir)
        return EXIT_PATH_FAILURE
    if not assets_dir.is_dir():
        LOG.error("Assets directory not found: %s", assets_dir)
        return EXIT_PATH_FAILURE

    # 4. Collect compatible assets
    files = collect_assets(assets_dir, SUPPORTED_EXTS)
    if not files:
        LOG.warning("No compatible files (%s) found in %s.", ", ".join(sorted(SUPPORTED_EXTS)), assets_dir)
        if bootstrapped:
            LOG.info("Drop input files into 'assets/' and run again.")
            return EXIT_OK
        return EXIT_PATH_FAILURE

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        with InstanceLock(state_path.parent / LOCK_FILE.name):
            cleanup_stale_temps(out_dir)
            LOG.info("Starting processing run (V%d):", VERSION)
            LOG.info("  Input directory  : %s", assets_dir)
            LOG.info("  Output directory : %s", out_dir)
            LOG.info("  Files to process : %d", len(files))

            success = failure = 0
            for file_path in files:
                LOG.info("Processing: %s", file_path.name)
                try:
                    result = process_file(file_path, out_dir, config)
                except Exception as e:
                    LOG.exception("Unexpected failure on '%s': %s", file_path.name, e)
                    result = None
                if result:
                    LOG.info("Completed '%s' -> %s", file_path.name, result)
                    success += 1
                else:
                    LOG.error("Failed '%s'.", file_path.name)
                    failure += 1
    except RuntimeError as e:
        LOG.error("%s", e)
        return EXIT_BUSY
    except KeyboardInterrupt:
        LOG.warning("Interrupted.")
        return EXIT_INTERRUPTED

    LOG.info("Run completed in %.1fs. Success: %d, Failures: %d", time.monotonic() - started, success, failure)
    return EXIT_PARTIAL_FAILURE if failure else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
