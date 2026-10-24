---
name: bejson-104-core
description: >-
  Create, read, update, delete, and query Foundational Era BEJSON 104, 104a, and 104db documents using libraries_104 (Release 300) across Python, JavaScript, TypeScript, and Bash with ResilientPIDLock atomic writes, _FieldMap O(1) field_map lookups, and boundary-layer whitespace sanitization. Use when manipulating .104.bejson entity tables, .104a.bejson ScriptConfig/tracker files (config/config.json, .bejson_project.json), or .104db.bejson multi-entity stores without Format 105 field_uuid/record_uuid columns. Do NOT use for recursive Nested 104 cell embedding (use bejson-104-nesting-core), black-box 104/104a/104db validation (use bejson-104-validator), Format 105/105a/105db documents with field_uuid and record_uuid (use bejson-105-core), E90-E95 105 validation (use bejson-105-validator), upgrading 104 files to 105 (use bejson-105-upgrade-automator), or MFDB manifest orchestration (use mfdb-104-core).
---

# Skill: `bejson-104-core` (Layer 1)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 1`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `104 (.104.bejson), 104a (.104a.bejson), 104db (.104db.bejson)`
- **Reference Specification**: `references/bejson_104_spec.md` (Crash Course 23)
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `2f416133-e3b7-5755-aebb-8ad10f692c55`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-104-core` operates at **Layer 1** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_core.py (v2.0.10)`
- `Lib_PY/Core/lib_bejson_Core_bejson_parse.py`
- `Lib_PY/Core/lib_bejson_Core_bejson_104db_parser.py`
- `Lib_JS/Core/lib_bejson_Core_bejson_core.js`
- `Lib_TS/Core/lib_bejson_Core_bejson_core.ts`
- `Lib_SH/Core/lib_bejson_Core_be_core.sh`

---

## 2. Core Structural & Policy Invariants

1. 104 allows string, integer, number, boolean, array, and object field types; forbids custom top-level keys except Parent_Hierarchy.
2. 104a enforces POL-002 (primitives only: string, integer, number, boolean; forbids array and object) and permits PascalCase custom top-level headers.
3. 104db requires 2+ entries in Records_Type, Fields[0] == Record_Type_Parent, per-field Record_Type_Parent ownership, and null-padding.
4. Always build and query via field_map = bejson_core_get_field_map(doc) before accessing row[field_map[col_name]].
5. Never persist top-level keys starting with '_' (rejected with E_RESERVED_KEY_COLLISION = 10).

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

When invoking subagents or CLI verification tools from `bejson-104-core`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-104-core verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-104-core` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Recursive Nested 104 cell embedding via NestAddress**: Redirect immediately to `bejson-104-nesting-core`.
- **Black-box E01-E12 and POL-002 validation of 104/104a/104db files**: Redirect immediately to `bejson-104-validator`.
- **Format 105, 105a, or 105db CRUD with field_uuid and record_uuid**: Redirect immediately to `bejson-105-core`.
- **Format 105 E90-E95 strict UUID integrity validation**: Redirect immediately to `bejson-105-validator`.
- **Migrating 104/104a/104db files to 105/105a/105db**: Redirect immediately to `bejson-105-upgrade-automator`.
- **MFDB 104a.mfdb.bejson manifest orchestration**: Redirect immediately to `mfdb-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
