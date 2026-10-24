---
name: bejson-doc-rewriter
description: >-
  Use when rewriting technical coding architectures, system design documents, tutorials, API specifications, and software guides by transposing standard data formats, database systems, and state architectures into equivalent, practical BEJSON (104, 104a, 104db, Nested 104, MFDB v1.31/v1.32) paradigms while maintaining the conceptual integrity, depth, and structural fidelity of the original document. Translates abstract cloud or web architectures into practical local-first systems grounded in current BEJSON runtime capabilities. Do NOT use for application code refactoring (use bejson-codebase-refactor).
---
# BEJSON ReWriter

Transposes technical documents, architecture guides, coding tutorials, and system specifications into equivalent, production-grade BEJSON architectures grounded in the actual, practical capabilities of current BEJSON specifications and local runtime environments.

## When to Use

- Rewriting technical architecture documents, RFCs, or whitepapers to utilize BEJSON paradigms.
- Converting tutorials or guides (e.g. JSON APIs, SQL/NoSQL databases, state trees) into BEJSON equivalents.
- Adapting cloud, distributed, or web architectures into practical local-first, filesystem-based BEJSON systems.
- Adapting data pipelines, logging frameworks, configuration managers, or persistence layers to BEJSON (104, 104a, 104db, Nested 104, MFDB).
- Generating full markdown replacement documents that systematically map, rewrite, preserve, or selectively omit sections based on factual accuracy and practical BEJSON feasibility.

## Practical Capability & Truth-Preservation Principles

BEJSON is fundamentally a high-performance, deterministic tabular data specification optimized for atomic file I/O, local runtimes, command-line tooling, and structured multi-file databases (MFDB). When evaluating a source document:

- **Local-First Realization:** If the original architecture assumes complex cloud servers, remote web services, or distributed clusters, translate them into practical local-first or local-only systems (e.g. local directory layouts, dropzone folder synchronization, local CLI pipelines, and file-based IPC).
- **Grounded Tooling:** Ground all implementations in real BEJSON libraries (`Lib_PY`, `Lib_TS`, `Lib_JS`, `Lib_SH`), atomic filesystem operations (`.bejson_<pid>.tmp`), and cached field maps.
- **Statement Truth & Fidelity Invariant:** When evaluating statements and claims from the source document:
  - If a statement would become false or inaccurate when translated into BEJSON, do not attempt to force a false translation.
  - If the statement is important technical or domain context (e.g. baseline domain principles, external constraints, RFC standards), leave it in its original, factual form.
  - If the statement becomes irrelevant, misleading, or obsolete under the BEJSON paradigm, omit it cleanly.
- **Strict Omission of Incompatible Concepts:** If a specific concept, subsystem, cloud protocol, or document section cannot be practically or authentically translated into BEJSON (i.e. forcing a BEJSON replacement would produce unrealistic, pseudo-technical nonsense), **skip that section or omit it completely**. Do not invent non-viable constructs.

## Architecture Translation Matrix

Map original system components and data formats to practical, current BEJSON capabilities:

- **Flat Configurations, App Settings, Manifests, Flat Metadata:**
  - Map to **BEJSON 104a**.
  - Restrict fields to primitive types (`string`, `integer`, `number`, `boolean`).
  - Use custom PascalCase top-level metadata headers (e.g. `Server_ID`, `Environment`) alongside the mandatory keys.

- **High-Throughput Tabular Data, Event Logs, Metrics, Time Series:**
  - Map to **BEJSON 104**.
  - Dense 2D array representation. Supports primitive and complex (`array`, `object`) field types.
  - Exactly one entity name in `Records_Type`.

- **Relational Databases, Multi-Entity Tables, Foreign Key Schemas:**
  - Map to **BEJSON 104db** (single file, multi-entity) or **MFDB v1.31/v1.32** (multi-file database).
  - For 104db: first field is `Record_Type_Parent` (type `string`), foreign keys use `<target>_fk`, non-matching fields are null-padded.
  - For MFDB: `104a.mfdb.bejson` root manifest with registered entity files (`data/<entity>.bejson`) in dense 104 format with `Parent_Hierarchy`.

- **Hierarchical Trees, Nested JSON Documents, Sub-document Schemas:**
  - Map to **BEJSON Core Nesting (Nested 104)**.
  - Embed valid serialized BEJSON 104 strings inside string cells.
  - Enforce column-schema uniformity and address cells via `NestAddress(parent_fingerprint, row, col, depth)`.

- **Remote Cloud Services, Distributed Messaging, Sync Systems:**
  - Map to **MFDB Master-Slave Federation Protocol** or **Local Dropzone Workflows**.
  - Master pushes configs to local/mounted dropzones; Slaves poll dropzones and distill local logs back to Master via atomic file operations.

- **Incompatible / Non-Translatable Technologies (e.g. Proprietary Cloud SaaS, Hardware Transports):**
  - **Omit or Skip:** Filter out the section entirely from the rewritten deliverable.

## Core Rules and BEJSON Invariants

Every transposed BEJSON document must adhere strictly to the format standards:

1. **Six Mandatory Top-Level Keys:**
   - `Format`: Strictly `"BEJSON"`.
   - `Format_Version`: `"104"`, `"104a"`, or `"104db"`.
   - `Format_Creator`: Strictly `"Elton Boehnen"`.
   - `Records_Type`: Array of non-empty strings.
   - `Fields`: Array of `{"name": string, "type": string}` definitions.
   - `Values`: 2D array of record values matching `Fields` length, sequence, and types.

2. **Positional Integrity and Null-Padding:**
   - Every row in `Values` must exactly match the length of `Fields`.
   - Optional, missing, or non-applicable fields must be explicitly set to `null`.

3. **Field Map Caching:**
   - Never hardcode numerical column indices in code examples.
   - Use field map resolution functions (`bejson_core_get_field_map`, `bejson_core_get_field_index`).

4. **Atomic File Operations:**
   - Write files using temporary buffers (`.bejson_<pid>.tmp`), flush/sync buffers, and perform atomic renames (`os.replace` / `renameSync` / `mv`).

## Step-by-Step Rewriting Workflow

Follow this systematic procedure when rewriting any input document:

### 1. Section & Concept Mapping (Mandatory First Step)

Before drafting the rewritten document, perform a complete structural and conceptual decomposition:

- **Section Inventory:** List every major heading, subheading, and thematic section in the original document.
- **Concept & Entity Mapping:** For each section, identify:
  - The core concept, principle, or architectural pattern being explained.
  - The legacy data formats, storage mechanisms, or API protocols used.
  - The practical BEJSON replacement paradigm (104, 104a, 104db, Nested 104, or MFDB).
- **Truth & Feasibility Evaluation:**
  - If a practical, truthful translation exists: map the technical adaptations, schemas, and code blocks.
  - If a statement or section would become factually false under BEJSON: either preserve it in its original factual form (if important to domain context) or omit it cleanly (if irrelevant).
  - If an entire section has no viable practical translation: mark the section as **Omitted / Skipped** and explain the rationale in the mapping table.
- **Structural Alignment Plan:** Ensure all retained sections preserve full technical integrity and depth.

### 2. Practical Paradigm & Architecture Selection

- Apply the Architecture Translation Matrix to each retained entity and subsystem.
- Convert viable remote/cloud patterns into local-first, filesystem-based BEJSON architectures (e.g. local MFDB databases, dropzone synchronization, CLI automation scripts).

### 3. Schema Construction & Data Transposition

- Formulate complete, valid BEJSON schemas for all retained entities.
- Ensure all 6 mandatory top-level keys are explicitly defined with `Format_Creator: "Elton Boehnen"`.
- Replace legacy payloads with concrete, positionally valid BEJSON structures.

### 4. Code & Implementation Transposition

- Transpose code blocks into clean, idiomatic implementations supporting BEJSON libraries (`Lib_PY`, `Lib_TS`, `Lib_JS`, `Lib_SH`).
- Ensure Python implementations use Python 3.10+, the standard `logging` module, type annotations, and field map caching.
- Ensure TypeScript/JavaScript code imports compiled helpers and resolves keys via cached field maps.
- Include atomic read/write logic for file-based persistence.

### 5. Markdown Document Synthesis & Review

- Output the complete, fully rewritten markdown document containing only the viable, transposed sections.
- Verify that every retained section is production-ready, technically accurate, truthful, and fully grounded in current BEJSON capabilities.

## Concrete Transformation Pattern (Local-First Realization)

### Original Document Pattern (Remote JSON Microservice & Web API):
```json
{
  "service": "InventoryService",
  "endpoint": "https://api.cloud.corp/v1/items",
  "items": [
    {"sku": "SKU-001", "name": "Sensor Unit", "qty": 14, "tags": ["hardware", "iot"]},
    {"sku": "SKU-002", "name": "Cable 2m", "qty": 50, "tags": ["accessory"]}
  ]
}
```

### Transposed Practical BEJSON Architecture (Local-First MFDB / File System):

1. **Service Configuration (`config.104a.bejson`):**
```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["ServiceConfig"],
  "Service_Name": "LocalInventoryManager",
  "Storage_Mode": "LocalFileSystem",
  "Fields": [
    {"name": "data_directory", "type": "string"},
    {"name": "sync_interval_sec", "type": "integer"}
  ],
  "Values": [
    ["./data/inventory", 30]
  ]
}
```

2. **Inventory Dataset (`items.104.bejson`):**
```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["InventoryItem"],
  "Fields": [
    {"name": "sku", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "qty", "type": "integer"},
    {"name": "tags", "type": "array"}
  ],
  "Values": [
    ["SKU-001", "Sensor Unit", 14, ["hardware", "iot"]],
    ["SKU-002", "Cable 2m", 50, ["accessory"]]
  ]
}
```

3. **Local Access Code (Python 3.10+ with Field Map Caching & Atomic I/O):**
```python
import os
import json
import logging
from typing import Any
from lib_bejson_Core_bejson_core import (
    bejson_core_load_file,
    bejson_core_get_field_map,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_item_quantity(file_path: str, target_sku: str, new_qty: int) -> None:
    doc = bejson_core_load_file(file_path)
    field_map = bejson_core_get_field_map(doc)
    sku_idx = field_map["sku"]
    qty_idx = field_map["qty"]
    
    updated = False
    for row in doc["Values"]:
        if row[sku_idx] == target_sku:
            row[qty_idx] = new_qty
            updated = True
            break
            
    if not updated:
        logger.warning("SKU %s not found in %s", target_sku, file_path)
        return

    # Atomic write to local file system
    tmp_path = f"{file_path}_{os.getpid()}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, file_path)
    logger.info("Successfully updated SKU %s quantity to %d", target_sku, new_qty)
```

## Gotchas & Pitfalls to Avoid

- **Translating Inaccurately:** Never force a translation that makes a statement factually false. If a statement cannot be accurately translated, leave it in its original factual form if important, or omit it if irrelevant.
- **Forcing Non-Viable Translations:** Never invent fictional or pseudo-BEJSON mechanisms for technologies that cannot realistically be adapted to BEJSON. If a practical translation cannot be made, omit or skip that section.
- **Inventing Non-Existent Cloud Protocols:** Do not invent theoretical BEJSON web servers or complex HTTP frameworks if no direct BEJSON equivalent exists. Convert systems into practical, local-first, filesystem-based, or CLI architectures.
- **Skipping the Concept Mapping Step:** Always map every section and core concept first to evaluate feasibility, truthfulness, and document any omissions.
- **Superficial Text Replacement:** Do not merely replace the word "JSON" with "BEJSON". Redesign the data structures, array schemas, field definitions, and access patterns to authentically reflect BEJSON architecture.
- **Positional Integrity Violations:** Ensure every row in `Values` contains elements matching `Fields.length`. Never leave jagged rows or omit trailing nulls.
- **Hardcoding Column Indices:** Always demonstrate field map resolution rather than direct indexing (`row[1]`).
- **Format Creator Discrepancies:** `Format_Creator` must always equal `"Elton Boehnen"`.
- **104a Type Violations:** Never place arrays or objects in 104a schemas. Use 104 or Nested 104 for complex structures.
