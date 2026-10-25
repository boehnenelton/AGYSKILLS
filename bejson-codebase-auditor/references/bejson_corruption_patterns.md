# BEJSON Data Corruption and Structural Mismatch Patterns

This reference manual documents standard failure modes, schema divergence patterns, and data corruption scenarios detected by `bejson-codebase-auditor`.

---

## 1. Top-Level Header Invariants (BEJSON 104 / 104a)

A valid BEJSON document MUST contain the six canonical root keys:
1. `Format`: Exactly `"BEJSON"`.
2. `Format_Version`: Valid versions include `"104"`, `"104a"`, `"104db"`, `"105"`, `"105a"`, `"105db"`.
3. `Format_Creator`: Canonical creator `"Elton Boehnen"`.
4. `Records_Type`: Array of strings identifying the entity record types, e.g., `["ScriptConfig"]` or `["AuditFindings"]`.
5. `Fields`: Ordered array of field specifications, each defining at minimum `{"name": "...", "type": "..."}`.
6. `Values`: 2D array of record rows matching the length and order of `Fields`.

### 1.1 Row-Width Mismatch (`E_DATA_WIDTH_MISMATCH`)
Every row in `Values` must have exactly $N$ elements, where $N = \text{len}(\text{Fields})$.
- **Truncated Rows**: Missing trailing cells. Causes `IndexError` when accessing columns mapped near the end of the schema.
- **Overfilled Rows**: Extra trailing cells. Corrupts positional alignment when serialized or queried.
- **Root Cause**: Manual file edits, unescaped comma delimiters in CSV conversions, or schema modifications without migrating historical data rows.

### 1.2 Type Divergence (`E_DATA_TYPE_MISMATCH`)
Cell values must conform to declared schema types:
- `string`: String primitives (`"active"`, `"pending"`).
- `integer`: Discrete integers (`100`, `42`). Booleans (`True`/`False`) must not masquerade as integers.
- `float`: Floating point values or integers.
- `boolean`: Strict boolean primitives (`true`, `false`).
- `array`: JSON list structures.
- `object`: JSON dictionary structures.

---

## 2. Integrity Era Format 105 UUID Requirements

Integrity Era documents (`Format_Version` 105/105a/105db) enforce strict fingerprinting:
- **Field UUIDs (`E_DATA_105_MISSING_FIELD_UUID`)**: Every object inside `Fields` must contain a pre-compiled UUIDv4 in `field_uuid`.
- **Reserved Record UUIDs**: Row index 0 (or row index 1 for 105db) is strictly reserved for the row's unique `record_uuid`.
- **Tamper Resistance**: E95 Fail-on-Switch protection triggers if a 104 file is re-headered as 105 without compiling row checksums and field UUIDs.

---

## 3. Project Tracker Governance (Policy §4.6)

In `bejson_project.json`:
- `Project_GUID`: Must remain `"GUID_PLACEHOLDER"` until assigned exclusively by the dedicated registration tool (`$PROJECT_INDEX_ROOT/cli_project_register.py`).
- If `Is_Registered` is set to `true`, having an unassigned `GUID_PLACEHOLDER` constitutes a registration state contradiction (`E_DATA_UNRESOLVED_GUID`).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
