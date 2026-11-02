---
name: audit-deviation-auditor
description: >-
  Audit systems, repositories, and active codebases against stated goals, user
  instructions, and policy directives extracted from AGENTS.md, GEMINI.md,
  instruction documents, and prompt context. Identifies goal deviations,
  forgotten negative constraints, unverified completion claims, and scope
  creep, synthesizing a structured, step-by-step course-correction plan in
  reports/audits/. Use when performing post-session or mid-project goal
  reconciliation, auditing system state against project specifications,
  verifying whether agent execution honored all constraints, or generating
  recovery plans. Do NOT use for real-time execution blocking with interactive
  user override gateways (use goal-drift-auditor), analyzing structural coverage
  blind spots and missing modules (use audit-gap-planner), detecting code and
  schema duplication (use audit-redundancy-planner), or runtime loop efficiency
  profiling (use audit-efficiency-auditor).
---

# Skill: `audit-deviation-auditor` (Layer 2 Goal Deviation & System Audit Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §7.2 (Goal-Driven Execution)`
- **Embedded Tool**: [`scripts/audit_deviation_tool.py`](./scripts/audit_deviation_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`audit-deviation-auditor` is the retrospective and mid-project diagnostic engine that inspects an entire codebase against its declared goals. Autonomous agents often drift across multi-turn sessions - skipping secondary requirements, forgetting negative boundaries, or declaring victory prematurely.

This skill extracts the authoritative intent from `AGENTS.md`, `GEMINI.md`, or project instructions, conducts an adversarial sweep across the physical filesystem, and generates an actionable **Course-Correction Plan**.

---

## 2. The Four-Stage Deviation Audit Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest       | --> | Stage 2: Inspect      |
| Authoritative Goals   |     | Physical State        |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Classify     |
| Course-Correction Plan|     | Discrepancies         |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Intent Ingestion)**: Parses stated goals, deliverables, and negative constraints from `AGENTS.md`, `GEMINI.md`, `dev/goal_contract.104a.bejson`, or session logs.
2. **Stage 2 (State Inspection)**: Analyzes `git status`, recent commits, modified files, exported documents, and test exit codes.
3. **Stage 3 (Discrepancy Classification)**:
   - *Omission*: A declared deliverable was not created.
   - *Breach*: An off-limits directory or file was altered.
   - *False Pass*: A task is marked done, but the verification command fails.
   - *Scope Creep*: Files were added or refactored with no basis in stated goals.
4. **Stage 4 (Plan Synthesis)**: Emits a structured Markdown remediation plan to `reports/audits/goal_deviation_audit_${TIMESTAMP}.md`.

---

## 3. Standard Audit Report & Course-Correction Plan Schema

Every audit output includes a standardized recovery plan:

```markdown
# Goal Deviation Audit Report

- **Target System**: `/path/to/project`
- **Audit Timestamp**: `2026-11-02T01:00:00Z`
- **Status**: `DEVIATIONS_DETECTED` (3 discrepancies found)

## Discovered Discrepancies
1. **[OMISSION]**: `tests/test_api.py` declared in goal contract was never created.
2. **[CONSTRAINT_BREACH]**: File `$ADMIN_LIBRARIES/Core/lib_core.py` was modified.
3. **[UNVERIFIED_STATUS]**: Unit tests fail with Exit Code 1.

## Course-Correction Remediation Plan
- [ ] Step 1: Revert unauthorized changes to `$ADMIN_LIBRARIES`.
- [ ] Step 2: Scaffold missing `tests/test_api.py`.
- [ ] Step 3: Fix broken assertion in `src/service.py` and run tests.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to execute goal deviation audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = Clean Pass, `10` = Path Failure, `20` = Env Failure, `30` = Deviations Detected):

```bash
python3 scripts/audit_deviation_tool.py --project "." --report
```

---

## When NOT to Use

Do NOT use `audit-deviation-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Real-time execution blocking during active tool calls**: Redirect immediately to `goal-drift-auditor`.
- **Auditing structural coverage gaps and missing language ports**: Redirect immediately to `audit-gap-planner`.
- **Auditing duplicate code and redundant skill triggers**: Redirect immediately to `audit-redundancy-planner`.
- **Measuring CPU, memory, and loop I/O efficiency**: Redirect immediately to `audit-efficiency-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
