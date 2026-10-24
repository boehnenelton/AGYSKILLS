---
name: mfdb-105-validator
description: >-
  Validate Integrity Era MFDB v1.40 federated multi-file databases for cross-entity foreign-key (_fk) referential integrity (E39 E_MFDB_UNRESOLVED_FK), fk_on_delete cascade/null/default/restrict conformance, bidirectional Parent_Hierarchy resolution (E30-E38), and Web Crypto ENC:AES-GCM cell encryption integrity using libraries_105. Use when auditing MFDB v1.40 databases containing Format 105 entities or cross-table foreign keys. Do NOT use for Foundational Era MFDB v1.31 manifest CRUD (use mfdb-104-core), packing or mounting MFDB-132 .mfdb132.bejson chunk containers (use mfdb-104-chunker), or single-file 105 validation without MFDB manifests (use bejson-105-validator).
---

# Skill: `mfdb-105-validator` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `105 (Integrity Era - libraries_105 MFDB v1.40)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `MFDB v1.40 (104a/105a Manifest + 105 Entities + ENC:AES-GCM cells)`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `a5e6447f-4081-5ceb-8d9b-083cd6cf8120`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-105-validator` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_mfdb_core.py (libraries_105)`
- `Lib_PY/Core/lib_bejson_Core_mfdb_validator.py (libraries_105)`
- `Lib_PY/Core/tests/test_mfdb_ref_integrity_suite.py`

---

## 2. Core Structural & Policy Invariants

1. Enforces E39 (E_MFDB_UNRESOLVED_FK) across all _fk columns referencing parent entity primary keys.
2. Verifies fk_on_delete cascade, null, default, and restrict behaviors across federated entity tables.
3. Validates Web Crypto AES-GCM 256-bit cell tags (ENC:AES-GCM:<salt_b64>:<iv_b64>:<ciphertext_b64>).

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

When invoking subagents or CLI verification tools from `mfdb-105-validator`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute mfdb-105-validator verification gate and return deterministic JSON status."
```

---

---

## 4. CLI Tool Reference (`scripts/validate_master_keymap_105.py`)

The skill provides the executable validator script `scripts/validate_master_keymap_105.py`:

```bash
# Validate an MFDB v1.40 database root or manifest file
python3 scripts/validate_master_keymap_105.py /path/to/mfdb_dir

# Validate with explicit manifest path
python3 scripts/validate_master_keymap_105.py --manifest /path/to/105a.mfdb.bejson
```

---

## When NOT to Use

Do NOT use `mfdb-105-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Foundational Era MFDB v1.31/v1.39 manifest and entity CRUD**: Redirect immediately to `mfdb-104-core`.
- **Packing or sticky-mounting .mfdb132.bejson chunk containers**: Redirect immediately to `mfdb-104-chunker`.
- **Single-file Format 105/105a/105db validation without an MFDB manifest**: Redirect immediately to `bejson-105-validator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
