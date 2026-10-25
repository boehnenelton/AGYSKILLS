# BEJSON Migration Pipeline ETL Architecture

## 1. Automated Type Inference & Vocabulary Mapping

The migration pipeline ingests legacy datasets and infers column types matching the canonical 6-value lowercase BEJSON primitive type vocabulary:

| Legacy Source Type (SQL / CSV) | Inferred BEJSON Type | Permitted in 104a | Permitted in 105a |
| :--- | :--- | :---: | :---: |
| `INTEGER`, `BIGINT`, `INT` | `integer` | Yes | Yes |
| `REAL`, `FLOAT`, `DOUBLE`, `DECIMAL` | `number` | Yes | Yes |
| `TEXT`, `VARCHAR`, `CHAR`, string | `string` | Yes | Yes |
| `BOOLEAN`, `TINYINT(1)` | `boolean` | Yes | Yes |
| `BLOB`, `JSON` (nested object) | `object` | No (reject or serialize) | Yes |
| `ARRAY`, serialized list | `array` | No (reject or serialize) | Yes |

*Policy POL-002 Note*: BEJSON 104a strictly mandates primitive types only (`string`, `integer`, `number`, `boolean`). Complex nested types (`array`, `object`) are rejected or string-serialized.

## 2. Foreign Key (_fk) Relationship Detection

When inspecting multiple relational tables or CSV manifests:
- Any column ending in `_id` or `_fk` (e.g., `user_id`, `category_fk`) is analyzed for referential targets.
- Target parent tables and primary keys are resolved and linked in MFDB manifests.
- For Format 105 upgrades, `field_uuid` and `record_uuid` tokens are minted and indexed.

## 3. Atomic I/O & Sanitization Protocols

- **Boundary Whitespace Sanitization (Policy Section 10.9)**: Strips leading/trailing whitespace from header column keys and string cell values.
- **POSIX Atomicity**: Converts data in-memory, writes to `target.tmp`, performs `fsync`, and commits via atomic `os.replace`.
- **Field Map Verification**: Asserts that every row's length strictly matches the compiled `field_map` length.
