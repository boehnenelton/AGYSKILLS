---
name: job-lifecycle-coordinator
description: >-
  Orchestrate the end-to-end autonomous lifecycle of JobMaker jobs across
  $JOBS_FOLDER, $COMPLETED_JOBS_FOLDER, and $JOB_LOGS_FOLDER. Dispatches
  conformance validation, sequences task-by-task execution via job-workflow-manager,
  verifies completion proofs, archives completed jobs, and writes structured daily
  audit logs per Policy §2.3. Use when sweeping $JOBS_FOLDER for pending jobs, running
  autonomous multi-task job queues, managing post-job archiving and log retention,
  or orchestrating JobMaker pipelines. Do NOT use for isolated single-file schema
  validation (use job-conformance-validator), composing new job blueprints (use
  job-template-composer), manual single-task stepping (use job-workflow-manager),
  or general goal dispatching (use domain-scoped-coordinators).
---

# Skill: `job-lifecycle-coordinator` (Layer 6 JobMaker Lifecycle & Archive Orchestrator)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 6 (System Orchestration, Governance & Multi-Agent Pipelines)`
- **Policy Anchor**: `Policy URGENT JOBS, Policy §2.3 (Post-Task Standardized Logging)`
- **Embedded Tool**: [`scripts/job_lifecycle_tool.py`](./scripts/job_lifecycle_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`job-lifecycle-coordinator` fulfills the central mandate of the system policy: **Urgent Job Lifecycle Automation**. When initialized or instructed, this coordinator sweeps `$JOBS_FOLDER`, validates pending JobMaker schemas, coordinates task execution step-by-step through `job-workflow-manager`, verifies deliverable artifacts, atomically moves completed jobs to `$COMPLETED_JOBS_FOLDER`, and writes structured logs to `$JOB_LOGS_FOLDER` and the global log sink.

---

## 2. The 5-Stage Job Lifecycle Pipeline

```text
+-------------------------------------------------------------+
| Stage 1: Sweep & Intake                                     |
| Ingest pending .bejson jobs in $JOBS_FOLDER                 |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Stage 2: Pre-Flight Conformance Gate                        |
| Validate schema invariants via job-conformance-validator    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Stage 3: Step-by-Step Task Dispatch                         |
| Execute tasks 1-by-1 in task_order via job-workflow-manager |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Stage 4: Verification & Completion Proof                    |
| Audit deliverable files on disk & update Job_Complete=true  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Stage 5: Atomic Archival & Global Logging                   |
| Move to $COMPLETED_JOBS_FOLDER & log to daily_log-*.md      |
+-------------------------------------------------------------+
```

1. **Stage 1 (Sweep)**: Scans `$JOBS_FOLDER` (`/storage/emulated/0/Admin/System/Job_Management/Jobs`).
2. **Stage 2 (Validation)**: Executes `job-conformance-validator` to ensure schema integrity before running.
3. **Stage 3 (Task Dispatch)**: Dispatches tasks sequentially, injecting `task_context` and prior outputs.
4. **Stage 4 (Proof Verification)**: Verifies physical file deliverables before marking tasks complete.
5. **Stage 5 (Archival & Log)**: Moves finished files to `$COMPLETED_JOBS_FOLDER` and commits structured logs.

---

## 3. Standard Lifecycle Output Schema

```markdown
# Job Lifecycle Execution Report

- **Job Name**: `migration_v2.bejson`
- **Execution Timestamp**: `2026-11-02T01:30:00Z`
- **Lifecycle Status**: `COMPLETED_AND_ARCHIVED`

## Execution Summary
1. Pre-Flight Validation: `PASSED` (0 errors)
2. Task Execution: `4/4 tasks completed`
3. Deliverable Verification: `All artifacts verified on disk`
4. Destination: Moved to `$COMPLETED_JOBS_FOLDER/migration_v2.bejson`
5. Telemetry Log: Appended to `$JOB_LOGS_FOLDER/daily_log-20261102.md`
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to orchestrate job queues, always mandate `--sandbox` containment and deterministic exit codes (`0` = All Jobs Completed, `10` = Path Failure, `20` = Env Failure, `30` = Job Failures Detected):

```bash
python3 scripts/job_lifecycle_tool.py --sweep --report
```

---

## When NOT to Use

Do NOT use `job-lifecycle-coordinator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Isolated single-file schema validation**: Redirect immediately to `job-conformance-validator`.
- **Composing new job blueprints or templates**: Redirect immediately to `job-template-composer`.
- **Manual single-task stepping without lifecycle management**: Redirect immediately to `job-workflow-manager`.
- **General multi-domain goal execution pipelines**: Redirect immediately to `domain-scoped-coordinators`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
