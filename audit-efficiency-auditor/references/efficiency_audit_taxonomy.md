# Efficiency & Redundancy Audit Taxonomy (Layer 2)

- **Version**: `1.1.0`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Verification Gate & Invariant Auditing)`
- **Binding**: `Policy §6.2, §10.6, §10.9, §12.1`
- **RELATIONAL_ID**: `6551d445-c9fd-4854-bd73-3d19f0756255`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Multi-Pass Execution Lifecycle

The efficiency auditor rejects hasty single-pass scans, enforcing a deliberate multi-pass evaluation model with intentional pacing to ensure thorough discovery and cross-correlation:

```
Pass 1: Discovery & Inventory       ──► Pacing Pause ──► Pass 2: Deep Flow & Correlation ──► Pacing Pause ──► Pass 3: Invariant Synthesis
- File & Asset Fingerprinting (EFF_07)  (0.5s - 1.0s)    - Dead Code Detection (EFF_01)         (0.5s - 1.0s)    - False-Positive Filtering
- Python AST & Symbol Cataloging                         - Duplicate Function Bodies (EFF_02)                    - Cross-Pass Convergence
- Line Budget Verification (EFF_06)                      - Linear BEJSON Lookups (EFF_03)                        - Actionable Remediation
                                                         - Loop I/O & Subprocesses (EFF_04, EFF_05)
                                                         - Unnormalized Redundancy (EFF_08)
```

### 1.1 Pass 1: Surface Discovery & AST Inventory
1. Sweeps target filesystem trees, catalogs all source files (`.py`, `.sh`, `.bejson`, `.md`), and computes SHA-256 binary digests.
2. Parses Python ASTs to register global function names, class definitions, and imported identifiers.
3. Audits documentation files (`SKILL.md`) for line budget ceiling violations exceeding 500 lines (`EFF_06`).

### 1.2 Pass 2: Deep Algorithmic Flow & Cross-Reference Audit
1. Re-evaluates target files against the synthesized global symbol registry from Pass 1.
2. Identifies unreferenced private helper routines (`EFF_01`) that have zero callers across the codebase.
3. Compares function AST unparsed bodies (>80 chars) to flag copy-pasted implementations (`EFF_02`).
4. Probes for direct `row[i]` indexing without $O(1)$ `field_map` cache in Python (`EFF_03`).
5. Evaluates loop bodies in Python and Bash for loop-nested I/O (`EFF_04`) and repetitive subprocess invocations (`EFF_05`).
6. Inspects BEJSON tables for unnormalized repetitive string payloads exceeding 40% column frequency (`EFF_08`).

### 1.3 Pass 3+: Verification, Convergence & Invariant Synthesis
1. Cross-validates candidate findings against architectural exclusion contracts (e.g. CLI entry points, standard visitor handlers).
2. Verifies line numbers and calculates audit stability convergence across passes.
3. Compiles final deterministic reports in Markdown or BEJSON 104a formats.

---

## 2. Diagnostic Code Specification

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

## 3. Inefficiency Remediation Matrix

### 3.1 EFF_03: Linear BEJSON Positional Indexing -> O(1) Field Map Caching
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

### 3.2 EFF_04: Redundant I/O Churn -> Single-Pass Atomic Persistence
```python
# PROHIBITED (EFF_04 Redundant I/O Churn):
for record in incoming_records:
    with open("data.json", "w") as f:
        json.dump(record, f)  # Repeated fsync thrashing

# REMEDIATION:
# Ingest all records in-memory, then write once atomically:
atomic_write_bejson(target_path, compiled_dataset)
```

### 3.3 EFF_05: Subprocess Thrashing in Loops -> Single Batch Processing
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

## 4. Exit Code Contracts

- **`0`**: Clean (zero critical/warning inefficiencies detected across all passes).
- **`1`**: Findings present (warnings or critical efficiency bottlenecks identified).
- **`10`**: Path error (specified audit target not found).
- **`20`**: Environment error (missing runtime binaries or environment definitions).
- **`30`**: Schema / AST parse error during scan.
