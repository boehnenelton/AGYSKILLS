#!/usr/bin/env python3
"""
File        : cli_standard_template.py
Description : Standardized CLI executable template embedding Python 3.10+ guard,
              deterministic exit codes, pre-bootstrap argparse (--help/--version/--about
              safe), atomic default configuration extraction and sanitization,
              self-locating path resolution, embedded BEJSON Core operations with
              O(1) edge-whitespace sanitization, embedded BEJSON validator with
              duplicate field rejection, and console + rotating file logging.
Version     : 3
Release_Ver : 300
Author      : Elton Boehnen
Contact     : boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("This tool requires Python 3.10 or newer.\n")
    sys.exit(1)

import os
import copy
import json
import logging
import argparse
import tempfile
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ==========================================
# METADATA, VERSIONING & EXIT CODES
# ==========================================

VERSION: int = 3
RELEASE_VERSION: int = 300
RELATIONAL_ID: str = "2f8a4c19-7d3e-4b5a-9c61-0e4f8a2b1d77"

EXIT_OK             = 0
EXIT_ACTION_FAILURE = 1
EXIT_PATH_FAILURE   = 10
EXIT_ENV_FAILURE    = 20
EXIT_SCHEMA_FAILURE = 30
EXIT_BUSY           = 50
EXIT_INTERRUPTED    = 130

SCRIPT_PATH: Path = Path(__file__).resolve().parent
CONFIG_DIR: Path  = SCRIPT_PATH / "config"
LOGS_DIR: Path    = SCRIPT_PATH / "logs"
CONFIG_FILE: Path = CONFIG_DIR / "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "CLI_Standard_Tool",
    "version": VERSION,
    "release_version": RELEASE_VERSION,
    "log_level": "INFO",
    "strict_validation": True,
    "pretty_output": True
}

C_ACCENT = "\033[38;2;222;38;38m"  # Red accent (#DE2626)
C_TEXT   = "\033[38;2;255;238;221m"  # Cream text
C_RESET  = "\033[0m"

LOG = logging.getLogger("cli_standard_tool")


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


def attach_file_logging(log_dir: Path, level: int, log_name: str = "cli_tool.log") -> None:
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(log_dir / log_name, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        LOG.addHandler(fh)
    except OSError as e:
        LOG.warning("File logging unavailable: %s", e)


# ==========================================
# CONFIGURATION MANAGEMENT & BOOTSTRAP
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


def initialize_config() -> bool:
    """Bootstraps the config directory and default config.json atomically on first run."""
    created = False
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
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

    pick("log_level", lambda v: isinstance(v, str) and v.upper() in ("DEBUG", "INFO", "WARNING", "ERROR"))
    pick("strict_validation", lambda v: isinstance(v, bool))
    pick("pretty_output", lambda v: isinstance(v, bool))
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


# ==========================================
# EMBEDDED ERROR REGISTRY (Codes 1-29)
# ==========================================

E_INVALID_JSON               = 1
E_MISSING_MANDATORY_KEY      = 2
E_INVALID_FORMAT             = 3
E_INVALID_VERSION            = 4
E_INVALID_RECORDS_TYPE       = 5
E_INVALID_FIELDS             = 6
E_INVALID_VALUES             = 7
E_TYPE_MISMATCH              = 8
E_RECORD_LENGTH_MISMATCH     = 9
E_RESERVED_KEY_COLLISION     = 10
E_INVALID_RECORD_TYPE_PARENT = 11
E_NULL_VIOLATION             = 12
E_FILE_NOT_FOUND             = 13
E_PERMISSION_DENIED          = 14
E_ATOMIC_WRITE_FAILED        = 15
E_INVALID_FORMAT_CREATOR     = 16

E_CORE_PARSE_ERROR            = 17
E_CORE_SERIALIZATION_ERROR    = 18
E_CORE_NULL_DOCUMENT          = 19
E_CORE_INVALID_VERSION        = 20
E_CORE_INVALID_OPERATION      = 21
E_CORE_INDEX_OUT_OF_BOUNDS    = 22
E_CORE_FIELD_NOT_FOUND        = 23
E_CORE_TYPE_CONVERSION_FAILED = 24
E_CORE_BACKUP_FAILED          = 25
E_CORE_WRITE_FAILED           = 26
E_CORE_QUERY_FAILED           = 27
E_CORE_ENCRYPTION_FAILED      = 28
E_CORE_DECRYPTION_FAILED      = 29

VALID_VERSIONS = {"104", "104a", "104db"}
VALID_FIELD_TYPES = {"string", "integer", "number", "boolean", "array", "object"}
MANDATORY_KEYS = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")


# ==========================================
# EMBEDDED BEJSON CORE OPERATIONS
# ==========================================

class BEJSONCoreError(Exception):
    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.code = code


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
    p = Path(path).expanduser()
    if not p.exists():
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return bejson_core_sanitize_doc(json.load(f))
    except (OSError, ValueError) as e:
        LOG.error("[BEJSON_CORE] Failed to load %s: %s", p, e)
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


_FIELD_MAP_CACHE: Dict[tuple, Dict[str, int]] = {}


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


def bejson_core_get_field_index(doc: dict, field_name: str) -> int:
    return bejson_core_get_field_map(doc).get(field_name, -1)


def bejson_core_create_104(record_type: str, fields: list, values: list) -> dict:
    return {
        "Format": "BEJSON",
        "Format_Version": "104",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [record_type],
        "Fields": fields,
        "Values": values,
    }


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


def bejson_core_create_104db(record_types: list, fields: list, values: list) -> dict:
    return {
        "Format": "BEJSON",
        "Format_Version": "104db",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": record_types,
        "Fields": fields,
        "Values": values,
    }


def bejson_core_get_record_count(doc: dict) -> int:
    return len(doc.get("Values", []))


def bejson_core_add_record(doc: dict, record: list) -> bool:
    if len(record) != len(doc.get("Fields", [])):
        return False
    doc.setdefault("Values", []).append(record)
    return True


def bejson_core_get_version(doc: dict) -> str:
    return doc.get("Format_Version", "unknown")


def bejson_core_get_stats(doc: dict) -> dict:
    return {
        "record_count": bejson_core_get_record_count(doc),
        "field_count": len(doc.get("Fields", [])),
        "version": bejson_core_get_version(doc),
    }


# ==========================================
# EMBEDDED BEJSON VALIDATOR
# ==========================================

@dataclass
class ValidationResult:
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    current_file: str = ""

    def add_error(self, message: str) -> None:
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def is_valid(self) -> bool:
        return self.valid


class BEJSONValidationError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


def bejson_validator_check_json_syntax(input_data: Union[str, Path, dict], res: ValidationResult, is_file: bool = False) -> dict:
    if is_file:
        p = Path(input_data)
        if not p.exists():
            raise BEJSONValidationError(f"File not found: {input_data}", E_FILE_NOT_FOUND)
        res.current_file = str(p)
        try:
            text = p.read_text(encoding="utf-8")
        except OSError as e:
            raise BEJSONValidationError(f"Cannot read {input_data}: {e}", E_PERMISSION_DENIED)
    else:
        text = input_data
    if isinstance(text, dict):
        return text
    try:
        return bejson_core_sanitize_doc(json.loads(text))
    except ValueError as e:
        raise BEJSONValidationError(f"Invalid JSON: {e}", E_INVALID_JSON)


def bejson_validator_check_mandatory_keys(doc: dict) -> str:
    if not isinstance(doc, dict):
        raise BEJSONValidationError("Document root must be an object", E_INVALID_FORMAT)
    for key in MANDATORY_KEYS:
        if key not in doc:
            raise BEJSONValidationError(f"Missing key: {key}", E_MISSING_MANDATORY_KEY)
    if doc["Format"] != "BEJSON":
        raise BEJSONValidationError("Invalid Format", E_INVALID_FORMAT)
    if doc["Format_Creator"] != "Elton Boehnen":
        raise BEJSONValidationError("Invalid Format_Creator: Must be 'Elton Boehnen'", E_INVALID_FORMAT_CREATOR)
    version = doc.get("Format_Version", "")
    if version not in VALID_VERSIONS:
        raise BEJSONValidationError(f"Invalid version: {version}", E_INVALID_VERSION)
    return version


def bejson_validator_check_records_type(doc: dict, version: str) -> None:
    rt = doc["Records_Type"]
    if not isinstance(rt, list):
        raise BEJSONValidationError("Records_Type must be a list", E_INVALID_RECORDS_TYPE)
    count = len(rt)
    if version in ("104", "104a") and count != 1:
        raise BEJSONValidationError(f"BEJSON {version} must have exactly 1 record type. Found {count}.", E_INVALID_RECORDS_TYPE)
    if version == "104db" and count < 2:
        raise BEJSONValidationError("104db requires 2+ types", E_INVALID_RECORDS_TYPE)


def bejson_validator_check_record_type_parent(doc: dict, version: str) -> bool:
    if version != "104db":
        return True
    fields = doc["Fields"]
    if not fields or fields[0].get("name") != "Record_Type_Parent":
        raise BEJSONValidationError("104db first field must be 'Record_Type_Parent'", E_INVALID_RECORD_TYPE_PARENT)
    valid_types = set(doc["Records_Type"])
    for i, record in enumerate(doc["Values"]):
        if not record:
            continue
        if record[0] not in valid_types:
            raise BEJSONValidationError(f"Invalid Record_Type_Parent '{record[0]}' at row {i}", E_INVALID_RECORD_TYPE_PARENT)
    return True


def bejson_validator_check_fields_structure(doc: dict, version: str) -> int:
    fields = doc["Fields"]
    if not isinstance(fields, list):
        raise BEJSONValidationError("Fields must be a list", E_INVALID_FIELDS)
    seen = set()
    for i, f in enumerate(fields):
        if not isinstance(f, dict):
            raise BEJSONValidationError(f"Field {i} must be an object", E_INVALID_FIELDS)
        fname = f.get("name")
        ftype = f.get("type")
        if not fname or not ftype:
            raise BEJSONValidationError(f"Field {i} missing name or type", E_INVALID_FIELDS)
        if fname in seen:
            raise BEJSONValidationError(f"Duplicate field name '{fname}'", E_INVALID_FIELDS)
        seen.add(fname)
        if ftype not in VALID_FIELD_TYPES:
            raise BEJSONValidationError(f"Field '{fname}' (index {i}) has invalid type '{ftype}'.", E_INVALID_FIELDS)
        if version == "104a" and ftype in ("array", "object"):
            raise BEJSONValidationError(f"104a forbids complex type: {ftype}", E_INVALID_FIELDS)
        if version == "104db" and fname != "Record_Type_Parent" and "Record_Type_Parent" not in f:
            raise BEJSONValidationError(f"Field '{fname}' missing Record_Type_Parent in 104db", E_INVALID_RECORD_TYPE_PARENT)
    return len(fields)


def bejson_validator_check_values(doc: dict, version: str, fields_count: int) -> None:
    fields = doc["Fields"]
    values = doc["Values"]
    if not isinstance(values, list):
        raise BEJSONValidationError("Values must be a list", E_INVALID_VALUES)
    for i, record in enumerate(values):
        if not isinstance(record, list) or len(record) != fields_count:
            raise BEJSONValidationError(f"Length mismatch at row {i}", E_RECORD_LENGTH_MISMATCH)
        for j, val in enumerate(record):
            if val is None:
                continue
            ftype = fields[j].get("type")
            name = fields[j]["name"]
            if ftype == "string" and not isinstance(val, str):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected string", E_TYPE_MISMATCH)
            elif ftype == "integer" and (not isinstance(val, int) or isinstance(val, bool)):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected integer", E_TYPE_MISMATCH)
            elif ftype == "number" and (not isinstance(val, (int, float)) or isinstance(val, bool)):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected number", E_TYPE_MISMATCH)
            elif ftype == "boolean" and not isinstance(val, bool):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected boolean", E_TYPE_MISMATCH)
            elif ftype == "array" and not isinstance(val, list):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected array", E_TYPE_MISMATCH)
            elif ftype == "object" and not isinstance(val, dict):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({name}): expected object", E_TYPE_MISMATCH)


def bejson_validator_check_custom_headers(doc: dict, version: str) -> None:
    mandatory_set = set(MANDATORY_KEYS)
    for key in doc:
        if key in mandatory_set or key == "Parent_Hierarchy":
            continue
        if version in ("104", "104db"):
            raise BEJSONValidationError(f"Custom key '{key}' forbidden in {version}", E_RESERVED_KEY_COLLISION)


def validate_bejson(input_data: Union[str, Path, dict], is_file: bool = False) -> ValidationResult:
    res = ValidationResult()
    try:
        doc = bejson_validator_check_json_syntax(input_data, res, is_file=is_file)
        version = bejson_validator_check_mandatory_keys(doc)
        bejson_validator_check_custom_headers(doc, version)
        bejson_validator_check_records_type(doc, version)
        bejson_validator_check_record_type_parent(doc, version)
        fields_count = bejson_validator_check_fields_structure(doc, version)
        bejson_validator_check_values(doc, version, fields_count)
    except BEJSONValidationError as e:
        res.add_error(str(e))
    except Exception as e:
        res.add_error(f"Unexpected validation error: {e}")
    return res


def bejson_validator_get_report(input_data: Union[str, Path, dict], is_file: bool = False) -> str:
    res = validate_bejson(input_data, is_file=is_file)
    lines = [
        "BEJSON Validation Report",
        f"  File: {res.current_file or '<string>'}",
        f"  Valid: {res.valid}"
    ]
    if res.errors:
        lines.append("  Errors:")
        lines.extend(f"    - {e}" for e in res.errors)
    if res.warnings:
        lines.append("  Warnings:")
        lines.extend(f"    - {w}" for w in res.warnings)
    return "\n".join(lines)


# ==========================================
# ABOUT & CLI ENTRYPOINT
# ==========================================

def about() -> str:
    return (
        f"{C_ACCENT}CLI Standard Tool{C_RESET} V{VERSION} (Release_Version {RELEASE_VERSION})\n"
        f"Relational_ID : {RELATIONAL_ID}\n"
        f"Embedded Core : BEJSON Core + Error Registry (1-29) + BEJSON Validator\n"
        f"Author        : Elton Boehnen\n"
        f"Contact       : boehnenelton2024@gmail.com | boehnenelton2024.pages.dev"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cli_standard_tool",
        description="Standardized Python CLI utility with embedded config, core, and validator.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s V{VERSION} (Release_Version {RELEASE_VERSION})",
        help="Show program version and exit."
    )
    parser.add_argument(
        "--about",
        action="store_true",
        help="Show tool metadata, author crediting, and embedded engine info."
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        default=None,
        help="Path to custom config.json file (default: config/config.json)."
    )
    parser.add_argument(
        "--validate",
        type=str,
        metavar="FILE",
        help="Validate a BEJSON target document using the embedded validator."
    )
    parser.add_argument(
        "--stats",
        type=str,
        metavar="FILE",
        help="Display summary statistics and record count for a BEJSON document."
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    configure_console_logging()

    if args.about:
        LOG.info("\n%s", about())
        return EXIT_OK

    if initialize_config():
        LOG.info("Initialized default configuration at: %s", CONFIG_FILE)

    try:
        config = sanitize_config(load_config(args.config))
    except ConfigError as e:
        LOG.error("%s", e)
        return EXIT_ENV_FAILURE

    level = getattr(logging, str(config["log_level"]).upper(), logging.INFO)
    LOG.handlers[0].setLevel(level)
    attach_file_logging(LOGS_DIR, level)

    if args.validate:
        LOG.info("Validating file: %s", args.validate)
        LOG.info("\n%s", bejson_validator_get_report(args.validate, is_file=True))
        res = validate_bejson(args.validate, is_file=True)
        return EXIT_OK if res.valid else EXIT_SCHEMA_FAILURE

    if args.stats:
        doc = bejson_core_load_file(args.stats)
        if not doc:
            LOG.error("Could not load document: %s", args.stats)
            return EXIT_PATH_FAILURE
        stats = bejson_core_get_stats(doc)
        LOG.info(
            "Document stats for %s -> Version: %s | Fields: %d | Records: %d",
            args.stats, stats["version"], stats["field_count"], stats["record_count"]
        )
        return EXIT_OK

    parser.print_help()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
