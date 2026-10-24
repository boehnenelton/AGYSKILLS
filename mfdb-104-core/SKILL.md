---
name: mfdb-104-core
description: >-
  Create, link, query, and validate Foundational Era Multi-File Databases (MFDB v1.31/v1.39) comprising a central 104a.mfdb.bejson manifest and dense BEJSON 104 entity files linked via bidirectional Parent_Hierarchy headers and Master-Slave Network_Role federation (E30-E38) using libraries_104. Use when managing 104a.mfdb.bejson manifests, registering 104 entity tables, or validating bidirectional manifest-to-entity paths. Do NOT use for packing or mounting single-file MFDB-132 (.mfdb132.bejson) chunk containers (use mfdb-104-chunker), validating Format 105 MFDB v1.40 cross-entity UUID FK cascades (use mfdb-105-validator), or standalone single-file 104 CRUD (use bejson-104-core).
---

# Skill: `mfdb-104-core` (Layer 1)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 1`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `104a.mfdb.bejson (Manifest) + data/*.104.bejson (Entities)`
- **Reference Specification**: `references/mfdb_104_spec.md` (Crash Course 23)
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `b08e1e29-552e-5c78-98a0-cc5f99ee6a69`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-104-core` operates at **Layer 1** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_mfdb_core.py`
- `Lib_PY/Core/lib_bejson_Core_mfdb_validator.py`
- `Lib_JS/Core/lib_bejson_Core_mfdb_core.js`
- `Lib_TS/Core/lib_bejson_Core_mfdb_core.ts`
- `Lib_SH/Core/lib_bejson_Core_mfdb_core.sh`

---

## 2. Core Structural & Policy Invariants

1. Manifest is a BEJSON 104a document with Records_Type: ['mfdb'] (E30, E32).
2. Every entity file is a BEJSON 104 document with a relative Parent_Hierarchy header pointing back to 104a.mfdb.bejson (E31, E36-E38).
3. Network_Role header ('Master' vs 'Slave') enforces structural blindness for slave nodes to preserve LLM context windows.

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

When invoking subagents or CLI verification tools from `mfdb-104-core`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute mfdb-104-core verification gate and return deterministic JSON status."
```

---

## 4. Accompanying Architecture Utilities

- **Two-Tier Content Scaffolder**: [`scripts/scaffold_two_tier_content.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-core/scripts/scaffold_two_tier_content.py)  
  Generates detached atomic `104db` content records (`pages_db/<uuid>.json`) containing `PageMeta` and `Content` discriminator rows.
- **MasterKeyMap Validator**: [`scripts/validate_master_keymap.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-core/scripts/validate_master_keymap.py)  
  Audits and verifies cross-taxonomy relational graph edge keys, route patterns, and companion links across disparate sub-taxonomies.

---

## When NOT to Use

Do NOT use `mfdb-104-core` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Packing or sticky-mounting MFDB-132 .mfdb132.bejson chunk containers**: Redirect immediately to `mfdb-104-chunker`.
- **Validating Format 105 MFDB v1.40 FK referential cascades and AES-GCM cells**: Redirect immediately to `mfdb-105-validator`.
- **Standalone single-file 104/104a/104db CRUD without MFDB federation**: Redirect immediately to `bejson-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
