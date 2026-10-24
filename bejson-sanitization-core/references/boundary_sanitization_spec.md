# Boundary-Layer Data Sanitization Specification (Policy §10.9)

* System: Layer 1 Core Substrate & Data Ingestion
* Policy Grounding: GEMINI.md — §10.9 (Boundary-Layer Data Sanitization)
* Component: `bejson-sanitization-core`
* Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
* Date Created: 2026-10-22

---

## 1. Policy §10.9 Mandate & Operational Rationale

```
[Raw Ingestion / Parser Input]
               │
               ▼
   [Boundary-Layer Sanitizer]  <--- Strips whitespace from keys, fields & rows
               │
               ▼
[Clean Payload Dictionary / Object]
               │
         ┌─────┴───────────────────────┐
         ▼                             ▼
[Field Map Cache Generation]    [Persistence / Atomic Write]
```

Policy §10.9 mandates:
> **Boundary-Layer Data Sanitization**: All parsers and ingestion scripts must implement boundary-layer sanitization by stripping leading and trailing whitespace from dictionary keys and string values prior to Field Map Cache generation or record processing.

### Operational Failure Modes Prevented:
1. **Broken Field Map Lookups**: If a dictionary key contains a hidden trailing space (`"user_id "`), a lookup for `"user_id"` fails or creates redundant field map offsets.
2. **Hash Collisions & Corruption**: Unsanitized boundary whitespace corrupts row hashes and duplicate detection metrics.
3. **Database Query Drift**: Querying `WHERE entity_name = "Auth"` fails if records store `" Auth "` or `"Auth\n"`.

---

## 2. Sanitization Contract

### 2.1 Dictionary Keys
- All string keys in JSON/BEJSON objects must be trimmed:
  $$\text{key}_{\text{clean}} = \text{key}.\text{strip}()$$

### 2.2 Fields Definitions (`Fields`)
- Each field object's `name`, `type`, and `description` string values must be trimmed:
  ```python
  field_def["name"] = field_def["name"].strip()
  field_def["type"] = field_def["type"].strip()
  ```

### 2.3 Values Array (`Values`)
- For every row in `Values`, string cells must be trimmed; non-string primitives (integers, floats, booleans, nulls) remain unmodified:
  ```python
  row[idx] = val.strip() if isinstance(val, str) else val
  ```

---

## 3. Multi-Language Usage Patterns

### 3.1 Python Integration
```python
from bejson_sanitizer import (
    bejson_sanitize_payload,
    bejson_sanitize_row,
    bejson_sanitize_incoming_payload,
)

# 1. Direct Payload Cleaning
clean_document = bejson_sanitize_payload(raw_document)

# 2. Decorator Pattern for Owning Writers
@bejson_sanitize_incoming_payload
def save_user_profile(user_payload: dict) -> None:
    # user_payload is guaranteed free of boundary whitespace
    ...
```

### 3.2 JavaScript / Node Integration
```javascript
const { bejsonSanitizePayload, bejsonSanitizationMiddleware } = require('./bejson_sanitizer');

// 1. Ingestion Function
const cleanDoc = bejsonSanitizePayload(rawDoc);

// 2. Express Middleware
app.use(bejsonSanitizationMiddleware);
```

### 3.3 Bash / jq Integration
```bash
# In-place file sanitization
bejson_sanitize_file_inplace "data/records.104a.bejson"

# In-memory pipeline
clean_json=$(echo "$raw_json" | bejson_sanitize_payload_string)
```
