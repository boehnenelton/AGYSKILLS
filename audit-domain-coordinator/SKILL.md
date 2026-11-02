---
name: audit-domain-coordinator
description: >-
  Orchestrate and dispatch multi-phase audit pipelines across repositories,
  skill suites, and staging workspaces. Analyzes audit targets, maps required
  stage gates, and sequences execution across pre-flight readiness
  (audit-readiness-auditor), negative boundary defense (audit-constraint-auditor),
  goal deviation checks (audit-deviation-auditor), and structural optimization
  (audit-gap-planner, audit-redundancy-planner). Emits unified Executive Audit
  Dossiers with consolidated checklists. Use when planning end-to-end repository
  audits, dispatching multi-stage quality gates, conducting pre-release
  certification, or coordinating multi-auditor workflows. Do NOT use for single
  readiness checks (use audit-readiness-auditor), single constraint sweeps (use
  audit-constraint-auditor), single deviation audits (use audit-deviation-auditor),
  or general goal dispatching (use domain-scoped-coordinators).
---

# Skill: `audit-domain-coordinator` (Layer 6 Audit Domain Orchestration & Cartography)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 6 (System Orchestration, Governance & Multi-Agent Pipelines)`
- **Policy Anchor**: `Policy §2.3 (Post-Task Standardized Logging), Policy §7.1 (Surgical Execution)`
- **Embedded Tool**: [`scripts/audit_domain_dispatcher.py`](./scripts/audit_domain_dispatcher.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`audit-domain-coordinator` is the master orchestrator, cartographer, and dispatcher for the entire audit ecosystem. Rather than requiring developers or autonomous agents to manually remember and invoke seven distinct auditing tools, the coordinator analyzes the target subject, builds an execution DAG, sequences the audit tools in strict dependency order, and synthesizes an authoritative **Executive Audit Dossier**.

---

## 2. The 4-Phase Multi-Auditor Orchestration Pipeline

```text
+-------------------------------------------------------------+
| Phase 1: Pre-Flight Readiness & Credential Safety           |
| -> audit-readiness-auditor & policy-secrets-leak-auditor    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 2: Negative Boundary & Invariant Defense              |
| -> audit-constraint-auditor & policy-bejson-auditor         |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 3: Goal Deviation & Execution Reconciliation          |
| -> audit-deviation-auditor & goal-drift-auditor             |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 4: Structural Gap & Code Optimization                 |
| -> audit-gap-planner, audit-redundancy-planner, efficiency   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Finalization: Unified Executive Audit Dossier               |
| -> Emitted to reports/audits/executive_audit_dossier_*.md   |
+-------------------------------------------------------------+
```

1. **Phase 1 (Pre-Flight Readiness)**: Blocks execution if prerequisites, scripts, permissions, or secret safety (`ENV:<var>`) fail.
2. **Phase 2 (Negative Boundaries)**: Verifies that immutable libraries (`$ADMIN_LIBRARIES`) and policies were untouched, and rule files contain negative constraints.
3. **Phase 3 (Goal Deviation)**: Reconciles declared tasks against physical filesystem artifacts and exit codes.
4. **Phase 4 (Optimization & Redundancy)**: Identifies structural blind spots, multi-language port gaps, and duplicated code routines.

---

## 3. Executive Audit Dossier Schema

```markdown
# Executive Audit Dossier

- **Target System**: `/path/to/project`
- **Orchestration Timestamp**: `2026-11-02T01:30:00Z`
- **Overall Certification Status**: `PASS_WITH_REMEDIATIONS`

## Phase Summaries
| Phase | Stage Gate | Status | Findings Count |
| :--- | :--- | :---: | :---: |
| Phase 1 | Readiness & Secrets | PASSED | 0 |
| Phase 2 | Negative Constraints | PASSED | 0 |
| Phase 3 | Goal Deviation | ATTENTION | 1 omission |
| Phase 4 | Gaps & Redundancies | ADVISORY | 2 gaps, 0 redundancies |

## Consolidated Remediation Action Plan
- [ ] High Priority: Scaffold missing `tests/test_api.py` (Phase 3).
- [ ] Medium Priority: Implement TypeScript port in `src/ts/` (Phase 4).
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to run full coordinated audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = Full Certification Pass, `10` = Path Failure, `20` = Env Failure, `30` = Remediations Required):

```bash
python3 scripts/audit_domain_dispatcher.py --target "." --all-phases --report
```

---

## When NOT to Use

Do NOT use `audit-domain-coordinator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Executing a single pre-flight readiness check**: Redirect immediately to `audit-readiness-auditor`.
- **Executing a single negative constraint breach audit**: Redirect immediately to `audit-constraint-auditor`.
- **Executing a single retrospective goal deviation check**: Redirect immediately to `audit-deviation-auditor`.
- **Executing a single structural gap analysis**: Redirect immediately to `audit-gap-planner`.
- **Executing a single code duplication scan**: Redirect immediately to `audit-redundancy-planner`.
- **General multi-phase goal delivery pipelines**: Redirect immediately to `domain-scoped-coordinators`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
