---
name: mfdb-105-upgrade-coordinator
description: >-
  Coordinate atomic whole-database upgrades of Foundational Era Multi-File Databases
  (104a.mfdb.bejson manifests and linked 104 entity tables) to Integrity Era Format 105
  (105a.mfdb.bejson manifests and 105 entity tables) with automated pre-upgrade verbatim backups,
  UUIDv4 field_uuid and record_uuid compilation, and E90-E95 verification using upgrade_mfdb_to_105.py.
  Use when migrating complete multi-file MFDB databases from v1.31 to v1.40. Do NOT use for
  single-file 104 document upgrades (use bejson-105-upgrade-automator), Foundational Era MFDB v1.31
  manifest CRUD (use mfdb-104-core), packing or mounting single-file MFDB-132 containers
  (use mfdb-104-chunker), or standalone MFDB validation without upgrading (use mfdb-105-validator).
---

# Skill: `mfdb-105-upgrade-coordinator` (Layer 4)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (Services & Deployment Automation)`
- **Era & Library Binding**: `104 -> 105 Multi-File Bridge (libraries_105, MFDB v1.40)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `104a.mfdb.bejson -> 105a.mfdb.bejson (+ data/*.105.bejson + Backups/)`
- **Date Created**: `2026-10-25`
- **RELATIONAL_ID**: `9e8d7c6b-5a4f-3e2d-1c0b-a9f8e7d6c5b4`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-105-upgrade-coordinator` orchestrates the complete, atomic, whole-database upgrade of Elton Boehnen's federated Multi-File Databases (MFDB) from Foundational Era v1.31 (`104a.mfdb.bejson` manifest + `.104.bejson` entity tables) to Integrity Era v1.40 (`105a.mfdb.bejson` manifest + `.105.bejson` entity tables).

While [`bejson-105-upgrade-automator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-105-upgrade-automator/SKILL.md) upgrades single standalone `.104.bejson` files, `mfdb-105-upgrade-coordinator` operates across the entire federated database boundary:
1. Traverses the central manifest's `Entities` table to identify all registered child tables.
2. Creates an atomic, timestamped pre-upgrade backup under `Backups/`.
3. Upgrades each registered entity table to Format 105, compiling `field_uuid` and `record_uuid`.
4. Updates bidirectional `Parent_Hierarchy` pointers to target `105a.mfdb.bejson`.
5. Promotes the manifest itself to `Format_Version: "105a"` and `MFDB_Version: "1.40"`.

---

## 2. When to Use

- Migrating a multi-file database from MFDB v1.31 to MFDB v1.40.
- Upgrading entire database folders containing a central `104a.mfdb.bejson` and registered entity child tables.
- Creating verbatim pre-upgrade snapshot backups prior to schema migration.
- Batch assigning `field_uuid` and `record_uuid` across federated tables.

## When NOT to Use

- Do NOT use for single standalone 104 document upgrades (use [`bejson-105-upgrade-automator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-105-upgrade-automator/SKILL.md)).
- Do NOT use for creating or editing Foundational Era MFDB v1.31 manifests (use [`mfdb-104-core`](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-core/SKILL.md)).
- Do NOT use for packing or mounting MFDB-132 chunk containers (use [`mfdb-104-chunker`](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-chunker/SKILL.md)).
- Do NOT use for validating MFDB v1.40 foreign key integrity without upgrading (use [`mfdb-105-validator`](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-105-validator/SKILL.md)).

---

## 3. CLI Tooling & Execution

The skill is driven by [`scripts/upgrade_mfdb_to_105.py`](./scripts/upgrade_mfdb_to_105.py).

### Command-Line Usage

```text
usage: upgrade_mfdb_to_105.py [-h] --manifest MANIFEST
                              [--backup-dir BACKUP_DIR] [--dry-run]
                              [--version]

options:
  --manifest MANIFEST     Path to central MFDB manifest (e.g. 104a.mfdb.bejson)
  --backup-dir BACKUP_DIR Custom directory path for pre-upgrade verbatim backups
  --dry-run               Simulate whole-database upgrade without mutating disk files
  --version               Show script version and exit
```

### Standard Invocations

```bash
# 1. Preview database upgrade without disk mutations
python3 ~/.gemini/config/skills/mfdb-105-upgrade-coordinator/scripts/upgrade_mfdb_to_105.py \
  --manifest "/path/to/database/104a.mfdb.bejson" \
  --dry-run

# 2. Execute full atomic whole-database upgrade with automatic backup
python3 ~/.gemini/config/skills/mfdb-105-upgrade-coordinator/scripts/upgrade_mfdb_to_105.py \
  --manifest "/path/to/database/104a.mfdb.bejson"
```

---

## 4. Deterministic Exit Codes

| Exit Code | Semantic Meaning | Recovery Action |
|:---:|---|---|
| `0` | Success | Upgrade complete, backup created, all tables verified. |
| `10` | Path Error | Verify `--manifest` points to a valid readable file. |
| `20` | Environment Error | Ensure Python $\ge 3.10$ and valid POSIX permissions. |
| `30` | Validation Failure | Check child table presence and schema integrity. |
