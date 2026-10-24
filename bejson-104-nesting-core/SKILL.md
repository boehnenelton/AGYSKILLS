---
name: bejson-104-nesting-core
description: >-
  Embed, extract, flatten, and query recursive BEJSON 104 documents inside individual parent table cells using NestAddress(parent_path, row, col, depth) coordinates up to a maximum depth of 16 with column-schema uniformity enforcement (E130-E159) via libraries_104. Use when working with Nested 104 hierarchical cell payloads or running lib_bejson_Core_bejson_core_nesting and lib_bejson_Core_bejson_nesting_query across Python, JS, TS, or Bash. Do NOT use for flat top-level 104/104a/104db table CRUD (use bejson-104-core), black-box 104 validation (use bejson-104-validator), Format 105/105a/105db UUID-tracked documents (use bejson-105-core), Format 105 validation (use bejson-105-validator), 104-to-105 migration (use bejson-105-upgrade-automator), or multi-file MFDB federation (use mfdb-104-core).
---

# Skill: `bejson-104-nesting-core` (Layer 1)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 1`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `Nested 104 (.104.bejson with embedded 104 child cubes)`
- **Reference Specification**: `references/bejson_104_nesting_spec.md` (Crash Course 23)
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `97e8c75c-ca30-5dae-a8cb-db7044734b3d`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-104-nesting-core` operates at **Layer 1** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_core_nesting.py`
- `Lib_PY/Core/lib_bejson_Core_bejson_nesting_query.py`
- `Lib_TS/Core/lib_bejson_Core_bejson_core_nesting.ts`
- `Lib_SH/Core/lib_bejson_Core_bejson_core_nesting.sh`

---

## 2. Core Structural & Policy Invariants

1. Hard recursion ceiling: NESTING_MAX_DEPTH = 16 (exceeding raises E130 E_NEST_EXCEEDED_DEPTH).
2. Column-Schema Uniformity (E134 E_NEST_UNIFORMITY_MISMATCH): all nested 104 documents within the same parent column must share identical field names, types, and order.
3. Physical cell coordinate NestAddress(parent_path, row, col, depth) acts as an implicit foreign key.
4. Always resolve column index via field_map before indexing row[field_map[col_name]].

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

When invoking subagents or CLI verification tools from `bejson-104-nesting-core`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-104-nesting-core verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-104-nesting-core` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Top-level flat 104, 104a, or 104db CRUD operations**: Redirect immediately to `bejson-104-core`.
- **Standalone 104/104a/104db validation**: Redirect immediately to `bejson-104-validator`.
- **Format 105/105a/105db operations**: Redirect immediately to `bejson-105-core`.
- **Format 105 E90-E95 validation**: Redirect immediately to `bejson-105-validator`.
- **Upgrading 104 files to 105**: Redirect immediately to `bejson-105-upgrade-automator`.
- **Multi-File Database (MFDB) manifest management**: Redirect immediately to `mfdb-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
