---
name: mfdb-105-core
description: >-
  Create, read, update, delete, and query Integrity Era Multi-File Databases
  (MFDB v1.40) comprising a central 105a.mfdb.bejson manifest and Format 105
  entity files linked via bidirectional Parent_Hierarchy headers, Master-Slave
  Network_Role federation, immutable UUIDv4 field_uuid and record_uuid invariants
  (E90-E95), and row checksum tamper verification via libraries_105. Use when
  mutating 105a.mfdb.bejson manifests, inserting or querying Format 105 entity
  tables, managing encrypted AES-GCM cells, or updating 105 multi-plane clusters.
  Do NOT use for Foundational Era 104 MFDB operations (use mfdb-104-core),
  black-box 105 FK referential cascade validation (use mfdb-105-validator),
  standalone single-file 105 CRUD without MFDB federation (use bejson-105-core),
  upgrading 104 MFDBs to 105 (use mfdb-105-upgrade-coordinator), or designing
  multi-MFDB topologies (use mfdb-multi-architect).
---

# Skill: `mfdb-105-core` (Layer 1 Core Substrate)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 1 (Core Substrate & Invariant Data Format)`
- **Era & Library Binding**: `105 (Integrity Era - libraries_105, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Libraries/libraries_105`
- **Target Formats**: `105a.mfdb.bejson (Manifest) + data/*.105.bejson (Entities)`
- **Reference Specification**: [`references/mfdb_105_spec.md`](./references/mfdb_105_spec.md)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-105-core` provides the canonical Layer 1 runtime substrate for **Integrity Era Multi-File Databases (MFDB v1.40)**. It enforces strict cryptographic guarantees, immutable UUIDv4 primary keys, schema-level `field_uuid` tracking, row-level checksum verification, and boundary sanitization across all data mutations.

### Bound Canonical Modules (`libraries_105`)
- `Lib_PY/Core/lib_bejson_Core_mfdb_core.py`
- `Lib_PY/Core/lib_bejson_Core_mfdb_validator.py`
- `Lib_JS/Core/lib_bejson_Core_mfdb_core.js`
- `Lib_TS/Core/lib_bejson_Core_mfdb_core.ts`
- `Lib_SH/Core/lib_bejson_Core_mfdb_core.sh`

---

## 2. Integrity Era Invariants & E90-E95 Guardrails

Every operation conducted under `mfdb-105-core` strictly enforces the five E90-E95 Integrity Era invariants:

1. **`field_uuid` Presence & Uniqueness (E90, E91)**:
   Every field descriptor in `Fields` MUST contain a unique RFC 4122 Version 4 `field_uuid`. Renaming a field preserves this UUID, eliminating schema-drift ambiguity.
2. **`record_uuid` Primary Key (E92, E93)**:
   Column index 0 of every row in `Values` is reserved for `record_uuid` (RFC 4122 Version 4 UUID). Duplicate record UUIDs trigger immediate `E93` halts.
3. **Cryptographic Row Tamper Checksums (E94)**:
   Row integrity is guarded by SHA-256 digests. Mutations automatically recompute row checksums and update the parent manifest entity digest.
4. **E95 Fail-on-Switch Guard**:
   Attempting to process or mutate a 105 document using 104-series tooling triggers an immediate hard termination to prevent silent data corruption.
5. **Bidirectional Parent_Hierarchy Verification**:
   Child entity tables declare `Parent_Hierarchy: "../105a.mfdb.bejson"` and `Network_Role: "Slave"`. The parent manifest registers each child relative path and SHA-256 table digest.

---

## 3. Mandatory Field Map Cache & Boundary Sanitization Pattern

All record reads and writes must strip boundary whitespace (Policy §10.9) and resolve column indices through a dynamic `field_map` (Policy §6.2):

```python
def bejson_105_read_cell(
    bejson_document: dict,
    compiled_field_map: dict[str, int],
    table_row_record: list,
    target_column_name: str
):
    sanitized_column_name = target_column_name.strip()
    target_column_index = compiled_field_map[sanitized_column_name]
    raw_cell_value = table_row_record[target_column_index]
    return raw_cell_value.strip() if isinstance(raw_cell_value, str) else raw_cell_value
```

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or CLI verification tools from `mfdb-105-core`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute mfdb-105-core verification gate and return deterministic JSON status."
```

---

## 5. Accompanying CLI Engine

- **MFDB 105 CLI Engine**: [`scripts/mfdb_105_cli.py`](./scripts/mfdb_105_cli.py)  
  High-performance Python 3.10+ command-line utility for atomic record insertion, row updates, manifest synchronization, and E90-E95 verification on MFDB v1.40 databases.

---

## When NOT to Use

Do NOT use `mfdb-105-core` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Managing Foundational Era 104 MFDB clusters**: Redirect immediately to `mfdb-104-core`.
- **Executing Layer 2 stage-gate validation and FK cascade verification**: Redirect immediately to `mfdb-105-validator`.
- **Standalone single-file 105/105a/105db CRUD without MFDB manifests**: Redirect immediately to `bejson-105-core`.
- **Migrating complete MFDB databases from 104 to 105**: Redirect immediately to `mfdb-105-upgrade-coordinator`.
- **Architecting Multi-MFDB cluster topologies and prefix taxonomies**: Redirect immediately to `mfdb-multi-architect`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
