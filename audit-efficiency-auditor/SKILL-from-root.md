---
name: audit-efficiency-auditor
description: >-
  Audit codebases, scripts, BEJSON stores, and skill bundles for computational inefficiency, duplicate routines, dead code, redundant I/O passes, subprocess thrashing, and unnormalized storage bloat using probe_efficiency.py. Use when probing specified systems for performance bottlenecks, redundant logic, loop I/O churn, duplicate functions, or context bloat. Do NOT use for static AST BEJSON policy compliance auditing (use policy-bejson-auditor), black-box schema structural validation (use bejson-104-validator or bejson-105-validator), skill routing topology auditing (use skill-ecosystem-cartographer), or general application code restructuring (use arch-layered-refactor).
---

# audit-efficiency-auditor (Layer 2 Verification & System Efficiency Probe)

## Summary

`audit-efficiency-auditor` is the canonical **Layer 2 Verification & Audit Gate** for systematically probing codebases, shell workflows, data persistence stores, and skill bundles for computational inefficiency and structural redundancy. It enforces strict algorithmic efficiency, detects dead and duplicate logic, eliminates redundant I/O thrashing, flags subprocess loops, and audits context bloat across the ecosystem.

## When to Use

- Probing a user-specified project, repository, directory, or script for algorithmic or execution inefficiencies.
- Scanning Python and Bash codebases for duplicate function implementations, dead helper routines, and subprocess loop thrashing (`EFF_01`, `EFF_02`, `EFF_05`).
- Detecting prohibited direct positional BEJSON `row[i]` indexing without $O(1)$ `field_map` caching (`EFF_03`).
- Auditing loop constructs for repeated file opening or disk persistence writes (`EFF_04`).
- Checking skill manifests and prompts for token/line budget overruns exceeding 500 lines (`EFF_06`).
- Scanning filesystem trees for duplicate binary assets and unnormalized repetitive data payloads (`EFF_07`, `EFF_08`).

## When NOT to Use

- Do NOT use for auditing AST code for BEJSON field map policy compliance or 5-test suite execution (use `policy-bejson-auditor`).
- Do NOT use for validating structural integrity, field counts, or list trees of Foundational Era BEJSON files (use `bejson-104-validator`).
- Do NOT use for validating Format 105 UUID integrity, reserved offsets, or checksums (use `bejson-105-validator`).
- Do NOT use for mapping skill routing topologies, computing pairwise collision matrices, or registering installed skills (use `skill-ecosystem-cartographer`).
- Do NOT use for refactoring or decomposing monolithic codebases into class hierarchies (use `arch-layered-refactor`).

---

## 1. Architectural Scope & Downward Dependencies

- **Assigned Skill Tier**: `Layer 2 (Verification Gate & Invariant Auditing)`
- **Codebase Layer Mapping**: `L1_Validation / L2_Verification`
- **Allowed Downward Dependencies**: `L1 only` (`bejson-104-core`, `bejson-sanitization-core`). Zero UI, HTTP, or CLI transport logic.
- **Reference Taxonomy**: [`references/efficiency_audit_taxonomy.md`](./references/efficiency_audit_taxonomy.md)
- **Probing Contracts**: [`references/probe_contracts_spec.md`](./references/probe_contracts_spec.md)
- **Primary CLI Probe**: [`scripts/probe_efficiency.py`](./scripts/probe_efficiency.py)

---

## 2. Inefficiency Diagnostic Code Matrix

Every scan evaluates the system against eight standardized diagnostic codes:

| Code | Severity | Description | Remediation Protocol |
| :--- | :--- | :--- | :--- |
| **`EFF_01_DEAD_CODE`** | `WARNING` | Unreferenced helper functions or unimported dead code. | Move to `dev/dead_code.md` and prune from runtime. |
| **`EFF_02_DUPLICATE_CODE_BLOCKS`** | `WARNING` | Identical or near-identical function implementations duplicated across modules. | Consolidate into canonical shared `lib/` modules. |
| **`EFF_03_LINEAR_BEJSON_LOOKUP`** | `CRITICAL` | Direct `row[i]` positional indexing without $O(1)$ `field_map` cache (Policy §6.2). | Compile dynamic `field_map` and access columns by name. |
| **`EFF_04_REDUNDANT_IO_CHURN`** | `WARNING` | File read/write calls executed inside loops instead of batched in-memory. | Buffer changes in-memory; perform single atomic POSIX write. |
| **`EFF_05_SUBPROCESS_THRASHING`** | `CRITICAL` | Shell subprocess spawning (`jq`, `cat`, `curl`, `agy`) inside iterative loops. | Use single-pass streaming pipes or native library calls. |
| **`EFF_06_CONTEXT_PROMPT_BLOAT`** | `CRITICAL` | `SKILL.md` manifests exceeding the 500-line budget or verbose fluff copy. | Partition into `references/` via 3-Stage Progressive Disclosure. |
| **`EFF_07_DUPLICATE_ASSET_STORAGE`** | `OPTIMIZATION` | Duplicate file byte digests found across target trees. | Consolidate duplicate assets to single canonical location. |
| **`EFF_08_UNNORMALIZED_DATA_REPETITION`** | `OPTIMIZATION` | Repetitive string payloads in BEJSON values exceeding 40% frequency. | Normalize into relational parent entity with `_fk` foreign keys. |

---

## 3. Execution & CLI Probe Workflows

Execute the black-box efficiency probe using [`scripts/probe_efficiency.py`](./scripts/probe_efficiency.py):

### 3.1 Basic System Audit (Auto-Generates `efficiency_report.md`)
```bash
# Probes target, prints telemetry, and automatically writes efficiency_report.md to target root:
python3 scripts/probe_efficiency.py /path/to/target_system
```

### 3.2 Machine-Readable BEJSON 104a Telemetry Export
```bash
python3 scripts/probe_efficiency.py /path/to/target_system --format bejson --output reports/efficiency_audit.104a.bejson
```

### 3.3 CI/Stage-Gate Strict Verification
```bash
# Returns Exit Code 1 if any CRITICAL or WARNING inefficiencies are flagged:
python3 scripts/probe_efficiency.py /path/to/target_system --exit-on-warn
```

---

## 4. Subagent Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents from `audit-efficiency-auditor`, always enforce headless `--sandbox` containment and deterministic exit codes:

```bash
agy --sandbox -p "Execute audit-efficiency-auditor probe on target directory and return structured findings table."
```

### Deterministic Exit Codes
- **`0`**: Clean completion; system meets all efficiency and deduplication invariants.
- **`1`**: Findings identified (warnings or critical performance bottlenecks present).
- **`10`**: Path error (specified audit target does not exist).
- **`20`**: Environment error (missing runtime binaries or environment variables).
- **`30`**: Schema / AST parse error during probe execution.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
