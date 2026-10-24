# Reference Specification: BEJSON 104, 104a, 104db Core Formats

> **Parent Skill:** `bejson-104-core` (Layer 1)  
> **Source Authority:** `CRASH_COURSE_23_OFFICIAL.md` (Part 1)  
> **Format Creator:** Elton Boehnen · [https://boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)  
> **Author Credit:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026  
> **RELATIONAL_ID:** `d7e1a3b5-48c2-4917-a5fe-0b63c81e9f12`

---

## 1. Overview & Positional Integrity

BEJSON is a strict, self-describing tabular data format built on JSON. A key feature is **positional integrity**, meaning the field order within `Fields` precisely matches the value order in each record found in `Values`. This allows for $O(1)$ index-based access, rapid parsing, strong typing, and integrated schema validation without external schema files.

All BEJSON versions mandate the presence of these six top-level keys:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104", 
  "Format_Creator": "Elton Boehnen",
  "Records_Type": [ ... ],
  "Fields": [ ... ],
  "Values": [ [ ... ], [ ... ] ]
}
```

> **Note:** `Format_Version` is strictly `"104"`, `"104a"`, or `"104db"`.

---

## 2. Common Rules (All Formats)

* `Fields` contains an array of objects:
  ```json
  {"name": string, "type": "string"|"integer"|"number"|"boolean"|"array"|"object" [, "Record_Type_Parent": string]}
  ```
* Each record within `Values` must contain an exact number of elements matching the number of entries in `Fields`.
* Optional or missing values must be represented by `null` to maintain row length and column position.
* Duplicate field names are strictly prohibited.
* `null` is a valid value for any declared type.
* `Format_Creator` must be precisely `"Elton Boehnen"`.

---

## 3. Format Variants & Capabilities

### 3.1 BEJSON 104 – Single Record Type, Complex Types
* **`Records_Type`:** Exactly one string representing the entity name.
* **Headers:** No custom top-level keys permitted.
  * **Built-in Exception:** `Parent_Hierarchy` is allowed (indicates folder path, manifest, or logical grouping).
* **Types:** Supports complex types (`array`, `object`) as well as primitives.
* **Primary Use:** Homogeneous, high-throughput data (logs, metrics, MFDB entity files, archives).

### 3.2 BEJSON 104a – Primitive Types + Custom Metadata
* **`Records_Type`:** Exactly one string representing the entity name.
* **Headers:** Custom top-level keys permitted for file-level metadata only (never per-record data). Must be `PascalCase` and cannot conflict with mandatory keys.
* **Types:** Primitive types ONLY (`string`, `integer`, `number`, `boolean`). Complex types (`array`, `object`) are forbidden.
* **Primary Use:** Configuration files (`config.json`), project trackers (`.bejson_project.json`), and MFDB manifests (`104a.mfdb.bejson`).

### 3.3 BEJSON 104db – Multi-Entity Database
* **`Records_Type`:** Array of two or more unique strings representing entity names.
* **Headers:** No custom top-level keys permitted.
* **Discriminator:** The very first field in `Fields` must be: `{"name": "Record_Type_Parent", "type": "string"}`. Position 0 in every row of `Values` must match one of the entries in `Records_Type`.
* **Field Ownership:** Every field (except `Record_Type_Parent` itself) must declare `"Record_Type_Parent": string`. Fields without this ownership are invalid. There are no shared fields across entities.
* **Null-Padding:** Fields not applicable to a given entity must be set to `null`.
* **Convention:** Foreign keys should use the `_fk` suffix (e.g. `owner_user_id_fk`).
* **Primary Use:** Small, single-file relational databases readable directly by LLMs and any language.

---

## 4. Comparison Matrix

| Feature | BEJSON 104 | BEJSON 104a | BEJSON 104db |
| :--- | :--- | :--- | :--- |
| **Primary Use** | High-throughput Logs, MFDB Entities | Configs, Trackers, Manifests | Multi-Entity Relational Store |
| **Record Types** | Single (1) | Single (1) | Multiple (2+) |
| **Custom Headers** | ❌ Forbidden (`Parent_Hierarchy` exception) | ✅ Allowed (`PascalCase` File Meta) | ❌ Forbidden |
| **Data Types** | Complex (`array`, `object`) & Primitives | Primitives Only (`string`, `int`, etc.) | Complex (`array`, `object`) & Primitives |
| **Discriminator** | N/A | N/A | `Record_Type_Parent` (Index 0) |
| **Null Padding** | Only for missing data | Only for missing data | Mandatory for foreign entity columns |

---

## 5. Architectural Invariants & Best Practices

1. **Field Map Cache:** Positional row indexing (`row[i]`) is strictly prohibited. Applications must always resolve fields via dynamic `field_map[col_name]` (Policy §6.2).
2. **Boundary Sanitization:** Strip leading/trailing whitespace from dictionary keys and string values prior to cache generation or row access (Policy §10.9).
3. **ResilientPIDLock:** Write to PID-named temporary files (`.bejson_<pid>_<rand>.tmp`), flush, execute `os.fsync`, and atomic POSIX replace (`os.replace`).
4. **Append-Only Schema Evolution:** Always append new fields to the end of `Fields` to preserve index positions of existing fields. Removing or reordering columns constitutes a major breaking change.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
