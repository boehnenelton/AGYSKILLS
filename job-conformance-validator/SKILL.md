---
name: job-conformance-validator
description: >-
  Validate structural integrity, field map conformity, task ordering, and execution
  state invariants for Elton Boehnen's JobMaker BEJSON 104a Job and Template schemas.
  Enforces 11 canonical task fields, contiguous 1-indexed task_order, synthetic UUID
  validity, audit flags, and schema header declarations. Use when auditing job files
  in $JOBS_FOLDER, validating newly instantiated job templates before execution,
  verifying completion proofs before archiving, or diagnosing JobMaker 104a parse
  errors. Do NOT use for autonomous multi-job lifecycle orchestration and folder
  sweeps (use job-lifecycle-coordinator), composing new job blueprints from natural
  language (use job-template-composer), step-by-step task execution (use
  job-workflow-manager), or base BEJSON format validation (use bejson-104-validator).
---

# Skill: `job-conformance-validator` (Layer 2 JobMaker 104a Schema & Invariant Gate)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §6.2 (BEJSON Core Mandate), Policy §10.6 (Enforcement Test Suites)`
- **Embedded Tool**: [`scripts/job_conformance_tool.py`](./scripts/job_conformance_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`job-conformance-validator` is the authoritative structural validator and diagnostic engine for Elton Boehnen's **JobMaker BEJSON 104a Job Schema** and template specifications. Before any job is queued or executed, this gatekeeper verifies schema conformity, preventing runtime crashes caused by missing field headers, non-contiguous task orders, or malformed audit flags.

---

## 2. The JobMaker Invariant Hierarchy

```text
+-------------------------------------------------------------+
| Invariant 1: Top-Level Envelope & Headers                   |
| Format="BEJSON", Format_Version="104a", Records_Type=["JobTask"] |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Invariant 2: The 11 Canonical Task Fields                   |
| task_id, task_order, task_title, task_description,          |
| task_context, task_reference, task_mandatory, is_completed,  |
| audit_enabled, audit_passed, audit_fail_reason              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Invariant 3: Ordering & Relational Integrity                |
| Contiguous 1..N task_order, unique task_ids, boolean audits |
+-------------------------------------------------------------+
```

### Key Invariant Gates:
1. **Envelope Gate (E-JOB-01)**: Must declare `Format="BEJSON"`, `Format_Version="104a"`, `Records_Type=["JobTask"]`.
2. **Field Map Gate (E-JOB-02)**: Must define all 11 canonical task fields without positional drift.
3. **Ordering Gate (E-JOB-03)**: `task_order` values must form an unbroken sequence from `1` to `N`.
4. **Audit Flag Gate (E-JOB-04)**: If `audit_enabled` is true and `is_completed` is true, `audit_passed` must be a valid boolean.
5. **Completion Proof Gate (E-JOB-05)**: If `Job_Complete` is true, all mandatory tasks must have `is_completed=true` and `Completion_Date` must be populated.

---

## 3. Standard Validation Output Schema

```markdown
# Job Conformance Validation Report

- **Target Job File**: `jobs/migration_task.bejson`
- **Validation Timestamp**: `2026-11-02T01:30:00Z`
- **Conformance Status**: `VALIDATION_PASSED` (0 errors, 4 tasks verified)

## Task Invariant Summary
- Total Tasks: `4`
- Contiguous Sequence: `1..4` [OK]
- Field Map Cache: `11 fields mapped O(1)` [OK]
- Mandatory Tasks Complete: `4/4` [OK]
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to execute job validations, always mandate `--sandbox` containment and deterministic exit codes (`0` = Conforming Pass, `10` = Path Failure, `20` = Env Failure, `30` = Conformance Violations):

```bash
python3 scripts/job_conformance_tool.py --job "jobs/my_job.bejson" --report
```

---

## When NOT to Use

Do NOT use `job-conformance-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Autonomous multi-job lifecycle orchestration and folder sweeps**: Redirect immediately to `job-lifecycle-coordinator`.
- **Composing new job blueprints from natural language**: Redirect immediately to `job-template-composer`.
- **Step-by-step task execution**: Redirect immediately to `job-workflow-manager`.
- **Base raw BEJSON format validation**: Redirect immediately to `bejson-104-validator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
