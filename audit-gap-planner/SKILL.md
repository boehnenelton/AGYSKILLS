---
name: audit-gap-planner
description: >-
  Analyze target architectures, codebases, library ecosystems, and schema registries
  for structural gaps, coverage blind spots, missing multi-language ports, and
  unhandled edge-case invariants. Evaluates capability matrices against production
  requirements and synthesizes a phased, prioritized gap-closure plan in reports/audits/.
  Use when conducting architectural gap audits, identifying missing error codes or
  schema fields, finding untyped contracts or missing language implementations, or
  planning technical roadmap additions. Do NOT use for auditing deviations against
  stated session goal contracts (use audit-deviation-auditor), detecting code and
  schema duplication (use audit-redundancy-planner), real-time execution blocking
  with user override gateways (use goal-drift-auditor), or loop I/O efficiency
  audits (use audit-efficiency-auditor).
---

# Skill: `audit-gap-planner` (Layer 5 Structural Gap & Blind Spot Analysis Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (Composition, Planning & Refactoring)`
- **Policy Anchor**: `Policy §7.1 (Surgical Execution & Goal-Driven Design)`
- **Embedded Tool**: [`scripts/audit_gap_tool.py`](./scripts/audit_gap_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`audit-gap-planner` systematically analyzes a software ecosystem, library suite, or project directory to identify structural absences, unhandled edge cases, and missing capabilities. Where other tools look for deviations from active session goals or runtime bugs, `audit-gap-planner` asks: **What is missing that ought to exist for full architectural completeness?**

Key analysis dimensions:
1. **Multi-Language Port Parity**: Ensuring four-language parity (Python, JS, TS, Bash) across foundational primitives.
2. **Schema Invariant Coverage**: Detecting missing error codes, unhandled validation states, or absent primary/foreign keys.
3. **Operational Blind Spots**: Missing CLI flags (`--help`, `--version`, `--json`), lack of dry-run execution, or absent rollback mechanisms.
4. **Test & Verification Coverage**: Missing unit tests, unexercised error branches, or skipped lifecycle stages.

---

## 2. Four-Stage Structural Gap Analysis Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Map          | --> | Stage 2: Audit        |
| Target Topology       |     | Matrix Coverage       |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Score &      |
| Phased Closure Plan   |     | Prioritize Gaps       |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Topology Mapping)**: Catalogs all files, modules, classes, and exported functions across the target system.
2. **Stage 2 (Matrix Auditing)**: Compares mapped components against canonical capability checklists (multi-language ports, CRUD methods, error codes).
3. **Stage 3 (Gap Scoring & Prioritization)**:
   - *P0 (Blocker Gap)*: Missing fundamental integrity validation or core security checks.
   - *P1 (High Gap)*: Missing parity port in an actively supported language (e.g., Python exists, JS missing).
   - *P2 (Medium Gap)*: Missing utility CLI flag or diagnostic command.
   - *P3 (Low Gap)*: Missing cosmetic helper or documentation example.
4. **Stage 4 (Roadmap Synthesis)**: Generates a phased implementation plan output to `reports/audits/gap_analysis_${TIMESTAMP}.md`.

---

## 3. Standard Gap Audit Report Schema

```markdown
# Structural Gap Audit Report

- **Target System**: `/path/to/project`
- **Audit Timestamp**: `2026-11-02T01:00:00Z`
- **Gap Coverage Score**: `74.5%` (12 gaps identified)

## Identified Gaps by Priority
1. **[P0 - SCHEMA_GAP]**: Missing foreign key referential integrity validation in TS runtime.
2. **[P1 - PORT_GAP]**: `lib_bejson_upgrade` implemented in Python and JS, but missing in Bash.
3. **[P2 - CLI_GAP]**: `scripts/runner.py` missing standard `--json` machine-readable output flag.

## Phased Gap-Closure Roadmap
### Phase 1: High-Priority Integrity & Security
- [ ] Task 1.1: Implement TS referential check in `src/ts/validator.ts`.

### Phase 2: Language Parity & Tooling
- [ ] Task 2.1: Port upgrade engine to Bash in `lib/sh/lib_upgrade.sh`.
- [ ] Task 2.2: Add `--json` flag to `scripts/runner.py`.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to run structural gap audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = 100% Coverage, `10` = Path Failure, `20` = Env Failure, `30` = Gaps Identified):

```bash
python3 scripts/audit_gap_tool.py --target "." --report
```

---

## When NOT to Use

Do NOT use `audit-gap-planner` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing execution deviations against declared session goal contracts**: Redirect immediately to `audit-deviation-auditor`.
- **Auditing duplicate code, redundant files, and trigger overlap**: Redirect immediately to `audit-redundancy-planner`.
- **Real-time execution blocking during active tool calls**: Redirect immediately to `goal-drift-auditor`.
- **Measuring CPU, memory, and loop I/O efficiency**: Redirect immediately to `audit-efficiency-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
