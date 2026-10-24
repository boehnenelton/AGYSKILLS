---
name: bejson-105-validator
description: >-
  Validate Integrity Era BEJSON 105, 105a, and 105db documents for strict E90-E95 UUID integrity (field_uuid presence/uniqueness E90/E91, reserved record_uuid row offset and uniqueness E92/E93, and E95 Fail-on-Switch guard against uncompiled re-headering) plus row checksum tamper verification via libraries_105 across Python, JS, TS, and Bash. Use when executing Layer 2 stage-gate verification on .105.bejson, .105a.bejson, or .105db.bejson files. Do NOT use for mutating 105/105a/105db records (use bejson-105-core), upgrading 104 files to 105 (use bejson-105-upgrade-automator), validating Foundational Era 104/104a/104db files (use bejson-104-validator), mutating 104 files (use bejson-104-core), recursive Nested 104 cells (use bejson-104-nesting-core), or MFDB v1.40 cross-file FK cascade auditing (use mfdb-105-validator).
---

# Skill: `bejson-105-validator` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `105 (Integrity Era - libraries_105, v3.5.3+)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `105, 105a, 105db`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `6c77d385-9ca6-56f5-84f0-3da6a19d5a1e`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-105-validator` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_validator.py (bejson_validator_check_105_strict_integrity)`
- `Lib_PY/Core/lib_bejson_Core_bejson_list_validator.py`
- `Lib_JS/Core/lib_bejson_Core_bejson_validator.js`
- `Lib_TS/Core/lib_bejson_Core_bejson_validators.ts`
- `Lib_SH/Core/lib_bejson_Core_bejson_validator.sh`

---

## 2. Core Structural & Policy Invariants

1. E90 (E_105_MISSING_FIELD_UUID): Every field object in Fields must have field_uuid.
2. E91 (E_105_DUPLICATE_FIELD_UUID): Every field_uuid in Fields must be unique.
3. E92 (E_105_MISSING_RECORD_UUID): Every row in Values must have a valid UUIDv4 record_uuid at index 0 (105/105a) or index 1 (105db).
4. E93 (E_105_DUPLICATE_RECORD_UUID): Every record_uuid across Values rows must be unique.
5. E95 (E_105_FAIL_ON_SWITCH): Rejects any 104 document re-headered to 105 without compiled UUID columns.

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

When invoking subagents or CLI verification tools from `bejson-105-validator`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-105-validator verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-105-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Creating or updating 105, 105a, or 105db records**: Redirect immediately to `bejson-105-core`.
- **Upgrading 104/104a/104db files to 105/105a/105db**: Redirect immediately to `bejson-105-upgrade-automator`.
- **Validating Foundational Era 104, 104a, or 104db files**: Redirect immediately to `bejson-104-validator`.
- **Creating or updating 104, 104a, or 104db records**: Redirect immediately to `bejson-104-core`.
- **Recursive Nested 104 cell operations**: Redirect immediately to `bejson-104-nesting-core`.
- **Multi-file MFDB v1.40 cross-entity FK referential integrity validation**: Redirect immediately to `mfdb-105-validator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
