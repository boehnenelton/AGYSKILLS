---
name: mfdb-schema-validator
description: >-
  Validate structural integrity, bidirectional Parent_Hierarchy handshakes,
  Network_Role alignment (Master, Slave, Proxy, Standalone), DAG cycle freedom,
  and unregistered entity compliance across Foundational Era 104 and Integrity
  Era 105 Multi-File Database clusters (error codes E30-E39). Use when executing
  Layer 2 pre-flight or post-mutation verification gates on 104a.mfdb.bejson
  or 105a.mfdb.bejson manifests, detecting dangling foreign keys, checking
  circular parent-child links, or auditing multi-manifest cluster consistency.
  Do NOT use for mutating 104 MFDB tables (use mfdb-104-core), mutating 105
  MFDB tables (use mfdb-105-core), single-file 104 schema validation (use
  bejson-104-validator), single-file 105 UUID validation (use bejson-105-validator),
  designing multi-MFDB topologies (use mfdb-multi-architect), or migrating
  MFDBs from 104 to 105 (use mfdb-105-upgrade-coordinator).
---

# Skill: `mfdb-schema-validator` (Layer 2 Multi-File Database Validator)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Verification Engine)`
- **Era Compatibility**: `Cross-Era (Foundational Era 104 & Integrity Era 105)`
- **Target Formats**: `104a.mfdb.bejson`, `105a.mfdb.bejson`, `*.104.bejson`, `*.105.bejson`
- **Error Code Coverage**: `E30` through `E39`
- **Reference Specification**: [`references/error_code_taxonomy.md`](./references/error_code_taxonomy.md)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`mfdb-schema-validator` is the authoritative Layer 2 gatekeeper for Multi-File Databases. It validates cluster integrity across physical filesystem boundaries, guaranteeing bidirectional manifest-entity registration, network role harmony, foreign key referential integrity, and mathematical cycle freedom.

---

## 2. The Ten MFDB Invariant Gates (E30-E39)

Every Multi-MFDB cluster evaluated by this validator must pass all ten invariant gates:

```text
[Cluster Root Manifest]
       |
       +--> [Gate E30]: Manifest exists at resolved path
       +--> [Gate E31]: Format version is valid (104a / 105a)
       +--> [Gate E32]: Records_Type contains 'mfdb'
       +--> [Gate E33]: Canonical Fields array declared
       +--> [Gate E34]: Values tabular matrix present
       +--> [Gate E35]: Child Parent_Hierarchy points back to manifest
       +--> [Gate E36]: Linkage graph has zero circular cycles (DFS DAG)
       +--> [Gate E37]: Network_Role matches (Master / Slave / Proxy)
       +--> [Gate E38]: Zero unregistered entity files in partition
       +--> [Gate E39]: Cross-entity foreign keys resolve without dangling pointers
```

---

## 3. Mandatory Execution & Containment Contract (Level 3 Guardrail)

When executing automated verification from `mfdb-schema-validator`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Validation Failure):

```bash
python3 scripts/mfdb_schema_validator.py --manifest "path/to/104a.mfdb.bejson" --report
```

---

## 4. Accompanying Validation Engine

- **Executable CLI Validator**: [`scripts/mfdb_schema_validator.py`](./scripts/mfdb_schema_validator.py)  
  High-speed Python 3.10+ command-line verification engine that recursively walks cluster manifests, builds adjacency matrices, detects cycles, and outputs structured audit reports to `reports/audits/`.

---

## When NOT to Use

Do NOT use `mfdb-schema-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Executing runtime CRUD mutations on 104 MFDB tables**: Redirect immediately to `mfdb-104-core`.
- **Executing runtime CRUD mutations on 105 MFDB tables**: Redirect immediately to `mfdb-105-core`.
- **Validating standalone single-file 104 data stores**: Redirect immediately to `bejson-104-validator`.
- **Validating standalone single-file 105 UUID documents**: Redirect immediately to `bejson-105-validator`.
- **Architecting Multi-MFDB cluster topologies**: Redirect immediately to `mfdb-multi-architect`.
- **Coordinating whole-database 104-to-105 upgrades**: Redirect immediately to `mfdb-105-upgrade-coordinator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
