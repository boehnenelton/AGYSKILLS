---
name: audit-readiness-auditor
description: >-
  Audit target systems, projects, and execution roadmaps for pre-flight structural
  readiness and dependency chain completeness. Verifies physical existence of required
  scripts, config/config.json defaults, environment stores (definitions.json), schema
  registries, and execution permissions (chmod +x) prior to running tasks or multi-step
  jobs. Use when verifying environment readiness before executing roadmaps, auditing
  prerequisite toolchains and file dependencies, validating input data files prior to
  batch processing, or conducting pre-flight staging audits. Do NOT use for auditing
  negative constraint breaches (use audit-constraint-auditor), retrospective goal
  deviations (use audit-deviation-auditor), scanning API token leaks (use
  policy-secrets-leak-auditor), real-time tool execution blocking (use
  goal-drift-auditor), or dispatching multi-audit pipelines (use
  audit-domain-coordinator).
---

# Skill: `audit-readiness-auditor` (Layer 2 Pre-Flight Structural & Dependency Readiness Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §4.4 (Script Configuration), Policy §4.5 (Environment Sourcing Standards)`
- **Embedded Tool**: [`scripts/audit_readiness_tool.py`](./scripts/audit_readiness_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

Before executing a complex roadmap, multi-stage refactoring plan, or autonomous job, systems frequently fail midway due to missing dependencies, unexecutable scripts (`permission denied`), or missing configuration defaults.

`audit-readiness-auditor` serves as the **Pre-Flight Structural Stage Gate**. It inspects the target workspace and verifies that the complete dependency chain is satisfied *before* any operational mutations begin.

---

## 2. Four-Stage Structural Readiness Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest Plan  | --> | Stage 2: Audit File   |
| & Prerequisites       |     | System Dependencies   |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Emit Go /    | <-- | Stage 3: Validate     |
| No-Go Readiness Gate  |     | Executable Perms & Data|
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Prerequisite Ingestion)**: Parses declared required files from project configs, execution roadmaps, or scripts.
2. **Stage 2 (Filesystem Dependency Sweep)**:
   - Verifies existence of `config/config.json` defaults (Policy §4.4).
   - Verifies access to canonical environment stores (`/storage/emulated/0/.env/user/definitions.json`).
   - Checks presence of required subdirectories (`lib/`, `config/`, `data/`, `exports/`, `dev/`, `docs/`).
3. **Stage 3 (Permissions & Data Pre-Validation)**:
   - Validates that executable scripts possess POSIX execute permissions (`chmod +x`).
   - Verifies that input BEJSON/JSON configuration documents parse without syntax errors.
4. **Stage 4 (Readiness Gate)**: Emits a structured Go / No-Go decision with missing dependencies enumerated.

---

## 3. Standard Readiness Report Schema

```markdown
# Structural Readiness Audit Report

- **Target System**: `/path/to/project`
- **Audit Timestamp**: `2026-11-02T01:30:00Z`
- **Readiness Decision**: `NO_GO` (2 prerequisite failures)

## Missing Prerequisites & Blockers
1. **[MISSING_DEPENDENCY]**: Required configuration file `config/config.json` does not exist.
2. **[PERMISSION_DENIED]**: Entrypoint `scripts/run.sh` lacks execute permission (`chmod +x`).

## Pre-Flight Remediation Actions
- [ ] Action 1: Bootstrap default `config/config.json` via Policy §4.4.
- [ ] Action 2: Execute `chmod +x scripts/run.sh`.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to execute readiness audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = Ready / Go, `10` = Path Failure, `20` = Env Failure, `30` = Unready / Missing Prerequisites):

```bash
python3 scripts/audit_readiness_tool.py --target "." --report
```

---

## When NOT to Use

Do NOT use `audit-readiness-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing negative constraint breaches and forbidden path touches**: Redirect immediately to `audit-constraint-auditor`.
- **Auditing retrospective goal deviations after execution**: Redirect immediately to `audit-deviation-auditor`.
- **Scanning files and logs for unmasked API credentials**: Redirect immediately to `policy-secrets-leak-auditor`.
- **Real-time execution blocking with interactive override gateways**: Redirect immediately to `goal-drift-auditor`.
- **Multi-phase audit workflow orchestration**: Redirect immediately to `audit-domain-coordinator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
