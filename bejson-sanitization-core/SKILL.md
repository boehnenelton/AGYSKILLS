---
name: bejson-sanitization-core
description: >-
  Sanitize boundary-layer BEJSON payloads, dictionary keys, and record rows across Python, JavaScript, and Bash per Policy §10.9 prior to Field Map Cache compilation, serialization, or persistence writes. Use when writing or refactoring BEJSON parsers, serializers, or ingestion pipelines, stripping whitespace from incoming dictionary keys and table cells, or embedding sanitization decorators and middleware. Do NOT use for top-level 104 table CRUD (use bejson-104-core), Format 105 UUID operations (use bejson-105-core), schema structural validation (use bejson-104-validator), or auditing code ASTs (use policy-bejson-auditor).
---

# bejson-sanitization-core (Layer 1 Boundary-Layer Data Sanitization Primitives)

## Summary

`bejson-sanitization-core` operates at Layer 1 (`L0_Substrate_L1_Entities`) to enforce the Policy §10.9 Boundary-Layer Data Sanitization mandate across the Antigravity ecosystem. It provides reusable, multi-language primitives (`Python`, `JavaScript`, `Bash`) to strip leading and trailing whitespace from dictionary keys, field definitions, and record values before Field Map Cache compilation or database writes.

## When to Use

- Writing or refactoring BEJSON parsers, serializers, or network ingestion pipelines.
- Stripping boundary whitespace from top-level keys, `Fields` declarations, and `Values` rows prior to generating the O(1) Field Map Cache.
- Applying `@bejson_sanitize_incoming_payload` decorators on Policy §10.4 owning writer functions.
- Integrating `BejsonSanitizationMiddleware` into API boundaries and ingestion routers.
- Cleansing external JSON drops or legacy tabular stores before running schema validators.

## When NOT to Use

- Do NOT use for standard top-level 104/104a/104db table CRUD (use `bejson-104-core`).
- Do NOT use for Format 105 UUID generation, row tracking, or E90-E95 migrations (use `bejson-105-core`).
- Do NOT use for black-box Layer 2 schema structural validation (use `bejson-104-validator` or `bejson-105-validator`).
- Do NOT use for static AST auditing of source code (use `policy-bejson-auditor`).

---

## 1. Architectural Guardrails & Invariants

- **Assigned Skill Tier**: Layer 1 (`L0_Substrate_L1_Entities` / Open Substrate).
- **Allowed Downward Dependencies**: None (Zero external dependencies; foundational primitive).
- **Policy §10.9 Grounding**: All dictionary keys and cell strings must be stripped of boundary whitespace prior to computing hashes, building field maps, or committing atomic writes.
- **Type Preservation**: Non-string values (integers, floats, booleans, nulls) must remain unaltered; never coerce numbers to strings during sanitization.

---

## 2. Multi-Language Primitive Reference

### 2.1 Python Primitives (`scripts/bejson_sanitizer.py`)

```python
from bejson_sanitizer import (
    bejson_sanitize_payload,
    bejson_sanitize_row,
    bejson_sanitize_incoming_payload,
)

# 1. Clean entire document before Field Map generation
clean_doc = bejson_sanitize_payload(raw_doc)

# 2. Clean single row before append
clean_row = bejson_sanitize_row(raw_row)

# 3. Decorator on Owning Writers
@bejson_sanitize_incoming_payload
def persist_record(record_payload: dict) -> None:
    ...
```

### 2.2 JavaScript / Node Primitives (`scripts/bejson_sanitizer.js`)

```javascript
const { bejsonSanitizePayload, bejsonSanitizationMiddleware } = require('./bejson_sanitizer');

// Ingestion Pipeline Sanitization
const cleanPayload = bejsonSanitizePayload(incomingPayload);

// Express Boundary Middleware
app.use(bejsonSanitizationMiddleware);
```

### 2.3 Bash / jq Primitives (`scripts/bejson_sanitizer.sh`)

```bash
# In-place file sanitization
bejson_sanitize_file_inplace "data/records.104a.bejson"

# In-memory stream filter
sanitized_json=$(echo "$raw_json" | bejson_sanitize_payload_string)
```

---

## 3. CLI Command Reference

* **Run Self-Test Validation Assertions:**
  ```bash
  python3 scripts/bejson_sanitizer.py --test
  ```
* **Sanitize a BEJSON File In-Place:**
  ```bash
  python3 scripts/bejson_sanitizer.py /path/to/target.104a.bejson
  ```
* **Display Configuration & Policy Info:**
  ```bash
  python3 scripts/bejson_sanitizer.py --config
  ```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
