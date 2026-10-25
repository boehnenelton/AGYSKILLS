# Efficiency & Redundancy Audit Taxonomy (Layer 2)

- **Version**: `1.0.0`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Verification Gate & Invariant Auditing)`
- **Binding**: `Policy §6.2, §10.6, §10.9, §12.1`
- **RELATIONAL_ID**: `5944e71e-ab7f-46a9-8cca-b811c7894406`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Diagnostic Code Specification

The efficiency auditor evaluates systems against eight standardized inefficiency and redundancy codes:

| Code | Canonical Identifier | Severity | Primary Target | Description | Remediation Protocol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EFF_01** | `EFF_01_DEAD_CODE` | `WARNING` | Python / JS / Bash | Unreferenced functions, dead modules, or unimported routines. | Move to `dev/dead_code.md` and excise from runtime. |
| **EFF_02** | `EFF_02_DUPLICATE_CODE_BLOCKS` | `WARNING` | Python / JS / TS | Identical or near-identical function bodies duplicated across modules. | Consolidate into canonical `lib/` or admin libraries. |
| **EFF_03** | `EFF_03_LINEAR_BEJSON_LOOKUP` | `CRITICAL` | Python / JS / Bash | Direct `row[i]` indexing or linear searches on BEJSON row arrays. | Compile and query via $O(1)$ `field_map` cache (§6.2). |
| **EFF_04** | `EFF_04_REDUNDANT_IO_CHURN` | `WARNING` | Python / Bash | Repeated file read/write operations inside loop constructs. | Batch mutations in memory; execute single atomic POSIX write. |
| **EFF_05** | `EFF_05_SUBPROCESS_THRASHING` | `CRITICAL` | Bash / Python | Repeated shell command spawning (`jq`, `cat`, `curl`, `agy`) inside loops. | Replace with pipeline streaming, single-pass filters, or internal APIs. |
| **EFF_06** | `EFF_06_CONTEXT_PROMPT_BLOAT` | `CRITICAL` | SKILL.md / Presets | Manifests exceeding the 500-line budget or verbose fluff copy. | Enforce 3-Stage Progressive Disclosure; move specs to `references/`. |
| **EFF_07** | `EFF_07_DUPLICATE_ASSET_STORAGE` | `OPTIMIZATION` | Filesystem Assets | Identical SHA-256 byte digests duplicated across directory subtrees. | Deduplicate; point to canonical single-source asset or symlink. |
| **EFF_08** | `EFF_08_UNNORMALIZED_DATA_REPETITION` | `OPTIMIZATION` | BEJSON Tables | High-frequency string values repeated across rows (>40% of rows). | Normalize into relational parent entity using `_fk` UUID pointers. |

---

## 2. Inefficiency Remediation Matrix

### 2.1 EFF_03: Linear BEJSON Positional Indexing -> O(1) Field Map Caching
```python
# PROHIBITED (EFF_03 Inefficiency & Policy §6.2 Violation):
for row in bejson_doc["Values"]:
    name = row[0]   # Fragile, non-portable, and unindexed
    score = row[4]

# REMEDIATION:
field_map = {field["name"]: idx for idx, field in enumerate(bejson_doc["Fields"])}
for row in bejson_doc["Values"]:
    name = row[field_map["name"]]
    score = row[field_map["score"]]
```

### 2.2 EFF_04: Redundant I/O Churn -> Single-Pass Atomic Persistence
```python
# PROHIBITED (EFF_04 Redundant I/O Churn):
for record in incoming_records:
    with open("data.json", "w") as f:
        json.dump(record, f)  # Repeated fsync thrashing

# REMEDIATION:
# Ingest all records in-memory, then write once atomically:
atomic_write_bejson(target_path, compiled_dataset)
```

### 2.3 EFF_05: Subprocess Thrashing in Loops -> Single Batch Processing
```bash
# PROHIBITED (EFF_05 Subprocess Thrashing):
while IFS= read -r item; do
    parsed=$(echo "$item" | jq -r '.field')  # Spawns new jq subshell per line
done < input.jsonl

# REMEDIATION:
jq -r '.field' input.jsonl | while IFS= read -r parsed; do
    # Process stream directly
done
```

---

## 3. Exit Code Contracts

- **`0`**: Clean (zero critical/warning inefficiencies detected).
- **`1`**: Findings present (warnings or critical efficiency bottlenecks identified).
- **`10`**: Path error (specified audit target not found).
- **`20`**: Environment error (missing runtime binaries or environment definitions).
- **`30`**: Schema / AST parse error during scan.
