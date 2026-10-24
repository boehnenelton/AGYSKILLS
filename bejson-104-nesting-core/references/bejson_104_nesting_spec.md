# Reference Specification: BEJSON Nested 104 Architecture

> **Parent Skill:** `bejson-104-nesting-core` (Layer 1)  
> **Source Authority:** `CRASH_COURSE_23_OFFICIAL.md` (Part 1, Core Nesting)  
> **Format Creator:** Elton Boehnen · [https://boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)  
> **Author Credit:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026  
> **RELATIONAL_ID:** `f1c830a2-6d4b-4835-97e0-2b19f07a4c98`

---

## 1. Principles of Core Nesting

BEJSON 104 allows deeply nested, validated tabular structures directly within individual cells via the `Core_Nesting` library (Error codes 130–159). This enables hierarchical, multi-level datasets while strictly preserving positional integrity.

* **Embedded 104 Documents:** A cell within a 104 document can contain a fully valid BEJSON 104 document (parsed as an object or serialized string). The nested document must include all six mandatory keys with `Format_Creator: "Elton Boehnen"` and `Format_Version: "104"`. There is no separate version identifier; it is simply 104 embedded within 104.
* **Implicit Foreign Keys:** The physical cell coordinate—defined by `NestAddress(parent_fp, row, col, depth)`—serves as the implicit foreign key, completely eliminating the need to declare manual relational foreign keys at nested levels.
* **Column-Schema Uniformity:** All nested documents residing within the same parent column must share identical field names, declared types, and sequence order. Any schema discrepancy triggers a hard `E134` validation error.
* **Dotted-Path Navigation:** Traversal of deeply nested tables uses standard dotted notation (`bejson_nesting_query`, e.g., `player_inventory[*].item_id`) across recursive depths.
* **Safe Mutation & Padding:** When mutating nested tables (`bejson_nesting_mutate`), the engine enforces append-only schema evolution and automatically null-pads existing records to preserve positional integrity.
* **Depth Safety Ceiling:** Hard ceiling of 16 recursive nesting depths (`NESTING_MAX_DEPTH = 16`).
* **Records_Type Convention:** The `Records_Type` in a nested document should match the parent field name in `PascalCase`.

---

## 2. Invariant Rules Summary

| Rule Code | Invariant | Description |
| :--- | :--- | :--- |
| **E130** | `E_NESTING_INVALID_DOC` | Nested cell payload is not a valid BEJSON 104 document |
| **E131** | `E_NESTING_MAX_DEPTH` | Nesting depth exceeds hard ceiling of 16 |
| **E134** | `E_NESTING_SCHEMA_MISMATCH` | Inconsistent schema among nested documents in the same column |
| **E135** | `E_NESTING_INVALID_ADDRESS` | Malformed `NestAddress` coordinate tuple |
| **E136** | `E_NESTING_MUTATION_COLLISION` | Non-append column modification during in-place mutation |

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
