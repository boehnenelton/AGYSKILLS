---
name: log-compliance-auditor
description: >-
  Audit daily global log sinks ($GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson) to verify
  strict compliance with Policy §2.3 Post-Task Standardized Logging. Confirms that
  recent task completions, job runs, and repository deliveries possess corresponding
  structured log entries with complete JSON --context payloads, valid log levels,
  and automated redaction placeholders for sensitive operations. Use when verifying
  session logging compliance, auditing daily log sinks for missing task entries,
  validating logging tool invocation payloads, or running post-session telemetry
  audits. Do NOT use for managing log rotations and dual-path secure sinks (use
  log-telemetry-coordinator), calculating historical KPI metrics (use
  log-analytics-decomposer), auditing task goal omissions (use
  audit-deviation-auditor), or scanning credentials in code (use
  policy-secrets-leak-auditor).
---

# Skill: `log-compliance-auditor` (Layer 2 Policy §2.3 Logging Verification Gate)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §2.3 (Post-Task Global Standardized Logging Protocol)`
- **Embedded Tool**: [`scripts/log_compliance_tool.py`](./scripts/log_compliance_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

Under Policy §2.3, every completed development task, job execution, script refactoring, or tool delivery MUST be recorded in the daily global log partition at `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson`.

`log-compliance-auditor` acts as the verification gatekeeper, ensuring that:
1. Every completed action has a logged entry in the authoritative daily sink.
2. Every entry includes a valid JSON `--context` dictionary specifying task status and modified files.
3. Sensitive actions route to `$GLOBAL_LOGS_SECURE/Log-<YYYY-MM-DD>-secure.bejson` while maintaining an automated `[redacted: secure entry]` row in the public daily log.

---

## 2. Three-Stage Log Verification Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest       | --> | Stage 2: Audit Entry  |
| Daily Log Sink        |     | Schema & Context      |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Correlate    |
| Compliance Report     |     | Commits & Task States |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Sink Ingestion)**: Reads the current UTC partition `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson`.
2. **Stage 2 (Schema & Context Audit)**: Validates BEJSON field map caching, log level, and JSON `--context` payload validity.
3. **Stage 3 (Correlation)**: Cross-references recent git commits and completed tasks against logged records to catch unlogged work.
4. **Stage 4 (Report)**: Emits a structured compliance summary to `reports/audits/log_compliance_${TIMESTAMP}.md`.

---

## 3. Standard Compliance Report Schema

```markdown
# Logging Compliance Audit Report

- **Target Log Sink**: `/storage/emulated/0/Admin/System/Global_Logs/Log-2026-11-02.bejson`
- **Audit Timestamp**: `2026-11-02T01:30:00Z`
- **Compliance Status**: `COMPLIANT` (18 entries verified)

## Verification Highlights
- Context Payload Completeness: `100%` (18/18 entries possess valid JSON context)
- Redaction Integrity: `1 secure entry properly masked`
- Correlation: `All recent git commits match recorded log tokens`
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to audit logging compliance, always mandate `--sandbox` containment and deterministic exit codes (`0` = Fully Compliant, `10` = Path Failure, `20` = Env Failure, `30` = Logging Violations Detected):

```bash
python3 scripts/log_compliance_tool.py --date "today" --report
```

---

## When NOT to Use

Do NOT use `log-compliance-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Managing daily log rotations and secure partition routing**: Redirect immediately to `log-telemetry-coordinator`.
- **Calculating historical velocity and error frequency analytics**: Redirect immediately to `log-analytics-decomposer`.
- **Auditing task deliverables against declared session goals**: Redirect immediately to `audit-deviation-auditor`.
- **Auditing raw secrets and credentials in code prior to release**: Redirect immediately to `policy-secrets-leak-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
