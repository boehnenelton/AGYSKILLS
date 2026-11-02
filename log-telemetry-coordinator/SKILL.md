---
name: log-telemetry-coordinator
description: >-
  Orchestrate and maintain the authoritative global logging and telemetry
  infrastructure across $GLOBAL_LOGS/, $GLOBAL_LOGS_SECURE/, and $GLOBAL_LOGS_ARCHIVES/.
  Manages daily UTC partition rotations (Log-<YYYY-MM-DD>.bejson), dual-path secure
  routing with automated redaction placeholders, archival retention policies, and
  log indexing per Policy §2.3. Use when managing daily log partition lifecycle,
  routing sensitive operational tokens to secure sinks, enforcing log retention,
  or orchestrating ecosystem-wide telemetry pipelines. Do NOT use for validating
  single-task logging policy compliance (use log-compliance-auditor), decomposing
  historical logs into KPI charts (use log-analytics-decomposer), managing urgent
  job queues (use job-lifecycle-coordinator), or general goal dispatching (use
  domain-scoped-coordinators).
---

# Skill: `log-telemetry-coordinator` (Layer 6 Global Logging & Dual-Path Telemetry Orchestrator)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 6 (System Orchestration, Governance & Multi-Agent Pipelines)`
- **Policy Anchor**: `Policy §2.3 (Post-Task Global Standardized Logging Protocol), Announcement October 31, 2026`
- **Embedded Tool**: [`scripts/log_telemetry_tool.py`](./scripts/log_telemetry_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`log-telemetry-coordinator` is the authoritative orchestrator for Elton Boehnen's global logging architecture. Under the **October 31, 2026 Standards Announcement**, logging is partitioned globally under `$GLOBAL_LOGS/` with strict daily UTC rotation (`Log-<YYYY-MM-DD>.bejson`) and isolated secure sinks (`$GLOBAL_LOGS_SECURE/Log-<YYYY-MM-DD>-secure.bejson`).

This skill coordinates:
1. **Management Tool & Subsystem Routing**: Integrates with the master management tool router at `$ADMIN_SYSTEM_TOOLS/management_tool/management_tool.py` routing between Mode 1 (Stateful Logging) and Mode 2 (Research Reports Tracking & Indexing).
2. **Stateful Loaded Chamber Telemetry**: Operates the stateful context engine (`lib_bejson_Standards_state.py`) allowing agents and daemons to load session context once (`subsystem`, `category`, `actor`, `session`, `flags`) and emit minimal, zero-friction log entries.
3. **Daily Partition Initialization**: Bootstraps compliant BEJSON 104a log envelopes at UTC midnight rollover.
4. **Dual-Path Secure Telemetry**: Routes secret modifications to secure sinks while maintaining automated redacted placeholder rows in public sinks.
5. **Archival Retention**: Automates movement of logs older than 30 days to `$GLOBAL_LOGS_ARCHIVES/`.
6. **Log Indexing**: Maintains an O(1) index of log dates and entries for fast ecosystem query resolution.

---

## 2. Four-Stage Telemetry Coordination Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Inspect Sink | --> | Stage 2: Initialize   |
| Status & UTC Rollover |     | Daily BEJSON Envelope |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Archive Stale| <-- | Stage 3: Reconcile    |
| Logs (>30 days)       |     | Dual-Path Partitions  |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Inspection)**: Inspects `$GLOBAL_LOGS/` to ensure current UTC partition exists.
2. **Stage 2 (Initialization)**: Bootstraps `Log-<YYYY-MM-DD>.bejson` with canonical 104a schema headers if absent.
3. **Stage 3 (Partition Reconciliation)**: Validates alignment between public and secure logs, verifying automated redaction placeholders.
4. **Stage 4 (Archival Retention)**: Sweeps logs older than 30 days, compresses, and moves to `$GLOBAL_LOGS_ARCHIVES/`.

---

## 3. Standard Coordinator Telemetry Report

```markdown
# Global Log Infrastructure Status Report

- **Inspection Timestamp**: `2026-11-02T01:30:00Z`
- **Current Active Sink**: `$GLOBAL_LOGS/Log-2026-11-02.bejson`
- **Secure Sink Status**: `ONLINE` (`Log-2026-11-02-secure.bejson`)

## Operational Health
- Daily Partition: `INITIALIZED` (104a envelope confirmed)
- Dual-Path Routing: `ACTIVE` (1 secure entry redacted in public sink)
- Retention Status: `0 files eligible for archive`
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to orchestrate logging infrastructure, always mandate `--sandbox` containment and deterministic exit codes (`0` = Fully Operational, `10` = Path Failure, `20` = Env Failure, `30` = Sink Anomalies Detected):

```bash
python3 scripts/log_telemetry_tool.py --status --report
```

---

## When NOT to Use

Do NOT use `log-telemetry-coordinator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing task logging policy compliance and context payloads**: Redirect immediately to `log-compliance-auditor`.
- **Decomposing historical daily logs into KPI analytics**: Redirect immediately to `log-analytics-decomposer`.
- **Autonomous JobMaker queue and urgent job sweeps**: Redirect immediately to `job-lifecycle-coordinator`.
- **General multi-domain goal execution pipelines**: Redirect immediately to `domain-scoped-coordinators`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
