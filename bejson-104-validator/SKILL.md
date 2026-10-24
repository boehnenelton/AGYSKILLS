---
name: bejson-104-validator
description: >-
  Validate Foundational Era BEJSON 104, 104a, and 104db documents and parent-child list trees for E01-E12 structural integrity, POL-002 104a primitive-only field conformance, 104db Record_Type_Parent discriminator rules, E10 reserved '_' key rejection, and cycle/orphan tree verification via libraries_104 and bejson_core_writer_cli.py. Use when executing Layer 2 stage-gate validation on .104.bejson, .104a.bejson, or .104db.bejson files. Do NOT use for mutating 104/104a/104db records (use bejson-104-core), recursive Nested 104 cell traversal (use bejson-104-nesting-core), validating Format 105/105a/105db E90-E95 UUID constraints (use bejson-105-validator), mutating Format 105 records (use bejson-105-core), upgrading 104 files to 105 (use bejson-105-upgrade-automator), or auditing Python/JS ASTs for policy compliance (use policy-bejson-auditor).
---

# Skill: `bejson-104-validator` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `104, 104a, 104db, and 104 Lists/Trees`
- **Reference Specification**: `references/bejson_104_validation_spec.md` (Crash Course 23)
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `671a7b9e-682a-57d7-be31-b87c1fcc9ee3`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-104-validator` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_validator.py`
- `Lib_PY/Lists/lib_bejson_Lists_list_validator.py`
- `/storage/emulated/0/Admin/Core/libraries/bejson_core_writer_cli.py`
- `Lib_JS/Core/lib_bejson_Core_bejson_validator.js`
- `Lib_TS/Core/lib_bejson_Core_bejson_validators.ts`
- `Lib_SH/Core/lib_bejson_Core_bejson_validator.sh`

---

## 2. Core Structural & Policy Invariants

1. Enforces error codes E01 through E12 across Python, JS, TS, and Bash.
2. In 104a, rejects any field with type 'array' or 'object' (POL-002).
3. In 104, rejects any custom top-level key except Parent_Hierarchy (E10).
4. In 104db, requires Fields[0].name == 'Record_Type_Parent' and Record_Type_Parent on all subsequent fields (E11).

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

When invoking subagents or CLI verification tools from `bejson-104-validator`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-104-validator verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-104-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Creating or updating 104, 104a, or 104db records**: Redirect immediately to `bejson-104-core`.
- **Navigating recursive Nested 104 cells**: Redirect immediately to `bejson-104-nesting-core`.
- **Validating Format 105, 105a, or 105db E90-E95 UUID rules**: Redirect immediately to `bejson-105-validator`.
- **Creating or updating Format 105 records**: Redirect immediately to `bejson-105-core`.
- **Upgrading 104-series files to 105-series**: Redirect immediately to `bejson-105-upgrade-automator`.
- **Auditing application source code AST for raw field literals**: Redirect immediately to `policy-bejson-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
