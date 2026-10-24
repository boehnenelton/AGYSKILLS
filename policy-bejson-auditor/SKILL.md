---
name: policy-bejson-auditor
description: >-
  Audit BEJSON application source code, owning writers, and schema registries for Policy §6.2 O(1) field_map cache compliance (zero raw row[i] positional indexing), Policy §10.1 zero raw field-name string literals outside taxonomy modules, Policy §10.9 boundary-layer whitespace sanitization, Policy §4.6 Project_GUID governance, and Policy §10.6 five-test suite execution (Conformance, Manifest Integrity, Round-Trip, Lifecycle Smoke, Post-Reset). Use when executing a Layer 2 verification gate after scaffolding or modifying any BEJSON code module. Do NOT use for standalone 104/104a/104db data file validation (use bejson-104-validator), standalone 105/105a/105db data file validation (use bejson-105-validator), or scaffolding templates (use template-104-template).
---

# Skill: `policy-bejson-auditor` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `Cross-Era Standardization & AST Gate (104 & 105)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `Python, JS, TS, Bash Source AST + schema_registry.104a.bejson`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `a599ed19-2904-5ac8-86f9-bdc94e993f6f`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`policy-bejson-auditor` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `libraries_104/Lib_PY/Core/tests/test_field_map_integrity.py`
- `libraries_105/Lib_PY/Core/tests/test_format105_suite.py`

---

## 2. Core Structural & Policy Invariants

1. Rejects any Python/JS/TS file that indexes a BEJSON Values row without resolving via field_map.
2. Rejects any raw field-name string literal in application logic outside src/lib/lib_<family>_taxonomy.py (§10.1).
3. Verifies all 5 mandatory Policy §10.6 tests pass with Exit Code 0.

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

When invoking subagents or CLI verification tools from `policy-bejson-auditor`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute policy-bejson-auditor verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `policy-bejson-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Standalone .104.bejson, .104a.bejson, or .104db.bejson data file validation**: Redirect immediately to `bejson-104-validator`.
- **Standalone .105.bejson, .105a.bejson, or .105db.bejson data file validation**: Redirect immediately to `bejson-105-validator`.
- **Scaffolding 104 or 105 templates and owning writers**: Redirect immediately to `template-104-template`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
