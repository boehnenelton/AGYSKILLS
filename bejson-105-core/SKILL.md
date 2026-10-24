---
name: bejson-105-core
description: >-
  Create, read, update, and manage Integrity Era BEJSON 105, 105a, and 105db documents using libraries_105 (v3.5.3+) across Python, JavaScript, TypeScript, and Bash with mandatory field_uuid fingerprinting, reserved record_uuid row tracking (index 0 for 105/105a, index 1 for 105db), self-maintaining by_name_row and by_uuid field_map caches, bejson_core_define_field() FK declarations, and row checksums. Use when constructing or mutating Format 105, 105a, or 105db documents or calling libraries_105 runtime APIs. Do NOT use for Foundational Era 104, 104a, or 104db files lacking field_uuid and record_uuid (use bejson-104-core), recursive Nested 104 cells (use bejson-104-nesting-core), 104 validation (use bejson-104-validator), black-box E90-E95 105 validation (use bejson-105-validator), or upgrading existing 104 files to 105 (use bejson-105-upgrade-automator).
---

# Skill: `bejson-105-core` (Layer 1)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 1`
- **Era & Library Binding**: `105 (Integrity Era - libraries_105, v3.5.3+)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `105 (.105.bejson), 105a (.105a.bejson), 105db (.105db.bejson)`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `d0cb9ce9-fd6d-5cdc-b4f8-e863ab756944`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-105-core` operates at **Layer 1** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_core.py (v3.5.3)`
- `Lib_JS/Core/lib_bejson_Core_bejson_core.js`
- `Lib_TS/Core/lib_bejson_Core_bejson_core_105.ts`
- `Lib_SH/Core/lib_bejson_Core_bejson_core.sh`

---

## 2. Core Structural & Policy Invariants

1. Every field definition in Fields must include a unique UUIDv4 'field_uuid' (E90, E91).
2. Every row in Values contains a reserved UUIDv4 'record_uuid' at index 0 for 105/105a (+1 data offset) or index 1 after Record_Type_Parent for 105db (+2 data offset) (E92, E93).
3. Self-maintaining field_map cache (by_name_row, by_uuid, fingerprint) automatically applies the +1/+2 offset so row[field_map[col_name]] always targets the exact column.
4. Use bejson_core_define_field() to declare fk_target_entity and fk_on_delete ('cascade' | 'null' | 'default' | 'restrict').

### Mandatory Field Map Cache & Boundary Sanitization Pattern
All record reads and writes must strip boundary whitespace (Policy §10.9) and resolve column indices through a dynamic `field_map` (Policy §6.2):

```python
def bejson_read_column(doc: dict, field_map: dict[str, int], row: list, col_name: str):
    clean_col = col_name.strip()
    col_idx = field_map[clean_col]
    val = row[col_idx]
    return val.strip() if isinstance(val, str) else val
```

---

## 3. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or CLI verification tools from `bejson-105-core`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-105-core verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-105-core` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Foundational Era 104, 104a, or 104db CRUD without UUID columns**: Redirect immediately to `bejson-104-core`.
- **Recursive Nested 104 cell operations**: Redirect immediately to `bejson-104-nesting-core`.
- **Validating Foundational Era 104/104a/104db files**: Redirect immediately to `bejson-104-validator`.
- **Black-box E90-E95 validation of 105/105a/105db files**: Redirect immediately to `bejson-105-validator`.
- **Migrating existing 104/104a/104db files to 105/105a/105db**: Redirect immediately to `bejson-105-upgrade-automator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
