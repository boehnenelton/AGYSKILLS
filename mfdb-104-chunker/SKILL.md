---
name: mfdb-104-chunker
description: >-
  Package, unpack, and sticky-mount Multi-File Databases and software repositories into single-file Chunked-104a containers (.mfdb132.bejson) with SHA-256 .mfdb132_lock verification and macro-chunking via libraries_104 (lib_bejson_Core_bejson_chunking.py and mfdb_chunker_v6.py). Use when collapsing an MFDB directory or codebase into a portable .mfdb132.bejson bundle or mounting a chunked container. Do NOT use for standard multi-file 104a.mfdb.bejson manifest CRUD (use mfdb-104-core), Format 105 MFDB v1.40 FK referential integrity validation (use mfdb-105-validator), or single-file 104 table edits (use bejson-104-core).
---

# Skill: `mfdb-104-chunker` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `Chunked-104a (.mfdb132.bejson) + .mfdb132_lock`
- **Reference Specification**: `references/mfdb_132_chunking_spec.md` (Crash Course 23)
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `50fb9c3a-fcc7-5581-bafe-480a487bd86d`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-104-chunker` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_chunking.py`
- `Lib_PY/Chunker/lib_bejson_Chunker_mfdb_chunker_v5.py`
- `Lib_PY/Chunker/lib_bejson_Chunker_mfdb_chunker_v6.py`
- `Lib_PY/ExpCMS/lib_bejson_ExpCMS_mfdb_chunker_v6.py`

---

## 2. Core Structural & Policy Invariants

1. Fixed Chunk Schema fields: File_Name, File_Extension, File_Content, File_Version, File_Hash, Relative_Path, Is_Binary, Is_Mounted.
2. Sticky Mount verifies SHA-256 hash against .mfdb132_lock before reusing or unpacking workspace.
3. Pre-Write Gate validates database integrity prior to disk flush.

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

When invoking subagents or CLI verification tools from `mfdb-104-chunker`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute mfdb-104-chunker verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `mfdb-104-chunker` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Standard multi-file 104a.mfdb.bejson manifest and entity CRUD**: Redirect immediately to `mfdb-104-core`.
- **Format 105 MFDB v1.40 foreign-key referential integrity auditing**: Redirect immediately to `mfdb-105-validator`.
- **Standard single-file 104/104a/104db CRUD**: Redirect immediately to `bejson-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
