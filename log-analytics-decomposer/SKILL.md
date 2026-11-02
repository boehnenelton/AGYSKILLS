---
name: log-analytics-decomposer
description: >-
  Parse, aggregate, and decompose historical daily BEJSON log partitions
  ($GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson) into structured KPI analytics, error
  frequency distributions, subsystem velocity telemetry, and developer productivity
  summaries. Emits Markdown telemetry dashboards and time-series reports. Use when
  analyzing system error rates, extracting development velocity trends over time,
  auditing subsystem execution distributions, or visualizing daily log trends. Do
  NOT use for auditing individual task logging policy compliance (use
  log-compliance-auditor), managing daily log partition rotation (use
  log-telemetry-coordinator), reverse-engineering web navigation trees (use
  ui-navigation-decomposer), or loop I/O profiling (use audit-efficiency-auditor).
---

# Skill: `log-analytics-decomposer` (Layer 4 BEJSON Daily Log Analytics & Telemetry Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (Spatial Decomposition & UI/Data Mapping)`
- **Policy Anchor**: `Policy §2.3 (Post-Task Standardized Logging), Announcement October 31, 2026`
- **Embedded Tool**: [`scripts/log_analytics_tool.py`](./scripts/log_analytics_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

As an ecosystem operates across days and weeks, `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson` accumulates rich operational telemetry. `log-analytics-decomposer` ingests single-day or multi-day partitioned BEJSON logs and decomposes them into high-level intelligence:
1. **Subsystem Activity**: Which domains (`skills`, `job`, `mfdb`, `behtml`) are consuming the most operational cycles.
2. **Error Code Distribution**: Frequencies of operational warnings, invariant breaches (E10-E95), and syntax errors.
3. **Execution Velocity**: Task completions per hour, mean turnaround times, and delivery frequencies.
4. **Markdown Telemetry Dashboards**: Generates formatted dashboards ready for review.

---

## 2. Four-Stage Log Decomposition Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest Range | --> | Stage 2: Aggregate    |
| of Daily .bejson Logs |     | Subsystems & Levels   |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Correlate    |
| Markdown KPI Report   |     | Error Codes & Trends  |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Range Ingestion)**: Ingests one or more daily logs matching a date window (e.g. past 7 days).
2. **Stage 2 (Aggregation)**: Counts entries by log level (`INFO`, `WARN`, `ERROR`), category token, and subsystem.
3. **Stage 3 (Error Correlation)**: Extracts error tokens and codes to isolate recurring failure points.
4. **Stage 4 (KPI Dashboard)**: Emits a structured telemetry report to `reports/analytics/log_analytics_${TIMESTAMP}.md`.

---

## 3. Standard Analytics Output Schema

```markdown
# Ecosystem Telemetry & KPI Report

- **Date Range**: `2026-10-25` to `2026-11-02` (9 daily sinks)
- **Total Entries Analyzed**: `342`
- **System Health Ratio**: `98.2%` (336 INFO, 4 WARN, 2 ERROR)

## Subsystem Activity Breakdown
| Subsystem | Entry Count | Share |
| :--- | :---: | :---: |
| `skills.audit_domain` | 142 | 41.5% |
| `job.lifecycle` | 98 | 28.7% |
| `mfdb.engine` | 64 | 18.7% |
| `behtml.layout` | 38 | 11.1% |

## Error Frequency Summary
- None detected in target window.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to generate log analytics, always mandate `--sandbox` containment and deterministic exit codes (`0` = Analytics Generated, `10` = Path Failure, `20` = Env Failure, `30` = Log Ingestion Error):

```bash
python3 scripts/log_analytics_tool.py --days 7 --report
```

---

## When NOT to Use

Do NOT use `log-analytics-decomposer` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing individual task logging policy compliance**: Redirect immediately to `log-compliance-auditor`.
- **Managing daily log rotations and secure sink routing**: Redirect immediately to `log-telemetry-coordinator`.
- **Reverse-engineering web UI navigation trees**: Redirect immediately to `ui-navigation-decomposer`.
- **Measuring CPU, memory, and loop I/O efficiency**: Redirect immediately to `audit-efficiency-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
