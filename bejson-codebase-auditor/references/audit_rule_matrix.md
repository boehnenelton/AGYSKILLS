# BEJSON Codebase Auditor - Diagnostic Rule Matrix

This document defines the diagnostic codes, categories, severity tiers, policy bindings, and remediation patterns enforced by `bejson-codebase-auditor`.

---

## 1. Diagnostic Code Registry

| Finding Code | Category | Severity | Policy Binding | Detection Target |
| :--- | :--- | :--- | :--- | :--- |
| `E_DATA_CORRUPT_JSON` | DATA_CORRUPTION | CRITICAL | RFC 8259 Standard | Malformed JSON syntax, truncated documents, syntax parse errors |
| `E_DATA_WIDTH_MISMATCH` | DATA_CORRUPTION | CRITICAL | Policy §6.2 | Row array length != `Fields` definition length in BEJSON `Values` |
| `E_DATA_FIELDS_NOT_LIST` | DATA_CORRUPTION | CRITICAL | Policy §4.4 | `Fields` top-level attribute is not a list of field specifications |
| `E_DATA_VALUES_NOT_LIST` | DATA_CORRUPTION | CRITICAL | Policy §4.4 | `Values` top-level attribute is not a 2D array of rows |
| `E_DATA_ROW_NOT_LIST` | DATA_CORRUPTION | CRITICAL | Policy §4.4 | Row entry in `Values` is not an array structure |
| `E_DATA_MISSING_HEADER` | DATA_CORRUPTION | HIGH | Policy §4.4 | Missing required BEJSON header (`Format`, `Format_Version`, `Fields`, etc.) |
| `E_DATA_MALFORMED_FIELD` | DATA_CORRUPTION | HIGH | Policy §4.4 | Field item is missing `'name'` or `'type'` dictionary attributes |
| `E_DATA_EMPTY_FIELD_NAME` | DATA_CORRUPTION | HIGH | Policy §4.4 | Field item has an empty or null name identifier |
| `E_DATA_DUPLICATE_FIELD` | DATA_CORRUPTION | HIGH | Policy §6.2 | Duplicate field name causing `field_map` index overwrite |
| `E_DATA_105_MISSING_FIELD_UUID` | DATA_CORRUPTION | HIGH | Policy E90 | Format 105 document field missing mandatory `field_uuid` attribute |
| `E_DATA_UNRESOLVED_GUID` | DATA_CORRUPTION | HIGH | Policy §4.6 | `bejson_project.json` has `Is_Registered: true` with placeholder GUID |
| `E_DATA_TYPE_MISMATCH` | DATA_CORRUPTION | MEDIUM | Policy §4.4 | Cell value type does not conform to specified field schema type |
| `E_DATA_WHITESPACE_IN_FIELD_NAME` | DATA_CORRUPTION | MEDIUM | Policy §10.9 | Leading or trailing whitespace in field name definition |
| `E_DATA_CELL_WHITESPACE` | DATA_CORRUPTION | LOW | Policy §10.9 | Untrimmed boundary whitespace in text cell values |
| `E_LOGIC_RAW_INDEXING` | LOGIC_FLAW | CRITICAL | Policy §6.2 | Direct row[0] or record[1] numeric indexing without `field_map` |
| `E_LOGIC_JS_RAW_INDEXING` | LOGIC_FLAW | CRITICAL | Policy §6.2 | JavaScript row[0] direct indexing on BEJSON data |
| `E_LOGIC_HARDCODED_COL_OFFSET` | LOGIC_FLAW | HIGH | Policy §6.2 | Static column index constants (e.g., `COL_IDX = 0`) |
| `E_LOGIC_NON_ATOMIC_WRITE` | LOGIC_FLAW | HIGH | Policy §1.1 | Non-atomic `open(path, 'w')` on BEJSON files without `.tmp` + `os.replace` |
| `E_LOGIC_SILENT_EXCEPTION` | LOGIC_FLAW | HIGH | Policy §7.3 | Empty `except: pass` suppressing exceptions without logging |
| `E_LOGIC_HARDCODED_HOST_PATH` | LOGIC_FLAW | HIGH | Policy §4.1 / §7.3 | Hardcoded host storage paths (`/storage/...`, `/data/...`) in runtime logic |
| `E_LOGIC_HARDCODED_BASH_PATH` | LOGIC_FLAW | HIGH | Policy §4.2 | Hardcoded absolute paths in shell scripts without `get_script_path` |
| `E_LOGIC_BASH_RAW_OFFSET` | LOGIC_FLAW | MEDIUM | Policy §6.2 | Shell stream column slicing (`cut`, `awk`) on BEJSON payloads |
| `E_LOGIC_PRINT_CALL` | LOGIC_FLAW | MEDIUM | Policy §7.3 | Built-in `print()` used in application code instead of `logging` module |
| `E_NAMING_SINGLE_LETTER` | NAMING_CONVENTION | LOW | Policy §6.1 | Single-letter variable identifiers (`i`, `j`, `x`, `p`, etc.) |
| `E_NAMING_CRYPTIC` | NAMING_CONVENTION | LOW | Policy §6.1 | Ambiguous variable names (`tmp`, `val`, `res`, `arr`, `obj`, `data`) |
| `E_NAMING_VAGUE_FUNCTION` | NAMING_CONVENTION | LOW | Policy §6.1 | Vague function names (`process`, `handle`, `run`, `do_stuff`) |
| `E_TAXONOMY_UNPREFIXED_FIELD` | TAXONOMY | INFO | Policy §6.1 / §10.2 | Entity schema fields lacking canonical entity prefix |
| `E_TAXONOMY_UNSTRUCTURED_DATA` | TAXONOMY | INFO | Policy §4.4 | Unnormalized JSON array-of-objects candidate for BEJSON compaction |

---

## 2. Severity Scoring & Action Hierarchy

- **CRITICAL (Weight 10)**: Immediate fatal corruption or schema violation. Code will crash at runtime, lose data, or corrupt storage.
- **HIGH (Weight 5)**: High-risk architectural anti-pattern. Missing schema metadata, insecure non-atomic disk operations, or path portability breakage.
- **MEDIUM (Weight 2)**: Standard compliance divergence. Missing sanitization, untrimmed whitespace, improper logging, or loose typing.
- **LOW (Weight 1)**: Naming convention issues. Single-letter or ambiguous variables violating Policy §6.1.
- **INFO (Weight 0)**: Optimization opportunities. Normalizing legacy JSON arrays into BEJSON 104a or adding entity prefixes.

---

## 3. Remediation Patterns

### 3.1 Resolving Raw Positional Indexing (`E_LOGIC_RAW_INDEXING`)
```python
# Non-compliant:
def extract_email(row: list) -> str:
    return row[2]  # Direct index

# Compliant (Policy §6.2 & §10.9):
def extract_email(fields: list[dict], row: list) -> str:
    field_map = {f["name"].strip(): idx for idx, f in enumerate(fields)}
    col_idx = field_map["user_email"]
    cell_val = row[col_idx]
    return cell_val.strip() if isinstance(cell_val, str) else cell_val
```

### 3.2 Resolving Non-Atomic Writes (`E_LOGIC_NON_ATOMIC_WRITE`)
```python
# Non-compliant:
with open("data/store.bejson", "w", encoding="utf-8") as f:
    json.dump(doc, f)

# Compliant (Atomic Write Protocol):
target_path = Path("data/store.bejson")
temp_path = target_path.with_suffix(".tmp")
with open(temp_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(temp_path, target_path)
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
