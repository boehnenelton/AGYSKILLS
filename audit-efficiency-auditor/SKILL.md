---
name: audit-efficiency-auditor
description: >-
  Audit codebases, scripts, BEJSON stores, and skill bundles for computational inefficiency, duplicate routines, dead code, redundant I/O passes, subprocess thrashing, and unnormalized storage bloat using deliberate multi-pass probe_efficiency.py sweeps. Use when probing specified systems for performance bottlenecks, redundant logic, loop I/O churn, duplicate functions, dead code, or context bloat across multiple deliberate review passes. Do NOT use for static AST BEJSON policy compliance auditing (use policy-bejson-auditor), black-box schema structural validation (use bejson-104-validator or bejson-105-validator), skill routing topology auditing (use skill-ecosystem-cartographer), or general application code restructuring (use arch-layered-refactor).
---

# audit-efficiency-auditor (Layer 2 Verification & System Efficiency Probe)

## Summary

`audit-efficiency-auditor` is the canonical **Layer 2 Verification & Audit Gate** for systematically probing codebases, shell workflows, data persistence stores, and skill bundles for computational inefficiency and structural redundancy. Rather than executing hasty, single-pass glances, it **takes its time and conducts multiple deliberate passes** over the target system to correlate cross-module call graphs, verify invariant stability, eliminate transient false positives, and validate deep algorithmic efficiency.

## When to Use

- Probing a user-specified project, repository, directory, or script for algorithmic or execution inefficiencies using deliberate multi-pass analysis.
- Scanning Python and Bash codebases across multiple passes for dead helper routines (`EFF_01`), duplicate function bodies (`EFF_02`), and subprocess loop thrashing (`EFF_05`).
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

## 1. Architectural Scope & Multi-Pass Invariants

- **Assigned Skill Tier**: `Layer 2 (Verification Gate & Invariant Auditing)`
- **Codebase Layer Mapping**: `L1_Validation / L2_Verification`
- **Allowed Downward Dependencies**: `L1 only` (`bejson-104-core`, `bejson-sanitization-core`). Zero UI, HTTP, or CLI transport logic.
- **Multi-Pass Methodology**: Mandatory phased execution with deliberate pacing between passes:
  - **Pass 1 (Surface Discovery & AST Inventory)**: Discovers all target files, computes SHA-256 asset digests, parses AST structures, and builds the global symbol and reference catalog.
  - **Pass 2 (Deep Algorithmic Flow & Cross-Reference Audit)**: Cross-references call graphs to detect dead code (`EFF_01`), compares function AST bodies (`EFF_02`), audits unindexed BEJSON access (`EFF_03`), and flags loop I/O or subprocess thrashing (`EFF_04`, `EFF_05`).
  - **Pass 3+ (Verification, Convergence & Synthesis)**: Validates stability of candidate findings, verifies exclusion contracts (framework hooks, standard visitors), and synthesizes actionable remediation roadmaps.
- **Reference Taxonomy**: [`references/efficiency_audit_taxonomy.md`](./references/efficiency_audit_taxonomy.md)
- **Probing Contracts**: [`references/probe_contracts_spec.md`](./references/probe_contracts_spec.md)
- **Primary CLI Probe**: [`scripts/probe_efficiency.py`](./scripts/probe_efficiency.py)

---

## 2. Inefficiency Diagnostic Code Matrix

Every multi-pass scan evaluates the target against eight standardized diagnostic codes:

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

## 3. Multi-Pass Execution & CLI Probe Workflows

Execute the black-box efficiency probe using [`scripts/probe_efficiency.py`](./scripts/probe_efficiency.py):

### 3.1 Standard Multi-Pass Audit (2 Deliberate Passes, Auto-Generates `efficiency_report.md`)
```bash
# Conducts 2 deliberate passes with 0.5s pacing delay, writing efficiency_report.md to target root:
python3 scripts/probe_efficiency.py /path/to/target_system
```

### 3.2 Deep Deliberate Multi-Pass Sweep (3 Passes with Extended Pacing)
```bash
# Conducts 3 passes with a 1.0s deliberate pacing pause to ensure thorough cross-reference synthesis:
python3 scripts/probe_efficiency.py /path/to/target_system --passes 3 --delay 1.0
```

### 3.3 Machine-Readable BEJSON 104a Telemetry Export
```bash
python3 scripts/probe_efficiency.py /path/to/target_system --format bejson --output reports/efficiency_audit.104a.bejson
```

### 3.4 CI/Stage-Gate Strict Verification
```bash
# Returns Exit Code 1 if any CRITICAL or WARNING inefficiencies remain across passes:
python3 scripts/probe_efficiency.py /path/to/target_system --exit-on-warn
```

---

## 4. Subagent Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents from `audit-efficiency-auditor`, always enforce headless `--sandbox` containment, multi-pass pacing, and deterministic exit codes:

```bash
agy --sandbox -p "Execute deliberate multi-pass audit-efficiency-auditor probe on target directory across 2-3 passes and return structured findings table."
```

### Deterministic Exit Codes
- **`0`**: Clean completion; system meets all efficiency and deduplication invariants across all passes.
- **`1`**: Findings identified (warnings or critical performance bottlenecks present).
- **`10`**: Path error (specified audit target does not exist).
- **`20`**: Environment error (missing runtime binaries or environment variables).
- **`30`**: Schema / AST parse error during probe execution.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
