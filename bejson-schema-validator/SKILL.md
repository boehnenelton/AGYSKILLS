---
name: bejson-schema-validator
description: >-
  Validate structural integrity, schema adherence, primitive field constraints, and era-specific invariants across all BEJSON formats (104, 104a, 104db, 105, 105a, 105db) using era-neutral dispatch. Use when verifying BEJSON files of unknown, mixed, or evolving eras, executing Layer 2 stage gates on data stores, checking POL-002 primitive-only rules, or verifying E90-E95 UUID integrity. Do NOT use for specialized Python/JS AST source policy audits (use policy-bejson-auditor), BEHTML coordinate quantization and DOM layout validation (use behtml-schema-validator), or MFDB v1.40 cross-file referential integrity (use mfdb-105-validator).
---

# Skill: `bejson-schema-validator` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (L1_Validation_L2_Verification)`
- **Era & Library Binding**: `Cross-Era Neutral Dispatcher (104 & 105 Series)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `104, 104a, 104db, 105, 105a, 105db`
- **Date Created**: `2026-10-24`
- **RELATIONAL_ID**: `b201a000-0002-4000-8000-000000000002`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-schema-validator` operates at **Layer 2** of the 6-Tier Layered Skill Architecture as the unified, era-neutral gateway for BEJSON schema validation. It inspects incoming `.bejson` payloads, identifies the target `Format_Version`, and executes strict deterministic validation against both **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** invariants.

### Bound Canonical Modules
- `scripts/validate_bejson_schema.py`: Primary era-neutral validation CLI and dispatch engine.
- `config/config.json`: Standard BEJSON 104a runtime configuration store.

---

## 2. When to Use

- Validating `.bejson` data stores when the underlying era (104 vs. 105) is dynamic, mixed, or not known ahead of time.
- Executing Layer 2 stage gates in build pipelines and DAG runners prior to payload delivery.
- Validating POL-002 primitive-only field typing rules for `104a` and `105a` configuration stores.
- Enforcing `104db` and `105db` discriminator row rules (`Record_Type_Parent` matching `Records_Type`).
- Enforcing Integrity Era E90–E95 UUID invariants (mandatory `field_uuid` definitions and row index 0 `record_uuid`).
- Batch scanning directories for corrupt or invalid `.bejson` files.

---

## 3. When NOT to Use

- **Static AST auditing of source code for O(1) field map compliance**: Redirect immediately to `policy-bejson-auditor`.
- **Validating spatial 8-lane / 32px BEHTML layouts and component grids**: Redirect immediately to `behtml-schema-validator`.
- **Validating MFDB v1.40 cross-file foreign-key cascade graphs**: Redirect immediately to `mfdb-105-validator`.
- **Deep nesting recursive cell queries**: Redirect immediately to `bejson-104-nesting-core`.
- **Scaffolding new BEJSON files or owning writers**: Redirect immediately to `template-104-template` (104) or `template-105-template` (105).

---

## 4. Core Structural Invariants Enforced

1. **Top-Level Key Mandate**: Every valid BEJSON document MUST contain `Format`, `Format_Version`, `Format_Creator`, `Records_Type`, `Fields`, and `Values`.
2. **Era Detection & Routing**:
   - `104`, `104a`, `104db`: Checked for column count parity, field type conformance, and reserved `_` key rejection (E10).
   - `105`, `105a`, `105db`: Checked for unique UUIDv4 `field_uuid` on every field (E90/E91) and unique UUIDv4 `record_uuid` at row offset `0` (E92/E93).
3. **Deterministic Exit Codes**:
   - `0`: Validation successful / all files valid.
   - `10`: Target file or directory path not found.
   - `20`: Environment or configuration failure.
   - `30`: Schema mismatch, missing mandatory keys, or type violation.

---

## 5. CLI Execution & Verification

Run the validator directly against any file or folder:

```bash
# Validate single file
python3 scripts/validate_bejson_schema.py data/store.104.bejson

# Enforce specific era
python3 scripts/validate_bejson_schema.py data/store.105.bejson --expected-era 105

# Batch audit directory
python3 scripts/validate_bejson_schema.py /path/to/project/data/
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
