---
name: bejson-105-upgrade-automator
description: >-
  Automate atomic migration of Foundational Era BEJSON 104, 104a, and 104db documents to Integrity Era Format 105, 105a, and 105db using libraries_105 lib_bejson_Core_bejson_upgrade.py and cli/bejson_upgrade_cli.py with dry-run validation, verbatim Backups/<filename>.104.bak preservation, UUIDv4 field_uuid and record_uuid compilation, E90-E95 verification, and POSIX atomic .105tmp replacement. Use when upgrading existing 104-series files to 105-series without triggering E95 (E_105_FAIL_ON_SWITCH). Do NOT use for CRUD on unmigrated 104 files (use bejson-104-core), CRUD on already-upgraded 105 files (use bejson-105-core), standalone 104 validation (use bejson-104-validator), standalone 105 validation (use bejson-105-validator), or recursive Nested 104 cell manipulation (use bejson-104-nesting-core).
---

# Skill: `bejson-105-upgrade-automator` (Layer 3)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 3`
- **Era & Library Binding**: `104 -> 105 Cross-Era Bridge (libraries_105, v1.0.2)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `104 -> 105, 104a -> 105a, 104db -> 105db (+ Backups/*.104.bak)`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `d5917975-d6f7-58f3-a2d4-17c8a0142655`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-105-upgrade-automator` operates at **Layer 3** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_upgrade.py (bejson_core_upgrade_to_105, bejson_core_upgrade_dry_run)`
- `Lib_PY/Core/cli/bejson_upgrade_cli.py`

---

## 2. Core Structural & Policy Invariants

1. Explicitly maps 104 -> 105, 104a -> 105a, and 104db -> 105db (preserving Record_Type_Parent at index 0 and inserting record_uuid at index 1 for 105db).
2. Always runs bejson_core_upgrade_dry_run() first to verify 0 errors on in-memory build.
3. Copies original file verbatim to Backups/<filename>.104.bak before writing .105tmp and executing os.fsync + os.replace.
4. Returns upgraded document with warm self-maintaining field_map cache.

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

When invoking subagents or CLI verification tools from `bejson-105-upgrade-automator`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-105-upgrade-automator verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-105-upgrade-automator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Standard CRUD on unmigrated 104, 104a, or 104db files**: Redirect immediately to `bejson-104-core`.
- **Standard CRUD on already-upgraded 105, 105a, or 105db files**: Redirect immediately to `bejson-105-core`.
- **Standalone validation of 104-series files**: Redirect immediately to `bejson-104-validator`.
- **Standalone validation of 105-series files**: Redirect immediately to `bejson-105-validator`.
- **Recursive Nested 104 cell operations**: Redirect immediately to `bejson-104-nesting-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
