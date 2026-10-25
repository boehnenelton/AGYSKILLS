---
name: bejson-migration-pipeline
description: >-
  Ingest, parse, and transform legacy relational datasets, SQLite databases, CSV spreadsheets, and tabular JSON into valid Foundational Era BEJSON 104a or Integrity Era Format 105a documents. Features automated column type inference, boundary whitespace sanitization (Policy Section 10.9), O(1) field map caching, and atomic POSIX file replacement. Use when importing external tabular data into BEJSON, migrating SQLite databases to MFDB, converting CSV tables to BEJSON, or modernizing flat storage. Do NOT use for editing existing BEJSON tables (use bejson-104-core), black-box schema validation (use bejson-104-validator), upgrading 104 to 105 files in-place (use bejson-105-upgrade-automator), or application code AST refactoring (use bejson-codebase-refactor).
---

# bejson-migration-pipeline (Layer 3 Legacy Database & Tabular Ingestion Service)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & Linux
- **Architectural Tier**: Layer 3 (L3) Automation & Service Pipeline
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `2c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f`
- **Version**: `1.0.0`
- **Upstream Collaborator**: `planning-schema-planner` (Layer 5)
- **Downstream Collaborators**: `bejson-104-validator` (Layer 2), `bejson-104-core` (Layer 1)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Migrating legacy SQLite database tables (`.db`, `.sqlite`, `.sqlite3`) into standalone BEJSON 104a files or multi-file MFDB entities.
- Converting CSV or TSV spreadsheets into structured BEJSON tabular formats.
- Automatically inferring schema column types (`integer`, `number`, `boolean`, `string`) from legacy row samples.
- Sanitizing boundary-layer whitespace from dictionary keys and string values prior to serialization.
- Logging migration transactions and SHA-256 hashes into BEJSON 104a audit registries.

### When NOT to Use:
- Do NOT use for basic CRUD operations on pre-existing BEJSON tables (use `bejson-104-core`).
- Do NOT use for schema validation and E01-E12 structural error checks (use `bejson-104-validator`).
- Do NOT use for upgrading valid 104 files to Format 105 in-place (use `bejson-105-upgrade-automator`).
- Do NOT use for refactoring Python or TypeScript application codebases (use `bejson-codebase-refactor`).

---

## 2. Ingestion Pipeline Architecture

`bejson-migration-pipeline` functions at Layer 3 to provide automated ETL ingress:

```
[External Data: SQLite / CSV / JSON]
                 |
                 v
[Layer 3 bejson-migration-pipeline (This Skill)]
    - Extracts headers and samples values
    - Infers canonical 4-primitive vocabulary (POL-002)
    - Performs boundary sanitization (Policy Sec 10.9)
    - Compiles O(1) field_map cache
    - Commits via atomic POSIX replace (.tmp -> rename)
                 |
                 v
[Layer 2 Validation Gate (bejson-104-validator / bejson-105-validator)]
                 |
                 v
[Layer 1 Invariant Persistence (storage/mfdb/)]
```

---

## 3. Tool Execution via CLI

The migration service is driven by `scripts/bejson_migrator.py`:

### Step 1: Migrate a CSV Spreadsheet to BEJSON 104a
```bash
python3 scripts/bejson_migrator.py \
    data/customers.csv \
    --output storage/mfdb/customers.104a.bejson \
    --record-type "CustomerRecord" \
    --manifest assets/migration_registry.104a.bejson
```

### Step 2: Extract and Migrate a SQLite Table
```bash
python3 scripts/bejson_migrator.py \
    database.sqlite \
    --table "orders" \
    --output storage/mfdb/orders.104a.bejson \
    --format-version 104a
```

### Step 3: Upgrade Ingestion to Integrity Era Format 105a
```bash
python3 scripts/bejson_migrator.py \
    data/transactions.csv \
    --output storage/mfdb/transactions.105a.bejson \
    --format-version 105a
```

---

## 4. Headless agy Execution Protocol

When invoking via Antigravity CLI, enforce `--sandbox` isolation:

```bash
agy --sandbox -p "Migrate SQLite database legacy_data.db table 'audit_events' to BEJSON 104a at storage/mfdb/audit_events.104a.bejson using bejson-migration-pipeline"
```

Negative Constraints: Zero conversational filler. Never overwrite destination files without atomic write confirmation.

---

## 5. BEJSON Manifest Integration (Format 104a)

Migration jobs are recorded in `assets/migration_registry.104a.bejson`:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["MigrationRecord"],
  "Fields": [
    {"name": "migration_id",          "type": "string"},
    {"name": "source_format",         "type": "string"},
    {"name": "source_path",           "type": "string"},
    {"name": "target_format",         "type": "string"},
    {"name": "target_path",           "type": "string"},
    {"name": "rows_migrated",         "type": "integer"},
    {"name": "columns_count",         "type": "integer"},
    {"name": "status",                "type": "string"},
    {"name": "sha256_hash",           "type": "string"},
    {"name": "migration_timestamp",   "type": "string"}
  ],
  "Values": []
}
```

In runtime operations, fields are accessed dynamically via `field_map`:
```python
field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}
target_path = row[field_map["target_path"]]
```
