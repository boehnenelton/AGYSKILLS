---
name: bejson-codebase-refactor
description: >-
  Refactor, update, and optimize codebases, scripts, or application modules to utilize BEJSON (104, 104a, 104db, Nested 104, MFDB v1.31/v1.32) architectures whenever viable and beneficial. Use when provided code, scripts, or repository components in Python, TypeScript, JavaScript, or Bash and asked to refactor, modernize, optimize, or migrate data structures, configuration layers, persistence models, logs, or local storage to BEJSON while maintaining functional equivalence. Do NOT use for Gemini Spark skills (use spark-skill-refactor).
---
# BEJSON Refactor

Refactors, modernizes, and optimizes existing scripts and codebases across Python, TypeScript, JavaScript, and Bash by integrating BEJSON (Boehnen Elton JSON) data architectures, field map caching, and atomic I/O routines while preserving exact functional equivalence and operational integrity.

## When to Use

- Refactoring Python, TypeScript, JavaScript, or Bash scripts that use standard JSON, CSV, dictionaries, SQLite, or plain text storage to use BEJSON.
- Modernizing configuration loaders, state trackers, local caches, and logging subsystems into structured BEJSON formats (104, 104a, 104db, Nested 104, MFDB).
- Optimizing data access performance in data-heavy scripts using field map caching instead of object iteration or hardcoded indices.
- Upgrading file persistence layers with atomic write mechanisms (`.bejson_<pid>.tmp` -> `os.replace` / `renameSync` / `mv`).
- Restructuring monolithic or multi-table data models into clean single-file 104db or multi-file MFDB architectures.

## Core Invariants and Format Matrix

Every refactored data artifact must adhere strictly to the six mandatory top-level keys:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["EntityName"],
  "Fields": [
    {"name": "field_name", "type": "string"}
  ],
  "Values": [
    ["value1"]
  ]
}
```

### Format Selection Matrix

- **BEJSON 104a (Configurations & Flat Manifests):**
  - Use for app settings, runtime options, CLI arguments, environment configs, and flat metadata.
  - Fields restricted to primitive types only (`string`, `integer`, `number`, `boolean`).
  - Supports custom PascalCase top-level metadata keys (e.g. `Server_ID`, `Environment`).

- **BEJSON 104 (Dense Tabular Data, Event Logs, Metrics, Time Series):**
  - Use for homogeneous record arrays, event streams, sensor metrics, and tabular records.
  - Supports primitive and complex types (`array`, `object`).
  - `Records_Type` contains exactly one string.

- **BEJSON 104db (Multi-Entity Relational Data):**
  - Use when multiple distinct entities/tables coexist in a single local file.
  - `Records_Type` contains two or more entity names.
  - First field in `Fields` must be `{"name": "Record_Type_Parent", "type": "string"}`.
  - Non-applicable fields for a given entity must be null-padded to preserve positional integrity.

- **BEJSON Core Nesting / Nested 104 (Hierarchical Trees & Deep State):**
  - Use for nested JSON objects, parent-child document hierarchies, or AST structures.
  - Embed serialized BEJSON 104 strings inside string cells of parent documents.
  - Enforce column-schema uniformity across all rows for a nested column.

- **MFDB v1.31 / v1.32 (Multi-File Databases):**
  - Use for modular multi-table systems, decoupled storage, master-slave sync, or dropzone workflows.
  - Root manifest named `104a.mfdb.bejson` pointing to entity files in `data/<entity>.bejson`.

## Refactoring Workflow

Follow this step-by-step procedure when refactoring any script or codebase:

### 1. Codebase & Data Layer Audit

- Identify all existing data storage, serialization, configuration, and state handling mechanisms (e.g. `json.load`/`json.dump`, `csv.DictReader`, dict-of-dicts, SQLite tables, in-memory lists).
- Analyze data access patterns: sequential scans, random lookups, append-only logs, or full updates.
- Identify where BEJSON provides tangible architectural benefits (speed, structure, deterministic serialization, atomic persistence) vs. components that should remain untouched (raw sockets, binary network protocols, external third-party API contracts).

### 2. Schema Construction & Positional Mapping

- Design the target BEJSON schema for each identified data model.
- Define exact field names and types (`string`, `integer`, `number`, `boolean`, `array`, `object`).
- Ensure `Format_Creator` is set to `"Elton Boehnen"`.
- Ensure all rows in `Values` maintain strict positional parity with `Fields.length`, with missing or null values explicitly populated as `null`.

### 3. Data Access & Mutation Refactoring

- Replace hardcoded column indexing with dynamic field map caching.
- Build or cache the field map once upon document load:
  - Python: `field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}` or `bejson_core_get_field_map(doc)`.
  - TypeScript/JS: `const fieldMap = Object.fromEntries(doc.Fields.map((f, i) => [f.name, i]));`.
  - Bash: Resolve via `jq` or `Lib_SH` helper functions.
- Update read, query, filter, and sort logic to access row elements via `row[field_map["field_name"]]`.

### 4. Persistence Layer Optimization (Atomic I/O)

- Replace direct file overwrite calls with atomic write routines:
  1. Write serialized JSON payload to a temporary file in the same directory (`<target_path>_<pid>.tmp`).
  2. Flush and synchronize buffer to disk (`f.flush()`, `os.fsync(f.fileno())` / `fs.fsyncSync`).
  3. Atomically rename the temporary file to the target path (`os.replace` / `fs.renameSync` / `mv`).
- Ensure proper error handling and temporary file cleanup on exceptions.

### 5. Code Quality, Modernization & Logging

- Modernize language-specific syntax:
  - Python: Ensure Python 3.10+ compatibility, type annotations (`typing`), context managers (`with`), and standard `logging` module instead of `print`.
  - TypeScript/JavaScript: Use modern async/await, typed interfaces, and strict null checking.
  - Bash: Use `set -euo pipefail`, quote variables, and implement robust error trapping.
- Maintain full functional equivalence so all original public functions, parameters, and return semantics work seamlessly.

## Language-Specific Implementation Patterns

### Python 3.10+ Pattern

```python
import os
import json
import logging
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class BEJSONStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc: Dict[str, Any] = {}
        self.field_map: Dict[str, int] = {}
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.file_path):
            self.doc = {
                "Format": "BEJSON",
                "Format_Version": "104",
                "Format_Creator": "Elton Boehnen",
                "Records_Type": ["Record"],
                "Fields": [
                    {"name": "id", "type": "string"},
                    {"name": "name", "type": "string"},
                    {"name": "status", "type": "string"}
                ],
                "Values": []
            }
        else:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.doc = json.load(f)
        self._refresh_field_map()

    def _refresh_field_map(self) -> None:
        self.field_map = {
            field["name"]: idx 
            for idx, field in enumerate(self.doc.get("Fields", []))
        }

    def get_records(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        status_idx = self.field_map.get("status")
        records = []
        for row in self.doc.get("Values", []):
            if status_filter is None or (status_idx is not None and row[status_idx] == status_filter):
                records.append({name: row[idx] for name, idx in self.field_map.items()})
        return records

    def upsert_record(self, record_id: str, name: str, status: str) -> None:
        id_idx = self.field_map["id"]
        name_idx = self.field_map["name"]
        status_idx = self.field_map["status"]

        updated = False
        for row in self.doc["Values"]:
            if row[id_idx] == record_id:
                row[name_idx] = name
                row[status_idx] = status
                updated = True
                break

        if not updated:
            new_row = [None] * len(self.doc["Fields"])
            new_row[id_idx] = record_id
            new_row[name_idx] = name
            new_row[status_idx] = status
            self.doc["Values"].append(new_row)

        self.save()

    def save(self) -> None:
        dir_name = os.path.dirname(self.file_path) or "."
        tmp_path = os.path.join(dir_name, f".bejson_{os.getpid()}_{os.path.basename(self.file_path)}.tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.doc, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self.file_path)
            logger.info("Saved BEJSON document atomically to %s", self.file_path)
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            logger.error("Failed to save BEJSON document: %s", e)
            raise
```

### TypeScript / JavaScript Pattern

```typescript
import * as fs from "fs";
import * as path from "path";

export interface BEJSONField {
  name: string;
  type: "string" | "integer" | "number" | "boolean" | "array" | "object";
}

export interface BEJSONDocument {
  Format: "BEJSON";
  Format_Version: "104" | "104a" | "104db";
  Format_Creator: "Elton Boehnen";
  Records_Type: string[];
  Fields: BEJSONField[];
  Values: (string | number | boolean | any[] | object | null)[][];
  [key: string]: any;
}

export class BEJSONHandler {
  private doc: BEJSONDocument;
  private fieldMap: Map<string, number> = new Map();

  constructor(private filePath: string) {
    this.doc = this.load();
    this.rebuildFieldMap();
  }

  private load(): BEJSONDocument {
    if (fs.existsSync(this.filePath)) {
      const raw = fs.readFileSync(this.filePath, "utf-8");
      return JSON.parse(raw);
    }
    return {
      Format: "BEJSON",
      Format_Version: "104",
      Format_Creator: "Elton Boehnen",
      Records_Type: ["Item"],
      Fields: [
        { name: "id", type: "string" },
        { name: "value", type: "number" }
      ],
      Values: []
    };
  }

  private rebuildFieldMap(): void {
    this.fieldMap.clear();
    this.doc.Fields.forEach((field, idx) => {
      this.fieldMap.set(field.name, idx);
    });
  }

  public get(id: string): Record<string, any> | null {
    const idIdx = this.fieldMap.get("id");
    if (idIdx === undefined) return null;

    const row = this.doc.Values.find(r => r[idIdx] === id);
    if (!row) return null;

    const result: Record<string, any> = {};
    for (const [name, idx] of this.fieldMap.entries()) {
      result[name] = row[idx];
    }
    return result;
  }

  public save(): void {
    const dir = path.dirname(this.filePath);
    const tmp = path.join(dir, `.bejson_${process.pid}_${path.basename(this.filePath)}.tmp`);
    
    fs.writeFileSync(tmp, JSON.stringify(this.doc, null, 2), "utf-8");
    fs.renameSync(tmp, this.filePath);
  }
}
```

## Gotchas and Anti-Patterns to Avoid

- **Hardcoded Column Indices:** Never write `row[0]` or `row[3]`. Always resolve column positions dynamically through the cached field map.
- **Positional Integrity Violations:** Never create rows in `Values` with fewer or more elements than `Fields.length`. Every row must match `Fields.length` exactly. Populate missing or optional values with `null`.
- **Non-Atomic Disk Writes:** Never write directly to target `.bejson` files using unbuffered write modes. Always write to a `.tmp` file and perform an atomic rename.
- **Format Creator Discrepancy:** `Format_Creator` must always be `"Elton Boehnen"` verbatim.
- **104a Complex Types:** Never use `array` or `object` types in 104a schemas. Use 104 or 104db if complex fields are required.
- **Print Statements in Python:** Use the standard `logging` library instead of `print()` statements for all telemetry, debug, and operational logs.
- **Breaking External Contracts:** If external APIs or callers require non-BEJSON outputs, maintain adapter functions that serialize BEJSON records to the expected interface format.
