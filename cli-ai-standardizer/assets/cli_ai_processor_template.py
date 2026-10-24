#!/usr/bin/env python3
"""
Name:            CLI AI Processor Template
File:            cli_ai_processor_template.py
Family:          CLI_AI
Description:     Standardized standalone CLI AI file-processing template with stdlib
                 REST API dispatch (Gemini REST, OpenAI-compatible REST, Ollama Local),
                 round-robin key rotation with backoff retry, self-bootstrapping
                 directories, embedded BEJSON 104/104a Core & Validator, single-instance
                 locking, and source-fingerprinted resumable state tracking.
Version:         100
Release_Version: 300
Date Created:    2026-10-17
Author:          Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Format_Creator:  Elton Boehnen
RELATIONAL_ID:   8f4e2c91-5a7b-4d3e-9c1f-2b6a8e4d7f30
"""

from __future__ import annotations

import sys

# ── 1. Python 3.10+ Runtime Guard ────────────────────────────────────────────
if sys.version_info < (3, 10):
    sys.stderr.write("ERROR: Python 3.10 or newer is required.\n")
    sys.exit(20)

import argparse
import base64
import copy
import errno
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import re
import shutil
import socket
import time
from typing import Any, Dict, Final, List, Optional, Sequence, Tuple, TypedDict
import urllib.error
import urllib.request
import uuid

# ── 2. Deterministic Exit-Code Registry ──────────────────────────────────────
EXIT_OK: Final[int]              = 0
EXIT_PARTIAL_FAILURE: Final[int] = 1    # one or more assets failed; rerun resumes
EXIT_PATH_FAILURE: Final[int]    = 10   # directory / path problem
EXIT_ENV_FAILURE: Final[int]     = 20   # configuration / environment / API key problem
EXIT_SCHEMA_FAILURE: Final[int]  = 30   # BEJSON validation / checksum failure
EXIT_DEP_MISSING: Final[int]     = 40   # external binary missing
EXIT_BUSY: Final[int]            = 50   # another instance holds the lock
EXIT_INTERRUPTED: Final[int]     = 130  # SIGINT / KeyboardInterrupt

# ── 3. Metadata & Script-Relative Portability ────────────────────────────────
TOOL_NAME: Final[str]        = "cli_ai_processor"
PRODUCT_TITLE: Final[str]    = "CLI AI REST File Processor"
VERSION: Final[int]          = 100
PACKAGE_VERSION: Final[int]  = 100
DATE_CREATED: Final[str]     = "2026-10-17"
RELATIONAL_ID: Final[str]    = "8f4e2c91-5a7b-4d3e-9c1f-2b6a8e4d7f30"

SCRIPT_PATH: Final[Path]     = Path(__file__).resolve().parent
CONFIG_DIR: Final[Path]      = SCRIPT_PATH / "config"
ASSETS_DIR: Final[Path]      = SCRIPT_PATH / "assets"
OUT_DIR: Final[Path]         = SCRIPT_PATH / "out"
LOGS_DIR: Final[Path]        = SCRIPT_PATH / "logs"

CONFIG_FILE: Final[Path]     = CONFIG_DIR / "config.json"
STATE_FILE: Final[Path]      = CONFIG_DIR / "job_state.104a.bejson"
KEYS_FILE: Final[Path]       = CONFIG_DIR / "ai_keys.104a.bejson"
CALL_LOG_FILE: Final[Path]   = LOGS_DIR / "ai_call_log.104a.bejson"
LOCK_FILE: Final[Path]       = CONFIG_DIR / "processor.lock"

SUPPORTED_EXTS: Final[Tuple[str, ...]] = (
    ".txt", ".md", ".json", ".bejson", ".py", ".js", ".ts", ".sh",
    ".html", ".css", ".xml", ".yaml", ".yml", ".csv",
)

# ── 4. Provider REST Endpoints & Env Prefix Catalog ──────────────────────────
PROVIDER_SPECS: Final[Dict[str, Dict[str, Any]]] = {
    "geminirest": {
        "wire": "gemini_rest",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models",
        "default_model": "gemini-3.6-flash",
        "env_var": "GEMINI_API_KEYS",
        "env_prefix": "GEMINI_KEY",
        "single_env": "GEMINI_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "groq": {
        "wire": "openai_compat",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "openai/gpt-oss-120b",
        "env_var": "GROQ_API_KEYS",
        "env_prefix": "GROQ_KEY",
        "single_env": "GROQ_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "openrouter": {
        "wire": "openai_compat",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "qwen/qwen3-coder:free",
        "env_var": "OPENROUTER_API_KEYS",
        "env_prefix": "OPENROUTER_KEY",
        "single_env": "OPENROUTER_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "tokenrouter": {
        "wire": "openai_compat",
        "base_url": "https://api.tokenrouter.com/v1",
        "default_model": "z-ai/glm-5.3-free",
        "env_var": "TOKENROUTER_API_KEYS",
        "env_prefix": "TOKENROUTER_KEY",
        "single_env": "TOKENROUTER_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "grok": {
        "wire": "openai_compat",
        "base_url": "https://api.x.ai/v1",
        "default_model": "grok-3-mini",
        "env_var": "XAI_API_KEYS",
        "env_prefix": "GROK_KEY",
        "single_env": "XAI_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "huggingface": {
        "wire": "openai_compat",
        "base_url": "https://router.huggingface.co/v1",
        "default_model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "env_var": "HUGGINGFACE_API_KEYS",
        "env_prefix": "HUGGINGFACE_MM_KEY",
        "single_env": "HF_TOKEN",
        "max_slots": 30,
        "requires_key": True,
    },
    "openai": {
        "wire": "openai_compat",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "env_var": "OPENAI_API_KEYS",
        "env_prefix": "OPENAI_KEY",
        "single_env": "OPENAI_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "ollama": {
        "wire": "openai_compat",
        "base_url": "https://ollama.com/v1",
        "default_model": "qwen2.5-coder:7b",
        "env_var": "OLLAMA_API_KEYS",
        "env_prefix": "OLLAMA_KEY",
        "single_env": "OLLAMA_API_KEY",
        "max_slots": 30,
        "requires_key": True,
    },
    "ollamalocal": {
        "wire": "ollama_local",
        "base_url": "http://127.0.0.1:11434",
        "default_model": "qwen2.5-coder:1.5b",
        "env_var": "",
        "env_prefix": "",
        "single_env": "",
        "max_slots": 0,
        "requires_key": False,
    },
}

DEFAULT_SECURE_ENV_PATHS: Final[Tuple[str, ...]] = (
    "/storage/emulated/0/.env/secure/secureenv_file.json",
    "/storage/emulated/0/.env/secure/secureenv_file.py",
)

DEFAULT_CONFIG: Final[Dict[str, Any]] = {
    "provider": "geminirest",
    "model_id": "gemini-3.6-flash",
    "system_instruction": (
        "You are a deterministic file-processing AI engine. Process the supplied input "
        "file according to the user prompt and emit structured output."
    ),
    "prompt_template": (
        "Process the following file ({filename}) and return the transformed output:\n\n"
        "{content}"
    ),
    "xml_output_tag": "file",
    "enforce_xml_output": True,
    "secure_env_path": "/storage/emulated/0/.env/secure/secureenv_file.json",
    "assets_subdir": "assets",
    "output_subdir": "out",
    "source_handling": "copy",  # "copy" | "move" | "keep"
    "rest_timeout_seconds": 120,
    "retry_attempts": 4,
    "retry_backoff_seconds": [5, 15, 30],
    "temperature": 0.2,
    "max_output_tokens": 8192,
    "log_ai_calls": True,
}

# ── 5. Structured Console & Rotating File Logging ────────────────────────────
class _ConsoleFormatter(logging.Formatter):
    """Applies Elton Boehnen's #DE2626 red accent and #FFEEDD cream palette on TTY."""

    RED_ACCENT = "\033[38;2;222;38;38m"
    CREAM_INFO = "\033[38;2;255;238;221m"
    RESET      = "\033[0m"

    def __init__(self, use_color: bool = True) -> None:
        super().__init__("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if not self.use_color:
            return msg
        if record.levelno >= logging.WARNING:
            return f"{self.RED_ACCENT}{msg}{self.RESET}"
        return f"{self.CREAM_INFO}{msg}{self.RESET}"


def setup_console_logging(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger(TOOL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        use_color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG if verbose else logging.INFO)
        sh.setFormatter(_ConsoleFormatter(use_color=use_color))
        logger.addHandler(sh)
    return logger


def attach_file_logging(logger: logging.Logger, logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{TOOL_NAME}.log"
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler):
            return
    fh = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(fh)


LOG = setup_console_logging()


# ── 6. Custom Exceptions ─────────────────────────────────────────────────────
class ConfigError(Exception):
    """Raised on configuration or environment validation failure (EXIT_ENV_FAILURE)."""


class PathSecurityError(Exception):
    """Raised on path traversal or directory initialization failure (EXIT_PATH_FAILURE)."""


class SchemaValidationError(Exception):
    """Raised when BEJSON document validation fails (EXIT_SCHEMA_FAILURE)."""


class BusyLockError(Exception):
    """Raised when another instance holds the processor lock (EXIT_BUSY)."""


# ── 7. Embedded BEJSON 104/104a Core & Validator Engine ──────────────────────
VALID_BEJSON_TYPES: Final[frozenset[str]] = frozenset(
    {"string", "integer", "number", "boolean", "array", "object"}
)


def bejson_core_sanitize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Boundary-layer sanitization: strips edge whitespace from keys and field names,
    and performs O(1) first/last character checks on string cell values so large
    strings are never linearly scanned or copied when already clean.
    """
    if not isinstance(doc, dict):
        return doc
    cleaned: Dict[str, Any] = {}
    for k, v in doc.items():
        ck = k.strip() if isinstance(k, str) and k and (k[0].isspace() or k[-1].isspace()) else k
        cleaned[ck] = v

    fields = cleaned.get("Fields")
    if isinstance(fields, list):
        for fld in fields:
            if isinstance(fld, dict):
                for fk, fv in list(fld.items()):
                    if isinstance(fv, str) and fv and (fv[0].isspace() or fv[-1].isspace()):
                        fld[fk] = fv.strip()

    values = cleaned.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for idx, cell in enumerate(row):
                    if isinstance(cell, str) and cell and (cell[0].isspace() or cell[-1].isspace()):
                        row[idx] = cell.strip()
    return cleaned


def bejson_validator_check_fields_structure(doc: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates BEJSON 104/104a structure, rejecting duplicate field names and invalid types."""
    errors: List[str] = []
    if not isinstance(doc, dict):
        return False, ["Document root must be a JSON object."]
    if doc.get("Format") != "BEJSON":
        errors.append(f"Invalid Format: {doc.get('Format')!r} (expected 'BEJSON').")
    if doc.get("Format_Version") not in ("104", "104a", "104db"):
        errors.append(f"Unsupported Format_Version: {doc.get('Format_Version')!r}.")
    if doc.get("Format_Creator") != "Elton Boehnen":
        errors.append("Format_Creator must be 'Elton Boehnen'.")

    fields = doc.get("Fields")
    if not isinstance(fields, list) or not fields:
        errors.append("Fields must be a non-empty list.")
        return False, errors

    seen_names: set[str] = set()
    for i, fld in enumerate(fields):
        if not isinstance(fld, dict):
            errors.append(f"Field[{i}] must be a dict.")
            continue
        name = fld.get("name")
        ftype = fld.get("type")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"Field[{i}] has missing or empty 'name'.")
        elif name in seen_names:
            errors.append(f"Duplicate field name {name!r} at index {i}.")
        else:
            seen_names.add(name)
        if ftype not in VALID_BEJSON_TYPES:
            errors.append(f"Field {name!r} has invalid type {ftype!r}; allowed: {sorted(VALID_BEJSON_TYPES)}.")

    values = doc.get("Values")
    if not isinstance(values, list):
        errors.append("Values must be a list.")
    else:
        expected_len = len(fields)
        for r_idx, row in enumerate(values):
            if not isinstance(row, list):
                errors.append(f"Row {r_idx} is not a list.")
            elif len(row) != expected_len:
                errors.append(f"Row {r_idx} length {len(row)} != Fields length {expected_len}.")

    return len(errors) == 0, errors


def bejson_core_get_field_map(doc: Dict[str, Any]) -> Dict[str, int]:
    """Returns O(1) cached mapping of field_name -> column_index."""
    cached = doc.get("_bejson_field_map")
    fields = doc.get("Fields", [])
    if isinstance(cached, dict) and len(cached) == len(fields):
        return cached
    fmap = {f["name"]: idx for idx, f in enumerate(fields) if isinstance(f, dict) and "name" in f}
    doc["_bejson_field_map"] = fmap
    return fmap


def write_json_atomic(target_path: Path, payload: Dict[str, Any]) -> None:
    """Writes JSON/BEJSON atomically via temp file + fsync + os.replace()."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    export_doc = {k: v for k, v in payload.items() if k != "_bejson_field_map"}
    tmp_path = target_path.parent / f".bejson_{target_path.name}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
    try:
        raw = json.dumps(export_doc, indent=2, ensure_ascii=False) + "\n"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target_path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def bejson_core_load_file(file_path: Path) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return bejson_core_sanitize_doc(data)


# ── 8. Secure Env Loader & Round-Robin Key Registry ──────────────────────────
_ENV_FILLED_ONCE: bool = False


def source_env_fill(custom_env_path: Optional[str] = None) -> int:
    """
    Non-overwriting environment loader modeled on lib_bejson_Core_bejson_env.source_env_fill().
    Loads keys from BEJSON 104/104a, plain JSON, or KEY=VALUE/.py files without exec().
    Returns count of newly populated environment variables.
    """
    global _ENV_FILLED_ONCE
    candidates: List[Path] = []
    if custom_env_path:
        candidates.append(Path(custom_env_path).expanduser())
    for p in DEFAULT_SECURE_ENV_PATHS:
        path_obj = Path(p)
        if path_obj not in candidates:
            candidates.append(path_obj)

    added = 0
    for cand in candidates:
        if not cand.is_file():
            continue
        try:
            text = cand.read_text(encoding="utf-8", errors="replace").strip()
            if text.startswith("{"):
                data = json.loads(text)
                if data.get("Format") == "BEJSON" and "Fields" in data and "Values" in data:
                    fmap = bejson_core_get_field_map(data)
                    k_idx = fmap.get("key_name", fmap.get("name", fmap.get("setting_name", 0)))
                    v_idx = fmap.get("key_value", fmap.get("value", fmap.get("setting_value", 1)))
                    for row in data.get("Values", []):
                        if isinstance(row, list) and len(row) > max(k_idx, v_idx):
                            k, v = str(row[k_idx] or "").strip(), str(row[v_idx] or "").strip()
                            if k and v and k not in os.environ:
                                os.environ[k] = v
                                added += 1
                else:
                    for k, v in data.items():
                        if isinstance(k, str) and isinstance(v, (str, int, float)) and k not in os.environ:
                            val_s = str(v).strip()
                            if val_s:
                                os.environ[k] = val_s
                                added += 1
            else:
                # Parse KEY = "VALUE" lines safely without exec()
                for line in text.splitlines():
                    line_s = line.strip()
                    if not line_s or line_s.startswith("#"):
                        continue
                    if line_s.startswith("export "):
                        line_s = line_s[7:].strip()
                    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$", line_s)
                    if m:
                        k, raw_v = m.group(1), m.group(2).strip()
                        if (raw_v.startswith('"') and raw_v.endswith('"')) or (
                            raw_v.startswith("'") and raw_v.endswith("'")
                        ):
                            raw_v = raw_v[1:-1]
                        if k and raw_v and k not in os.environ:
                            os.environ[k] = raw_v
                            added += 1
        except Exception as exc:
            LOG.debug("source_env_fill skipped %s: %s", cand, exc)
    _ENV_FILLED_ONCE = True
    return added


class RoundRobinKeyRegistry:
    """
    Loads API keys from environment variables (single var, comma list, and numbered slots
    PROVIDER_KEY_1..N checked independently) plus BEJSON 104a fallback store.
    Maintains a persistent rotation cursor so get_next_key() rotates across calls and retries.
    """

    PLACEHOLDER_MARKERS: Tuple[str, ...] = ("YOUR_", "KEY_HERE", "_KEY_HERE", "INSERT_")

    def __init__(self, provider: str, keys_file: Path, secure_env_path: Optional[str] = None) -> None:
        self.provider = provider.lower()
        self.keys_file = keys_file
        self.secure_env_path = secure_env_path
        self.keys: List[str] = []
        self._idx: int = 0
        self.load()

    def _is_valid_key(self, val: str) -> bool:
        s = (val or "").strip()
        if not s:
            return False
        return not any(marker in s.upper() for marker in self.PLACEHOLDER_MARKERS)

    def _ensure_keys_file(self) -> None:
        if not self.keys_file.exists():
            default_doc = {
                "Format": "BEJSON",
                "Format_Version": "104a",
                "Format_Creator": "Elton Boehnen",
                "Schema_Name": "AIKeyRegistry",
                "Records_Type": ["ApiKey"],
                "Fields": [
                    {"name": "provider", "type": "string"},
                    {"name": "key_slot", "type": "integer"},
                    {"name": "key", "type": "string"},
                ],
                "Values": [
                    ["geminirest", 1, "YOUR_GEMINI_KEY_HERE"],
                ],
            }
            write_json_atomic(self.keys_file, default_doc)

    def load(self) -> None:
        self.keys = []
        source_env_fill(self.secure_env_path)
        spec = PROVIDER_SPECS.get(self.provider, PROVIDER_SPECS["geminirest"])

        # 1. Single env var (e.g. GEMINI_API_KEY)
        single_env = spec.get("single_env", "")
        if single_env:
            val = os.environ.get(single_env, "").strip()
            if self._is_valid_key(val) and val not in self.keys:
                self.keys.append(val)

        # 2. Comma-separated env var (e.g. GEMINI_API_KEYS)
        env_var = spec.get("env_var", "")
        if env_var:
            for item in os.environ.get(env_var, "").split(","):
                val = item.strip()
                if self._is_valid_key(val) and val not in self.keys:
                    self.keys.append(val)

        # 3. Numbered slots (e.g. GEMINI_KEY_1..30) — checked independently!
        prefix = spec.get("env_prefix", "")
        max_slots = int(spec.get("max_slots", 30))
        if prefix and max_slots > 0:
            for slot in range(1, max_slots + 1):
                val = os.environ.get(f"{prefix}_{slot}", "").strip()
                if self._is_valid_key(val) and val not in self.keys:
                    self.keys.append(val)

        # 4. Fallback BEJSON 104a file
        self._ensure_keys_file()
        try:
            doc = bejson_core_load_file(self.keys_file)
            fmap = bejson_core_get_field_map(doc)
            p_idx = fmap.get("provider")
            k_idx = fmap.get("key")
            if k_idx is not None:
                for row in doc.get("Values", []):
                    if p_idx is not None and str(row[p_idx]).lower() not in (self.provider, "*"):
                        continue
                    val = str(row[k_idx] or "").strip()
                    if self._is_valid_key(val) and val not in self.keys:
                        self.keys.append(val)
        except Exception as exc:
            LOG.warning("Failed reading fallback keys file %s: %s", self.keys_file, exc)

    def get_next_key(self) -> Tuple[Optional[str], int]:
        """Returns (api_key, 1-based_slot_index) and advances the rotation cursor."""
        if not self.keys:
            return None, 0
        slot_idx = (self._idx % len(self.keys)) + 1
        key = self.keys[slot_idx - 1]
        self._idx += 1
        return key, slot_idx


_KEY_REGISTRIES: Dict[str, RoundRobinKeyRegistry] = {}


def get_key_registry(provider: str, keys_file: Path, secure_env_path: Optional[str] = None) -> RoundRobinKeyRegistry:
    """Singleton per provider so key rotation persists across calls and retries."""
    prov = provider.lower()
    if prov not in _KEY_REGISTRIES:
        _KEY_REGISTRIES[prov] = RoundRobinKeyRegistry(prov, keys_file, secure_env_path)
    return _KEY_REGISTRIES[prov]


# ── 9. Unified AIResponse & Stdlib REST API Dispatcher ───────────────────────
class AIResponse(TypedDict):
    success: bool
    content: str
    thought: str
    error: Optional[str]
    provider: str
    model_id: str
    key_slot: int
    attempts: int
    raw: Any


RETRYABLE_HTTP_CODES: Final[Tuple[int, ...]] = (429, 500, 502, 503, 504)


def _call_gemini_rest_once(
    base_url: str,
    model_id: str,
    api_key: str,
    user_input: str,
    system_instruction: Optional[str],
    timeout: int,
    temperature: float,
    max_output_tokens: int,
    inline_media: Optional[Tuple[str, bytes]] = None,
) -> Tuple[str, str, Any]:
    """Executes one HTTP POST against Gemini v1beta generateContent REST API using stdlib urllib."""
    url = f"{base_url.rstrip('/')}/{model_id}:generateContent"
    parts: List[Dict[str, Any]] = []
    if inline_media is not None:
        mime_type, raw_bytes = inline_media
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(raw_bytes).decode("ascii"),
            }
        })
    parts.append({"text": user_input})

    payload: Dict[str, Any] = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }
    if system_instruction:
        payload["system_instruction"] = {"parts": [{"text": system_instruction}]}

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    candidates = data.get("candidates") or []
    if not candidates:
        reason = (data.get("promptFeedback") or {}).get("blockReason") or "empty candidates"
        raise ValueError(f"Gemini REST returned no candidates ({reason})")

    content_parts = (candidates[0].get("content") or {}).get("parts") or []
    text_chunks: List[str] = []
    thought_chunks: List[str] = []
    for p in content_parts:
        if not isinstance(p, dict):
            continue
        if p.get("thought") is True:
            thought_chunks.append(str(p.get("text", "")))
        elif "text" in p:
            text_chunks.append(str(p.get("text", "")))

    return "".join(text_chunks), "".join(thought_chunks), data


def _call_openai_compat_once(
    base_url: str,
    model_id: str,
    api_key: str,
    user_input: str,
    system_instruction: Optional[str],
    timeout: int,
    temperature: float,
    max_output_tokens: int,
) -> Tuple[str, str, Any]:
    """Executes one HTTP POST against an OpenAI-compatible /chat/completions REST endpoint."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    messages: List[Dict[str, str]] = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": user_input})

    payload: Dict[str, Any] = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_output_tokens,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": f"{TOOL_NAME}/{VERSION}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    choices = data.get("choices") or []
    if not choices:
        raise ValueError("OpenAI-compatible REST endpoint returned empty choices.")
    msg = choices[0].get("message") or {}
    content = str(msg.get("content") or "")
    thought = str(msg.get("reasoning_content") or msg.get("reasoning") or "")
    return content, thought, data


def _call_ollama_local_once(
    base_url: str,
    model_id: str,
    user_input: str,
    system_instruction: Optional[str],
    timeout: int,
    temperature: float,
) -> Tuple[str, str, Any]:
    """Executes one HTTP POST against a local Ollama server (/api/chat, stream=False)."""
    url = f"{base_url.rstrip('/')}/api/chat"
    messages: List[Dict[str, str]] = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": user_input})

    payload: Dict[str, Any] = {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    msg = data.get("message") or {}
    return str(msg.get("content") or ""), "", data


def rest_ai_dispatch(
    provider: str,
    user_input: str,
    *,
    model_id: Optional[str] = None,
    system_instruction: Optional[str] = None,
    keys_file: Path = KEYS_FILE,
    secure_env_path: Optional[str] = None,
    timeout: int = 120,
    retry_attempts: int = 4,
    retry_backoff: Sequence[int] = (5, 15, 30),
    temperature: float = 0.2,
    max_output_tokens: int = 8192,
    inline_media: Optional[Tuple[str, bytes]] = None,
) -> AIResponse:
    """
    Provider-agnostic stdlib REST dispatcher with automatic round-robin key rotation
    and exponential backoff across HTTP 429/5xx and transient network/timeout errors.
    """
    prov = provider.lower().strip()
    if prov not in PROVIDER_SPECS:
        return AIResponse(
            success=False,
            content="",
            thought="",
            error=f"Unknown provider {provider!r}. Supported: {sorted(PROVIDER_SPECS)}",
            provider=prov,
            model_id=model_id or "",
            key_slot=0,
            attempts=0,
            raw=None,
        )

    spec = PROVIDER_SPECS[prov]
    target_model = model_id or str(spec["default_model"])
    wire = spec["wire"]
    base_url = str(spec["base_url"])
    requires_key = bool(spec["requires_key"])

    key_reg: Optional[RoundRobinKeyRegistry] = None
    if requires_key:
        key_reg = get_key_registry(prov, keys_file, secure_env_path)
        if not key_reg.keys:
            return AIResponse(
                success=False,
                content="",
                thought="",
                error=f"No valid API keys loaded for provider {prov!r}.",
                provider=prov,
                model_id=target_model,
                key_slot=0,
                attempts=0,
                raw=None,
            )

    max_tries = max(1, int(retry_attempts))
    last_err = ""
    last_slot = 0

    for attempt in range(1, max_tries + 1):
        api_key, slot = (key_reg.get_next_key() if key_reg else ("", 0))
        last_slot = slot
        total_keys = len(key_reg.keys) if key_reg else 0
        LOG.info(
            "[REST Dispatch] provider=%s model=%s key_slot=%d/%d attempt=%d/%d",
            prov, target_model, slot, total_keys, attempt, max_tries,
        )

        retryable = False
        try:
            if wire == "gemini_rest":
                content, thought, raw = _call_gemini_rest_once(
                    base_url, target_model, api_key or "", user_input,
                    system_instruction, timeout, temperature, max_output_tokens,
                    inline_media=inline_media,
                )
            elif wire == "openai_compat":
                content, thought, raw = _call_openai_compat_once(
                    base_url, target_model, api_key or "", user_input,
                    system_instruction, timeout, temperature, max_output_tokens,
                )
            else:
                content, thought, raw = _call_ollama_local_once(
                    base_url, target_model, user_input,
                    system_instruction, timeout, temperature,
                )
            return AIResponse(
                success=True,
                content=content,
                thought=thought,
                error=None,
                provider=prov,
                model_id=target_model,
                key_slot=slot,
                attempts=attempt,
                raw=raw,
            )
        except urllib.error.HTTPError as http_err:
            detail = ""
            try:
                detail = http_err.read().decode("utf-8", errors="replace")[:400]
            except Exception:
                pass
            last_err = f"HTTP {http_err.code} {http_err.reason}: {detail}"
            # Rotate and retry on 429/5xx, or on 401/403 if multiple keys exist
            retryable = (http_err.code in RETRYABLE_HTTP_CODES) or (
                http_err.code in (401, 403) and total_keys > 1
            )
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as net_err:
            last_err = f"Network/Timeout error: {net_err}"
            retryable = True
        except Exception as exc:
            last_err = f"Generation error: {exc}"
            retryable = False

        LOG.warning(
            "[REST Dispatch] Attempt %d/%d failed (%s): %s",
            attempt, max_tries, "retryable" if retryable else "fatal", last_err[:200],
        )
        if not retryable or attempt >= max_tries:
            break
        wait_s = retry_backoff[min(attempt - 1, len(retry_backoff) - 1)] if retry_backoff else 5
        time.sleep(wait_s)

    return AIResponse(
        success=False,
        content="",
        thought="",
        error=last_err or "Unknown REST dispatch failure",
        provider=prov,
        model_id=target_model,
        key_slot=last_slot,
        attempts=max_tries,
        raw=None,
    )


def append_ai_call_log(call_log_path: Path, provider: str, model_id: str, prompt_text: str, response_text: str) -> None:
    """Appends a record to logs/ai_call_log.104a.bejson using O(1) field map + atomic write."""
    fields = [
        {"name": "timestamp", "type": "string"},
        {"name": "service", "type": "string"},
        {"name": "model_id", "type": "string"},
        {"name": "message", "type": "string"},
        {"name": "response", "type": "string"},
        {"name": "uuid", "type": "string"},
    ]
    if call_log_path.exists():
        try:
            doc = bejson_core_load_file(call_log_path)
        except Exception:
            doc = {
                "Format": "BEJSON",
                "Format_Version": "104a",
                "Format_Creator": "Elton Boehnen",
                "Schema_Name": "AICallLog",
                "Records_Type": ["CallLogEntry"],
                "Fields": fields,
                "Values": [],
            }
    else:
        doc = {
            "Format": "BEJSON",
            "Format_Version": "104a",
            "Format_Creator": "Elton Boehnen",
            "Schema_Name": "AICallLog",
            "Records_Type": ["CallLogEntry"],
            "Fields": fields,
            "Values": [],
        }

    fmap = bejson_core_get_field_map(doc)
    row: List[Any] = [None] * len(doc["Fields"])
    row[fmap["timestamp"]] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    row[fmap["service"]] = provider
    row[fmap["model_id"]] = model_id
    row[fmap["message"]] = prompt_text[:4000]
    row[fmap["response"]] = response_text[:8000]
    row[fmap["uuid"]] = str(uuid.uuid4())
    doc["Values"].append(row)
    write_json_atomic(call_log_path, doc)


# ── 10. XML Command Instruction & Extraction Helpers ─────────────────────────
def build_xml_output_instruction(tag_name: str = "file") -> str:
    """Builds system/prompt instruction telling the AI to emit files inside XML command tags."""
    clean_tag = re.sub(r"[^A-Za-z0-9_-]", "", tag_name) or "file"
    return (
        f"\n\n[XML_OUTPUT_MANDATE]\n"
        f"Emit every output file inside a <{clean_tag} path=\"relative_filename.ext\">..."
        f"</{clean_tag}> XML command block. You may emit one or more <{clean_tag}> blocks. "
        f"Do not wrap the XML tags in markdown code fences inside the file body.\n"
        f"Example:\n"
        f"<{clean_tag} path=\"output.txt\">\n"
        f"Processed content here\n"
        f"</{clean_tag}>\n"
    )


def parse_xml_file_commands(raw_text: str, tag_name: str = "file") -> List[Tuple[str, str]]:
    """
    Extracts (<tag path="..."></tag>) blocks from AI output.
    Returns list of (sanitized_relative_path, file_content).
    Falls back to single ("output.txt", raw_text) if no XML tags are present.
    """
    clean_tag = re.sub(r"[^A-Za-z0-9_-]", "", tag_name) or "file"
    pattern = re.compile(
        rf"<{re.escape(clean_tag)}(?:\s+[^>]*?(?:path|name|filename)\s*=\s*['\"]([^'\"]+)['\"][^>]*)?>\s*(.*?)\s*</{re.escape(clean_tag)}>",
        re.DOTALL | re.IGNORECASE,
    )
    results: List[Tuple[str, str]] = []
    for idx, match in enumerate(pattern.finditer(raw_text or ""), 1):
        raw_path = (match.group(1) or f"output_{idx}.txt").strip()
        body = match.group(2)
        # Strip accidental outer markdown code fence inside XML tag if model added one
        fence = re.match(r"^```[A-Za-z0-9_-]*\n(.*)\n```$", body.strip(), re.DOTALL)
        if fence:
            body = fence.group(1)
        safe_parts = [p for p in Path(raw_path).parts if p not in ("", ".", "..", "/", "\\")]
        safe_rel = "/".join(safe_parts) if safe_parts else f"output_{idx}.txt"
        results.append((safe_rel, body))
    return results


# ── 11. Configuration Bootstrapping & Validation ─────────────────────────────
def _validate_subfolder_name(value: Any, default: str, setting_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        LOG.warning("Invalid %s=%r; falling back to %r.", setting_name, value, default)
        return default
    cleaned = value.strip()
    if "/" in cleaned or "\\" in cleaned or ".." in cleaned or cleaned.startswith("."):
        LOG.warning("Unsafe path characters in %s=%r; falling back to %r.", setting_name, value, default)
        return default
    return cleaned


def sanitize_config(raw_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Type-checks and range-validates every configuration parameter."""
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    if not isinstance(raw_cfg, dict):
        LOG.warning("Configuration root is not a JSON object; using defaults.")
        return cfg

    prov = str(raw_cfg.get("provider", cfg["provider"])).lower().strip()
    if prov in PROVIDER_SPECS:
        cfg["provider"] = prov
    else:
        LOG.warning("Unknown provider %r in config; falling back to %r.", prov, cfg["provider"])

    model_id = raw_cfg.get("model_id")
    if isinstance(model_id, str) and model_id.strip():
        cfg["model_id"] = model_id.strip()
    else:
        cfg["model_id"] = PROVIDER_SPECS[cfg["provider"]]["default_model"]

    for str_key in ("system_instruction", "prompt_template", "xml_output_tag", "secure_env_path"):
        val = raw_cfg.get(str_key)
        if isinstance(val, str) and val.strip():
            cfg[str_key] = val.strip()

    for bool_key in ("enforce_xml_output", "log_ai_calls"):
        val = raw_cfg.get(bool_key)
        if isinstance(val, bool):
            cfg[bool_key] = val

    cfg["assets_subdir"] = _validate_subfolder_name(raw_cfg.get("assets_subdir"), "assets", "assets_subdir")
    cfg["output_subdir"] = _validate_subfolder_name(raw_cfg.get("output_subdir"), "out", "output_subdir")

    handling = str(raw_cfg.get("source_handling", cfg["source_handling"])).lower().strip()
    if handling in ("copy", "move", "keep"):
        cfg["source_handling"] = handling
    else:
        LOG.warning("Invalid source_handling=%r; falling back to 'copy'.", handling)

    timeout = raw_cfg.get("rest_timeout_seconds")
    if isinstance(timeout, int) and 5 <= timeout <= 1800:
        cfg["rest_timeout_seconds"] = timeout

    retries = raw_cfg.get("retry_attempts")
    if isinstance(retries, int) and 1 <= retries <= 10:
        cfg["retry_attempts"] = retries

    backoff = raw_cfg.get("retry_backoff_seconds")
    if isinstance(backoff, list) and all(isinstance(x, int) and 0 <= x <= 300 for x in backoff) and backoff:
        cfg["retry_backoff_seconds"] = backoff

    temp = raw_cfg.get("temperature")
    if isinstance(temp, (int, float)) and 0.0 <= float(temp) <= 2.0:
        cfg["temperature"] = float(temp)

    max_tok = raw_cfg.get("max_output_tokens")
    if isinstance(max_tok, int) and 64 <= max_tok <= 131072:
        cfg["max_output_tokens"] = max_tok

    return cfg


def initialize_directories() -> bool:
    """
    Atomically extracts DEFAULT_CONFIG into config/config.json on first run
    and initializes config/, assets/, out/, and logs/.
    Returns True if this invocation was the first-run bootstrap.
    """
    first_run = not CONFIG_FILE.exists()
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        if first_run:
            write_json_atomic(CONFIG_FILE, DEFAULT_CONFIG)
            LOG.info("Initialized default configuration at %s", rel_to_script(CONFIG_FILE))
    except OSError as exc:
        raise PathSecurityError(f"Failed initializing directories: {exc}") from exc
    return first_run


def load_config(explicit_config_path: Optional[str] = None) -> Dict[str, Any]:
    """Loads and validates configuration. Fails fast if explicit -c/--config is missing or corrupt."""
    target = Path(explicit_config_path).expanduser().resolve() if explicit_config_path else CONFIG_FILE
    if explicit_config_path and not target.is_file():
        raise ConfigError(f"Explicit configuration file not found: {target}")

    if not target.exists():
        return copy.deepcopy(DEFAULT_CONFIG)

    try:
        with open(target, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    except Exception as exc:
        if explicit_config_path:
            raise ConfigError(f"Malformed explicit configuration file {target}: {exc}") from exc
        LOG.warning("Malformed %s (%s); falling back to defaults.", target, exc)
        return copy.deepcopy(DEFAULT_CONFIG)

    return sanitize_config(user_data)


# ── 12. Single-Instance Lock & Stale Temp Cleanup ────────────────────────────
class InstanceLock:
    """PID-verified single-instance lock using os.O_CREAT | os.O_EXCL | os.O_WRONLY."""

    def __init__(self, lock_path: Path) -> None:
        self.lock_path = lock_path
        self._fd: Optional[int] = None

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
            return True
        except OSError as exc:
            return exc.errno == errno.EPERM

    def acquire(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                self._fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                os.write(self._fd, f"{os.getpid()}\n".encode("ascii"))
                os.fsync(self._fd)
                return
            except FileExistsError:
                try:
                    raw = self.lock_path.read_text(encoding="utf-8").strip()
                    existing_pid = int(raw.splitlines()[0])
                except Exception:
                    existing_pid = -1
                if self._pid_alive(existing_pid):
                    raise BusyLockError(f"Another instance (PID {existing_pid}) holds lock {self.lock_path}")
                LOG.warning("Recovering stale lock file from dead PID %s", existing_pid)
                try:
                    self.lock_path.unlink()
                except OSError as exc:
                    raise BusyLockError(f"Cannot remove stale lock {self.lock_path}: {exc}") from exc
        raise BusyLockError(f"Could not acquire lock {self.lock_path}")

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = None
        try:
            if self.lock_path.exists():
                self.lock_path.unlink()
        except OSError:
            pass

    def __enter__(self) -> "InstanceLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


def cleanup_stale_temps(*directories: Path) -> int:
    """Removes leftover .tmp_* and .bejson_*.tmp files while holding InstanceLock."""
    removed = 0
    for d in directories:
        if not d.exists():
            continue
        for root, _, files in os.walk(d):
            for fname in files:
                if fname.startswith(".tmp_") or (fname.startswith(".bejson_") and fname.endswith(".tmp")):
                    fpath = Path(root) / fname
                    try:
                        fpath.unlink()
                        removed += 1
                    except OSError:
                        pass
    if removed:
        LOG.info("Cleaned up %d stale temporary file(s).", removed)
    return removed


# ── 13. Smart Asset Discovery & Resumable BEJSON 104a State Tracking ─────────
STATE_FIELDS: Final[List[Dict[str, str]]] = [
    {"name": "rel_path", "type": "string"},
    {"name": "source_size", "type": "integer"},
    {"name": "source_mtime", "type": "number"},
    {"name": "folder_name", "type": "string"},
    {"name": "stage_prompted", "type": "boolean"},
    {"name": "stage_written", "type": "boolean"},
    {"name": "stage_completed", "type": "boolean"},
    {"name": "provider_used", "type": "string"},
    {"name": "model_used", "type": "string"},
    {"name": "files_emitted", "type": "integer"},
    {"name": "updated_at", "type": "string"},
]


def rel_to_script(path: Path) -> str:
    try:
        return path.resolve().relative_to(SCRIPT_PATH).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _new_state_doc() -> Dict[str, Any]:
    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Schema_Name": "ProcessorJobState",
        "Records_Type": ["JobRecord"],
        "Fields": copy.deepcopy(STATE_FIELDS),
        "Values": [],
    }


def migrate_state_schema(doc: Dict[str, Any], state_path: Path) -> Dict[str, Any]:
    """Idempotent schema migration appending any missing STATE_FIELDS with .premigration backup."""
    existing_fields = [f.get("name") for f in doc.get("Fields", []) if isinstance(f, dict)]
    expected_fields = [f["name"] for f in STATE_FIELDS]
    if existing_fields == expected_fields:
        return doc

    backup_path = state_path.with_suffix(state_path.suffix + ".premigration")
    if state_path.exists() and not backup_path.exists():
        shutil.copy2(state_path, backup_path)

    old_fmap = bejson_core_get_field_map(doc)
    new_doc = _new_state_doc()
    defaults_by_type = {
        "string": "",
        "integer": 0,
        "number": 0.0,
        "boolean": False,
        "array": [],
        "object": {},
    }
    for old_row in doc.get("Values", []):
        if not isinstance(old_row, list):
            continue
        new_row: List[Any] = []
        for fld in STATE_FIELDS:
            fname, ftype = fld["name"], fld["type"]
            if fname in old_fmap and old_fmap[fname] < len(old_row):
                new_row.append(old_row[old_fmap[fname]])
            else:
                new_row.append(defaults_by_type[ftype])
        new_doc["Values"].append(new_row)

    write_json_atomic(state_path, new_doc)
    return new_doc


def load_or_init_state(state_path: Path) -> Dict[str, Any]:
    if not state_path.exists():
        doc = _new_state_doc()
        write_json_atomic(state_path, doc)
        return doc

    try:
        doc = bejson_core_load_file(state_path)
        doc = migrate_state_schema(doc, state_path)
        valid, errs = bejson_validator_check_fields_structure(doc)
        if not valid:
            raise ValueError("; ".join(errs))
        return doc
    except Exception as exc:
        corrupt_backup = state_path.with_suffix(state_path.suffix + f".corrupt.{int(time.time())}")
        LOG.warning("State file %s corrupt (%s); backing up to %s and reinitializing.", state_path.name, exc, corrupt_backup.name)
        try:
            shutil.copy2(state_path, corrupt_backup)
        except OSError:
            pass
        doc = _new_state_doc()
        write_json_atomic(state_path, doc)
        return doc


def get_job_record(state_doc: Dict[str, Any], rel_path: str, size: int, mtime: float) -> Optional[Dict[str, Any]]:
    fmap = bejson_core_get_field_map(state_doc)
    for row in state_doc.get("Values", []):
        if row[fmap["rel_path"]] == rel_path:
            # Verify source fingerprint (size + mtime within 1ms tolerance)
            if int(row[fmap["source_size"]]) == size and abs(float(row[fmap["source_mtime"]]) - mtime) < 0.001:
                return {k: row[idx] for k, idx in fmap.items()}
            return None
    return None


def checkpoint_job(
    state_doc: Dict[str, Any],
    state_path: Path,
    *,
    rel_path: str,
    source_size: int,
    source_mtime: float,
    folder_name: str,
    stage_prompted: bool,
    stage_written: bool,
    stage_completed: bool,
    provider_used: str,
    model_used: str,
    files_emitted: int,
) -> None:
    fmap = bejson_core_get_field_map(state_doc)
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    new_row = [None] * len(STATE_FIELDS)
    new_row[fmap["rel_path"]] = rel_path
    new_row[fmap["source_size"]] = source_size
    new_row[fmap["source_mtime"]] = round(source_mtime, 3)
    new_row[fmap["folder_name"]] = folder_name
    new_row[fmap["stage_prompted"]] = stage_prompted
    new_row[fmap["stage_written"]] = stage_written
    new_row[fmap["stage_completed"]] = stage_completed
    new_row[fmap["provider_used"]] = provider_used
    new_row[fmap["model_used"]] = model_used
    new_row[fmap["files_emitted"]] = files_emitted
    new_row[fmap["updated_at"]] = now_iso

    rows = state_doc.get("Values", [])
    for idx, row in enumerate(rows):
        if row[fmap["rel_path"]] == rel_path:
            rows[idx] = new_row
            write_json_atomic(state_path, state_doc)
            return
    rows.append(new_row)
    write_json_atomic(state_path, state_doc)


def collect_assets(assets_dir: Path, supported_exts: Sequence[str] = SUPPORTED_EXTS) -> List[Path]:
    """Scans assets_dir for supported extensions, skipping dotfiles, symlinks, and 0-byte files."""
    if not assets_dir.exists():
        return []
    allowed = {e.lower() for e in supported_exts}
    discovered: List[Path] = []
    for entry in sorted(assets_dir.iterdir(), key=lambda p: p.name):
        if entry.name.startswith("."):
            continue
        if entry.is_symlink():
            LOG.warning("Skipping symlink asset: %s", entry.name)
            continue
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in allowed:
            continue
        try:
            if entry.stat().st_size == 0:
                LOG.warning("Skipping 0-byte asset: %s", entry.name)
                continue
        except OSError:
            continue
        discovered.append(entry)
    return discovered


def choose_folder_name(asset: Path, all_assets: Sequence[Path], persisted_folder: Optional[str] = None) -> str:
    """Disambiguates same-stem asset collisions (e.g. doc.txt + doc.md -> doc_txt / doc_md)."""
    if persisted_folder:
        return persisted_folder
    same_stem = [a for a in all_assets if a.stem.lower() == asset.stem.lower()]
    if len(same_stem) > 1:
        ext_clean = asset.suffix.lower().lstrip(".") or "file"
        return f"{asset.stem}_{ext_clean}"
    return asset.stem


def place_original(src: Path, dest_dir: Path, mode: str = "copy") -> Optional[Path]:
    """Moves or copies original asset into dest_dir with cross-device fallback and size verification."""
    if mode == "keep":
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / f"source_{src.name}"
    src_size = src.stat().st_size
    if mode == "move":
        try:
            os.replace(src, target)
            return target
        except OSError:
            pass
    tmp_target = dest_dir / f".tmp_src_{os.getpid()}_{src.name}"
    shutil.copy2(src, tmp_target)
    if tmp_target.stat().st_size != src_size:
        tmp_target.unlink(missing_ok=True)
        raise OSError(f"Size mismatch placing original {src.name}")
    os.replace(tmp_target, target)
    if mode == "move":
        src.unlink(missing_ok=True)
    return target


# ── 14. Per-Asset Processing Pipeline ────────────────────────────────────────
def process_file(
    asset_path: Path,
    all_assets: Sequence[Path],
    cfg: Dict[str, Any],
    out_root: Path,
    state_doc: Dict[str, Any],
    *,
    dry_run: bool = False,
) -> bool:
    """
    Processes a single asset file through the configured REST AI provider,
    extracts XML command output blocks, writes outputs atomically to out/<folder_name>/,
    and updates BEJSON 104a state checkpoints.
    """
    stat = asset_path.stat()
    rel_path = rel_to_script(asset_path)
    existing = get_job_record(state_doc, rel_path, stat.st_size, stat.st_mtime)
    if existing and existing.get("stage_completed") is True:
        LOG.info("Skipping already-completed asset: %s -> out/%s/", asset_path.name, existing["folder_name"])
        return True

    folder_name = choose_folder_name(
        asset_path, all_assets, persisted_folder=existing.get("folder_name") if existing else None
    )
    target_dir = out_root / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    raw_content = asset_path.read_text(encoding="utf-8", errors="replace")
    prompt_body = (
        cfg["prompt_template"]
        .replace("{filename}", asset_path.name)
        .replace("{stem}", asset_path.stem)
        .replace("{ext}", asset_path.suffix)
        .replace("{content}", raw_content)
    )
    if cfg.get("enforce_xml_output", True):
        prompt_body += build_xml_output_instruction(cfg.get("xml_output_tag", "file"))

    provider = cfg["provider"]
    model_id = cfg["model_id"]

    if dry_run:
        LOG.info("[DRY-RUN] Would prompt %s (%s) for %s -> %s", provider, model_id, asset_path.name, rel_to_script(target_dir))
        return True

    resp = rest_ai_dispatch(
        provider,
        prompt_body,
        model_id=model_id,
        system_instruction=cfg.get("system_instruction"),
        keys_file=KEYS_FILE,
        secure_env_path=cfg.get("secure_env_path"),
        timeout=int(cfg["rest_timeout_seconds"]),
        retry_attempts=int(cfg["retry_attempts"]),
        retry_backoff=cfg["retry_backoff_seconds"],
        temperature=float(cfg["temperature"]),
        max_output_tokens=int(cfg["max_output_tokens"]),
    )

    if cfg.get("log_ai_calls", True):
        append_ai_call_log(
            CALL_LOG_FILE,
            provider,
            model_id,
            f"asset:{asset_path.name}",
            resp["content"] if resp["success"] else f"ERROR: {resp['error']}",
        )

    if not resp["success"]:
        LOG.error("AI REST call failed for %s: %s", asset_path.name, resp["error"])
        checkpoint_job(
            state_doc, STATE_FILE,
            rel_path=rel_path, source_size=stat.st_size, source_mtime=stat.st_mtime,
            folder_name=folder_name, stage_prompted=False, stage_written=False,
            stage_completed=False, provider_used=provider, model_used=model_id, files_emitted=0,
        )
        return False

    checkpoint_job(
        state_doc, STATE_FILE,
        rel_path=rel_path, source_size=stat.st_size, source_mtime=stat.st_mtime,
        folder_name=folder_name, stage_prompted=True, stage_written=False,
        stage_completed=False, provider_used=provider, model_used=model_id, files_emitted=0,
    )

    extracted = parse_xml_file_commands(resp["content"], tag_name=cfg.get("xml_output_tag", "file"))
    if not extracted:
        extracted = [(f"{asset_path.stem}_processed.txt", resp["content"])]

    written_count = 0
    for rel_out, file_body in extracted:
        out_file = (target_dir / rel_out).resolve()
        if not str(out_file).startswith(str(target_dir.resolve())):
            LOG.warning("Rejected unsafe relative output path %r in %s", rel_out, asset_path.name)
            continue
        out_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_file = out_file.parent / f".tmp_{os.getpid()}_{uuid.uuid4().hex[:6]}_{out_file.name}"
        encoded = (file_body or "").encode("utf-8")
        with open(tmp_file, "wb") as f:
            f.write(encoded)
            f.flush()
            os.fsync(f.fileno())
        if tmp_file.stat().st_size != len(encoded):
            tmp_file.unlink(missing_ok=True)
            raise OSError(f"Output size verification failed for {out_file.name}")
        os.replace(tmp_file, out_file)
        written_count += 1

    place_original(asset_path, target_dir, mode=cfg.get("source_handling", "copy"))

    checkpoint_job(
        state_doc, STATE_FILE,
        rel_path=rel_path, source_size=stat.st_size, source_mtime=stat.st_mtime,
        folder_name=folder_name, stage_prompted=True, stage_written=True,
        stage_completed=True, provider_used=provider, model_used=model_id, files_emitted=written_count,
    )
    LOG.info("Processed %s -> out/%s/ (%d file(s) written)", asset_path.name, folder_name, written_count)
    return True


# ── 15. Pre-Bootstrap CLI Argument Parser & Entry Point ──────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description=f"{PRODUCT_TITLE} — Standardized REST AI asset pipeline with BEJSON 104a state tracking.",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version and RELATIONAL_ID and exit.")
    parser.add_argument("--about", action="store_true", help="Show product credits, metadata, and active paths.")
    parser.add_argument("-c", "--config", type=str, default=None, help="Path to custom JSON configuration file.")
    parser.add_argument("-p", "--provider", type=str, default=None, help=f"REST provider override ({', '.join(sorted(PROVIDER_SPECS))}).")
    parser.add_argument("-m", "--model", type=str, default=None, help="Model ID override.")
    parser.add_argument("-s", "--system", type=str, default=None, help="System instruction override.")
    parser.add_argument("--prompt", type=str, default=None, help="One-shot direct prompt (bypasses assets/ folder).")
    parser.add_argument("--validate", action="store_true", help="Validate BEJSON state/key stores and configuration.")
    parser.add_argument("--stats", action="store_true", help="Show loaded API key counts and job state statistics.")
    parser.add_argument("--dry-run", action="store_true", help="Discover assets and preview REST dispatch without network calls.")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG console logging.")
    return parser


def format_about_block() -> str:
    return (
        f"\n{PRODUCT_TITLE}\n"
        f"Version:        {VERSION} (PKG {PACKAGE_VERSION})\n"
        f"Release_Version:300\n"
        f"Date:           {DATE_CREATED}\n"
        f"RELATIONAL_ID:  {RELATIONAL_ID}\n"
        f"Author:         Elton Boehnen\n"
        f"Contact:        boehnenelton2024@gmail.com\n"
        f"Website:        boehnenelton2024.pages.dev | github.com/boehnenelton\n"
        f"Format Creator: Elton Boehnen (BEJSON 104 / 104a)\n"
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    # 1. Pre-bootstrap parse_args() so --help / --version / --about never create folders
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        setup_console_logging(verbose=True)

    if args.version:
        LOG.info("%s v%s (PKG %s) | RELATIONAL_ID: %s", TOOL_NAME, VERSION, PACKAGE_VERSION, RELATIONAL_ID)
        return EXIT_OK

    if args.about:
        LOG.info(format_about_block().strip())
        return EXIT_OK

    # 2. Bootstrap directories & load validated config
    try:
        first_run = initialize_directories()
        attach_file_logging(LOG, LOGS_DIR)
        cfg = load_config(args.config)
    except ConfigError as exc:
        LOG.error("Configuration error: %s", exc)
        return EXIT_ENV_FAILURE
    except PathSecurityError as exc:
        LOG.error("Path initialization error: %s", exc)
        return EXIT_PATH_FAILURE

    # Apply CLI overrides
    if args.provider:
        prov_override = args.provider.lower().strip()
        if prov_override not in PROVIDER_SPECS:
            LOG.error("Unsupported provider %r. Choose from: %s", prov_override, ", ".join(sorted(PROVIDER_SPECS)))
            return EXIT_ENV_FAILURE
        cfg["provider"] = prov_override
        if not args.model:
            cfg["model_id"] = PROVIDER_SPECS[prov_override]["default_model"]
    if args.model:
        cfg["model_id"] = args.model.strip()
    if args.system:
        cfg["system_instruction"] = args.system.strip()

    assets_dir = SCRIPT_PATH / cfg["assets_subdir"]
    out_dir = SCRIPT_PATH / cfg["output_subdir"]
    assets_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 3. Handle --validate and --stats
    state_doc = load_or_init_state(STATE_FILE)
    key_reg = get_key_registry(cfg["provider"], KEYS_FILE, cfg.get("secure_env_path"))

    if args.validate:
        ok_state, errs_state = bejson_validator_check_fields_structure(state_doc)
        keys_doc = bejson_core_load_file(KEYS_FILE)
        ok_keys, errs_keys = bejson_validator_check_fields_structure(keys_doc)
        if not ok_state or not ok_keys:
            for e in errs_state + errs_keys:
                LOG.error("BEJSON validation error: %s", e)
            return EXIT_SCHEMA_FAILURE
        LOG.info("Validation PASSED: config.json, %s, and %s are valid.", STATE_FILE.name, KEYS_FILE.name)
        return EXIT_OK

    if args.stats:
        fmap = bejson_core_get_field_map(state_doc)
        rows = state_doc.get("Values", [])
        done = sum(1 for r in rows if r[fmap["stage_completed"]] is True)
        LOG.info(
            "Provider: %s | Model: %s | Keys Loaded: %d | Jobs Tracked: %d (%d completed)",
            cfg["provider"], cfg["model_id"], len(key_reg.keys), len(rows), done,
        )
        return EXIT_OK

    # 4. Acquire single-instance lock before running prompts or processing files
    try:
        with InstanceLock(LOCK_FILE):
            cleanup_stale_temps(out_dir, CONFIG_DIR)

            # One-shot prompt mode (--prompt)
            if args.prompt:
                if args.dry_run:
                    LOG.info("[DRY-RUN] Would send one-shot prompt to %s (%s).", cfg["provider"], cfg["model_id"])
                    return EXIT_OK
                resp = rest_ai_dispatch(
                    cfg["provider"],
                    args.prompt,
                    model_id=cfg["model_id"],
                    system_instruction=cfg.get("system_instruction"),
                    keys_file=KEYS_FILE,
                    secure_env_path=cfg.get("secure_env_path"),
                    timeout=int(cfg["rest_timeout_seconds"]),
                    retry_attempts=int(cfg["retry_attempts"]),
                    retry_backoff=cfg["retry_backoff_seconds"],
                    temperature=float(cfg["temperature"]),
                    max_output_tokens=int(cfg["max_output_tokens"]),
                )
                if cfg.get("log_ai_calls", True):
                    append_ai_call_log(
                        CALL_LOG_FILE, cfg["provider"], cfg["model_id"],
                        args.prompt, resp["content"] if resp["success"] else f"ERROR: {resp['error']}",
                    )
                if not resp["success"]:
                    LOG.error("One-shot prompt failed: %s", resp["error"])
                    return EXIT_ENV_FAILURE if "No valid API keys" in (resp["error"] or "") else EXIT_PARTIAL_FAILURE
                LOG.info("Response (%s / %s):\n%s", resp["provider"], resp["model_id"], resp["content"])
                return EXIT_OK

            # Asset folder batch processing mode
            assets = collect_assets(assets_dir)
            if not assets:
                if first_run:
                    LOG.info(
                        "First-run initialization complete. Drop supported files (%s) into %s/ and rerun.",
                        ", ".join(SUPPORTED_EXTS[:6]), rel_to_script(assets_dir),
                    )
                else:
                    LOG.info("No compatible assets found in %s/.", rel_to_script(assets_dir))
                return EXIT_OK

            if not args.dry_run and PROVIDER_SPECS[cfg["provider"]]["requires_key"] and not key_reg.keys:
                LOG.error(
                    "No API keys found for provider %r. Populate %s or %s.",
                    cfg["provider"], cfg.get("secure_env_path"), rel_to_script(KEYS_FILE),
                )
                return EXIT_ENV_FAILURE

            LOG.info("Discovered %d asset(s) in %s/.", len(assets), rel_to_script(assets_dir))
            failures = 0
            for asset in assets:
                ok = process_file(asset, assets, cfg, out_dir, state_doc, dry_run=args.dry_run)
                if not ok:
                    failures += 1

            if failures > 0:
                LOG.warning("Completed with %d failed asset(s). Rerun to resume unfinished items.", failures)
                return EXIT_PARTIAL_FAILURE

            LOG.info("All %d asset(s) processed cleanly.", len(assets))
            return EXIT_OK

    except BusyLockError as exc:
        LOG.error("%s", exc)
        return EXIT_BUSY


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        LOG.warning("Interrupted by user (SIGINT).")
        sys.exit(EXIT_INTERRUPTED)
